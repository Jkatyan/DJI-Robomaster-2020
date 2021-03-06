import numpy as np
import statistics

class simple_train_one_num:
    #Initialization, the incoming parameters are data: training data set, training label set, training tolerance value,
    #coefficient step value, intercept step value
    def __init__(self, data, labels, toler, step_w, step_b):
        self.train_data = data #Training data set
        self.train_label = labels #Training label set
        self.toler = toler #Tolerance
        self.step_w = step_w #Coefficient step value
        self.step_b = step_b #Intercept step value
        self.num_kind = self.label_rank_num(self.train_label) #Calculate the number of types of numbers in the standard set
        self.train_data_dim = int(np.shape(self.train_data)[1])
        
        #According to the number of types of numbers, calculate the number of training matrices, and group them in
        #pairs. For example, if there are 1, 2, 3 numbers, that is, there are 3 types of numbers, then the training matrix includes 1, 2 matrix, 1, 3 matrix, 2 , 3 matrices total 3*(3-1)/2 = 3 matrices
        self.w = np.zeros((int(len(self.num_kind) * (len(self.num_kind) - 1) / 2), self.train_data_dim) )
        self.b = np.zeros((int(len(self.num_kind) * (len(self.num_kind) - 1) / 2), 1))
    #Calculate the types of numbers in the label set
    def label_rank_num(self, label):
        rank = []
        for i in label:
            flag = False
            # Traverse rank, find the number that is not there
            for j in rank:
                if j == i:
                   flag = True
            #Add number without
            if flag == False:
                 rank.append(i)
        return rank
    #Training the distinction between two numbers
    def train_learn_two_num(self, i, j):
        #Declare matrix and intercept
        w = np.zeros(np.shape(self.train_data)[1])
        b = 0
        #Used to judge whether all tags can be judged correctly
        train_flag = 1
        while train_flag != 0:
            train_flag = 0
            
            num = 0
            #Cycle all tags
            while num < len(self.train_label):
                y = 0
                #Judge whether it is the first number or the second number
                if self.train_label[num] == self.num_kind[i]:
                    y = 1
                elif self.train_label[num] == self.num_kind[j]:
                    y = -1
                
                if y != 0:
                    #Calculate model value
                    if (y * np.dot(w.T, self.train_data[num]) + b) <= self.toler:
                        w += self.step_w * self.train_data[num] * y
                        b += self.step_b * y
                        train_flag = 1
                num+=1
        return w,b
    def train_learn(self):
        num = 0
        num_len = len(self.num_kind)
        #Cycle all combinations of numbers
        i = 0
        while i < num_len:
            j = i+1
            while j < num_len:
                #Train two numbers
                self.w[num], self.b[num] = self.train_learn_two_num(i, j)
                j+=1
                num+=1
            i+=1
        
    def predict(self, test_data):
        ans = []
        num_len = len(self.num_kind)
        for i in test_data:
            #Calculate the combination of every two numbers, and then judge the final prediction result with the most number of occurrences
            test_ans = np.zeros(num_len)
            
            num_i = 0
            
            num = 0
            #Traverse all number combinations
            while num_i < num_len:
                num_j = num_i + 1
                while num_j < num_len:
                    #Calculate the judgment of two numbers, greater than 0 is the first number, less than the second number
                    if (np.dot(self.w[num].T, i) + self.b[num]) > 0:
                        #Count votes to the corresponding number
                        test_ans[num_i]+=1
                    else:
                        #Count votes to the corresponding number
                        test_ans[num_j]+=1
                    num_j+=1
                    num+=1
                num_i+=1
            #Count all the votes to see which number is the most
            num_i = 0
            ans_max = -1
            ans_i = -1
            while num_i < num_len:
                if ans_max < test_ans[num_i]:
                    ans_max = test_ans[num_i]
                    ans_i = num_i
                num_i+=1
            ans.append(self.num_kind[ans_i])
        ans = np.array(ans)
        return ans


if __name__ == "__main__":
    import sys

    sys.path.append("../read_picture/")
    import read_picture

    # imports sets of images and their correct answers
    train_image, train_label = read_picture.read_image_data('../mnist_data/train-images.idx3-ubyte',
                                                            '../mnist_data/train-labels.idx1-ubyte')

    # reformats the train image into a matrix of 60000x784
    train_image_vector = np.reshape(train_image, (60000, 784))
    # creates a simple_train_one_num object, and gives it the first 5000 images
    simple_trainer = []
    for i in range(25):
        first_num = 2000 * i
        last_num = 2000 * (1 + i)
        simple_trainer.append(
            simple_train_one_num(train_image_vector[first_num:last_num], train_label[first_num:last_num], 10, 0.1,
                                 2.55))
        simple_trainer[i].train_learn()
        print("trainer ", i, " is trained")

    # Construction test set
    # creates a new variable, and gives it the next 100 images after the training set
    test_image_vector = train_image_vector[50000:60000]
    # creates a new set with the correct answers
    test_ans = train_label[50000:60000]
    # Calculate forecast
    # guesses the numbers
    pre_ans = []
    for i in range(25):
        pre_ans.append(simple_trainer[i].predict(test_image_vector))
        print("trainer ", i, " has learned")

    reset = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    votes = reset
    ans = []
    max = 0
    pos = 0
    for k in range(len(test_image_vector)):
        for i in range(25):
            votes[pre_ans[i][k]] += 1
        for j in range(10):
            if max < votes[j]:
                max = votes[j]
                pos = j
        ans.append(pos)
        max = 0
        pos = 0
        # print(max)
        # print(pos)
        # print(votes)
        votes = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
        # print(votes)
    i = 0
    correct = 0
    while i < len(test_image_vector):
        if ans[i] == test_ans[i]:
            correct += 1
        i += 1
    print("correct is ", (correct))
