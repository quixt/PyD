import user
class Message:
    def __init__(self, data, edit_url, session, headers):
        self._session = session
        self._change_urls = edit_url
        self.headers = headers

        self.set_attrs(data)
    def set_attrs(self, data):
        self.content = data['content']
        self.id = data['id']
        self.channel_id = data['channel_id']
        self.embeds = data['embeds']
        self.attachments = data['attachments']
        self.mentions = data['mentions']
        self.is_pinned = data['pinned']
        self.author = user.User(data['author'])
        self.tts = data['tts']
    async def edit(self, content):
        json = {'content':content}
        d = await self._session.patch(self._change_urls,json=json, headers=self.headers)
        mjson = await d.json()

        self.set_attrs(mjson)

    async def delete(self):
        await self._session.delete(self._change_urls, headers=self.headers)

