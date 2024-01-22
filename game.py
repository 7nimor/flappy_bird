import random


def game():
    print('Welcome to my game! :/')
    num = 1
    print('****0:left,   1:right****')
    l = int(input("how rand you want play?: "))
    print('..........')
    me=0
    computer=0
    while num <= l:
        choice = int(input('0 or 1?: '))
        rand = random.randint(0, 1)
        if choice != rand:
            print('computer win')
            computer+=1
        else:
            print('you win')
            me+=1
        num += 1
    print(f'You win {me} times and Computer win {computer} times')
    print('Thanks for playing......')

game()
