import os
import sys
import time

sys.path.append('AssembleeNationale')
import AssembleeNationale

if os.getenv("POSTGRESQL_ADDON_DB") is not None:
    # Clever cloud
    assembleeNationale = AssembleeNationale.AssembleeNationale(
        database=os.getenv("POSTGRESQL_ADDON_DB"),
        userDatabase = os.getenv("POSTGRESQL_ADDON_USER"),
        passwordDatabase = os.getenv("POSTGRESQL_ADDON_PASSWORD"),
        hostDatabase = os.getenv("POSTGRESQL_ADDON_HOST"),
        portDatabase = os.getenv("POSTGRESQL_ADDON_PORT"),
        verbose=2, 
        setup=False)
else:
    # Local
    assembleeNationale = AssembleeNationale.AssembleeNationale(
        database='postgres',
        userDatabase='postgres',
        passwordDatabase='password',
        hostDatabase='localhost',
        portDatabase='5432',
        verbose=2,
        setup=False)

while True:
    r = assembleeNationale.downloadSources("AssembleeNationale/data/")
    assembleeNationale.processSources(
        "AssembleeNationale/data/", r["updatedSources"])
    print("Finished all dump")
    time.sleep(7200)

# Tests      
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
