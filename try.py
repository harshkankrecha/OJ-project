import sys
file1 = open("/Users/harsh/Desktop/demo.py","r") 
print(file1.read())

orig_stdout = sys.stdout
sys.stdout = open('file.txt', 'w')
exec("/Users/harsh/Desktop/demo.py")
sys.stdout.close()
sys.stdout=orig_stdout
output = open('file.txt', 'r').read()
print(output)