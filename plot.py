import matplotlib.pyplot as plt

fig1, ax1 = plt.subplots()
ax1.set_title('Basic Plot')
ax1.boxplot([[1, 2, 3], [4, 5, 6]], labels=['abc', 'def'])

plt.show()
