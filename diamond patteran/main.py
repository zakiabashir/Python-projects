

def dimond(row):
    # upper part of diamod
    for j in range(row ):
        print(' ' * (row - j - 1), end = '')
        print('*' * (2 * j + 1))
        # lower part of diamond
    for j in range(row - 2, -1, -1):
        print(' ' * (row - j - 1), end = '')
        print('*' * (2 * j + 1))    
rows = 5
dimond(rows)
        