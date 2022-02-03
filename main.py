import sys
sys.path.append('AssembleNationale')
import AssembleNationale


assembleNationale = AssembleNationale.AssembleNationale(verbose=0)

r = assembleNationale.downloadSources("AssembleNationale/data/")
assembleNationale.processSources("AssembleNationale/data/", r["updatedSources"])


