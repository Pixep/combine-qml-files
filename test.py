import os

print "-----"
os.system("python combine-qml.py --help")

print "-----"
os.system("python combine-qml.py -v tests/main-base.qml tests/main.qml -c tests/Button.qml Button")
