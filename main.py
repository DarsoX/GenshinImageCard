from PIL import Image, ImageDraw, ImageFont

import collections
import asyncio
import genshin

slot_size = (267,267)

bg = Image.open('img/cart.png')
z_bg = Image.open('img/cart.png')
font_stats = ImageFont.truetype("font/Genshin_Impact.ttf", 57)
font_name = ImageFont.truetype("font/Genshin_Impact.ttf", 34)
font_name_text = ImageFont.truetype("font/Genshin_Impact.ttf", 24)

avatar = Image.open('img/ava.png')
avatar.thumbnail(slot_size)


all_genstat = [
    'uid',
    'level',
    'nickname',
    'server_name',
    'achievements',
    'days_active',
    'characters',
    'spiral_abyss',
    'anemoculi',
    'geoculi',
    'electroculi',
    'common_chests',
    'exquisite_chests',
    'precious_chests',
    'luxurious_chests',
    'remarkable_chests',
    'unlocked_waypoints',
    'unlocked_domains'
    ]

async def up_img(img):
    img.save("Card.png")
    print('save')

async def get_client(Hid,HtokenId):
    try:
        cookies = {"ltuid": Hid, "ltoken": HtokenId}
        client = genshin.Client(cookies)
        data = await client.get_record_card(Hid)
        
        info: dict[str, int] = collections.namedtuple('GenStats', ['uid','level','nickname','server_name'])
        GenStats = info(data.uid, data.level, data.nickname,data.server_name)
        
        return GenStats
    except:
        return False
    
class PlayerСard(object):
    def __init__(self, HtokenId:str = '', Hid:int = 0):
        super(PlayerСard, self).__init__()
        if HtokenId != '' and Hid != 0:
            self.HtokenId = HtokenId
            self.Hid = Hid
            GenStats = asyncio.run(get_client(Hid,HtokenId))
            if not GenStats:
                return False
            self.uid = GenStats.uid, 
            self.level = GenStats.level
            self.nickname = GenStats.nickname
            self.server_name = GenStats.server_name
            self.cookies = {"ltuid": Hid, "ltoken": HtokenId}
        else:
            return False
    
    async def get_genshinStats(self, fuid:int = 0):
        uid = self.uid
        level = self.level
        nickname = self.nickname
        server_name = self.server_name
        client = genshin.Client(self.cookies)
        if uid != 0:
            client = genshin.Client(self.cookies)
            record = await client.get_record_card(fuid) 
            info: dict[str, int] = collections.namedtuple('GenStats', all_genstat)
            try:
                data = await client.get_genshin_user(record.uid)
                GenStats = info(record.uid, record.level, record.nickname,record.server_name,data.stats.achievements,data.stats.days_active,data.stats.characters,data.stats.spiral_abyss,data.stats.anemoculi,data.stats.geoculi,data.stats.electroculi,data.stats.common_chests,data.stats.exquisite_chests,data.stats.precious_chests,data.stats.luxurious_chests,data.stats.remarkable_chests,data.stats.unlocked_waypoints,data.stats.unlocked_domains)
            except:
                return False
        return GenStats


    async def creat(self, frend_hid: int = 0):
        GenStats = await self.get_genshinStats(fuid = frend_hid)
        if not GenStats:
            return False
        # Avatar Add
        img = bg.copy()
        img.paste(avatar, (59,153))
        img.paste(z_bg, (0,0),z_bg)

        # Name Banner Add
        text = ImageDraw.Draw(img)
        text.text((354,226), f"{GenStats.nickname} | {GenStats.level} Lvl", font=font_name, fill=(255,255,255,255))

        text.text((354,273), f"{GenStats.server_name.replace('Server', '')} | UID: {GenStats.uid}", font=font_name_text, fill=(255,255,255,255))

        # Name Stats Add
        #1
        text.text((150,497), str(GenStats.days_active), font=font_stats, fill=(255,255,255,255))
        text.text((405,497), str(GenStats.achievements), font=font_stats, fill=(255,255,255,255))
        text.text((649,497), str(GenStats.characters), font=font_stats, fill=(255,255,255,255))

        #2
        text.text((160,688), str(GenStats.anemoculi), font=font_stats, fill=(255,255,255,255))
        text.text((405,688), str(GenStats.geoculi), font=font_stats, fill=(255,255,255,255))
        text.text((649,688), str(GenStats.electroculi), font=font_stats, fill=(255,255,255,255))

        #3
        text.text((160,882), str(GenStats.unlocked_waypoints), font=font_stats, fill=(255,255,255,255))
        text.text((405,882), str(GenStats.unlocked_domains), font=font_stats, fill=(255,255,255,255))
        text.text((649,882), str(GenStats.spiral_abyss), font=font_stats, fill=(255,255,255,255))

        #4
        text.text((160,1066), str(GenStats.common_chests), font=font_stats, fill=(255,255,255,255))
        text.text((405,1066), str(GenStats.exquisite_chests), font=font_stats, fill=(255,255,255,255))
        text.text((649,1066), str(GenStats.precious_chests), font=font_stats, fill=(255,255,255,255))

        #5
        text.text((160,1242), str(GenStats.luxurious_chests), font=font_stats, fill=(255,255,255,255))

        await up_img(img)
