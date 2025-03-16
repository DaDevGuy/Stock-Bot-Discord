# Stock-Bot-Discord

Stock-Bot-Discord is a versatile Discord bot designed to provide stock-related information and user verification features. Built using `discord.py`, it includes functionality for fetching data and verifying users with Google Sheets integration.

---

## **Features**

- **Stock Commands**: Retrieve stock-related information (future updates planned).
- **User Verification**: Verifies Discord users against a list stored in a Google Sheet.

---

## **Setup**

### **Prerequisites**

1. **Python**: Ensure Python 3.8 or later is installed.
2. **Discord Bot Token**: Obtain a bot token from the [Discord Developer Portal](https://discord.com/developers/applications).
3. **Google Service Account**:
   - Create a service account in the [Google Cloud Console](https://console.cloud.google.com/).
   - Download the JSON key file.
   - Share the target Google Sheet with the service account email.

---

# **VerificationCog Documentation**

The `VerificationCog` is a Discord bot module that enables user verification using data from a Google Sheet. It checks whether a user's name exists in a specific column of the sheet and provides a command to verify users directly in Discord.

---

## **Features**

- Verifies Discord members against a Google Sheet.
- Sends feedback to Discord channels using rich embeds.
- Handles authentication with Google Sheets using a service account.

---



### **Prerequisites**

1. **Google Service Account**:
   - Create a service account in the Google Cloud Console.
   - Download the JSON key file for the service account.
   - Share the target Google Sheet with the service account email.

2. **Google Sheet**:
   - Ensure your Google Sheet contains a column with usernames that need verification.
   - Replace `'REPLACE_WITH_DOCS_LINK_THINGY'` in the code with the URL of your Google Sheet.

3. **Environment**:
   - Install the required Python libraries (see [Dependencies](#dependencies)).
   - Set up your Discord bot token and environment as per the `discord.py` library documentation.

---

## **Commands**

### **1. Check Verification**
```plaintext
Command: !check @member


### **Installation**

1. Clone the repository:
   ```bash
   git clone https://github.com/DaDevGuy/Stock-Bot-Discord.git
   cd Stock-Bot-Discord
