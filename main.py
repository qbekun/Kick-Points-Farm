import asyncio,json,traceback

from _websockets.ws_connect import KickWebSocket
from kick_api import KickAPI
from loguru import logger

config = json.load(open("config.json", "r", encoding="utf-8"))

async def main():
    tasks = [asyncio.create_task(handle_streamer(streamer)) for streamer in config['Streamers']]
    await asyncio.gather(*tasks)

async def send_chat_periodically(streamer_name, chatroom_id, message, interval_minutes):
    await asyncio.sleep(interval_minutes * 60)
    
    while True:
        try:
            api = KickAPI(config['Private']['token'])
            api.send_message(chatroom_id, message)
            logger.info(f"[CHAT] '{message}' sent to {streamer_name}")
            await asyncio.sleep(interval_minutes * 60)
        except asyncio.CancelledError:
            break
        except Exception as e:
            logger.error(f"Failed to send message: {e}")
            await asyncio.sleep(interval_minutes * 60)

async def check_points_periodically(streamer_name):
    while True:
        try:
            await asyncio.sleep(60)
            api = KickAPI(config['Private']['token'])
            amount = api.get_points(streamer_name)
            logger.info(f"[POINTS] {streamer_name}: {amount}")
        except asyncio.CancelledError:
            break
        except:
            traceback.print_exc()

async def handle_streamer(streamer_config):
    streamer_name = streamer_config['name']
    logger.info(f"[START] Connecting to {streamer_name}...")

    try:
        api = KickAPI(config['Private']['token'])
        
        token = api.get_ws_token()
        if not token:
            logger.error(f"Failed to get WebSocket token for {streamer_name}")
            return

        stream_id = api.get_stream_id(streamer_name)
        channel_id = api.get_channel_id(streamer_name)
        chatroom_id = api.get_chatroom_id(streamer_name)

        if not stream_id or not channel_id or not chatroom_id:
            logger.error(f"Failed to get IDs for {streamer_name}")
            return

        logger.info(f"[INFO] Channel: {channel_id} | Chatroom: {chatroom_id}")

        chat_message = streamer_config.get('chat_message', '[emote:37226:KEKW]')
        chat_interval = streamer_config.get('chat_interval_minutes', 30)

        kick_websocket_client = KickWebSocket(
            data={
                "token": token,
                "streamId": stream_id,
                "channelId": channel_id,
                "auth_token": config['Private']['token']
            },
            chat_message=chat_message,
            chat_interval_minutes=chat_interval
        )

        websocket_task = asyncio.create_task(kick_websocket_client.connect())
        points_task = asyncio.create_task(check_points_periodically(streamer_name))
        chat_task = asyncio.create_task(send_chat_periodically(streamer_name, chatroom_id, chat_message, chat_interval))

        try:
            await asyncio.gather(websocket_task, points_task, chat_task, return_exceptions=True)
        except KeyboardInterrupt:
            logger.info("Shutting down...")
            websocket_task.cancel()
            points_task.cancel()
            chat_task.cancel()
            await kick_websocket_client.disconnect()
    except:
        traceback.print_exc()

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        logger.info("[STOP] Bot stopped by user")
        pass