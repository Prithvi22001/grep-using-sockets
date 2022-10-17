import os
from sys import stderr, stdout
from subprocess import PIPE,Popen
def extract_words(query):
	if os.sys.platform.startswith('win'):
		cmd='findstr -r -c:"^'+query.replace("*",'.*')+'$\" wordlist.txt'
	else:
		cmd='grep -ir {query} wordlist.txt'	
		output,error=Popen(cmd,stdout=PIPE,stderr=PIPE).communicate()
		# print(output.decode(),error.decode())
	# print(f"{query}")
	return output.decode()




if __name__=='__main__':
	query=input()
	print(extract_words(query))