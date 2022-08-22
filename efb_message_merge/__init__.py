import threading
import time
import yaml
import re
from typing import Optional, Union, Dict
from typing import Dict , Any

from ehforwarderbot import Middleware, Message, Status, coordinator, utils, MsgType
from ehforwarderbot.types import ModuleID, MessageID, InstanceID, ChatID
from ehforwarderbot.chat import Chat, SystemChat, GroupChat
from ehforwarderbot.message import MsgType, MessageCommands, MessageCommand, Substitutions
from ehforwarderbot import utils as efb_utils


class MessageMergeMiddleware(Middleware):
    """
    """
    middleware_id: ModuleID = ModuleID("QQ_War.message_merge")
    middleware_name: str = "Message Merge Middleware"
    __version__: str = '0.1.0'

    
    def __init__(self, instance_id: Optional[InstanceID] = None):
        super().__init__(instance_id)
        #config_path = efb_utils.get_config_path(self.middleware_id)
        #self.config = self.load_config(config_path)
        #self.keywords=self.config['keywords'] if 'keywords' in self.config.keys() else {}
        self.messagecache = list()


    #@staticmethod
    #def load_config(path : str) -> Dict[str, Any]:
    #    if not path.exists():
    #        return
    #    with path.open() as f:
    #        d = yaml.full_load(f)
    #        if not d:
    #            return
    #        config: Dict[str, Any] = d
    #    return config

    @staticmethod
    def sent_by_master(message: Message) -> bool:
        return message.deliver_to != coordinator.master

    def process_message(self, message: Message) -> Optional[Message]:
        if message.type == MsgType.Text:
            return self.mergetextmessage(message)
        return message
        

    def mergetextmessage(self, message: Message) -> Optional[Message]:
        if self.sent_by_master(message):
            self.messagecache.append(message)
            if len(self.messagecache)>30:
                self.messagecache.pop(0)
            return message
        else:
            for i in self.messagecache:
                if i.text == message.text and i.chat.uid == message.chat.uid :
                    self.messagecache.remove(i)
                    #message.edit = True
                    #message.uid = i.uid
                    #message.deliver_to = coordinator.master
                    return None 
        return message
