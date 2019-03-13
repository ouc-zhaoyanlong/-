import struct

def readImg(path):
    with open(path,'rb') as f:
        info = f.read()
    return info

def writeImg(path,info):
    with open(path,'wb') as f:
        f.write(info)

if __name__=="__main__":
    path = 'logo.bmp'
    toPath = 'logo5.bmp'

    info = readImg(path)#位图二进制信息

    print("位图文件头")
    dataFileHeader = struct.unpack('<HIHHI',info[0:14])
    print(dataFileHeader)  #元组，里面元素是int型
    print('位图信息头')
    dataInfoHeader = struct.unpack('<IIIHHIIIIII',info[14:54])
    print(dataInfoHeader)

    resInfo = info[0:54] #头部信息复制

    heightLen = dataInfoHeader[1]
    widthLen = dataInfoHeader[2] #获取图像size
    color = dataInfoHeader[4] #获取每个像素点的比特值
    startLocation = dataFileHeader[4] #获取图像数据开始坐标

    #计算每一行字节数
    heightSize = (heightLen*color+31)//32*4

    #信息处理
    for i in range(widthLen):
        sl = startLocation + i*heightSize
        el = sl + heightSize
        for j in range(sl,el,3):
            if j+2<el:
                if info[j]<=40 and info[j+1]<=40 and info[j+2]<=40:
                    resInfo = resInfo + bytes([0])+bytes([255])+bytes([0])
                else:
                    resInfo = resInfo + bytes([info[j]])+bytes([info[j+1]])+bytes([info[j+2]])
            elif j+1<el:
                resInfo = resInfo + bytes([info[j]])+bytes([info[j+1]])
            else:
                resInfo = resInfo + bytes([info[j]])
    #空余信息补全
    for i in range(len(resInfo), len(info), 1):
        resInfo += bytes([0])
    #写入文件
    writeImg(toPath, resInfo)
