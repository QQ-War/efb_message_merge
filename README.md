# MessageMergeMiddleware
当前实现的功能：
```
1.实现主端发送的消息，如果从端会再以Sendoutmessage的形式发回来，屏蔽掉。

2.对于发送的相同消息，整合并显示该成员发送的次数。(参考https://github.com/iaurman/efb-msg-filter的代码）
2.1 本功能，相同消息在配置文件里面配置，且对群组和私聊分开设置整合关键字。
2.2 第一次收到信息不整合。
2.3 前后两条信息之间相距时间可以配置，默认不超过5分钟。再次收到以后重新计时。

```

## 1.安装

```pip install git+https://github.com/QQ-War/efb_message_merge.git```

## 2.注册到middleware

```
master_channel: blueset.telegram
slave_channels:
- honus.CuteCatiHttp
middlewares:
- 其他middleware
- QQ_War.message_merge
```
## 3.配置文件config.yaml，放到QQ_War.message_merge目录下面
```
mastersendback: True

messagekeeptime: 120
#此处单位是分钟，不配置的话，默认时间5分钟。
samemessagegroup:
 - "收到/取消 群语音邀请"
 - "收到"
samemessageprivate:
 - "语音/视频聊天\n  - - - - - - - - - - - - - - - \n不支持的消息类型, 请在微信端查看"
```
