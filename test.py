with open('hotmail.txt', 'r') as file:
        line = file.readline()
        gmail, pwd = line.strip().split("|")
        print(gmail)