# import module
import matplotlib.pyplot as plt
import numpy as np

# data set source: http://vlado.fmf.uni-lj.si/pub/networks/data/soc/Tina/Tina.htm
# Student Government of the University of Ljubljana / 1992

# helpler function
def network_plot_circle(N):
    n = len(N)
    x = [np.cos(2*np.pi*i/n) for i in range(n)]
    y = [np.sin(2*np.pi*i/n) for i in range(n)]
    for i in range(n):
        for j in range(i):
            if N[i][j] == 1:
                plt.plot([x[i], x[j]], [y[i], y[j]], 'c')

    # an explanation of the colored dots in the output graph:
    # in the data set, there are 8 ministers and 3 advisers in the Student Government
    # in order to show the communication interactions between two positions intuitively
    # we use red color to represent ministers and blue color to represent advisers
    # we also make a note for every node in the output graph to make it clearer

    plt.plot(x[0:8], y[0:8], 'ro')
    plt.plot(x[8:11], y[8:11], 'bo')
    plt.text(x[0], y[0], "minister1")
    plt.text(x[1], y[1], "minister2")
    plt.text(x[2], y[2], "minister3")
    plt.text(x[3], y[3], "minister4")
    plt.text(x[4], y[4], "minister5")
    plt.text(x[5], y[5], "minister6")
    plt.text(x[6], y[6], "minister7")
    plt.text(x[7], y[7], "minister8")
    plt.text(x[8], y[8], "adviser1")
    plt.text(x[9], y[9], "adviser2")
    plt.text(x[10], y[10], "adviser3")
    #plt.plot(x, y, 'ro')
    plt.title("Communication Interactions among 11 members of the Student Government")
    plt.show()

# read the data from the data set
ask = open("AskCal.txt").read()
pairs = [s.split('\t') for s in ask.splitlines()]
pairs = [[int(a) for a in b]for b in pairs]
m = max(max(b for b in pairs))
adjMatrix = [[0]*m for _ in range(m)]
for p in pairs:
    adjMatrix[p[0]-1][p[1]-1] = 1
    adjMatrix[p[1]-1][p[0]-1] = 1

network_plot_circle(adjMatrix)

