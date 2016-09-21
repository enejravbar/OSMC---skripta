import time
import commands

zazeniPrvic=True;
kontrolaIzpadaMount=0;

print("Zaganjam program za predvajanje seznama!")

def narediMount():
	commands.getoutput("sleep 20")
	commands.getoutput("mount -t cifs -o username=osmc,password=osmc,rw,sec=ntlm //10.10.101.114/osmc/TV-Vhod /home/osmc/pivka")
	print ("Izvedel sem ukaz za mount diska.")
	return

def jeMount():
	stdout=commands.getoutput("df")
	if(stdout.find("/home/osmc/pivka")>-1 ) :
		print ("Share je uspesno mountan.")
		return True
	else :
		print ("Share ni uspesno mountan.")
		return False

def zazeniSeznamPredvajanja():
	
	commands.getoutput("xbmc-send --action='XBMC.Action(Close)'")
	commands.getoutput("xbmc-send --action='XBMC.Action(Close)'")	
	commands.getoutput("xbmc-send --action='XBMC.Action(Close)'")
	commands.getoutput("xbmc-send --action='XBMC.Action(Stop)'")
	commands.getoutput("xbmc-send --action='XBMC.PlayMedia(/home/osmc/pivka/)'")
	commands.getoutput("xbmc-send --action='XBMC.PlayerControl(RepeatAll)'")
	print ("Izvedel sem ukaze  za zagon seznama predvajanja.")


while True :
	
	zacCas= time.time()
	statusMount = jeMount()
	porabljeniCas=time.time()-zacCas
	#print(porabljeniCas)	

	if(zazeniPrvic &  (not statusMount)) :
		print("Share ni bil ze prej mountan, zato sem izvedel ukaz za mount.")
		narediMount()
	if(zazeniPrvic & statusMount) :	
		print("Share je bil ze prej uspesno moutan")

	if(statusMount & zazeniPrvic) :
		
		zazeniSeznamPredvajanja()
		zazeniPrvic=False
	
	if(not zazeniPrvic) :
		# ce je rabil ukaz df vec kot 4 sekunde in je v tem casu povezava bila ponovno vzpostavljena je potrebno ponovno izvrsiti ukaze za predvajanje

		if( (porabljeniCas > 4) & statusMount): 		
			print(porabljeniCas)
			print("Ker je porabljeni cas vecji od 4 sem nastavil kontrolaIzpada na 1")
			kontrolaIzpadaMount=1			

		if(not statusMount):
			print ("NAPAKA! Prislo je do izpada omreznega diska")
			kontrolaIzpadaMount=1
		
		if( (kontrolaIzpadaMount==1) & statusMount) :
			print ("Po izpadu omreznega diska je povezava ponovno vzpostavljena")
			zazeniSeznamPredvajanja()
			kontrolaIzpadaMount=0
	
	time.sleep(2)	
	
		




