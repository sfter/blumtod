import os
import sys
import time
import json
import random
import requests
import argparse
from json import dumps as dp, loads as ld
from datetime import datetime
from colorama import *
from urllib.parse import unquote, parse_qs
from base64 import b64decode

init(autoreset=True)

merah = Fore.LIGHTRED_EX
putih = Fore.LIGHTWHITE_EX
hijau = Fore.LIGHTGREEN_EX
kuning = Fore.LIGHTYELLOW_EX
biru = Fore.LIGHTBLUE_EX
reset = Style.RESET_ALL
hitam = Fore.LIGHTBLACK_EX


class BlumTod:
    def __init__(self):
        self.base_headers = {
            "accept": "application/json, text/plain, */*",
            "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125.0.0.0 Safari/537.36 Edg/125.0.0.0",
            "content-type": "application/json",
            "origin": "https://telegram.blum.codes",
            "x-requested-with": "org.telegram.messenger",
            "sec-fetch-site": "same-site",
            "sec-fetch-mode": "cors",
            "sec-fetch-dest": "empty",
            "referer": "https://telegram.blum.codes/",
            "accept-encoding": "gzip, deflate",
            "accept-language": "en,en-US;q=0.9",
        }
        self.garis = putih + "~" * 50

    def renew_access_token(self, tg_data):
        headers = self.base_headers.copy()
        data = dp(
            {
                "query": tg_data,
            },
        )
        headers["Content-Length"] = str(len(data))
        url = "https://user-domain.blum.codes/api/v1/auth/provider/PROVIDER_TELEGRAM_MINI_APP"
        res = self.http(url, headers, data)
        if "token" not in res.json().keys():
            self.log(f"{merah}'token' is not found in response, check you data !!")
            return False

        access_token = res.json()["token"]["access"]
        self.log(f"{hijau}success get access token ")
        return access_token

    def check_tasks(self, token):
        headers = {
            'Authorization': f'Bearer {token}',
            'accept': 'application/json, text/plain, */*',
            'accept-language': 'en-US,en;q=0.9',
            'content-length': '0',
            'origin': 'https://telegram.blum.codes',
            'priority': 'u=1, i',
            'sec-ch-ua': '"Microsoft Edge";v="125", "Chromium";v="125", "Not.A/Brand";v="24", "Microsoft Edge WebView2";v="125"',
            'sec-ch-ua-mobile': '?0',
            'sec-ch-ua-platform': '"Windows"',
            'sec-fetch-dest': 'empty',
            'sec-fetch-mode': 'cors',
            'sec-fetch-site': 'same-site',
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125.0.0.0 Safari/537.36 Edg/125.0.0.0'
        }
    
        try:
            response = requests.get('https://game-domain.blum.codes/api/v1/tasks', headers=headers)
            if response.status_code == 200:
                tasks = response.json()
                for task in tasks:
                    titlenya = task['title']
                    print(f"{Fore.YELLOW+Style.BRIGHT}Checking Task: {titlenya} Lists")
                    taskList = task.get('tasks', [])
                    for lists in taskList:
                        task_status = lists.get('status', None)
                        task_title = lists.get('title', None)
                        if task_status == 'FINISHED':
                            print(f"{Fore.CYAN+Style.BRIGHT}Task {task_title} already claimed")
                        elif task_status == 'NOT_STARTED':
                            print(f"{Fore.YELLOW+Style.BRIGHT}Starting Task: {task_title}")
                            self.start_task(token, lists['id'], task_title)
                            self.claim_task(token, lists['id'], task_title)
                        # Check for subtasks
                        subTasks = lists.get('subTasks', [])
                        for subtask in subTasks:
                            subtask_status = subtask.get('status', None)
                            subtask_title = subtask.get('title', None)
                            if subtask_status == 'NOT_STARTED':
                                print(f"{Fore.YELLOW+Style.BRIGHT}Starting Subtask: {subtask_title}")
                                self.start_subtask(token, subtask['id'], subtask_title)
                                self.claim_subtask(token, subtask['id'], subtask_title)
            else:
                print(f"{Fore.RED+Style.BRIGHT}\nFailed to get tasks")
        except Exception as e:
            print(f"{Fore.RED+Style.BRIGHT}\nFailed to get tasks Error Code: {response.status_code} | {str(e)}")

    def start_task(self, token, task_id,titlenya):
        url = f'https://game-domain.blum.codes/api/v1/tasks/{task_id}/start'
        headers = {
            'Authorization': f'Bearer {token}',
            'accept': 'application/json, text/plain, */*',
            'accept-language': 'en-US,en;q=0.9',
            'content-length': '0',
            'origin': 'https://telegram.blum.codes',
            'priority': 'u=1, i',
            'sec-ch-ua': '"Microsoft Edge";v="125", "Chromium";v="125", "Not.A/Brand";v="24", "Microsoft Edge WebView2";v="125"',
            'sec-ch-ua-mobile': '?0',
            'sec-ch-ua-platform': '"Windows"',
            'sec-fetch-dest': 'empty',
            'sec-fetch-mode': 'cors',
            'sec-fetch-site': 'same-site',
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125.0.0.0 Safari/537.36 Edg/125.0.0.0'
        }
        try:
            response = requests.post(url, headers=headers)
            if response.status_code == 200:
                print(f"{Fore.GREEN+Style.BRIGHT}\nTask {titlenya} started")
            else:
                print(f"{Fore.RED+Style.BRIGHT}\nFailed to start task {titlenya} {response.json()}")
            return 
        except:
            print(f"{Fore.RED+Style.BRIGHT}\nFailed to start task {titlenya} {response.status_code} ")

    def start_subtask(self, token, subtask_id, title):
        url = f'https://game-domain.blum.codes/api/v1/tasks/{subtask_id}/start'
        headers = {
            'Authorization': f'Bearer {token}',
            'accept': 'application/json, text/plain, */*',
            'accept-language': 'en-US,en;q=0.9',
            'content-length': '0',
            'origin': 'https://telegram.blum.codes',
            'priority': 'u=1, i',
            'sec-ch-ua': '"Microsoft Edge";v="125", "Chromium";v="125", "Not.A/Brand";v="24", "Microsoft Edge WebView2";v="125"',
            'sec-ch-ua-mobile': '?0',
            'sec-ch-ua-platform': '"Windows"',
            'sec-fetch-dest': 'empty',
            'sec-fetch-mode': 'cors',
            'sec-fetch-site': 'same-site',
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125.0.0.0 Safari/537.36 Edg/125.0.0.0'
        }
        try:
            response = requests.post(url, headers=headers)
            if response.status_code == 200:
                print(f"{Fore.GREEN+Style.BRIGHT}\nSubtask {title} started")
            else:
                print(f"{Fore.RED+Style.BRIGHT}\nFailed to start subtask {title} {response.json()}")
        except Exception as e:
            print(f"{Fore.RED+Style.BRIGHT}\nFailed to start subtask {title} due to error: {str(e)}")

    def claim_subtask(self, token, subtask_id, title):
        print(f"{Fore.YELLOW+Style.BRIGHT}\nClaiming subtask {title}")
        url = f'https://game-domain.blum.codes/api/v1/tasks/{subtask_id}/claim'
        headers = {
            'Authorization': f'Bearer {token}',
            'accept': 'application/json, text/plain, */*',
            'accept-language': 'en-US,en;q=0.9',
            'content-length': '0',
            'origin': 'https://telegram.blum.codes',
            'priority': 'u=1, i',
            'sec-ch-ua': '"Microsoft Edge";v="125", "Chromium";v="125", "Not.A/Brand";v="24", "Microsoft Edge WebView2";v="125"',
            'sec-ch-ua-mobile': '?0',
            'sec-ch-ua-platform': '"Windows"',
            'sec-fetch-dest': 'empty',
            'sec-fetch-mode': 'cors',
            'sec-fetch-site': 'same-site',
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125.0.0.0 Safari/537.36 Edg/125.0.0.0'
        }
        try:
            response = requests.post(url, headers=headers)
            if response.status_code == 200:
                print(f"{Fore.CYAN+Style.BRIGHT}\nSubtask {title} claimed")
            else:
                print(f"{Fore.RED+Style.BRIGHT}\nFailed to claim subtask {title}")
        except Exception as e:
            print(f"{Fore.RED+Style.BRIGHT}\nFailed to claim subtask {title} due to error: {str(e)}")

    def claim_task(self, token, task_id,titlenya):
        print(f"{Fore.YELLOW+Style.BRIGHT}\nClaiming task {titlenya}")
        url = f'https://game-domain.blum.codes/api/v1/tasks/{task_id}/claim'
        headers = {
            'Authorization': f'Bearer {token}',
            'accept': 'application/json, text/plain, */*',
            'accept-language': 'en-US,en;q=0.9',
            'content-length': '0',
            'origin': 'https://telegram.blum.codes',
            'priority': 'u=1, i',
            'sec-ch-ua': '"Microsoft Edge";v="125", "Chromium";v="125", "Not.A/Brand";v="24", "Microsoft Edge WebView2";v="125"',
            'sec-ch-ua-mobile': '?0',
            'sec-ch-ua-platform': '"Windows"',
            'sec-fetch-dest': 'empty',
            'sec-fetch-mode': 'cors',
            'sec-fetch-site': 'same-site',
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125.0.0.0 Safari/537.36 Edg/125.0.0.0'
        }
        try:
            response = requests.post(url, headers=headers)
            if response.status_code == 200:
                print(f"{Fore.CYAN+Style.BRIGHT}\nTask {titlenya} claimed")
            else:
                print(f"{Fore.RED+Style.BRIGHT}\nFailed to claim task {titlenya}")
        except:
            print(f"{Fore.RED+Style.BRIGHT}\nFailed to claim task {titlenya} {response.status_code} ")

    def claim_farming(self, access_token):
        url = "https://game-domain.blum.codes/api/v1/farming/claim"
        headers = self.base_headers.copy()
        headers["Authorization"] = f"Bearer {access_token}"
        res = self.http(url, headers, "")
        balance = res.json()["availableBalance"]
        self.log(f"{hijau}balance after claim : {balance}")
        return

    def get_balance(self, access_token, only_show_balance=False):
        url = "https://game-domain.blum.codes/api/v1/user/balance"
        headers = self.base_headers.copy()
        headers["Authorization"] = f"Bearer {access_token}"
        res = self.http(url, headers)
        balance = res.json()["availableBalance"]
        self.log(f"{hijau}balance : {putih}{balance}")
        if only_show_balance:
            return
        timestamp = round(res.json()["timestamp"] / 1000)
        if "farming" not in res.json().keys():
            return False, "not_started"
        end_farming = round(res.json()["farming"]["endTime"] / 1000)
        if timestamp > end_farming:
            self.log(f"{hijau}now is time to claim farming !")
            return True, end_farming

        self.log(f"{kuning}not time to claim farming !")
        end_date = datetime.fromtimestamp(end_farming)
        self.log(f"{hijau}end farming : {putih}{end_date}")
        return False, end_farming

    def start_farming(self, access_token):
        url = "https://game-domain.blum.codes/api/v1/farming/start"
        headers = self.base_headers.copy()
        headers["Authorization"] = f"Bearer {access_token}"
        res = self.http(url, headers, "")
        end = res.json()["endTime"]
        end_date = datetime.fromtimestamp(end / 1000)
        self.log(f"{hijau}start farming successfully !")
        self.log(f"{hijau}end farming : {putih}{end_date}")
        return round(end / 1000)

    def get_friend(self, access_token):
        url = "https://gateway.blum.codes/v1/friends/balance"
        headers = self.base_headers.copy()
        headers["Authorization"] = f"Bearer {access_token}"
        res = self.http(url, headers)
        can_claim = res.json()["canClaim"]
        limit_invite = res.json()["limitInvitation"]
        amount_claim = res.json()["amountForClaim"]
        ref_code = res.json()["referralToken"]
        self.log(f"{putih}limit invitation : {hijau}{limit_invite}")
        self.log(f"{hijau}claim amount : {putih}{amount_claim}")
        self.log(f"{putih}can claim : {hijau}{can_claim}")
        if can_claim:
            url_claim = "https://gateway.blum.codes/v1/friends/claim"
            res = self.http(url_claim, headers, "")
            if "claimBalance" in res.json().keys():
                self.log(f"{hijau}success claim referral bonus !")
                return
            self.log(f"{merah}failed claim referral bonus !")
            return

    def checkin(self, access_token):
        url = "https://game-domain.blum.codes/api/v1/daily-reward?offset=-420"
        headers = self.base_headers.copy()
        headers["Authorization"] = f"Bearer {access_token}"
        res = self.http(url, headers)
        if res.status_code == 404:
            self.log(f"{kuning}already check in today !")
            return
        res = self.http(url, headers, "")
        if "ok" in res.text.lower():
            self.log(f"{hijau}success check in today !")
            return

        self.log(f"{merah}failed check in today !")
        return

    def playgame(self, access_token):
        url_play = "https://game-domain.blum.codes/api/v1/game/play"
        url_claim = "https://game-domain.blum.codes/api/v1/game/claim"
        url_balance = "https://game-domain.blum.codes/api/v1/user/balance"
        headers = self.base_headers.copy()
        headers["Authorization"] = f"Bearer {access_token}"
        res = self.http(url_balance, headers)
        play = res.json()["playPasses"]
        self.log(f"{hijau}you have {putih}{play}{hijau} game ticket")
        for i in range(play):
            try:
                res = self.http(url_play, headers, "")
                game_id = res.json()["gameId"]
                self.countdown(30)
                point = random.randint(self.MIN_WIN, self.MAX_WIN)
                data = json.dumps({"gameId": game_id, "points": point})
                res = self.http(url_claim, headers, data)
                if "OK" in res.text:
                    self.log(f"{hijau}success earn {putih}{point}{hijau} from game !")
                    self.get_balance(access_token, only_show_balance=True)
                    continue

                self.log(f"{merah}failed earn {putih}{point}{merah} from game !")
                continue
            except KeyError:
                print("KeyError: 'request blum json has error")

    def data_parsing(self, data):
        return {k: v[0] for k, v in parse_qs(data).items()}

    def log(self, message):
        now = datetime.now().isoformat(" ").split(".")[0]
        print(f"{hitam}[{now}]{reset} {message}")

    def get_local_token(self, userid):
        if not os.path.exists('tokens.json'):
            open("tokens.json", "w").write(json.dumps({}))
        tokens = json.loads(open("tokens.json", "r").read())
        if str(userid) not in tokens.keys():
            return False

        return tokens[str(userid)]

    def save_local_token(self, userid, token):
        tokens = json.loads(open("tokens.json", "r").read())
        tokens[str(userid)] = token
        open("tokens.json", "w").write(json.dumps(tokens, indent=4))

    def is_expired(self, token):
        header, payload, sign = token.split(".")
        payload = b64decode(payload + "==").decode()
        jload = json.loads(payload)
        now = round(datetime.now().timestamp())
        exp = jload['exp']
        if now > exp:
            return True

        return False

    def save_failed_token(self, userid, data):
        file = "auth_failed.json"
        if not os.path.exists(file):
            open(file, "w").write(json.dumps({}))

        acc = json.loads(open(file, 'r').read())
        if str(userid) in acc.keys():
            return

        acc[str(userid)] = data
        open(file, 'w').write(json.dumps(acc, indent=4))

    def load_config(self):
        config = json.loads(open('config.json', 'r').read())
        self.DEFAULT_INTERVAL = config['interval']
        self.MIN_WIN = config['game_point']['low']
        self.MAX_WIN = config['game_point']['high']
        if self.MIN_WIN > self.MAX_WIN:
            self.log(f"{kuning}high value must be higher than lower value")
            sys.exit()

    def http(self, url, headers, data=None):
        while True:
            try:
                if data is None:
                    headers["content-length"] = "0"
                    res = requests.get(url, headers=headers, timeout=30)
                    open("http.log", "a", encoding="utf-8").write(res.text + "\n")
                    if "<html>" in res.text:
                        self.log(f'{merah}failed fetch json response !')
                        time.sleep(2)
                        continue

                    return res

                if data == "":
                    res = requests.post(url, headers=headers, timeout=30)
                    open("http.log", "a", encoding="utf-8").write(res.text + "\n")
                    if "<html>" in res.text:
                        self.log(f'{merah}failed fetch json response !')
                        time.sleep(2)
                        continue

                    return res

                res = requests.post(url, headers=headers, data=data, timeout=30)
                open("http.log", "a", encoding="utf-8").write(res.text + "\n")
                if "<html>" in res.text:
                    self.log(f'{merah}failed fetch json response !')
                    time.sleep(2)
                    continue

                return res

            except (
                    requests.exceptions.ConnectionError,
                    requests.exceptions.ConnectTimeout,
                    requests.exceptions.ReadTimeout,
            ):
                self.log(f"{merah}connection error")

    def countdown(self, t):
        while t:
            menit, detik = divmod(t, 60)
            jam, menit = divmod(menit, 60)
            jam = str(jam).zfill(2)
            menit = str(menit).zfill(2)
            detik = str(detik).zfill(2)
            print(f"{putih}waiting until {jam}:{menit}:{detik} ", flush=True, end="\r")
            t -= 1
            time.sleep(1)
        print("                          ", flush=True, end="\r")

    def main(self):
        banner = f"""
    {hijau}AUTO CLAIM FOR {putih}BLUM {hijau}/ {biru}@BlumCryptoBot
    
    {hijau}By : {putih}t.me/AkasakaID
    {putih}Github : {hijau}@AkasakaID
    
    {hijau}Message : {putih}Dont forget to 'git pull' maybe i update the bot !
        """
        arg = argparse.ArgumentParser()
        arg.add_argument('--marinkitagawa', action="store_true", help="no clear the terminal !")
        arg.add_argument('--data', help="Custom data input (default: data.txt)", default="data.txt")
        arg.add_argument('--autotask', action="store_true", help="enable feature auto complete task !")
        arg.add_argument('--autogame', action='store_true', help="enable feature auto playing game !")
        args = arg.parse_args()
        if not args.marinkitagawa:
            os.system("cls" if os.name == "nt" else "clear")

        print(banner)
        if not os.path.exists(args.data):
            self.log(f'{merah}{args.data} not found, please input valid file name !')
            sys.exit()

        datas = open(args.data, "r").read().splitlines()
        self.log(f"{hijau}total account : {putih}{len(datas)}")
        if len(datas) <= 0:
            self.log(f"{merah}add data account in {args.data} first")
            sys.exit()

        self.log(self.garis)
        while True:
            try:
                list_countdown = []
                for no, data in enumerate(datas):
                    try:
                        self.log(f"{hijau}account number - {putih}{no + 1}")
                        data_parse = self.data_parsing(data)
                        user = json.loads(data_parse["user"])
                        userid = user['id']
                        self.log(f"{hijau}login as : {putih}{user['first_name']}")
                        access_token = self.get_local_token(userid)
                        failed_fetch_token = False
                        while True:
                            if access_token is False:
                                access_token = self.renew_access_token(data)
                                if access_token is False:
                                    self.save_failed_token(userid, data)
                                    failed_fetch_token = True
                                    break
                                self.save_local_token(userid, access_token)
                            expired = self.is_expired(access_token)
                            if expired:
                                access_token = False
                                continue
                            break
                        if failed_fetch_token:
                            continue
                        self.checkin(access_token)
                        self.get_friend(access_token)
                        if args.autotask:
                            self.check_tasks(access_token)
                        status, res_bal = self.get_balance(access_token)
                        if status:
                            self.claim_farming(access_token)
                            res_bal = self.start_farming(access_token)
                        if isinstance(res_bal, str):
                            res_bal = self.start_farming(access_token)
                        list_countdown.append(res_bal)
                        if args.autogame:
                            self.playgame(access_token)
                        self.log(self.garis)
                        self.countdown(self.DEFAULT_INTERVAL)
                    except KeyError:
                        print("KeyError: 'request blum json has error")

                min_countdown = min(list_countdown)
                now = int(time.time())
                result = min_countdown - now
                if result <= 0:
                    continue

                self.countdown(result)
            except KeyboardInterrupt:
                sys.exit()
            except BaseException as e:
                print(f"An error occurred: {e}")


if __name__ == "__main__":
    try:
        app = BlumTod()
        app.load_config()
        app.main()
    except KeyboardInterrupt:
        sys.exit()
