#!/usr/bin/python
# -*- coding: utf-8 -*-

'''
Diferentes utilidades para trabajar con expresiones matemáticas
'''

class CombinacionLineal(object):
  def __init__(self, coeficientes,variables):
    if isinstance(coeficientes,(list,tuple)):
      self._coeficientes=coeficientes
      self._variables=variables
    else:
      raise Exception(" Error: Los coeficientes deben corresponder a una lista o tupla")
  @property
  def coeficientes(self):
    return tuple(self._coeficientes)
  
  def __str__(self):
    nvars= len(self._variables)
    s=''
    for i, c in enumerate(self._coeficientes):
      var=''
      if i<nvars:
        var= self._variables[i]
      #Si el signo es negativo no se agrega nada
      signo='+'
      if c<0 or s == '':
        signo=''
      #Verifica si el coeficiente es uno o menos uno
      # para obviar el número
      cstr=''
      if c == -1:
        cstr='-'
      elif c*c > 1:
        cstr= str(c)
      if c != 0:
        if cstr =='' and var=='':
          # Esto es en caso de que la constante 
          # sea 1, y no tenga variable
          cstr=1
        s+='%s%s%s'%(signo,cstr,var)
    return s

#%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
#%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

class Polinomio(object):
  '''
  orden_usual: indica si se inicia desde el término de mayor grado en los 
  coeficientes pasados para crear el polinomio. Se debe tener cuidado con 
  el orden interno de los coeficientes, el cual siempre será de menor 
  grado a mayor grado, orden usual afecta a como se muestra el polinomio y 
  al momento de crearlo
  '''
  def __init__(self,coeficientes, variable='x', orden_usual=False):
    
    if isinstance( coeficientes, Polinomio):
      self._coeficientes = coeficientes._coeficientes[::]
      self._orden_usual = coeficientes._orden_usual
      self._variables = coeficientes._variables
      return
    
    self._orden_usual=orden_usual
    if orden_usual:
      coeficientes=coeficientes[::-1]
    #Ajusta las variables
    variables=['',variable]
    for i in range(len(coeficientes)-2):
      variables.append('%s^%i'%(variable,i+2))
    
    if orden_usual:
      variables=variables[::-1]
    
    if isinstance(coeficientes,(list,tuple)):
      self._coeficientes=coeficientes
      self._variables=variables
    else:
      raise Exception(" Error: Los coeficientes deben corresponder a una lista o tupla")
    
  @property
  def orden_usual(self):
    return self._orden_usual
  @orden_usual.setter
  def orden_usual(self,value):
    if not isinstance(value,bool):
      raise Exception('se esperaba un valor booleano')
    if value !=self._orden_usual:
      self._variables=self._variables[::-1]
      self._orden_usual=value
      
      
  @property
  def coeficientes(self):
    return self._coeficientes
  
  @property
  def variable(self):
    if self._orden_usual:
        return self._variables[-2]
    else:
        return self._variables[1]
  @property
  def grado(self):
    return len(self._coeficientes)-1

  def Multiplicar(self,polinomio):
    '''Multiplicación con otro polinomio'''
    if isinstance(polinomio,(int, float)):
      newPolinomio = Polinomio(self)
      newPolinomio.escalar(polinomio)
      return newPolinomio
    if self.variable != polinomio.variable:
      raise Exception('Error: los polinomios no son compatibles'
      +'en variables: %s, %s'%(self.variable , polinomio.variable))
    coefA= self.coeficientes
    coefB= polinomio.coeficientes
    
      
    
    gradoNuevo= self.grado+polinomio.grado
    coefR=[0]*(gradoNuevo+1)
    for i,a in enumerate(coefA):
      for j,b in enumerate(coefB):
        coefR[i+j]+=a*b
    
    # Ajusta el orden de los coeficientes para que se entienda en orden usual
    # si es necesario
    if self._orden_usual:
      coefR = coefR[::-1]
    
    return Polinomio(coefR,variable=self.variable,orden_usual= self._orden_usual)
    
  def Sumar(self,polinomio):
    if self.variable != polinomio.variable:
      raise Exception('Error: los polinomios no son compatibles'
      +'en variables: %s, %s'%(self.variable , polinomio.variable))
    
    coefA= self.coeficientes
    coefB= polinomio.coeficientes
    nA= len(coefA)
    nB= len(coefB)
    # coloca al final los ceros para completar
    if nA > nB:
      coefB+=(0,)*(nA-nB)
    elif nB > nA:
      coefA+=(0,)*(nB-nA)
    coefR=[a+b for a,b in zip(coefA,coefB)]
    if self._orden_usual:
        coefR = coefR[::-1]
    return Polinomio(coefR,self.variable, self._orden_usual)
  
  def Restar(self, polinomio):
    # cambia de signos los coeficientes
    newPol = polinomio*(-1)
    return self.Sumar(newPol)
  
  def escalar(self, k):
    self._coeficientes=[k*c for c in self._coeficientes]
  
  def Ruffini(self, v):
    """
    División para un binomio lineal ax+b, donde v = -b/a
    Retorna los coeficientes resultantes, el cociente y el residuo
    """
    
    # Invierte coeficientes para iniciar desde el de mayor grado
    coef = self._coeficientes[::-1]
    coefR = [0]*len(coef)
    for i, c in enumerate(coef):
      if i == 0:
        coefR[i] = c
      else:
        coefR[i] = coef[i]+coefR[i-1]*v
    residuo = coefR[-1]
    cociente = Polinomio(coefR[:-1],orden_usual=True)
    return (cociente, residuo, coefR)
  #%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
  def __str__(self):
    nvars= len(self._variables)
    coeficientes=self._coeficientes
    if self._orden_usual:
      coeficientes=coeficientes[::-1]
    s=''
    for i, c in enumerate(coeficientes):
      var=''
      if i<nvars:
        var= self._variables[i]
      #Si el signo es negativo no se agrega nada
      signo='+'
      if c<0 or s == '':
        signo=''
      #Verifica si el coeficiente es uno o menos uno
      # para obviar el número
      cstr=''
      if c == -1:
        cstr='-'
      elif c*c > 1:
        cstr= str(c)
      if c != 0:
        if cstr =='' and var=='':
          # Esto es en caso de que la constante 
          # sea 1, y no tenga variable
          cstr='1'
          #print('***** se da 1')
        elif cstr=='-' and var =='':
          cstr='-1'
        s+='%s%s%s'%(signo,cstr,var)
    return s
  
  def __call__(self, value):
    '''
    Evalua el polinomio
    '''
    r=0
    coeficientes=self._coeficientes
    
#    if self._orden_usual:
#      coeficientes=coeficientes[::-1]
    #print(coeficientes)
    for i, coef in enumerate(coeficientes):
      t=coef*value**i
      r+=t
      #print('  %i *%i^%i=%i    r=%i'%(coef,value,i,t,r))
    return r
  
  
  def __mul__(self,other):
    return self.Multiplicar(other)
    
  def __add__(self,other):
    if isinstance(other,int):
      coeficientes=self._coeficientes[:]
      coeficientes[0]+=other
      return Polinomio(coeficientes,variable=self.variable, orden_usual=self.orden_usual)
    return self.Sumar(other)
  def __sub__(self, other):
    if isinstance(other,int):
      coeficientes=self._coeficientes[:]
      coeficientes[0]+=other
      return Polinomio(coeficientes,variable=self.variable)
    return self.Restar(other)
