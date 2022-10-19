import os
from sys import stderr, stdout
from subprocess import PIPE,Popen
def extract_words(queries):
	
	if type(queries)==list:
		answer={}
		for query in queries: 	
			answer[query]=run_cmd(query)
		print(answer)	
		return answer	
	else:
		output=run_cmd(queries)
		return output


def run_cmd(query):
	if os.sys.platform.startswith('win'):
		cmd='findstr -r -c:"^'+query.replace("*",'.*')+'$\" wordlist.txt'
	else:
		cmd='grep -E ^'+ query.replace("*",".*")+'$ wordlist.txt'
	try:
		output,error=Popen(cmd,stdout=PIPE,stderr=PIPE).communicate()
	except Exception as e:
		return f"Server Error!! {e}"
	return output.decode()	

if __name__=='__main__':
	query=input()
	print(extract_words(query))