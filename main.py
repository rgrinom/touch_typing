import sys
sys.path.insert(1, 'src')

from application import Application

app = Application(1080, 720, 25)
app.run()
