import random
import math
import statistics

# Banish strategies are as follows
# 0: Banish any non-blooper
# 1: Banish Bullet Bill, then Black-White-Coloured, then Triple-Coloured
# 2: Banish Bullet Bill, then Triple-Coloured, then Black-White-Coloured
# 3: Banish Bullet Bill, then anything that doesn't contribute to my lowest coloured pixel count (excluding bloopers)
# 4: Banish Bullet Bill, then anything that contributes to my highest coloured pixel count (excluding bloopers)
# 5: Banish bloopers, don't let the man tell you what to do

# Macrometeorite isn't a thing that exists, presently item drop is being ignored. 100% item drop isn't hard to get, dangit.
# CURRENTLY ONLY STRATEGY ZERO FUNCTIONS

monsterData = {
	0: ("Bullet Bill", [0,0,0,0]),
	1: ("Buzzy Beetle/Goomba", [1,1,0,0]),
	2: ("Koopa Troopa", [1,0,1,0]),
	3: ("Tektite", [1,0,0,1]),
	4: ("Octorok", [0,3,0,0]),
	5: ("Zol", [0,0,3,0]),
	6: ("Keese", [0,0,0,3]),
	7: ("Blooper", [3,0,0,0])
}

class eightBitSim():
	def __init__(self, itemdrop = 100, olfaction = True, wish = False, enamorang = False, banishes = 2, nonolfactcopies = 2, strategy = 0):
		self.itemdrop = itemdrop
		self.olfaction = olfaction
		self.nonolfactcopies = nonolfactcopies
		self.banishes = banishes
		self.wish = wish
		self.enamorang = enamorang
		self.strategy = strategy
	
	def prepareRun(self):
		self.comQueue = []
		self.zoneMonsters = [0, 1, 2, 3, 4, 5, 6, 7]
		self.turnsspent = 0
		self.pixels = [0, 0, 0, 0]
		self.remainingBanishes = self.banishes
		self.olfactionUsed = False
		random.seed()
		
	def shouldIBanishThis(self, monster):
		if self.remainingBanishes == 0:
			return False
		if self.strategy == 0:
			return monster != 7
		return False
	
	def craftPixels(self):
		while self.pixels[1] > 0 and self.pixels[2] > 0 and self.pixels[3] > 0:
			if logging:
				print("> > Crafted one of each pixel into a white pixel")
			self.pixels[0] = self.pixels[0] + 1
			self.pixels[1] = self.pixels[1] - 1
			self.pixels[2] = self.pixels[2] - 1
			self.pixels[3] = self.pixels[3] - 1
			if logging:
				print("> > Now have " + str(self.pixels[0]) + " white pixels.")
			
	def fightMonster(self, monster):
		if self.shouldIBanishThis(monster):
			self.remainingBanishes -= 1
			self.zoneMonsters.remove(monster)
			if logging:
				print("> > > Banished " + monsterData[monster][0]+ ", " + str(self.remainingBanishes) + " banishes left")
			return False
		if monster == 7 and not self.olfactionUsed:
			if logging:
				print("> > > Sniffing the Blooper as hard as possible")
			self.olfactionUsed = True
			for i in range(2 + self.nonolfactcopies if self.olfaction else self.nonolfactcopies):
				self.zoneMonsters.append(7)
		for i in range(4):
			self.pixels[i] += monsterData[monster][1][i]
		return True
			
			
	def runAdv(self):
		reroll = True
		adv = ""
		while reroll:
			reroll = False
			adv = random.choice(self.zoneMonsters)
			if logging:
				print("> > Rolled " + monsterData[adv][0] + " as monster")
			if (adv in self.comQueue) and (random.randint(1, 4) > 1) and not (self.olfactionUsed and self.olfaction and adv == 7):
				reroll = True
				if logging:
					print("> > > Rejected, rerolling!")
		self.comQueue.append(adv)
		self.comQueue = self.comQueue[-5:]
		if logging:
			print("> > Locked in. Combat queue is now " + str(list(map(lambda x: monsterData[x][0], self.comQueue))))
		return self.fightMonster(adv)
	
	def runEightBitRealm(self):
		self.prepareRun()
		if logging:
			print("> Starting turn 1 with no pixels")
		if self.wish:
			if logging:
				print("> Wishing for a Blooper")
				print("> Shim Shalla Slooper, now you can fight a Blooper!")
			self.fightMonster(7)
			self.turnsspent += 1
		while self.pixels[0] < 30:
			if logging:
				print("> Starting turn " + str(self.turnsspent) + " with " + str(self.pixels[0]) + " white pixels. (" + str(self.pixels[1]) + " red, " + str(self.pixels[2]) + " blue, " + str(self.pixels[3]) + " green)")
			if self.runAdv():
				self.turnsspent += 1
				self.craftPixels()
		if logging:
			print("> Starting turn " + str(self.turnsspent) + " with " +str(self.pixels[0]) + " white pixels.")
			print("> Digital key purchased")
			print("> Digital key created in " + str(self.turnsspent) + " turns")
		return self.turnsspent
	
	def runSimulations(self, runcount = 1000):
		runs = []
		for i in range(runcount):
			if logging:
				print("-----------------------------------")
				print("Simulating run " + str(i))
			runs.append(self.runEightBitRealm())
		return [statistics.mean(runs), statistics.harmonic_mean(runs), statistics.median(runs), statistics.pstdev(runs)]
		


logging = True

if __name__ == "__main__":
	print(
		eightBitSim(
		itemdrop = 100, 	# Unimplemented, but some day may reflect your item drop %
		olfaction = True, 	# Do you have transcendent olfaction?
		wish = True, 		# Are you wishing to fight a blooper to sniff it?
		enamorang = False, 	# Unimplemented, but some day may ask if you're going to enamorang a blooper
		banishes = 3, 		# How many banishes do you have access to?
		nonolfactcopies = 1,# Aside from transcendent olfaction, how many weak sniffs do you have? (Galapagosian, Offer Latte, etc)
		strategy = 0		# Unimplemented, but some day may determine your banish strategy
		).runSimulations())
