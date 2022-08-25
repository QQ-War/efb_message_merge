# MessageMergeMiddleware
当前实现的功能：
```
1.实现主端发送的消息，如果从端会再以Sendoutmessage的形式发回来，屏蔽掉。

2.对于发送的相同消息，整合并显示该成员发送的次数。相同消息在配置文件里面配置，前后两条信息之间相距不超过10分钟。(参考https://github.com/iaurman/efb-msg-filter的代码）
本功能，仅对群组有效，且第一条信息不整合。
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

samemessage:
 - "收到/取消 群语音邀请"
 - "收到"
```
