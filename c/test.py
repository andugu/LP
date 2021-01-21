import sys
import copy
from antlr4 import *
from EnquestesLexer import EnquestesLexer
from EnquestesParser import EnquestesParser
from antlr4.InputStream import InputStream
from EnquestesVisitor import EnquestesVisitor
import matplotlib.pyplot as plt
import networkx as nx
import pickle as pickle

if len(sys.argv) > 1:
    file = open(sys.argv[1], encoding='utf8')
    input_stream = InputStream(file.read())
    file.close()
else:
    input_stream = InputStream(input('? '))

lexer = EnquestesLexer(input_stream)
token_stream = CommonTokenStream(lexer)
parser = EnquestesParser(token_stream)
tree = parser.root()
visitor = EnquestesVisitor()
l = visitor.visit(tree)

# Creem el graf
G = nx.DiGraph()
# Index per recorre la llist
i = 0
# Guardem la sequencia inicial
Header = []
# Guarda la equivalencia entre els ids
# (LinkID, PreguntaID)
ids = []
# Nodes i els seus noms
node_list = []
node_labels = {}
# Edges blaus PreguntaID-RespostaID
blue_edge_list = []
blue_edge_labels = {}
# Edges verds Alternativa
green_edge_list = []
green_edge_labels = {}
# Edges sequencia inicial
black_edge_list = []

# Guardem la estructura principal
while l[i] != "LINKS":
    Header.append(l[i])
    i += 1

i += 1

# Creem els nodes E i END
G.add_node(Header[0])
G.add_node(Header[len(Header)-1])
node_list.append(Header[0])
node_list.append(Header[len(Header)-1])
node_labels[Header[0]] = Header[0]
node_labels[Header[len(Header)-1]] = Header[len(Header)-1]

# Agreguem totes les preguntes i respostes al grafic
# I els labels del graf
while l[i] != "ALTERNATIVA":
    # Guardem els nodes
    G.add_node(l[i+1])
    G.add_node(l[i+2])
    node_list.append(l[i+1])
    node_list.append(l[i+2])
    node_labels[l[i+1]] = l[i+1]
    node_labels[l[i+2]] = l[i+2]

# Edges blaus PreguntaID-RespostaID
    G.add_edge(l[i+1], l[i+2], color='blue', label=l[i])
    blue_edge_list += [(l[i+1], l[i+2])]
    blue_edge_labels[(l[i+1], l[i+2])] = l[i]

# Guardem la traduccio de LinkID-PreguntaID-RespostaID
    ids.append((l[i], l[i+1], l[i+1]))

# Reemplacem els LinkID pels PreguntaID a la sequencia inicial
    for r in range(1, len(Header)-1):
        if Header[r] == l[i]:
            Header[r] = l[i+1]
    i += 3

j = 1
while j < len(Header):
    # Edge de sequencia inicial
    G.add_edge(Header[j-1], Header[j])
    black_edge_list += [(Header[j-1], Header[j])]
    j += 1

identificador_actual = ""
while l[i] != "PREGUNTA":
    # Guarda el id actual
    if l[i] == "ALTERNATIVA":
        identificador_actual = l[i+1]
        for r in ids:
            if r[0] == identificador_actual:
                identificador_actual = r[1]
        i += 2
    # Posa un edge entre id actual
    else:
        tmp = ""
        for r in ids:
            if r[0] == l[i+1]:
                tmp = r[1]
        G.add_edge(identificador_actual, tmp, color='green', label=l[i])
        green_edge_list += [(identificador_actual, tmp)]
        green_edge_labels[(identificador_actual, tmp)] = l[i]
        i += 2

# Guardem el contingut de les preguntes i les respostes
# al graf tambe com a atributs
while l[i] != "RESPOSTA":
    G.nodes[l[i+1]]['content'] = l[i+2]
    i += 3

while i < len(l):
    if l[i] == "RESPOSTA":
        respID = l[i+1]
        G.nodes[respID]['content'] = []
        i += 2
    else:
        G.nodes[respID]['content'] += [[l[i][0], l[i][1], 0]]
        i += 1


# Creem un file object
file = open('graf', 'wb')
# Guarda el graf amb els seus nodes i edges amb atributs en un pickle
pickle.dump(G, file)
file.close()

# Creem un layout
pos = nx.circular_layout(G)

# Pintem els nodes i els seus noms
nx.draw_networkx_nodes(G, pos, nodelist=node_list)
nx.draw_networkx_labels(G, pos, node_labels)

# Pintem els edges blaus
nx.draw_networkx_edges(G, pos, edgelist=blue_edge_list, edge_color='b')
nx.draw_networkx_edge_labels(G, pos, edge_labels=blue_edge_labels,
                             font_color='b')

# Pintem els edge verds
nx.draw_networkx_edges(G, pos, edgelist=green_edge_list, edge_color='g')
nx.draw_networkx_edge_labels(G, pos, edge_labels=green_edge_labels,
                             font_color='g')

# Pintem els edge negres
nx.draw_networkx_edges(G, pos, edgelist=black_edge_list)

plt.show()
