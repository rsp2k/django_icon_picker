# take_screenshots.py
import os
import sys
from playwright.sync_api import sync_playwright

# Define the base URL for your running Django project
BASE_URL = os.environ.get('BASE_URL', 'http://127.0.0.1:8000')

# List of URLs to screenshot (relative to BASE_URL)
URLS_TO_SCREENSHOT = [
    '/',  # Root URL (might show a 404 or redirect, but useful for testing)
    '/admin/',  # Django admin login page
    '/admin/example/',  # Example app admin
    '/admin/example/examplemodel/',  # Example model admin list
    '/icon_picker/download-svg/',  # Icon picker endpoint (might be a POST-only endpoint)
]

OUTPUT_DIR = 'screenshots'

def login_to_admin_if_needed(page, username, password):
    """
    Logs into the Django admin if credentials are provided.
    """
    if username and password:
        print("Attempting to log into Django admin...")
        try:
            page.goto(f"{BASE_URL}/admin/login/")
            
            # Wait for login form to be visible
            page.wait_for_selector('input[name="username"]', timeout=10000)
            
            page.fill('input[name="username"]', username)
            page.fill('input[name="password"]', password)
            page.click('input[type="submit"]')

            # Wait for successful login - look for admin index page elements
            try:
                page.wait_for_selector('h1:has-text("Django administration")', timeout=10000)
                print("Admin login successful!")
                return True
            except:
                # If we don't see the admin header, check if we're still on login page
                if 'login' in page.url:
                    print("Login failed - still on login page")
                    return False
                else:
                    print("Login appears successful (redirected away from login)")
                    return True
                    
        except Exception as e:
            print(f"Admin login failed: {e}")
            return False
    return False

def take_screenshot_with_retry(page, url_path, filename, retries=2):
    """
    Take a screenshot with retry logic for better reliability.
    """
    full_url = f"{BASE_URL}{url_path}"
    
    for attempt in range(retries + 1):
        try:
            print(f"Navigating to {full_url} (attempt {attempt + 1})...")
            
            # Navigate to the URL with a longer timeout
            page.goto(full_url, wait_until='domcontentloaded', timeout=30000)
            
            # Wait a bit for any dynamic content to load
            page.wait_for_timeout(2000)
            
            # Take the screenshot
            page.screenshot(path=filename, full_page=True)
            print(f"Screenshot saved: {filename}")
            return True
            
        except Exception as e:
            print(f"Attempt {attempt + 1} failed for {full_url}: {e}")
            if attempt < retries:
                print("Retrying...")
                page.wait_for_timeout(1000)  # Wait before retry
            else:
                print(f"Failed to screenshot {full_url} after {retries + 1} attempts")
                
                # Take a screenshot of whatever page we're on for debugging
                try:
                    debug_filename = filename.replace('.png', '_error.png')
                    page.screenshot(path=debug_filename)
                    print(f"Error screenshot saved: {debug_filename}")
                except:
                    pass
                    
    return False

def main():
    if not os.path.exists(OUTPUT_DIR):
        os.makedirs(OUTPUT_DIR)

    # Get credentials from environment variables
    DJANGO_SUPERUSER_USERNAME = os.environ.get('DJANGO_SUPERUSER_USERNAME')
    DJANGO_SUPERUSER_PASSWORD = os.environ.get('DJANGO_SUPERUSER_PASSWORD')

    with sync_playwright() as p:
        # Launch browser
        browser = p.chromium.launch(
            args=['--no-sandbox', '--disable-dev-shm-usage']  # Useful for CI environments
        )
        
        # Create a new page with a larger viewport for better screenshots
        page = browser.new_page(viewport={'width': 1920, 'height': 1080})
        
        # Perform admin login if credentials are provided
        admin_logged_in = login_to_admin_if_needed(page, DJANGO_SUPERUSER_USERNAME, DJANGO_SUPERUSER_PASSWORD)

        screenshot_results = []
        
        for url_path in URLS_TO_SCREENSHOT:
            # Create a safe filename from the URL path
            safe_filename = url_path.replace('/', '_').strip('_') or 'root'
            filename = os.path.join(OUTPUT_DIR, f"{safe_filename}.png")
            
            # Skip admin pages if we couldn't log in
            if '/admin/' in url_path and url_path != '/admin/' and not admin_logged_in:
                print(f"Skipping {url_path} - admin login required but not available")
                continue
            
            success = take_screenshot_with_retry(page, url_path, filename)
            screenshot_results.append({
                'url': url_path,
                'filename': filename,
                'success': success
            })

        browser.close()
        
        # Print summary
        print("\n" + "="*50)
        print("SCREENSHOT SUMMARY")
        print("="*50)
        successful = sum(1 for r in screenshot_results if r['success'])
        total = len(screenshot_results)
        print(f"Successfully captured: {successful}/{total} screenshots")
        
        for result in screenshot_results:
            status = "✓" if result['success'] else "✗"
            print(f"{status} {result['url']} -> {result['filename']}")
        
        if successful == 0:
            print("\nWARNING: No screenshots were captured successfully!")
            sys.exit(1)
        elif successful < total:
            print(f"\nWARNING: {total - successful} screenshots failed")
        else:
            print(f"\n🎉 All screenshots captured successfully!")

if __name__ == '__main__':
    main()
