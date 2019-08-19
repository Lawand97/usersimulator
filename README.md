# usersimulator



A.1.1    Description
To prepare for the of the tool you would need to setup a special Google Chrome instance.
To use this tool, you must run an instance of Google Chrome with the remote-debugging
option, like in the following example.


google-chrome –remote-debugging-port=9222


To add the remote debugging port to chrome, open the properties of a Google Chrome
shortcut.  Add then the in the Target section at the end .


A.1.2    Prerequisites and Installation

Very  few  dependencies  must  be  satisfied:  an  updated  Google-Chrome  version  and  the
python packages requests and websocket.  Those should be installed by default.  Further-
more following packages need to be installed.
tkinter
psutil
threading
PyChromeDevTools
xlutils
xlsxwriter

Secondly, a text file called simulator.txt needs to be created.  The file should contain the
list of URLs , which should be opened by the simulator tool.  Every URL
entry in the file should be on a new line.  Otherwise the tool will not work correctly.  The
file should be located in the same folder as the Python script.



A.1.3    Operation
To operate the simulator tool open first a instance of the Google Chrome browser with the
remote debugging port configured.  Now make sure that the simulator.txt files is located
in the same folder.  Next run the simulator using the follow command:

python simulator.py

This command should open the User Interface where the button to start the simulation
is available.  Now the simulation can be started.  After all pages have been loaded, the
results are shown on the User Interface as well as it will generate the results in a xls file
(
i.e.,
Results.xls)
