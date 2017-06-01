import networkx as nx
import matplotlib.pyplot as plt
from matplotlib.patches import FancyArrowPatch, Circle
import numpy as np


def connect(l1, l2, arr):
    ret = []
    for e in arr:
        ret.append(((l1, e[0]), (l2, e[1])))
    return ret


# TODO Shape for recurrent
def weights(w=1):
    pos = {}
    labels = {}
    init = ['s']
    offset = []

    G = nx.DiGraph()
    G.add_node('s')
    G.add_node('d')
    G.add_nodes_from([i for i in range(w)])
    G.add_edges_from([('s', i) for i in range(w)])
    G.add_edges_from([(i, 'd') for i in range(w)])
    G.add_edge('d', 'd')
    pos['s'] = (0, (w - 1) / 2)
    for i in range(w):
        pos[i] = (1, i)
    pos['d'] = (2, (w - 1) / 2)

    for n in G.nodes():
        labels[n] = n

    return G, pos, labels, init, offset


def two_bit_setup(inp=[False, False]):
    G = nx.DiGraph()

    layer_size = [3, 6, 4, 1]
    Nodes = []
    offset = []

    for i, l in enumerate(layer_size):
        Nodes.append([(i, t) for t in range(l)])
        G.add_nodes_from([(i, t) for t in range(l)])

    init = [(0, 0)]
    for i, e in enumerate(inp):
        if e:
            init.append((0, i + 1))

    pos = {}

    for l in Nodes:
        for e in l:
            pos[e] = e

    Edges = []
    Edges.append(connect(0, 1, [(0, 0), (1, 1), (1, 2), (1, 3), (2, 3), (2, 4), (2, 5)]))
    Edges.append(connect(1, 2, [(0, 0), (1, 1), (2, 1), (3, 2), (4, 3), (5, 3)]))

    labels = {(0, 0): '1', (0, 1): 'a', (0, 2): 'b', (2, 0): '!a+!b', (2, 1): 'a+!b', (2, 2): 'a+b', (2, 3): '!a+b'}

    return G, pos, labels, Edges, init, offset


def shoot_at(t=0):
    G = nx.DiGraph()
    offset = []
    labels = {}
    pos = {}
    G.add_node('loop')
    G.add_edge('loop', 'loop')
    pos['loop'] = (t - 1, 1)
    for n in range(t):
        G.add_node(n)
        pos[n] = (n, 0)
    for n in range(1, t):
        G.add_edge(n - 1, n)
    init = ['loop', 0]
    for n in G.nodes():
        labels[n] = n

    return G, pos, labels, init, offset


def twoTM(inp=[0, 1]):
    G = nx.DiGraph()


def even_odd_FSM(inp=[0, 1, 0, 1]):
    G = nx.DiGraph()
    offset = []
    init = [0, '0a', '1s0', '1s1']
    pos = {}
    labels = {}

    G.add_nodes_from(
        ['00', '01', '0a', '0s0', '0s1', '10', '11', '1a', '1s0', '1s1', 'ao0', 'ao1', 'ao2', 'ae0', 'ae1', 'ae2'])
    WTAs = [['00', '01', '0a', '0s0', '0s1', 'ao0', 'ao1', 'ao2'],
            ['10', '11', '1a', '1s0', '1s1', 'ae0', 'ae1', 'ae2']]

    pos['00'] = (0, -1)
    pos['01'] = (1, -1)
    pos['0a'] = (1, -3)
    pos['0s0'] = (0.5, -1.8)
    pos['0s1'] = (0.5, -2.2)

    pos['ao0'] = (1.2, -1.5)
    pos['ao1'] = (1.2, -1.75)
    pos['ao2'] = (1.2, -2)

    pos['ae0'] = (3.8, -1.5)
    pos['ae1'] = (3.8, -1.75)
    pos['ae2'] = (3.8, -2)

    pos['10'] = (4, -1)
    pos['11'] = (5, -1)
    pos['1a'] = (4, -3)
    pos['1s0'] = (4.5, -1.8)
    pos['1s1'] = (4.5, -2.2)

    WTA = []
    for i in range(len(inp)):
        if i != 0:
            G.add_edge('w' + str(i - 1) + '1', i)
        j = 0
        for e in [i, 'w' + str(i) + '0', 'w' + str(i) + '1']:
            WTA.append(e)
            G.add_node(e)  # Add waiting nodes
            pos[e] = (i, j)
            j += 1
        G.add_edges_from([(i, '0' + str(inp[i])), (i, '1' + str(inp[i]))])  # Add edge from input to unit
        G.add_edges_from([(i, 'w' + str(i) + '0'),
                          ('w' + str(i) + '0', 'w' + str(i) + '1')])  # Add edge from input to waiting

    G.add_edge('w' + str(len(inp) - 1) + '1', 'w' + str(len(inp) - 1) + '1')

    WTAs.append(WTA)
    G.add_edges_from([('0a', '0a'), ('0s0', '0s0'), ('0s1', '0s1'), ('0s0', '0s1'), ('0s1', '0s0')])  # recurrent edges
    G.add_edges_from([('1a', '1a'), ('1s0', '1s0'), ('1s1', '1s1'), ('1s0', '1s1'), ('1s1', '1s0')])  # recurrent
    G.add_edges_from([('01', '0s0'), ('01', '0s1'), ('11', '1s0'), ('11', '1s1')])  # stop current State
    G.add_edges_from([('01', 'ao0'), ('01', 'ao1'), ('01', 'ao2'),
                      ('11', 'ae0'), ('11', 'ae1'), ('11', 'ae2'),
                      ('ao0', '1a'), ('ao1', '1a'), ('ao2', '1a'),
                      ('ae0', '0a'), ('ae1', '0a'), ('ae2', '0a')])  # between WTA edges

    for n in G.nodes():
        labels[n] = n

    for n in range(len(inp)):
        labels[n] = inp[n]

    return G, WTAs, pos, labels, init, offset


def iterate(G, WTAs, pos, labels, init, offset=[], node_size=1000):
    node_color_map = {}
    for WTA in WTAs:
        # colors
        random_color = (np.random.rand() / 2 + 0.5, np.random.rand() / 2 + 0.5, np.random.rand() / 2 + 0.5)
        for e in WTA:
            node_color_map[e] = random_color

    node_color = []
    for u in G.nodes():
        node_color.append(node_color_map[u])

    t = 0
    active = init
    mngr = plt.get_current_fig_manager()
    mngr.window.setGeometry(0, 0, 1920, 1080)
    linewidths = [5 if n in active else 1 for n in G.nodes()]

    if pos == {}:
        nx.draw(G, labels=labels, node_color=node_color, linewidths=linewidths, font_size=16, node_size=node_size)
    else:
        nx.draw(G, pos=pos, labels=labels, node_color=node_color, linewidths=linewidths, font_size=16,
                node_size=node_size)
    plt.suptitle('t = ' + str(t))
    plt.show()

    while (True):
        t = t + 1
        succ = [G.successors(e) for e in active]
        active = []

        # serialize array
        temp = []
        for a in succ:
            for e in a:
                temp.append(e)
        succ = temp
        for WTA in WTAs:
            graph_dict = {}
            # convert array to dict
            for s in G.nodes():
                graph_dict[s] = 0
            for s in succ:
                if s in offset:
                    graph_dict[s] = graph_dict[s] + 1
                if s in WTA:
                    graph_dict[s] = graph_dict[s] + 1
            WTA_dict = {}
            for e in WTA:
                WTA_dict[e] = graph_dict[e]
            # maximum of this WTA
            maximum = WTA_dict[max(WTA_dict, key=WTA_dict.get)]

            # new active nodes of this WTA
            new_active = []
            for key, value in WTA_dict.items():
                if value == maximum:
                    new_active.append(key)
            active.append(new_active)

        temp = []
        for wta in active:
            for u in wta:
                temp.append(u)
        active = temp

        mngr = plt.get_current_fig_manager()
        mngr.window.setGeometry(0, 0, 1920, 1080)
        linewidths = [5 if n in active else 1 for n in G.nodes()]
        if pos == {}:
            nx.draw(G, labels=labels, node_color=node_color, linewidths=linewidths, font_size=16, node_size=node_size,
                    arrowstyle='-|>')
        else:
            nx.draw(G, pos=pos, labels=labels, node_color=node_color, linewidths=linewidths, font_size=16,
                    node_size=node_size)
        plt.suptitle('t = ' + str(t))
        plt.show()


def Nand(inp=[False, False]):
    G, pos, labels, Edges, init, offset = two_bit_setup(inp)

    labels[(3, 0)] = "Nand"

    Edges.append(connect(2, 3, [(0, 0), (1, 0), (3, 0)]))
    Edges.append([((3, 0), (3, 0))])
    Edges.append([((2, 2), (2, 2))])

    for e in Edges:
        G.add_edges_from(e)

    iterate(G, [G.nodes()], pos, labels, init, offset, 2000)


def Nor(inp=[False, False]):
    G, pos, labels, Edges, init, offset = two_bit_setup(inp)

    labels[(3, 0)] = "Nor"

    Edges.append(connect(2, 3, [(0, 0)]))
    Edges.append([((3, 0), (3, 0))])
    Edges.append([((2, 1), (2, 1))])
    Edges.append([((2, 2), (2, 2))])
    Edges.append([((2, 3), (2, 3))])

    for e in Edges:
        G.add_edges_from(e)

    iterate(G, [G.nodes()], pos, labels, init, offset, 2000)


def timer(t=0):
    # G, pos, labels, init, offset
    G, pos, labels, init, offset = shoot_at(t)

    iterate(G, [G.nodes()], pos, labels, init,  2000/(t/5))


def edge_weight(w=1):
    G, pos, labels, init, offset = weights(w)
    iterate(G, [G.nodes()], pos, labels, init)


def FSM(inp=[0, 1, 0, 1]):
    # G, WTAs, pos, labels, init, offset
    G, WTAs, pos, labels, init, offset = even_odd_FSM(inp)

    iterate(G, WTAs, pos, labels, init, offset)


# FSM([1, 1, 0, 1, 0])
# Nand([True, True])
# Nor([True,False])
edge_weight(3)
