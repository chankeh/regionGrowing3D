import numpy as np

def regionGrowing(grayImg,seed,threshold):
    """
    :param grayImg: 灰度图像
    :param seed: 生长起始点的位置
    :param threshold: 阈值
    :return: 取值为{0, 255}的二值图像
    """
    [maxX, maxY,maxZ] = grayImg.shape[0:3]

    # 用于保存生长点的队列
    pointQueue = []
    pointQueue.append((seed[0], seed[1],seed[2]))
    outImg = np.zeros_like(grayImg)
    outImg[seed[0], seed[1],seed[2]] = 255

    pointsNum = 1
    pointsMean = float(grayImg[seed[0], seed[1],seed[2]])

    # 用于计算生长点周围26个点的位置
    Next26 = [[-1, -1, -1],[-1, 0, -1],[-1, 1, -1],
                [-1, 1, 0], [-1, -1, 0], [-1, -1, 1],
                [-1, 0, 1], [-1, 0, 0],[-1, 0, -1],
                [0, -1, -1], [0, 0, -1], [0, 1, -1],
                [0, 1, 0],[-1, 0, -1],
                [0, -1, 0],[0, -1, 1],[-1, 0, -1],
                [0, 0, 1],[1, 1, 1],[1, 1, -1],
                [1, 1, 0],[1, 0, 1],[1, 0, -1],
                [1, -1, 0],[1, 0, 0],[1, -1, -1]]

    while(len(pointQueue)>0):
        # 取出队首并删除
        growSeed = pointQueue[0]
        del pointQueue[0]

        for differ in Next26:
            growPointx = growSeed[0] + differ[0]
            growPointy = growSeed[1] + differ[1]
            growPointz = growSeed[2] + differ[2]

            # 是否是边缘点
            if((growPointx < 0) or (growPointx > maxX - 1) or
               (growPointy < 0) or (growPointy > maxY - 1) or (growPointz < 0) or (growPointz > maxZ - 1)) :
                continue

            # 是否已经被生长
            if(outImg[growPointx,growPointy,growPointz] == 255):
                continue

            data = grayImg[growPointx,growPointy,growPointz]
            # 判断条件
            # 符合条件则生长，并且加入到生长点队列中
            if(abs(data - pointsMean)<threshold):
                pointsNum += 1
                pointsMean = (pointsMean * (pointsNum - 1) + data) / pointsNum
                outImg[growPointx, growPointy,growPointz] = 255
                pointQueue.append([growPointx, growPointy,growPointz])

    return outImg