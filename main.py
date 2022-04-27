from PIL import Image, ImageDraw, ImageFont
from io import BytesIO

import vk_api
import requests

import asyncio
import genshin

vk = vk_api.VkApi(token = "fb1a8225db7222b4e52ea4dbab8fc4b5b05163122069832ea2c8e6b8640c59b818ae0e6a8e51673c6cefa")

vkpril = vk_api.VkApi(token = "5e380fc25e380fc25e380fc2675e444fd555e385e380fc23c67269f3cb20e68698358ef")


slot_size = (267,267)

bg = Image.open('card/cart.png')
z_bg = Image.open('card/cart.png')
font_stats = ImageFont.truetype("card/Genshin_Impact.ttf", 57)
font_name = ImageFont.truetype("card/Genshin_Impact.ttf", 34)
font_name_text = ImageFont.truetype("card/Genshin_Impact.ttf", 24)

ava = Image.open('card/ava.png')
ava.thumbnail(slot_size)

async def up_img(img):
    bytes = BytesIO()

    img.save(bytes, format='png')

    url = vk.method('photos.getMessagesUploadServer')['upload_url']
    response = vk.http.post(url, files = [('file', ('file.png', bytes.getvalue()))])
    response = vk.method('photos.saveMessagesPhoto', response.json())

    return 'photo{}_{}'.format(response[0]['owner_id'], response[0]['id'])


async def get_client(Hid,HtokenId):
    try:
        cookies = {"ltuid": Hid, "ltoken": HtokenId}
        client = genshin.Client(cookies)
        data = await client.get_record_card(Hid)
        return data.uid, data.level, data.nickname,data.server_name
    except:
        return None,None,None,None
class PlayerСard(object):
    def __init__(self, HtokenId:str = '', Hid:int = 0):
        super(PlayerСard, self).__init__()
        if HtokenId != '' and Hid != 0:
            self.HtokenId = HtokenId
            self.Hid = Hid
            self.uid, self.level, self.nickname, self.server_name = asyncio.run(get_client(Hid,HtokenId))
            self.cookies = {"ltuid": Hid, "ltoken": HtokenId}
        else:
            return False
    async def get_name_vk(self,from_id:int = 0):
        info = vkpril.method('users.get', {'user_ids': from_id})[0]
        
        return f"{info['first_name']} {info['last_name']}"

    async def get_photo(self,from_id:int = 0):
        if from_id != 0:
            url = vkpril.method('users.get', {'user_ids': from_id, 'fields': 'photo_max_orig'})[0]['photo_max_orig']
            if url != 'https://vk.com/images/camera_200.png':
                img = Image.open(BytesIO(requests.get(url).content))
                img.thumbnail(slot_size)
                return img
        return ava
    
    async def get_genshinStats(self, fuid:int = 0):
        uid = self.uid
        level = self.level
        nickname = self.nickname
        server_name = self.server_name
        client = genshin.Client(self.cookies)
        if uid != 0:
            client = genshin.Client(self.cookies)
            record = await client.get_record_card(fuid) #Имя игрока
            try:
                uid = record.uid
                level = record.level
                nickname = record.nickname
                server_name = record.server_name
            except:
                return False,False,False,False,False,False,False,False,False,False,False,False,False,False,False

        data = await client.get_genshin_user(uid) #Получаем игровую статистику
        achievements = data.stats.achievements #Достижения
        days_active = data.stats.days_active #Актив день
        characters = data.stats.characters #Персонажей
        spiral_abyss = data.stats.spiral_abyss #Бездна
        anemoculi = data.stats.anemoculi #Анемокулы
        geoculi = data.stats.geoculi #Геокулы
        electroculi = data.stats.electroculi #Электрокулы
        common_chests = data.stats.common_chests #Обычный сундук
        exquisite_chests = data.stats.exquisite_chests #Большой сундук
        precious_chests = data.stats.precious_chests #Драгоценный сундук
        luxurious_chests = data.stats.luxurious_chests #Роскошный сундук
        remarkable_chests = data.stats.remarkable_chests #Удивительный сундук
        unlocked_waypoints = data.stats.unlocked_waypoints #Телепорты
        unlocked_domains = data.stats.unlocked_domains #Подземелья
        return achievements, days_active, characters,spiral_abyss,anemoculi,geoculi,electroculi,common_chests,exquisite_chests,precious_chests,luxurious_chests,remarkable_chests,unlocked_waypoints,unlocked_domains, uid,level,nickname, server_name


    async def creat(self, from_id: int = 0, frend_hid: int = 0):
        achievements, days_active, characters,spiral_abyss,anemoculi,geoculi,electroculi,common_chests,exquisite_chests,precious_chests,luxurious_chests,remarkable_chests,unlocked_waypoints,unlocked_domains, uid,level,nickname,server_name = await self.get_genshinStats(fuid = frend_hid)
        avatar = await self.get_photo(from_id)
        if from_id != 0:
            name_vk = await self.get_name_vk(from_id)
            vk_id = f"vk.com/id{from_id}"
        else:
            name_vk = "Genshin Imapct Bot"
            vk_id = "vk.com/bot.genshin"

        # Avatar Add
        img = bg.copy()
        img.paste(avatar, (59,153))
        img.paste(z_bg, (0,0),z_bg)

        # Name Banner Add
        text = ImageDraw.Draw(img)
        text.text((354,226), f"{nickname} | {level} Lvl", font=font_name, fill=(255,255,255,255))

        text.text((354,273), f"{server_name.replace('Server', '')} | UID: {uid}", font=font_name_text, fill=(255,255,255,255))
        text.text((354,307), name_vk, font=font_name_text, fill=(255,255,255,255))
        text.text((354,336), vk_id, font=font_name_text, fill=(255,255,255,255))


        # Name Stats Add
        #1
        text.text((150,497), str(days_active), font=font_stats, fill=(255,255,255,255))
        text.text((405,497), str(achievements), font=font_stats, fill=(255,255,255,255))
        text.text((649,497), str(characters), font=font_stats, fill=(255,255,255,255))

        #2
        text.text((160,688), str(anemoculi), font=font_stats, fill=(255,255,255,255))
        text.text((405,688), str(geoculi), font=font_stats, fill=(255,255,255,255))
        text.text((649,688), str(electroculi), font=font_stats, fill=(255,255,255,255))

        #3
        text.text((160,882), str(unlocked_waypoints), font=font_stats, fill=(255,255,255,255))
        text.text((405,882), str(unlocked_domains), font=font_stats, fill=(255,255,255,255))
        text.text((649,882), str(spiral_abyss), font=font_stats, fill=(255,255,255,255))

        #4
        text.text((160,1066), str(common_chests), font=font_stats, fill=(255,255,255,255))
        text.text((405,1066), str(exquisite_chests), font=font_stats, fill=(255,255,255,255))
        text.text((649,1066), str(precious_chests), font=font_stats, fill=(255,255,255,255))

        #5
        text.text((160,1242), str(luxurious_chests), font=font_stats, fill=(255,255,255,255))


        return await up_img(img)