# 参考
https://github.com/serverless/examples/tree/master/aws-python-flask-api

# セットアップ

```
python3.8 -m venv ./venv
source ./venv/bin/activate
pip install -r requirements.txt
```

# ローカル起動

```
serverless wsgi serve
```

# デプロイ

```
serverless deploy
```

# ログ
https://ap-northeast-1.console.aws.amazon.com/cloudwatch/home?region=ap-northeast-1#logsV2:log-groups/log-group/$252Faws$252Flambda$252Faws-python-flask-api-dev-api