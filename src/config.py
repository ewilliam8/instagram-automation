import os
from dotenv import load_dotenv

PROGRAM_VERSION = '2'

dotenv_path = os.path.join(os.path.dirname(__file__), '.env')
if os.path.exists(dotenv_path):
    load_dotenv(dotenv_path)


if os.getenv("HEADLESS_BROWSER") == "True":
    HEADLESS_BROWSER_BOOL = True
elif os.getenv("HEADLESS_BROWSER") == "False":
    HEADLESS_BROWSER_BOOL = False
else:
    HEADLESS_BROWSER_BOOL = False


FILTER_FOLDER = "FILTER\\"
PARSE_FOLDER = "PARSE\\"
INTERACTED_FILE = "interacted.txt"
MANAGER_FILE = "manager.json"

account = os.getenv("TARGET_ACCOUNT")
target_accaunts = [account]
exclude_accaunts = []

skip_name_keywords = [
    "rabota", "onlin", "ipoteka", "karaoke", "fotoramki",
    "xudeet", "flowers", ".ru", ".com", ".pro", ".ua", ".net", "avtovorota",
    "namanicure", "cocktails", "otdih", "adler", "sohci", "discount", "nike",
    "adidas", "nogti", "vnalichii", "shop", "kakdoma", "toys", "handmade",
    "motivation", "pitanie", "nazakaz", "rings", "kalik", "shisha", "nogotok",
    "nogotochki", "nogotki", "nogoto4ki", "school", "prokat", "matras",
    "postel", "kids", "bags", "hlopok", "tkani", "malyshu", "_com", "mebel",
    "_magnitogorsk", "makeup", "cotton", "sinteshar", "hollofaiber",
    "sintepuh", "shapki", "_club", "pitomniki", "store", "avon", "dedmoroz",
    "khlopok", "vinyl", "photo", "narashivanie", "volos", "cindy",
    "bizhyteriya", "massage", "dietolog", "hlopok", "news", "dress", "recepti",
    "tekstile", "_nails", "_studio", "uslugi", "center", "oriflame", "sale",
    "style", "mp3", "support", "sport", "podelki", "kuhni", "remont",
    "komfort", "fincontrol"]

# "www.", "https",
skip_bio_keyword = [
    "бесплатно", "доставка", "Бесплатно", "Доставка", "ДИРЕКТ", "директ",
    "Одежда", "ОДЕЖДА", "одежда", "в наличии", "В наличии", "В НАЛИЧИИ",
    "под заказ", "ПОД ЗАКАЗ", "производство", "Производство", "отправка",
    "Отправка", "89", "+79", "+7 9", "8(9", "8 9", "+7 (", "WhatsApp",
    "зарабатываю", "Пн-Пт", "Пн-Сб", "пн-пт", "пн-сб", "срок работы",
    "Срок работы", "Производителей", "производителей", "заказ", "Заказ",
    "Direct", "Viber", "Ссылка", "ссылка", "ул. ", "ОПЫТ РАБОТЫ",
    "Опыт работы", "опыт работы", "СНГ ", "снг", "Риэлтор", "риэлтор",
    "наращивание", "Наращивание", "шугарринг", "Шугаринг", "Макияж",
    "СВЯЗАТЬСЯ", "Связаться", "связаться", "РАСПРОДАЮ", "Распродаю",
    "распродаю", "Ткани", "ткани", "прайс", "ПРАЙС", "Прайс", "бизнес",
    "Бизнес", "WA/VB", "VB/WA", "WatsApp", "ПОД КЛЮЧ", "под ключ", "V/WA",
    "AVON", "Тел:", "Хлопок", "хлопок", "Ткани", "ткани", "парикхмахер",
    "Парикхмахер", "Блогер", "блогер", "производителя", "Ручной работы",
    "ручной работы", "отправка", "Отправка", "косметика", " руб.", "магазин",
    "Магазин", "продажа", "Продажа", "Ремонт", "ремонт", "Обслуживание",
    "обслуживание", "Фаберлик", "фаберлик", "реклама", "Реклама", "Печать",
    "печать", "dir", "what’s up", "бровист", "Бровист", "Пиши мне", "Шоурум",
    "ШОУРУМ", "шоурум", "what’s app", "Самовывоз", "САМОВЫВОЗ", "Меню", "МЕНЮ",
    "Ипотека", "ИПОТЕКА", "Совкомбанк", "Работаем", "Вознаграждение", "Сайты",
    "Отчет", "платья", "Платья", "ОБУЧЕНИЕ", "обувь", "Обувь", "Кожа", "кожа",
    "КУКЛЫ", "Куклы", "куклы", "Набираю команду", "набираю команду",
    "НАБИРАЮ КОМАНДУ", "Научу зарабатывать", "дайрект", "нумеролог",
    "чакролог", "матрицу судьбы", "формулу души", "кармическую нумерологию",
    "Косметика", "косметика", "КОСМЕТИКА", "таргет", "Таргет", "ТАРГЕТ",
    "Гарантия", "гарантия", "ГАРАНТИЯ", "game studio", "1С-программирование",
    "проектирование", "СКУД", "БЕСПЛАТН", "Tele2", "Разрабатываем", "центр ",
    "поддержки", "WA/TGRAM", "ОБУЧЕНИЕ", "LEBEL", "FABULOSO", "REDKEN",
    "лайфхаки", "крутые видео", "Поделки", "Нумеролог", "Изготовление",
    "изготовление", "support", "Support", "Ремонт", "ремонт", "РЕМОНТ",
    "ЗАКАЗАТЬ", "МОТИВАТОР", "франшиза"]

person_categories = [
    "Architectural Designer", "Artist", "Athlete", "Creators & Celebrities",
    "Camera/Photo", "Contractor", "Doctor", "Dancer", "Entrepreneur", "Gamer",
    "Graphic Designer", "Journalist", "Just For Fun", "Lawyer & Law Firm",
    "Not a Business", "Optometrist", "Personal Blog", "Photographer",
    "Public Figure", "Real Estate Agent", "Real Estate Appraiser",
    "Real Estate Developer", "Song", "Tutor/Teacher", "Veterinarian",
    "Video Creator", "Visual Arts", "Web Designer", "Writer",
    "General Interest"]

all_business_categories = [
    "Advertising/Marketing", "Album", "Amateur Sports Team",
    "Apartment & Condo Building", "Appliance Repair Service", "App Page",
    "Architectural Designer", "Art", "Artist", "Arts & Entertainment",
    "Athlete", "Automotive Repair Shop", "Baby & Children’s Clothing Store",
    "Baby Goods/Kids Goods", "Bar", "Beauty, Cosmetic & Personal Care",
    "Beauty Salon", "Book", "Business Center", "Business Service",
    "Camera/Photo", "Canoe & Kayak Rental", "Chicken Joint",
    "Church of Christ", "Church of Jesus Christ of Latter-day Saints",
    "Clothing (Brand)", "Clothing Store", "College & University",
    "Commercial & Industrial", "Commercial & Industrial Equipment Supplier",
    "Commercial Bank", "Commercial Equipment", "Commercial Real Estate Agency",
    "Commercial Truck Dealership", "Community", "Community Organization",
    "Consulting Agency", "Contractor", "Convenience Store", "Credit Union",
    "Doctor", "Deli", "Dancer", "Design & Fashion", "Dessert Shop",
    "Discount Store", "Dorm", "E-Cigarette Store", "E-commerce Website",
    "Education", "Engineering Service", "Entertainment Website",
    "Entrepreneur", "Episode", "Event", "Family Style Restaurant",
    "Fashion Designer", "Fashion Model", "Fast Food Restaurant",
    "Financial Service", "Food & Beverage", "Food Stand", "Footwear Store",
    "Gamer", "Games/Toys", "Gaming Video Creator", "Government Organization",
    "Graphic Designer", "Grocery Store", "Hardware Store", "Health/Beauty",
    "Heating, Ventilating & Air Conditioning Service", "Home Decor",
    "Home Improvement", "Hospital", "Hotel", "Hotel & Lodging",
    "Ice Cream Shop", "In-Home Service", "Industrial Company",
    "Information Technology Company", "Insurance Company",
    "Interior Design Studio", "Internet Company", "Internet Marketing Service",
    "Japanese Restaurant", "Jazz & Blues Club", "Jewelry/Watches",
    "Jewelry & Watches Company", "Journalist", "Just For Fun", "Karaoke",
    "Kennel", "Kitchen & Bath Contractor", "Kitchen/Cooking",
    "Korean Restaurant", "Landmark & Historical Place", "Lawyer & Law Firm",
    "Library", "Loan Service", "Local Service", "Lumber Yard",
    "Marketing Agency", "Media", "Media/News Company", "Medical Center",
    "Medical School", "Men’s Clothing Store", "Mental Health Service", "Movie",
    "Musician/Band", "Music Lessons & Instruction School", "Music Video",
    "News & Media Website", "Newspaper", "Nonprofit Organization",
    "Non-Governmental Organization (NGO)", "Not a Business", "Nursing Agency",
    "Obstetrician-Gynecologist (OBGYN)", "Office Equipment Store",
    "Office Supplies", "Optician", "Optometrist",
    "Outdoor & Sporting Goods Company", "Personal Blog", "Petting Zoo",
    "Photographer", "Product/Service", "Public & Government Service",
    "Public Figure", "Public Utility Company", "Quay", "Real Estate",
    "Real Estate Agent", "Real Estate Appraiser", "Real Estate Company",
    "Real Estate Developer", "Record Label", "Religious Center",
    "Religious Organization", "Residence", "Restaurant", "Retail Bank",
    "School", "Science, Technology & Engineering", "Shopping & Retail",
    "Shopping District", "Shopping Mall", "Smoothie & Juice Bar", "Song",
    "Specialty School", "Sports & Recreation", "Sports League", "Sports Team",
    "Teens & Kids Website", "Telemarketing Service",
    "Tire Dealer & Repair Shop", "Trade School", "Traffic School",
    "Train Station", "Tutor/Teacher", "TV Channel", "TV Network", "TV Show",
    "Udon Restaurant", "Ukranian Restaurant", "Unagi Restaurant",
    "Uniform Supplier", "Urban Farm", "Vacation Home Rental", "Veterinarian",
    "Video Creator", "Video Game", "Visual Arts", "Web Designer", "Website",
    "Wedding Planning Service", "Winery/Vineyard", "Women’s Clothing Store",
    "Women’s Health Clinic", "Writer", "Xinjiang Restaurant",
    "Yakiniku Restaurant", "Yakitori Restaurant", "Yoga Studio",
    "Yoshoku Restaurant", "Youth Organization", "Zhejiang Restaurant", "Zoo]"]
