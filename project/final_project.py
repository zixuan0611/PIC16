import matplotlib.pyplot as plt
import matplotlib.colors as colors
import matplotlib.cm as cmx
import networkx as nx
import sys
from collections import Counter
import re

#Global variables
title_list = []
author_list = []
reference_list = []
num = 0

#data_clean function
def dataclean(lines):
    global num
    global title_list
    global author_list
    global reference_list

    #total number of the data
    num = int(lines[0])
    i = 0

    #for every book's data
    for line in lines:
        if line != '':
            #extract title
            if line[0] == "#" and line[1] == "*":
                title_list.append(line[2:])
                author_list.append([])
                reference_list.append([])
                i += 1
            #extract author names
            elif line[0] == "#" and line[1] == "@":
                if len(line) > 2:
                    author_list[i - 1].append(line[2:])
            #extract reference list
            elif line[0] == "#" and line[1] == "%":
                reference_list[i - 1].append(line[2:])
    # print(author_list)
    # print(reference_list)
    # print(len(reference_list))

"""
In this function, we try to sort the data by reference list, the list of papers a paper referenced to,
we output two results: the paper with the highest referenced rate: introduction to algorithm;
and the top 5 referenced papers and three relative papers.
"""
def referenceGraph():
    global num
    global reference_list
    refg_list = []
    nodes = []

    #we sort the reference list to a list of tuples whose first element is the paper
    # and second is the papers this paper referencing to
    for i in range(num):
        for n in range(len(reference_list[i])):
            refg_list.append((str(i), reference_list[i][n]))
    # print (refg_list)
    for i in range(num):
        nodes.append(str(i))
    # print len(refg_list)
    # print (nodes)

    #draw graph
    G = nx.DiGraph()
    G.add_nodes_from(nodes)
    G.add_edges_from(refg_list)

    #using pagerank function to determine the importance of these papers
    pr = nx.pagerank(G, alpha=0.95)
    # print (pr)

    #w_list is the sorted pagerank values
    w_list = pr.values()
    w_list = sorted(w_list, reverse=True)
    neww_list = []
    neww_nodes = []
    # print(w_list)

    # for top 1 books with highest referencing rate
    # we added all the papers referencing it
    for i in range(1):
        neww_list.append(w_list[i])
    # print len(neww_list)
    for i in range(len(neww_list)):
        for key in pr:
            if pr[key] == neww_list[i]:
                neww_nodes.append(key)
    neww_nodesc = neww_nodes[:]
    #print len(neww_nodes)



    #neww_nodes:list of the nodes of largest pagerank node
    for j in range(len(neww_nodesc)):
        for k in range(len(refg_list)):
            if refg_list[k][1] == neww_nodesc[j]:
                neww_nodes.append(refg_list[k][0])
    #print neww_nodes
    #print(len(neww_nodes))

    # nodes_list1 = list of tuples (pagerankvalue, nodesnumber)
    nodes_list1 = []
    for i in neww_nodes:
        nodes_list1.append((pr[i], i))
    def getKey(t):
        return t[0]

    #sort the nodes_list1 function
    nodes_list1 = sorted(nodes_list1, key=getKey, reverse=True)
    #print nodes_list1
    nodes_list = []
    for i in nodes_list1:
        nodes_list.append(i[1])
    #nodes_list = nodes_list[0:200]
    for i in nodes_list[1:31]:
        print title_list[int(i)]


    H = G.subgraph(nodes_list)
    pos = nx.spring_layout(H)
    nodes = list(H.nodes())

    #adjust the size of nodes
    nodes_size = [450]+[250]*30+[150]*50+[0.05]*(len(nodes_list)-30-50)
    #print len(nodes_size)

    #adjust the color of nodes
    rei = int(neww_nodes[0])
    val_map = {neww_nodes[0]: 1} #, nodes[1]: 2, nodes[2]: 3, nodes[3]: 4, nodes[4]: 5}
    # I had this list for the name corresponding t the color but different from the node name
    ColorLegend = {title_list[rei]: 1} #, new_titles[1]: 2, new_titles[2]: 3, new_titles[3]: 4, new_titles[4]: 5}

    # Color mapping
    #jet = plt.get_cmap('jet')
    #cNorm = colors.Normalize(vmin=0, vmax=max(values))
    #scalarMap = cmx.ScalarMappable(norm=cNorm, cmap=jet)
    nodes_color = [0.8] + [0.7] * 30 + [0.65] * 50 + [0.6] * (len(nodes_list) - 1 - 30 - 50)


    # Using a figure to use it as a parameter when calling nx.draw_networkx
    f = plt.figure(1)
    ax = f.add_subplot(1, 1, 1)
    for label in ColorLegend:
        ax.plot([0], [0], color="navy", label=label)


    nx.draw_networkx(H, pos, edge_color="#A9A9A9", width=0.02, nodelist = nodes_list,node_size =nodes_size, cmap= plt.get_cmap('Blues'), node_color=nodes_color, arrows= False, with_labels=False, ax=ax, alpha=0.8)

    #print H.nodes()

    # Setting it to how it was looking before.
    plt.axis('off')
    f.set_facecolor('w')

    plt.legend(loc=0, prop={'size': 8}, bbox_to_anchor=(0.5, 1.05))

    f.tight_layout()
    plt.show()


    # then begin our process to output top 5 pagerank values nodes with their top 3 pagerank value nodes
    # for top 5 books with highest referencing rate
    paper_list = []
    for i in range(5):
        paper_list.append(w_list[i])
    paper_nodes = []
    for i in range(len(paper_list)):
        for key in pr:
            if pr[key] == paper_list[i]:
                paper_nodes.append(key)
    paper_nodes = paper_nodes[0:5]
    npaper_nodes = paper_nodes[:]
    #print len(npaper_nodes) #5
    #print paper_nodes


    # paper_nodes:list of the 3 nodes of top 5 pagerank nodes
    x = int(num/100)
    #print x

    for j in range(len(npaper_nodes)):
        furuya = 0
        temp = []
        w_list2 = w_list[0:x]
        for k in range(len(refg_list)):
            if refg_list[k][1] == npaper_nodes[j]:
                temp.append(refg_list[k][0])
        i = 0
        while i < len(temp):
            s = temp[i]
            if pr[s] in (w_list2):
                paper_nodes.append(s)
                #print s
                furuya += 1
            if furuya == 3:
                break
            i+=1


    #print(len(paper_nodes))
    #print paper_nodes

    # list of tuples (pagerankvalue, nodesnumber)
    nodes_list2 = []
    for i in paper_nodes:
        nodes_list2.append((pr[i], i))


    #sort the nodes list as what we did before
    nodes_list2 = sorted(nodes_list2, key=getKey, reverse=True)
    #print nodes_list2
    pnodes_list = []
    for i in nodes_list2:
        pnodes_list.append(i[1])

    S = G.subgraph(pnodes_list)
    pos = nx.random_layout(S)

    nodes_size = [800, 700, 600, 500, 400] + [250] * (len(pnodes_list) - 5)
    # print len(nodes_size)

    rei = int(npaper_nodes[0])
    ichi = int(npaper_nodes[1])
    ni = int(npaper_nodes[2])
    san = int(npaper_nodes[3])
    shi = int(npaper_nodes[4])
    # , nodes[1]: 2, nodes[2]: 3, nodes[3]: 4, nodes[4]: 5}
    # I had this list for the name corresponding t the color but different from the node name
    ColorLegend = {title_list[rei]: 1, title_list[ichi]: 2, title_list[ni]:3, title_list[san]:4, title_list[shi]:5}


    nodes_color = ["salmon"] * 5 + ["thistle"] * (len(pnodes_list) - 5)

    # Using a figure to use it as a parameter when calling nx.draw_networkx
    f = plt.figure(1)
    ax = f.add_subplot(1, 1, 1)
    for label in ColorLegend:
        ax.plot([0], [0], color="salmon", label=label)

    # Just fixed the color map
    nx.draw_networkx(S, pos, edge_color="rosybrown", width=0.1, nodelist=pnodes_list, node_size=nodes_size,
                     node_color=nodes_color, with_labels=True, font_size=6, ax=ax,
                     alpha=0.8)
    # nx.draw_networkx(H, pos[0], cmap=jet, vmin=0, vmax=max(values), node_size=0.1, node_color=values, with_labels=True,
    # ax=ax)
    # print H.nodes()

    # Setting it to how it was looking before.
    plt.axis('off')
    f.set_facecolor('w')

    plt.legend(loc=0, prop={'size': 5}, bbox_to_anchor=(0.5, 1.05))

    f.tight_layout()
    plt.show()



#this function returns the authors in the dataset that have most papers published
#we return the top 5 authors who publish the most amount of papers
#we also find their co-authors who are rated top 0.5% most famous publishers in the dataset
#we draw connection between them to see if they collaborate with each other
def author_sort():
    global author_list

    # a_list is the list of authors name (repetitive)
    # a_edges is the list of connection they have
    a_list = []
    a_edges = []

    A = nx.Graph()
    for a_for_book in author_list:
        if (len(a_for_book) != 0):
            #here we seperate the author if one book has several co-authors
            if re.match(r'.+[,].+', a_for_book[0]):
                a_for_book = a_for_book[0].split(",")
            #create author lists and edges lists
            for i in range(len(a_for_book)):
                a_list.append(a_for_book[i])
                if len(a_for_book) > 1:
                    for j in range(i+1, len(a_for_book)):
                        a_edges.append((a_for_book[i], a_for_book[j]))


    #print len(a_list)
    #print len(a_edges)

    # Try to get the first five authors that has been referenced as co-authors the most times
    # sort the first 0.5% authors that has most works
    com_a = Counter(a_list).most_common(len(Counter(a_list))/2000)
    com_a_100 = []
    for com in com_a:
        com_a_100.append(com[0])

    #we find that the first several elements are suffix but not author names
    #so we extract the most possible authors
    com_a_5 = com_a_100[4:9]
    com_a_nodes = com_a_5[:]
    com_a_edges =[]

    # visit the nodes list to find the authors that have connections with the top 5 authors
    # make sure these authors are in the first 0.5% rated authors in the whole author list
    for a in com_a_5:
        for n in a_edges:
            if (a == n[0] and n[1] in com_a_100 and n[1] not in com_a_nodes):
                com_a_nodes.append(n[1])
            elif (com_a == n[1] and n[0] in com_a_100 and n[0] not in com_a_nodes):
                com_a_nodes.append(n[0])

    #print com_a_nodes
    #print len(com_a_nodes)

    A.add_nodes_from(com_a_nodes)
    for b_edges in a_edges:
        if (b_edges[0] in  com_a_nodes and b_edges[1] in com_a_nodes):
            #print b_edges
            com_a_edges.append(b_edges)

    #print com_a_edges
    #print len(com_a_edges)
    pos = nx.random_layout(A)

    A.add_edges_from(com_a_edges)

    nodes_size = [500]*5 + [300]*(len(com_a_nodes)-5)
    nodes_color = ['SeaGreen']*5 + ['DarkSeaGreen']*(len(com_a_nodes)-5)

    #output as what we did before
    colorlegend = {com_a_nodes[0]: 1, com_a_nodes[1]: 2, com_a_nodes[2]: 3, com_a_nodes[3]: 4, com_a_nodes[4]: 5}
    f = plt.figure(1)
    ax = f.add_subplot(1, 1, 1)
    for label in colorlegend:
        ax.plot([0], [0], color="SeaGreen", label=label)
    nx.draw_networkx(A, pos, width=0.3, font_size=5, node_size = nodes_size, node_color=nodes_color, edge_color='Olive', alpha=0.8)

    plt.axis('off')
    plt.legend(loc=0, prop={'size': 5}, bbox_to_anchor=(0.5, 1.05))
    plt.show()


if __name__ == "__main__":
    try:
        infile = open("outputacm.txt", "r")
    except:
        sys.stderr.write("File Open Error\n")
        exit(1)
    # print sys.path

    text = infile.read().split('\n')

    dataclean(text)
    referenceGraph()
    author_sort()
    # print (text)
