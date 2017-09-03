import matplotlib.pylab as plt

plt.figure()
ax=plt.gca()
y=[1,2,3,4,5,4,3,2,1,1,1,1,1,1,1,1]
#plt.plot([10,10,14,14,10],[2,4,4,2,2],'r')
col_labels=['callnumber','ocount','odur']
row_labels=['row1','row2','row3']
table_vals=[[11,12,13],[21,22,23],[31,32,33]]
# the rectangle is where I want to place the table
the_table = plt.table(cellText=table_vals,
                      colWidths = [0.1]*3,
                  rowLabels=row_labels,
                  colLabels=col_labels,
                  loc='center right')
plt.text(12,3.4,'Table Title',size=8)

plt.plot(y)
plt.show()