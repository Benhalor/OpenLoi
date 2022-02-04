import sys
import time
import datetime

sys.path.append('AssembleeNationale')
import AssembleeNationale


assembleeNationale = AssembleeNationale.AssembleeNationale(verbose=2)

r = assembleeNationale.downloadSources("AssembleeNationale/data/")
assembleeNationale.processSources("AssembleeNationale/data/", r["updatedSources"])
assembleeNationale.search("covid")
