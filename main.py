import random, string
import os
from flask import Flask, render_template, request
import subprocess
import logging

app = Flask(  # Create a flask app
	__name__,
	template_folder='index',  # Name of html file folder
	static_folder='static'  # Name of directory for static files
)

##disable log output in terminal
log = logging.getLogger('werkzeug')
log.disabled = False
app.logger.disabled = False

#------

ok_chars = string.ascii_letters + string.digits

@app.route('/')  # What happens when the user visits the site
def base_page():
  return render_template('base.html')

if __name__ == "__main__":  # Makes sure this is the main process
	app.run( # Starts the site
		host='0.0.0.0',  # Establishes the host, required for repl to detect the site
		port=random.randint(2000, 9000)  # Randomly select the port the machine hosts on.
	)
