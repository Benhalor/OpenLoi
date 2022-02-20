import sys

sys.path.append('AssembleeNationale')
import AssembleeNationale


# Clever cloud
assembleeNationale = AssembleeNationale.AssembleeNationale(
    database='assembleenationale',
    initialDatabase = os.getenv("POSTGRESQL_ADDON_DB"),
    userDatabase = os.getenv("POSTGRESQL_ADDON_USER"),
    passwordDatabase = os.getenv("POSTGRESQL_ADDON_PASSWORD"),
    hostDatabase = os.getenv("POSTGRESQL_ADDON_HOST"),
    portDatabase = os.getenv("POSTGRESQL_ADDON_PORT"),
    verbose=2, 
    setup=True)

# Local
"""assembleeNationale = AssembleeNationale.AssembleeNationale(
    database='assembleenationale',
    initialDatabase='postgres',
    userDatabase='postgres',
    passwordDatabase='password',
    hostDatabase='localhost',
    portDatabase='5432',
    verbose=2,
    setup=False)"""

r = assembleeNationale.downloadSources("AssembleeNationale/data/")
assembleeNationale.processSources(
    "AssembleeNationale/data/", r["updatedSources"])
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
