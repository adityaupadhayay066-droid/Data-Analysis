import matplotlib.pyplot as plt 
name = ["Raj Kumar" , "Rohan Prasad","Prasati", "Kiran Tiwari"]
marks = [20,26,23,18]

# Show data in bargraph
plt.figure()  # use to create graph window 
plt.bar(name,marks , color = ["#336E20", "#0347AB" ,"#238E94", "#203A6E"])
plt.xlabel("Name of Student")
plt.ylabel("Marks of Student")
plt.title("Test marks analysis of Student")
plt.ylim(0,35)
plt.xlim()

#Show data in line 
plt.figure()
plt.plot(name, marks,label= "Marks Trend of students",marker ="^", color = "#0347AB", linestyle = "dotted", linewidth=2)
plt.legend()

# Show data in histograph 
plt.figure()
plt.hist(marks, bins=3, edgecolor='black',color = "green")
plt.show()
