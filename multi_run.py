import hybrid_lib as hl
import subprocess


test_values_etaS = ["0.08","0.12","0.16"]
test_values_ecrit = ["0.4","0.5"]
test_values_eta0 = ["3.7"]
test_values_sigEta = ["1.4"]

Nevents = 1000
centrality="20-50"
icfile  = "/home/palermo/vhlle/ic/glissando/sources.LHC."+centrality+".dat"
count=0
for EtaS in test_values_etaS:
	for Ecrit in test_values_ecrit:
		for Eta0 in test_values_eta0:
			for SEta in test_values_sigEta:
				subprocess.run(["bsub","-q","theoq","-B","-N","-e","error"+str(count)+".txt","-o","output"+str(count)+".txt","python3","custom_call.py",icfile,centrality,"etaS="+EtaS,"e_crit="+Ecrit,"eta0="+Eta0,"sigEta="+SEta])
				count = count +1
