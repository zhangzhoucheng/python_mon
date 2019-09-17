import sys
import pymssql
import configparser

#append 是为了import导入处理非一个包问题
##或者：sys.path.append(os.path.abspath(os.path.dirname(__file__)+'/'+'..')) 把当前python程序所在目录的父目录的绝对路径加入到环境变量PYTHON_PATH中。PYTHON_PATH是python的搜索路径，再引入模块时就可以从父目录中搜索得到
sys.path.append(r'H:/softwarenew/workspace/python_money/rel_config_file')

# 从文件系统读取配置文件
cf = configparser.ConfigParser()
print(cf.sections())
cf.read("H:/softwarenew/workspace/python_money/rel_config_file/mysql_config.txt")
print(cf.sections())
host = cf.get("MYSQL", "host")
user = cf.get("MYSQL", "user")
pwd = cf.get("MYSQL", "pwd")
db = cf.get("MYSQL", "db")
charset = cf.get("MYSQL","charset")
print(host,pwd,user,db,charset)


class DbUtils:
    # def __init__(self,host=None,user=None,pwd=None,db=None):
    def __init__(self):
        self.host = host
        self.user = user
        self.pwd = pwd
        self.db = db
        self.charset = charset

        self._conn = self.GetConnect()
        if (self._conn):
            self._cur = self._conn.cursor()

            # 连接数据库

    def GetConnect(self):
        conn = False
        try:
            conn = pymssql.connect(
                host=self.host,
                user=self.user,
                password=self.pwd,
                database=self.db,
                charset=self.charset
            )
        except Exception as err:
            print("连接数据库失败, %s" % err)
        else:
            return conn

            # 执行查询

    def ExecQuery(self, sql):
        res = ""
        try:
            self._cur.execute(sql)
            res = self._cur.fetchall()
        except Exception as err:
            print("查询失败, %s" % err)
        else:
            return res

            # 执行非查询类语句

    def ExecNonQuery(self, sql):
        flag = False
        try:
            self._cur.execute(sql)
            self._conn.commit()
            flag = True
        except Exception as err:
            flag = False
            self._conn.rollback()
            print("执行失败, %s" % err)
        else:
            return flag

            # 获取连接信息

    def GetConnectInfo(self):
        print("连接信息：")
        print("服务器:%s , 用户名:%s , 数据库:%s " % (self.host, self.user, self.db))

        # 关闭数据库连接

    def Close(self):
        if (self._conn):
            try:
                if (type(self._cur) == 'object'):
                    self._cur.close()
                if (type(self._conn) == 'object'):
                    self._conn.close()
            except:
                raise ("关闭异常, %s,%s" % (type(self._cur), type(self._conn)))