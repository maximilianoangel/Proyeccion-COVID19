from pandas import read_csv
from datetime import datetime
import matplotlib.pyplot as plt
import numpy as np
import copy
import random
import math
Semilla=0
fac=0
def llenar(inicio,fin,lista,A):
    j=0
    while j<len(lista)-1:
        i=copy.copy(inicio)
        f=fin
        it=0
        while i<f:
            A[j][it]=lista[j][i]
            i=i+1
            it=it+1
        j=j+1

# def FactorContagio(contagios): # calcula el factor de contagios de una semana
#     inicio=0
#     aux=[]
#     fin=len(contagios)-1
#     promedio=0
#     while inicio<fin-1:
#         factor=contagios[inicio+1]/contagios[inicio]
#         if factor ==0:
#             factor=0.1
#         aux.append(factor)
#         promedio=promedio+aux[inicio]
#         inicio=inicio+1
#     promedio=promedio/(inicio-1)
#     aux.append(promedio)
#     return aux

def FactorContagio(contagios): # calcula el factor de contagios de una semana
    inicio=0
    aux=[]
    fin=len(contagios)-1
    global region
    global fac
    while inicio<fin-1:
        factor=contagios[inicio+1]/contagios[inicio]
        if contagios[inicio+1]==0 or contagios[inicio]==0:
            factor=0.1
        elif factor>5:
            factor=factor
        factor=factor+fac
        aux.append(factor)
        inicio=inicio+1
    aux.sort()
    longitud = len(aux)
    mitad = int(longitud / 2)
    if longitud % 2 == 0:
        mediana = (aux[mitad - 1]+aux[mitad]) / 2
    else:
        # Si no, es la del centro
        mediana = aux[mitad]
    aux.append(mediana)
    return aux


# def FactorContagio(contagios): # calcula el factor de contagios de una semana
#     inicio=0
#     aux=[]
#     fin=len(contagios)-1
#     while inicio<fin-1:
#         factor=contagios[inicio+1]/contagios[inicio]
#         if factor ==0:
#             factor=0.1
#         aux.append(factor)
#         inicio=inicio+1
#     aux.sort()
#     media=np.mean(aux)
#     aux.append(media)
#     return aux


def SeleccionFactor(factor): #selecciona uno de los factores de contagios
    global Semilla
    random.seed(Semilla)
    aux=random.randint(0,9)
    Semilla=Semilla+1
    if 0<=aux<7:
        return factor[len(factor)-1] # retorna el calculo de factor promedio
    else:
        random.seed(Semilla)
        aux=random.randint(0,len(factor)-2) # retorna el factor de contagio de algun dia
        Semilla=Semilla+1
        return factor[aux]



# def SeleccionFactor(factor): #selecciona uno de los factores de contagios
#     global Semilla
#     random.seed(Semilla)
#     aux=random.randint(0,9)
#     Semilla=Semilla+1
#     if 0<=aux<7:
#         return factor[len(factor)-1] # retorna el calculo de factor promedio
#     else:
#         random.seed(Semilla)
#         aux=random.randint(0,9) # retorna el factor de contagio de algun dia
#         Semilla=Semilla+1
#         random.seed(Semilla)
#         aux3=random.randint(1,9)
#         Semilla=Semilla+1
#         if 0<=aux<6:
#             aux2=factor[len(factor)-1]+(aux3/10)
#         else:
#             if (aux3/10)>=factor[len(factor)-1]:
#                 aux2=factor[len(factor)-1]-(aux3/100)
#             else:
#                 aux2=factor[len(factor)-1]-(aux3/10)
#         return aux2

def proyeccionInicial(inicio,CS,SS,dias):
    fin=inicio+dias
    aux=[]
    VInicial=CS[inicio+(dias-1)]+SS[inicio+(dias-1)]
    if VInicial==0:
        VInicial=1
    i=copy.copy(inicio)
    while i<fin:
        aux.append(CS[i]+SS[i])
        i=i+1
    factor=FactorContagio(aux)
    aux=[]
    while inicio<fin:
        seleccion=SeleccionFactor(factor)
        if len(aux)==0:
            NCovid=(VInicial)*seleccion
        else:
            NCovid=(aux[len(aux)-1])*seleccion
        aux.append(math.ceil(NCovid))
        inicio=inicio+1
    return aux



def proyeccion(inicio,contagios,CS,SS,dias):
    fin=inicio+dias
    aux=[]
    VInicial=contagios[len(contagios)-1]
    if VInicial==0:
        VInicial=1
    i=copy.copy(inicio)
    while i<fin:
        aux.append(CS[i+(dias-1)]+SS[i+(dias-1)])
        i=i+1
    factor=FactorContagio(aux)
    aux=[]
    while inicio<fin:
        seleccion=SeleccionFactor(factor)
        if len(aux)==0:
            NCovid=(VInicial)*seleccion
        else:
            NCovid=(aux[len(aux)-1])*seleccion
        aux.append(math.ceil(NCovid))
        inicio=inicio+1
    return aux

def agregar(lista,region):
    fin=len(lista)
    i=0
    while i < fin:
        region.append(lista[i])
        i=i+1

def comparacion(CS,SS,proyectado,dias):
    i=0
    err=[]
    while i<len(proyectado):
        aux=CS[i+dias]+SS[i+dias]
        if aux ==0:
            aux=1
        error=((proyectado[i]-(CS[i+dias]+SS[i+dias]))/(aux))*100
        if error<0:
            error=error*(-1)
        err.append(error)
        i=i+1
    return err

def promedio(error):
    i=0
    aux=0
    while i<len(error):
        aux=aux+error[i]
        i=i+1
    err=aux/len(error)
    return err


def solver(CS_ut,SS_ut,Nregion,dias,region):
    i=0
    while i<5:
        if i==0:
            aux=proyeccionInicial(0,CS_ut[Nregion],SS_ut[Nregion],dias)
        else:
            if i ==1:
                aux=proyeccion(0,region,CS_ut[Nregion],SS_ut[Nregion],dias)
            else:
                aux=proyeccion((dias*(i-1)),region,CS_ut[Nregion],SS_ut[Nregion],dias)
        agregar(aux,region)
        i=i+1

CSintomas=read_csv('CasosNuevosConSintomas.csv')
SSintomas=read_csv('CasosNuevosSinSintomas.csv')

CS_it=CSintomas.values
SS_it=SSintomas.values

CS_ut=np.empty((16,875),int)
SS_ut=np.empty((16,875),int)


region=0

arica=[]
tarapaca=[]
antofagasta=[]
atacama=[]
coquimbo=[]
valparaiso=[]
metropolitana=[]
ohiggins=[]
maule=[]
nuble=[]
biobio=[]
Araucania=[]
losrios=[]
loslagos=[]
aysen=[]
magallanes=[]

llenar(58,933,CS_it,CS_ut)
llenar(1,876,SS_it,SS_ut)
i=0
dias=14
solver(CS_ut,SS_ut,0,dias,arica)

print(arica)
print(promedio(comparacion(CS_ut[region],SS_ut[region],arica,dias)))

