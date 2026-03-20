import matplotlib.pyplot as plt
x = [1,2,3,4,5,6,7,8,9,10]
y1 = [2,5,3,8,2,11,15,6,8,3]
y2 = [6,7,2,12,1,14,12,10,4,2]
fig, ax = plt.subplots()
ax.plot(x,y1,label = "Line 1", color = "Red", marker = "o", linestyle ="dashdot", linewidth = 2, markersize =12)
ax.plot(x,y2,label = "Line 1", color = "Blue", marker = "^",linestyle ="solid", linewidth = 4, markersize =12, alpha=0.56 )
ax.set_xlabel("X axis")
ax.set_ylabel("Y axis")
ax.set_title("Simple example Graph ")
ax.legend()
plt.show()