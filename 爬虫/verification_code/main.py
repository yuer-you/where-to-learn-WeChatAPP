from ImgFunction import ImgInOut, EnlargeImg
from train import runKNN  # , numberTest
from GetImg import getImg, mkdir, deldir

# 训练模型并保存
# numberTest('./train/all', './test', './')

# 先创建三个文件夹, 分别为a, b, c
# 其中c不用加 './', 因为在函数中已经添加, c内存放原始验证码图片, a内存放降噪处理后的分割图像, b内存放扩大尺寸后的a内的图像

# 因为图片处理过程中仍有机率处理不达标准导致识别错误，所以要使用try函数来避免错误的抛出，并进行下一次登录尝试
ok = 0
while (ok == 0):
    try:
        a = './a'
        b = './b'
        c = 'c'
        # 创建文件夹
        mkdir(a)
        mkdir(b)
        mkdir(c)
        # 从网页下载验证码
        getImg(c)
        # 处理图片及调用模型进行计算
        ImgInOut(c, a)
        EnlargeImg(a, b)
        print('答案是：%d' % runKNN(b))
        # 删除文件夹
        deldir(a)
        deldir(b)
        deldir(c)
        ok = 1
        print('Pass!')
    except Exception:
        print('ERROR! Try again!')
