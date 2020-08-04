import sys
import numpy as np
import matplotlib.image as img

from simple_train import simple_train as train

sys.path.append("../read_picture/")
import read_picture

lst = []  # List of all Square objects, includes square color and number

class Square:
    color = int
    number = int
    def __init__(self, color, number=None):
        self.color = color  # RED is 1, BLUE is 2, GREEN is 3
        self.number = number

def set_squares():

    train_image, train_label = read_picture.read_image_data('../mnist_data/train-images.idx3-ubyte',
                                                            '../mnist_data/train-labels.idx1-ubyte')

    train_image_vector = np.reshape(train_image, (60000, 784))
    simple_train = train.simple_train_one_num(train_image_vector[0:5000], train_label[0:5000], 10, 0.1, 2.55)
    simple_train.train_learn()

    counter_a = 0
    while counter_a < 64:
        image = img.imread("../auto_grader/image/"+str(counter_a)+".png")
        w, h = image.shape[:2]

        grayImg = np.zeros([w, h, 4])

        flag = 0

        for i in range(w):
            for j in range(h):
                pxl = [float(image[i][j][0]), float(image[i][j][1]), float(image[i][j][2])]
                if flag > 0:
                    break
                else:
                    if pxl[0] > 0:
                        flag = 1
                    elif pxl[1] > 0:
                        flag = 2
                    elif pxl[2] > 0:
                        flag = 3

        for i in range(w):
            for j in range(h):
                pxl = [float(image[i][j][0]), float(image[i][j][1]), float(image[i][j][2])]
                avg = float(np.average(pxl))
                grayImg[i][j][0] = avg
                grayImg[i][j][1] = avg
                grayImg[i][j][2] = avg
                grayImg[i][j][3] = 1

        img.imsave('image_processing/image/'+str(counter_a)+'.png', grayImg)

        square = Square(flag)
        lst.append(square)

        counter_a += 1

    numberLst = []
    numCounter = 0
    while numCounter < 64:

        image = img.imread("image_processing/image/" + str(numCounter) + ".png")
        w, h = image.shape[:2]

        counter_b = 0
        predictLst = []

        while counter_b < 64:
            grayImg = []
            for i in range(w):
                for j in range(h):
                    pxl = float(image[i][j][0])
                    grayImg.append(pxl)
                    predictLst.append(grayImg)

            counter_b += 1

        predictLst = np.array(predictLst)
        predict = predictLst[0:63]

        numbers = simple_train.predict(predict)
        numberLst.append(numbers[0])

        numCounter += 1

    counter_c = 0
    while counter_c < 64:
        lst[counter_c].number = numberLst[counter_c]
        print(lst[counter_c].number)
        print(lst[counter_c].color)
        counter_c += 1

