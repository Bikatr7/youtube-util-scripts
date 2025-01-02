from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

def check_channel_available(driver):
    try:
        error_messages = [
            "This channel isn't available",
            "This channel does not exist",
            "Channel not found"
        ]
        
        for message in error_messages:
            elements = driver.find_elements(By.XPATH, f"//*[contains(text(), '{message}')]")
            if(elements):
                return False
        return True
    except:
        return True

def try_subscribe(driver, wait):
    try:
        print("Waiting for subscribe button...")
        subscribe_button = wait.until(EC.presence_of_element_located((
            By.CSS_SELECTOR,
            "ytd-subscribe-button-renderer button"
        )))
        
        time.sleep(5)
        button_text = subscribe_button.text
        print(f"Found button with text: '{button_text}'")
        
        if(not button_text):
            time.sleep(2)
            button_text = subscribe_button.text
            print(f"Retried button text: '{button_text}'")
        
        if("Subscribed" == button_text):
            print("Already subscribed")
            return False
            
        if("Subscribe" == button_text):
            subscribe_button.click()
            time.sleep(1)
            print("Subscribed successfully")
            return True
            
        raise Exception(f"Unexpected button text: '{button_text}'")
            
    except Exception as e:
        raise Exception(f"Failed to find or click subscribe button: {str(e)}")

def subscribe_to_channels(links_file):
    driver = webdriver.Chrome()
    wait = WebDriverWait(driver, 10)
    
    driver.get("https://www.youtube.com")
    print("Please login to YouTube manually...")
    print("Type 'start' and press Enter when you're ready to begin:")
    
    while(input().lower().strip() != 'start'):
        print("Please type 'start' to begin:")
    
    with open(links_file, 'r', encoding='utf-8') as f:
        channel_links = [line.strip() for line in f if(line.strip())]
    
    print(f"Found {len(channel_links)} channels to subscribe to")
    
    successful_subs = 0
    failed_subs = 0
    unavailable_channels = 0
    already_subbed = 0
    
    failed_channels = []
    unavailable_channel_links = []
    
    for index, channel_url in enumerate(channel_links, 1):
        print(f"\nProcessing channel {index}/{len(channel_links)}: {channel_url}")
        
        try:
            driver.get(channel_url)
            time.sleep(2)
            
            if(not check_channel_available(driver)):
                print(f"Channel {index} is unavailable")
                unavailable_channels += 1
                unavailable_channel_links.append(channel_url)
                continue
            
            if(try_subscribe(driver, wait)):
                successful_subs += 1
                print(f"Successfully subscribed to channel {index}")
            else:
                already_subbed += 1
                print(f"Already subscribed to channel {index}")
            
            time.sleep(1)
            
        except Exception as e:
            print(f"Failed to subscribe to channel {index}: {str(e)}")
            failed_subs += 1
            failed_channels.append(channel_url)
    
    print(f"\nProcess completed!")
    print(f"Successfully subscribed: {successful_subs} channels")
    print(f"Already subscribed: {already_subbed} channels")
    print(f"Failed to subscribe: {failed_subs} channels")
    print(f"Unavailable channels: {unavailable_channels} channels")
    
    if(failed_channels):
        print("\nFailed channels (need to subscribe manually):")
        for url in failed_channels:
            print(url)
            
    if(unavailable_channel_links):
        print("\nUnavailable channels:")
        for url in unavailable_channel_links:
            print(url)
    
    driver.quit()

if(__name__ == "__main__"):
    input_file = "channels to sub_to.txt"
    subscribe_to_channels(input_file) 