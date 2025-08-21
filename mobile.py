class Mobile:
          #properties
    company = "SAMSUNG"
    ram = 8
    rom = 128
    colour = "sky blue"
          #functions
    def communication(self):
        print("it is used for communication")
    def entertainment(self):
        print("it is used for entertainment purpose")
    def watch_movies(self):
        print("it is used for watching movies")
    #object
obj = Mobile()
print(obj.company)
print(obj.ram)
print(obj.rom)
print(obj.colour)
obj.communication()
obj.entertainment()  
obj.watch_movies()
