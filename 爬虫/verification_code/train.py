import numpy as np
import operator
import time
import os
import pickle
from cv2 import imread


# 调用KNN算法
# 参数：(inputPoint :vectorUnderTest 测试文本向量化 32x32 -> 1x1024)
# 参数：(dataSet :trainingMat        训练集文本向量化 32x32 -> 1x1024)
# 参数：(labels :hwLabels            训练集文本中解析分类数字  )
# 参数：(k :3)
def classify(inputPoint, dataSet, labels, k):
    dataSetSize = dataSet.shape[0]  # 已知分类的训练集的行数
    # 先tile函数将输入点拓展成与训练集相同维数的矩阵，再计算欧氏距离
    diffMat = np.tile(inputPoint, (dataSetSize, 1)) - dataSet  # 样本与训练集的差值矩阵
    sqDiffMat = diffMat**2  # 差值矩阵平方
    sqDistances = sqDiffMat.sum(axis=1)  # 计算每一行上元素的和
    distances = sqDistances**0.5  # 开方得到欧拉距离矩阵
    sortedDistIndicies = distances.argsort()  # 按distances中元素进行升序排序后得到的对应下标的列表
    classCount = {}  # 选择距离最小的k个点
    for i in range(k):
        voteIlabel = labels[sortedDistIndicies[i]]
        classCount[voteIlabel] = classCount.get(voteIlabel, 0) + 1
    # 按classCount字典的第2个元素（即类别出现的次数）从大到小排序
    sortedClassCount = sorted(classCount.items(),
                              key=operator.itemgetter(1),
                              reverse=True)
    return sortedClassCount[0][0]


# 1. 数据准备：数字图像文本向量化，这里将32x32的二进制图像文本矩阵转换成1x1024的向量。循环读出文件的前32行，存储在向量中。
# 文本向量化 32x32 -> 1x1024
def img2vector(filename):
    returnVect = []
    img = imread(filename, 0)
    for i in range(32):
        lineStr = img[i]
        for j in range(32):
            returnVect.append(int(lineStr[j]))
    return returnVect


# 2. 构建训练数据集：利用目录trainingDigits中的文本数据构建训练集向量，以及对应的分类向量
# 从文件名中解析分类数字
def classnumCut(fileName):
    fileStr = fileName.split('.')[0]
    classNumStr = fileStr.split(' ')[0]
    return classNumStr


# 构建训练集数据向量，及对应分类标签向量
def trainingDataSet(TrainPath):
    hwLabels = []
    trainingFileList = os.listdir(TrainPath)  # 获取目录内容
    m = len(trainingFileList)
    trainingMat = np.zeros((m, 1024))  # m维向量的训练集
    for i in range(m):
        fileNameStr = trainingFileList[i]  # 找到一个样本文件
        hwLabels.append(classnumCut(fileNameStr))  # 将文件传入classnumCut函数，从文件名中解析分类数字
        trainingMat[i, :] = img2vector('%s/%s' % (TrainPath, fileNameStr))  # 将文件传入img2vector函数中，这里将32x32的二进制图像文本矩阵转换成1x1024的向量
    return hwLabels, trainingMat  # 返回两个文件


# 3. 测试集数据测试：通过测试testDigits目录下的样本，来计算算法的准确率。
# 测试函数
def numberTest(TrainPath, TestPath, SavePath):
    hwLabels, trainingMat = trainingDataSet(TrainPath)  # 构建训练集
    testFileList = os.listdir(TestPath)  # 获取测试集
    errorCount = 0.0  # 错误数
    mTest = len(testFileList)  # 测试集总样本数
    t1 = time.time()

    for i in range(mTest):
        fileNameStr = testFileList[i]  # 找到一个测试文件
        classNumStr = classnumCut(fileNameStr)  # 将文件传入classnumCut函数，从文件名中解析分类数字
        vectorUnderTest = img2vector('%s/%s' % (TestPath, fileNameStr))  # 将文件传入img2vector函数，将32x32的二进制图像文本矩阵转换成1x1024的向量
        classifier_result = classify(vectorUnderTest, trainingMat, hwLabels, 3)  # 调用    KNN          算法进行测试
        print("classifier_result: %s, the real answer is: %s\n" % (classifier_result, classNumStr))
        if classifier_result != classNumStr:
            errorCount += 1.0
    print("the total number of tests is: %d" % mTest)  # 输出测试总样本数
    print("the total number of errors is: %d" % errorCount)  # 输出测试错误样本数
    print("the total error rate is: %f" % (errorCount / float(mTest)))  # 输出错误率
    t2 = time.time()
    print("Cost time: %.2fmin, %.4fs." % ((t2 - t1) // 60, (t2 - t1) % 60))  # 测试耗时

    # 保存模型
    knn = trainingMat
    with open(SavePath + 'knn_1.pickle', 'wb') as f:
        pickle.dump(knn, f)
    knn = hwLabels
    with open(SavePath + 'knn_2.pickle', 'wb') as f:
        pickle.dump(knn, f)


# 4. 运行模型, 并返回最终答案
def runKNN(TestPath):
    with open('./verification_code/knn_1.pickle', 'rb') as f:
        trainingMat = pickle.load(f)
    with open('./verification_code/knn_2.pickle', 'rb') as f:
        hwLabels = pickle.load(f)
    testFileList = os.listdir(TestPath)  # 获取图片
    mTest = len(testFileList)  # 要判断的图片总数
    outcome = []
    for i in range(mTest):
        fileNameStr = testFileList[i]  # 找到一个图片
        vectorUnderTest = img2vector('%s/%s' % (TestPath, fileNameStr))  # 将文件传入img2vector函数，将32x32的二进制图像文本矩阵转换成1x1024的向量
        classifier_result = classify(vectorUnderTest, trainingMat, hwLabels, 3)  # 调用KNN算法进行测试
        outcome.append(classifier_result)
        # print("classifier_result: %s\n" % classifier_result)

    mode = 0
    operational = 0
    equalSign = 0
    num1 = []
    num2 = []
    a = 0
    b = 0
    # 删除多余的元素o
    for i in outcome:
        if (i == 'o'):
            outcome.remove(i)
    print(outcome)
    # 判断运算形式, 并保存数字
    for i in outcome:
        if (i == '+'):
            mode = 1
            operational = outcome.index(i)
            num1.extend(outcome[:operational])
        elif (i == '-'):
            mode = 2
            operational = outcome.index(i)
            num1.extend(outcome[:operational])
        elif (i == 'x'):
            mode = 3
            operational = outcome.index(i)
            num1.extend(outcome[:operational])
        elif (i == '='):
            equalSign = outcome.index(i)
            num2.extend(outcome[operational + 1:equalSign])
    a = digit(num1)
    b = digit(num2)
    return operation(mode, a, b)


# 判断数字位数，并返回整形
def digit(num):
    if (len(num) == 1):
        return int(num[0])
    else:
        return ((int(num[0]) * 10) + int(num[1]))


# 计算方法
def operation(mode, num1, num2):
    if (mode == 1):
        return num1 + num2
    elif (mode == 2):
        return num1 - num2
    else:
        return num1 * num2
