def draw_pyramid(rows):
    for i in range(rows):
        # Print leading spaces
        print(' ' * (rows - i - 1), end='')
        # Print asterisks
        print('*' * (2 * i + 1))

# Number of rows for the pyramid
num_rows = 5
draw_pyramid(num_rows)

