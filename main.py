import time
import re
import json
from playwright.sync_api import sync_playwright, Page
import neotermcolor
from textwrap import shorten

def login(page, dp_id, username, password):
    page.query_selector("#selectBranch").click()
    time.sleep(1)
    page.query_selector(".select2-search__field").fill(dp_id)
    time.sleep(1)
    page.keyboard.press("Enter")
    page.get_by_label("Username").fill(username)
    time.sleep(1)
    page.get_by_label("Password").fill(password)
    time.sleep(1)
    page.query_selector(".sign-in").click()
    time.sleep(3)

def logout(page):
    try:
        logout_button = page.query_selector("a.header-menu__link[tooltip='Logout']")
        if logout_button:
            logout_button.click()
            time.sleep(3)
            neotermcolor.cprint("🔒 Logged out successfully.", "yellow")
        else:
            raise Exception("Logout button not found.")
    except Exception as e:
        neotermcolor.cprint(f"⚠️ Logout failed: {e}", "red")

def goto_asba(page):
    page.query_selector('xpath=//*[@id="sideBar"]/nav/ul/li[8]/a').click()
    time.sleep(5)
    company_elements = page.query_selector_all(".company-name")
    type_elements = page.query_selector_all(".company-type")
    ipo_list = []
    for i in range(len(company_elements)):
        company = company_elements[i].inner_text().strip()
        ipo_type = type_elements[i].inner_text().strip() if i < len(type_elements) else "N/A"
        ipo_list.append({"Company": company, "Type": ipo_type})
    return ipo_list

def ipo_selector(page, position):
    page.wait_for_load_state("networkidle")
    time.sleep(2)
    apply_buttons = page.query_selector_all("button.btn-issue")
    if not apply_buttons:
        raise Exception("No apply buttons found.")
    if position < 1 or position > len(apply_buttons):
        raise Exception("Invalid IPO position.")

    selected_button = apply_buttons[position - 1]
    button_text = selected_button.inner_text().strip().lower()

    if "edit" in button_text:
        raise Exception("Already applied for this IPO. Edit button is visible.")
    elif "apply" not in button_text:
        raise Exception(f"Unexpected button text: '{button_text}'")

    selected_button.click()
    time.sleep(3)
    neotermcolor.cprint(f"✅ IPO #{position} selected successfully.", "green")

def apply_share(page: Page, preferred_bank: str, kitta: str, crn: str, txn_no: str):
    try:
        bank_options = page.query_selector_all("#selectBank option")
        valid_banks = [opt for opt in bank_options if "Please choose" not in opt.inner_text()]
        if not valid_banks:
            raise Exception("No bank options found.")

        selected_bank = None
        for opt in valid_banks:
            if preferred_bank.strip().upper() in opt.inner_text().strip().upper():
                selected_bank = opt
                print(f"\nAuto-selected preferred bank: {opt.inner_text().strip()}")
                break

        if not selected_bank:
            raise Exception(f"Preferred bank '{preferred_bank}' not found.")

        bank_value = selected_bank.get_attribute("value")
        page.select_option("#selectBank", value=bank_value)
        page.eval_on_selector("#selectBank", "el => el.dispatchEvent(new Event('change', { bubbles: true }))")

        time.sleep(2)
        page.wait_for_selector("#accountNumber", state="visible", timeout=30000)
        time.sleep(1)

        account_options = page.query_selector_all("#accountNumber option")
        valid_accounts = [opt for opt in account_options if "Please choose" not in opt.inner_text()]
        if not valid_accounts:
            raise Exception("No valid account numbers.")

        selected_account = valid_accounts[0]
        page.select_option("#accountNumber", value=selected_account.get_attribute("value"))
        print(f"Auto-selected account number: {selected_account.inner_text().strip()}")

        account_text = selected_account.inner_text().strip()
        match = re.search(r'-\s*(.+)$', account_text)
        branch_name = match.group(1).strip() if match else ""
        print(f"Auto-extracted branch name: {branch_name}")

        page.fill("#appliedKitta", kitta)
        page.fill("#crnNumber", crn)
        page.check("input[type='checkbox']")
        page.click("button:has-text('Proceed')")

        page.wait_for_selector("#transactionPIN")
        page.fill("#transactionPIN", txn_no)
        page.click("button:has-text('Apply')")

        print("✅ IPO application submitted.")
    except Exception as e:
        raise Exception(f"Error while applying: {e}")

def display_ipos(ipo_list):
    neotermcolor.cprint(f"{'Option':<6} {'Company':<45} {'Type':<30}", "cyan")
    neotermcolor.cprint("-" * 85, "cyan")
    for i, ipo in enumerate(ipo_list, 1):
        company = shorten(ipo['Company'], width=45, placeholder="...")
        ipo_type = shorten(ipo['Type'], width=30, placeholder="...")
        print(f"{i:<6} {company:<45} {ipo_type:<30}")
    neotermcolor.cprint("-" * 85, "cyan")

def get_user_choice(max_option):
    while True:
        try:
            choice = int(input(f"Enter IPO option number (1-{max_option}): "))
            if 1 <= choice <= max_option:
                return choice
            print(f"Invalid choice. Try 1-{max_option}.")
        except ValueError:
            print("Invalid input. Enter a number.")

def main():
    success_accounts = []
    failed_accounts = []

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)
        page = browser.new_page(user_agent='Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.116 Safari/537.36')
        page.goto("https://meroshare.cdsc.com.np")
        time.sleep(5)

        with open("demats.json", 'r') as f:
            accounts = json.load(f)

        for account in accounts:
            try:
                name = account["name"]
                print(f"\n🔐 Working for {name}:")
                login(page, account["dp_id"], account["username"], account["password"])
                time.sleep(2)

                ipo_list = goto_asba(page)
                if not ipo_list:
                    raise Exception("No IPOs found.")

                display_ipos(ipo_list)
                position = get_user_choice(len(ipo_list))

                ipo_selector(page, position)
                apply_share(page, account["preferred_bank"], account["kitta"], account["crn"], account["txn_pin"])

                neotermcolor.cprint("✅ IPO Applied Successfully!", "green")
                success_accounts.append(name)
            except Exception as e:
                neotermcolor.cprint(f"❌ Error for {account.get('name', 'Unknown')}: {e}", "red")
                failed_accounts.append(account.get("name", "Unknown"))
            finally:
                logout(page)
                neotermcolor.cprint("-" * 40, "green")
                time.sleep(3)

        browser.close()

        # Final Summary
        print("\n📋 IPO Application Summary")
        neotermcolor.cprint("✅ Successful Applications:", "green")
        for name in success_accounts:
            print(f"  - {name}")

        neotermcolor.cprint("❌ Failed Applications:", "red")
        for name in failed_accounts:
            print(f"  - {name}")

if __name__ == "__main__":
    main()
