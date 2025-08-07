# dict = {
# "name":"hammad hassan",
# "roll no":12345,
# "marks":96,
# }
# print(dict)

# #----------------------lenth--------------------------:
# print(len(dict))

# #----------------------add new key value pair-----------------------:
# dict["key"]="value"
# print(dict)

# #----------------------check mutable---------------------------:
# dict["marks "]= 98
# print(dict)
# print(dict["name"])

# #--------------------usning get method to acess----------------------:
# print(dict.get("marks"))

# #--------------------pop method to remove a pair----------------------:
# dict.pop("name")
# print(dict)



# dict = {
#  "name" : "hammad hassan",
#     "subject" : {
#     "phy" : 97,
#     "chem" :98,
#     "eng" : 99,
#     }
# }
# print(dict)
# #--------------------------single value from sub_dict:
# print(dict["subject"]["chem"])

# #--------------------------keys method:
# print(dict.keys())

# #------------------------converting keys into list (type casting):
# print(list(dict.keys()))

# #-------------------------length of dict:
# print(len(dict))

# #-------------------------values method:
# print(dict.values())

# #------------------------items method:
# print(dict.items())
# print(list(dict.items()))

#------------------------access any pair by index:

# dict = {
#  "name" : "hammad hassan",
#     "subject" : {
#     "phy" : 97,
#     "chem" :98,
#     "eng" : 99,
#     }
# }
# print(dict)

# acessing_pairs = list(dict.items())
# print(acessing_pairs[0])  #----acess any pair by index 

#--------------------usning get method to acess----------------------:
# print(dict.get("marks"))

#-------------------update method:
# new_dict = {"age" : 17 , "roll no" : 1234,}
# dict.update(new_dict)
# print(dict)



#------------------------Set in Python--------------------

# collection = {1,2,3,4,5,6,"hello","world"}
# print(collection)
# print(type(set))
# print(len(set))
#--------------------null set or empty set:
# empty_set = set()
# print(empty_set)

#-------------------add method:
# collection.add(7)
# collection.add(8)
# empty_set.add("hammad")
# print(collection)
# print(empty_set)

#-------------------remove method:
# collection.remove(4)
# print(collection)

#------------------passing tupple by add method:
# collection.add((9,10,11,12))
# print(collection)

#------------------clear method:
# collection.clear()
# print(collection)
# print(len(collection))

#------------------pop method:
# collection.pop()
# print(collection)

#------------------union method:
student1 = {1,2,3,4,5,6}
student2 = {5,6,7,8,9}
# print (student1)
# print(student2)
# print(student1.union(student2))


#------------------intersection method:
print(student1.intersection(student2))