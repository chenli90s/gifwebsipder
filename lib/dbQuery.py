import pymysql

class DBQuery:
    
    def __init__(self, **kwargs):
        self.kw = kwargs
        # self.pool = dict()
    
    def create_conn(self):
        conn = pymysql.connect(
            host=self.kw.get('host', 'localhost'),
            port=self.kw.get('port', 3306),
            user=self.kw.get('user', 'root'),
            password=self.kw.get('password', 'root'),
            db=self.kw['db'],
            charset=self.kw.get('charset', 'utf8')
        )
        # self.pool.append(conn)
        return conn
    
    def select(self, sql, args=None, size=None):
        conn = self.create_conn()
        cur = conn.cursor()
        sql = sql.replace('?', '%s')
        print(sql)
        cur.execute(sql, args)
        if size:
            rs = cur.fetchmany(size)
        else:
            rs = cur.fetchall()
        cur.close()
        conn.close()
        return rs
    
    def execute(self, sql, args=None):
        conn = self.create_conn()
        cur = conn.cursor()
        re = cur.execute(sql.replace('?', '%s'), args)
        conn.commit()
        cur.close()
        conn.close()
        return re
    
if __name__ == '__main__':
    db = DBQuery(db = 'jing_dong')
    print(db.select("select * from goods"))