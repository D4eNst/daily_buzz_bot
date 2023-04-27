from .models import User, Product, History, get_final_price
import asyncpg


async def create_pool():
    return await asyncpg.create_pool(user="dev", password="qwerty", database="postgres",
                                     host="localhost", port=5432, command_timeout=60)


class Database:

    def __init__(self, connector: asyncpg.pool.Pool):
        self.connector = connector
        self.cursor = self.connector

    async def create_tables(self) -> None:
        await self.connector.execute("""
        CREATE TABLE IF NOT EXISTS users(
            tg_id BIGINT PRIMARY KEY,
            balance INT DEFAULT 0,
            total_buy INT DEFAULT 0,
            status INT DEFAULT 0,
            subscribe BOOL DEFAULT FALSE,
            subscribe_date TEXT,
            subscribe_period INT
        )""")

        await self.connector.execute("""
        CREATE TABLE IF NOT EXISTS products(
            product_type TEXT,
            product_id SERIAL PRIMARY KEY,
            title TEXT,
            period INT,
            price INT,
            is_active INTEGER DEFAULT 1
        )""")

        await self.connector.execute("""
            CREATE TABLE IF NOT EXISTS history(
                id SERIAL PRIMARY KEY,
                tg_id BIGINT,
                product_id INT,
                date TEXT,
                current_status INT DEFAULT 0,
                FOREIGN KEY (tg_id) REFERENCES users (tg_id),
                FOREIGN KEY (product_id) REFERENCES products (product_id)
            )""")

    async def add_user(self, user: User) -> None:
        query = """INSERT INTO users(tg_id) VALUES($1)"""
        await self.connector.execute(query, user.tg_id)

    async def get_user(self, user_id: int) -> User or None:
        query = f"SELECT * FROM users WHERE tg_id = $1"
        res = (await self.connector.fetch(query, user_id))
        if not res:
            return None
        else:
            user = User(*res[0])
            return user

    async def update_user(self, user: User) -> None:
        query = """UPDATE users SET
        balance = $1,
        total_buy = $2,
        status = $3,
        subscribe = $4,
        subscribe_date = $5,
        subscribe_period = $6 WHERE tg_id = $7
        """
        await self.connector.execute(query, *user.get_values(), user.tg_id)

    def del_user(self, user: User) -> None:
        pass

    async def add_subscribe(self, sub: Product) -> None:
        query = """INSERT INTO products(product_type, title, period, price) VALUES($1, $2, $3, $4)"""
        await self.connector.execute(query, *sub.get_values())

    async def get_product(self, sub_id) -> Product or None:
        query = """SELECT * FROM products WHERE product_id=$1"""
        res = (await self.connector.fetch(query, sub_id))
        if not res:
            return None
        else:
            product = Product(*res[0])
            return product

    async def get_subscribes(self) -> list:
        query = """SELECT * FROM products WHERE is_active=1 AND product_type='Subscribe' ORDER BY price"""
        res = await self.connector.fetch(query)
        subs = []
        for item in res:
            subs.append(Product(*item))
        return subs

    def update_subscribe(self, sub) -> None:
        pass

    async def del_product(self, sub: Product) -> None:
        query = """UPDATE products SET is_active=$1 WHERE product_id=$2"""
        await self.connector.execute(query, 0, sub.product_id)

    async def add_history(self, history: History) -> None:
        query = """INSERT INTO history(tg_id, product_id, date, current_status) VALUES($1, $2, $3, $4)"""
        await self.connector.execute(query, *history.get_values())

    async def get_history(self, user: User) -> list:
        query = """SELECT history.*, products.* FROM history
                   LEFT JOIN products ON history.product_id = products.product_id 
                   WHERE history.tg_id=$1 order by date"""
        res = await self.connector.fetch(query, user.tg_id)

        histories = []
        total_buy = 0
        for item in res:
            history_values = item[:5]
            product_values = item[5:]
            histories.append(
                {
                    'product': Product(*product_values),
                    'history': History(*history_values),
                    'total_buy': -1
                }
            )
            total_buy += get_final_price(histories[-1]['product'].price, histories[-1]['history'].current_status)
        if histories:
            histories[-1]['total_buy'] = total_buy
        return histories

    def update_history(self) -> None:
        pass

    def del_history(self) -> None:
        pass
