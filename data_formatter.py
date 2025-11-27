

import csv
from io import StringIO
from typing import List, Dict, Any
import json

class DataFormatter:
    """Format nested Instagram data into flat table structure"""
    
    @staticmethod
    def flatten_profile_data(profile_data: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Flatten nested profile data structure into rows suitable for tables/CSV"""
        if not profile_data:
            return []
        
        rows = []
        
        # Extract ALL profile-level data - each field gets its own column
        profile_base = {
            # Basic Profile Info
            'input_url': profile_data.get('inputUrl', ''),
            'profile_id': profile_data.get('id', ''),
            'username': profile_data.get('username', ''),
            'profile_url': profile_data.get('url', ''),
            'full_name': profile_data.get('fullName', ''),
            'biography': profile_data.get('biography', ''),
            
            # Counts
            'followers_count': profile_data.get('followersCount', 0),
            'following_count': profile_data.get('followsCount', 0),
            'posts_count': profile_data.get('postsCount', 0),
            'highlight_reel_count': profile_data.get('highlightReelCount', 0),
            'igtv_video_count': profile_data.get('igtvVideoCount', 0),
            
            # Status Flags
            'is_verified': profile_data.get('verified', False),
            'is_private': profile_data.get('private', False),
            'is_business_account': profile_data.get('isBusinessAccount', False),
            'has_channel': profile_data.get('hasChannel', False),
            'joined_recently': profile_data.get('joinedRecently', False),
            
            # Business Info
            'business_category_name': profile_data.get('businessCategoryName', ''),
            'business_email': profile_data.get('businessEmail', ''),
            'business_phone_number': profile_data.get('businessPhoneNumber', ''),
            'public_email': profile_data.get('publicEmail', ''),
            'public_phone_number': profile_data.get('publicPhoneNumber', ''),
            'contact_phone_number': profile_data.get('contactPhoneNumber', ''),
            
            # Profile Pictures
            'profile_pic_url': profile_data.get('profilePicUrl', ''),
            'profile_pic_hd_url': profile_data.get('profilePicUrlHD', ''),
            
            # Social IDs
            'fbid': profile_data.get('fbid', ''),
            
            # Timestamp
            'scraped_at': profile_data.get('scraped_at', '')
        }
        
        # Handle external URLs - create separate columns (up to 5)
        external_urls = profile_data.get('externalUrls', [])
        for idx in range(5):
            if idx < len(external_urls):
                url_obj = external_urls[idx]
                if isinstance(url_obj, dict):
                    profile_base[f'external_url_{idx + 1}'] = url_obj.get('url', '')
                    profile_base[f'external_url_{idx + 1}_title'] = url_obj.get('title', '')
                else:
                    profile_base[f'external_url_{idx + 1}'] = str(url_obj)
                    profile_base[f'external_url_{idx + 1}_title'] = ''
            else:
                profile_base[f'external_url_{idx + 1}'] = ''
                profile_base[f'external_url_{idx + 1}_title'] = ''
        
        # Extract posts
        latest_posts = profile_data.get('latestPosts', [])
        
        if not latest_posts:
            # Return just profile data if no posts
            rows.append(profile_base)
        else:
            # Create a row for each post with ALL post details
            for post_idx, post in enumerate(latest_posts, 1):
                row = profile_base.copy()
                
                # Add ALL post-level data - each field gets its own column
                row.update({
                    # Post Identification
                    'post_number': post_idx,
                    'post_id': post.get('id', ''),
                    'post_type': post.get('type', ''),
                    'post_shortcode': post.get('shortCode', ''),
                    'post_url': post.get('url', ''),
                    
                    # Post Content
                    'post_caption': post.get('caption', ''),
                    'post_alt_text': post.get('alt', ''),
                    
                    # Engagement Metrics
                    'post_likes_count': post.get('likesCount', 0),
                    'post_comments_count': post.get('commentsCount', 0),
                    'post_video_views': post.get('videoViewCount', 0),
                    
                    # Post Metadata
                    'post_timestamp': post.get('timestamp', ''),
                    'post_product_type': post.get('productType', ''),
                    'post_is_comments_disabled': post.get('isCommentsDisabled', False),
                    
                    # Media URLs
                    'post_display_url': post.get('displayUrl', ''),
                    'post_video_url': post.get('videoUrl', ''),
                    
                    # Dimensions
                    'post_dimensions_height': post.get('dimensionsHeight', ''),
                    'post_dimensions_width': post.get('dimensionsWidth', ''),
                    
                    # Owner Info
                    'post_owner_username': post.get('ownerUsername', ''),
                    'post_owner_id': post.get('ownerId', ''),
                    
                    # Child Posts Count (for carousels)
                    'post_child_count': len(post.get('childPosts', []))
                })
                
                # Hashtags - create separate columns for first 20 hashtags
                hashtags = post.get('hashtags', [])
                row['hashtags_count'] = len(hashtags)
                for idx in range(20):
                    row[f'hashtag_{idx + 1}'] = hashtags[idx] if idx < len(hashtags) else ''
                
                # Mentions - create separate columns for first 20 mentions
                mentions = post.get('mentions', [])
                row['mentions_count'] = len(mentions)
                for idx in range(20):
                    row[f'mention_{idx + 1}'] = mentions[idx] if idx < len(mentions) else ''
                
                # Tagged users - create separate columns for first 10 users
                tagged_users = post.get('taggedUsers', [])
                row['tagged_users_count'] = len(tagged_users)
                for idx in range(10):
                    if idx < len(tagged_users):
                        user = tagged_users[idx]
                        row[f'tagged_user_{idx + 1}_username'] = user.get('username', '')
                        row[f'tagged_user_{idx + 1}_full_name'] = user.get('full_name', '')
                        row[f'tagged_user_{idx + 1}_id'] = user.get('id', '')
                        row[f'tagged_user_{idx + 1}_is_verified'] = user.get('is_verified', False)
                        row[f'tagged_user_{idx + 1}_profile_pic'] = user.get('profile_pic_url', '')
                    else:
                        row[f'tagged_user_{idx + 1}_username'] = ''
                        row[f'tagged_user_{idx + 1}_full_name'] = ''
                        row[f'tagged_user_{idx + 1}_id'] = ''
                        row[f'tagged_user_{idx + 1}_is_verified'] = ''
                        row[f'tagged_user_{idx + 1}_profile_pic'] = ''
                
                # Child posts (carousel items) - create columns for first 10 child posts
                child_posts = post.get('childPosts', [])
                for idx in range(10):
                    if idx < len(child_posts):
                        child = child_posts[idx]
                        row[f'child_post_{idx + 1}_id'] = child.get('id', '')
                        row[f'child_post_{idx + 1}_shortcode'] = child.get('shortCode', '')
                        row[f'child_post_{idx + 1}_display_url'] = child.get('displayUrl', '')
                        row[f'child_post_{idx + 1}_video_url'] = child.get('videoUrl', '')
                        row[f'child_post_{idx + 1}_is_video'] = child.get('isVideo', False)
                    else:
                        row[f'child_post_{idx + 1}_id'] = ''
                        row[f'child_post_{idx + 1}_shortcode'] = ''
                        row[f'child_post_{idx + 1}_display_url'] = ''
                        row[f'child_post_{idx + 1}_video_url'] = ''
                        row[f'child_post_{idx + 1}_is_video'] = ''
                
                # Images array (if any separate image URLs exist)
                images = post.get('images', [])
                for idx in range(5):
                    row[f'image_{idx + 1}_url'] = images[idx] if idx < len(images) else ''
                
                rows.append(row)
        
        return rows
    
    @staticmethod
    def flatten_posts_data(posts_data: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Flatten posts data into table format"""
        if not posts_data:
            return []
        
        rows = []
        for idx, post in enumerate(posts_data, 1):
            row = {
                'post_number': idx,
                # support both new ('post_url') and old ('posturl') keys
                'post_url': post.get('post_url', '') or post.get('posturl', ''),
                'image_url': post.get('image_url', '') or post.get('imageurl', ''),
                'caption_preview': post.get('caption_preview', '') or post.get('captionpreview', ''),
                'scraped_at': post.get('scraped_at', '')
            }
            rows.append(row)
        
        return rows
    
    @staticmethod
    def flatten_followers_data(followers_data: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Flatten followers data into table format"""
        if not followers_data:
            return []
        
        rows = []
        for idx, follower in enumerate(followers_data, 1):
            row = {
                'index': idx,
                'username': follower.get('username', ''),
                'full_name': follower.get('full_name', ''),
                'profile_url': follower.get('profile_url', '') or follower.get('profileurl', ''),
                'profile_pic_url': follower.get('profile_pic_url', ''),
                'is_verified': follower.get('is_verified', False),
                'is_private': follower.get('is_private', False),
                'scraped_at': follower.get('scraped_at', '')
            }
            rows.append(row)
        
        return rows
    
    @staticmethod
    def flatten_following_data(following_data: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Flatten following data into table format"""
        return DataFormatter.flatten_followers_data(following_data)
    
    @staticmethod
    def flatten_hashtag_data(hashtag_data: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Flatten hashtag posts data into table format"""
        if not hashtag_data:
            return []
        
        rows = []
        for idx, post in enumerate(hashtag_data, 1):
            row = {
                'index': idx,
                'post_url': post.get('post_url', '') or post.get('posturl', ''),
                'image_url': post.get('image_url', '') or post.get('imageurl', ''),
                'hashtag': post.get('hashtag', ''),
                'likes_count': post.get('likes_count', 0),
                'comments_count': post.get('comments_count', 0),
                'scraped_at': post.get('scraped_at', '')
            }
            rows.append(row)
        
        return rows
    
    @staticmethod
    def flatten_comments_data(comments_data: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """
        Flatten comments data into table format.
        With the new scraper, each comment is already a "lead":
        {
            "username", "email", "phone", "madid",
            "fn", "ln", "ct", "zip", "st",
            "country", "dob", "doby", "gen", "age",
            "uid", "value", "fbid"
        }
        """
        if not comments_data:
            return []
        
        lead_fields = [
            "username",
            "email",
            "phone",
            "madid",
            "fn",
            "ln",
            "ct",
            "zip",
            "st",
            "country",
            "dob",
            "doby",
            "gen",
            "age",
            "uid",
            "value",
            "fbid",
        ]
        
        rows = []
        for idx, comment in enumerate(comments_data, 1):
            row = {"comment_number": idx}
            for field in lead_fields:
                row[field] = comment.get(field, "")
            rows.append(row)
        
        return rows
    
    @staticmethod
    def flatten_likes_data(likes_data: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Flatten likes data into table format"""
        if not likes_data:
            return []
        
        rows = []
        for idx, like in enumerate(likes_data, 1):
            row = {
                'index': idx,
                'username': like.get('username', ''),
                'full_name': like.get('full_name', ''),
                'profile_url': like.get('profile_url', '') or like.get('profileurl', ''),
                'profile_pic_url': like.get('profile_pic_url', ''),
                'is_verified': like.get('is_verified', False),
                'is_private': like.get('is_private', False),
                'scraped_at': like.get('scraped_at', '')
            }
            rows.append(row)
        
        return rows
    
    @staticmethod
    def format_for_task_type(task_type: str, data: Any) -> List[Dict[str, Any]]:
        """Format data based on task type"""
        if not data:
            return []
        
        # If data is wrapped in extra layers, unwrap it
        if isinstance(data, list) and len(data) > 0:
            if isinstance(data[0], dict) and 'data' in data[0]:
                data = data[0]['data']
        
        if task_type == 'profile':
            # Handle both single dict and list containing dict
            if isinstance(data, list) and len(data) > 0:
                data = data[0]
            return DataFormatter.flatten_profile_data(data)
        
        elif task_type == 'posts':
            if isinstance(data, dict):
                data = [data]
            return DataFormatter.flatten_posts_data(data)
        
        elif task_type == 'followers':
            if isinstance(data, dict):
                data = [data]
            return DataFormatter.flatten_followers_data(data)
        
        elif task_type == 'following':
            if isinstance(data, dict):
                data = [data]
            return DataFormatter.flatten_following_data(data)
        
        elif task_type == 'hashtag':
            if isinstance(data, dict):
                data = [data]
            return DataFormatter.flatten_hashtag_data(data)
        
        elif task_type == 'comments':
            if isinstance(data, dict):
                data = [data]
            return DataFormatter.flatten_comments_data(data)
        
        elif task_type == 'likes':
            if isinstance(data, dict):
                data = [data]
            return DataFormatter.flatten_likes_data(data)
        
        else:
            # Return as-is for unknown types
            if isinstance(data, dict):
                return [data]
            return data if isinstance(data, list) else [data]
        
    @staticmethod
    def to_csv(rows: List[Dict[str, Any]]) -> str:
        """Convert rows to CSV string"""
        if not rows:
            return ""
        
        output = StringIO()
        
        # Get all unique fieldnames from all rows (in case columns vary)
        fieldnames = []
        seen = set()
        for row in rows:
            for key in row.keys():
                if key not in seen:
                    fieldnames.append(key)
                    seen.add(key)
        
        writer = csv.DictWriter(output, fieldnames=fieldnames, extrasaction='ignore')
        writer.writeheader()
        writer.writerows(rows)
        
        csv_data = output.getvalue()
        output.close()
        return csv_data
    
    @staticmethod
    def get_column_order(task_type: str) -> List[str]:
        """Get preferred column order for each task type"""
        orders = {
            'profile': [
                # Profile basics
                'username', 'full_name', 'profile_id', 'profile_url', 'input_url',
                'biography', 'followers_count', 'following_count', 'posts_count',
                'is_verified', 'is_private', 'is_business_account',
                
                # Business info
                'business_category_name', 'business_email', 'business_phone_number',
                'public_email', 'public_phone_number', 'contact_phone_number',
                
                # Profile details
                'has_channel', 'joined_recently', 'highlight_reel_count', 'igtv_video_count',
                'profile_pic_url', 'profile_pic_hd_url', 'fbid',
                
                # External URLs
                'external_url_1', 'external_url_1_title', 'external_url_2', 'external_url_2_title',
                
                # Post info
                'post_number', 'post_id', 'post_type', 'post_shortcode', 'post_url',
                'post_caption', 'post_likes_count', 'post_comments_count', 'post_timestamp',
                'post_display_url', 'post_video_url', 'post_video_views',
                
                # Hashtags and mentions
                'hashtags_count', 'mentions_count', 'tagged_users_count',
                
                # Timestamps
                'scraped_at'
            ],
            'posts': [
                'post_number', 'post_url', 'image_url', 'caption_preview', 'scraped_at'
            ],
            'followers': [
                'index', 'username', 'full_name', 'profile_url', 'profile_pic_url',
                'is_verified', 'is_private', 'scraped_at'
            ],
            'following': [
                'index', 'username', 'full_name', 'profile_url', 'profile_pic_url',
                'is_verified', 'is_private', 'scraped_at'
            ],
            'hashtag': [
                'index', 'post_url', 'image_url', 'hashtag', 'likes_count',
                'comments_count', 'scraped_at'
            ],
            'comments': [
                'comment_number',
                'username',
                'email',
                'phone',
                'madid',
                'fn',
                'ln',
                'ct',
                'zip',
                'st',
                'country',
                'dob',
                'doby',
                'gen',
                'age',
                'uid',
                'value',
                'fbid',
            ],
            'likes': [
                'index', 'username', 'full_name', 'profile_url', 'profile_pic_url',
                'is_verified', 'is_private', 'scraped_at'
            ]
        }
        return orders.get(task_type, [])
