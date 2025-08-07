         #-------------------------------List----------------------------#
# list = [90,91,92,93,94,95]
# print(list)
#...................type of list:..................
# print(type(list))
#...................indexing:......................
# print(list[0])
# print(list[1])

# ................student details...............
# student =["Muhammad Moeen",16, 87,"Hammad Hassan"]
# print(student)
#....................length......................
# print(len(student))
#..................type of given data...............
# print(type(student))
#.............indexing.............
# print(student[1])
# print(student[2])
#.............slicing...............
# print(student[0:1])
# print(student[:2])
# print(student[1:])
#..................checking for mutable.................
# student[1] = 'ali'
# print(student)


#.................append method............
# student =["Muhammad Moeen",16, 87,"Hammad Hassan"]
# student.append("ali")
# print(student)


#..................sort method................
#.................assending by sort method...........
# student =["Muhammad Moeen","Ali","Hammad Hassan"]
# student.sort()
# print(student)
# student =[1,2,4,6,3,5]
# student.sort()
# print(student)


#..................decending by sort method..................
# student =["Muhammad Moeen","Ali","Hammad Hassan"]
# student.sort(reverse=True)
# print(student)


# ....................reverse method..............
# student =["Muhammad Moeen","Ali","Hammad Hassan"]
# student.reverse()
# print(student)

#..................insert method.............
# student =["Muhammad Moeen","Ali","Hammad Hassan"]
# student.insert(0,"saad")
# print(student)

#................remove method..........
# student =[1,2,4,6,4,3,5]
# student.remove(4)
# print(student)

#...................pop method..............
# student =[1,2,4,6,4,3,5]
# student.pop(3)
# print(student)


# student =[1,2,4,6,4,3,5]
# student.copy()
# print(student)


             #-------------------------tuple------------------------------#
# marks = (1,2,4,5,7,9,8,6,3,6)
# print(type(marks))
# print(marks)
# print(marks[4])
# print(marks[5])
# print(marks[0:5])
# print(marks[-3:-5])
# print(len(marks))
# print(marks.count(6))
# print(marks.index(8))


# b=("n", "o", "s", "l", "A")
# print(b)
# print(len(b))
# print(b[0])
# print(b[0:len(b)])
# print(b[:3])
# print(b[2:])

# print(b.count("n"))
# print(b.index("s"))

#-------------------even & odd -----------------------#

# a = int(input("enter any number:"))
# if(a%2==0):
#     print("number is even")
# else:
#     print("number is odd")

#-------------------------sum of two numbers-----------------------#
# a = input("enter two_digit number:")
# num1 = int(a[0])
# num2 = int(a[1])
# sum= num1+num2
# print("sum of two digits is: " , sum)
# if(sum%2==0):
#     print("sum of numbers is even")
# else:
#     print("sum of numbers is odd")


# ------------------------leap year or not ---------------------#

# year = int(input("enter any year:"))

# if(year%4==0 and year%100!=0) or(year%400==0):

#     print("it is a leap year")

# else:

#     print("it is not a leap year")


# #-------------------------pizza order:
# print("Welcome to python pizza🍕 deliveries!")
# bill = 0
# size = input("what size of pizza🍕 do you want? S,M,or L").upper()
# if(size=="S"):
#     bill+=15
# elif(size=="M"):
#     bill+=20
# else:
#  bill+= 25

# add_pepperoni = input("do you want to add pepperoni? Y or N").upper()
# if(add_pepperoni=="Y"):
#     if(size=="S"):
#          bill+=2
#     else:
#          bill+=3

# extra_cheez = input("do you want to add extra cheez? Y or N").upper()
# if(extra_cheez=="Y"):
#     bill+=1

# print(f"final bill is: ${bill}")

