from collections import defaultdict
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

class Grafo():
  def __init__(self):
    self.vertices = 0
    self.arestas = 0 
    self.adj_list =  defaultdict(list)
    self.type = ''

  #a. O número de vértices do grafo (ordem);
  def n_vertices(self):
    return self.vertices

  #b. O número de arestas do grafo (tamanho);
  def n_arestas(self):
    return self.arestas
  
  def adiciona_vertice(self, nome):
    
    if nome not in self.adj_list:
      self.adj_list[nome] = []
      self.vertices += 1
    else:
      print("Um node com esse nome já existe!")

  def remove_vertice(self, node): # remove o vértice u

    lista = self.adj_list.keys()

    if node in lista:
      #desconecta todas as arestas que chegam até ele
      for elem in self.adj_list.keys():
        if self.tem_aresta(elem, node):
          self.remove_aresta(elem, node)
          
      #remove a chave da lista principal
      self.adj_list.pop(node)
      self.vertices -= 1

    else:
      print("Esse vértice não existe")

  def addDirectedEdge(self, u, v):

    #cria os nodes se n existirem
    if not u in self.adj_list.keys():
      self.adiciona_vertice(u)

    #verifica se ja tem aresta para alterar o peso e nao criar mais uma
    if self.tem_aresta(u, v):
      for elem in self.adj_list[u]:
        if elem[0] == v:
          #apenas incrementa diretamente no peso
          elem[1] +=1
    else:
      self.adj_list[u].append([v, 1])
      self.arestas += 1

  def addUndirectedEdge(self, u, v):

    #cria os nodes se n existirem
    if not u in self.adj_list.keys():
      self.adiciona_vertice(u)
    
    if not v in self.adj_list.keys():
      self.adiciona_vertice(v)

    #verifica se ja tem aresta para alterar o peso e nao criar mais uma
    if self.tem_aresta(u, v):
      for elem in self.adj_list[u]:
        if elem[0] == v:
          #apenas incrementa diretamente no peso
          elem[1] +=1

    #verifica se ja tem aresta para alterar o peso e nao criar mais uma
    if self.tem_aresta(v, u):
      for elem in self.adj_list[v]:
        if elem[0] == u:
          #apenas increumenta diretamente no peso
          elem[1] +=1

    else:
      self.adj_list[u].append([v, 1])
      self.adj_list[v].append([u, 1])
      self.arestas += 1


  def remove_aresta(self,u ,v):
    #verifica em ambos os vertices se ela existe
    lista_u = self.adj_list[u]
    for par in lista_u:
      if par[0] == v:
        self.arestas -=1
        lista_u.remove(par)
  
  def tem_aresta(self, u, v):
    for elem in self.adj_list[u]:
      if elem[0] == v:
        return True

    return False

  def grau_entrada(self, u): # retorna a quantidade total de arestas que chegam até o vértice u do grafo G.

    entradas = 0
    lista = self.adj_list
    for item in lista.keys():      #itera sobre os vertices de origem
      for vertice in lista[item]:  #para chegar aos vertices de chegada
        if vertice[0] == u:        #e compara o valor do nome de cada par (nome, peso)
          entradas += 1
    return entradas

  def grau_saida(self, u): # retorna a quantidade total de arestas que saem do vértice u do grafo G.
    return len(self.adj_list[u])

  def grau(self, u): # retorna a quantidade total de arestas conectadas (indegree + outdegree) ao vértice u do grafo G.
    return self.grau_saida(u) + self.grau_entrada(u)

  def get_peso(self, u, v): # retorna qual é o peso da aresta entre os vértices u e v do grafo G, caso exista uma aresta entre eles.

    for elem in self.adj_list[u]:
      if elem[0] == v:
        return elem[1]
    for elem in self.adj_list[v]:
      if elem[0]==u:
        return elem[1]

    return None

  def imprime_lista_adjacencias(self): # imprime na tela a lista de adjacências do grafo G.
    lista = self.adj_list
    print("\n")
    print("Lista de Adjacências")
    for item in lista.keys():
      s = f"{item}: "
      for aresta in lista[item]:
        s += f"{aresta} -> "

      print(s)
    print("\n")

  # Função que calcula a Centralidade de Grau (Degree Centrality) de um vértice. 
  def degreeCentrality(self, node): 
    if self.type == 'Directed':
      return self.grau(node) / (self.vertices - 1)
    else:
      return self.grau_saida(node) / (self.vertices - 1)
    

  def generateDegreeCentralityList(self):
    
    dcs = []
    nodeAndDcs = []
    for node in self.adj_list:
      dc = self.degreeCentrality(node)
      dcs.append(dc)
      nodeAndDcs.append((node, dc))
    
    sortedNodeAndDcs = sorted(nodeAndDcs, key=lambda x: x[1], reverse=True)

    return dcs, sortedNodeAndDcs
    
  #gerar gráficos de histograma com a distribuição de graus dos vértices de cada grafo

  def generateHistogram(self, degreeList):
    print(degreeList)
    media = np.mean(degreeList)
    plt.figure(figsize=(10,10))
    plt.title(f"Degree Centrality distribution of the {self.type} Graph")
    plt.hist(degreeList,bins=16,color='skyblue',edgecolor='black')
    plt.axvline(x=media,color='red',linestyle='dashed',label=f'média: {media}')
    plt.xlabel('Degree')
    plt.ylabel('Frequency')
    plt.legend()
    plt.show()

  def generateBarGraphic(self, sortedDegreesTuple):

    nodes, degrees = zip(*sortedDegreesTuple[:10])

    plt.figure(figsize=(10, 10))
    plt.bar(nodes, degrees, color='skyblue')
    plt.title(f'Top-10 nodes with Higher Degree Centrality for the {self.type} Graph')
    plt.xlabel('Node')
    plt.ylabel('Degree Centrality')
    plt.xticks(rotation=45, ha='right')
    plt.tight_layout()
    plt.show()

  
def buildDirectGraph(df):
  graph = Grafo()
  graph.type = 'Directed'

  for index, row in df.iterrows():
    cast = row['cast'].split(',')
    directors = row['director'].split(',')

    for actor in cast:
      for dir in directors:
        graph.addDirectedEdge(actor, dir)
  return graph

def buildUndirectGraph(df):

  graph = Grafo()
  graph.type = 'Undirected'
  for index, row in df.iterrows():
    cast = row['cast'].split(',')
    totalSize = len(cast)
    for _ in range(totalSize):
      [graph.addUndirectedEdge(cast[0], cast[i]) for i in range(1, len(cast))]
      cast.remove(cast[0])
  return graph

  

df = pd.read_csv('netflix_amazon_disney_titles.csv')
columns = ['director','cast']
people = df[columns]
people.head(5)
people = people.dropna()
people['cast'] = people['cast'].str.replace(", ", ",").str.upper()
people['director'] = people['director'].str.replace(", ", ",").str.upper()

def testUndirected():
    
  test = people[0:100]
  #print(test)
  name = 'DEMIÁN BICHIR'
  undirectGraph = buildUndirectGraph(people)
  #undirectGraph.imprime_lista_adjacencias()
  print(f"vertices {undirectGraph.vertices}")
  print(f"arestas {undirectGraph.arestas} ")
  degreeList, sortedNodeAndDcs = undirectGraph.generateDegreeCentralityList()
  undirectGraph.generateBarGraphic(sortedNodeAndDcs)
  undirectGraph.generateHistogram(degreeList)


def testDirected():
  test = people[0:10]
  print(test)
  name = 'DEMIÁN BICHIR'
  directedGraph = buildDirectGraph(people)  # Mudança aqui
  #directedGraph.imprime_lista_adjacencias()
  print(directedGraph.degreeCentrality(name))
  vertices = str(directedGraph.vertices)
  arestas  = str(directedGraph.arestas)
  print(f"vertices {directedGraph.vertices}")  
  print(f"arestas {directedGraph.arestas} ")   
  degreeList, sortedNodeAndDcs = directedGraph.generateDegreeCentralityList()
  directedGraph.generateHistogram(degreeList)
  directedGraph.generateBarGraphic(sortedNodeAndDcs)
  print('deu erro')

  
testDirected()
