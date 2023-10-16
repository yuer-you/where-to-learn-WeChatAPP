import os
import time
import random

delay_time = random.randint(0, 300)
time.sleep(delay_time)

start_dire1 = r"selenium_login.py"
start_dire2 = r"cdz.py"
start_dire3 = r"cdz2.py"

r1 = os.system("python %s" %start_dire1)
r2 = os.system("python %s" %start_dire2)
r3 = os.system("python %s" %start_dire3)

print(r1)
print(r2)
print(r3)
