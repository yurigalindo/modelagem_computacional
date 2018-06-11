import math as math
import random as rand
import plotly.offline as py
import plotly.graph_objs as go
import string 
import networkx as nx

def lattice(n,k):
#funcao que cria um grafo regular
#n: numero de nos no grafo 
#k: grau medio do grafo
#p: porcentagem de individuos do grafo que acreditam no rumor
	lista=[]
	G = nx.Graph()	
	for i in range (0,n):
		lista.append(Pessoa())
	if(k%2==0):
		half=k//2
		for i in range(0,n):
			for j in range(1,half+1):
				lista[i].newFriend(lista[(i+j)%n])
				lista[i].newFriend(lista[(i-j)%n])
				G.add_edge(i,(i+j)%n)
				G.add_edge(i,(i-j)%n)
	if(k%2==1):
		if (n%2==0):
			half=(k-1)//2
			for i in range(0,n):
				for j in range(1,half+1):
					lista[i].newFriend(lista[(i+j)%n])
					lista[i].newFriend(lista[(i-j)%n])
					G.add_edge(i,(i+j)%n)
					G.add_edge(i,(i-j)%n)
				lista[i].newFriend(lista[(n-(1+i))%n])
				G.add_edge(i,(n-(1+i))%n)
		else:
			lista="Grafo n pode ser regular"
	return lista,G


def randGraph(n,k):
#funcao que cria um grafo aleatorio
#n: numero de nos no grafo 
#k: grau medio do grafo
#p: porcentagem de individuos do grafo que acreditam no rumor
	lista=[]
	G = nx.Graph()
	for i in range (0,n):
		lista.append(Pessoa())
	possibilities = (n*n-1)//2
	connections=rand.sample(range(1,possibilities),n*k//2)
	for i in connections:
		primeiro = i//n
		segundo = i%n
		G.add_edge(primeiro,segundo)
		lista[primeiro].newFriend(lista[segundo])
		lista[segundo].newFriend(lista[segundo])
	return lista,G

def barabasi(n,k):
#funcao que cria um grafo de Barabasi
#n: numero de nos no grafo 
#k: grau medio do grafo
#p: porcentagem de individuos do grafo que acreditam no rumor
	n0=k*k+2
	if(n<=n0):
		return -1
	c=k//2
	lista,G=randGraph(n0,k)
	totalDegree=0
	for i in range(0,n0):
		if (lista[i].degree==0):
			G.add_edge(i,i-1)
			lista[i].newFriend(lista[i-1])
			lista[i-1].newFriend(lista[i])
		totalDegree+=lista[i].degree
	for i in range (n0,n):
		lista.append(Pessoa())
		j=0
		m=0
		while (m!=k):
			deg= lista[j].degree
			prob=deg/float(totalDegree)
			if(rand.random()<=prob):
				G.add_edge(i,j)
				lista[i].newFriend(lista[j])
				lista[j].newFriend(lista[i])
				m+=1
			j=(j+1)%i
		totalDegree+=lista[i].degree
	return lista,G

def readGraph(file,n):
	grafo=[]
	G = nx.Graph()
	for i in range(0,n):
		grafo.append(Pessoa())
	reader=open(file)
	nodes=reader.readlines()
	for node in nodes:
		a,b=node.split('	')
		grafo[int(a)-1].newFriend(grafo[int(b)-1])
		G.add_edge(int(a)-1,int(b)-1)
	return grafo,G
class Pessoa: 
#classe que representa as pessoas da rede, que sao os nos do grafo
	def __init__(self):
		self.decay=0.9
		#taxa com a qual a pessoa deixa de acreditar no rumor
		self.degree=0
		#degree armazena o grau do noh, no caso quantos amigos a pessoa tem
		self.rumor=0
		#sempre inicia como nao acreditando no rumor
		self.friends=[]
	def newFriend(self, person):
		self.friends.append(person)
		self.degree+=1
	def update(self):
	#funcao que simula uma iteracao
		self.rumor*=self.decay
		#a pessoa acredita menos no rumor de acordo com a taxa de decaimento
		sum=0
		for neighbor in self.friends:
			sum+=neighbor.rumor
		#a probabilidade da pessoa passar a acreditar no rumor eh (o quanto amigos acreditam)/(numero de amigos+1)
		#tambem eh a probabilidade da crenca ser renovada
		if(rand.random()<(sum/(self.degree+1))):
			self.rumor=1

def plotarGrafo(G):
	### Plotando o grafo
	pos=nx.spring_layout(G)
	nx.set_node_attributes(G,name='pos',values=pos)
	dmin=1
	ncenter=0
	for n in pos:
	    x,y=pos[n]
	    d=(x-0.5)**2+(y-0.5)**2
	    if d<dmin:
	        ncenter=n
	        dmin=d

	p=nx.single_source_shortest_path_length(G,ncenter)

	edge_trace = go.Scatter(
	    x=[],
	    y=[],
	    line=dict(width=1,color='#888'),
	    hoverinfo='none',
	    mode='lines')

	for edge in G.edges():
	    x0, y0 = G.node[edge[0]]['pos']
	    x1, y1 = G.node[edge[1]]['pos']
	    edge_trace['x'] += [x0, x1, None]
	    edge_trace['y'] += [y0, y1, None]

	node_trace = go.Scatter(
	    x=[],
	    y=[],
	    text=[],
	    mode='markers',
	    hoverinfo='text',
	    marker=dict(
	        # showscale=True,
	        # # colorscale options
	        # # 'Greys' | 'Greens' | 'Bluered' | 'Hot' | 'Picnic' | 'Portland' |
	        # # Jet' | 'RdBu' | 'Blackbody' | 'Earth' | 'Electric' | 'YIOrRd' | 'YIGnBu'
	        # colorscale='YIGnBu',
	        # reversescale=True,
	        color=[],
	        size=10,
	        line=dict(width=2))
	    )

	for node in G.nodes():
	    x, y = G.node[node]['pos']
	    node_trace['x'].append(x)
	    node_trace['y'].append(y)

	# for node, adjacencies in enumerate(G.adjacency_list()):
	#     node_trace['marker']['color'].append(len(adjacencies))
	#     node_info = '# of connections: '+str(len(adjacencies))
	#     node_trace['text'].append(node_info)    
	fig = go.Figure(data=[edge_trace, node_trace],
	             layout=go.Layout(
	                title='<br>Grafo',
	                titlefont=dict(size=16),
	                showlegend=False,
	                hovermode='closest',
	                margin=dict(b=20,l=5,r=5,t=40),
	                xaxis=dict(showgrid=False, zeroline=False, showticklabels=False),
	                yaxis=dict(showgrid=False, zeroline=False, showticklabels=False)))
	return fig
## Main ##
tipo="none"
print("Simulacao de rumores\n")
control=int(input("Digite 0 para ler o grafo de um arquivo e 1 para gerar seu grafo:"))
if(control==0):
	file=input("Digite o nome ou caminho do arquivo:")
	file = "network.txt"
	n=int(input("Digite o numero de nos contidos nesse arquivo:"))
	lista1,G=readGraph(file,n)
else:
	tipo=int(input("Digite 0 para um grafo aleatorio, 1 para um grafo regular, e 2 para um grafo de Barabasi:"))
	n=int(input("Digite a quantidade de nos desejados:"))
	k=int(input("Digite	o grau medio desejado:"))
	if(tipo==0):
		lista1,G=randGraph(n,k)
	elif(tipo==1):
		lista1,G=lattice(n,k)
	elif(tipo==2):
		lista1,G=barabasi(n,k)

m=int(input("Digite quantos nos comecam acreditando no rumor:"))
control=int(input("Digite 0 para escolher os nos aleatoriamente, 1 para escolher os de menor grau e 2 para escolher os de maior grau:"))
if(control==0):
	escolhidos=rand.sample(range(0,n),m)
	for i in escolhidos:
		lista1[i].rumor=1
if(control==1):
	lista1.sort(key=lambda person:person.degree)
	for i in range(0,m):
		lista1[i].rumor=1
if(control==2):
	lista1.sort(key=lambda person:-person.degree)
	for i in range(0,m):
		lista1[i].rumor=1

inutil=0
if(tipo==0):
	lista1.sort(key=lambda person:person.degree)
	inutil=0
	while (lista1[inutil].degree==0):
		inutil=inutil+1
	inutil = inutil-1
	if(inutil==-1):
		inutil=0
	print("{0} nos foram desconsiderados por terem grau 0\n".format(inutil))
# file = "network.txt"
# lista1,G=readGraph(file,1000)
#Gerando a rede
#50: numero de pessoas na rede social
#3: grau medio da rede
#0: porcentagem de pessoas que acreditam no rumor desde o inicio (deixei como zero para escolher manualmente os dois de maior grau)

#lista1.sort(key=lambda person:person.degree)
##Ordenando do menor grau pro maior grau

# lista1.sort(key=lambda person:-person.degree)
# #Para ordenar do maior grau pro menor grau

# print (lista1[0].degree)
# lista1[0].rumor=1
# lista1[1].rumor=1
# #Colocando os dois individuos mais influentes (maior grau) como acreditando no rumor




### Simulacao ###
x1=[]
x2=[]
for i in range(0,200):
#Simulando 1000 iteracoes
	count=0
	for person in lista1:
		if(person.rumor>0.05):
			count+=1
		person.update()
		
			#Contando a quantidade de pessoas na rede que acreditam no rumor (acreditar menos de 5% eh desconsiderado)
	
	x1.append(count)
	x2.append(n-inutil-count)
	#x1 armazena quantas pessoas acreditam no rumor a cada iteracao

traces=[
	(go.Scatter(
    x = list(range(0,200)),
    y = x1,
    #plotando os que acreditam no rumor
    name='Acreditam',
    line = dict(
        color = ('rgb(250, 100, 125)'),
        width = 1)
     )),
	(go.Scatter(
    x = list(range(0,200)),
    y = x2,
    name='Nao acreditam',
    #plotando os que nao acreditam no rumor
    line = dict(
        color = ('rgb(150, 130, 255)'),
        width = 1)
     ))

]

fig1=plotarGrafo(G)
fig2 = dict(data=traces)
py.plot(fig1, filename='grafo.html')
py.plot(fig2, filename='rumor.html')
