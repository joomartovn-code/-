import sqlite3
from datetime import datetime

class Database:
    def __init__(self, db_name='orders.db'):
        self.conn = sqlite3.connect(db_name, check_same_thread=False)
        self.create_table()
    
    def create_table(self):
        query = '''
        CREATE TABLE IF NOT EXISTS orders (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            customer_name TEXT NOT NULL,
            order_item TEXT NOT NULL,
            delivery_time TEXT NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
        '''
        self.conn.execute(query)
        self.conn.commit()
    
    def add_order(self, customer_name, order_item, delivery_time):
        query = '''
        INSERT INTO orders (customer_name, order_item, delivery_time)
        VALUES (?, ?, ?)
        '''
        self.conn.execute(query, (customer_name, order_item, delivery_time))
        self.conn.commit()
        return self.conn.cursor().lastrowid
    
    def get_all_orders(self):
        query = '''
        SELECT id, customer_name, order_item, delivery_time, created_at 
        FROM orders 
        ORDER BY created_at DESC
        '''
        cursor = self.conn.execute(query)
        return cursor.fetchall()
    
    def get_order(self, order_id):
        query = '''
        SELECT id, customer_name, order_item, delivery_time 
        FROM orders 
        WHERE id = ?
        '''
        cursor = self.conn.execute(query, (order_id,))
        return cursor.fetchone()
    
    def update_order(self, order_id, customer_name=None, order_item=None, delivery_time=None):
        updates = []
        params = []
        
        if customer_name:
            updates.append("customer_name = ?")
            params.append(customer_name)
        if order_item:
            updates.append("order_item = ?")
            params.append(order_item)
        if delivery_time:
            updates.append("delivery_time = ?")
            params.append(delivery_time)
        
        if not updates:
            return False
        
        params.append(order_id)
        query = f"UPDATE orders SET {', '.join(updates)} WHERE id = ?"
        
        self.conn.execute(query, params)
        self.conn.commit()
        return self.conn.total_changes > 0
    
    def delete_order(self, order_id):
        query = 'DELETE FROM orders WHERE id = ?'
        self.conn.execute(query, (order_id,))
        self.conn.commit()
        return self.conn.total_changes > 0
    
    def close(self):
        self.conn.close()