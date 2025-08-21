class Wifi:
     #properties
    colour = "White"
    device = "SAMSUNG"                               
    speed = "5MBS"
    range_of_device = "100m"
     #function or method
    def network(self):
        print("it is used to control the network")
    def allow_more_connections(self):
        print("it is also used to give network to more then one devices")
        
     #object
obj = Wifi()
obj.speed = "7MBS"
obj1 = Wifi()
obj1.range_of_device = "200m"
print(obj.colour)
print(obj.device)
print(obj.range_of_device)
print(obj.speed)
obj.allow_more_connections()
obj.network()

print(obj1.range_of_device)