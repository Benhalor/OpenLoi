import os
import sys
import time

sys.path.append('AssembleeNationale')
import AssembleeNationale

sys.path.append('Senat')
import Senat



if os.getenv("POSTGRESQL_ADDON_DB") is not None:
    # Clever cloud
    assembleeNationale = AssembleeNationale.AssembleeNationale(
        database=os.getenv("POSTGRESQL_ADDON_DB"),
        userDatabase=os.getenv("POSTGRESQL_ADDON_USER"),
        passwordDatabase=os.getenv("POSTGRESQL_ADDON_PASSWORD"),
        hostDatabase=os.getenv("POSTGRESQL_ADDON_HOST"),
        portDatabase=os.getenv("POSTGRESQL_ADDON_PORT"),
        verbose=2,
        setup=True)
    senat = Senat.Senat(
        database=os.getenv("POSTGRESQL_ADDON_DB"),
        userDatabase=os.getenv("POSTGRESQL_ADDON_USER"),
        passwordDatabase=os.getenv("POSTGRESQL_ADDON_PASSWORD"),
        hostDatabase=os.getenv("POSTGRESQL_ADDON_HOST"),
        portDatabase=os.getenv("POSTGRESQL_ADDON_PORT"),
        verbose=2)
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

    senat = Senat.Senat(
        database='postgres',
        userDatabase='postgres',
        passwordDatabase='password',
        hostDatabase='localhost',
        portDatabase='5432',
        verbose=2)

#senat.reloadDatabase("Senat/data/")

r = assembleeNationale.downloadSources("AssembleeNationale/data/")
assembleeNationale.processSources(
    "AssembleeNationale/data/", r["updatedSources"], replace=True)


print("Finished all dump")
