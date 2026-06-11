class human:
    height = 0
    weight = 0
    speed = 0
    def walk(self):#走路的函式
        self.speed = 10
    def run(self):#跑步的函式
        self.speed = 20
    def talk(self):#說話的函式
        self.speed = 0

harry = human()
print(harry.speed)
harry.run()
print(harry.speed)