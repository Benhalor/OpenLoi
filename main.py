import sys
import time
import datetime

sys.path.append('AssembleeNationale')
import AssembleeNationale


assembleeNationale = AssembleeNationale.AssembleeNationale(verbose=2, setup=False)

r = assembleeNationale.downloadSources("AssembleeNationale/data/")
assembleeNationale.processSources("AssembleeNationale/data/", r["updatedSources"])
print(assembleeNationale.search("'');DROP TABLE DOSSIERS_LEGISLATIFS;--"))
print(assembleeNationale.getDossierLegislatifByUid("PIONANR5L15B3619"))