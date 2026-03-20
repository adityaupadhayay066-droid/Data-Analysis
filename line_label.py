import matplotlib.pylab as plt
x = [1,2,3,4,5,6,7,8,9,10]
y1 = [2,5,3,8,2,11,15,6,8,3]
y2 = [6,7,2,12,1,14,12,10,4,2]
plt.plot(x,y1, label = "Line 1")
plt.plot(x,y2, label="Line 2")
plt.xlabel(" X axis ")
plt.ylabel(" Y axis ")
plt.title("Example Graph")
plt.plot(x,y1)
plt.legend()   # without legend the labels of line does not appear 
plt.show()
