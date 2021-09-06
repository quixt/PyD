import user, message
class ApplicationCommand:
    def __init__(self,data):
        self.id:int = data['id']
        self.bot_id:int = data['application_id']
        self.name:str  = data['name']
        self.description:str = data['description']
        self.type = 1

class Context:
    def __init__(self, member_class:user.Member, token, iid, session, headers, aid):
        self.Member = member_class
        self._interaction_token =  token
        self._interaction_id = iid
        self.finished = False
        self.session = session
        self.headers = headers
        self._applicaton_id = aid
        self._messages_url = f'https://discord.com/api/v8/webhooks/{self._applicaton_id}/{self._interaction_token}'
        self._bi_url = f'https://discord.com/api/v8/interactions/{self._interaction_id}/{self._interaction_token}/callback'
   
    async def wait(self):
        self.finished = True 
        d = await self.session.post(self._bi_url, json={'type':5},headers = self.headers)
    async def send(self, content):
        if self.finished:
            json = {
                
                "content": f"{content}"
                
            }
            d = await self.session.post(self._messages_url,json=json,headers=self.headers)
            d = await d.json()
            m = message.Message(d,f'{self._messages_url}/messages/{d["id"]}', self.session, self.headers)
            return m        
        else:
            json = {
                "type": 4,
                "data": {
                    "content": f"{content}"
                }
            }
            self.finished = True
            d = await self.session.post(self._bi_url, json = json, headers = self.headers)
    async def edit(self,content):
        url = f'{self._messages_url}/messages/@original'
        await self.session.patch(url = url, json={'content':content},headers=self.headers)
    async def delete(self):
        url = f'{self._messages_url}/messages/@original'
        await self.session.delete(url = url,headers=self.headers)

        