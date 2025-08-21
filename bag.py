class Bag:
        #properties
    colour = "black"
    size = "medium"
    zips = 4
    strips = 2
        #functions
    def holdBooks(self):
        print("it is used to hold things")
    def holdClothes(self):
        print("it is used to hold clothes and luggage")
        #object
obj = Bag()
obj.colour = "red"
obj1 = Bag()
obj1.zips = 5
print(obj.colour)        
print(obj.size)
print(obj.zips)
print(obj.strips)
obj.holdBooks()
obj.holdClothes()