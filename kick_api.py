from curl_cffi import requests
import time

class KickAPI:
    def __init__(self, token: str):
        self.token = token
        self.session = requests.Session(impersonate="chrome120")
        self.session.headers = {
            "accept": "application/json",
            "accept-language": "en-US,en;q=0.9,pl;q=0.8",
            "authorization": f"Bearer {token}",
            "cache-control": "max-age=0",
            "origin": "https://kick.com",
            "referer": "https://kick.com/",
            "x-app-platform": "web",
            "x-client-token": "e1393935a959b4020a4491574f6490129f678acdaa92760471263db43487f823",
        }
    
    def get_ws_token(self) -> str:
        response = self.session.get("https://websockets.kick.com/viewer/v1/token")
        if response.status_code != 200:
            raise Exception(f"Failed to retrieve WebSocket token: {response.text}")
        
        data = response.json()
        if 'data' not in data or 'token' not in data['data']:
            raise Exception(f"Invalid response format: {data}")
        
        return data['data']['token']
    
    def get_stream_id(self, username: str) -> int:
        response = self.session.get(f"https://kick.com/api/v2/channels/{username}/videos")
        if response.status_code != 200:
            raise Exception(f"Failed to retrieve stream ID for {username}: {response.text}")
        
        data = response.json()
        live_stream = next((stream for stream in data if stream['is_live'] == True), None)
        return live_stream['id'] if live_stream else None
    
    def get_channel_id(self, username: str) -> int:
        response = self.session.get(f"https://kick.com/api/v2/channels/{username}/videos")
        if response.status_code != 200:
            raise Exception(f"Failed to retrieve channel ID for {username}: {response.text}")
        
        return response.json()[0]['channel_id']
    
    def get_chatroom_id(self, username: str) -> int:
        response = self.session.get(f"https://kick.com/api/v2/channels/{username}")
        if response.status_code != 200:
            raise Exception(f"Failed to retrieve chatroom ID for {username}: {response.text}")
        
        return response.json()['chatroom']['id']
    
    def get_points(self, username: str) -> int:
        response = self.session.get(f"https://kick.com/api/v2/channels/{username}/points")
        if response.status_code != 200:
            raise Exception(f"Failed to retrieve points for {username}: {response.text}")
        
        return response.json()['data']['points']
    
    def send_message(self, chatroom_id: int, content: str) -> bool:
        message_ref = str(int(time.time() * 1000))
        payload = {
            "content": content,
            "type": "message",
            "message_ref": message_ref
        }
        
        self.session.headers["content-type"] = "application/json"
        response = self.session.post(f"https://kick.com/api/v2/messages/send/{chatroom_id}", json=payload)
        
        if response.status_code == 200:
            return True
        else:
            raise Exception(f"Failed to send message: {response.status_code} - {response.text}")
