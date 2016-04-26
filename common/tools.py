def get_credentials(filename):
    with open(filename) as f:
        return f.readline().rstrip('\n')
