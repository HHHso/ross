x=0
while x<5:
    print(x)
    x=x+1
print("end")

print('---')

x=0
while x<=5:
    print(x)
    x=x+5
    break
print("end")

print('---')

x=0
while x<9:
    x=x+1
    y=1
    while y<10:
        print(str(x)+"*"+str(y)+"="+str(x*y))
        y=y+1
print("end")
