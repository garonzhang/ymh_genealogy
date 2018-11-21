import pymysql


class DbManager:
    def __init__(self):
        self.conn = pymysql.connect(host='127.0.0.1',
                                    unix_socket='/tmp/mysql.sock',
                                    user='root',
                                    passwd='zgl123',
                                    db='jiapu',
                                    charset='utf8')

    def commit(self):
        self.conn.commit()

    def close(self):
        self.conn.close()
