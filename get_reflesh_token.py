from dropbox import DropboxOAuth2FlowNoRedirect
from dotenv import load_dotenv
import os

load_dotenv()

app_key = os.environ['KEY']
app_secret = os.environ['PASS']


# 内容表示用
auth_flow = DropboxOAuth2FlowNoRedirect(app_key,
                                        consumer_secret=app_secret,
                                        token_access_type='offline',
                                        scope=['files.metadata.read'])

# ダウンロード権限用
# auth_flow = DropboxOAuth2FlowNoRedirect(app_key,
#                                         consumer_secret=app_secret,
#                                         token_access_type='offline',
#                                         scope=['files.content.read'])

authorize_url = auth_flow.start()
print("1. URLにアクセスして: " + authorize_url)
print("2. 実行をおしてコード発行してね.")

inp = input("3. コピーしたコードを入力してEnter")

oauth_result = auth_flow.finish(inp)

print(oauth_result.refresh_token)