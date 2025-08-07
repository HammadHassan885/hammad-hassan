
print('''
                          !                         !
               !          |>>>                      |>>>        !
               |>>>       |>>>                      |>>>        | >>>
               |          |>>>                      |>>>        |
              .|.         |_|          .|.
            /     \       |WWWWWWWWWWWWWWWWWWWWWWWWW|        /     \     
          /         \     |    )~(    |      /         \               
        /             \   |   (                 )   |    /             \    
      /                 \ |   )                 (   |  /                 \    
     #################### |  (                   )  | WWWWWWWWWWWWWWWWWWWW
     |[ ] [ ] [] [ ] [ ]| |  )                   (  | |/\/\/\/\/\/\/\/\/\|
     | |   |  /\  |   | | | (                     ) | | |   |  /\  |   | | 
     | |   | /  \ |   | | |=<_>=| | |   | /  \ |   | |
     | |   ||    ||   | | | )                     ( | | |   ||    ||   | |
     | |   ||    ||   | | |(!!!!!!!!!!!!!!!!!!!!!!!)| | |   ||    ||   | |
     | |   ||||   | | |)| || || || |(| | |   ||_||   | |
     ||||    |||| |(| || || || |)| ||||    |||_|    
                          |)||||||||_(|lc ''')
print("🤌 Welcome in The Secret Castle Story 😶")
print("You stand in front of the mysterious castle . there are three different paths.")
print("1. Red Door 🔴")
print("2. Blue Door 🔵")
print("3. Green Door 🟢")
choice = int(input("Select One Option from these three:(1/2/3)"))
if(choice==1):
    print("You walk 🚶‍➡️ into a long , dark 🌑 hallway")
    print(" You hear🧏 someone calling for help 💁‍♂️")
    print("you have two choices 💁‍♂️")
    print("1. Free The Fairy 🧚‍♂️")
    print("2. Pickup a Book 📙")
    red_choice = int(input("choose one option from these two options :(1/2)"))
    if(red_choice == 1):
        print("you have helped the fairy 🧚‍♂️")
        print("fairy 🧚‍♂️ is impressed ❤️ by you and then she gives you an invisible key 🗝️")
        print("you reached a megical  sealed 🔏 door 🚪")
        print("Now you have two  other choices 💁‍♂️")
        print("1. unlock he door by key 🗝️ :")
        print("2. unlock the door by breaking  it :")
        key_choice = int(input("choose one option from these two optios:(1/2)"))
        if(key_choice == 1):
            print("you have used the key which was given by Fairy 🧚‍♂️ to unlock the door")
            print("you have win the game because you have selected a right path to unlock the door")
        else:
            print("you have tried to break the door")
            print("Guards heared the noice  and catch you")
            print("Game over")
    elif(red_choice == 2): 
      print("you Picked up a Book")
      print("A Monster appears from the book and asks you a riddle")
      print("Now again you have to choices")
      print("1. you have to give right answer of question asked by monster")
      print("2. you have  given wrong answer of question asked by monster")
      red_choice1=input("choose one option from these two optios:(1/2)")
      if(red_choice1 == 1):
           print("you gave the right answer of the question")
           print("you win the game")
      else:
           print("you have given wrong answer")
           print("you are turned into a stone")
           print("game over")
    else:
     print(" you have selected wrong path ")
     print("you lose")
elif(choice == 2):
   print("You have selected Blue Door")
   print("you enter an icy hall")
   print("A frozen Ice Guardian stands before you")
   print("Now you have two options here")
   print("1. Take a Fire Torch")
   print("2. Drink the Magic Potion")
   blue_choice = int(input("choose one option from these two options :(1/2)"))
   if(blue_choice == 1):
       print("you have taken a fire torch")
       print("The Guardian starts Melting")
       print("Now you have other two choices")
       print("1. help the guardian and get reward")
       print("2. run ahead")
       blue_choice3 = int(input("Select one option from these two options: (1/2)"))
       if(blue_choice3 == 1):
           print("you have help the guardian")
           print("guardian gave you a reward")
           print("you won the game")
       else:
           print("you have run ahead")
           print("the guardian gets angry and attacked on you")
           print("you lose")
   elif(blue_choice == 2):
       print("you have drank the magic potion")   
       print("you become invisible")    
       print("yoy enter a hall of mirros")
       print("Now you have two more choices")
       print("1. you have to walk straight")
       print("2. you get lost as the potion fades")
       blue_choice6 = input("you have to select one option from these two options: (1/2)")
       if(blue_choice6 == 1):
           print("you walked straight and find a secret to exit safely")
           print("you won the game")
       else:
           print("you get lost as the potion fades")
           print("you lose")
   else:
      print("you have selected wrong path ")   
      print("you lose")  
else:
    print("you have selected green door")    
    print("A poisonous jungle filled with living plants")  
    print("Here you have two options")
    print("1. pick up the magic flute")
    print("2. take the wooden sword")
    green_choice1 = int(input("select one option from these two options: (1/2)"))
    if(green_choice1 == 1):
        print("you have picked up the magic flute")
        print("the plants fall asleep due to magic flute")
        print("Here you have two options")
        print("1. Play the flute near the pond")
        print("2. swim across the pond")
        green_choice2 = int(input("select one from these two options: (1/2)"))
        if(green_choice2 == 1):
            print("A secret path opened under the water and can pass the pond by this path safely")
            print("you win")
        else:
            print("you have to swim across the pound but it is not safe")
            print("A crocodile killed you in the pond")
            print("you lose")
    elif(green_choice1 == 2):
        print("you have taken a wooden sword") 
        print("The poisonous plants attacked on you") 
        print("now you are injured due to plants attack") 
        print("Here you have two options")
        print("1. search for healing")
        print("2. keep going injured")
        green_choice3 = int(input("select one from these two options : (1/2)"))
        if(green_choice3 == 1):
            print("you saerched some herbs to heal your injuries")
            print("you have found these herbs and applied on injuries and gets recover")
            print("now you are able to escape from the poisonous jungle")
            print("you have not won because its nutral")
            print("here you have other two choices")
            print("1. apply ")
            print("2. eat ")
            print("select one option from these two: (1/2)")
            apply_eat = int(input("elect one option from these two: (1/2)"))
            if(apply_eat == 1):
                print("you have applied the herbs on your injuries and you become healthy")
                print("you won the game")
            else:
                print("you have eat the herbs and it is wrong")
                print("you lose the game")
        else:
            print("you have not searched the herbs to heal your self")
            print("so your health become zero and you are died")
            print("you lose")
    else:  
        print("you have selected wrong path")   
        print("you have lost the game")
        print("you are a loser")