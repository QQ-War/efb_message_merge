## MessageMergeMiddleware
当前实现的功能：
```
1.实现主端发送的消息，如果从端会再以Sendoutmessage的形式发回来，屏蔽掉。
```

# 1.安装

```pip install git+https://github.com/QQ-War/efb_message_merge.git```

# 2.注册到middleware

```
master_channel: blueset.telegram
slave_channels:
- honus.CuteCatiHttp
middlewares:
- 其他middleware
- QQ_War.message_merge
```

