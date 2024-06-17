import asyncio
import aiohttp
import logging
import time
from config import Config

logging.basicConfig(level=logging.INFO)

TOKEN = Config().get_fb_token()
PIXEL_ID = 1143904666755716


async def send_facebook_event(event_name: str, user_id: int):
    url = f'https://graph.facebook.com/v15.0/{PIXEL_ID}/events'
    payload = {
        'data': [
            {
                'event_name': event_name,
                'event_time': int(time.time()),
                'user_data': {
                    'external_id': str(user_id)
                }
            }
        ],
        'access_token': TOKEN
    }
    async with aiohttp.ClientSession() as session:
        async with session.post(url, json=payload) as response:
            if response.status == 200:
                logging.info('Event sent to Facebook Pixel successfully')
            else:
                logging.error('Failed to send event to Facebook Pixel',
                              response.json())

if __name__ == "__main__":
    asyncio.run(send_facebook_event("Subscribe", 123123123))
