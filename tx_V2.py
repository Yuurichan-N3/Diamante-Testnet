import os
import sys
import random
import asyncio
from datetime import datetime
from dotenv import load_dotenv
from eth_account import Account
from eth_account.messages import encode_defunct
from colorama import Fore, Style, init
import pyfiglet
from curl_cffi.requests import AsyncSession

BASE_URL = "https://campapi.diamante.io/api/v1"

init(autoreset=False)

BOLD = Style.BRIGHT
RESET = Style.RESET_ALL
GREEN = Fore.GREEN + BOLD
YELLOW = Fore.YELLOW + BOLD
RED = Fore.RED + BOLD

ASCII_BANNER = pyfiglet.figlet_format("Yuurisandesu", font="standard")
LOG_LINES = []
INFO_TOGGLE = 0


def set_title():
    sys.stdout.write("\x1b]2;Diamante Testnet by : 佐賀県産 (YUURI)\x1b\\")
    sys.stdout.flush()


def render_screen():
    os.system("cls" if os.name == "nt" else "clear")
    print(Fore.CYAN + Style.BRIGHT + ASCII_BANNER + RESET)
    print(Fore.MAGENTA + Style.BRIGHT + "Welcome to Yuuri Diamante Testnet" + RESET)
    print(GREEN + "Ready to hack the world" + RESET)
    print(
        YELLOW
        + BOLD
        + "Current time "
        + datetime.now().strftime("%d/%m/%Y %H:%M:%S")
        + RESET
    )
    print()


def banner():
    render_screen()


def log_info(message):
    global INFO_TOGGLE
    if INFO_TOGGLE == 0:
        color = GREEN
        INFO_TOGGLE = 1
    else:
        color = YELLOW
        INFO_TOGGLE = 0
    line = color + "INFO " + message + RESET
    LOG_LINES.append(line)
    print(line)


def log_warn(message):
    line = YELLOW + "WARN " + message + RESET
    LOG_LINES.append(line)
    print(line)


def log_error(message):
    line = RED + "ERROR " + message + RESET
    LOG_LINES.append(line)
    print(line)


def LG(message):
    log_info(message)


def load_private_keys():
    load_dotenv()
    items = []
    for key, value in os.environ.items():
        if key.startswith("PRIVATEKEY_") and value:
            try:
                index = int(key.split("_", 1)[1])
            except ValueError:
                index = 0
            items.append((index, value.strip()))
    items.sort(key=lambda pair: pair[0])
    keys = [value for _, value in items]
    return keys


async def build_session():
    access_header = os.getenv("ACCESS_HEADER_TOKEN", "key")
    access_cookie = os.getenv("ACCESS_TOKEN_COOKIE", "").strip()
    
    headers = {
        "accept": "application/json, text/plain, */*",
        "accept-language": "ja,en-US;q=0.9,en;q=0.8",
        "access-token": access_header,
        "cache-control": "no-cache",
        "origin": "https://campaign.diamante.io",
        "pragma": "no-cache",
        "referer": "https://campaign.diamante.io/",
        "user-agent": (
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
            "AppleWebKit/537.36 (KHTML, like Gecko) "
            "Chrome/143.0.0.0 Safari/537.36 Edg/143.0.0.0"
        ),
        "sec-ch-ua": '"Microsoft Edge";v="143", "Chromium";v="143", "Not?A_Brand";v="24"',
        "sec-ch-ua-mobile": "?0",
        "sec-ch-ua-platform": '"Windows"',
        "sec-fetch-dest": "empty",
        "sec-fetch-mode": "cors",
        "sec-fetch-site": "same-site",
    }
    
    cookies = {}
    if access_cookie:
        cookies["access_token"] = access_cookie
    
    session = AsyncSession(
        headers=headers,
        impersonate="chrome110",
        timeout=20
    )
    
    if cookies:
        session.cookies.update(cookies)
    
    return session


async def refresh_session(session):
    access_header = os.getenv("ACCESS_HEADER_TOKEN", "key")
    access_cookie = os.getenv("ACCESS_TOKEN_COOKIE", "").strip()
    
    session.headers["access-token"] = access_header
    
    if access_cookie:
        session.cookies.update({"access_token": access_cookie})


async def send_request(session, method, url, **kwargs):
    attempt = 0
    while True:
        attempt += 1
        try:
            if method == "GET":
                resp = await session.get(url, **kwargs)
            else:
                resp = await session.post(url, **kwargs)
            
            status = resp.status_code
            if status == 200:
                data = resp.json()
            else:
                _ = resp.text
                
        except Exception as e:
            log_error(f"Network failure during request: {str(e)}")
            return None
            
        if status == 429:
            if attempt >= 5:
                log_error("Rate limit persists request aborted")
                return None
            wait_time = 3 * attempt
            log_warn("Rate limit detected wait " + str(wait_time) + " second")
            await asyncio.sleep(wait_time)
            continue
            
        if status in (401, 403):
            log_error("Access token appears invalid or expired")
            return None
            
        if status != 200:
            log_error(f"Request http status not successful: {status}")
            return None
            
        return data


def generate_device_payload(address, index):
    base_lat = 35.6895
    base_lng = 139.6917
    jitter_lat = (random.random() - 0.5) * 0.02
    jitter_lng = (random.random() - 0.5) * 0.02
    latitude = base_lat + jitter_lat + index * 0.0003
    longitude = base_lng + jitter_lng - index * 0.0003
    ip_last = 40 + (index % 150)
    ip_value = "153.127.0." + str(ip_last)
    device_id = "DEVJP" + str(1000 + index)
    cities = ["Tokyo", "Osaka", "Yokohama", "Sapporo", "Nagoya", "Fukuoka"]
    regions = ["Tokyo", "Osaka", "Kanagawa", "Hokkaido", "Aichi", "Fukuoka"]
    city_value = cities[(index - 1) % len(cities)]
    region_value = regions[(index - 1) % len(regions)]
    payload = {
        "address": address,
        "deviceId": device_id,
        "deviceSource": "web_app",
        "deviceType": "Windows",
        "browser": "Edge",
        "ipAddress": ip_value,
        "latitude": latitude,
        "longitude": longitude,
        "countryCode": "JP",
        "country": "Japan",
        "continent": "Asia",
        "continentCode": "AS",
        "region": region_value,
        "regionCode": "Unknown",
        "city": city_value,
    }
    return payload


async def connect_wallet(session, address, index):
    payload = generate_device_payload(address, index)
    log_info("Connect wallet request started for address")
    data = await send_request(
        session,
        "POST",
        BASE_URL + "/user/connect-wallet",
        json=payload,
    )
    if data is None:
        log_error("Connect wallet request can not be completed")
        return None
    if not data.get("success"):
        log_error("Connect wallet response indicates failure")
        return None
    user_data = data.get("data") or {}
    user_id = user_data.get("userId")
    if not user_id:
        log_error("Connect wallet did not return user id")
        return None
    log_info("User id acquired for current wallet")
    return user_id


def login_with_signature(private_key, address):
    message_text = "Diamante wallet login"
    message = encode_defunct(text=message_text)
    try:
        Account.sign_message(message, private_key=private_key)
    except Exception:
        log_error("Login signature failure for wallet")
        return False
    log_info("Login signature created for wallet")
    return True


async def claim_mystery_box(session, user_id):
    url = BASE_URL + "/mystery/claim/" + user_id
    log_info("Mystery box claim request started")
    data = await send_request(session, "GET", url)
    if data is None:
        return False
    if not data.get("success"):
        log_error("Mystery box claim response indicates failure")
        return False
    reward_data = data.get("data") or {}
    desc = reward_data.get("description")
    reward = reward_data.get("mysteryReward")
    reward_type = reward_data.get("rewardType")
    msg_parts = ["Mystery box claim success"]
    if desc:
        msg_parts.append("description " + str(desc))
    if reward is not None:
        msg_parts.append("reward " + str(reward))
    if reward_type:
        msg_parts.append("type " + str(reward_type))
    log_info(" ".join(msg_parts))
    return True


async def claim_faucet_balance(session, user_id):
    url = BASE_URL + "/transaction/get-balance/" + user_id
    log_info("Faucet balance request started")
    data = await send_request(session, "GET", url)
    if data is None:
        return None
    if not data.get("success"):
        log_error("Faucet balance response indicates failure")
        return None
    balance_data = data.get("data") or {}
    balance_value = balance_data.get("balance")
    if balance_value is None:
        log_warn("Faucet balance field not available")
        return None
    message = "Current faucet balance " + str(balance_value)
    log_info(message)
    return balance_value


async def fetch_user_status(session, user_id):
    url = BASE_URL + "/auth/get-user-status/" + user_id
    log_info("User status request started")
    data = await send_request(session, "GET", url)
    if data is None:
        return None
    if not data.get("success"):
        log_error("User status response indicates failure")
        return None
    status = data.get("data") or {}
    tx_count = status.get("transactionCount")
    badge_count = status.get("badgeCount")
    message = (
        "User status transaction count "
        + str(tx_count)
        + " badge count "
        + str(badge_count)
    )
    log_info(message)
    return status


async def fetch_leaderboard_entry(session, user_id):
    url = BASE_URL + "/leaderboard/user/" + user_id + "?limit=20&page=1"
    log_info("Leaderboard request started")
    data = await send_request(session, "GET", url)
    if data is None:
        return None
    if not data.get("success"):
        log_error("Leaderboard response indicates failure")
        return None
    container = data.get("data") or {}
    rows = container.get("data") or []
    if not isinstance(rows, list):
        log_warn("Leaderboard data format not expected")
        return None
    entry = None
    for item in rows:
        if isinstance(item, dict) and item.get("userId") == user_id:
            entry = item
            break
    if entry is None:
        log_warn("Leaderboard entry for current user not found")
        return None
    rank = entry.get("rank")
    total_xp = entry.get("totalXP")
    tx_count = entry.get("transactionCount")
    badges = entry.get("badges") or []
    badge_text = " ".join(str(badge) for badge in badges)
    message = (
        "Leaderboard summary rank "
        + str(rank)
        + " total xp "
        + str(total_xp)
        + " transaction count "
        + str(tx_count)
        + " badges "
        + badge_text
    )
    log_info(message)
    return entry


async def perform_single_transfer(session, user_id, attempt_index, state):
    temp_account = Account.create()
    to_address = temp_account.address
    payload = {
        "toAddress": to_address,
        "amount": 1,
        "userId": user_id,
    }
    log_info("Transfer attempt " + str(attempt_index) + " started")
    data = await send_request(
        session,
        "POST",
        BASE_URL + "/transaction/transfer",
        json=payload,
    )
    if data is None:
        state["failure_streak"] += 1
        log_warn("Transfer request failure wait 15 second before next attempt")
        if state["failure_streak"] >= 2:
            log_warn("Transfer failure streak reached 2 refreshing session")
            await refresh_session(session)
            state["failure_streak"] = 0
        await asyncio.sleep(15)
        return False
    if not data.get("success"):
        state["failure_streak"] += 1
        log_error("Transfer response indicates failure")
        log_warn("Wait 15 second before next transfer attempt")
        if state["failure_streak"] >= 2:
            log_warn("Transfer failure streak reached 2 refreshing session")
            await refresh_session(session)
            state["failure_streak"] = 0
        await asyncio.sleep(15)
        return False
    
    state["failure_streak"] = 0
    state["success_count"] += 1
    log_info("Transfer success for current attempt")
    
    transfer_container = data.get("data") or {}
    box_info = transfer_container.get("mysteryBoxInfo") or {}
    if isinstance(box_info, dict) and box_info:
        current = box_info.get("current")
        minimum = box_info.get("min")
        eligible = box_info.get("eligible")
        log_info(
            "Mystery box progress current "
            + str(current)
            + " min "
            + str(minimum)
            + " eligible "
            + str(eligible)
        )
        if eligible is True:
            await claim_mystery_box(session, user_id)
    
    if state["success_count"] % 5 == 0:
        await fetch_leaderboard_entry(session, user_id)
    
    cooldown_time = random.randint(58, 60)
    log_info(f"Cooldown {cooldown_time} seconds before next transfer")
    await asyncio.sleep(cooldown_time)
    
    return True


async def perform_transfer(session, user_id, count):
    state = {"success_count": 0, "failure_streak": 0}
    attempt_index = 1
    
    while attempt_index <= count:
        success = await perform_single_transfer(
            session,
            user_id,
            attempt_index,
            state,
        )
        
        if success:
            attempt_index += 1
    
    return state["success_count"]


async def process_wallet(session, position, private_key, address, transfer_count):
    log_info("Processing wallet " + str(position))
    
    user_id = await connect_wallet(session, address, position)
    if not user_id:
        log_error("User id can not be resolved for current wallet")
        return 0
    
    if not login_with_signature(private_key, address):
        log_error("Login step failed for current wallet")
        return 0
    
    await claim_faucet_balance(session, user_id)
    await fetch_user_status(session, user_id)
    await fetch_leaderboard_entry(session, user_id)
    
    completed = await perform_transfer(
        session,
        user_id,
        transfer_count,
    )
    
    log_info(
        "Completed transfer count "
        + str(completed)
        + " for current wallet"
    )
    
    return completed


async def main():
    set_title()
    render_screen()
    private_keys = load_private_keys()
    
    if not private_keys:
        log_error("Private key data not found in environment")
        return
    
    try:
        count_text = input(
            YELLOW + "INPUT enter transfer count per wallet " + RESET
        ).strip()
        try:
            transfer_count = int(count_text)
        except ValueError:
            log_error("Transfer count input is not a valid integer")
            return
        
        if transfer_count <= 0:
            log_error("Transfer count must be a positive integer")
            return
        
        if transfer_count > 1000:
            log_warn("Transfer count too large limit to 1000 per wallet recommended 10")
            transfer_count = 1000
        else:
            log_info("Recommended transfer count per wallet is 10 for long running loop")
    except KeyboardInterrupt:
        log_warn("Input interrupted by user")
        return
    
    wallet_entries = []
    for position, private_key in enumerate(private_keys, start=1):
        try:
            account = Account.from_key(private_key)
        except Exception:
            log_error("Private key can not be decoded for one wallet")
            continue
        address = account.address
        wallet_entries.append((position, private_key, address))
    
    if not wallet_entries:
        log_error("No valid wallet entries available")
        return
    
    session = await build_session()
    
    try:
        wallet_total = len(wallet_entries)
        log_info("Total wallet count " + str(wallet_total))
        
        cycle_count = 0
        while True:
            cycle_count += 1
            log_info(f"Starting cycle {cycle_count}")
            
            total_completed = 0
            
            for position, private_key, address in wallet_entries:
                completed = await process_wallet(
                    session,
                    position,
                    private_key,
                    address,
                    transfer_count
                )
                total_completed += completed
            
            log_info(f"Cycle {cycle_count} completed - Total transfers: {total_completed}")
            
            log_info("Waiting 60 seconds before next cycle...")
            await asyncio.sleep(60)
        
    except KeyboardInterrupt:
        log_info("Process interrupted by user")
    finally:
        await session.close()


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print()
        log_info("Process terminated")
        sys.exit()
