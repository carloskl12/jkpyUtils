'''
Clase para facilitar el trabajo con fechas en español
'''
from datetime import datetime

MESES=( ('enero', 31), ('febrero',28), ('marzo',31), ('abril',30), 
        ('mayo',31), ('junio',30), ('julio',31), ('agosto',31), 
        ('septiembre',30) , ('octubre',31), ('noviembre',30),('diciembre',31))

DIC_MESES={v[0]:(i,v[1]) for i,v in enumerate(MESES)}

DIC_DIAS={'lunes':0,'martes':1, 'miércoles':2, 'jueves':3, 'viernes':4,
          'sábado':5, 'domingo':6}
DIAS=('lunes','martes','miércoles','jueves','viernes','sábado','domingo')
DAYS=('monday','tuesday','wednesday','thursday','friday','saturday','sunday')

class Fecha(object):
  '''
  Encapsula una fecha
  que se inicia con una fecha particular
  especificada como 
  
  día-semana día-mes mes año 
  martes 28 julio 2020
  
  que en formato de fecha de la clase sería
  -d -dm -m -y
  '''
  __formato='-d -dm -m -y'
  def __init__(self, fecha):
    day, mday, month, year  =self.GetInfo(fecha)
    self.day=day #número del día de la semana
    self.year=year #número del año
    self.month=month # número del mes
    self.mday=mday #día del mes
  
  def GetInfo(self, fecha):
    '''
    Obtiene el año, més, día, dia de la semana 
    en forma numérica
    '''
    if isinstance(fecha,str):
      s=fecha.strip().lower()
      day, mday, month, year= s.split(' ')
      day=DIC_DIAS[day]
      year=int(year)
      month=DIC_MESES[month][0]
      mday=int(mday)-1
      return day, mday, month, year
    elif isinstance(fecha, datetime):
      s=fecha.strftime('%w %d %m %Y')
      day, mday, month, year= s.split(' ')
      day=int(day)-1
      year=int(year)
      month=int(month)-1
      mday=int(mday)-1
      return day, mday, month, year
    
    elif isinstance(fecha,tuple):
      # En este caso es una tupla indicando el formato del string segun
      # el datetime (stringFecha, strFormato)
      sfecha,sformato=fecha
      return self.GetInfo(datetime.strptime(sfecha, sformato))
    else:
      raise Exception('  Error: formato no válido')
  def PasarAl(self, day):
    '''
    Avanza la fecha al próximo día que se de como parámetro
    '''
    day=day.strip().lower()
    if not day in DIAS:
      raise Exception('  Error: no se reconoce el día "%s"'%str(day))
    day=DIAS.index(day)
    for i in range(8):
      self.IncDay()
      if self.day == day:
        break
    
  def IncDay(self):
    '''
    Incrementa un día
    '''
    self.day+=1
    if self.day >= 7:
      self.day=0
    
    self.mday+=1
    if self.month == 1 and self.year%4==0:
      #Año biciesto
      if self.mday >= 29:
        self.mday=0
        self.month+=1
    else:
      if self.mday >= MESES[self.month][1]:
        self.mday=0
        self.month+=1
    if self.month >=12:
      self.year+=1
      self.month=0
  
  def DecDay(self):
    '''
    Decrementa un día
    '''
    self.day-=1
    if self.day<=-1:
      self.day=6
    
    self.mday-=1
    
    if self.month == 2 and self.year%4==0:
      #Año biciesto
      if self.mday == -1:
        self.mday=29
        self.month-=1
    else:
      if self.mday == -1: 
        self.month-=1
        self.mday=MESES[self.month][1]-1
        
    if self.month ==-1:
      self.year-=1
      self.month=11


  def __call__(self,formato='-d -dm de -m'):
    '''
    Obtiene la fecha en un formato especificado
    -d : día de la semana
    -dm : día del mes
    -m : mes
    -y : año
    -M : mes iniciado con mayúscula
    -D : día del més iniciado con mayúscula
    '''
    partes=formato.strip().split(' ')
    s=''
    for p in partes:
      if s !='':
        s+=' '
      if p== '-d':
        s+=DIAS[self.day]
      elif p=='-D':
        s+=DIAS[self.day].capitalize()
      elif p=='-dm':
        s+=str(self.mday+1)
      elif p=='-m':
        s+=MESES[self.month][0]
      elif p=='-M':
        s+=MESES[self.month][0].capitalize()
      elif p=='-y':
        s+=str(self.year)
      else:
        s+=p
    return s
  
  def __add__(self,other):
    if isinstance(other,int):
      if other>=0:
        for i in range(other):
          self.IncDay()
      else:
        raise Exception('No se puede incrementar %i días.'%other)
    else:
      raise Exception('No se puede sumar el tipo '+type(other).__name__)
  
  def __sub__(self,other):
    if isinstance(other,int):
      if other>=0:
        for i in range(other):
          self.DecDay()
      else:
        raise Exception('No se puede decrementar %i días.'%other)
    else:
      raise Exception('No se puede restar el tipo '+type(other).__name__)

  def __str__(self):
    '''
    Con el string generado se puede volver a replicar el 
    mismo objeto de fecha
    '''
    return self(self.__formato)
    
  def ToDatetime(self, hora=0):
    '''
    Pasa a tiempo estandar sumando la hora especificada
    en formato de 0 a 23
    '''
    date='%i %i %i %i'%(self.year,self.month+1,self.mday+1,hora)
    date=datetime.strptime(date, '%Y %m %d %H')
    return date


#%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
#%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
# calcula fechas
if __name__ == '__main__':
  fecha=Fecha('lunes 3 agosto 2020')
  fIni=str(fecha)
  for i in range(56):
    fecha+1
    if fecha.day==0:
      print( '  fecha:',fecha('-d -m -dm de -y'))
  for i in range(56):
    fecha-1
  if str(fecha) == fIni:
    print('  La resta es correcta')
  else:
    print('  No coincide la resta:',fIni, fecha)
  
  print('  fecha:',fecha)
  
  fecha.PasarAl('miércoles')
  
  print('  fecha final:', fecha)


