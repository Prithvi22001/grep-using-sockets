import os
def make_wordlist_file():
	cmd ='curl https://raw.githubusercontent.com/Prithvi22001/PatternMatchingUsingSocket/master/wordlist.txt -o wordlist.txt'
	os.system(cmd)
	return

if __name__=='__main__':
	make_wordlist_file()


	