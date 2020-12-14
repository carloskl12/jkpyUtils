'''
Interfaz para brindar las funcionalidades de logger a una 
Clase
'''
# paquetes para el loggin y gestión de errores
from inspect import currentframe, getframeinfo
import logging, time, sys
import traceback


class AdminLog(object):
  '''
  en el init se ejecuta requisitos para que se instale el logger 
  correctamente, además se debería sobreescribir 
  requisitos para el caso particular de una aplicación con 
  algunos requisitos particulares
  '''
  _logger_lvl='info'
  _logger=None
  _logger_nuevo=True
  
  @property
  def logger_lvl(self):
    return self._logger_lvl
    
  @property
  def logger(self):
    if self._logger == None:
      self.setup_logger()
    return self._logger
  
  #%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
  def requisitos(self):
    '''
    Verifica los requisitos actuales
    '''
    logger = self.logger
    if self._logger_nuevo:
      '''
      Si ya se inició antes un administrador, no se 
      vuelve a realizar la verificación de versiones.
      '''
      logger.info('** Verificando versiones')
      logger.info('  python: '+sys.version.split(' ')[0])

  #%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
  def lineno(self):
    """Returns the current line number in our program."""
    cf = currentframe()
    filename = getframeinfo(cf).f_back.filename
    msg='Traceback(most recent call last):\n  File "%s"'%filename
    msg+=', line %i'%currentframe().f_back.f_lineno
    return msg
  #%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
  def TestError(self):
    '''
    Solo con el fin de testear el manejo de errores insalvables
    
    '''
    pass #Error
    self.ErrorOcurrido('Un error de TestError')
  
  #%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
  def ErrorOcurrido(self, msg=None,line=-1):
    '''
    Maneja un error que no tiene solución, es decir la ejecusión se termina.
    msg: es el mensaje del error
    line: indica el offset desde la linea en la cual se invoca a esta función
    
    la idea es que a cambio de utilizar el usuar raise Exception, 
    se utilice ErrorOcurrido(msg,-1) si el error ocurre una linea 
    antes de donde se hace lla llamada a esta función.
    '''
    infoLinea=traceback.format_exc()
    if infoLinea=='NoneType: None\n':
      
      cf = currentframe()
      filename = getframeinfo(cf.f_back).filename
      funName= getframeinfo(cf.f_back).function
      lineNumber=currentframe().f_back.f_lineno+line
      codeContext=''
      with open(filename,'r') as f:
        for i, line in enumerate(f):
          if i == lineNumber-1:
            codeContext=line.strip()
      
      ss='Traceback(most recent call last):\n  File "%s"'%filename
      ss+='\n  line: %i'%lineNumber
      ss+='\n  function: '+funName
      ss+='\n  code: "%s"'%codeContext
      ss+='\n  msg: %s\n'%msg
      self.logger.error('ERROR: '+ss)
    else:
      self.logger.error('\nERROR: '+infoLinea)
    sys.exit(1)
    
  #%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
  def setup_logger(self,modo=None):
    '''
    Configura el looger
    '''
    if modo == None:
      modo= self._logger_lvl
    dicModos={'info':logging.INFO, 'debug':logging.DEBUG, 'warning':logging.WARNING}
    if self._logger != None:
      '''
      Evita crear muchos loggers
      '''
      self._logger.setLevel(dicModos[modo])
      return self._logger
    logger = logging.getLogger()
    logger.setLevel(dicModos[modo])
    if not len(logger.handlers):
      '''
      En este caso se verifica si ya tiene manejadores activos,
      de no existir, implica que es por primera vez que se configura
      por lo tanto se deben agregar
      '''
      # Imprime la información en terminal
      ch = logging.StreamHandler()
      # Manejador para archivo
      fileHandler = logging.FileHandler('adminLog.log')
      # crea un formato
      formatter = logging.Formatter("%(message)s")#Formato sencillo
      # agrega el formato
      ch.setFormatter(formatter)
      fileHandler.setFormatter(formatter)
      
      logger.addHandler(ch)
      logger.addHandler(fileHandler)
      stime= time.strftime("%d %b %Y %H:%M:%S", time.localtime())
      logger.info('*'*30)
      logger.info('**   %s   **'%stime)
      logger.info('**  Administrador iniciado  **')
      logger.info('logger level: %s'%modo.upper())
    else:
      self._logger_nuevo=False
    self._logger= logger
    return logger
