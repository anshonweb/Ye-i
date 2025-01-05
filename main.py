import asyncpraw
import praw
from dotenv import load_dotenv
import os
import time
import random
import google.generativeai as genai
import requests
import json




load_dotenv()
genai.configure(api_key=os.getenv('gemini'))
reddit = praw.Reddit(

    client_secret=os.getenv('client_secret'),
    client_id=os.getenv('client_id'),
    user_agent = 'yebot',
    username=os.getenv('username'),
    password = os.getenv('password'),
    requestor_kwargs={'timeout': 10})



try:
    print(f"Logged in as: {reddit.user.me()}")
except Exception as e:
    print(f'Failed to log in: {e}')

def generate_response(comment):

  

    url = "https://api.kanye.rest/"
    response = requests.get(url)
    tweet = response.json().get('quote')
    prompt = f"""
    You are a bot on the subreddit "goodasssub". Your task is to reply to the given comment with the following tweet:{tweet}. You can modify the tweet (make it very few words (3-4)/, remove one-two words only,
    add emoji) or leave it untouched with respect to the context of the comment. You dont have to do anything extra except this.
    The Comment is:"{comment}"
    """

    model = genai.GenerativeModel('gemini-1.5-flash-8b')
    try:
        response =model.generate_content(prompt)
        return response.text
    except Exception as e:
        print(f"Error generating reply: {e}")
        return None
    



def reply_to_comments():
    subreddit = reddit.subreddit('goodasssub')
    for submission in subreddit.new(limit=3): 
        submission.comments.replace_more(limit=0)  
        comments = [comment for comment in submission.comments if isinstance(comment, praw.models.Comment)]

        
        if comments:
           
            comment_to_reply = random.choice(comments)

            if random.random() < 0.3:  
                reply_text = generate_response(comment_to_reply.body)
                
                
                comment_to_reply.reply(reply_text)
                print(f"Replied to comment: {comment_to_reply.body}")

            else:
                print(f"Skipping comment: {comment_to_reply.body}")

if __name__ == "__main__":
    while True:
        try:
            reply_to_comments()  
        except Exception as e:
            print(f"Error: {e}")
        time.sleep(180) 
