from selenium import webdriver
from selenium.webdriver import ChromeOptions
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome import service as fs
from selenium.webdriver.chrome.service import Service
import chromedriver_binary
from webdriver_manager.chrome import ChromeDriverManager
import time
from dotenv import load_dotenv
import os
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.alert import Alert
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from selenium.webdriver.common.action_chains import ActionChains
from selenium.common.exceptions import TimeoutException
import re


class Spgirl_Auto:
    def __init__(self, username, password):
        self.username = username
        self.password = password

    # ログインするまでの処理
    def login(self):
        options = webdriver.ChromeOptions()
        options.headless = True
        # serv = Service(ChromeDriverManager().install())  # driverの自動更新
        driver = webdriver.Chrome(options=options)
        wait = WebDriverWait(driver=driver, timeout=20)
        # URLにアクセス
        url = "https://spgirl.cityheaven.net/J1Login.php?girlId=aqOK%2FRBOsM0%3D&PHPSESSID=8be4e6213cd52fc42bf5e4b6870df3b7"

        driver.get(url)
        time.sleep(2)
        driver.find_element(by=By.ID, value='userid').send_keys(self.username)
        driver.find_element(by=By.ID, value='passwd').send_keys(self.password)
        driver.find_element(by=By.ID, value='loginBtn').click()
        time.sleep(2)
        return driver

    # きてねの残りを数える
    def kitene_limit(self):
        driver = self.login()
        time.sleep(2)

        # キテねがつかいきってるか確認
        try:
            driver.find_element(By.CLASS_NAME, value='no_kitene_count')
            print("使い切りました")
        except:
            c_text = driver.find_element(By.CLASS_NAME, value='kitene_count').text
            many = re.findall(r'キテネ残り回数：(\w+)回', c_text)
            print(many)
            try:
                driver.get(f"https://spgirl.cityheaven.net/J10ComeonAiMatchingList.php?gid={self.username}")
                WebDriverWait(driver, 80).until(
                    EC.visibility_of_element_located((By.CLASS_NAME, "kitene_btn")))
                btns = driver.find_elements(By.CLASS_NAME, value='kitene_btn')
                for btn in btns:
                    btn.click()
                    Alert(driver).accept()
                    time.sleep(3)
                log = f"{many}回追加で実行しました"
            except:
                log = "失敗しました"
            logs = f"logs/{self.username}/log.txt"
            with open(logs, mode="a") as f:
                f.write("%s\n" % log)

    # マイページから自分のURLを取得する(エリアが変わらなければやる必要なし)
    def mypage(self):
        driver = self.login()
        get_url = driver.find_element(By.NAME, value='form_mypage').get_attribute("action")
        return get_url

    # 自分のURLからエリアのお店の一覧を取得する(エリアの対象のお店のURLを取得)
    def myshops(self):
        options = webdriver.ChromeOptions()
        # options.headless = True
        # serv = Service(ChromeDriverManager().install())  # driverの自動更新
        driver = webdriver.Chrome(options=options)
        wait = WebDriverWait(driver=driver, timeout=60)

        # URLにアクセス
        # url = self.mypage()
        # ToDo:個人のURLを保管する場所作る
        url = "https://www.cityheaven.net/tokyo/A1304/A130401/fullco/girlid-44275681/?mypage_flg=1"
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

        # location-breadcrumbs-wrap > li:nth-child(5) > a

    # ファイルからURLと回数を取得してそれぞれその回数だけキテねする
    def url_read_kitene(self):
        text_file = f"users/{self.username}.txt"
        follows = f"logs/{self.username}/follows.txt"
        my_log = []

        # もしフォローファイルがなかったら作成
        if (os.path.isfile(follows) == False):
            with open(follows, 'w') as f:
                pass

        # 対象のURLリストから一番上のURLを取得
        with open(text_file, mode="r") as f:
            targets = f.readlines()

        # フォローした人たちの読み込み
        with open(follows, mode='r') as f:
            my_follow_file = f.read()
        my_follow = my_follow_file.split()

        # スクレイピング
        options = webdriver.ChromeOptions()

        serv = Service(ChromeDriverManager().install())  # driverの自動更新

        # ヘッドレスモード
        options.headless = True
        options.add_argument('--disable-gpu')

        # 画像非表示
        options.add_argument('--blink-settings=imagesEnabled=false')

        # 読み込み待ち回避
        desired = DesiredCapabilities().CHROME
        desired['pageLoadStrategy'] = 'none'

        # user_profile = 'UserProfile'
        # options.add_argument('--user-data-dir=' + user_profile)
        # driver = webdriver.Chrome(options=options, desired_capabilities=desired)
        driver = webdriver.Chrome(options=options)
        driver.set_window_size(1500, 1500)
        driver.set_page_load_timeout(20)

        driver.get(f"{targets[0][3:]}reviews/?lo=1")
        driver.implicitly_wait(5)
        driver.execute_script("window.scrollTo(0, 0)")
        driver.find_element(By.ID, value='login_header').click()
        driver.find_element(By.ID, value='user').send_keys(self.username)
        driver.find_element(By.ID, value='pass').send_keys(self.password)
        time.sleep(1)
        driver.find_element(By.ID, value='submitLogin').click()
        time.sleep(1)

        wait = WebDriverWait(driver, 3)

        print(self.username)

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
            print(tar_url)
            my_log.append(tar_url)
            while cou < many:
                try:
                    wait.until(EC.alert_is_present())
                    alert = driver.switch_to.alert
                    # print(alert.text)
                    alert.accept()
                except:
                    pass

                # 表示されたページのメンバーのURLを取得
                try:
                    WebDriverWait(driver, 10).until(
                        EC.visibility_of_element_located((By.CLASS_NAME, "review-item-shopnameButton")))
                    members = driver.find_elements(By.CLASS_NAME, value='review-item-shopnameButton')
                    ac_url = []

                    now_url = driver.current_url
                    print(now_url)
                    my_log.append(now_url)
                    time.sleep(2)

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
                    # for i in range(len(members)):
                    for i in ac_url:
                        url = i
                        # url = driver.find_elements(By.CLASS_NAME, value='review-item-shopnameButton')[i].find_element(
                        #     By.TAG_NAME, value="a").get_attribute(name="href")
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
                                try:
                                    alert = driver.switch_to.alert
                                    print(alert.text)
                                    my_log.append(alert.text)
                                    alert.accept()
                                except:
                                    pass
                                # wait.until(EC.element_to_be_clickable((By.CLASS_NAME, "kitene_send")))

                                # driver.save_screenshot("スクショ.img")
                                WebDriverWait(driver, 10).until(
                                    EC.visibility_of_element_located((By.CLASS_NAME, "kitene_send")))
                                kitene = driver.find_element(By.CLASS_NAME, value="kitene_send")
                                kitene.click()
                                # time.sleep(1)
                                # wait.until(EC.alert_is_present())
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
                            driver.back()
                            # time.sleep(1)

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
                    time.sleep(3)
                    print(driver.current_url)
                    print("次のページに進みます")
                    my_log.append("次のページに進みます")
                    WebDriverWait(driver, 10).until(
                        EC.visibility_of_element_located((By.CLASS_NAME, "next")))
                    driver.get(driver.find_element(By.CLASS_NAME, value='next').get_attribute(name='href'))
                except:
                    print("次のページはありません")
                    my_log.append("次のページはありません")
                    break

            # キテねした人をフォローリストに追加
            with open(follows, mode="w") as f:
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

        driver.close()

        logs = f"logs/{self.username}/log.txt"
        with open(logs, mode="w") as f:
            for d in my_log:
                f.write("%s\n" % d)


if __name__ == '__main__':
    # 時間のカウント
    time_sta = time.perf_counter()

    # ユーザー情報の取り込み
    users = []
    with open("account.txt", "r", encoding="utf-8") as f:
        # リストとして読み込む
        lines = f.readlines()

    for line in lines:
        li = line.strip('\n')
        l = li.split(" ")
        users.append(l)

    for user in users:
        test = Spgirl_Auto(user[0], user[1])
        test.url_read_kitene()
        test.kitene_limit()

    # 時間を測る
    time_end = time.perf_counter()
    tim = time_end - time_sta

    print(tim)
