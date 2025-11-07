# config.py
import os

# توكن البوت من BotFather
# يفضّل في Pella تضيفينه كمتغير بيئة باسم BOT_TOKEN
TELEGRAM_TOKEN = os.getenv("BOT_TOKEN", "YOUR_BOT_TOKEN_HERE")

# رابط مصدر التحديات (نفس بيانات rdo-dailies.com تقريباً)
API_URL = "https://api.rdo.gg/challenges/index.json"

# زمن الكاش (ثواني) لتقليل عدد الطلبات على الـ API
CACHE_SECONDS = 600  # 10 دقائق تقريباً

# عناوين الأدوار بالعربي (تظهر في الرسائل)
ARABIC_ROLE_TITLES = {
    "general": "التحديات العامة",
    "bounty": "تحديات الباونتي هونتر",
    "trader": "تحديات التاجر",
    "collector": "تحديات الكولكتر",
    "moonshiner": "تحديات المونشاينر",
    "naturalist": "تحديات الطبيعة",
}

# كلمات مفتاحية بالعربي لرسائل الشات (بدون أوامر)
KEYWORDS_MAP = {
    "general": [
        "التحديات",
        "عرض التحديات العامة",
    ],
    "bounty": [
        "تحديات الباونتي",
        "تحديات الباونتي هونتر",
    ],
    "trader": [
        "تحديات التاجر",
    ],
    "collector": [
        "تحديات الكولكتر",
        "تحديات الكوليكتور",
    ],
    "moonshiner": [
        "تحديات المونشاينر",
        "تحديات المون شاينر",
    ],
    "naturalist": [
        "تحديات الطبيعة",
        "تحديات الناشرالست",
    ],
}# config.py
import os

# توكن البوت من BotFather
# يفضّل في Pella تضيفينه كمتغير بيئة باسم BOT_TOKEN
TELEGRAM_TOKEN = os.getenv("BOT_TOKEN", "YOUR_BOT_TOKEN_HERE")

# رابط مصدر التحديات (نفس بيانات rdo-dailies.com تقريباً)
API_URL = "https://api.rdo.gg/challenges/index.json"

# زمن الكاش (ثواني) لتقليل عدد الطلبات على الـ API
CACHE_SECONDS = 600  # 10 دقائق تقريباً

# عناوين الأدوار بالعربي (تظهر في الرسائل)
ARABIC_ROLE_TITLES = {
    "general": "التحديات العامة",
    "bounty": "تحديات الباونتي هونتر",
    "trader": "تحديات التاجر",
    "collector": "تحديات الكولكتر",
    "moonshiner": "تحديات المونشاينر",
    "naturalist": "تحديات الطبيعة",
}

# كلمات مفتاحية بالعربي لرسائل الشات (بدون أوامر)
KEYWORDS_MAP = {
    "general": [
        "التحديات",
        "عرض التحديات العامة",
    ],
    "bounty": [
        "تحديات الباونتي",
        "تحديات الباونتي هونتر",
    ],
    "trader": [
        "تحديات التاجر",
    ],
    "collector": [
        "تحديات الكولكتر",
        "تحديات الكوليكتور",
    ],
    "moonshiner": [
        "تحديات المونشاينر",
        "تحديات المون شاينر",
    ],
    "naturalist": [
        "تحديات الطبيعة",
        "تحديات الناشرالست",
    ],
}
