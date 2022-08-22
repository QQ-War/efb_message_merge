# MessageMergeMiddleware
1.安装

```pip install git+https://github.com/QQ-War/efb-message-merge.git```

2.注册到middleware

```
master_channel: blueset.telegram
slave_channels:
- honus.CuteCatiHttp
middlewares:
- 其他middleware
- QQ_War.message_merge
```

