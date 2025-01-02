import pyodbc
import os
#Set up PATH variable correctly, then use 'PIP INSTALL PYODBC'
#Install Microsoft SQL Express
#Install Microsoft SQL Server Management Studio
#Attach Database file in SQL Studio to mount as a service
bad = 0
conn = pyodbc.connect('Driver={SQL Server};' #Required Text
                      'Server=[redacted]\SQLEXPRESS;' #Server=[hostname]\[sql version] can copy right from SMSS
                      'Database=OasisPull9;' #Name of database mounted in SQL Server
                      'Trusted_Connection=yes;') #Required Text

cursor = conn.cursor() #Create the cursor object
cursor.execute('SELECT * FROM OasisPull9.dbo.catdvformat') #command to run SQL query


for row in cursor:
    xmlname = row.Xmlname
    location = row.Path
    airdate = row.Airdate
    script = row.Script
    #length = row.Length
    #XML and File Name
    xmlname1 = xmlname.replace("<Filename>",'', 1)
    xmlname2 = xmlname1.replace('</Filename>','', 1)
    medianame = xmlname2.replace('.xml','',1)
    print(xmlname2)
    f= open('i.txt', 'w') #Placeholder File
    f.write('<clip>\n') #CatDV Opening Tag
    f.write('<NAME>'+medianame+'</NAME>\n') #Media Filename
    f.write('<BIN>Oasis</BIN>\n')
    #Media Path Info
    f.write('<USER5 name="Station ID">WFTX</USER5>') #Station ID
    print(row.Path)
    f.write(row.Path + '\n') #Path to original media
    print(airdate)
    f.write('<USER9 name="DATE">'+ str(row.Airdate) + '</USER9>\n') #Air date and time approximate
    print(row.Script)
    for x in row.Script.splitlines():
        f.write(x)
        f.write('\n')
    #print(length)
    #f.write(row.Length + '\n')
    f.write ('</clip>\n')
    f.close()
    if os.path.isfile(xmlname2):
        badtext = str(bad)
        os.rename('i.txt',badtext + '.txt')
    else:
        os.rename('i.txt',xmlname2)
    
    bad += 1
    input('Press ENTER')
    #for field in row:
        #print(field)
        #input("Press Enter to Continue") #Pause, testing only