from pandas import read_csv
from datetime import datetime
import matplotlib.pyplot as plt
import numpy as np
import copy
import random
import math
Semilla=0
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
    while inicio<fin-1:
        factor=contagios[inicio+1]/contagios[inicio]
        if contagios[inicio+1]==0 or contagios[inicio]==0:
            factor=0.1
        elif factor>5:
            factor=factor
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
    if 0<=aux<6:
        return factor[len(factor)-1] # retorna el calculo de factor promedio
    else:
        random.seed(Semilla)
        aux=random.randint(0,len(factor)-2) # retorna el factor de contagio de algun dia
        Semilla=Semilla+1
        return factor[aux]


def proyeccionInicial(inicio,CS,SS):
    fin=inicio+14
    aux=[]
    VInicial=CS[inicio+13]+SS[inicio+13]
    if VInicial==0:
        VInicial=1
    i=copy.copy(inicio)
    while i<fin:
        aux.append(CS[i]+SS[i])
        i=i+1
    factor=FactorContagio(aux)
    print(factor)
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



def proyeccion(inicio,contagios,CS,SS):
    fin=inicio+14
    aux=[]
    VInicial=contagios[len(contagios)-1]
    if VInicial==0:
        VInicial=1
    i=copy.copy(inicio)
    while i<fin:
        aux.append(CS[i+14]+SS[i+14])
        i=i+1
    factor=FactorContagio(aux)
    print(factor)
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

def comparacion(CS,SS,proyectado):
    i=0
    err=[]
    while i<len(proyectado):
        error=((proyectado[i]-(CS[i+14]+SS[i+14]))/(CS[i+14]+SS[i+14]))*100
        err.append(error)
        i=i+1
    return err


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
aricaI=[]

llenar(58,933,CS_it,CS_ut)
llenar(1,876,SS_it,SS_ut)

region=0
aux=proyeccionInicial(0,CS_ut[region],SS_ut[region]) # dia 7 al 13
agregar(aux,arica)
aux=proyeccion(0,arica,CS_ut[region],SS_ut[region]) # dia 14 al 20
agregar(aux,arica)
aux=proyeccion(14,arica,CS_ut[region],SS_ut[region]) # dia 21 al 27
agregar(aux,arica)
aux=proyeccion(28,arica,CS_ut[region],SS_ut[region]) # dia 28 al 34
agregar(aux,arica)
aux=proyeccion(42,arica,CS_ut[region],SS_ut[region]) # dia 35 al 41
agregar(aux,arica)
# print(comparacion(CS_ut[region],SS_ut[region],arica))
# print(arica)

# region=6
# aux=proyeccionInicial(0,CS_ut[region],SS_ut[region]) # dia 7 al 13
# agregar(aux,metropolitana)
# aux=proyeccion(0,metropolitana,CS_ut[region],SS_ut[region]) # dia 14 al 20
# agregar(aux,metropolitana)
# aux=proyeccion(14,metropolitana,CS_ut[region],SS_ut[region]) # dia 21 al 27
# agregar(aux,metropolitana)
# aux=proyeccion(28,metropolitana,CS_ut[region],SS_ut[region]) # dia 28 al 34
# agregar(aux,metropolitana)
# aux=proyeccion(42,metropolitana,CS_ut[region],SS_ut[region]) # dia 35 al 41
# agregar(aux,metropolitana)
# print(comparacion(CS_ut[region],SS_ut[region],metropolitana))
# print(metropolitana)
