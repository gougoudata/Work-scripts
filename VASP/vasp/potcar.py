'''
Created on Mar 29, 2012

@author: chtho
'''

class Potcar(object):
    '''
    Class for generating potcars
    '''

    def __init__(self, path, path_to_potcars=None, potentials=None):
        '''
        Constructor
        '''
        self.path = path
        self.path_to_potcars = path_to_potcars
        self.potentials = potentials
        if path_to_potcars == None:
            self._extract_data()
    
    def create_file(self):
        potcar = open("%s/POTCAR" % self.path, 'w')
        for potential in self.potentials:
            f = open("%s/%s/POTCAR" % (self.path_to_potcars, potential), 'r')
            for line in f:
                potcar.write(line)
            f.close()
        potcar.close()
        
    def _extract_data(self):
        potcar = open("%s/POTCAR" % self.path, 'r')
        for line in potcar:
            if "TITEL" in line:
                self.potentials.append(line.split()[3])
        potcar.close()

if __name__ == '__main__':
    path = '/Users/chtho/Desktop'
    path_to_potcars ='/Volumes/Macintosh HD 2/git/Work/VASP/Potentials/5.2/PAW/'
    potentials = ['PBE/Ti_pv/', 'PBE/N/', 'PBE/Al/']
    Potcar(path, path_to_potcars, potentials).create_file()
