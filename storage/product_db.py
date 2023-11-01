import sqlite3

from datetime import datetime
from typing import Optional

from product import Product


class ProductDatabase:
    def __init__(self, db_file):
        self.conn = sqlite3.connect(db_file, check_same_thread=False)
        self.cursor = self.conn.cursor()
        self.cursor.execute('''
                    CREATE TABLE IF NOT EXISTS products (
                        name TEXT,
                        url TEXT PRIMARY KEY,
                        last_price REAL,
                        min_price REAL,
                        min_price_date TEXT,
                        max_price REAL,
                        max_price_date TEXT
                    )
                ''')

    def add_product(self, product: Product):
        try:
            self.cursor.execute("INSERT INTO products VALUES (?, ?, ?, ?, ?, ?, ?)", (
                product.name,
                product.url,
                product.current_price,
                product.current_price,
                None,
                product.current_price,
                None
            ))
        except sqlite3.IntegrityError:
            self.cursor.execute("UPDATE products SET name=?, last_price=?, min_price=?, min_price_date=?,"
                                "  max_price=?, max_price_date=?  WHERE url=?", (
                                    product.name,
                                    product.current_price,
                                    product.current_price,
                                    None,
                                    product.current_price,
                                    None,
                                    product.url
                                ))
        self.conn.commit()

    def get_price(self, url: str) -> Optional[str]:
        self.cursor.execute("SELECT last_price FROM products WHERE url=?", (url,))
        result = self.cursor.fetchone()
        if result is None:
            return None
        else:
            return result[0]

    def get_product(self, url: str) -> Optional[Product]:
        self.cursor.execute("SELECT * FROM products WHERE url=?", (url,))
        result = self.cursor.fetchone()
        if result is None:
            return None
        else:
            name, url, last_price, min_price, min_price_date, max_price, max_price_date = result
            return Product(url=url,
                           name=name,
                           last_price=last_price,
                           min_price_date=min_price_date,
                           max_price=max_price,
                           max_price_date=max_price_date
                           )

    def get_all_products(self) -> list[Product]:
        self.cursor.execute("SELECT * FROM products")
        results = self.cursor.fetchall()
        return [Product(url=url, name=name, current_price=last_price) for name, url, last_price in results]

    def get_all_urls(self) -> list[str]:
        self.cursor.execute("SELECT url FROM products")
        results = self.cursor.fetchall()
        return [url[0] for url in results]

    def remove_product(self, product: Product):
        self.cursor.execute("DELETE FROM products WHERE url=?", (product.url,))
        self.conn.commit()

    def update_price(self, product: Product):
        assert product.has_price()
        product = self.get_product(product.url)
        assert product
        self.cursor.execute("UPDATE products SET last_price=?, min_price=?, min_price_date=?, max_price=?,"
                            " max_price_date=? WHERE url = ?",
                            (product.last_price,
                             product.last_price if product.last_price < product.min_price else product.min_price,
                             datetime.now().strftime('%Y-%m-%d %H:%M')
                                if product.last_price < product.min_price else product.min_price_date,
                             product.last_price if product.last_price > product.max_price else product.max_price,
                             datetime.now().strftime('%Y-%m-%d %H:%M')
                                if product.last_price > product.max_price else product.max_price_date,
                             product.url))
        self.conn.commit()

    def __del__(self):
        self.cursor.close()
        self.conn.close()
