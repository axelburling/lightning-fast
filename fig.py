import matplotlib.pyplot as plt
import random


def generate_random_data():
    data = []
    for i in range(10):
        data.append(random.randint(0, 100))
    return data


data1 = generate_random_data()

data2 = generate_random_data()

plt.figure(100)
plt.plot(data1, label="Data 1")
plt.figure(101)
plt.plot(data2, label="Data 2")

plt.show()    
    
    

