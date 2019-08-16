#!/usr/bin/python
# coding:UTF-8

# -------------------------------------------------------------------------------------
#   PYTHON UTILITY SCRIPT FILE FOR THE FORENSIC ANALYSIS OF WINDOWS MEMORY DUMP-FILES
#               BY TERENCE BROADBENT BSC CYBER SECURITY (FIRST CLASS)
# -------------------------------------------------------------------------------------

# ------------------------------------------------------------------------------------- 
# AUTHOR  : Terence Broadbent                                                    
# CONTRACT: GitHub
# Version : 2.0                                                                
# Details : Load required imports.
# Modified: N/A
# -------------------------------------------------------------------------------------

import os
import sys
import subprocess
import os.path
import fileinput
import shutil
import unicodedata
from termcolor import colored					# pip install termcolor

# -------------------------------------------------------------------------------------
# AUTHOR  : Terence Broadbent                                                    
# CONTRACT: GitHub                                                               
# Version : 2.0                                                                
# Details : Conduct simple and routine tests on user supplied arguements.   
# Modified: N/A                                                               
# -------------------------------------------------------------------------------------

if os.geteuid() != 0:
    print "\nPlease run this python script as root..."
    exit(True)

if len(sys.argv) < 2:
    print "\nUse the command python memory_master.py memorydump.mem\n"
    exit(True)

fileName = sys.argv[1]

if os.path.exists(fileName) == 0:
    print "\nFile " + fileName + " was not found, did you spell it correctly?"
    exit(True)

extTest = fileName[-3:]

if extTest != "mem":
    print "This is not a .mem file...\n"
    exit (True)

while len(fileName) < 25:
  fileName += " "

# -------------------------------------------------------------------------------------
# AUTHOR  : Terence Broadbent                                                    
# CONTRACT: GitHub                                                               
# Version : 2.0
# Details : Initialise system variables.
# Modified: N/A                                                               
# -------------------------------------------------------------------------------------

PRO = "UNSELECTED           "
DIS = "UNSELECTED           "
PRM = "UNSELECTED           "
PI1 = "0                    "
OFF = "0                    "
SAM = "0x0000000000000000"
SEC = "0x0000000000000000"
SOF = "0x0000000000000000"
COM = "0x0000000000000000"
SYS = "0x0000000000000000"
HST = "NOT FOUND     "
ADM = "NOT FOUND     "
GUS = "NOT FOUND     "
USR = "NOT FOUND     "
UN4 = "RESERVED      "
UN5 = "EMPTY"
UN6 = "EMPTY"
UN7 = "EMPTY"
UN8 = "EMPTY"
UN9 = "EMPTY"
BLK = "BLANK"

# -------------------------------------------------------------------------------------
# AUTHOR  : Terence Broadbent                                                    
# CONTRACT: GitHub
# Version : 2.0                                                                
# Details : Display a universal header.    
# Modified: N/A                                                               
# -------------------------------------------------------------------------------------

def header ():
   os.system("clear")
   print "\t\t\t __  __ _____ __  __  ___  ______   __  __  __    _    ____ _____ _____ ____   "
   print "\t\t\t|  \/  | ____|  \/  |/ _ \|  _ \ \ / / |  \/  |  / \  / ___|_   _| ____|  _ \  "
   print "\t\t\t| |\/| |  _| | |\/| | | | | |_) \ V /  | |\/| | / _ \ \___ \ | | |  _| | |_) | "
   print "\t\t\t| |  | | |___| |  | | |_| |  _ < | |   | |  | |/ ___ \ ___) || | | |___|  _ <  "
   print "\t\t\t|_|  |_|_____|_|  |_|\___/|_| \_\|_|   |_|  |_/_/   \_\____/ |_| |_____|_| \_\ "
   print "                                                                                     "
   print "\t\t\t             BY TERENCE BROADBENT BSC CYBER SECURITY (FIRST CLASS)           \n"

# -------------------------------------------------------------------------------------
# AUTHOR  : Terence Broadbent                                                    
# CONTRACT: GitHub                                                               
# Version : 2.0
# Details : Populate system variables.
# Modified: N/A                                                               
# -------------------------------------------------------------------------------------

header()
print "Booting!! - Please wait...\n"

os.system("volatility imageinfo -f " + fileName + " > IMAGE.txt")
with open("IMAGE.txt") as fp:
   line = fp.readline()
   PRO = line.split(None,4)[3]
   PRO = PRO.rstrip(',')
   PRO = " --profile " + PRO
   DIS = PRO.replace(" --profile ","")
fp.close()
os.remove('IMAGE.txt')
while len(DIS) < 21:
   DIS = DIS + " "

if PRO[:2] == "NO":
   print "ERROR - Profile not found..."
   exit(1)

os.system("volatility -f " + fileName + PRO + " hivelist > hivelist.txt")
with open("hivelist.txt") as fp:  
   line = fp.readline()
   while line:
      line = fp.readline()
      if "\SAM" in line:
         SAM = line.split(None, 1)[0]
         while len(SAM) < 18:
            SAM = SAM + " "
      if "SECURITY" in line:
         SEC = line.split(None, 1)[0]
         while len(SEC) < 18:
            SEC = SEC + " "
      if "\SOFTWARE" in line:
         SOF = line.split(None, 1)[0]
         while len(SOF) < 18:
            SOF = SOF + " "
      if "\SYSTEM" in line:
         SYS = line.split(None, 1)[0]
         while len(SYS) < 18:
            SYS = SYS + " "
      if "\COMPONENTS" in line:
         COM = line.split(None, 1)[0]
         while len(COM) < 18:
            COM = COM + " "
fp.close()
os.remove('hivelist.txt')

os.system("volatility -f " + fileName + PRO + " printkey -o " + SYS + " -K 'ControlSet001\Control\ComputerName\ComputerName' > host.txt")
with open("host.txt") as fp:
   wordlist = (list(fp)[-1])
fp.close()
os.remove('host.txt')
wordlist = wordlist.split()
HST = wordlist[-1].upper().rstrip('')
while len(HST.encode()) < 15:          						# patch required len2 for X?
   HST = HST + " "

os.system("echo 'HASH FILE' > hash.txt")
os.system("volatility -f " + fileName + PRO + " hashdump -y " + SYS + " -s " + SAM + " >> hash.txt")
usercount = 0
with open("hash.txt") as fp:
   line = fp.readline()
   while line:
      line = fp.readline()
      if "Administrator" in line:
         ADM = "FOUND         "
      if "Guest" in line :
         GUS = "FOUND         "
      usercount = usercount + 1
fp.close()
os.remove('hash.txt')

usercount = usercount -1
if ADM == "FOUND         ":
   usercount = usercount -1
if GUS == "FOUND         ":
   usercount = usercount -1
if usercount > 0:
   USR = "FOUND "
   USR = USR + str(usercount)
while len(USR) < 14:
   USR = USR + " "

# -------------------------------------------------------------------------------------
# AUTHOR  : Terence Broadbent                                                    
# CONTRACT: GitHub                                                               
# Version : 2.0
# Details : Display pertinant system information.
# Modified: N/A                                                               
# -------------------------------------------------------------------------------------

def display():
   print "="*15,
   print colored("WINDOWS O/S",'white'),
   print "="*20,
   print colored("SYSTEM HIVES",'white'),
   print "="*17,
   print colored("HOST/USERS",'white'),
   print "="*43

   print "FILENAME [",
   print colored(str.upper(fileName[:21]),'blue'),
   print "] SAM      [",
   if (SAM == "0x0000000000000000"):
      print colored(SAM,'red'),
   else:
      print colored(SAM,'blue'),
   print "] HOST NAME[",
   if HST == "NOT FOUND         ":
      print colored(HST,'red'),
   else:
       print colored(HST,'blue'),
   print "] RESERVED [ " + UN5 + " ]",
   print "RESERVED [ " + BLK + " ]"   #new

   print "PROFILE  [",
   if DIS == "UNSELECTED              ":
      print colored(str.upper(DIS),'red'),
   else:
      print colored(str.upper(DIS),'blue'),
   print "] SECURITY [",
   if SEC == "0x0000000000000000":
      print colored(SEC,'red'),
   else:
      print colored(SEC,'blue'),
   print "] ADMIN    [",
   if ADM == "NOT FOUND         ":
      print colored(ADM,'red'),
   else:
      print colored(ADM,'blue'),
   print "] RESERVED [ " + UN6 + " ]",
   print "RESERVED [ " + BLK + " ]"   #new

   print "PID      [",
   if PI1[:1] == "0":
      print colored(PI1,'red'),
   else:
      print colored(PI1,'blue'),
   print "] SOFTWARE [",
   if SOF == "0x0000000000000000":
      print colored(SOF,'red'),
   else:
      print colored(SOF,'blue'),
   print "] GUEST    [",
   if GUS == "NOT FOUND         ":
      print colored(GUS,'red'),
   else:
      print colored(GUS,'blue'),
   print "] RESERVED [ " + UN7 + " ]",
   print "RESERVED [ " + BLK + " ]"   #new

   print "OFFSET   [",
   if OFF[:1] == "0":
      print colored(OFF,'red'),
   else:
      print colored(OFF,'blue'),
   print "] COMPONENT[",
   if COM == "0x0000000000000000":
      print colored(COM,'red'),
   else:
      print colored(COM,'blue'),
   print "] USERS    [",
   if USR == "NOT FOUND         ":
      print colored(USR,'red'),
   else:
      print colored(USR,'blue'),
   print "] RESERVED [ " + UN8 + " ]",
   print "RESERVED [ " + BLK + " ]"   #new

   print "PARAMETER[",
   if PRM == "UNSELECTED           ":
      print colored(PRM,'red'),
   else:
      print colored(str.upper(PRM),'blue'),
   print "] SYSTEM   [",
   if SYS == "0x0000000000000000":
      print colored(SYS,'red'),
   else:
      print colored(SYS,'blue'),
   print "] RESERVED [ " + UN4 + " ] RESERVED [ " + UN9 + " ]",
   print "RESERVED [ " + BLK + " ]"   #new

   print "*"*134
   print " "*9,
   print colored("SETTINGS",'white'),
   print " "*14,
   print colored("IDENTIFY",'white'),
   print " "*15,
   print colored("ANALYSE",'white'),
   print " "*13,
   print colored("INVESTIGATE",'white'),
   print " "*18,
   print colored("EXTRACT",'white'),
   print " "*10
   print "*"*134

# -------------------------------------------------------------------------------------
# AUTHOR  : Terence Broadbent                                                    
# CONTRACT: GitHub                                                               
# Version : 2.0
# Details : Create the menu system.
# Modified: N/A                                                               
# -------------------------------------------------------------------------------------

menu = {}
menu['(1)']="Set PROFILE\t	(10) User Passwords	(20) SAM Hive		(30) PARAMETER Search	(40) Timeline"
menu['(2)']="Set PID		(11) Default Password	(21) SECURITY Hive	(31) Malfind PID	(41) Screenshots"
menu['(3)']="Set OFFSET		(12) Running Processes	(22) SOFTWARE Hive	(32) Mutant PID		(42) MFT Table"
menu['(4)']="Set PARAMETER	(13) Running Services	(23) COMPONENT Hive	(33) Vaddump PID	(43) " 
menu['(5)']="			(14) Clipboard Contents	(24) SYSTEM Hive	(34) Dump PID		(44) "
menu['(6)']="			(15) Console Contents	(25) Network Traffic	(35) 			(45) "
menu['(7)']="Clean and Exit	(16) User Assist Keys 	(26) Connscan PARAMETER	(36)			(46) Bulk Extractor"


# -------------------------------------------------------------------------------------
# AUTHOR  : Terence Broadbent                                                    
# CONTRACT: GitHub                                                               
# Version : 2.0
# Details : Start the main menu controller.
# Modified: N/A                                                               	
# -------------------------------------------------------------------------------------

while True: 
   header()
   display()
   options=menu.keys()
   options.sort()
   for entry in options: 
      print entry, menu[entry]
   selection=raw_input("\nPlease Select: ")

# ------------------------------------------------------------------------------------- 
# AUTHOR  : Terence Broadbent                                                    
# CONTRACT: GitHub
# Version : 2.0
# Details : Menu option selected - Lets the user select a new Windows profile.
# Modified: N/A
# -------------------------------------------------------------------------------------

   if selection =='1':
      BAK = PRO
      MATCH = 0
      PRO = raw_input("Please enter profile: ")
      if PRO == "":
         PRO = BAK      
      with open("profiles.txt") as fp:
         line = fp.readline()
         while line:
            line = fp.readline()
            if PRO in line:
               MATCH = 1  
      if MATCH == 0:
         PRO = BAK
      else:
         PRO = " --profile " + PRO
         DIS = PRO.replace(" --profile ","")
         while len(DIS) < 21:
            DIS += " "
      fp.close()        

# ------------------------------------------------------------------------------------- 
# AUTHOR  : Terence Broadbent                                                    
# CONTRACT: GitHub
# Version : 2.0
# Details : Menu option selected - Allowd the user to set the PID value.
# Modified: N/A
# -------------------------------------------------------------------------------------

   if selection =='2':
      PI1 = raw_input("Please enter PID value: ")
      while len(PI1) < 21:
         PI1 += " "

# ------------------------------------------------------------------------------------- 
# AUTHOR  : Terence Broadbent                                                    
# CONTRACT: GitHub
# Version : 2.0
# Details : Menu option selected - Allows the user to set the PPID value.
# Modified: N/A
# -------------------------------------------------------------------------------------

   if selection =='3':
      OFF = raw_input("Please enter PPID value: ")
      while len(OFF) < 21:
         OFF += " "

# ------------------------------------------------------------------------------------- 
# AUTHOR  : Terence Broadbent                                                    
# CONTRACT: GitHub
# Version : 2.0
# Details : Menu option selected - Allows the user to set the Parameter string.
# Modified: N/A
# -------------------------------------------------------------------------------------

   if selection =='4':
      PRM = raw_input("Please enter parameter value: ")
      while len(PRM) < 21:
         PRM += " "

# ------------------------------------------------------------------------------------- 
# AUTHOR  : Terence Broadbent                                                    
# CONTRACT: GitHub
# Version : 2.0
# Details : Menu option selected - Clean up system files and exit the program.
# Modified: N/A
# -------------------------------------------------------------------------------------

   if selection =='7':
      if os.path.exists('timeline.txt'):
         os.remove('timeline.txt')
      if os.path.exists('mfttable.txt'):
         os.remove('mfttable.txt')
      if os.path.exists('screenShots'):
         shutil.rmtree('screenShots') 
      if os.path.exists('bulkOut'):
         shutil.rmtree('bulkOut') 
      if os.path.exists('PIData'):
         shutil.rmtree('PIData')
      if os.path.exists('malFind'):
         shutil.rmtree('malFind')   
      if os.path.exists('mutantFiles'):
         shutil.rmtree('mutantFiles') 
      if os.path.exists('vadDump'):
         shutil.rmtree('vadDump')
      exit(False)

# ------------------------------------------------------------------------------------- 
# AUTHOR  : Terence Broadbent                                                    
# CONTRACT: GitHub
# Version : 2.0
# Details : Menu option selected - Dumps the SAM file hashes for export to hashcat.
# Modified: N/A
# -------------------------------------------------------------------------------------

   if selection =='10':
      print ""
      if (SAM == "0x0000000000000000") or (SYS == "0x0000000000000000"):
         print colored("Missing HIVE - its not possible to extract the hashes...",'white')	
      else:
         os.system("volatility -f " + fileName + PRO + " hashdump -y " + SYS + " -s " + SAM)
      raw_input("\nPress ENTER to continue...")

# ------------------------------------------------------------------------------------- 
# AUTHOR  : Terence Broadbent                                                    
# CONTRACT: GitHub
# Version : 2.0
# Details : Menu option selected - Dispays any LSA secrets
# Modified: N/A
# -------------------------------------------------------------------------------------

   if selection =='11':
      os.system("volatility -f " + fileName + PRO + " lsadump")
      raw_input("\nPress ENTER to continue...")

# ------------------------------------------------------------------------------------- 
# AUTHOR  : Terence Broadbent                                                    
# CONTRACT: GitHub
# Version : 2.0
# Details : Menu option selected - Shows running processes and provides a brief analyse.
# Modified: N/A
# -------------------------------------------------------------------------------------

   if selection =='12':
      os.system("volatility -f " + fileName + PRO + " psscan | more")
      os.system("volatility -f " + fileName + PRO + " psscan --output greptext > F1.txt")
      os.system("tail -n +2 F1.txt > F2.txt")
      os.system("sed -i 's/>//g' F2.txt")
      with open("F2.txt") as read1:
         for line in read1:
            for word in line.split('|'):
                output = subprocess.check_output("echo " + word + " >> F3.txt", shell=True)
      read1.close()
      os.system("tail -n +2 F3.txt > F4.txt")
      os.system("wc -l F2.txt > NUM.txt")
      NUMLINES = open("NUM.txt").readline().replace(' F2.txt','')
      COUNT = int(NUMLINES)
      print "\n[1]. There were",COUNT,"processes running at the time of the memory dump.\n"
      read2 = open('PID.txt','w')
      read3 = open('PPID.txt','w')
      with open('F4.txt') as read4:
         while COUNT > 0:
            A = read4.readline()
            B = read4.readline() # Executable name
            C = read4.readline().rstrip('\n') # PI1
            print >>read2,C
            D = read4.readline().rstrip('\n') # OFF             
            print >>read3,D		
            E = read4.readline()
            G = read4.readline()
            H = read4.readline() # blank
            COUNT = (COUNT-1)
      read2.close()
      read3.close()
      os.remove('F1.txt')
      os.remove('F2.txt')
      os.remove('F3.txt')
      os.remove('F4.txt')
      os.system("bash patch.sh")
      print "[2]. Analyse of these processes reveals that:"
      with open('SUSPECT.txt') as read5:
         line = read5.readline().rstrip('\n')
         while line != "":
            if line != "0":
               print "     Parent process PPID",line,"does not have a process spawn! and should be investigated further..."
            line = read5.readline().strip('\n')
      read5.close()
      os.remove('PID.txt')
      os.remove('PPID.txt')
      os.remove('NUM.txt')
      os.remove('SUSPECT.txt')
      raw_input("\nPress ENTER to continue...")

# ------------------------------------------------------------------------------------- 
# AUTHOR  : Terence Broadbent                                                    
# CONTRACT: GitHub
# Version : 2.0
# Details : Menu option selected - Shows running services.
# Modified: N/A
# -------------------------------------------------------------------------------------

   if selection =='13':
      os.system("volatility -f " + fileName + PRO + " svcscan | more")
      raw_input("\nPress ENTER to continue...")

# ------------------------------------------------------------------------------------- 
# AUTHOR  : Terence Broadbent                                                    
# CONTRACT: GitHub
# Version : 2.0
# Details : Menu option selected - Shows clipboard information.
# Modified: N/A
# -------------------------------------------------------------------------------------

   if selection =='14':
      os.system("volatility -f " + fileName + PRO + " clipboard")
      raw_input("\nPress ENTER to continue...")

# ------------------------------------------------------------------------------------- 
# AUTHOR  : Terence Broadbent                                                    
# CONTRACT: GitHub
# Version : 2.0
# Details : Menu option selected - Shows console information.
# Modified: N/A
# -------------------------------------------------------------------------------------

   if selection =='15':
      os.system("volatility -f " + fileName + PRO + " consoles")
      raw_input("\nPress ENTER to continue...")

# ------------------------------------------------------------------------------------- 
# AUTHOR  : Terence Broadbent                                                    
# CONTRACT: GitHub
# Version : 2.0
# Details : Menu option selected - Show userassist key values.
# Modified: N/A
# -------------------------------------------------------------------------------------

   if selection =='16':
      os.system("volatility -f " + fileName + PRO + " userassist")
      raw_input("\nPress ENTER to continue...")

# ------------------------------------------------------------------------------------- 
# AUTHOR  : Terence Broadbent                                                    
# CONTRACT: GitHub
# Version : 2.0
# Details : Menu option selected - Shows SAM hive.
# Modified: N/A
# -------------------------------------------------------------------------------------

   if selection =='20':
      os.system("volatility -f " + fileName + PRO + " hivedump -o " + SAM)
      raw_input("Press ENTER to continue...")

# ------------------------------------------------------------------------------------- 
# AUTHOR  : Terence Broadbent                                                    
# CONTRACT: GitHub
# Version : 2.0
# Details : Menu option selected - Shows SECURITY hive.
# Modified: N/A
# -------------------------------------------------------------------------------------

   if selection =='21':
      if (SEC == "0x0000000000000000"):
         print colored("Not possible...",'white')
      else:
         os.system("volatility -f " + fileName + PRO + " hivedump -o " + SEC)
      raw_input("\nPress ENTER to continue...")

# ------------------------------------------------------------------------------------- 
# AUTHOR  : Terence Broadbent                                                    
# CONTRACT: GitHub
# Version : 2.0
# Details : Menu option selected - Shows SOFTWARE hive.
# Modified: N/A
# -------------------------------------------------------------------------------------

   if selection =='22':
      if (SOF == "0x0000000000000000"):
         print colored("Not possible...",'white')
      else:
         os.system("volatility -f " + fileName + PRO + " hivedump -o " + SOF)
      raw_input("\nPress ENTER to continue...")

# ------------------------------------------------------------------------------------- 
# AUTHOR  : Terence Broadbent                                                    
# CONTRACT: GitHub
# Version : 2.0
# Details : Menu option selected - Shows COMPONENT hive.
# Modified: N/A
# -------------------------------------------------------------------------------------

   if selection =='23':
      if (COM == "0x0000000000000000"):
         print colored("Not possible...",'white')
      else:
         os.system("volatility -f " + fileName + PRO + " hivedump -o " + COM)
      raw_input("\nPress ENTER to continue...")

# ------------------------------------------------------------------------------------- 
# AUTHOR  : Terence Broadbent                                                    
# CONTRACT: GitHub
# Version : 2.0
# Details : Menu option selected - Shows SYSTEM hive.
# Modified: N/A
# -------------------------------------------------------------------------------------

   if selection =='24':
      if (SYS == "0x0000000000000000"):
         print colored("Not possible...",'white')
      else:
         os.system("volatility -f " + fileName + PRO + " hivedump -o " + SYS)
      raw_input("\nPress ENTER to continue...")    

# ------------------------------------------------------------------------------------- 
# AUTHOR  : Terence Broadbent                                                    
# CONTRACT: GitHub
# Version : 2.0
# Details : Menu option selected - Shows network traffic.
# Modified: N/A
# -------------------------------------------------------------------------------------

   if selection =='25':
      os.system("volatility -f " + fileName + PRO + " netscan")
      raw_input("\nPress ENTER to continue...") 

# ------------------------------------------------------------------------------------- 
# AUTHOR  : Terence Broadbent                                                    
# CONTRACT: GitHub
# Version : 2.0
# Details : Menu option selected - Extracts specific network traffic.
# Modified: N/A
# -------------------------------------------------------------------------------------

   if selection =='26':
      os.system("volatility -f " + fileName + " connscan | egrep " + PRM)
      raw_input("\nPress ENTER to continue...") 

# ------------------------------------------------------------------------------------- 
# AUTHOR  : Terence Broadbent                                                    
# CONTRACT: GitHub
# Version : 2.0
# Details : Menu option selected - Allows the iuser to Search the PARAM string.
# Modified: N/A
# ------------------------------------------------------------------------------------- 
   
   if selection =='7':
      os.system("volatility -f " + fileName + " " + PRO + " pslist | grep " + PRM)
      raw_input("Press ENTER to continue...")

# ------------------------------------------------------------------------------------- 
# AUTHOR  : Terence Broadbent                                                    
# CONTRACT: GitHub
# Version : 2.0
# Details : Menu option selected - Finds Malware!
# Modified: N/A
# -------------------------------------------------------------------------------------

   if selection =='31':
      test = os.path.exists('malFind')
      if test !=1:
         os.system('mkdir malFind')
      os.system("volatility -f " + fileName + PRO + " malfind -p " + PI1 + " --dump-dir malFind")
      print "\nMalfind extraction is now available in directory malFind...\n"
      raw_input("Press ENTER to continue...")

# ------------------------------------------------------------------------------------- 
# AUTHOR  : Terence Broadbent                                                    
# CONTRACT: GitHub
# Version : 2.0
# Details : Menu option selected - Finds Mutants!
# Modified: N/A
# -------------------------------------------------------------------------------------

   if selection =='32':
      test = os.path.exists('mutantFiles')
      if test !=1:
         os.system('mkdir mutantFiles')
      os.system("volatility -f " + fileName + PRO + " handles -p " + PI1 + " -t mutantFiles -s")
      print "\nMutant extraction is now available in directory mutantFiles...\n"
      raw_input("Press ENTER to continue...")

# ------------------------------------------------------------------------------------- 
# AUTHOR  : Terence Broadbent                                                    
# CONTRACT: GitHub
# Version : 2.0
# Details : Menu option selected -  Vaddump!
# Modified: N/A
# -------------------------------------------------------------------------------------

   if selection =='33':
      test = os.path.exists('vadDump')
      if test !=1:
         os.system('mkdir vadDump')
      os.system("volatility -f " + fileName + PRO + " vaddump -p " + PI1 + " -D vadDump")
      print "\nVaddunp extraction is now available in directory vadDump...\n"
      raw_input("Press ENTER to continue...")

# ------------------------------------------------------------------------------------- 
# AUTHOR  : Terence Broadbent                                                    
# CONTRACT: GitHub
# Version : 2.0
# Details : Menu option selected - Memory dump PID.
# Modified: N/A
# -------------------------------------------------------------------------------------

   if selection =='34':
      test = os.path.exists('PIData')
      if test !=1:
         os.system('mkdir PIData') 
      os.system("volatility -f " + fileName + PRO + " memdump -p " + PI1 + " -D PIData")
      print "\nPID dump is now available in directory PIData...\n"
      raw_input("Press ENTER to continue...")

# ------------------------------------------------------------------------------------- 
# AUTHOR  : Terence Broadbent                                                    
# CONTRACT: GitHub
# Version : 2.0
# Details : Menu option selected - Build timeline.
# Modified: N/A
# -------------------------------------------------------------------------------------

   if selection =='40':
      os.system("volatility -f " + fileName + PRO + " timeliner --output-file timeline.txt")

#------------------------------------------------------------------------------------- 
# AUTHOR  : Terence Broadbent                                                    
# CONTRACT: GitHub
# Version : 2.0
# Details : Menu option selected - Download windows screenshots.
# Modified: N/A
# -------------------------------------------------------------------------------------

   if selection =='41':
      test = os.path.exists('screenShots')
      if test !=1:
         os.system('mkdir screenShots')   
      os.system("volatility -f " + fileName + PRO + " -D screenShots screenshot")
      print "\nScreenshots are now available in directory screenShots...\n"
      raw_input("Press ENTER to continue...")

# ------------------------------------------------------------------------------------- 
# AUTHOR  : Terence Broadbent                                                    
# CONTRACT: GitHub
# Version : 2.0
# Details : Menu option selected - Extracts the MFT table and it contents.
# Modified: N/A
# -------------------------------------------------------------------------------------

   if selection =='42':
      os.system("volatility -f " + fileName + PRO + " mftparser >> mfttable.txt")
      print "The MFT has been sucessfully exported to mfttable.txt..."
      raw_input("Press ENTER to continue...")

# ------------------------------------------------------------------------------------- 
# AUTHOR  : Terence Broadbent                                                    
# CONTRACT: GitHub
# Version : 2.0
# Details : Menu option selected - Bulk Extract files.
# Modified: N/A
# -------------------------------------------------------------------------------------

   if selection =='46':
      os.system("bulk_extractor -o bulkOut " + fileName)
      print "\nBulk extraction is now available in directory bulkOut...\n"
      raw_input("Press ENTER to continue...")

#Eof...
