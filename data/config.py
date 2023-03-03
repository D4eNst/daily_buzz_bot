import os
import dotenv

dotenv.load_dotenv(".env")


token = os.environ["TOKEN"]
admin_id = os.environ["ADMIN_ID"]
language = "ru"
currency = "₽"
min_replenishment_amount = 40
