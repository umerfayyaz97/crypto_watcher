import pyautogui as auto
import get_value_fns
import subprocess
import time
from pyautogui import ImageNotFoundException
import io
import base64
from agents import Agent, Runner,  set_tracing_disabled, set_default_openai_client, set_default_openai_api
from openai import AsyncOpenAI
import asyncio
import os
from dotenv import load_dotenv
from instructions import SMA_STRATEGY_INSTRUCTIONS

load_dotenv()

set_tracing_disabled(True)

# --- To using Gemini API KEY Uncomment the following code inside *s

# ************************************************
# gemini_api_key = os.getenv('GEMINI_API_KEY')
# gemini_api_key = os.getenv('GEMINI_API_KEY')
# client = AsyncOpenAI(api_key=gemini_api_key,
#                      base_url="https://generativelanguage.googleapis.com/v1beta/openai/")
# set_default_openai_api("chat_completions")
# set_default_openai_client(client)
# agent = Agent(name="Crypto Technical Analyst", instructions=SMA_STRATEGY_INSTRUCTIONS, model='gemini-1.5-flash')
# **************************************************



# Uncomment the following line when using OPENAI_API_KEY
agent = Agent(name="Crypto Technical Analyst", instructions=SMA_STRATEGY_INSTRUCTIONS)

# ------------------------------------------------------------------------------------
# ------------------------------------------------------------------------------------

# auto.alert(text="Welcome to Crypto Watcher. \n Enter currency pair, enter desired exchange and enter desired timeframe \n The bot will watch the charts for you and notify when you can buy and sell" , title='Crypto Watcher' , button='Got it')     
        

def open_chart(url: str):
    "This function makes the URL, opens window, confirms the chart is opened and working"
    while True: 
        chrome_path = r"C:\Program Files\Google\Chrome\Application\chrome.exe"
        subprocess.Popen(chrome_path)

        time.sleep(1)

        auto.typewrite(url)
        auto.press('enter')
        time.sleep(10)

        try: 
            auto.locateOnScreen("invalid_symbol.png")
            print(f"Chart not available, try changind Exchange or symbol. Most probably changing exchange solves the issue \n")
            auto.hotkey('alt','f4')
            # auto.alert(text="Chart Not Available, try changing Exchange or time", title="Invalid Symbol", button="Got it")
            return False
        
        except ImageNotFoundException:
            print("✅ Chart opened successfully!")
            return True
                
            
def take_screenshots_as_base64():
    """Captures a screenshot, converts it to bytes in memory, and then to a Base64 string.
    This Base64 string is ready to be sent directly to an LLM API.
    Does not save any file to the computer.
    Returns:
        A Base64-encoded string of the screenshot, or None if an error occurs
    """
    print("Capturing screenshot...")
    
    try:
        chart_photo=auto.screenshot()
        img_byte_arr = io.BytesIO()
        chart_photo.save(img_byte_arr, format='PNG')
        img_bytes = img_byte_arr.getvalue()

        base64_encoded_string = base64.b64encode(img_bytes).decode('utf-8')
        return base64_encoded_string
        
    
    except Exception as e:
        print(f"An error occured while taking Screenshot: {e}")
        return None


# Using Gemini Direct LLM call via API

# async def main():
#     """Main function to Run crypto Watcher Bot"""

#     # This loop will continue until a valid chart is successfully opened.
#     while True:
#         # Get fresh user input in each iteration of this loop
#         user_interval_minutes = get_value_fns.schedule_interval_check()
#         user_exchange = get_value_fns.exchange_name()
#         user_pair = get_value_fns.currency_pair()
#         print("--- Opening chart! --- \n")

#         # Build the URL using the new inputs
#         chart_url = get_value_fns.construct_url(user_exchange, user_pair, user_interval_minutes)
#         screenshot_delay_seconds = get_value_fns.screenshot_interval(user_interval_minutes)

#         # Try to open the chart
#         if open_chart(chart_url):
#             # If successful, print a confirmation and break the setup loop
#             print(f"\n🚀 Chart confirmed. ")
#             break
#         else:
            
#             print("--- Please re-enter chart details. ---\n")
        
#     print(f"\n🚀 Starting Crypto Watcher Loop. Checking every {screenshot_delay_seconds} seconds.")
#     while True:
#         base64_image = take_screenshots_as_base64()

#         if base64_image:
#             query = query = {
#                             "prompt": "Analyze this chart screenshot based on my instructions.",
#                             "image": base64_image
#                                 }
            
#             print(f"[{time.strftime('%H:%M:%S')}] 🤖 Agent is analyzing the screenshot...")

#             try:
#                 response = await client.chat.completions.create(
#                     model='gemini-1.5-flash',
#                     messages=[
#                         {
#                             "role": "system",
#                             "content": sma_strategy_instructions
#                         },
#                         {
#                             "role": "user",
#                             "content": [
#                                 {"type": "text", "text": "Analyze this chart screenshot based on my instructions."},
#                                 {"type": "image_url", "image_url": {"url": f"data:image/png;base64,{base64_image}"}}
#                             ]
#                         }
#                     ]
#                 )
#                 analysis_result = response.choices[0].message.content
#                 print("\n--- Analysis Result ---")
#                 print(analysis_result)
#                 print("-----------------------\n")

#             except Exception as e:
#                 print(f"An error occurred during API call: {e}")
                    
            # print(f"Waiting for {screenshot_delay_seconds} seconds before next check...")
            # for i in range(screenshot_delay_seconds, 0, -1):
            #     print(f"   Next check in: {i:2d} seconds... ", end="\r")
            #     time.sleep(1) 


# Using OPENAI Agents SDK for Analysis
async def main():
    """Main function to Run crypto Watcher Bot"""
    while True:
        user_interval_minutes = get_value_fns.schedule_interval_check()
        user_exchange = get_value_fns.exchange_name()
        user_pair = get_value_fns.currency_pair()
        print("--- Opening chart! --- \n")

        chart_url = get_value_fns.construct_url(user_exchange, user_pair, user_interval_minutes)
        screenshot_delay_seconds = get_value_fns.screenshot_interval(user_interval_minutes)

        if open_chart(chart_url):
            print(f"\n🚀 Chart confirmed.")
            break
        else:
            print("--- Please re-enter chart details. ---\n")

    print(f"\n🚀 Starting Crypto Watcher Loop. Checking every {screenshot_delay_seconds} seconds.")
    while True:
        base64_image = take_screenshots_as_base64()

        if base64_image:
         
            messages_payload = [
                {
                    "role": "user",
                    "content": [
                        {
                            "type": "input_image",
                            "detail": "auto",  
                            "image_url": f"data:image/png;base64,{base64_image}"
                        }
                    ]
                },
                {
                    "role": "user",
                    "content": "Analyze this chart screenshot based on my instructions."
                }
            ]
            
            print(f"[{time.strftime('%H:%M:%S')}] 🤖 Agent is analyzing the screenshot...")
            
          
            try:
                result = await Runner.run(agent, messages_payload) 
                print("\n--- Analysis Result ---")
                print(result.final_output) 
                print("-----------------------\n")
            except Exception as e:
                print(f"An error occurred during agent analysis: {e}")
          
            print(f"Waiting for {screenshot_delay_seconds} seconds before next check...")
            for i in range(screenshot_delay_seconds, 0, -1):
                print(f"   Next check in: {i:2d} seconds... ", end="\r")
                time.sleep(1)     



if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\nWatcher stopped by user. Goodbye! 👋")
    

    



