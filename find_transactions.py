from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup
from webdriver_manager.chrome import ChromeDriverManager

chrome_options = Options()
chrome_options.add_argument("--headless")  
chrome_options.add_argument("--disable-gpu")
chrome_options.add_argument("--no-sandbox")


driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)


def get_transaction_div():
    try:
        url = "https://blockstream.info/block/000000000000000000076c036ff5119e5a5a74df77abf64203473364509f7732"
        driver.get(url)
        page_source = driver.page_source
        driver.quit()

        soup = BeautifulSoup(page_source, "html.parser")
        transactions_div = soup.find("div", class_="transactions")

        return transactions_div
    except Exception as e:
        print(f"Error while fetching the URL: {str(e)}")
        driver.quit()
        return None
    finally:
        driver.quit()


HEADING = "25 of 2875 Transactions"

def validate_transaction_heading(transactions_div):
    try:
        if transactions_div:
            header = transactions_div.find("h3", class_="font-h3")

            if header and header.text.strip() == HEADING:
                return True
            
        return False
    except Exception as e:
        print(f"Error while validating header: {str(e)}")

def get_transactions(transactions_div):

    transaction_list = []

    try:
        if transactions_div:
            transaction_boxes = transactions_div.find_all("div", class_="transaction-box")

            for box in transaction_boxes:
                
                txn_div = box.find("div", class_="txn font-p2")
                if txn_div:
                    tx_hash = txn_div.find("a").text.strip()  
                    
                    vin_headers = box.find_all("div", class_="vin-header")
                    vout_headers = box.find_all("div", class_="vout-header")

                    if len(vin_headers) == 1 and len(vout_headers) == 2:
                        transaction_list.append(tx_hash)
                else:
                    print("No transactions found.")
        return transaction_list
    except Exception as e:
        print(f"Error while extracting transactions: {str(e)}")


transactions_div  = get_transaction_div()


# TEST CASE 1
# Visit the page https://blockstream.info/block/000000000000000000076c036ff5119e5a5a74df77abf64203473364509f7732 
# Below the block details div, you will see the transaction list section.
print(validate_transaction_heading(transactions_div=transactions_div))

# TEST CASE 2 
# Parse through the 25 transactions which are visible on the page.
# Print the transaction hash of the transactions which has exactly 1 input and 2 outputs
print(get_transactions(transactions_div=transactions_div))
