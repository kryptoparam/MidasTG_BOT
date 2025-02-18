import cloudscraper
import time
import random
from pyfiglet import Figlet

CYAN = '\033[96m'
GREEN = '\033[92m'
RED = '\033[91m'
YELLOW = '\033[93m'
MAGENTA = '\033[95m'
RESET = '\033[0m'

def print_intro():
    """Prints the introductory banner."""
    f = Figlet(font='starwars')
    ascii_art = f.renderText('MIdas B0T')
    print('\033[94m' + ascii_art + '\033[0m')
    print(f"{GREEN}📡 Farming MIDAS{RESET}")

    answer = input(f"{RED}Will you F** Midas Airdrop? (Y/N): {RESET}")
    if answer.lower() != 'y':
        print(f"{RED}Aborting installation.{RESET}")
        exit(1)

def debug(message):
    print(f"{MAGENTA}[DEBUG]: {message}{RESET}")

def post_request(url, headers, payload=None, proxies=None):
    scraper = cloudscraper.create_scraper()
    if proxies:
        scraper.proxies.update(proxies)
    try:
        response = scraper.post(url, json=payload, headers=headers)
        if response.status_code in [200, 201]:
            try:
                return response.json(), response.cookies
            except ValueError:
                return response.text, response.cookies
        else:
            print(f"{RED}Error: Request failed. Status code: {response.status_code}{RESET}")
            debug(f"Response text: {response.text}")
            return None, None
    except Exception as e:
        print(f"{RED}Error: {e}{RESET}")
        debug(f"URL: {url}, Headers: {headers}, Payload: {payload}")
        return None, None

def get_request(url, headers, proxies=None):
    scraper = cloudscraper.create_scraper()
    if proxies:
        scraper.proxies.update(proxies)
    try:
        response = scraper.get(url, headers=headers)
        if response.status_code == 200:
            try:
                return response.json()
            except ValueError:
                print(f"{RED}Response is not JSON.{RESET}")
                debug(f"Response text: {response.text}")
                return None
        else:
            print(f"{RED}Error: Request failed. Status code: {response.status_code}{RESET}")
            debug(f"Response text: {response.text}")
            return None
    except Exception as e:
        print(f"{RED}Error: {e}{RESET}")
        debug(f"URL: {url}, Headers: {headers}")
        return None

def read_file(filename):
    try:
        with open(filename, 'r') as file:
            return [line.strip() for line in file if line.strip()]
    except FileNotFoundError:
        print(f"{RED}File {filename} not found.{RESET}")
        debug(f"Attempted to read file: {filename}")
        return []

def validate_proxy(proxy):
    test_url = "http://api64.ipify.org?format=json"
    try:
        scraper = cloudscraper.create_scraper()
        scraper.proxies.update(proxy)
        response = scraper.get(test_url, timeout=10)
        if response.status_code == 200:
            ip = response.json().get('ip')
            print(f"{GREEN}Proxy is working: {ip}{RESET}")
            return True
        else:
            print(f"{RED}Proxy test failed with status code: {response.status_code}{RESET}")
            return False
    except Exception as e:
        print(f"{RED}Proxy validation error: {e}{RESET}")
        debug(f"Proxy: {proxy}")
        return False

def get_streak_info(headers, proxies):
    url_streak = "https://api-tg-app.midas.app/api/streak"
    streak_data = get_request(url_streak, headers, proxies)

    if streak_data:
        streak_days_count = streak_data.get("streakDaysCount", "Not found")
        next_rewards = streak_data.get("nextRewards", {})
        points = next_rewards.get("points", "Not found")
        tickets = next_rewards.get("tickets", "Not found")
        claimable = streak_data.get("claimable", False)

        print(f"Streak Days Count: {streak_days_count}")
        print(f"Claimable Rewards - Points: {GREEN}{points}{RESET}, Tickets: {GREEN}{tickets}{RESET}")

        if tickets > 0:
            play_game(headers, proxies, tickets)

        if claimable:
            print(f"{GREEN}Streak is available to claim.{RESET}")
            claim_streak(headers, proxies)
        else:
            print(f"{YELLOW}Streak is not available to claim.{RESET}")
    else:
        print(f"{RED}Error: Unable to access streak API.{RESET}")

def claim_streak(headers, proxies):
    url_claim = "https://api-tg-app.midas.app/api/streak"
    response, _ = post_request(url_claim, headers, proxies=proxies)

    if response:
        print(f"{GREEN}Successfully claimed daily streak rewards!{RESET}")
    else:
        print(f"{RED}Error: Failed to claim daily streak rewards.{RESET}")

def process_tasks(headers, proxies):
    url_tasks = "https://api-tg-app.midas.app/api/tasks/available"
    tasks = get_request(url_tasks, headers, proxies)

    if tasks:
        for task in tasks:
            task_name = task.get("name", "Unknown")
            state = task.get("state", "UNKNOWN")

            if state == "COMPLETED":
                print(f"Task: {GREEN}{task_name}{RESET}, State: {GREEN}{state}{RESET}")
            elif state == "CLAIMABLE":
                print(f"Task: {CYAN}{task_name}{RESET}, State: {GREEN}{state}{RESET}")
                claim_task(task.get("id"), headers, proxies)
                time.sleep(1)  # Sleep between tasks
            elif state == "WAITING":
                print(f"Task: {CYAN}{task_name}{RESET}, State: {YELLOW}{state}{RESET}")
                if start_task(task.get("id"), headers, proxies):
                    print(f"{YELLOW}Task '{task_name}' started. Waiting for 10 seconds before claiming...{RESET}")
                    time.sleep(10)  # Wait for task verification
                    claim_task(task.get("id"), headers, proxies)
            else:
                print(f"Task: {CYAN}{task_name}{RESET}, State: {RED}{state}{RESET}")

def play_game(headers, proxies, tickets):
    url_game = "https://api-tg-app.midas.app/api/game/play"
    total_points = 0

    while tickets > 0:
        print(f"{YELLOW}Playing game... Tickets left: {tickets}{RESET}")
        response, _ = post_request(url_game, headers, proxies=proxies)

        if response:
            points_earned = response.get("points", 0)
            total_points += points_earned
            tickets -= 1
            print(f"{GREEN}Earned {points_earned} points. Total points: {total_points}{RESET}")
        else:
            print(f"{RED}Error: Failed to play game.{RESET}")
            break

        time.sleep(2)  # Small delay between games

    print(f"{GREEN}Finished playing games. Total points earned: {total_points}{RESET}")

def claim_task(task_id, headers, proxies):
    url_claim = f"https://api-tg-app.midas.app/api/tasks/claim/{task_id}"
    response, _ = post_request(url_claim, headers, proxies=proxies)

    if response:
        print(f"{GREEN}Task claimed successfully!{RESET}")
    else:
        print(f"{RED}Error: Failed to claim task {task_id}.{RESET}")

def start_task(task_id, headers, proxies):
    url_start = f"https://api-tg-app.midas.app/api/tasks/start/{task_id}"
    response, _ = post_request(url_start, headers, proxies=proxies)

    if response:
        print(f"{GREEN}Task started successfully!{RESET}")
        return response.get("state") == "CLAIMABLE"
    else:
        print(f"{RED}Error: Failed to start task {task_id}.{RESET}")
        return False

def process_account(init_data, proxies):
    print(f"\nProcessing initData: {YELLOW}...{init_data[-20:]}{RESET}")

    if proxies and not validate_proxy(proxies):
        print(f"{RED}Skipping account due to invalid proxy.{RESET}")
        return

    url_register = "https://api-tg-app.midas.app/api/auth/register"
    headers_register = {
        "Accept": "application/json, text/plain, */*",
        "Origin": "https://prod-tg-app.midas.app",
        "Referer": "https://prod-tg-app.midas.app/",
        "User-Agent": "Mozilla/5.0 (Linux; Android 10; K) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Mobile Safari/537.36"
    }

    payload = {
        "initData": init_data
    }

    response_text, cookies = post_request(url_register, headers_register, payload, proxies=proxies)

    if response_text:
        print(f"Obtained token: {YELLOW}...{response_text[-20:]}{RESET}")
        cookies_dict = cookies.get_dict()
        token = response_text

        headers_user = {
            "Accept": "application/json, text/plain, */*",
            "Origin": "https://prod-tg-app.midas.app",
            "Referer": "https://prod-tg-app.midas.app/",
            "User-Agent": "Mozilla/5.0 (Linux; Android 10; K) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Mobile Safari/537.36",
            "Authorization": f"Bearer {token}",
            "Cookie": "; ".join([f"{key}={value}" for key, value in cookies_dict.items()])
        }

        debug(f"Headers for user: {headers_user}")
        get_streak_info(headers_user, proxies)
        process_tasks(headers_user, proxies)

def main():
    print_intro()

    init_data_list = read_file('auth.txt')
    proxy_list = read_file('proxy.txt')

    while True:
        for i, init_data in enumerate(init_data_list):
            proxies = None
            if i < len(proxy_list):
                proxy = proxy_list[i]
                if proxy.startswith("socks5://"):
                    proxies = {
                        "http": proxy,
                        "https": proxy
                    }
                elif "@" in proxy:  
                    auth, address = proxy.split("@")
                    proxies = {
                        "http": f"http://{auth}@{address}",
                        "https": f"https://{auth}@{address}"
                    }
                else:  
                    proxies = {
                        "http": f"http://{proxy}",
                        "https": f"https://{proxy}"
                    }

                debug(f"Processed proxy: {proxies}")

            process_account(init_data, proxies)

        print(f"{YELLOW}All accounts processed. Sleeping for 8 hours...{RESET}")
        time.sleep(8 * 3600)

if __name__ == "__main__":
    main()
