import sys
import time
import datetime
import json

sys.path.append('AssembleeNationale')
import AssembleeNationale


assembleeNationale = AssembleeNationale.AssembleeNationale(verbose=2, setup=True)

r = assembleeNationale.downloadSources("AssembleeNationale/data/")
assembleeNationale.processSources("AssembleeNationale/data/", r["updatedSources"])
print(assembleeNationale.search("test"))
print(assembleeNationale.getDossierLegislatifByUid("DLR5L15N37471"))
assembleeNationale.getDossierLegislatifdocumentsByUid("PIONANR5L15B3619")
print(assembleeNationale.getAmendementsByUid("PNREANR5L15B0480"))

"""
filev = open("/home/gabriel/OpenLoi/AssembleeNationale/data/DOSSIERS_LEGISLATIFS/Dossiers_Legislatifs_XV/json/dossierParlementaire/DLR5L15N36287.json")
jsonv = json.load(filev)
ret = assembleeNationale.xtractLastDateDossierParlementaire(jsonv)
print(ret)
"""