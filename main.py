import tls_client, json, base64

class MFA:
    def __init__(self):
        self.session = tls_client.Session(client_identifier="chrome_128")
        with open("config.json", "r") as config:
            self.data = json.load(config)
            self.vanity_code = self.data["vanity-code"]
            self.password = self.data["password"]
            self.token = self.data["token"]
            self.guild_id = self.data["guild-id"]

        self.super_properties = "eyJvcyI6Ik1hYyBPUyBYIiwiYnJvd3NlciI6IkRpc2NvcmQgQ2xpZW50IiwicmVsZWFzZV9jaGFubmVsIjoic3RhYmxlIiwiY2xpZW50X3ZlcnNpb24iOiIwLjAuMzMwIiwib3NfdmVyc2lvbiI6IjIzLjAuMCIsIm9zX2FyY2giOiJhcm02NCIsImFwcF9hcmNoIjoiYXJtNjQiLCJzeXN0ZW1fbG9jYWxlIjoiZW4tVVMiLCJoYXNfY2xpZW50X21vZHMiOmZhbHNlLCJicm93c2VyX3VzZXJfYWdlbnQiOiJNb3ppbGxhLzUuMCAoTWFjaW50b3NoOyBJbnRlbCBNYWMgT1MgWCAxMF8xNV83KSBBcHBsZVdlYktpdC81MzcuMzYgKEtIVE1MLCBsaWtlIEdlY2tvKSBkaXNjb3JkLzAuMC4zMzAgQ2hyb21lLzEyOC4wLjY2MTMuMTg2IEVsZWN0cm9uLzMyLjIuNyBTYWZhcmkvNTM3LjM2IiwiYnJvd3Nlcl92ZXJzaW9uIjoiMzIuMi43Iiwib3Nfc2RrX3ZlcnNpb24iOiIyMyIsImNsaWVudF9idWlsZF9udW1iZXIiOjM1NTYyNCwibmF0aXZlX2J1aWxkX251bWJlciI6bnVsbCwiY2xpZW50X2V2ZW50X3NvdXJjZSI6bnVsbH0="
    
        self.ticket = self.get_mfa_ticket()
        print(f"Ticket: {self.ticket}")
        self.mfa_auth = self.get_vanity_token()
        print(f"Vanity Token response: {self.mfa_auth}")

    def get_mfa_ticket(self):
        return self.session.patch(
            f"https://discord.com/api/v9/guilds/{self.guild_id}/vanity-url",
            headers={
                "Authorization": self.token,
                "x-super-properties": self.super_properties,
            },
            json={"code": self.vanity_code},
        ).json()["mfa"]["ticket"]

    def get_vanity_token(self):
        return self.session.post(
            "https://discord.com/api/v9/mfa/finish",
            headers={
                "Authorization": self.token,
                "x-super-properties": self.super_properties,
            },
            json={"data": self.password, "mfa_type": "password", "ticket": self.ticket},
        ).json()["token"]
        
    def set_vanity(self): # wont be called unless user wants to change vanity
        return self.session.patch(f"https://discord.com/api/v9/guilds/{self.guild_id}/vanity-url", headers={
            "Authorization": self.token,
            "x-super-properties": self.super_properties,
            "x-discord-mfa-authorization": self.mfa_auth,
            "Cookie": f"__Secure-recent_mfa={self.mfa_auth};",
            "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) discord/0.0.330 Chrome/128.0.6613.186 Electron/32.2.7 Safari/537.36"
        }, json={"code": self.vanity_code}).json()


init = MFA()
