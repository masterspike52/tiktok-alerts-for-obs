import requests
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.application import MIMEApplication

# TikTok API credentials
api_key = "YOUR_API_KEY"
api_secret = "YOUR_API_SECRET"

# TikTok user ID for the user you want to monitor
user_id = "USER_ID_TO_MONITOR"

# Email settings
sender_email = "YOUR_EMAIL@gmail.com"
sender_password = "YOUR_EMAIL_PASSWORD"
receiver_email = "RECEIVER_EMAIL@gmail.com"

# Initialize session for TikTok API requests
session = requests.Session()
session.headers.update({"Authorization": f"Bearer {api_key}.{api_secret}"})

# Get initial follower count
response = session.get(f"https://api.tiktok.com/v1.3/user/follower/list/?user_id={user_id}")
initial_followers = response.json()["follower_list"]

while True:
    # Check for new followers
    response = session.get(f"https://api.tiktok.com/v1.3/user/follower/list/?user_id={user_id}")
    current_followers = response.json()["follower_list"]
    
    new_followers = [follower for follower in current_followers if follower not in initial_followers]
    
    if new_followers:
        # Send an email alert if there are new followers
        subject = "New TikTok Followers Alert"
        body = f"You have {len(new_followers)} new followers on TikTok!\n\nNew followers: {', '.join(new_followers)}"
        
        # Create email message
        message = MIMEMultipart()
        message["From"] = sender_email
        message["To"] = receiver_email
        message["Subject"] = subject
        message.attach(MIMEText(body, "plain"))
        
        # Connect to the email server and send the email
        try:
            server = smtplib.SMTP("smtp.gmail.com", 587)
            server.starttls()
            server.login(sender_email, sender_password)
            server.sendmail(sender_email, receiver_email, message.as_string())
            server.quit()
            print("Email alert sent successfully.")
        except Exception as e:
            print(f"Error sending email: {str(e)}")
    
    # Update the initial followers list for the next iteration
    initial_followers = current_followers

    # Sleep for a while before checking again (e.g., every hour)
    import time
    time.sleep(3600)  # Sleep for 1 hour
