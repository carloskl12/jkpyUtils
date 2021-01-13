import subprocess
import os.path as osp
'''
Codigo obtenido de https://gist.github.com/godber/7692812
'''

def pdfinfo(infile):
    """
    Wraps command line utility pdfinfo to extract the PDF meta information.
    Returns metainfo in a dictionary.
    sudo apt-get install poppler-utils
    This function parses the text output that looks like this:
        Title:          PUBLIC MEETING AGENDA
        Author:         Customer Support
        Creator:        Microsoft Word 2010
        Producer:       Microsoft Word 2010
        CreationDate:   Thu Dec 20 14:44:56 2012
        ModDate:        Thu Dec 20 14:44:56 2012
        Tagged:         yes
        Pages:          2
        Encrypted:      no
        Page size:      612 x 792 pts (letter)
        File size:      104739 bytes
        Optimized:      no
        PDF version:    1.5
    """

    cmd = '/usr/bin/pdfinfo'
    if not osp.exists(cmd):
        raise RuntimeError('System command not found: %s' % cmd)

    if not osp.exists(infile):
        raise RuntimeError('Provided input file not found: %s' % infile)

    def _extract(row):
        """Extracts the right hand value from a : delimited row"""
        return row.split(':', 1)[1].strip()

    output = {}

    labels = ['Title', 'Author', 'Creator', 'Producer', 'CreationDate',
              'ModDate', 'Tagged', 'Pages', 'Encrypted', 'Page size',
              'File size', 'Optimized', 'PDF version']

    cmd_output = subprocess.check_output([cmd, infile]).decode("utf-8")
    for line in map(str, cmd_output.splitlines()):
        for label in labels:
            if label in line:
                output[label] = _extract(line)

    return output
    
#%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
# Función para extraer la dimensión de página como una tupla (width, height, unit)
def pdfpagesize(fname):
  dicPdfinfo = pdfinfo(fname)
  vals= dicPdfinfo['Page size'].split(' ')
  return (float(vals[0]), float(vals[2]), vals[3])
