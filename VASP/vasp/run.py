'''
Created on Mar 28, 2012

@author: chtho
'''


class Run(object):
    '''
    Class generating RUN files
    '''

    def __init__(self, path, title, project, walltime,
                 nodes, vasp_version, computer, filename_suffix=''):
        '''
        Constructor
        '''
        self.path = path
        self.title = title
        self.project = project
        self.walltime = walltime
        self.nodes = nodes
        self.vasp_version = vasp_version
        self.computer = computer
        self.filename_suffix = filename_suffix

    def create_file(self):
        if self.computer == 'pdc':
            self._create_PDC_file()
        elif self.computer == 'nsc':
            self._create_NSC_file()

    def _create_PDC_file(self):
        f = open("%s/RUN%s" % (self.path, self.filename_suffix), 'w')
        f.write("#!/bin/bash\n")
        f.write("#PDC run file\n")
        f.write("#PBS -N %s\n" % self.title)
        f.write("#PBS -l walltime=%s\n" % self.walltime)
        f.write("#PBS -l mppwidth=%i\n" % self.nodes)
        f.write("#PBS -e error_file.e\n")
        f.write("#PBS -o output_file.o\n")
        f.write('\n' * 2)
        f.write("#Setting correct working directory\n")
        f.write("PERMDIR=$PBS_O_WORKDIR\n")
        f.write("cd ${PERMDIR}\n")
        f.write('\n')
        f.write("#Loading modules\n")
        f.write(". /opt/modules/default/etc/modules.sh\n")
        f.write("module add vasp/%s\n" % self.vasp_version)
        f.write('\n')
        f.write("#Run calculation\n")
        f.write("aprun -n %i /pdc/vol/vasp/%s/vasp\n" % (self.nodes,
                                                         self.vasp_version))
        f.close()

    def _create_NSC_file(self):
        f = open("%s/RUN%s" % (self.path, self.filename_suffix), 'w')
        f.write("#!/bin/bash\n")
        f.write("#NSC run file\n")
        f.write("#SBATCH -J %s\n" % self.title)
        f.write("#SBATCH -t %s\n" % self.walltime)
        f.write("#SBATCH -N %i\n" % self.nodes)
        f.write("#SBATCH %s\n" % self.project)
        f.write('\n' * 2)
        f.write("#Setting correct working directory\n")
        f.write("PERMDIR=%s\n" % self.path)
        f.write("cd ${PERMDIR}\n")
        f.write('\n')
        f.write("#Run calculation\n")
        f.write("mpprun /software/apps/vasp/%s/default/vasp-half" %
                (self.vasp_version))

if __name__ == '__main__':
    path = '/Users/chtho/Desktop'
    title = 'test'
    project = '-A liu1 -p green'
    walltime = "00:00:00"
    nodes = 1
    vasp_version = "1.1.1"
    Run(path, title, project, walltime, nodes, vasp_version,
        'pdc', '_pdc').create_file()
    Run(path, title, project, walltime, nodes, vasp_version,
        'nsc', '_nsc').create_file()