from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
import time
import os
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.alert import Alert
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from selenium.common.exceptions import TimeoutException
import re
import sys
from selenium import webdriver
import dropbox
import chromedriver_binary
from dotenv import load_dotenv
import subprocess
import datetime
import slackweb
import random

load_dotenv()

def my_time():
    rand = random.randrange(3, 7, 1)
    return time.sleep(rand)


def my_driver():
    # スクレイピング
    options = webdriver.ChromeOptions()

    # driverの自動更新
    serv = Service(ChromeDriverManager().install())

    # ヘッドレスモード
    options.headless = True
    options.add_argument('--disable-gpu')
    # シークレットモード
    options.add_argument('--incognito')

    # 画像非表示
    options.add_argument('--blink-settings=imagesEnabled=false')

    # セキュリティ対策などのchromeに搭載してある保護機能をオフにする。
    options.add_argument("--no-sandbox")
    # ディスクのメモリスペースを使う。
    options.add_argument('--disable-dev-shm-usage')
    # リモートデバッグフラグを立てる。
    options.add_argument('--remote-debugging-port=9222')

    driver = webdriver.Chrome(options=options)
    driver.set_window_size(1500, 1500)

    return driver


def my_drop_box():
    inp = input("読み込むフォルダ名を入力してください")
    # ローカルのメッセージを削除
    try:
        cmd = 'rm messages/*'
        subprocess.run(cmd, shell=True)
    except:
        pass

    app_key = os.environ['KEY']
    app_secret = os.environ['PASS']
    token = os.environ['TOKEN']
    token2 = os.environ['TOKEN2']

    # 内容確認
    drop = dropbox.Dropbox(app_key=app_key, app_secret=app_secret,
                           oauth2_refresh_token=token)
    drop2 = dropbox.Dropbox(app_key=app_key, app_secret=app_secret,
                            oauth2_refresh_token=token2)
    today_path = f'/heaven_auto/{inp}/'
    for entry in drop.files_list_folder(f'{today_path}urls').entries:
        drop2.files_download_to_file(f'urls/{entry.name}', f'{today_path}urls/{entry.name}')

    drop2.files_download_to_file('account.txt', f'{today_path}account.txt')

    try:
        for entry in drop.files_list_folder(f'{today_path}messages/').entries:
            drop2.files_download_to_file(f'messages/{entry.name}', f'{today_path}messages/{entry.name}')

        print("ダウンロードしました")
    except:
        print("ダウンロードしました(メッセージテンプレなし)")

def today_drop_box():
    today = datetime.date.today().strftime('%Y%m%d')
    inp = today
    # ローカルのメッセージを削除
    try:
        cmd = 'rm messages/*'
        subprocess.run(cmd, shell=True)
    except:
        pass
        # ローカルのリセットテキストを削除
        try:
            cmd = 'rm reset.txt'
            subprocess.run(cmd, shell=True)
        except:
            pass

    app_key = os.environ['KEY']
    app_secret = os.environ['PASS']
    token = os.environ['TOKEN']
    token2 = os.environ['TOKEN2']

    # 内容確認
    drop = dropbox.Dropbox(app_key=app_key, app_secret=app_secret,
                           oauth2_refresh_token=token)
    drop2 = dropbox.Dropbox(app_key=app_key, app_secret=app_secret,
                            oauth2_refresh_token=token2)
    try:
        try:
            # 通常の場合
            today_path = f'/heaven_auto/{inp}/'
            for entry in drop.files_list_folder(f'{today_path}urls').entries:
                drop2.files_download_to_file(f'urls/{entry.name}', f'{today_path}urls/{entry.name}')

            drop2.files_download_to_file('account.txt', f'{today_path}account.txt')
            drop2.files_download_to_file('account2.txt', f'{today_path}account2.txt')
        except:
            # resetの場合
            today_path = f'/heaven_auto/{inp}reset/'
            for entry in drop.files_list_folder(f'{today_path}urls').entries:
                drop2.files_download_to_file(f'urls/{entry.name}', f'{today_path}urls/{entry.name}')

            drop2.files_download_to_file('account2.txt', f'{today_path}account2.txt')
            print("キテねリストを消去します")
            try:
                cmd = 'rm logs/*/follows.txt'
                subprocess.run(cmd, shell=True)
                print("消去しました。")
            except:
                print("失敗しました")


        try:
            for entry in drop.files_list_folder(f'{today_path}messages/').entries:
                drop2.files_download_to_file(f'messages/{entry.name}', f'{today_path}messages/{entry.name}')

            print("ダウンロードしました")
            return True
        except:
            print("ダウンロードしました(メッセージテンプレなし)")
            return True
    except:
        print("ファイルがありませんでした")
        return False


# ドライバーを一旦すべて終了
def clear_driver():
    try:
        cmd = "ps aux | grep chromedriver | grep -v grep | awk '{ print \"kill -9\", $2 }' | sh"
        subprocess.run(cmd, shell=True)
        cmd1 = "ps aux | grep 'Google Helper' | grep -v grep | awk '{ print \"kill -9\", $2 }' | sh"
        subprocess.run(cmd1, shell=True)
        cmd2 = "ps aux | grep 'Google Chrome' | grep -v grep | awk '{ print \"kill -9\", $2 }' | sh"
        subprocess.run(cmd2, shell=True)
        cmd3 = "pkill chrome"
        subprocess.run(cmd3, shell=True)
    except:
        pass


def time_count(start_time):
    # 時間を測る
    time_end = time.perf_counter()
    tim = time_end - start_time
    result_time = tim / 60
    print(result_time)


class Spgirl_Auto:
    def __init__(self, username, password):
        self.username = username
        self.password = password

    # ログインするまでの処理
    def login(self):
        url = "https://spgirl.cityheaven.net/J1Login.php"
        driver = my_driver()
        driver.get(url)
        my_time()
        driver.find_element(by=By.ID, value='userid').send_keys(self.username)
        driver.find_element(by=By.ID, value='passwd').send_keys(self.password)
        driver.find_element(by=By.ID, value='loginBtn').click()
        my_time()
        return driver

    # 残りのキテねの数のみ出力
    def kitene_confirm(self):
        driver = self.login()
        login_check = True

        try:
            check = driver.find_element(By.CLASS_NAME, value='errorMsg')
            if check:
                login_check = False
        except:
            pass

        logs = "log.txt"
        log = ""
        print(self.username)

        with open(logs, mode="a") as f:
            f.write("%s\n" % self.username)
        if login_check:
            my_time()
            # 認証コードを求められた場合
            try:
                auth = driver.find_element(By.CLASS_NAME, value='title-txt')
                if auth.text == "認証コードを入力":
                    print("認証コードが必要です")
                    with open(logs, mode="a") as f:
                        f.write("%s\n" % "認証コードが必要です")
            except:
                # キテねがつかいきってるか確認
                try:
                    driver.find_element(By.CLASS_NAME, value='no_kitene_count')
                    log = "使い切りました"
                except:
                    try:
                        WebDriverWait(driver, 60).until(
                            EC.visibility_of_element_located((By.CLASS_NAME, "kitene_count")))
                        c_text = driver.find_element(By.CLASS_NAME, value='kitene_count').text
                        many = re.findall(r'キテネ残り回数：(\w+)回', c_text)[0]
                        log = f"{many}残ってます"
                    except:
                        log = "失敗しました"
                with open(logs, mode="a") as f:
                    f.write("%s\n" % log)
                    print(log)
            driver.quit()
        else:
            log = "ログインできないユーザーです"
            print(log)
        return log

    # きてねの残りを数えてキテねを実行
    def kitene_limit(self):
        logs = f"log.txt"
        print(self.username)
        driver = self.login()
        my_time()
        try:
            # 認証コードを求められた場合
            try:
                auth = driver.find_element(By.CLASS_NAME, value='title-txt')
                if auth.text == "認証コードを入力":
                    print("認証コードが必要です")
                    with open(logs, mode="a") as f:
                        f.write("%s\n" % "認証コードが必要です")
            except:
                # キテねがつかいきってるか確認
                try:
                    driver.find_element(By.CLASS_NAME, value='no_kitene_count')
                    log = "使い切りました"
                    print(log)
                except:
                    try:
                        WebDriverWait(driver, 60).until(
                            EC.visibility_of_element_located((By.CLASS_NAME, "kitene_count")))
                        c_text = driver.find_element(By.CLASS_NAME, value='kitene_count').text
                        many = re.findall(r'キテネ残り回数：(\w+)回', c_text)[0]
                        print(many)
                        try:
                            driver.get(f"https://spgirl.cityheaven.net/J10ComeonAiMatchingList.php?gid={self.username}")
                            WebDriverWait(driver, 60).until(
                                EC.visibility_of_element_located((By.CLASS_NAME, "kitene_mada")))
                        except:
                            # うまく読み込めなかった場合にもう一度実行
                            driver.get(f"https://spgirl.cityheaven.net/J10ComeonAiMatchingList.php?gid={self.username}")
                            WebDriverWait(driver, 60).until(
                                EC.visibility_of_element_located((By.CLASS_NAME, "kitene_mada")))
                        time.sleep(10)
                        btns = driver.find_elements(By.CLASS_NAME, value='kitene_mada')

                        for i in range(int(many)):
                            my_time()
                            # btns = driver.find_elements(By.CLASS_NAME, value='kitene_btn')
                            driver.execute_script('arguments[0].scrollIntoView(true);', btns[i])
                            btns[i].click()
                            my_time()
                            Alert(driver).accept()
                            my_time()
                            print(f'{i + 1}回目キテねしました')
                        log = f"{many}回追加で実行しました"
                    except Exception as e:
                        print(e)
                        log = "失敗しました"
                with open(logs, mode="a") as f:
                    f.write("%s\n" % log)
        except:
            print("ログインできないアカウントです")
        finally:
            driver.quit()

    # マイページから自分のURLを取得する(エリアが変わらなければやる必要なし)
    def mypage(self):
        driver = self.login()
        get_url = driver.find_element(By.NAME, value='form_mypage').get_attribute("action")
        return get_url

    # 自分のURLからエリアのお店の一覧を取得する(エリアの対象のお店のURLを取得)
    def myshops(self):
        # URLにアクセス
        # url = self.mypage()
        url = "https://www.cityheaven.net/tokyo/A1304/A130401/fullco/girlid-44275681/?mypage_flg=1"
        driver = my_driver()
        wait = WebDriverWait(driver=driver, timeout=60)
        driver.get(url)
        driver.find_element(By.ID, value='location-breadcrumbs-wrap').find_elements(By.TAG_NAME, value="li")[4].click()
        wait.until(EC.presence_of_all_elements_located)

        more_button = driver.find_element(By.CLASS_NAME, value='submit_btn')
        while more_button:
            try:
                driver.find_element(By.CLASS_NAME, value='submit_btn').click()
                time.sleep(5)
            except:
                break

        shops = driver.find_elements(By.CLASS_NAME, value="shop_title_shop")
        # もしユーザーのディレクトリがなければ作成
        if not os.path.exists(self.username):
            os.makedirs(self.username)
        text_file = f"{self.username}/shops.txt"
        for s in shops:
            # FULLCOは対象から外す
            fullco = "https://www.cityheaven.net/tokyo/A1304/A130401/fullco/"
            if not s.get_attribute(name="href") == fullco:
                with open(text_file, mode="a") as f:
                    f.write(s.get_attribute(name="href"))
                    f.write("\n")

    # ファイルからURLと回数を取得してそれぞれその回数だけキテねする
    def url_read_kitene(self):
        text_file = f"urls/{self.username}.txt"
        # ログようディレクトリがない場合
        if not os.path.isdir(f"logs/{self.username}"):
            os.mkdir(f"logs/{self.username}")

        follows = f"logs/{self.username}/follows.txt"
        my_log = []

        # もしフォローファイルがなかったら作成
        if (os.path.isfile(follows) == False):
            with open(follows, 'w') as f:
                pass
        try:
            # 対象のURLリストから一番上のURLを取得
            with open(text_file, mode="r") as f:
                targets = f.readlines()
        except:
            my_log.append("URLファイルがないか不正です。")

        # フォローした人たちの読み込み
        with open(follows, mode='r') as f:
            my_follow_file = f.read()
        my_follow = my_follow_file.split()

        driver = my_driver()
        driver.get(f"{targets[0][3:]}reviews/?lo=1")
        driver.implicitly_wait(10)
        driver.execute_script("window.scrollTo(0, 0)")

        # スクリーンショットを取得
        # driver.save_screenshot('result.png')


        WebDriverWait(driver, 30).until(
            EC.visibility_of_element_located((By.ID, "login_header")))
        driver.find_element(By.ID, value='login_header').click()
        my_time()
        driver.find_element(By.ID, value='user').send_keys(self.username)
        driver.find_element(By.ID, value='pass').send_keys(self.password)
        my_time()
        driver.find_element(By.ID, value='submitLogin').click()
        print(self.username)

        wait = WebDriverWait(driver, 30)
        check = True
        try:
            driver.find_element(By.ID, value='login_header')
            check = False
        except:
            pass
        if check:
            try:
                for target in targets:
                    tar = target.split(" ")
                    many = int(tar[0])
                    tar_url = tar[1]
                    cou = 0
                    error = 0

                    # キテねできなかった時
                    try:
                        alert = driver.switch_to.alert
                        print(alert.text)
                        alert.accept()
                        my_log.append(alert.text)
                    except:
                        pass

                    driver.get(f"{tar_url}reviews/?lo=1")
                    my_time()
                    print(tar_url)
                    # 対象の口コミ一覧
                    my_url = str(driver.current_url)
                    my_log.append(tar_url)
                    while cou < many:
                        try:
                            wait.until(EC.alert_is_present())
                            alert = driver.switch_to.alert
                            # print(alert.text)
                            my_time()
                            alert.accept()
                        except:
                            pass

                        # 表示されたページのメンバーのURLを取得
                        try:
                            WebDriverWait(driver, 30).until(
                                EC.visibility_of_element_located((By.CLASS_NAME, "review-item-shopnameButton")))
                            members = driver.find_elements(By.CLASS_NAME, value='review-item-shopnameButton')
                            ac_url = []

                            now_url = driver.current_url
                            print(now_url)
                            my_log.append(now_url)
                            my_time()

                            # 取得したURLをリストにする
                            for i in range(len(members)):
                                try:
                                    pick = driver.find_elements(By.CLASS_NAME, value='review-item-shopnameButton')[
                                        i].find_element(
                                        By.TAG_NAME, value="a").get_attribute(name="href")
                                    ac_url.append(pick)
                                except:
                                    my_log.append("退会済みユーザーがいました")
                                    pass
                            print(len(ac_url))
                            my_log.append(len(ac_url))

                            # 取得したurlからすでに自分のフォローした人がいないか確認
                            for i in ac_url:
                                url = i
                                driver.implicitly_wait(5)
                                try:
                                    alert = driver.switch_to.alert
                                    print(alert.text)
                                    my_log.append(alert.text)
                                    alert.accept()
                                except:
                                    pass

                                print(url)
                                my_log.append(url)

                                # もし口コミした人のURLがフォローリストにいなくて、指定の数以内の場合
                                if not url in my_follow and cou < many:
                                    driver.get(url)
                                    try:
                                        # if driver.switch_to.alert:
                                        #     alert = driver.switch_to.alert
                                        #     print(alert.text)
                                        #     my_log.append(alert.text)
                                        #     alert.accept()

                                        # wait.until(EC.element_to_be_clickable((By.CLASS_NAME, "kitene_send")))

                                        # driver.save_screenshot("スクショ.img")
                                        WebDriverWait(driver, 30).until(
                                            EC.visibility_of_element_located((By.CLASS_NAME, "kitene_send")))
                                        kitene = driver.find_element(By.CLASS_NAME, value="kitene_send")
                                        my_time()
                                        kitene.click()
                                        my_time()
                                        Alert(driver).accept()
                                        print(f"キテネを押しました")
                                        my_log.append("キテねを押しました")
                                        cou += 1
                                        my_follow.append(url)
                                        if cou >= many:
                                            print(f'{cou}回キテねしました')
                                            my_log.append(f"{cou}回キテねしました")
                                            break
                                    except TimeoutException as e:
                                        print("時間切れです")
                                        error += 1
                                        print(e)
                                        my_follow.append(url)
                                        if error >= 10:
                                            break
                                        pass
                                    except Exception as e:
                                        error += 1
                                        print(f"失敗しました {error}")
                                        print(e)
                                        my_follow.append(url)
                                        my_log.append(f"失敗しました{error}")
                                        my_log.append(e)
                                        if error >= 10:
                                            break
                                        pass

                                    # キテねできなかった時
                                    try:
                                        alert = driver.switch_to.alert
                                        print(alert.text)
                                        my_log.append(alert.text)
                                        alert.accept()
                                    except:
                                        pass
                                    time.sleep(1)
                                    # driver.back()

                                # エラーが10以上だった場合
                                if error >= 10:
                                    print("エラーが10回以上でました")
                                    my_log.append("エラーが10回以上でました")
                                    break

                            if error >= 10 or cou >= many:
                                break
                        except Exception as e:
                            print(e)
                        try:
                            if driver.current_url == 'data:,':
                                driver.forward()
                            my_time()
                            driver.get(my_url)
                            print(driver.current_url)
                            my_log.append(driver.current_url)
                            print("次のページに進みます")
                            my_log.append("次のページに進みます")
                            WebDriverWait(driver, 30).until(
                                EC.visibility_of_element_located((By.CLASS_NAME, "next")))
                            driver.get(driver.find_element(By.CLASS_NAME, value='next').get_attribute(name='href'))
                            my_url = str(driver.current_url)
                        except:
                            print("次のページはありません")
                            my_log.append("次のページはありません")
                            break

                    # キテねした人をフォローリストに追加
                    with open(follows, mode="a") as f:
                        for d in my_follow:
                            f.write("%s\n" % d)

                    if error >= 10:
                        break

                try:
                    alert = driver.switch_to.alert
                    print(alert.text)
                    my_log.append(alert.text)
                    alert.accept()
                except:
                    pass

                driver.quit()

                logs = f"log.txt"
                with open(logs, mode="w") as f:
                    for d in my_log:
                        f.write("%s\n" % d)

            except Exception as ex:
                driver.quit()
                print("キテねに失敗しました")
                print(ex)
                log = f"log.txt"
                with open(log, mode="a") as fi:
                    fi.write("%s\n" % ex)
        else:
            print("ログインできません")

    # マイガールのフォローされている人でまたフォローを返していない人がいたらフォローする
    def mygirl_follower(self):
        return_log = ""
        driver = self.login()
        my_time()
        # 認証コードを求められた場合
        try:
            auth = driver.find_element(By.CLASS_NAME, value='title-txt')
            if auth.text == "認証コードを入力":
                return_log += "\n認証コードが必要です"
        except:
            try:
                # フォロー確認
                my_follower = f"https://spgirl.cityheaven.net/J9FollowerList.php?gid={self.username}"
                driver.get(my_follower)
                WebDriverWait(driver, 8).until(
                    EC.visibility_of_element_located((By.CLASS_NAME, "f_off"))
                )
                try:
                    btns = driver.find_elements(By.CLASS_NAME, value='f_off')
                    wait = WebDriverWait(driver=driver, timeout=8)
                    wait.until(EC.presence_of_all_elements_located)
                    my_time()
                    did = 0
                    miss = 0

                    for btn in btns:
                        try:
                            # 対象のボタンが見えるまでスクロールする
                            driver.execute_script('arguments[0].scrollIntoView(true);', btn)
                            btn.click()
                            my_time()
                            did += 1
                        except:
                            miss += 1
                    print(f"フォロー数:{did} 失敗数:{miss}回")
                    return_log += f"\nフォロー数:{did} 失敗数:{miss}回"
                except:
                    return_log += f"\nフォローに失敗しました"

            except:
                return_log += "できるフォローがありませんでした"
            try:
                message_url = f"https://spgirl.cityheaven.net/J2OkiniTalkUserList.php?gid={self.username}"
                driver.get(message_url)
                WebDriverWait(driver, 8).until(
                    EC.visibility_of_element_located((By.CLASS_NAME, "link_user"))
                )
                targets = driver.find_elements(By.CLASS_NAME, value='link_user')
                my_time()

                # メッセージを送る処理
                send = 0
                miss = 0
                message_path = f"messages/{self.username}.txt"
                with open(message_path, "r", encoding="utf-8") as f:
                    message = f.read()
                message_lists = []

                for target in targets:
                    target_txt = target.find_element(By.CLASS_NAME, value='talk_text').text
                    # 一度も送ってない人のみ作業
                    if target_txt == "":
                        message_lists.append(target.get_attribute(name="href"))
                for m_list in message_lists:
                    try:
                        driver.get(m_list)
                        WebDriverWait(driver, 8).until(
                            EC.visibility_of_element_located((By.ID, "te_box"))
                        )
                        my_time()
                        # 絵文字の対応
                        INPUT_EMOJI = """
                            arguments[0].value += arguments[1];
                            arguments[0].dispatchEvent(new Event('change'));
                            """
                        element = driver.find_element(By.ID, value='te_box')
                        driver.execute_script(INPUT_EMOJI, element, message)

                        # driver.find_element(By.ID, value='te_box').send_keys(message)
                        my_time()
                        WebDriverWait(driver, 8).until(
                            EC.visibility_of_element_located((By.CLASS_NAME, "te_submit"))
                        )
                        driver.find_element(By.CLASS_NAME, value="te_submit").click()
                        my_time()
                        send += 1
                    except:
                        miss += 1
                return_log += f"\n{send}件送りました。{miss}件送れませんでした。"
            except:
                return_log += "\n送信対象がいませんでした。"
        return return_log


if __name__ == '__main__':
    start_desc = f"{datetime.datetime.now(datetime.timezone(datetime.timedelta(hours=9)))}の実行"
    print(start_desc)
    with open("log.txt", mode="a") as f:
        f.write("%s\n" % start_desc)

    # 時間のカウント
    time_sta = time.perf_counter()

    answer = input(
        "[1]自動キテね実行 [2]残りのキテね確認 [3]マッチユーザーのみ [4]本日のファイルダウンロード [5]キテねリスト削除 [6]履歴削除 [7]サーバシャットダウン [8]フォロー返し")

    # ユーザー情報の取り込み
    users = []
    with open("account.txt", "r", encoding="utf-8") as f:
        # リストとして読み込む
        lines = f.readlines()

    for line in lines:
        li = line.strip('\n')
        l = li.split(" ")
        users.append(l)

    if answer == "1":
        clear_driver()
        drop = today_drop_box()
        if drop:
            slack_send = "自動実行開始"
            print(slack_send)
            slack = slackweb.Slack(url=os.environ['SLACK'])
            slack.notify(text=slack_send)
            for user in users:
                clear_driver()
                text_file = f"urls/{user[0]}.txt"

                # ファイルがなかったら終了
                if not os.path.isfile(text_file):
                    print("URLファイルがありません")
                else:
                    test = Spgirl_Auto(user[0], user[1])
                    clear_driver()

                    with open("log.txt", mode="a") as f:
                        f.write("%s\n" % user[0])
                    subprocess.run("echo pure2juntan | sudo -S chmod -R 777 urls", shell=True)
                    try:
                        test.url_read_kitene()
                    except Exception as e:
                        print(e)
                    my_time()

            my_time()
            clear_driver()
            for user in users:
                clear_driver()

                test = Spgirl_Auto(user[0], user[1])
                clear_driver()
                logs = f"log.txt"
                with open(logs, mode="a") as f:
                    f.write("%s\n" % datetime.datetime.now())
                try:
                    test.kitene_limit()
                    clear_driver()
                except Exception as e:
                    print("キテねに失敗しました")
                    clear_driver()
                    print(e)
                    with open(logs, mode="a") as f:
                        f.write("%s\n" % e)
                my_time()
            clear_driver()
            my_time()
            # 確認
            slack_send = ""
            for user in users:
                # 念の為chromeを停止
                # cmd = 'killall chrome'
                # subprocess.run(cmd, shell=True)
                clear_driver()

                test = Spgirl_Auto(user[0], user[1])
                clear_driver()
                try:
                    sl = test.kitene_confirm()
                    clear_driver()
                except Exception as e:
                    sl = "キテねの確認に失敗しました"
                    clear_driver()
                    print(sl)
                    print(e)
                    logs = f"log.txt"
                    with open(logs, mode="a") as f:
                        f.write("%s\n" % e)
                slack_send += f"\n{user[0]}\n{sl}\n"
            # Slackに通知
            slack = slackweb.Slack(url=os.environ['SLACK'])
            slack.notify(text=slack_send)
            # 時間を出力
            time_count(time_sta)

            clear_driver()

            # フォロー返し
            slack_send = ""
            # ユーザー情報の取り込み
            users = []
            try:
                with open("account2.txt", "r", encoding="utf-8") as f:
                    # リストとして読み込む
                    lines = f.readlines()

                for line in lines:
                    li = line.strip('\n')
                    l = li.split(" ")
                    users.append(l)

                for check in users:
                    clear_driver()
                    print(check[0])
                    test = Spgirl_Auto(check[0], check[1])
                    clear_driver()
                    try:
                        sl = test.mygirl_follower()
                    except Exception as e:
                        sl = f"失敗しました"
                        clear_driver()
                        print(sl)
                        print(e)
                    my_time()
                    slack_send += f"\n{check[0]}\n{sl}\n"
                # Slackに通知
                slack = slackweb.Slack(url=os.environ['SLACK'])
                slack.notify(text=slack_send)
                print(slack_send)
            except:
                print("フォロー返しなしです。")
            # サーバーをシャットダウン
            try:
                cmd = 'sudo shutdown -h now'
                subprocess.run(cmd, shell=True)
            except:
                print("シャットダウン失敗しました")
        else:
            # Slackに通知
            slack_send = "本日のファイル取得できませんでした"
            print(slack_send)
            slack = slackweb.Slack(url=os.environ['SLACK'])
            slack.notify(text=slack_send)
             # サーバーをシャットダウン
            try:
                cmd = 'sudo shutdown -h now'
                subprocess.run(cmd, shell=True)
            except:
                print("シャットダウン失敗しました")

            # サーバーをシャットダウン
            try:
                cmd = 'sudo shutdown -h now'
                subprocess.run(cmd, shell=True)
            except:
                print("シャットダウン失敗しました")

    elif answer == "2":
        clear_driver()
        slack_send = ""
        for user in users:
            # 念の為chromeを停止
            # cmd = 'pkill chrome'
            # subprocess.run(cmd, shell=True)
            clear_driver()

            test = Spgirl_Auto(user[0], user[1])
            clear_driver()
            try:
                sl = test.kitene_confirm()
            except Exception as e:
                sl = "キテねの確認に失敗しました"
                clear_driver()
                print(sl)
                print(e)
                logs = f"log.txt"
                with open(logs, mode="a") as f:
                    f.write("%s\n" % e)
            slack_send += f"\n{user[0]}\n{sl}\n"
        # Slackに通知
        slack = slackweb.Slack(url=os.environ['SLACK'])
        slack.notify(text=slack_send)


    elif answer == "3":
        clear_driver()
        slack_send = ""
        for user in users:
            # 念の為chromeを停止
            # cmd = 'pkill chrome'
            # subprocess.run(cmd, shell=True)
            clear_driver()

            test = Spgirl_Auto(user[0], user[1])
            clear_driver()
            logs = f"log.txt"
            with open(logs, mode="a") as f:
                f.write("%s\n" % datetime.datetime.now())
            try:
                test.kitene_limit()
                clear_driver()
            except Exception as e:
                print("キテねに失敗しました")
                clear_driver()
                print(e)
                with open(logs, mode="a") as f:
                    f.write("%s\n" % e)
        clear_driver()

        for user in users:
            # 念の為chromeを停止
            # cmd = 'pkill chrome'
            # subprocess.run(cmd, shell=True)
            clear_driver()

            test = Spgirl_Auto(user[0], user[1])
            try:
                sl = test.kitene_confirm()
                clear_driver()
            except Exception as e:
                sl = "キテねの確認に失敗しました"
                clear_driver()
                print(sl)
                print(e)
                logs = f"log.txt"
                with open(logs, mode="a") as f:
                    f.write("%s\n" % e)
            slack_send += f"\n{user[0]}\n{sl}\n"
        # Slackに通知
        slack = slackweb.Slack(url=os.environ['SLACK'])
        slack.notify(text=slack_send)
        clear_driver()

        # 時間を出力
        time_count(time_sta)
        # サーバーをシャットダウン
        try:
            cmd = 'sudo shutdown -h now'
            subprocess.run(cmd, shell=True)
        except:
            print("シャットダウン失敗しました")

    elif answer == "4":
        try:
            my_drop_box()
        except Exception as e:
            print("ダウンロード失敗しました")
            print(e)

    elif answer == "5":
        print("キテねリストを消去します")
        try:
            cmd = 'rm logs/*/follows.txt'
            subprocess.run(cmd, shell=True)
            print("消去しました。")
        except:
            print("失敗しました")

    elif answer == "6":
        print("履歴を消去します")
        try:
            # cmd = 'rm logs/*/log.txt'
            cmd = 'rm -f main_logs/*'
            subprocess.run(cmd, shell=True)
            print("消去しました。")
        except:
            print("失敗しました")
    elif answer == "7":
        # サーバーをシャットダウン
        print("サーバーをシャットダウンします")
        try:
            cmd = 'sudo shutdown -h now'
            subprocess.run(cmd, shell=True)
        except:
            print("シャットダウン失敗しました")

    # マイガールのフォロー返しとメッセージ送信を行う
    elif answer == "8":
        clear_driver()
        slack_send = ""
        # ユーザー情報の取り込み
        users = []
        try:
            with open("account2.txt", "r", encoding="utf-8") as f:
                # リストとして読み込む
                lines = f.readlines()

            for line in lines:
                li = line.strip('\n')
                l = li.split(" ")
                users.append(l)

            for check in users:
                clear_driver()
                print(check[0])
                test = Spgirl_Auto(check[0], check[1])
                clear_driver()
                try:
                    sl = test.mygirl_follower()
                except Exception as e:
                    sl = f"失敗しました"
                    clear_driver()
                    print(sl)
                    print(e)
                my_time()
                slack_send += f"\n{check[0]}\n{sl}\n"
            # Slackに通知
            slack = slackweb.Slack(url=os.environ['SLACK'])
            slack.notify(text=slack_send)
            print(slack_send)
        except:
            print("フォロー返しなしです。")
        # サーバーをシャットダウン
        try:
            cmd = 'sudo shutdown -h now'
            subprocess.run(cmd, shell=True)
        except:
            print("シャットダウン失敗しました")
    elif answer == "9":
        slack_send = "テスト"
        slack = slackweb.Slack(url=os.environ['SLACK'])
        slack.notify(text=slack_send)

    elif answer == "a":
        today_drop_box()

    # 時間を測る
    time_end = time.perf_counter()
    tim = time_end - time_sta
    result_time = tim / 60
    print(result_time)
