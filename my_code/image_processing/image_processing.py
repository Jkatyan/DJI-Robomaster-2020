import sys
import numpy as np
import matplotlib.image as plt
import statistics

from simple_train import simple_train as train

sys.path.append("../read_picture/")
import read_picture

stdout = sys.stdout

# Lists
lst = []
lst2 = []

class Square:
    def __init__(self, color=None, number=None, x=None, y=None):
        if color == -1 and number == -1:
            self.edge = True
        else:
            self.edge = False
        self.color = color
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

    def __eq__(self, obj):
        return \
            self.x == obj.x and \
            self.y == obj.y and \
            self.dist == obj.dist


def start_recognition_simple():

    print("> Starting training.", end="\n\n")

    train_image, train_label = read_picture.read_image_data('../mnist_data/train-images.idx3-ubyte',
                                                            '../mnist_data/train-labels.idx1-ubyte')

    train_image_vector = np.reshape(train_image, (60000, 784))
    simple_train = train.simple_train_one_num(train_image_vector[0:5000], train_label[0:5000], 10, 0.01, 0.255)
    simple_train.train_learn()
    print("> Trainer 1/5 trained.")
    simple_train2 = train.simple_train_one_num(train_image_vector[5001:10000], train_label[5001:10000], 10, 0.01, 0.255)
    simple_train2.train_learn()
    print("> Trainer 2/5 trained.")
    simple_train3 = train.simple_train_one_num(train_image_vector[10001:15000], train_label[10001:15000], 10, 0.01, 0.255)
    simple_train3.train_learn()
    print("> Trainer 3/5 trained.")
    simple_train4 = train.simple_train_one_num(train_image_vector[15001:20000], train_label[15001:20000], 10, 0.01, 0.255)
    simple_train4.train_learn()
    print("> Trainer 4/5 trained.")
    simple_train5 = train.simple_train_one_num(train_image_vector[20001:25000], train_label[20001:25000], 10, 0.01, 0.255)
    simple_train5.train_learn()
    print("> Trainer 5/5 trained.", end="\n\n")

    print("> Starting color recognition.", end="\n\n")

    counter_a = 0
    while counter_a < 64:
        image = plt.imread("../auto_grader/image/"+str(counter_a)+".png")
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

        plt.imsave('image_processing/image/'+str(counter_a)+'.png', grayImg)

        square = Square(flag)
        lst.append(square)
        lst2.append(square)

        counter_a += 1

    print("> Starting number recognition.", end="\n\n")

    predict_lst = []
    vote_lst = []
    numbers = []
    numbers_second = []

    for num_counter in range(64):

        image = plt.imread("image_processing/image/" + str(num_counter) + ".png")
        w, h = image.shape[:2]

        gray_img = []

        for i in range(w):
            for j in range(h):
                pxl = float(image[i][j][0])
                gray_img.append(pxl)

        predict_lst.append(gray_img)

    numbers1 = simple_train.predict(predict_lst)
    numbers2 = simple_train2.predict(predict_lst)
    numbers3 = simple_train3.predict(predict_lst)
    numbers4 = simple_train4.predict(predict_lst)
    numbers5 = simple_train5.predict(predict_lst)

    for i in range(64):
        vote_lst.append(numbers1[i])
        vote_lst.append(numbers2[i])
        vote_lst.append(numbers3[i])
        vote_lst.append(numbers4[i])
        vote_lst.append(numbers5[i])

        numbers.append(int(statistics.mode(vote_lst)))

        if (numbers1[i] != int(statistics.mode(vote_lst))) or \
            (numbers2[i] != int(statistics.mode(vote_lst))) or \
            (numbers3[i] != int(statistics.mode(vote_lst))) or \
            (numbers4[i] != int(statistics.mode(vote_lst))) or \
            (numbers5[i] != int(statistics.mode(vote_lst))):

            list(filter(lambda a: a != int(statistics.mode(vote_lst)), vote_lst))
            numbers_second.append(int(statistics.mode(vote_lst)))
        else:
            numbers_second.append(int(statistics.mode(vote_lst)))

        vote_lst.clear()

    print("> Finished image recognition.", end="\n\n")

    for i in range(64):
        lst[i].number = numbers[i]
        lst2[i].number = numbers_second[i]
        if lst[i].color == 1:
            color = "R"
        elif lst[i].color == 2:
            color = "G"
        else:
            color = "B"
        print(color + str(lst[i].number) + ", ", end="")
        if i % 8 == 7:
            print()
