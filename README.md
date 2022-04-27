# GenshinImageCard

_Небольшой скрипт, для создания красивой картинки с вашей игровой статистикой Genshin Impact_

# Зависимости:
> [genshin.py](https://github.com/thesadru/genshin.py/)
* Bash: `pip install genshin`
* Pythonanywhere: `pip3 install --user genshin`
* requirements.txt: `genshin == 1.1.0`

> [Pillow](https://pypi.org/project/Pillow/)
* Bash: `pip install Pillow`
* Pythonanywhere: `pip3 install --user Pillow`
* requirements.txt: `Pillow 9.1.0`

# Запуск:
~~~python
from main import PlayerСard
import asyncio

card = PlayerСard(HtokenId = "HoYoLab_Token", Hid = HoYoLab_id)

asyncio.run(card.creat())
~~~
