import mysql.connector

def getAreaCode(inp):
	if inp == "east asia and pacific":
		return "EAP"
	elif inp == "europe and central asia":
		return "ECA"
	elif inp == "latin america and caribbean":
		return "LAC"
	elif inp == "middle east and north africa":
		return "MENA"
	elif inp == "south asia":
		return "SA"
	elif inp == "sub-saharan africa":
		return "SSA"
	else:
		return NONE

class Database():
	def __init__(self, host, user, password, dbname):
		self.host = host
		self.user = user
		self.password = password
		self.dbname = dbname
		self._conn = mysql.connector.connect(host = host, user = user, password = password, database = dbname)
		self._cursor = self._conn.cursor()

	def __enter__(self):
		return self

	def __exit__(self, exc_type, exc_val, exc_tb):
		self.close()

	@property
	def connection(self):
		return self._conn
	
	@property
	def cursor(self):
		return self._cursor

	def commit(self):
		self.connection.commit()

	def close(self, commit = True):
		if commit:
			self.commit()
		self.connection.close()

	def fetchall(self):
		return self.cursor.fetchall()

	def fetchone(self):
		return self.cursor.fetchone()

	def query(self, query, params = None):
		self.cursor.execute(query, params or ())
		return self.fetchall()

	def getMalePopulation_byLocYear(self, year, region):
		sql = "SELECT M_Population FROM region_year_pop WHERE Name = %s and year = %s"
		infos = self.query(sql, (region, year))
		print("Male Population: ", infos)

	def getFemalePopulation_byLocYear(self, year, region):
		sql = "SELECT F_Population FROM region_year_pop WHERE Name = %s and year = %s"
		infos = self.query(sql, (region, year))
		print("Female Population: ", infos)
	
	def getAveAge_byGenLocYear(self, gender, year, region):
		sql = "SELECT aveage, INITIAL FROM region_year_aveage WHERE year = %s and Name = %s AND INITIAL = %s"
		result = self.query(sql, (year, region, gender))
		print("Average Marriage Age in this location is: ", result)

	def addYear(self, year, code, areayear):
		sql = "INSERT INTO year VALUES (%s,%s,%s)"
		self.cursor.execute(sql, (year, code, areayear))
		self.commit()

	def addMalePop(self, population, areayear):
		sql = "INSERT INTO population VALUES (NULL,%s,%s)"
		self.cursor.execute(sql, (population, areayear))
		self.commit()
		
	def addFemalePop(self, population, areayear):
		sql = "INSERT INTO population VALUES (%s,NULL,%s)"
		self.cursor.execute(sql, (population, areayear))
		self.commit()

	def addAveAge(self, aveage, areayear, gender):
		sql = "INSERT INTO aveage VALUES (%s, %s, %s)"
		self.cursor.execute(sql, (gender, aveage, areayear))
		self.commit()	

	def deletePopData(self, areayear):
		sql = "DELETE FROM population WHERE AREA_YEAR = %s"
		self.cursor.execute(sql, (areayear, ))
		self.commit()

	def deleteAgeData(self, areayear):
		sql = "DELETE FROM aveage WHERE AREA_YEAR = %s"
		self.cursor.execute(sql, (areayear, ))
		self.commit()

	def deleteKey(self, areayear):
		sql = "DELETE FROM year WHERE AREA_YEAR = %s"
		self.cursor.execute(sql, (areayear, ))
		self.commit()

	def updateFPop(self, population, areayear):
		sql = "UPDATE population SET F_Population = %s WHERE AREA_YEAR = %s"
		self.cursor.execute(sql, (population, areayear))
		self.commit()

	def updateMPop(self, population, areayear):
		sql = "UPDATE population SET M_Population = %s WHERE AREA_YEAR = %s"
		self.cursor.execute(sql, (population, areayear))
		self.commit()

	def updateAvgAge(self, avgage, areayear, gender):
		sql = "UPDATE aveage SET AveAge = %s WHERE AREA_YEAR = %s AND INITIAL = %s"
		self.cursor.execute(sql, (avgage, areayear, gender))
		self.commit()


def main():
	rep = ""
	run = True
	while run == True:
		print("Hello!")
		print("Available regions: 'east asia and pacific','europe and central asia','latin america and caribbean','middle east and north africa','south asia','sub-saharan africa'")
		print("What do you want to do?")
		print("1 for getting data")
		print("2 for adding data")
		print("3 for deleting data")
		print("4 for updating data")
		print("quit to close this program")

		# getting input
		choice = input("Type your choice here :")
		choice = choice.lower()
		
		if choice == "1":
			print("***" *15)
			print("What do you want to know?")
			print("You can choose one of these: 'Male Population', 'Female Population', 'Average Age'")
			data = input("Type your choice here: ")
			rep = data.lower()
			if rep == "male population":
				place = input("Of where? > ")
				place = place.title()
				rep = place.lower()
				if rep in ("east asia and pacific","europe and central asia","latin america and caribbean","middle east and north africa","south asia","sub-saharan africa"):
					year = input("When? > ")
					try:
						with Database("localhost","root","Wellthissucks1","testing") as db:
							db.getMalePopulation_byLocYear(year, place)
					except mysql.connector.Error as e:
						print("There is no data about this year")
				else:
					print("Unknown region")

			elif rep == "female population":
				place = input("Of where? > ")
				place = place.title()
				rep = place.lower()
				if rep in ("east asia and pacific","europe and central asia","latin america and caribbean","middle east and north africa","south asia","sub-saharan africa"):
					year = input("When? > ")
					try:
						with Database("localhost","root","Wellthissucks1","testing") as db:
							db.getFemalePopulation_byLocYear(year, place)
					except mysql.connector.Error as e:
						print("There is no data about this year")

			elif rep == "average age":
				place = input("Of where? > ")
				place = place.title()
				rep = place.lower()
				if rep in ("east asia and pacific", "europe and central asia", "latin america and caribbean", "middle east and north africa", "south asia", "sub-saharan africa"):
					year = input("When? > ")
					gender = input("Which gender would you like to get data from? Type 'Male' or 'Female' > ")
					rep = gender.lower()
					if rep == "male" or "female":
						try:
							with Database("localhost","root","Wellthissucks1","testing") as db:
								if rep == "male":
									db.getAveAge_byGenLocYear("M", year, place)
								elif rep == "female":
									db.getAveAge_byGenLocYear("F", year, place)
						except mysql.connector.Error as e:
							print("There is no data about this year")

					else:
						print("Invalid! Male or Female only.")

			else:
				print("Invalid option! Make sure your syntax is right :)")

			cont = input("Do you want to do anything else? Type 'yes' or 'no' >")
			cont = cont.lower()
			if cont == 'no':
				run = False
			elif cont == 'yes':
				run = True
			else:
				print("Invalid choice! The program will close now.")
				run = False

		elif choice == "2":
			print("***" *15)
			placement = input("What kind of data do you want to add? 'Year', 'Male Population', or 'Female Population' >")
			rep = placement.lower()
			if rep == "year":
				data = input("Where and when? (i.e: South Asia:2003) > ")
				word = data.split(':')
				code = getAreaCode(word[0].lower())
				year = word[1]
				areayear = code + year
				with Database("localhost","root","Wellthissucks1","testing") as db:
					db.addYear(year, code, areayear)
					print("Inserted a new year")

			elif rep == "male population":
				data = input("How many, where and when? (i.e: 200000:South Asia:1992) > ")
				word = data.split(':')
				code = getAreaCode(word[1].lower())
				year = word[2]
				areayear = code + year
				try:
					with Database("localhost","root","Wellthissucks1","testing") as db:
						db.addMalePop(word[0], areayear)
				except mysql.connector.Error as e:
					with Database("localhost","root","Wellthissucks1","testing") as db:
						db.addYear(year, code, areayear)
						db.addMalePop(word[0], areayear)
				print("Inserted a male population")


			elif rep == "female population":
				data = input("How many, where and when? (i.e: 200000:South Asia:1992) > ")
				word = data.split(':')
				code = getAreaCode(word[1].lower())
				year = word[2]
				areayear = code + year
				try:
					with Database("localhost","root","Wellthissucks1","testing") as db:
						db.addFemalePop(word[0], areayear)
				except mysql.connector.Error as e:
					with Database("localhost","root","Wellthissucks1","testing") as db:
						db.addYear(year, code, areayear)
						db.addFemalePop(word[0], areayear)
				print("Inserted a female population")

			elif rep == "average age":
				gender = input("Female age or Male age? Type 'male' or 'female' > ")
				gender = gender.lower() 
				if gender == "female":
					print("Type your data in this format: 'how old:where:when' ")
					data = input("Type your data here > ")
					word = data.split(':')
					code = getAreaCode(word[1].lower())
					year = word[2]
					areayear = code + year
					try: 
						with Database("localhost","root","Wellthissucks1","testing") as db:
							db.addAveAge(word[0], areayear, 'F')
					except mysql.connector.Error as e:
						print("Uh oh an error has appeared! ", e)
					print("Updated new female data")


				elif gender == "male":
					print("Type your data in this format: 'how old:where:when' ")
					data = input("Type your data here > ")
					word = data.split(':')
					code = getAreaCode(word[1],lower())
					year = word[2]
					areayear = code + year
					try: 
						with Database("localhost","root","Wellthissucks1","testing") as db:
							db.addAveAge(word[0], areayear, 'M')
					except mysql.connector.Error as e:
						print("Uh oh an error has appeared! ", e)
					print("Updated new male data")

				else:
					print("Invalid gender choice")

			cont = input("Do you want to do anything else? Type 'yes' or 'no' >")
			cont = cont.lower()
			if cont == 'no':
				run = False
			elif cont == 'yes':
				run = True
			else:
				print("Invalid choice! The program will close now.")
				run = False

		elif choice == "3":
			print("***" *10)
			print("A - Delete all data of a region in a specific time")
			print("B - Delete specific data of a region in a specific time")
			placement = input("What do you want to delete? > ")
			rep = placement.lower()
			if rep == "a":
				choice = input("Where and when? (i.e: South Asia:2005) > ")
				word = choice.split(':')
				code = getAreaCode(word[0].lower())
				year = word[1]
				areayear = code + year
				try:
					with Database("localhost","root","Wellthissucks1","testing") as db:
						db.deleteKey(areayear)
				except mysql.connector.Error as e:
					print("Uh oh an error has appeared! ", e)
				print("Deleted all data of " + word[0] + "in" + year)

			elif rep == "b":
				choice = input("Delete the average age or the population? > ")
				rep = choice.lower()
				if rep == "average age":
					data = input("The data of which region and when? (i.e: South Asia:2005) > ")
					word = data.split(':')
					code = getAreaCode(word[0].lower())
					year = word[1]
					areayear = code + year
					try:
						with Database("localhost","root","Wellthissucks1","testing") as db:
							db.deleteAgeData(areayear)
					except mysql.connector.Error as e:
						print("Uh oh an error has appeared! ", e)
					print("Deleted the average age data of " + word[0] + "in " + year)

				elif rep == "population":
					data = input("The data of which region and when? (i.e: South Asia:2005) > ")
					word = data.split(':')
					code = getAreaCode(word[0].lower())
					year = word[1]
					areayear = code + year
					try:
						with Database("localhost","root","Wellthissucks1","testing") as db:
							db.deletePopData(areayear)
					except mysql.connector.Error as e:
						print("Uh oh an error has appeared! ", e)
				print("Deleted the population data of " + word[0] + "in " + year)

			else:
				print("Invalid choice!")

			cont = input("Do you want to do anything else? Type 'yes' or 'no' >")
			cont = cont.lower()
			if cont == 'no':
				run = False
			elif cont == 'yes':
				run = True
			else:
				print("Invalid choice! The program will close now.")
				run = False

		elif choice == "4":
			print("***" *10)
			print("A - Update population data") #how many, when, where, gender
			print("B - Update average marriage age data") #age, area, year, gender
			choice = input("What do you want to change? > ")
			rep = choice.lower()
			if rep == "a":
				gender = input("Female population or Male population? Type 'male' or 'female' > ")
				gender = gender.lower()
				if gender == "female":
					print("Type your data in this format: 'how many:where:when' ")
					data = input("Type your data here > ")
					word = data.split(':')
					code = getAreaCode(word[1].lower())
					year = word[2]
					areayear = code + year
					try: 
						with Database("localhost","root","Wellthissucks1","testing") as db:
							db.updateFPop(word[0], areayear)
					except mysql.connector.Error as e:
						print("Uh oh an error has appeared! ", e)
					print("Updated new female population data")


				elif gender == "male":
					print("Type your data in this format: 'how many:where:when' ")
					data = input("Type your data here > ")
					word = data.split(':')
					code = getAreaCode(word[1],lower())
					year = word[2]
					areayear = code + year
					try: 
						with Database("localhost","root","Wellthissucks1","testing") as db:
							db.updateMPop(word[0], areayear)
					except mysql.connector.Error as e:
						print("Uh oh an error has appeared! ", e)
					print("Updated new male population data")

				else:
					print("Invalid gender choice")

			elif rep == "b":
				gender = input("Female age or Male age? Type 'male' or 'female' > ")
				gender = gender.lower()
				if gender == "female":
					print("Type your data in this format: 'how old:where:when' ")
					data = input("Type your data here > ")
					word = data.split(':')
					code = getAreaCode(word[1].lower())
					year = word[2]
					areayear = code + year
					try: 
						with Database("localhost","root","Wellthissucks1","testing") as db:
							db.updateAvgAge(word[0], areayear, "F")
					except mysql.connector.Error as e:
						print("Uh oh an error has appeared! ", e)
					print("Updated new age data")

				elif gender == "male":
					print("Type your data in this format: 'how old:where:when' ")
					data = input("Type your data here > ")
					word = data.split(':')
					code = getAreaCode(word[1].lower())
					year = word[2]
					areayear = code + year
					try: 
						with Database("localhost","root","Wellthissucks1","testing") as db:
							db.updateAvgAge(word[0], areayear, "M")
					except mysql.connector.Error as e:
						print("Uh oh an error has appeared! ", e)
					print("Updated new age data")

				else:
					print("Invalid gender choice")

			else:
				print("Invalid choice")

			cont = input("Do you want to do anything else? Type 'yes' or 'no' >")
			cont = cont.lower()
			if cont == 'no':
				run = False
			elif cont == 'yes':
				run = True
			else:
				print("Invalid choice! The program will close now.")
				run = False

		elif choice == "quit":
			run = False

		else:
			print("Invalid choice")

	print("The program has been closed.")

main()
