import sys
import os
from tkinter import Tk
from ClienteGUI import ClienteGUI
os.environ.__setitem__('DISPLAY', ':0.0')	
if __name__ == "__main__":
	try:
		addr = '10.0.0.10'
		port = 25000
	except:
		print("[Usage: Cliente.py]\n")	
	
	root = Tk()
	
	# Create a new client
	app = ClienteGUI(root, addr, port)
	app.master.title("Cliente Exemplo")	
	root.mainloop()
	
