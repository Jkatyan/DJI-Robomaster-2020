import sys
import numpy as np
import matplotlib.image as img

from simple_train import simple_train as train

sys.path.append("../read_picture/")
import read_picture

stdout = sys.stdout
lst = []


class Square:
    def __init__(self, color=None, number=None, x=None, y=None):
        if color == -1 and number == -1:
            self.edge = True
        else:
            self.edge = False
        self.color = color  # RED is 1, BLUE is 2, GREEN is 3
        self.number = number
        self.x = x
        self.y = y
        self.dist = 0
        self.isExact = False

    def __repr__(self):
        if self.dist != 0:
            return '0' + str(self.dist)
        elif not self.edge:
            return [None, 'R', 'G', 'B'][self.color]+str(self.number)
        else:
            return "ED"
        #return str(self.x) + str(self.y)

    def __eq__(self, obj):
        return \
            self.x == obj.x and \
            self.y == obj.y and \
            self.dist == obj.dist

def start_recognition():
    print("> Starting training.", end="\n\n")
    train_image, train_label = read_picture.read_image_data('../mnist_data/train-images.idx3-ubyte',
                                                            '../mnist_data/train-labels.idx1-ubyte')
    train_image_vector = np.reshape(train_image, (60000, 784))
    simple_train = train.simple_train_one_num(train_image_vector[0:5000], train_label[0:5000], 10, 0.01, 0.255)
    simple_train.train_learn()
    print("> Training finished.", end="\n\n")

    print("> Starting color recognition.", end="\n\n")
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

    print("> Starting number recognition.", end="\n\n")

    predict_lst = []
    for num_counter in range(64):

        image = img.imread("image_processing/image/" + str(num_counter) + ".png")
        w, h = image.shape[:2]

        gray_img = []

        for i in range(w):
            for j in range(h):
                pxl = float(image[i][j][0])
                gray_img.append(pxl)

        predict_lst.append(gray_img)

    numbers = simple_train.predict(predict_lst)

    print("> Finished image recognition.", end="\n\n")

    for i in range(64):
        lst[i].number = numbers[i]
        if lst[i].color == 1:
            color = "R"
        elif lst[i].color == 2:
            color = "G"
        else:
            color = "B"
        print(color + str(lst[i].number) + ", ", end="")
        if i % 8 == 7:
            print()
