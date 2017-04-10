import calpy


def main():
    running = True
    solution = 0.0

    print('Testing calpy, enter a math expression or \'exit\' to exit.')
    while running:
        user_input = input('> ')
        if user_input.lower() == 'exit':
            running = False
        else:
            try:
                solution = calpy.solve(user_input)
            except calpy.CalcSyntaxError as e:
                print(' ', e)
            except calpy.CalcOverflowError as e:
                print(' ', e)
            else:
                print(' ', solution)


if __name__ == '__main__':
    main()
