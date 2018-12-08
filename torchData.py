import torch
import torch.utils.data
import torch.nn.functional as F
import torch.optim as lfunc
from sklearn.utils import shuffle
import matplotlib.pyplot as plt
import numpy as np
import cv2

class Cnn(torch.nn.Module):
    def __init__(self):
        super(Cnn, self).__init__()
        self.conv1 = torch.nn.Conv2d(3, 6, 5)
        self.pool = torch.nn.MaxPool2d(2, 2)
        self.conv2 = torch.nn.Conv2d(6, 16, 5)
        self.fc1 = torch.nn.Linear(16 * 5 * 5, 120)
        self.fc2 = torch.nn.Linear(120, 84)
        self.fc3 = torch.nn.Linear(84, 10)

    def forward(self, x):
        x = self.pool(F.relu(self.conv1(x)))
        x = self.pool(F.relu(self.conv2(x)))
        x = x.view(-1, 16 * 5 * 5)
        x = F.relu(self.fc1(x))
        x = F.relu(self.fc2(x))
        x = self.fc3(x)
        return x


class Train():
    def __init__(self, trainloader,testloader):
        self.net = Cnn()
        self.criterion = torch.nn.CrossEntropyLoss()
        self.optimizer = lfunc.SGD(self.net.parameters(), lr=0.001, momentum=0.9)
        self.training(trainloader)
        self.test(testloader)

    def training(self, trainloader):
        for epoch in range(2):  # loop over the dataset multiple times

            running_loss = 0.0
            for i, data in enumerate(trainloader, 0):
                # get the inputs
                inputs, labels = data

                # zero the parameter gradients
                self.optimizer.zero_grad()
                # forward + backward + optimize
                outputs = self.net(inputs.float())
                loss = self.criterion(outputs, labels)
                loss.backward()
                self.optimizer.step()

                # print statistics
                running_loss += loss.item()
                print('[%d, %5d] loss: %.3f' %
                      (epoch + 1, i + 1, running_loss / 500))
                running_loss = 0.0

        print('Finished Training')

    def test(self, testloader):
        correct = 0
        total = 0
        with torch.no_grad():
            for data in testloader:
                images, labels = data
                outputs = self.net(images.float())
                _, predicted = torch.max(outputs.data, 1)
                total += labels.size(0)
                correct += (predicted == labels).sum().item()

        print('Accuracy of the network on the test images: %d %%' % (
                100 * correct / total))



class PreProcessCnn():

    def imshow(self, img):
        img = img
        npimg = img.numpy()
        plt.imshow(npimg)
        plt.show()

    def __init__(self, data):
        data = shuffle(data.all_data)
        labels = np.zeros(500, dtype=int)
        a = []
        i = 0
        for index, row in data.iterrows():
            genre = row['genre']

            if (genre == 'electronic'):
                labels[i] = 0

            if (genre == 'indie'):
                labels[i] = 1

            if (genre == 'pop'):
                labels[i] = 2

            if (genre == 'metal'):
                labels[i] = 3

            if (genre == 'alternative rock'):
                labels[i] = 4

            if (genre == 'classic rock'):
                labels[i] = 5

            if (genre == 'jazz'):
                labels[i] = 6

            if (genre == 'folk'):
                labels[i] = 7

            if (genre == 'Hip-Hop'):
                labels[i] = 8

            if (genre == 'Classical'):
                labels[i] = 9

            img = (row['image'])
            img2 = cv2.resize(img, (32, 32))
            tp = np.transpose(img2)
            a.append(tp)



            i = i + 1

        a = np.array(a)
        a = torch.from_numpy(a)
        labels = torch.from_numpy(labels)
        train_data = torch.utils.data.TensorDataset(a, labels)
        trainloader = torch.utils.data.DataLoader(train_data, batch_size=400, shuffle=True)
        testloader = torch.utils.data.DataLoader(train_data, batch_size=100, shuffle=True)
        trainData = Train(trainloader,testloader)