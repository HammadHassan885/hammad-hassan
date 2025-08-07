total=0
for even in range(1,101):
    if even%2==0:
        print(even)
        total += even
print("sum of even numbers from 2 to 100 is:" ,total) 