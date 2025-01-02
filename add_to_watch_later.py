from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

def check_video_available(driver):
    try:
        error_messages = [
            "Video unavailable",
            "This video isn't available anymore",
            "This video has been removed",
            "This video is private"
        ]
        
        for message in error_messages:
            elements = driver.find_elements(By.XPATH, f"//*[contains(text(), '{message}')]")
            if(elements):
                return False
        return True
    except:
        return True

def try_three_dots_method(driver, wait):
    menu_button = wait.until(EC.element_to_be_clickable((
        By.CSS_SELECTOR, 
        "button.yt-spec-button-shape-next[aria-label='More actions']"
    )))
    menu_button.click()
    time.sleep(1)
    
    save_option = wait.until(EC.element_to_be_clickable((
        By.XPATH, 
        "//tp-yt-paper-item//yt-formatted-string[text()='Save']"
    )))
    save_option.click()

def try_direct_save(driver, wait):
    save_button = wait.until(EC.element_to_be_clickable((
        By.CSS_SELECTOR,
        "button.yt-spec-button-shape-next[aria-label='Save to playlist']"
    )))
    save_button.click()

def try_add_to_watch_later(driver, wait, url):
    try:
        try_three_dots_method(driver, wait)
        print("Used three dots method")
    except Exception as e:
        print("Three dots method failed, reloading and trying direct save...")
        driver.get(url)
        time.sleep(2)
        try:
            try_direct_save(driver, wait)
            print("Used direct save method")
        except:
            raise Exception("Both save methods failed")
    
    time.sleep(1)
    
    watch_later = wait.until(EC.element_to_be_clickable((
        By.XPATH, 
        "//yt-formatted-string[@id='label' and contains(@title, 'Watch later')]"
    )))
    
    checkbox = driver.find_element(By.CSS_SELECTOR, "tp-yt-paper-checkbox#checkbox")
    if(not checkbox.get_attribute("checked")):
        watch_later.click()
        time.sleep(1)
        print("Added to Watch Later")
        return True
    else:
        print("Already in Watch Later, skipping...")
        try:
            close_button = driver.find_element(By.CSS_SELECTOR, "ytd-button-renderer[dialog-dismiss] button")
            close_button.click()
        except:
            pass
        return False

def add_videos_to_watch_later(links_file):
    driver = webdriver.Chrome()
    wait = WebDriverWait(driver, 10)
    
    driver.get("https://www.youtube.com")
    print("Please login to YouTube manually...")
    print("Type 'start' and press Enter when you're ready to begin:")
    
    while(input().lower().strip() != 'start'):
        print("Please type 'start' to begin:")
    
    with open(links_file, 'r', encoding='utf-8') as f:
        video_links = [line.strip() for line in f if(line.strip())]
    
    print(f"Found {len(video_links)} videos to add")
    
    successful_adds = 0
    failed_adds = 0
    unavailable_videos = 0
    already_added = 0
    
    failed_videos = []
    unavailable_video_links = []
    
    for index, video_url in enumerate(video_links, 1):
        print(f"\nProcessing video {index}/{len(video_links)}: {video_url}")
        
        try:
            driver.get(video_url)
            time.sleep(2)
            
            if(not check_video_available(driver)):
                print(f"Video {index} is unavailable")
                unavailable_videos += 1
                unavailable_video_links.append(video_url)
                continue
            
            if(try_add_to_watch_later(driver, wait, video_url)):
                successful_adds += 1
                print(f"Successfully added video {index}")
            else:
                already_added += 1
                print(f"Video {index} was already in Watch Later")
            
            time.sleep(1)
            
        except Exception as e:
            print(f"Failed to add video {index}: {str(e)}")
            failed_adds += 1
            failed_videos.append(video_url)
    
    print(f"\nProcess completed!")
    print(f"Successfully added: {successful_adds} videos")
    print(f"Already in Watch Later: {already_added} videos")
    print(f"Failed to add: {failed_adds} videos")
    print(f"Unavailable videos: {unavailable_videos} videos")
    
    if(failed_videos):
        print("\nFailed videos (need to add manually):")
        for url in failed_videos:
            print(url)
            
    if(unavailable_video_links):
        print("\nUnavailable videos:")
        for url in unavailable_video_links:
            print(url)
    
    driver.quit()

if(__name__ == "__main__"):
    input_file = "VIDOES TO ADD TO WATCH LATER.txt"
    add_videos_to_watch_later(input_file) 