import sys
sys.path.insert(0, "/var/www/html/punch")

activate_this = '/var/www/html/punch/env/bin/activate_this.py'
with open (activate_this) as file_:
        exec(file_.read(), dict(__file__=activate_this))

from daily_punch import app as application
application.secret_key = 'qwertyuijhgfdfg'
