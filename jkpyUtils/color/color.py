#funciones alusivas al color
# El formato HSV es bastante conveniente para el diseño de paletas de colores
# dado su valor semántico en cada componente
# H: matiz 0 - 360 grados
#   0: rojo, 60: amarillo
#   120: verde  180: cian
#   240: azul   300: magenta
#
# S: saturación, 0-1
#    representa la distancia al eje de brillo negro-blanco. A menor saturación
#    mas grisáceo es el color
#
# V: representa la altura en el eje blanco-negro, 0-255, 0 indica negro, y
#    255 blanco o un color particular según el nivel de saturación y matiz.

def htmlToRGB( htmlColor ):
  '''Transforma un color en formato de color html a tupla rgb '''
  return tuple(int(htmlColor[i:i+2], 16) for i in (1, 3, 5) ) 

def RGBTohtml( rgb ):
  return '#%02x%02x%02x'%tuple(rgb)
  
def rgb_to_HSV(r,g,b):
  """
  pasa de rgb a HSV
  
  """
  vmax = r
  if vmax < g: vmax = g
  if vmax < b: vmax = b
  
  vmin = r
  if vmin > g: vmin = g
  if vmin > b: vmin = b
  
  H=0
  if vmax == r  and g >= b:
    H=60*( g - b )/ ( vmax - vmin )
  elif vmax == r  and g < b:
    H=60*( g - b )/ ( vmax - vmin )+360
  elif vmax == g  and g < b:
    H=60*( b - r )/ ( vmax - vmin )+120
  elif vmax == b  and g < b:
    H=60*( r - g )/ ( vmax - vmin )+240
    
  S=0
  if vmax >0:
    S= 1 - vmin/vmax
  V= vmax
  return (H, S, V)


def HSV_to_rgb(H, S, V):
  while H > 360:
    H-=360
  
  Hi= (H//60) % 6
  f= ((H/60)%6 - Hi)
  p = V*(1-S)
  q = V*(1-f*S)
  t = V*(1-(1-f)*S)
  dicResult = {0:(V,t,p), 1:(q,V,p), 2:(p,V,t), 3:(p,q,V), 4:(t,p,V), 5:(V,p,q)}
  
  return dicResult[Hi]

class Color(object):
  
  
  def __init__(**kwargs):
    
    if len(kwargs)==1:
      if "rgb" in kwargs:
        self.h, self.s, self.v = rgb_to_HSV(*kwargs['rgb'])
    
      elif "html" in kwargs:
        self.h, self.s, self.v = rgb_to_HSV( htmlToRGB(*kwargs['html']) )
      elif "HSV" in kwargs:
        self.h, self.s, self.v = kwargs["HSV"]
  


   
  
  
  
