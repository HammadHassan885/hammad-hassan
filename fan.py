class Fan:
          #properties
    company = "SuperCool Fans"
    speed = 50
    color = "White"
    wings = 3
          #function
    def turnOn(self):
        print("make the room cool with air")
        #object
obj = Fan()
obj1 = Fan()
obj.company = "Cool Breeze Fans"
obj1.color = "black"
print(obj.company)
print(obj.speed)
print(obj.color)
print(obj.wings)
obj.turnOn()
print(obj1.color)