import subprocess
import os

def uploadXML():

    #Finding path for the php file and the recent xml files
    php_path = os.path.abspath("companyscripts/helperscripts/XML_Upload/XML_Upload_PHP_BASE.php")
    xml_path = os.path.abspath("recentXML") + "/"

    #Opens the recentXML folder and gets all of the xml in the form of a string
    with os.scandir(xml_path) as entries:
        for entry in entries:
            if entry.is_file():
                with open(xml_path + entry.name) as xml_file:
                    xml = '$xml = "' + xml_file.read() + '";'

    #Opens the base php file
    with open(php_path) as php_file:
        php = php_file.read()
        print("Uploading XML...")
        #Giving the xml variable in the php file the xml data
        php = php.replace('$xml = "";', xml)

    #Writing a new php run file so the xml variable can be changed and utilized
    php_run_file = open("XML_Upload_PHP_Run.php", "w")
    php_run_file.write(php)
    php_run_file.close()

    #Running the php script
    proc = subprocess.Popen("php XML_Upload_PHP_Run.php", shell=True, stdout=subprocess.PIPE)
    print("XML Upload Complete")
