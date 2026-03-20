import matplotlib.pyplot as plt
x = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
y1 = [2, 5, 3, 8, 6, 9, 7, 10, 8, 12] 
y2 = [1, 4, 2, 6, 5, 7, 6, 8, 7, 9]
fig, (ax1, ax2) = plt.subplots(1,2)
fig.suptitle("Horizontally Plotted")
ax1.plot(x,y1,label = "Line 1", color = "Red", marker = ">", linestyle ="dashdot", linewidth = 2, markersize =12)
ax2.plot(x,y2,label = "Line 1", color = "Blue", marker = "o",linestyle ="solid", linewidth = 2, markersize =12 )
plt.show()