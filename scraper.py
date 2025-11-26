# import undetected_chromedriver as uc
# from selenium.webdriver.common.by import By
# from selenium.webdriver.support.ui import WebDriverWait
# from selenium.webdriver.support import expected_conditions as EC
# from selenium.common.exceptions import (
#     TimeoutException, 
#     NoSuchElementException,
#     WebDriverException,
#     NoSuchWindowException
# )
# import time
# import random
# import os
# import requests
# import json
# import re
# from datetime import datetime
# from config import Config


# class InstagramScraper:
#     def __init__(self):
#         self.driver = None
#         self.is_logged_in = False
#         self.current_account = None
#         self.instagram_app_id = "936619743392459"

#     def init_driver(self):
#         """Initialize undetected Chrome driver with robust error handling"""
#         try:
#             options = uc.ChromeOptions()
#             options.add_argument('--disable-blink-features=AutomationControlled')
#             options.add_argument('--disable-dev-shm-usage')
#             options.add_argument('--no-sandbox')
#             options.add_argument('--disable-gpu')
#             options.add_argument('--window-size=1920,1080')
            
#             # Stability improvements
#             options.add_argument('--disable-extensions')
#             options.add_argument('--disable-popup-blocking')
#             options.add_argument('--disable-notifications')
#             options.add_argument('--disable-infobars')
#             options.add_argument('--ignore-certificate-errors')
#             options.add_argument('--ignore-ssl-errors')
            
#             # MacOS specific fixes
#             options.add_argument('--disable-dev-tools')
#             options.add_argument('--remote-debugging-port=9222')
            
#             # Headless mode - can be controlled via environment variable
#             if os.getenv('HEADLESS', 'true').lower() == 'true':
#                 options.add_argument('--headless=new')
            
#             # Random user agent rotation
#             user_agents = [
#                 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36',
#                 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36',
#                 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36'
#             ]
#             options.add_argument(f'user-agent={random.choice(user_agents)}')
            
#             # Initialize driver with version management
#             self.driver = uc.Chrome(
#                 options=options,
#                 version_main=None,  # Auto-detect Chrome version
#                 driver_executable_path=None
#             )
            
#             self.driver.implicitly_wait(Config.IMPLICIT_WAIT)
#             self.driver.set_page_load_timeout(Config.PAGE_LOAD_TIMEOUT)
            
#             # Verify window is accessible
#             self.driver.current_url
            
#             print('✅ Chrome driver initialized successfully')
#             return self.driver
            
#         except Exception as e:
#             print(f"❌ Failed to initialize driver: {str(e)}")
#             if self.driver:
#                 try:
#                     self.driver.quit()
#                 except:
#                     pass
#             self.driver = None
#             raise

#     def is_driver_alive(self):
#         """Check if the driver is still alive and responsive"""
#         try:
#             if not self.driver:
#                 return False
#             # Try to access current_url to verify window is alive
#             _ = self.driver.current_url
#             return True
#         except (WebDriverException, NoSuchWindowException):
#             return False

#     def human_delay(self, min_delay=None, max_delay=None):
#         """Add random delay to mimic human behavior"""
#         min_d = min_delay or Config.REQUEST_DELAY_MIN
#         max_d = max_delay or Config.REQUEST_DELAY_MAX
#         time.sleep(random.uniform(min_d, max_d))

#     def scrape_profile_api(self, username):
#         """
#         Scrape comprehensive Instagram profile data using Instagram's API
#         This method doesn't require authentication and is much faster
#         """
#         url = f"https://i.instagram.com/api/v1/users/web_profile_info/?username={username}"
        
#         headers = {
#             "x-ig-app-id": self.instagram_app_id,
#             "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
#             "Accept": "*/*",
#             "Accept-Language": "en-US,en;q=0.9",
#         }
        
#         try:
#             print(f"📊 Scraping profile via API: {username}")
#             response = requests.get(url, headers=headers, timeout=10)
            
#             if response.status_code != 200:
#                 print(f"❌ API request failed with status {response.status_code}")
#                 return None
            
#             data = response.json()
#             user = data.get('data', {}).get('user', {})
            
#             if not user:
#                 print("❌ No user data found in API response")
#                 return None
            
#             profile = {
#                 "inputUrl": f"https://www.instagram.com/{username}",
#                 "id": user.get("id"),
#                 "username": user.get("username"),
#                 "url": f"https://www.instagram.com/{username}",
#                 "fullName": user.get("full_name"),
#                 "biography": user.get("biography"),
#                 "externalUrls": user.get("bio_links", []),
#                 "followersCount": user.get("edge_followed_by", {}).get("count", 0),
#                 "followsCount": user.get("edge_follow", {}).get("count", 0),
#                 "hasChannel": user.get("has_channel", False),
#                 "highlightReelCount": user.get("highlight_reel_count", 0),
#                 "isBusinessAccount": user.get("is_business_account", False),
#                 "joinedRecently": user.get("is_joined_recently", False),
#                 "businessCategoryName": user.get("business_category_name"),
#                 "private": user.get("is_private", False),
#                 "verified": user.get("is_verified", False),
#                 "profilePicUrl": user.get("profile_pic_url"),
#                 "profilePicUrlHD": user.get("profile_pic_url_hd"),
#                 "igtvVideoCount": user.get("edge_felix_video_timeline", {}).get("count", 0),
#                 "relatedProfiles": [],
#                 "latestIgtvVideos": [],
#                 "postsCount": user.get("edge_owner_to_timeline_media", {}).get("count", 0),
#                 "latestPosts": [],

#                 "businessEmail": user.get("business_email"),
#                 "businessPhoneNumber": user.get("business_phone_number"),
#                 "publicEmail": user.get("public_email"),
#                 "publicPhoneNumber": user.get("public_phone_number"),
#                 "contactPhoneNumber": user.get("contact_phone_number"),
                
#                 "fbid": user.get("fbid"),
#                 "scraped_at": time.strftime("%Y-%m-%d %H:%M:%S")
#             }


            
            
#             # Extract latest posts with comprehensive details
#             posts_data = user.get("edge_owner_to_timeline_media", {}).get("edges", [])
            
#             for edge in posts_data:
#                 node = edge.get("node", {})
                
#                 # Determine post type
#                 post_type = "Image"
#                 if node.get("is_video"):
#                     post_type = "Video"
#                 elif node.get("edge_sidecar_to_children"):
#                     post_type = "Sidecar"
                
#                 # Extract caption
#                 caption_edges = node.get("edge_media_to_caption", {}).get("edges", [])
#                 caption = caption_edges[0].get("node", {}).get("text", "") if caption_edges else ""
                
#                 # Extract hashtags and mentions from caption
#                 hashtags = re.findall(r'#(\w+)', caption) if caption else []
#                 mentions = re.findall(r'@(\w+)', caption) if caption else []
                
#                 # Extract tagged users
#                 tagged_users = []
#                 tagged_edges = node.get("edge_media_to_tagged_user", {}).get("edges", [])
#                 for tagged_edge in tagged_edges:
#                     tagged_node = tagged_edge.get("node", {}).get("user", {})
#                     if tagged_node:
#                         tagged_users.append({
#                             "full_name": tagged_node.get("full_name"),
#                             "id": tagged_node.get("id"),
#                             "is_verified": tagged_node.get("is_verified", False),
#                             "profile_pic_url": tagged_node.get("profile_pic_url"),
#                             "username": tagged_node.get("username")
#                         })
                
                
#                 # Extract video URL if it's a video
#                 video_url = node.get("video_url") if node.get("is_video") else None
                
#                 # Build post object
#                 post = {
#                     "id": node.get("id"),
#                     "type": post_type,
#                     "shortCode": node.get("shortcode"),
#                     "caption": caption,
#                     "hashtags": hashtags,
#                     "mentions": mentions,
#                     "url": f"https://www.instagram.com/p/{node.get('shortcode')}/",
#                     "commentsCount": node.get("edge_media_to_comment", {}).get("count", 0),
#                     "dimensionsHeight": node.get("dimensions", {}).get("height"),
#                     "dimensionsWidth": node.get("dimensions", {}).get("width"),
#                     "displayUrl": node.get("display_url"),
#                     "videoUrl": video_url,
#                     "alt": node.get("accessibility_caption"),
#                     "likesCount": node.get("edge_liked_by", {}).get("count", 0) or node.get("edge_media_preview_like", {}).get("count", 0),
#                     "videoViewCount": node.get("video_view_count"),
#                     "timestamp": datetime.fromtimestamp(node.get("taken_at_timestamp", 0)).strftime("%Y-%m-%dT%H:%M:%S.000Z") if node.get("taken_at_timestamp") else None,
#                     "childPosts": [],
#                     "ownerUsername": user.get("username"),
#                     "ownerId": user.get("id"),
#                     "productType": node.get("product_type"),
#                     "taggedUsers": tagged_users,
#                     "isCommentsDisabled": node.get("comments_disabled", False)
#                 }
                
#                 # Handle carousel/sidecar posts
#                 if node.get("edge_sidecar_to_children"):
#                     sidecar_edges = node.get("edge_sidecar_to_children", {}).get("edges", [])
#                     for sidecar_edge in sidecar_edges:
#                         sidecar_node = sidecar_edge.get("node", {})
#                         child_post = {
#                             "id": sidecar_node.get("id"),
#                             "shortCode": sidecar_node.get("shortcode"),
#                             "displayUrl": sidecar_node.get("display_url"),
#                             "videoUrl": sidecar_node.get("video_url") if sidecar_node.get("is_video") else None,
#                             "isVideo": sidecar_node.get("is_video", False)
#                         }
#                         post["childPosts"].append(child_post)
                
#                 profile["latestPosts"].append(post)
            
#             print(f"✅ Successfully scraped profile via API: {username} ({len(profile['latestPosts'])} posts)")
#             return profile
            
#         except requests.exceptions.RequestException as e:
#             print(f"❌ Request error: {e}")
#             return None
#         except json.JSONDecodeError as e:
#             print(f"❌ JSON decode error: {e}")
#             return None
#         except Exception as e:
#             print(f"❌ Unexpected error scraping profile via API: {e}")
#             return None

#     def login(self, username, password):
#         """Login to Instagram with given credentials and robust error handling"""
#         try:
#             # Initialize driver if not exists or not alive
#             if not self.is_driver_alive():
#                 print("🔄 Driver not alive, reinitializing...")
#                 self.close()
#                 self.init_driver()
            
#             print(f"🔐 Logging in as {username}...")
            
#             # Navigate to login page with error handling
#             try:
#                 self.driver.get(Config.INSTAGRAM_LOGIN_URL)
#             except WebDriverException as e:
#                 print(f"❌ Failed to navigate to login page: {str(e)}")
#                 return False
            
#             self.human_delay(3, 5)
            
#             # Verify window is still alive
#             if not self.is_driver_alive():
#                 raise Exception("Browser window closed unexpectedly before login")
            
#             # Wait for and fill username
#             username_input = WebDriverWait(self.driver, 15).until(
#                 EC.presence_of_element_located((By.NAME, "username"))
#             )
#             username_input.clear()
#             username_input.send_keys(username)
#             self.human_delay(1, 2)
            
#             # Verify window is still alive
#             if not self.is_driver_alive():
#                 raise Exception("Browser window closed unexpectedly during username input")
            
#             # Fill password
#             password_input = self.driver.find_element(By.NAME, "password")
#             password_input.clear()
#             password_input.send_keys(password)
#             self.human_delay(1, 2)
            
#             # Click login button
#             login_button = self.driver.find_element(By.XPATH, "//button[@type='submit']")
#             login_button.click()
            
#             # Wait for login to complete
#             self.human_delay(5, 7)
            
#             # Verify window is still alive after login
#             if not self.is_driver_alive():
#                 raise Exception("Browser window closed unexpectedly after login attempt")
            
#             # Handle "Save Your Login Info" popup
#             try:
#                 not_now_button = WebDriverWait(self.driver, 5).until(
#                     EC.element_to_be_clickable((By.XPATH, "//button[contains(text(), 'Not now') or contains(text(), 'Not Now')]"))
#                 )
#                 not_now_button.click()
#                 self.human_delay(2, 3)
#             except TimeoutException:
#                 pass
            
#             # Handle "Turn on Notifications" popup
#             try:
#                 not_now_button = WebDriverWait(self.driver, 5).until(
#                     EC.element_to_be_clickable((By.XPATH, "//button[contains(text(), 'Not Now')]"))
#                 )
#                 not_now_button.click()
#                 self.human_delay(2, 3)
#             except TimeoutException:
#                 pass
            
#             # Verify successful login by checking URL or elements
#             current_url = self.driver.current_url
#             if "login" in current_url.lower():
#                 # Check for error messages
#                 try:
#                     error_elem = self.driver.find_element(By.XPATH, "//*[contains(text(), 'incorrect') or contains(text(), 'Sorry')]")
#                     raise Exception(f"Login failed: {error_elem.text}")
#                 except NoSuchElementException:
#                     raise Exception("Login failed: Still on login page")
            
#             self.is_logged_in = True
#             self.current_account = username
#             print(f"✅ Successfully logged in as {username}")
#             return True
            
#         except NoSuchWindowException as e:
#             print(f"❌ Login failed: Browser window was closed - {str(e)}")
#             self.close()
#             return False
#         except WebDriverException as e:
#             print(f"❌ Login failed: WebDriver error - {str(e)}")
#             self.close()
#             return False
#         except Exception as e:
#             print(f"❌ Login failed: {str(e)}")
#             return False

#     def scrape_profile(self, username):
#         """
#         Scrape profile information - tries API first, falls back to Selenium
#         """
#         # Try API method first (faster and doesn't require login)
#         profile = self.scrape_profile_api(username)
#         if profile:
#             return profile
        
#         # Fallback to Selenium method if API fails
#         print(f"⚠️ API method failed, falling back to Selenium for {username}")
#         return self.scrape_profile_selenium(username)

#     def scrape_profile_selenium(self, username):
#         """Scrape profile information using Selenium (fallback method)"""
#         try:
#             profile_url = f"{Config.INSTAGRAM_URL}/{username}/"
#             print(f"📊 Scraping profile via Selenium: {username}")
#             self.driver.get(profile_url)
#             self.human_delay(3, 5)
            
#             # Extract profile data
#             profile_data = {
#                 'username': username,
#                 'url': profile_url,
#                 'scraped_at': time.strftime('%Y-%m-%d %H:%M:%S')
#             }
            
#             try:
#                 followers_elem = self.driver.find_element(By.XPATH, "//a[contains(@href, '/followers/')]/span")
#                 profile_data['followers'] = followers_elem.get_attribute('title') or followers_elem.text
#             except NoSuchElementException:
#                 profile_data['followers'] = 'N/A'
                
#             try:
#                 following_elem = self.driver.find_element(By.XPATH, "//a[contains(@href, '/following/')]/span")
#                 profile_data['following'] = following_elem.text
#             except NoSuchElementException:
#                 profile_data['following'] = 'N/A'
                
#             try:
#                 posts_elem = self.driver.find_element(By.XPATH, "//span[contains(text(), 'posts')]/span")
#                 profile_data['posts_count'] = posts_elem.text
#             except NoSuchElementException:
#                 profile_data['posts_count'] = 'N/A'
                
#             try:
#                 bio_elem = self.driver.find_element(By.XPATH, "//div[@class='_aa_c']/span")
#                 profile_data['bio'] = bio_elem.text
#             except NoSuchElementException:
#                 profile_data['bio'] = 'N/A'
                
#             try:
#                 name_elem = self.driver.find_element(By.XPATH, "//span[@class='_aacl _aaco _aacw _aacx _aad7 _aade']")
#                 profile_data['full_name'] = name_elem.text
#             except NoSuchElementException:
#                 profile_data['full_name'] = 'N/A'
                
#             print(f"✅ Scraped profile via Selenium: {username}")
#             return profile_data
            
#         except Exception as e:
#             print(f"❌ Error scraping profile {username}: {str(e)}")
#             raise e

#     def scrape_posts(self, username, max_posts=12):
#         """Scrape posts from a profile"""
#         try:
#             profile_url = f"{Config.INSTAGRAM_URL}/{username}/"
#             print(f"📸 Scraping posts from {username}")
#             self.driver.get(profile_url)
#             self.human_delay(3, 5)
            
#             posts_data = []
#             last_height = self.driver.execute_script("return document.body.scrollHeight")
#             posts_loaded = 0
            
#             while posts_loaded < max_posts:
#                 post_links = self.driver.find_elements(By.XPATH, "//a[contains(@href, '/p/')]")
                
#                 for link in post_links[:max_posts]:
#                     if posts_loaded >= max_posts:
#                         break
                        
#                     try:
#                         post_url = link.get_attribute('href')
#                         img = link.find_element(By.TAG_NAME, 'img')
#                         img_src = img.get_attribute('src')
#                         alt_text = img.get_attribute('alt')
                        
#                         posts_data.append({
#                             'post_url': post_url,
#                             'image_url': img_src,
#                             'caption_preview': alt_text[:100] if alt_text else 'N/A',
#                             'scraped_at': time.strftime('%Y-%m-%d %H:%M:%S')
#                         })
#                         posts_loaded += 1
                        
#                     except Exception as e:
#                         continue
                
#                 self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
#                 self.human_delay(2, 4)
                
#                 new_height = self.driver.execute_script("return document.body.scrollHeight")
#                 if new_height == last_height:
#                     break
#                 last_height = new_height
            
#             print(f"✅ Scraped {len(posts_data)} posts from {username}")
#             return posts_data
            
#         except Exception as e:
#             print(f"❌ Error scraping posts from {username}: {str(e)}")
#             raise e

#     def scrape_hashtag(self, hashtag, max_posts=20):
#         """Scrape posts from a hashtag"""
#         try:
#             hashtag_url = f"{Config.INSTAGRAM_URL}/explore/tags/{hashtag.replace('#', '')}/"
#             print(f"#️⃣ Scraping hashtag: #{hashtag}")
#             self.driver.get(hashtag_url)
#             self.human_delay(3, 5)
            
#             posts_data = []
#             posts_loaded = 0
#             last_height = self.driver.execute_script("return document.body.scrollHeight")
            
#             while posts_loaded < max_posts:
#                 post_links = self.driver.find_elements(By.XPATH, "//a[contains(@href, '/p/')]")
                
#                 for link in post_links[:max_posts]:
#                     if posts_loaded >= max_posts:
#                         break
                        
#                     try:
#                         post_url = link.get_attribute('href')
#                         img = link.find_element(By.TAG_NAME, 'img')
#                         img_src = img.get_attribute('src')
                        
#                         posts_data.append({
#                             'post_url': post_url,
#                             'image_url': img_src,
#                             'hashtag': hashtag,
#                             'scraped_at': time.strftime('%Y-%m-%d %H:%M:%S')
#                         })
#                         posts_loaded += 1
                        
#                     except Exception as e:
#                         continue
                
#                 self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
#                 self.human_delay(2, 4)
                
#                 new_height = self.driver.execute_script("return document.body.scrollHeight")
#                 if new_height == last_height:
#                     break
#                 last_height = new_height
            
#             print(f"✅ Scraped {len(posts_data)} posts from #{hashtag}")
#             return posts_data
            
#         except Exception as e:
#             print(f"❌ Error scraping hashtag #{hashtag}: {str(e)}")
#             raise e

#     def scrape_followers(self, username, max_followers=100):
#         """Scrape followers list"""
#         try:
#             profile_url = f"{Config.INSTAGRAM_URL}/{username}/"
#             print(f"👥 Scraping followers from: {username}")
#             self.driver.get(profile_url)
#             self.human_delay(3, 5)
            
#             try:
#                 followers_link = WebDriverWait(self.driver, 10).until(
#                     EC.element_to_be_clickable((By.XPATH, "//a[contains(@href, '/followers/')]"))
#                 )
#                 followers_link.click()
#                 print("🔄 Opened followers modal")
#                 self.human_delay(3, 4)
#             except Exception as e:
#                 print(f"❌ Could not open followers modal: {str(e)}")
#                 return []
            
#             try:
#                 modal = WebDriverWait(self.driver, 10).until(
#                     EC.presence_of_element_located((By.XPATH, "//div[@role='dialog']"))
#                 )
#                 print("✅ Followers modal loaded")
#             except:
#                 print("❌ Followers modal did not load")
#                 return []
            
#             followers = []
#             seen_usernames = set()
#             scroll_attempts = 0
#             max_scroll_attempts = 200
#             no_change_count = 0
            
#             scrollable_element = None
#             scroll_selectors = [
#                 "//div[@role='dialog']//div[contains(@style, 'overflow')]",
#                 "//div[@role='dialog']//div[contains(@class, 'x')]//div[contains(@style, 'height')]",
#                 "//div[@role='dialog']//ul/parent::div",
#             ]
            
#             for selector in scroll_selectors:
#                 try:
#                     scrollable_element = self.driver.find_element(By.XPATH, selector)
#                     if scrollable_element:
#                         print(f"✅ Found scrollable element")
#                         break
#                 except:
#                     continue
            
#             if not scrollable_element:
#                 scrollable_element = modal
            
#             while len(followers) < max_followers and scroll_attempts < max_scroll_attempts:
#                 try:
#                     follower_elements = []
#                     username_selectors = [
#                         "//div[@role='dialog']//a[contains(@href, '/')]/span",
#                         "//div[@role='dialog']//span[contains(@class, 'x')]//span",
#                     ]
                    
#                     for selector in username_selectors:
#                         try:
#                             elements = self.driver.find_elements(By.XPATH, selector)
#                             if elements:
#                                 follower_elements = elements
#                                 break
#                         except:
#                             continue
                    
#                     previous_count = len(followers)
                    
#                     for element in follower_elements:
#                         try:
#                             username_text = element.text.strip()
#                             if username_text and username_text not in seen_usernames:
#                                 if ' ' not in username_text and len(username_text) <= 30:
#                                     seen_usernames.add(username_text)
                                    
#                                     try:
#                                         parent_link = element.find_element(By.XPATH, "./ancestor::a")
#                                         profile_link = parent_link.get_attribute('href')
#                                     except:
#                                         profile_link = f"{Config.INSTAGRAM_URL}/{username_text}/"
                                    
#                                     follower_data = {
#                                         'username': username_text,
#                                         'profile_url': profile_link,
#                                         'scraped_at': time.strftime('%Y-%m-%d %H:%M:%S')
#                                     }
#                                     followers.append(follower_data)
                                    
#                                     if len(followers) >= max_followers:
#                                         break
#                         except Exception as e:
#                             continue
                    
#                     if len(followers) == previous_count:
#                         no_change_count += 1
#                         if no_change_count >= 10:
#                             break
#                     else:
#                         no_change_count = 0
                        
#                 except Exception as e:
#                     print(f"⚠️ Error finding followers: {str(e)}")
                
#                 try:
#                     self.driver.execute_script(
#                         "arguments[0].scrollTop = arguments[0].scrollHeight",
#                         scrollable_element
#                     )
#                     self.human_delay(2, 3)
#                     print(f"📜 Scrolling... Found {len(followers)} followers so far")
#                 except Exception as e:
#                     print(f"⚠️ Scroll error: {str(e)}")
                
#                 scroll_attempts += 1
            
#             print(f"✅ Successfully scraped {len(followers)} followers from {username}")
#             return followers
            
#         except Exception as e:
#             print(f"❌ Error scraping followers from {username}: {str(e)}")
#             return []

#     def scrape_following(self, username, max_following=100):
#         """Scrape following list"""
#         try:
#             profile_url = f"{Config.INSTAGRAM_URL}/{username}/"
#             print(f"👤 Scraping following from: {username}")
#             self.driver.get(profile_url)
#             self.human_delay(3, 5)
            
#             try:
#                 following_link = WebDriverWait(self.driver, 10).until(
#                     EC.element_to_be_clickable((By.XPATH, "//a[contains(@href, '/following/')]"))
#                 )
#                 following_link.click()
#                 print("🔄 Opened following modal")
#                 self.human_delay(3, 4)
#             except Exception as e:
#                 print(f"❌ Could not open following modal: {str(e)}")
#                 return []
            
#             try:
#                 modal = WebDriverWait(self.driver, 10).until(
#                     EC.presence_of_element_located((By.XPATH, "//div[@role='dialog']"))
#                 )
#                 print("✅ Following modal loaded")
#             except:
#                 print("❌ Following modal did not load")
#                 return []
            
#             following = []
#             seen_usernames = set()
#             scroll_attempts = 0
#             max_scroll_attempts = 200
#             no_change_count = 0
            
#             scrollable_element = None
#             scroll_selectors = [
#                 "//div[@role='dialog']//div[contains(@style, 'overflow')]",
#                 "//div[@role='dialog']//div[contains(@class, 'x')]//div[contains(@style, 'height')]",
#                 "//div[@role='dialog']//ul/parent::div",
#             ]
            
#             for selector in scroll_selectors:
#                 try:
#                     scrollable_element = self.driver.find_element(By.XPATH, selector)
#                     if scrollable_element:
#                         break
#                 except:
#                     continue
            
#             if not scrollable_element:
#                 scrollable_element = modal
            
#             while len(following) < max_following and scroll_attempts < max_scroll_attempts:
#                 try:
#                     following_elements = []
#                     username_selectors = [
#                         "//div[@role='dialog']//a[contains(@href, '/')]/span",
#                         "//div[@role='dialog']//span[contains(@class, 'x')]//span",
#                     ]
                    
#                     for selector in username_selectors:
#                         try:
#                             elements = self.driver.find_elements(By.XPATH, selector)
#                             if elements:
#                                 following_elements = elements
#                                 break
#                         except:
#                             continue
                    
#                     previous_count = len(following)
                    
#                     for element in following_elements:
#                         try:
#                             username_text = element.text.strip()
#                             if username_text and username_text not in seen_usernames:
#                                 if ' ' not in username_text and len(username_text) <= 30:
#                                     seen_usernames.add(username_text)
                                    
#                                     try:
#                                         parent_link = element.find_element(By.XPATH, "./ancestor::a")
#                                         profile_link = parent_link.get_attribute('href')
#                                     except:
#                                         profile_link = f"{Config.INSTAGRAM_URL}/{username_text}/"
                                    
#                                     following_data = {
#                                         'username': username_text,
#                                         'profile_url': profile_link,
#                                         'scraped_at': time.strftime('%Y-%m-%d %H:%M:%S')
#                                     }
#                                     following.append(following_data)
                                    
#                                     if len(following) >= max_following:
#                                         break
#                         except Exception as e:
#                             continue
                    
#                     if len(following) == previous_count:
#                         no_change_count += 1
#                         if no_change_count >= 10:
#                             break
#                     else:
#                         no_change_count = 0
                        
#                 except Exception as e:
#                     print(f"⚠️ Error finding following: {str(e)}")
                
#                 try:
#                     self.driver.execute_script(
#                         "arguments[0].scrollTop = arguments[0].scrollHeight",
#                         scrollable_element
#                     )
#                     self.human_delay(2, 3)
#                     print(f"📜 Scrolling... Found {len(following)} following so far")
#                 except Exception as e:
#                     print(f"⚠️ Scroll error: {str(e)}")
                
#                 scroll_attempts += 1
            
#             print(f"✅ Successfully scraped {len(following)} following from {username}")
#             return following
            
#         except Exception as e:
#             print(f"❌ Error scraping following from {username}: {str(e)}")
#             return []
    

#     def scrape_post_comments(self, post_url_or_shortcode, max_comments=None):
#         """
#         Scrape comments from an Instagram post
        
#         Args:
#             post_url_or_shortcode: Full Instagram post URL or just the shortcode
#             max_comments: Maximum number of comments to scrape (None = unlimited)
        
#         Returns:
#             List of comment dictionaries
#         """
#         import requests
#         import json
#         import time
#         from datetime import datetime
#         from urllib.parse import quote
        
#         INSTAGRAM_APP_ID = "936619743392459"
        
#         # Extract shortcode if full URL provided
#         if 'instagram.com' in post_url_or_shortcode:
#             parts = post_url_or_shortcode.rstrip('/').split('/')
#             shortcode = None
#             for i, part in enumerate(parts):
#                 if part in ['p', 'reel', 'tv'] and i + 1 < len(parts):
#                     shortcode = parts[i + 1].split('?')[0]
#                     break
#             if not shortcode:
#                 raise ValueError("Invalid Instagram URL")
#         else:
#             shortcode = post_url_or_shortcode
        
#         print(f"💬 Scraping comments for shortcode: {shortcode}")
#         if max_comments:
#             print(f"   📊 Target: {max_comments} comments")
#         else:
#             print(f"   📊 Target: ALL comments")
        
#         comments = []
#         after = None
#         has_next = True
        
#         while has_next:
#             if max_comments and len(comments) >= max_comments:
#                 print(f"✅ Reached comment limit: {max_comments}")
#                 break
            
#             batch_size = 50
#             if max_comments:
#                 remaining = max_comments - len(comments)
#                 batch_size = min(50, remaining)
            
#             variables = {
#                 "shortcode": shortcode,
#                 "first": batch_size,
#             }
            
#             if after:
#                 variables["after"] = after
            
#             variables_json = quote(json.dumps(variables, separators=(',', ':')))
#             url = f"https://www.instagram.com/graphql/query/?query_hash=bc3296d1ce80a24b1b6e40b1e72903f5&variables={variables_json}"
            
#             try:
#                 headers = {
#                     "x-ig-app-id": INSTAGRAM_APP_ID,
#                     "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
#                     "Accept": "*/*",
#                     "Accept-Language": "en-US,en;q=0.9",
#                     "Accept-Encoding": "gzip, deflate, br",
#                     "X-Requested-With": "XMLHttpRequest",
#                     "Origin": "https://www.instagram.com",
#                     "Referer": "https://www.instagram.com/",
#                     "Sec-Fetch-Dest": "empty",
#                     "Sec-Fetch-Mode": "cors",
#                     "Sec-Fetch-Site": "same-origin",
#                 }
                
#                 # Use existing session if available (from login)
#                 if hasattr(self, 'driver') and self.driver:
#                     # Use Selenium cookies if available
#                     cookies = self.driver.get_cookies()
#                     session = requests.Session()
#                     for cookie in cookies:
#                         session.cookies.set(cookie['name'], cookie['value'])
#                     response = session.get(url, headers=headers)
#                 else:
#                     # Fallback to direct request
#                     response = requests.get(url, headers=headers)
                
#                 if response.status_code != 200:
#                     print(f"❌ Failed to fetch comments: Status {response.status_code}")
#                     break
                
#                 data = response.json()
#                 media_data = data.get('data', {}).get('shortcode_media', {})
#                 comment_data = media_data.get('edge_media_to_parent_comment', {})
                
#                 for edge in comment_data.get('edges', []):
#                     if max_comments and len(comments) >= max_comments:
#                         break
                    
#                     node = edge.get('node', {})
#                     owner = node.get('owner', {})
                    
#                     comment = {
#                         "username": username,
#                         "email": "|".join(bio_emails),
#                         "phone": "|".join(bio_phones),
#                         "madid": str(uuid.uuid4()),
#                         "fn": first_name,
#                         "ln": last_name,
#                         "ct": user.get("ct", ""),
#                         "zip": user.get("zip", ""),
#                         "st": user.get("st", ""),
#                         "country": user.get("country", ""),
#                         "dob": user.get("dob", ""),
#                         "doby": user.get("doby", ""),
#                         "gen": user.get("gen", ""),
#                         "age": user.get("age", ""),
#                         "uid": user.get("id", ""),
#                         "value": user.get("valuecountry", ""),
#                         "fbid": user.get("fbid", "")
#                     }
#                     comments.append(comment)
                
#                 page_info = comment_data.get('page_info', {})
#                 has_next = page_info.get('has_next_page', False)
#                 after = page_info.get('end_cursor')
                
#                 print(f"   📊 Scraped {len(comments)} comments so far...")
#                 time.sleep(1)
                
#             except Exception as e:
#                 print(f"❌ Error scraping comments: {str(e)}")
#                 break
        
#         print(f"✅ Total comments scraped: {len(comments)}")
#         return comments



#     def scrape_post_likes(self, post_url, max_likes=100):
#         """
#         Scrape likes and likers from an Instagram post
#         """
#         try:
#             print(f"❤️ Scraping likes from: {post_url}")
#             self.driver.get(post_url)
#             self.human_delay(3, 5)
            
#             likes_data = []
#             seen_usernames = set()
            
#             # Click on likes count to open modal
#             try:
#                 likes_button = WebDriverWait(self.driver, 10).until(
#                     EC.element_to_be_clickable((By.XPATH, 
#                         "//a[contains(@href, '/liked_by/') or contains(text(), 'likes')]"))
#                 )
#                 likes_button.click()
#                 print("🔄 Opened likes modal")
#                 self.human_delay(3, 4)
#             except Exception as e:
#                 print(f"❌ Could not open likes modal: {str(e)}")
#                 return []
            
#             # Wait for modal to load
#             try:
#                 modal = WebDriverWait(self.driver, 10).until(
#                     EC.presence_of_element_located((By.XPATH, "//div[@role='dialog']"))
#                 )
#                 print("✅ Likes modal loaded")
#             except:
#                 print("❌ Likes modal did not load")
#                 return []
            
#             scroll_attempts = 0
#             max_scroll_attempts = 200
#             no_change_count = 0
            
#             # Find scrollable container
#             scrollable_element = None
#             scroll_selectors = [
#                 "//div[@role='dialog']//div[contains(@style, 'overflow')]",
#                 "//div[@role='dialog']//div[contains(@class, 'x')]//div[contains(@style, 'height')]",
#                 "//div[@role='dialog']//ul/parent::div",
#             ]
            
#             for selector in scroll_selectors:
#                 try:
#                     scrollable_element = self.driver.find_element(By.XPATH, selector)
#                     if scrollable_element:
#                         break
#                 except:
#                     continue
            
#             if not scrollable_element:
#                 scrollable_element = modal
            
#             # Scroll and collect likers
#             while len(likes_data) < max_likes and scroll_attempts < max_scroll_attempts:
#                 # Find liker elements
#                 try:
#                     username_selectors = [
#                         "//div[@role='dialog']//a[contains(@href, '/')]/span",
#                         "//div[@role='dialog']//span[contains(@class, 'x')]//span",
#                     ]
                    
#                     liker_elements = []
#                     for selector in username_selectors:
#                         try:
#                             elements = self.driver.find_elements(By.XPATH, selector)
#                             if elements:
#                                 liker_elements = elements
#                                 break
#                         except:
#                             continue
                    
#                     if not liker_elements:
#                         print(f"⚠️ No liker elements found on attempt {scroll_attempts + 1}")
                    
#                     previous_count = len(likes_data)
                    
#                     for element in liker_elements:
#                         try:
#                             username_text = element.text.strip()
                            
#                             # Validate username
#                             if username_text and len(username_text) > 0 and username_text not in seen_usernames:
#                                 if ' ' not in username_text and len(username_text) <= 30:
#                                     seen_usernames.add(username_text)
                                    
#                                     # Get profile URL
#                                     try:
#                                         parent_link = element.find_element(By.XPATH, "./ancestor::a")
#                                         profile_link = parent_link.get_attribute('href')
#                                     except:
#                                         profile_link = f"{Config.INSTAGRAM_URL}/{username_text}/"
                                    
#                                     likes_data.append({
#                                         'username': username_text,
#                                         'profile_url': profile_link,
#                                         'scraped_at': time.strftime('%Y-%m-%d %H:%M:%S')
#                                     })
                                    
#                                     if len(likes_data) >= max_likes:
#                                         break
#                         except:
#                             continue
                    
#                     # Check if we got new likes
#                     if len(likes_data) == previous_count:
#                         no_change_count += 1
#                         if no_change_count >= 10:
#                             print("⚠️ No new likes found after 10 scroll attempts")
#                             break
#                     else:
#                         no_change_count = 0
                        
#                 except Exception as e:
#                     print(f"⚠️ Error finding likes: {str(e)}")
                
#                 # Scroll the modal
#                 try:
#                     self.driver.execute_script(
#                         "arguments[0].scrollTop = arguments[0].scrollHeight",
#                         scrollable_element
#                     )
#                     self.human_delay(2, 3)
#                     print(f"📜 Scrolling... Found {len(likes_data)} likes so far")
#                 except Exception as e:
#                     print(f"⚠️ Scroll error: {str(e)}")
                
#                 scroll_attempts += 1
            
#             print(f"✅ Successfully scraped {len(likes_data)} likes")
#             return likes_data
            
#         except Exception as e:
#             print(f"❌ Error scraping likes: {str(e)}")
#             return []


#     def close(self):
#         """Close the browser safely"""
#         if self.driver:
#             try:
#                 self.driver.quit()
#                 print("🔒 Browser closed")
#             except:
#                 pass
#             finally:
#                 self.driver = None
#                 self.is_logged_in = False
#                 self.current_account = None

import undetected_chromedriver as uc
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import (
    TimeoutException,
    NoSuchElementException,
    WebDriverException,
    NoSuchWindowException
)
import time
import random
import os
import requests
import json
import re
import uuid
from datetime import datetime
from urllib.parse import quote
from config import Config


class InstagramScraper:
    def __init__(self):
        self.driver = None
        self.is_logged_in = False
        self.current_account = None
        self.instagram_app_id = "936619743392459"

    # ===================== COMMON HELPERS =====================

    def init_driver(self):
        """Initialize undetected Chrome driver with robust error handling"""
        try:
            options = uc.ChromeOptions()
            options.add_argument('--disable-blink-features=AutomationControlled')
            options.add_argument('--disable-dev-shm-usage')
            options.add_argument('--no-sandbox')
            options.add_argument('--disable-gpu')
            options.add_argument('--window-size=1920,1080')

            # Stability improvements
            options.add_argument('--disable-extensions')
            options.add_argument('--disable-popup-blocking')
            options.add_argument('--disable-notifications')
            options.add_argument('--disable-infobars')
            options.add_argument('--ignore-certificate-errors')
            options.add_argument('--ignore-ssl-errors')

            # MacOS specific fixes
            options.add_argument('--disable-dev-tools')
            options.add_argument('--remote-debugging-port=9222')

            # Headless mode - can be controlled via environment variable
            if os.getenv('HEADLESS', 'true').lower() == 'true':
                options.add_argument('--headless=new')

            # Random user agent rotation
            user_agents = [
                'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36',
                'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36',
                'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36'
            ]
            options.add_argument(f'user-agent={random.choice(user_agents)}')

            # Initialize driver with version management
            self.driver = uc.Chrome(
                options=options,
                version_main=None,  # Auto-detect Chrome version
                driver_executable_path=None
            )

            self.driver.implicitly_wait(Config.IMPLICIT_WAIT)
            self.driver.set_page_load_timeout(Config.PAGE_LOAD_TIMEOUT)

            # Verify window is accessible
            _ = self.driver.current_url

            print('✅ Chrome driver initialized successfully')
            return self.driver

        except Exception as e:
            print(f"❌ Failed to initialize driver: {str(e)}")
            if self.driver:
                try:
                    self.driver.quit()
                except:
                    pass
            self.driver = None
            raise

    def is_driver_alive(self):
        """Check if the driver is still alive and responsive"""
        try:
            if not self.driver:
                return False
            _ = self.driver.current_url
            return True
        except (WebDriverException, NoSuchWindowException):
            return False

    def human_delay(self, min_delay=None, max_delay=None):
        """Add random delay to mimic human behavior"""
        min_d = min_delay or Config.REQUEST_DELAY_MIN
        max_d = max_delay or Config.REQUEST_DELAY_MAX
        time.sleep(random.uniform(min_d, max_d))

    def extract_emails_from_bio(self, text):
        if not text:
            return []
        return re.findall(r"[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}", text)

    def extract_phones_from_bio(self, text):
        if not text:
            return []
        pattern = r'\+?\d{1,4}?[-.\s]?\(?\d{1,3}\)?[-.\s]?\d{1,4}[-.\s]?\d{1,9}'
        return re.findall(pattern, text)

    # ===================== PROFILE (API) =====================

    def scrape_profile_api(self, username):
        """
        Scrape comprehensive Instagram profile data using Instagram's API
        This method doesn't require authentication and is much faster
        """
        url = f"https://i.instagram.com/api/v1/users/web_profile_info/?username={username}"

        headers = {
            "x-ig-app-id": self.instagram_app_id,
            "User-Agent": (
                "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                "AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
            ),
            "Accept": "*/*",
            "Accept-Language": "en-US,en;q=0.9",
        }

        try:
            print(f"📊 Scraping profile via API: {username}")
            response = requests.get(url, headers=headers, timeout=10)

            if response.status_code != 200:
                print(f"❌ API request failed with status {response.status_code}")
                return None

            data = response.json()
            user = data.get('data', {}).get('user', {})

            if not user:
                print("❌ No user data found in API response")
                return None

            bio = user.get("biography", "") or ""
            bio_emails = self.extract_emails_from_bio(bio)
            bio_phones = self.extract_phones_from_bio(bio)

            full_name = user.get("full_name", "").strip()
            parts = full_name.split(" ", 1)
            first_name = parts[0] if parts else ""
            last_name = parts[1] if len(parts) > 1 else ""

            # Base profile with rich IG info
            profile = {
                "inputUrl": f"https://www.instagram.com/{username}",
                "id": user.get("id"),
                "username": user.get("username"),
                "url": f"https://www.instagram.com/{username}",
                "fullName": user.get("full_name"),
                "biography": bio,
                "externalUrls": user.get("bio_links", []),
                "followersCount": user.get("edge_followed_by", {}).get("count", 0),
                "followsCount": user.get("edge_follow", {}).get("count", 0),
                "hasChannel": user.get("has_channel", False),
                "highlightReelCount": user.get("highlight_reel_count", 0),
                "isBusinessAccount": user.get("is_business_account", False),
                "joinedRecently": user.get("is_joined_recently", False),
                "businessCategoryName": user.get("business_category_name"),
                "private": user.get("is_private", False),
                "verified": user.get("is_verified", False),
                "profilePicUrl": user.get("profile_pic_url"),
                "profilePicUrlHD": user.get("profile_pic_url_hd"),
                "igtvVideoCount": user.get("edge_felix_video_timeline", {}).get("count", 0),
                "relatedProfiles": [],
                "latestIgtvVideos": [],
                "postsCount": user.get("edge_owner_to_timeline_media", {}).get("count", 0),
                "latestPosts": [],
                "businessEmail": user.get("business_email"),
                "businessPhoneNumber": user.get("business_phone_number"),
                "publicEmail": user.get("public_email"),
                "publicPhoneNumber": user.get("public_phone_number"),
                "contactPhoneNumber": user.get("contact_phone_number"),
                "fbid": user.get("fbid"),
                "scraped_at": time.strftime("%Y-%m-%d %H:%M:%S"),
            }

            # 👉 REQUIRED PARAMETER STRUCTURE YOU ASKED FOR
            profile.update({
                "email": "|".join(bio_emails),
                "phone": "|".join(bio_phones),
                "madid": str(uuid.uuid4()),
                "fn": first_name,
                "ln": last_name,
                "ct": user.get("ct", ""),
                "zip": user.get("zip", ""),
                "st": user.get("st", ""),
                "country": user.get("country", ""),
                "dob": user.get("dob", ""),
                "doby": user.get("doby", ""),
                "gen": user.get("gen", ""),
                "age": user.get("age", ""),
                "uid": user.get("id", ""),
                "value": user.get("valuecountry", ""),
                "fbid": user.get("fbid", ""),
            })

            # Extract latest posts with comprehensive details
            posts_data = user.get("edge_owner_to_timeline_media", {}).get("edges", [])

            for edge in posts_data:
                node = edge.get("node", {})

                # Determine post type
                post_type = "Image"
                if node.get("is_video"):
                    post_type = "Video"
                elif node.get("edge_sidecar_to_children"):
                    post_type = "Sidecar"

                # Extract caption
                caption_edges = node.get("edge_media_to_caption", {}).get("edges", [])
                caption = caption_edges[0].get("node", {}).get("text", "") if caption_edges else ""

                # Extract hashtags and mentions from caption
                hashtags = re.findall(r'#(\w+)', caption) if caption else []
                mentions = re.findall(r'@(\w+)', caption) if caption else []

                # Extract tagged users
                tagged_users = []
                tagged_edges = node.get("edge_media_to_tagged_user", {}).get("edges", [])
                for tagged_edge in tagged_edges:
                    tagged_node = tagged_edge.get("node", {}).get("user", {})
                    if tagged_node:
                        tagged_users.append({
                            "full_name": tagged_node.get("full_name"),
                            "id": tagged_node.get("id"),
                            "is_verified": tagged_node.get("is_verified", False),
                            "profile_pic_url": tagged_node.get("profile_pic_url"),
                            "username": tagged_node.get("username")
                        })

                # Extract video URL if it's a video
                video_url = node.get("video_url") if node.get("is_video") else None

                # Build post object
                post = {
                    "id": node.get("id"),
                    "type": post_type,
                    "shortCode": node.get("shortcode"),
                    "caption": caption,
                    "hashtags": hashtags,
                    "mentions": mentions,
                    "url": f"https://www.instagram.com/p/{node.get('shortcode')}/",
                    "commentsCount": node.get("edge_media_to_comment", {}).get("count", 0),
                    "dimensionsHeight": node.get("dimensions", {}).get("height"),
                    "dimensionsWidth": node.get("dimensions", {}).get("width"),
                    "displayUrl": node.get("display_url"),
                    "videoUrl": video_url,
                    "alt": node.get("accessibility_caption"),
                    "likesCount": (
                        node.get("edge_liked_by", {}).get("count", 0)
                        or node.get("edge_media_preview_like", {}).get("count", 0)
                    ),
                    "videoViewCount": node.get("video_view_count"),
                    "timestamp": (
                        datetime.fromtimestamp(node.get("taken_at_timestamp", 0))
                        .strftime("%Y-%m-%dT%H:%M:%S.000Z")
                        if node.get("taken_at_timestamp") else None
                    ),
                    "childPosts": [],
                    "ownerUsername": user.get("username"),
                    "ownerId": user.get("id"),
                    "productType": node.get("product_type"),
                    "taggedUsers": tagged_users,
                    "isCommentsDisabled": node.get("comments_disabled", False)
                }

                # Handle carousel/sidecar posts
                if node.get("edge_sidecar_to_children"):
                    sidecar_edges = node.get("edge_sidecar_to_children", {}).get("edges", [])
                    for sidecar_edge in sidecar_edges:
                        sidecar_node = sidecar_edge.get("node", {})
                        child_post = {
                            "id": sidecar_node.get("id"),
                            "shortCode": sidecar_node.get("shortcode"),
                            "displayUrl": sidecar_node.get("display_url"),
                            "videoUrl": sidecar_node.get("video_url") if sidecar_node.get("is_video") else None,
                            "isVideo": sidecar_node.get("is_video", False)
                        }
                        post["childPosts"].append(child_post)

                profile["latestPosts"].append(post)

            print(f"✅ Successfully scraped profile via API: {username} ({len(profile['latestPosts'])} posts)")
            return profile

        except requests.exceptions.RequestException as e:
            print(f"❌ Request error: {e}")
            return None
        except json.JSONDecodeError as e:
            print(f"❌ JSON decode error: {e}")
            return None
        except Exception as e:
            print(f"❌ Unexpected error scraping profile via API: {e}")
            return None

    # ===================== LOGIN =====================

    def login(self, username, password):
        """Login to Instagram with given credentials and robust error handling"""
        try:
            # Initialize driver if not exists or not alive
            if not self.is_driver_alive():
                print("🔄 Driver not alive, reinitializing...")
                self.close()
                self.init_driver()

            print(f"🔐 Logging in as {username}...")

            # Navigate to login page with error handling
            try:
                self.driver.get(Config.INSTAGRAM_LOGIN_URL)
            except WebDriverException as e:
                print(f"❌ Failed to navigate to login page: {str(e)}")
                return False

            self.human_delay(3, 5)

            # Verify window is still alive
            if not self.is_driver_alive():
                raise Exception("Browser window closed unexpectedly before login")

            # Wait for and fill username
            username_input = WebDriverWait(self.driver, 15).until(
                EC.presence_of_element_located((By.NAME, "username"))
            )
            username_input.clear()
            username_input.send_keys(username)
            self.human_delay(1, 2)

            # Verify window is still alive
            if not self.is_driver_alive():
                raise Exception("Browser window closed unexpectedly during username input")

            # Fill password
            password_input = self.driver.find_element(By.NAME, "password")
            password_input.clear()
            password_input.send_keys(password)
            self.human_delay(1, 2)

            # Click login button
            login_button = self.driver.find_element(By.XPATH, "//button[@type='submit']")
            login_button.click()

            # Wait for login to complete
            self.human_delay(5, 7)

            # Verify window is still alive after login
            if not self.is_driver_alive():
                raise Exception("Browser window closed unexpectedly after login attempt")

            # Handle "Save Your Login Info" popup
            try:
                not_now_button = WebDriverWait(self.driver, 5).until(
                    EC.element_to_be_clickable(
                        (By.XPATH, "//button[contains(text(), 'Not now') or contains(text(), 'Not Now')]")
                    )
                )
                not_now_button.click()
                self.human_delay(2, 3)
            except TimeoutException:
                pass

            # Handle "Turn on Notifications" popup
            try:
                not_now_button = WebDriverWait(self.driver, 5).until(
                    EC.element_to_be_clickable((By.XPATH, "//button[contains(text(), 'Not Now')]"))
                )
                not_now_button.click()
                self.human_delay(2, 3)
            except TimeoutException:
                pass

            # Verify successful login by checking URL or elements
            current_url = self.driver.current_url
            if "login" in current_url.lower():
                # Check for error messages
                try:
                    error_elem = self.driver.find_element(
                        By.XPATH,
                        "//*[contains(text(), 'incorrect') or contains(text(), 'Sorry')]"
                    )
                    raise Exception(f"Login failed: {error_elem.text}")
                except NoSuchElementException:
                    raise Exception("Login failed: Still on login page")

            self.is_logged_in = True
            self.current_account = username
            print(f"✅ Successfully logged in as {username}")
            return True

        except NoSuchWindowException as e:
            print(f"❌ Login failed: Browser window was closed - {str(e)}")
            self.close()
            return False
        except WebDriverException as e:
            print(f"❌ Login failed: WebDriver error - {str(e)}")
            self.close()
            return False
        except Exception as e:
            print(f"❌ Login failed: {str(e)}")
            return False

    # ===================== PROFILE (SELENIUM FALLBACK) =====================

    def scrape_profile(self, username):
        """
        Scrape profile information - tries API first, falls back to Selenium
        """
        profile = self.scrape_profile_api(username)
        if profile:
            return profile

        print(f"⚠️ API method failed, falling back to Selenium for {username}")
        return self.scrape_profile_selenium(username)

    def scrape_profile_selenium(self, username):
        """Scrape profile information using Selenium (fallback method)"""
        try:
            profile_url = f"{Config.INSTAGRAM_URL}/{username}/"
            print(f"📊 Scraping profile via Selenium: {username}")
            self.driver.get(profile_url)
            self.human_delay(3, 5)

            profile_data = {
                'username': username,
                'url': profile_url,
                'scraped_at': time.strftime('%Y-%m-%d %H:%M:%S')
            }

            try:
                followers_elem = self.driver.find_element(
                    By.XPATH,
                    "//a[contains(@href, '/followers/')]/span"
                )
                profile_data['followers'] = followers_elem.get_attribute('title') or followers_elem.text
            except NoSuchElementException:
                profile_data['followers'] = 'N/A'

            try:
                following_elem = self.driver.find_element(
                    By.XPATH,
                    "//a[contains(@href, '/following/')]/span"
                )
                profile_data['following'] = following_elem.text
            except NoSuchElementException:
                profile_data['following'] = 'N/A'

            try:
                posts_elem = self.driver.find_element(
                    By.XPATH,
                    "//span[contains(text(), 'posts')]/span"
                )
                profile_data['posts_count'] = posts_elem.text
            except NoSuchElementException:
                profile_data['posts_count'] = 'N/A'

            try:
                bio_elem = self.driver.find_element(By.XPATH, "//div[@class='_aa_c']/span")
                profile_data['bio'] = bio_elem.text
            except NoSuchElementException:
                profile_data['bio'] = 'N/A'

            try:
                name_elem = self.driver.find_element(
                    By.XPATH,
                    "//span[@class='_aacl _aaco _aacw _aacx _aad7 _aade']"
                )
                profile_data['full_name'] = name_elem.text
            except NoSuchElementException:
                profile_data['full_name'] = 'N/A'

            print(f"✅ Scraped profile via Selenium: {username}")
            return profile_data

        except Exception as e:
            print(f"❌ Error scraping profile {username}: {str(e)}")
            raise e

    # ===================== POSTS & HASHTAGS =====================

    def scrape_posts(self, username, max_posts=12):
        """Scrape posts from a profile"""
        try:
            profile_url = f"{Config.INSTAGRAM_URL}/{username}/"
            print(f"📸 Scraping posts from {username}")
            self.driver.get(profile_url)
            self.human_delay(3, 5)

            posts_data = []
            last_height = self.driver.execute_script("return document.body.scrollHeight")
            posts_loaded = 0

            while posts_loaded < max_posts:
                post_links = self.driver.find_elements(By.XPATH, "//a[contains(@href, '/p/')]")

                for link in post_links[:max_posts]:
                    if posts_loaded >= max_posts:
                        break

                    try:
                        post_url = link.get_attribute('href')
                        img = link.find_element(By.TAG_NAME, 'img')
                        img_src = img.get_attribute('src')
                        alt_text = img.get_attribute('alt')

                        posts_data.append({
                            'post_url': post_url,
                            'image_url': img_src,
                            'caption_preview': alt_text[:100] if alt_text else 'N/A',
                            'scraped_at': time.strftime('%Y-%m-%d %H:%M:%S')
                        })
                        posts_loaded += 1

                    except Exception:
                        continue

                self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
                self.human_delay(2, 4)

                new_height = self.driver.execute_script("return document.body.scrollHeight")
                if new_height == last_height:
                    break
                last_height = new_height

            print(f"✅ Scraped {len(posts_data)} posts from {username}")
            return posts_data

        except Exception as e:
            print(f"❌ Error scraping posts from {username}: {str(e)}")
            raise e

    def scrape_hashtag(self, hashtag, max_posts=20):
        """Scrape posts from a hashtag"""
        try:
            hashtag_url = f"{Config.INSTAGRAM_URL}/explore/tags/{hashtag.replace('#', '')}/"
            print(f"#️⃣ Scraping hashtag: #{hashtag}")
            self.driver.get(hashtag_url)
            self.human_delay(3, 5)

            posts_data = []
            posts_loaded = 0
            last_height = self.driver.execute_script("return document.body.scrollHeight")

            while posts_loaded < max_posts:
                post_links = self.driver.find_elements(By.XPATH, "//a[contains(@href, '/p/')]")

                for link in post_links[:max_posts]:
                    if posts_loaded >= max_posts:
                        break

                    try:
                        post_url = link.get_attribute('href')
                        img = link.find_element(By.TAG_NAME, 'img')
                        img_src = img.get_attribute('src')

                        posts_data.append({
                            'post_url': post_url,
                            'image_url': img_src,
                            'hashtag': hashtag,
                            'scraped_at': time.strftime('%Y-%m-%d %H:%M:%S')
                        })
                        posts_loaded += 1

                    except Exception:
                        continue

                self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
                self.human_delay(2, 4)

                new_height = self.driver.execute_script("return document.body.scrollHeight")
                if new_height == last_height:
                    break
                last_height = new_height

            print(f"✅ Scraped {len(posts_data)} posts from #{hashtag}")
            return posts_data

        except Exception as e:
            print(f"❌ Error scraping hashtag #{hashtag}: {str(e)}")
            raise e

    # ===================== FOLLOWERS / FOLLOWING =====================

    def scrape_followers(self, username, max_followers=100):
        """Scrape followers list"""
        try:
            profile_url = f"{Config.INSTAGRAM_URL}/{username}/"
            print(f"👥 Scraping followers from: {username}")
            self.driver.get(profile_url)
            self.human_delay(3, 5)

            try:
                followers_link = WebDriverWait(self.driver, 10).until(
                    EC.element_to_be_clickable((By.XPATH, "//a[contains(@href, '/followers/')]"))
                )
                followers_link.click()
                print("🔄 Opened followers modal")
                self.human_delay(3, 4)
            except Exception as e:
                print(f"❌ Could not open followers modal: {str(e)}")
                return []

            try:
                modal = WebDriverWait(self.driver, 10).until(
                    EC.presence_of_element_located((By.XPATH, "//div[@role='dialog']"))
                )
                print("✅ Followers modal loaded")
            except Exception:
                print("❌ Followers modal did not load")
                return []

            followers = []
            seen_usernames = set()
            scroll_attempts = 0
            max_scroll_attempts = 200
            no_change_count = 0

            scrollable_element = None
            scroll_selectors = [
                "//div[@role='dialog']//div[contains(@style, 'overflow')]",
                "//div[@role='dialog']//div[contains(@class, 'x')]//div[contains(@style, 'height')]",
                "//div[@role='dialog']//ul/parent::div",
            ]

            for selector in scroll_selectors:
                try:
                    scrollable_element = self.driver.find_element(By.XPATH, selector)
                    if scrollable_element:
                        print("✅ Found scrollable element")
                        break
                except Exception:
                    continue

            if not scrollable_element:
                scrollable_element = modal

            while len(followers) < max_followers and scroll_attempts < max_scroll_attempts:
                try:
                    follower_elements = []
                    username_selectors = [
                        "//div[@role='dialog']//a[contains(@href, '/')]/span",
                        "//div[@role='dialog']//span[contains(@class, 'x')]//span",
                    ]

                    for selector in username_selectors:
                        try:
                            elements = self.driver.find_elements(By.XPATH, selector)
                            if elements:
                                follower_elements = elements
                                break
                        except Exception:
                            continue

                    previous_count = len(followers)

                    for element in follower_elements:
                        try:
                            username_text = element.text.strip()
                            if username_text and username_text not in seen_usernames:
                                if ' ' not in username_text and len(username_text) <= 30:
                                    seen_usernames.add(username_text)

                                    try:
                                        parent_link = element.find_element(By.XPATH, "./ancestor::a")
                                        profile_link = parent_link.get_attribute('href')
                                    except Exception:
                                        profile_link = f"{Config.INSTAGRAM_URL}/{username_text}/"

                                    follower_data = {
                                        'username': username_text,
                                        'profile_url': profile_link,
                                        'scraped_at': time.strftime('%Y-%m-%d %H:%M:%S')
                                    }
                                    followers.append(follower_data)

                                    if len(followers) >= max_followers:
                                        break
                        except Exception:
                            continue

                    if len(followers) == previous_count:
                        no_change_count += 1
                        if no_change_count >= 10:
                            break
                    else:
                        no_change_count = 0

                except Exception as e:
                    print(f"⚠️ Error finding followers: {str(e)}")

                try:
                    self.driver.execute_script(
                        "arguments[0].scrollTop = arguments[0].scrollHeight",
                        scrollable_element
                    )
                    self.human_delay(2, 3)
                    print(f"📜 Scrolling... Found {len(followers)} followers so far")
                except Exception as e:
                    print(f"⚠️ Scroll error: {str(e)}")

                scroll_attempts += 1

            print(f"✅ Successfully scraped {len(followers)} followers from {username}")
            return followers

        except Exception as e:
            print(f"❌ Error scraping followers from {username}: {str(e)}")
            return []

    def scrape_following(self, username, max_following=100):
        """Scrape following list"""
        try:
            profile_url = f"{Config.INSTAGRAM_URL}/{username}/"
            print(f"👤 Scraping following from: {username}")
            self.driver.get(profile_url)
            self.human_delay(3, 5)

            try:
                following_link = WebDriverWait(self.driver, 10).until(
                    EC.element_to_be_clickable((By.XPATH, "//a[contains(@href, '/following/')]"))
                )
                following_link.click()
                print("🔄 Opened following modal")
                self.human_delay(3, 4)
            except Exception as e:
                print(f"❌ Could not open following modal: {str(e)}")
                return []

            try:
                modal = WebDriverWait(self.driver, 10).until(
                    EC.presence_of_element_located((By.XPATH, "//div[@role='dialog']"))
                )
                print("✅ Following modal loaded")
            except Exception:
                print("❌ Following modal did not load")
                return []

            following = []
            seen_usernames = set()
            scroll_attempts = 0
            max_scroll_attempts = 200
            no_change_count = 0

            scrollable_element = None
            scroll_selectors = [
                "//div[@role='dialog']//div[contains(@style, 'overflow')]",
                "//div[@role='dialog']//div[contains(@class, 'x')]//div[contains(@style, 'height')]",
                "//div[@role='dialog']//ul/parent::div",
            ]

            for selector in scroll_selectors:
                try:
                    scrollable_element = self.driver.find_element(By.XPATH, selector)
                    if scrollable_element:
                        break
                except Exception:
                    continue

            if not scrollable_element:
                scrollable_element = modal

            while len(following) < max_following and scroll_attempts < max_scroll_attempts:
                try:
                    following_elements = []
                    username_selectors = [
                        "//div[@role='dialog']//a[contains(@href, '/')]/span",
                        "//div[@role='dialog']//span[contains(@class, 'x')]//span",
                    ]

                    for selector in username_selectors:
                        try:
                            elements = self.driver.find_elements(By.XPATH, selector)
                            if elements:
                                following_elements = elements
                                break
                        except Exception:
                            continue

                    previous_count = len(following)

                    for element in following_elements:
                        try:
                            username_text = element.text.strip()
                            if username_text and username_text not in seen_usernames:
                                if ' ' not in username_text and len(username_text) <= 30:
                                    seen_usernames.add(username_text)

                                    try:
                                        parent_link = element.find_element(By.XPATH, "./ancestor::a")
                                        profile_link = parent_link.get_attribute('href')
                                    except Exception:
                                        profile_link = f"{Config.INSTAGRAM_URL}/{username_text}/"

                                    following_data = {
                                        'username': username_text,
                                        'profile_url': profile_link,
                                        'scraped_at': time.strftime('%Y-%m-%d %H:%M:%S')
                                    }
                                    following.append(following_data)

                                    if len(following) >= max_following:
                                        break
                        except Exception:
                            continue

                    if len(following) == previous_count:
                        no_change_count += 1
                        if no_change_count >= 10:
                            break
                    else:
                        no_change_count = 0

                except Exception as e:
                    print(f"⚠️ Error finding following: {str(e)}")

                try:
                    self.driver.execute_script(
                        "arguments[0].scrollTop = arguments[0].scrollHeight",
                        scrollable_element
                    )
                    self.human_delay(2, 3)
                    print(f"📜 Scrolling... Found {len(following)} following so far")
                except Exception as e:
                    print(f"⚠️ Scroll error: {str(e)}")

                scroll_attempts += 1

            print(f"✅ Successfully scraped {len(following)} following from {username}")
            return following

        except Exception as e:
            print(f"❌ Error scraping following from {username}: {str(e)}")
            return []

    # ===================== COMMENTS (YOUR PARAM STRUCTURE) =====================

    def scrape_post_comments(self, post_url_or_shortcode, max_comments=None):
        """
        Scrape comments from an Instagram post
        Return one record per commenter with your parameter structure
        """

        # Extract shortcode if full URL provided
        if 'instagram.com' in post_url_or_shortcode:
            parts = post_url_or_shortcode.rstrip('/').split('/')
            shortcode = None
            for i, part in enumerate(parts):
                if part in ['p', 'reel', 'tv'] and i + 1 < len(parts):
                    shortcode = parts[i + 1].split('?')[0]
                    break
            if not shortcode:
                raise ValueError("Invalid Instagram URL")
        else:
            shortcode = post_url_or_shortcode

        print(f"💬 Scraping comments for shortcode: {shortcode}")
        if max_comments:
            print(f"   📊 Target: {max_comments} comments")
        else:
            print("   📊 Target: ALL comments")

        comments = []
        after = None
        has_next = True

        while has_next:
            if max_comments and len(comments) >= max_comments:
                print(f"✅ Reached comment limit: {max_comments}")
                break

            batch_size = 50
            if max_comments:
                remaining = max_comments - len(comments)
                batch_size = min(50, remaining)

            variables = {
                "shortcode": shortcode,
                "first": batch_size,
            }

            if after:
                variables["after"] = after

            variables_json = quote(json.dumps(variables, separators=(',', ':')))
            url = (
                "https://www.instagram.com/graphql/query/"
                "?query_hash=bc3296d1ce80a24b1b6e40b1e72903f5"
                f"&variables={variables_json}"
            )

            try:
                headers = {
                    "x-ig-app-id": self.instagram_app_id,
                    "User-Agent": (
                        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) "
                        "AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
                    ),
                    "Accept": "*/*",
                    "Accept-Language": "en-US,en;q=0.9",
                    "Accept-Encoding": "gzip, deflate, br",
                    "X-Requested-With": "XMLHttpRequest",
                    "Origin": "https://www.instagram.com",
                    "Referer": "https://www.instagram.com/",
                }

                # Use existing session if available (from login)
                if self.driver:
                    cookies = self.driver.get_cookies()
                    session = requests.Session()
                    for cookie in cookies:
                        session.cookies.set(cookie['name'], cookie['value'])
                    response = session.get(url, headers=headers)
                else:
                    response = requests.get(url, headers=headers)

                if response.status_code != 200:
                    print(f"❌ Failed to fetch comments: Status {response.status_code}")
                    break

                data = response.json()
                media_data = data.get('data', {}).get('shortcode_media', {})
                if not media_data:
                    print("❌ No media data found for this shortcode")
                    break

                comment_data = media_data.get('edge_media_to_parent_comment', {})

                for edge in comment_data.get('edges', []):
                    if max_comments and len(comments) >= max_comments:
                        break

                    node = edge.get('node', {})
                    owner = node.get('owner', {})

                    commenter_username = owner.get("username")
                    if not commenter_username:
                        continue

                    # Fetch full profile data for commenter (to fill your schema)
                    profile = self.scrape_profile_api(commenter_username)
                    if not profile:
                        continue

                    # bio-based contact info
                    bio = profile.get("biography", "") or ""
                    bio_emails = self.extract_emails_from_bio(bio)
                    bio_phones = self.extract_phones_from_bio(bio)

                    full_name = profile.get("fullName", "") or ""
                    parts = full_name.split(" ", 1)
                    first_name = parts[0] if parts else ""
                    last_name = parts[1] if len(parts) > 1 else ""

                    # we still compute created_at if you want to log it elsewhere
                    created_at_ts = node.get("created_at")
                    _created_at = (
                        datetime.fromtimestamp(created_at_ts).strftime("%Y-%m-%d %H:%M:%S")
                        if created_at_ts else ""
                    )

                    # Build object with YOUR required parameters ONLY
                    comment_obj = {
                        "username": commenter_username,
                        "email": "|".join(bio_emails),
                        "phone": "|".join(bio_phones),
                        "madid": str(uuid.uuid4()),
                        "fn": first_name,
                        "ln": last_name,
                        "ct": profile.get("ct", ""),
                        "zip": profile.get("zip", ""),
                        "st": profile.get("st", ""),
                        "country": profile.get("country", ""),
                        "dob": profile.get("dob", ""),
                        "doby": profile.get("doby", ""),
                        "gen": profile.get("gen", ""),
                        "age": profile.get("age", ""),
                        "uid": profile.get("uid", "") or profile.get("id", ""),
                        "value": profile.get("value", ""),
                        "fbid": profile.get("fbid", "")
                    }

                    comments.append(comment_obj)

                page_info = comment_data.get('page_info', {})
                has_next = page_info.get('has_next_page', False)
                after = page_info.get('end_cursor')

                print(f"   📊 Scraped {len(comments)} comments so far...")
                time.sleep(1)

            except Exception as e:
                print(f"❌ Error scraping comments: {str(e)}")
                break

        print(f"✅ Total comments scraped: {len(comments)}")
        return comments

    # ===================== LIKES =====================

    def scrape_post_likes(self, post_url, max_likes=100):
        """
        Scrape likes and likers from an Instagram post
        """
        try:
            print(f"❤️ Scraping likes from: {post_url}")
            self.driver.get(post_url)
            self.human_delay(3, 5)

            likes_data = []
            seen_usernames = set()

            # Click on likes count to open modal
            try:
                likes_button = WebDriverWait(self.driver, 10).until(
                    EC.element_to_be_clickable(
                        (By.XPATH, "//a[contains(@href, '/liked_by/') or contains(text(), 'likes')]")
                    )
                )
                likes_button.click()
                print("🔄 Opened likes modal")
                self.human_delay(3, 4)
            except Exception as e:
                print(f"❌ Could not open likes modal: {str(e)}")
                return []

            # Wait for modal to load
            try:
                modal = WebDriverWait(self.driver, 10).until(
                    EC.presence_of_element_located((By.XPATH, "//div[@role='dialog']"))
                )
                print("✅ Likes modal loaded")
            except Exception:
                print("❌ Likes modal did not load")
                return []

            scroll_attempts = 0
            max_scroll_attempts = 200
            no_change_count = 0

            # Find scrollable container
            scrollable_element = None
            scroll_selectors = [
                "//div[@role='dialog']//div[contains(@style, 'overflow')]",
                "//div[@role='dialog']//div[contains(@class, 'x')]//div[contains(@style, 'height')]",
                "//div[@role='dialog']//ul/parent::div",
            ]

            for selector in scroll_selectors:
                try:
                    scrollable_element = self.driver.find_element(By.XPATH, selector)
                    if scrollable_element:
                        break
                except Exception:
                    continue

            if not scrollable_element:
                scrollable_element = modal

            # Scroll and collect likers
            while len(likes_data) < max_likes and scroll_attempts < max_scroll_attempts:
                try:
                    username_selectors = [
                        "//div[@role='dialog']//a[contains(@href, '/')]/span",
                        "//div[@role='dialog']//span[contains(@class, 'x')]//span",
                    ]

                    liker_elements = []
                    for selector in username_selectors:
                        try:
                            elements = self.driver.find_elements(By.XPATH, selector)
                            if elements:
                                liker_elements = elements
                                break
                        except Exception:
                            continue

                    if not liker_elements:
                        print(f"⚠️ No liker elements found on attempt {scroll_attempts + 1}")

                    previous_count = len(likes_data)

                    for element in liker_elements:
                        try:
                            username_text = element.text.strip()

                            if username_text and username_text not in seen_usernames:
                                if ' ' not in username_text and len(username_text) <= 30:
                                    seen_usernames.add(username_text)

                                    try:
                                        parent_link = element.find_element(By.XPATH, "./ancestor::a")
                                        profile_link = parent_link.get_attribute('href')
                                    except Exception:
                                        profile_link = f"{Config.INSTAGRAM_URL}/{username_text}/"

                                    likes_data.append({
                                        'username': username_text,
                                        'profile_url': profile_link,
                                        'scraped_at': time.strftime('%Y-%m-%d %H:%M:%S')
                                    })

                                    if len(likes_data) >= max_likes:
                                        break
                        except Exception:
                            continue

                    if len(likes_data) == previous_count:
                        no_change_count += 1
                        if no_change_count >= 10:
                            print("⚠️ No new likes found after 10 scroll attempts")
                            break
                    else:
                        no_change_count = 0

                except Exception as e:
                    print(f"⚠️ Error finding likes: {str(e)}")

                try:
                    self.driver.execute_script(
                        "arguments[0].scrollTop = arguments[0].scrollHeight",
                        scrollable_element
                    )
                    self.human_delay(2, 3)
                    print(f"📜 Scrolling... Found {len(likes_data)} likes so far")
                except Exception as e:
                    print(f"⚠️ Scroll error: {str(e)}")

                scroll_attempts += 1

            print(f"✅ Successfully scraped {len(likes_data)} likes")
            return likes_data

        except Exception as e:
            print(f"❌ Error scraping likes: {str(e)}")
            return []

    # ===================== CLOSE =====================

    def close(self):
        """Close the browser safely"""
        if self.driver:
            try:
                self.driver.quit()
                print("🔒 Browser closed")
            except Exception:
                pass
            finally:
                self.driver = None
                self.is_logged_in = False
                self.current_account = None
