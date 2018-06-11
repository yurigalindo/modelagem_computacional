import math as math
import random as rand
import plotly.offline as py
import plotly.graph_objs as go
import string 

def lattice(n,k):
	lista=[]
	for i in range (0,n):
		lista.append(Neurons())
	if(k%2==0):
		half=k//2
		for i in range(0,n):
			for j in range(1,half+1):
				lista[i].couple(lista[(i+j)%n])
				lista[i].couple(lista[(i-j)%n])
	if(k%2==1):
		if (n%2==0):
			half=(k-1)//2
			for i in range(0,n):
				for j in range(1,half+1):
					lista[i].couple(lista[(i+j)%n])
					lista[i].couple(lista[(i-j)%n])
				lista[i].couple(lista[(n-(1+i))%n])
		else:
			lista="Grafo n pode ser regular"
	return lista

def randGraph(n,k):
	lista=[]
	for i in range (0,n):
		lista.append(Neurons())
	possibilities = (n*n-1)//2
	connections=rand.sample(range(1,possibilities),n*k//2)
	for i in connections:
		primeiro = i//n
		segundo = i%n
		lista[primeiro].couple(lista[segundo])
		lista[segundo].couple(lista[segundo])
	return lista

def barabasi(n,k):
	n0=k*k+2
	if(n<=n0):
		return -1
	c=k//2
	lista=randGraph(n0,k)
	totalDegree=0
	for i in range(0,n0):
		if (lista[i].degree==0):
			lista[i].couple(lista[i-1])
			lista[i-1].couple(lista[i])
		totalDegree+=lista[i].degree
	for i in range (n0,n):
		lista.append(Neurons())
		j=0
		m=0
		while (m!=k):
			deg= lista[j].degree
			p=deg/float(totalDegree)
			if(rand.random()<=p):
				lista[i].couple(lista[j])
				lista[j].couple(lista[i])
				m+=1
			j=(j+1)%i
		totalDegree+=lista[i].degree
	return lista

class Neurons: 
	theta=0.5
	alpha=6
	epsilon=0.02
	beta=0.1
	timestep=0.15
	def __init__(self):
		
		self.inputs=0
		self.I=-0.02
		self.x=rand.randrange(-2,2)
		self.y=rand.randrange(1,5)
		self.coupledNeurons=[]
		self.degree=0
	def activate(self):
		self.I=0.2
	def couple(self, neuron):
		self.coupledNeurons.append(neuron)
		self.degree+=1
	def receive(self,input):
		if (input-self.theta)>=0:
			self.inputs+=0.1
			#print 'received'
		#print 'not received'
	def output(self):
		for neuron in self.coupledNeurons:
			neuron.receive(self.x)

	def update(self):
		#print self.inputs
		#print deltax
		self.x+=(3*self.x-self.x*self.x*self.x+2-self.y+self.I+self.inputs)*self.timestep
		self.y+=self.epsilon*(self.alpha*(1+math.tanh(self.x/self.beta))-self.y)*self.timestep
		self.output()
		self.inputs=0

## Main ##
tipo="none"
print("Simulacao de neuronios acoplados\n")

tipo=int(input("Digite 0 para um grafo aleatorio, 1 para um grafo regular, e 2 para um grafo de Barabasi:"))
n=int(input("Digite a quantidade de neuronios desejados:"))
k=int(input("Digite	o grau medio de conexoes desejado:"))
if(tipo==0):
	lista1=randGraph(n,k)
elif(tipo==1):
	lista1=lattice(n,k)
elif(tipo==2):
	lista1=barabasi(n,k)

m=int(input("Digite quantos neuronios comecam ativos:"))
control=int(input("Digite 0 para escolher os nos aleatoriamente, 1 para escolher os de menor grau e 2 para escolher os de maior grau:"))
if(control==0):
	escolhidos=rand.sample(range(0,n),m)
	for i in escolhidos:
		lista1[i].activate()
if(control==1):
	lista1.sort(key=lambda person:person.degree)
	for i in range(0,m):
		lista1[i].activate()
if(control==2):
	lista1.sort(key=lambda person:-person.degree)
	for i in range(0,m):
		lista1[i].activate()


y=[[] for i in range(0,n)]
quant=50
if(n<=50):
	quant=n
neuroniosAcompanhados =rand.sample(range(0,n),quant)
for i in range(0,15000):
	for neuronio in lista1:
		neuronio.update()
	if i%30==0:
		for j,neuronio in enumerate(neuroniosAcompanhados):
			y[j].append(lista1[neuronio].x+5*j)	

traces=[]
for i in range(0,quant):
	traces.append (go.Scatter(
	    x = list(range(0,500)),
	    y = y[i],
	    line = dict(
	        color = ('rgb({0}, {1}, {2})').format((i*21)%250,(i*68)%250,(i*33)%250),
	        width = 1)
	))


fig = dict(data=traces)
print("Para visualizacao, sera mostrado o comportamento de 50 neuronios aleatoriamente escolhidos")
py.plot(fig, filename='Neuronios Acoplados.html')
