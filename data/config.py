import os
import dotenv

dotenv.load_dotenv(".env")

token = os.environ["TOKEN"]
payment_token = os.environ["PAYMENT_TOKEN"]
admin_id = int(os.environ["ADMIN_ID"])
language = "ru"
currency = "₽"
min_replenishment_amount = 2

discount_list = [0, 5, 10, 20]
status_titles = ['Bronze', 'Silver', 'Gold', 'Diamond']
status_points = [0, 350, 750, 1500]
