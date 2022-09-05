import threading
import logging
import time
import yaml
import re
from typing import Optional, Union, Dict
from typing import Dict , Any

from ehforwarderbot import Middleware, Message, Status, coordinator, utils, MsgType
from ehforwarderbot.types import ModuleID, MessageID, InstanceID, ChatID
from ehforwarderbot.chat import Chat, SystemChat, GroupChat, ChatNotificationState
from ehforwarderbot.message import MsgType, MessageCommands, MessageCommand, Substitutions
from ehforwarderbot import utils as efb_utils


class MessageMergeMiddleware(Middleware):
    """
    """
    middleware_id: ModuleID = ModuleID("QQ_War.message_merge")
    middleware_name: str = "Message Merge Middleware"
    __version__: str = '0.1.0'
    logger: logging.Logger = logging.getLogger(
        "plugins.%s.MessageMergeMiddleware" % middleware_id)

    
    def __init__(self, instance_id: Optional[InstanceID] = None):
        
        super().__init__(instance_id)

        config_path = efb_utils.get_config_path(self.middleware_id)
        self.config = self.load_config(config_path)
        self.mastersendback = self.config.get("mastersendback", True)
        self.samemessagegroupconfig = self.config.get('samemessagegroup', [])
        self.samemessageprivateconfig = self.config.get('samemessageprivate',[])
        self.messagekeeptime = self.config.get('messagekeeptime', 5)

        self.mastersendoutmessagecache = list()
        """ 
            [message1, message2,...]
        """
        self.smmgroupcache = {}
        self.smmprivatecache = {}
        """
            [samemessage:{
                "[group_id]":
                    {
                        time: "1234567890",
                        members: {name1:1, name2:3}
                        uid: "8908ds_sadjd_3dkajs"
                    }
                }
            ]
        """
        for i in self.samemessagegroupconfig:
            self.smmgroupcache[i] = {}
        for i in self.samemessageprivateconfig:
            self.smmprivatecache[i] = {}


    @staticmethod
    def load_config(path : str) -> Dict[str, Any]:
        if not path.exists():
            return
        with path.open() as f:
            d = yaml.full_load(f)
            if not d:
                return
            config: Dict[str, Any] = d
        return config

    @staticmethod
    def sent_by_master(message: Message) -> bool:
        return message.deliver_to != coordinator.master

    def process_message(self, message: Message) -> Optional[Message]:
        if message.type == MsgType.Text and self.mastersendback:
            message = self.mergemastersendouttextmessage(message)
        
        if message == None:
            return message

        if isinstance(message.chat, GroupChat):
            for i in self.samemessagegroupconfig:
                if message.text == i:
                    message = self.mergesamemessage(message, 'group', i)
        else:
            for i in self.samemessageprivateconfig:
                if message.text == i:
                    message = self.mergesamemessage(message, 'private', i)

        return message
        

    def mergemastersendouttextmessage(self, message: Message) -> Optional[Message]:
        if self.sent_by_master(message):
            self.mastersendoutmessagecache.append(message)
            self.logger.debug('master send message:'+str(message))
            if len(self.mastersendoutmessagecache)>30:
                self.mastersendoutmessagecache.pop(0)
            return message
        else:
            for i in self.mastersendoutmessagecache:
                if i.text == message.text and i.chat.uid == message.chat.uid :
                    self.logger.debug('slave send back master message:'+str(message))
                    self.mastersendoutmessagecache.remove(i)
                    #message.edit = True
                    #message.uid = i.uid
                    #message.deliver_to = coordinator.master
                    return None 
        return message

    def mergesamemessage(self, message: Message, key: str, samemessage: str):
        if key == 'group':
            smmcache = self.smmgroupcache
        elif key == 'private':
            smmcache = self.smmprivatecache

        def get_name():
            if message.author.alias == '' or message.author.alias is None:
                return message.author.name
            else:
                return message.author.alias

        name=get_name()

        def implement():
            smmcache[samemessage][message.chat.uid] = {
                'time': time.time(),
                'members': {name:1},
                'uid': message.uid+'QQ_War.message_merge'
            }
            #message.author = sys_author

            #if self.sent_by_master(message):
                #message.author = message.chat.self
            #    smmcache[samemessage][message.chat.uid]['uid'] = "{uni_id}".format(uni_id=str(int(time.time())))
            message.uid += 'QQ_War.message_merge'
            return message

        sys_author = message.chat.make_system_member(
            uid="QQ_War.message_merge",
            name="msg_merge",
            middleware=self
        )


        if message.chat.uid not in smmcache[samemessage]:
            self.logger.debug('first message to be merged:'+str(message))
            return implement()
        else:
            # The last samemessage should be valid only within 10 minutes
            if time.time() - smmcache[samemessage][message.chat.uid]["time"] < self.messagekeeptime*60:
                # Update Msg
                smmcache[samemessage][message.chat.uid]["time"] = time.time()

                if name in smmcache[samemessage][message.chat.uid]["members"].keys():
                    smmcache[samemessage][message.chat.uid]["members"][name]+=1
                else:
                    smmcache[samemessage][message.chat.uid]["members"][name]=1
                
                if not self.sent_by_master(message):
                    message.text = samemessage + "\n"
                    for i in smmcache[samemessage][message.chat.uid]["members"]:
                        message.text += i + "*" + str(smmcache[samemessage][message.chat.uid]["members"][i]) +", "
                    message.text.strip(", ")
                    message.edit = True
                    message.uid = MessageID(smmcache[samemessage][message.chat.uid]["uid"])
                    message.author = sys_author
                    message.type = MsgType.Text

                #message.chat.notification = ChatNotificationState.ALL

                self.logger.debug('messages merged:'+str(message))
                return message
            # If not, implement a new one
            else:
                self.logger.debug('messages to be merged start over:'+str(message))
                return implement()

        return message
