import matplotlib.pylab as pt
x = [1,2,3,4,5,6,7,8,9,10]
y1 = [2,5,3,8,2,11,15,6,8,3]
y2 = [6,7,2,12,1,14,12,10,4,2]
fig, (ax1, ax2) = plt.subplots(2,1)
fig.suptitle("Vertically Plotted")
ax1.plot(x,y1,label = "Line 1", color = "Red", marker = ">", linestyle ="dashdot", linewidth = 2, markersize =12)
ax2.plot(x,y2,label = "Line 1", color = "Blue", marker = "o",linestyle ="solid", linewidth = 2, markersize =12 )
plt.show()