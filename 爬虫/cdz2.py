import os
import pandas as pd
import time
from sqlalchemy import create_engine
time0=0
time1=0
def findAllFile(base):
    for root, ds, fs in os.walk(base):
        for f in fs:
            yield f
def findAllFileName(base):
    for root, ds, fs in os.walk(base):
        for f in fs:
            fullname = os.path.join(root, f)
            yield fullname
def path_name(base):
    for path,name in zip(findAllFile(base),findAllFileName(base)):
        yield (path,name)
def main(base):
    for path,name in enumerate(path_name(base)): 
        name=list(name)
        print(name)
        time0=time.time()

        engine = create_engine('mysql+pymysql://你的用户名:你的密码@localhost:3306/'+name[1].split('\\')[2])
        # 读取本地CSV文件
        df = pd.read_csv(name[1], sep=',')

        # 将新建的DataFrame储存为MySQL中的数据表，不储存index列
        df.to_sql(name=name[0][:-4],if_exists='replace', con=engine, index= False)
        time1=time.time()
        print(time1-time0)


if __name__ == '__main__':
    main(".\\data\\")


