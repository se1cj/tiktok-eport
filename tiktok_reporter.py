import requests
import json
import time
import random

# -----------------------------------------
# TikTok Reporting Tool
# Developed by secj
# -----------------------------------------

# Define session
session = requests.Session()

def login_to_tiktok(username, password):
    login_url = 'https://api.tiktok.com/login'  # Verify the correct URL
    credentials = {'username': username, 'password': password}

    try:
        response = session.post(login_url, data=credentials)
        response.raise_for_status()  # Check HTTP status
        return response.json()  # Return account data if login successful
    except requests.exceptions.HTTPError as http_err:
        print(f"\033[1;31mHTTP Error: {http_err}\033[0m")
        print(f"Details: {response.text}")  # Print response content for diagnostics
    except Exception as e:
        print(f"\033[1;31mAn error occurred during login: {e}\033[0m")
    return None

def report_account(auth_token, target_username, reason):
    report_url = f'https://api.tiktok.com/report/{target_username}'  # Verify the correct URL
    headers = {
        'Authorization': f'Bearer {auth_token}',
        'Content-Type': 'application/json'
    }
    report_data = {'reason': reason}

    try:
        response = session.post(report_url, headers=headers, data=json.dumps(report_data))
        response.raise_for_status()  # Check request status
        print(f"\033[1;32mReport successfully sent for account: {target_username}\033[0m")
    except requests.exceptions.HTTPError as http_err:
        print(f"\033[1;31mHTTP Error: {http_err}\033[0m")
        print(f"Details: {response.text}")
    except Exception as e:
        print(f"\033[1;31mAn error occurred while sending the report: {e}\033[0m")

def automated_reporting(auth_token, accounts, reasons):
    for account in accounts:
        reason = reasons.get(account, "General Report")
        for _ in range(random.randint(3, 5)):  # Random number of reports to simulate repeated reporting
            report_account(auth_token, account, reason)
            time.sleep(random.uniform(1, 3))  # Random delay to avoid detection
        print(f"\033[1;33mWaiting before moving to next account...\033[0m")
        time.sleep(random.uniform(5, 10))  # Wait time between accounts

def analyze_account(username):
    # Placeholder for content analysis or pattern detection
    return "Spam"  # Example reason, could be replaced with actual analysis

# Main program
if __name__ == '__main__':
    print("\033[1;34mTikTok Reporting Tool (Developed by secj)\033[0m")
    username = input("Enter your username: ")
    password = input("Enter your password: ")

    account_data = login_to_tiktok(username, password)
    if account_data and 'auth_token' in account_data:
        auth_token = account_data.get('auth_token')
        
        # Define accounts and reasons for automated reporting
        accounts_to_report = [
            'account1', 'account2', 'account3'  # Add target usernames here
        ]
        
        reasons_for_reporting = {
            account: analyze_account(account) for account in accounts_to_report
        }

        automated_reporting(auth_token, accounts_to_report, reasons_for_reporting)
    else:
        print("\033[1;31mLogin failed.\033[0m")
