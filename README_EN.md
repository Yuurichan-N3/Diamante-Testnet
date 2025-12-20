# ⚡ Diamante Testnet Farming Script by Yuurisandesu (佐賀県産 YUURI)

## 📌 Overview  
These two Python scripts (`tx_V1.py` and `tx_V2.py`) are designed to automate **farming points/XP** on the **[Diamante Network Campaign Testnet](https://campaign.diamante.io)**.  
**Main goal:** Increase transactions, XP, leaderboard ranking, and claim mystery boxes for potential airdrop/rewards.  

Both scripts are created by the same author with identical banner displays and logging, but feature **different farming strategies**.

---

## 🔍 Similarities Between Both Scripts  
✅ Fetch private keys from the `.env` file (format: `PRIVATEKEY_1=...`, `PRIVATEKEY_2=...`, etc.)  
✅ Simulate device fingerprint (Japan location, unique deviceId, IP variation, latitude/longitude)  
✅ Use `access-token` header from `.env` (default: `"key"`)  
✅ Colored logging + ASCII banner **"Yuurisandesu"**  
✅ Connect wallet → obtain `userId` → perform repeated transfers  
✅ Handle rate limits (429), invalid tokens (401/403), and retry mechanisms  
✅ Run in an **infinite loop** until manually stopped (**Ctrl+C**)

---

## ⚖️ Key Differences

### 🚨 tx_V1.py (Version 1 – **Not Recommended but Faucet-Efficient**)
- **Strategy:** Aggressive – creates a new dummy account each cycle, registers with referral `"RO5-BL18"`, claims faucet, transfers small amounts to dummy, then sends back to a fixed address (`0x222306e34a54455aa10c215b26aaad3d6037dbf8`)  
- **Multi Wallet:** Supported, but not optimal due to infinite loop within the first wallet  
- **Transfer Input:** None (hardcoded, infinite per wallet)  
- **Additional Features:** Dummy account registration + fake Twitter handle + referral spam  
- **Monitoring:** Basic (balance + leaderboard once per wallet)  
- **Cooldown:** Fixed 60 seconds  
- **Risk:** High – easily detected as referral spam and faucet syphoning  
- **Recommendation:** ❌ Not recommended (outdated and campaign restrictions are stricter)

---

### ✅ tx_V2.py (Version 2 – **Recommended**)
- **Strategy:** Safe & simple – farming directly on main wallet, transfers 1 token to a new random address (token disposal)  
- **Multi Wallet:** Optimal – processes all wallets in rotation each cycle  
- **Transfer Input:** Yes – user is prompted to input the number of transfers per wallet per cycle (recommended: **10**)  
- **Additional Features:** Login with signature, cookie support, comprehensive monitoring (user status, mystery box progress per transfer, leaderboard every 5 transfers, badge info)  
- **Cooldown:** Random 58–60 seconds  
- **Risk:** Low – mimics normal user activity  
- **Recommendation:** ✅ **Use this version only** – more stable and secure

**🎯 Conclusion:** Use **tx_V2.py** only. V1 carries high risk and is less effective for multi-wallet operations.

---

## 🛠️ Usage Tutorial (Focus on tx_V2.py)

### 1. 📦 Preparation
- Install **Python 3.10** or newer
- Install dependencies:
  ```bash
  pip install python-dotenv eth-account colorama pyfiglet faker curl-cffi
  ```

### 2. 📁 Create a `.env` file (in the same folder as the script)
  ```env
  PRIVATEKEY_1=0xabcdef1234567890abcdef1234567890abcdef1234567890abcdef1234567890
  PRIVATEKEY_2=0x1234567890abcdef1234567890abcdef1234567890abcdef1234567890abcdef
  # Add as many as you like: PRIVATEKEY_3, PRIVATEKEY_4, etc.
  ```

### 3. ▶️ Run the script
  ```bash
  python tx_V2.py
  ```

### 4. 📊 During execution
- The script will display a banner and prompt for **input of the number of transfers per wallet per cycle**
- **Recommended input:** `10` (safe enough for long runs without being too aggressive)
- **Process performed:**
  - Connect all wallets
  - Login with signature
  - Check balance, status, and leaderboard
  - Perform transfers according to the input number
  - Automatically claim mystery box if eligible
  - Update leaderboard every 5 successful transfers
  - After all wallets are done → sleep 60 seconds → repeat cycle indefinitely

### 5. ⏹️ Stopping the script
Press **Ctrl + C** (will exit cleanly)

---

## ⚠️ If You Still Want to Use tx_V1.py
Replace the fixed address in the following line:
```python
fixed = "0x222306e34a54455aa10c215b26aaad3d6037dbf8"
```
With:
```python
fixed = "0xYourOwnWalletAddressHere"  # Replace with your own web wallet address
```

**⚠️ Warning:** Still not recommended due to high risk of being banned and ineffective multi-wallet handling.

---

## 📝 Important Notes
- This script is created for **educational and testing purposes on testnet networks**
- The author is not responsible for any losses or consequences arising from the use of this script
- **Always comply with the Terms of Service of the platform you are using**

---

**🚀 Happy Farming & Good Luck on the Leaderboard!**
