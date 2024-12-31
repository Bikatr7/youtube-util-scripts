from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
import time

def get_playlist_links(playlist_url):
    driver = webdriver.Chrome()
    wait = WebDriverWait(driver, 10)
    
    try:
        driver.get(playlist_url)
        print("Loading playlist...")
        time.sleep(3)
        
        print("Loading all videos by scrolling down...")
        last_height = driver.execute_script("return document.documentElement.scrollHeight")
        while True:
            driver.execute_script("window.scrollTo(0, document.documentElement.scrollHeight);")
            time.sleep(2)
            new_height = driver.execute_script("return document.documentElement.scrollHeight")
            if(new_height == last_height):
                break
            last_height = new_height
        
        print("Scrolling back to top...")
        driver.execute_script("window.scrollTo(0, 0);")
        time.sleep(2)

        video_containers = driver.find_elements(By.CSS_SELECTOR, "ytd-playlist-video-renderer")
        print(f"Found {len(video_containers)} videos in playlist")
        
        video_urls = []
        for index, container in enumerate(video_containers, 1):
            try:
                print(f"\nProcessing video {index}/{len(video_containers)}")
                
                title = container.find_element(By.CSS_SELECTOR, "a#video-title").text
                print(f"Video title: {title}")
                
                video_link = container.find_element(By.CSS_SELECTOR, "a#video-title").get_attribute('href')
                if(video_link and 'watch?v=' in video_link):
                    video_id = video_link.split('watch?v=')[1].split('&')[0]
                    share_url = f"https://youtu.be/{video_id}"
                    print(f"Got share URL: {share_url}")
                    video_urls.append(share_url)
                
                if(index % 5 == 0):
                    driver.execute_script("window.scrollBy(0, 500);")
                    time.sleep(1)
                
            except Exception as e:
                print(f"Error processing video {index}: {str(e)}")
                with open('youtube_links_partial.txt', 'w', encoding='utf-8') as f:
                    for url in video_urls:
                        f.write(url + '\n')
                continue

        with open('youtube_links.txt', 'w', encoding='utf-8') as f:
            for url in video_urls:
                f.write(url + '\n')
        
        print(f"\nSuccessfully saved {len(video_urls)} video links to youtube_links.txt")
        
    except Exception as e:
        print(f"An error occurred: {str(e)}")
        import traceback
        print(traceback.format_exc())
    
    finally:
        driver.quit()

if(__name__ == "__main__"):
    playlist_url = "YOUR_PLAYLIST_URL"
    get_playlist_links(playlist_url)
