class Airpods:
       #properties
    colour = "White"
    shape = "circular"
    battery = "10V"
    charging_time = "1H"
       #functions
    def reduce_noice(self):
        print("Airpods are used to reduce noice")
    def clearity(self):
        print("Airpods are used for clear sound of any movie or any new")    
   #object
obj = Airpods()
obj.battery = "20V"

obj1 = Airpods()
obj.charging_time = "1.5H"

print(obj.colour)
print(obj.shape)
print(obj.battery)
print(obj.charging_time)

obj.reduce_noice()
obj.clearity()

print(obj1.charging_time)