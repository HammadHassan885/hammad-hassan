
print("---------------🙌Welcome to my Calculator🔢---------------")

print("-----😊 please enter your choose ❤️-----")

#choose one from these:
print("1. ➕ sum:")
print("2.➖ difference:")
print("3.*️⃣ multiply:")
print("4. ➗ division")
choice = input("please choose from (1,2,3,4):")


a = int(input("enter first number 🥇:"))

b = int(input("enter second number 🥈:"))
sum = a + b
difference = a - b
multiply = a * b
division = a / b

#choices
if choice ==  '1':
    print("sum of two numbers is 🤌:" , sum)
elif choice == '2':
    print("difference of two numbers is 🤌:" , difference)
elif choice == '3' :
    print("multiplication of two numbers is 🤌: " , multiply)
elif choice == '4' :
    if b != 0:
        print("division of two numbers is 🤌" , division)
    else :
        print("division by zero is not possible ❌")
else:
  print("selection is invalid 😔")