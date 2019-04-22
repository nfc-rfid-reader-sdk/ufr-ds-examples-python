import ctypes
from ctypes import c_uint32, c_char_p, c_void_p, c_uint,c_ulong, c_ubyte, windll, byref, c_uint8, c_char
import sys
import os
import array
import ErrorCodes
import msvcrt
from Functions import *
import globals
import string
########################################################################## 
# dll loading
if sys.platform.startswith('win32'):
    uFR = ctypes.windll.LoadLibrary("ufr-lib//windows//x86//uFCoder-x86.dll")
elif sys.platform.startswith('linux'):
    uFR = cdll.LoadLibrary("ufr-lib//linux//x86//libuFCoder-x86.so")

##########################################################################

def PrepareSettings():
    i = c_uint32
    i = 0
    with open("config.txt", 'r') as f:
       globals.settings = f.read().splitlines()
    for i in range(len(globals.settings)):
        print(globals.settings[i])
        position = globals.settings[i].find(':')+1
        #print(position)
        length = len(globals.settings[i])
        #print(length)
        parse_string = globals.settings[i]
        globals.settings[i] = globals.settings[i][position:length].strip()
        #print(settings[i])
    return globals.settings    
    
##########################################################################

def PrepareKey(aes_key):

    key_used = globals.settings[0]
    key_length = len(key_used)
    
    if key_length != 32:
       print("Key length in 'config.txt' must be 16 bytes")
       aes_key = ""
       return False
       
    else:
        for x in range(0,len(key_used),2):
            temp = int(key_used[x:x+2],16)
            aes_key[x/2] = temp
        return aes_key
      
########################################################################## 

def ConvertInputKeyToAesKey(aes_key):
    aes_key_temp = (c_ubyte * 16)()
    key_length = len(aes_key)
    if key_length != 32:
       print("Key length must be 16 bytes")
       aes_key = ""
       return False
       
    else:
        for x in range(0,len(aes_key),2):
            temp = int(aes_key[x:x+2],16)
            aes_key_temp[x/2] = temp
        aes_key = aes_key_temp
        return aes_key
        
########################################################################## 

def print_settings():

    print("1 - Change AES key")
    print("2 - Change AID")
    print("3 - Change AID key number")
    print("4 - Change File ID")
    print("5 - Change internal key number")
    print("ESC - Exit to main menu")

########################################################################## 

def ChangeSettings():

    print("##########################################################################")
    print("Current config:")
    print("AES key: " + str(globals.settings[0]))
    print("AID: " + str(globals.settings[1]))
    print("AID key number for auth: " + str(globals.settings[2]))
    print("File ID: " + str(globals.settings[3]))
    print("Internal key number: " + str(globals.settings[4]))
    print("##########################################################################")

    print("1 - Change AES key")
    print("2 - Change AID")
    print("3 - Change AID key number")
    print("4 - Change File ID")
    print("5 - Change internal key number")
    print("ESC - Exit to main menu")
    
    key = str()
    
    new_aes_key =str()
    new_aid =str()
    new_aid_key_nr =str()
    new_file_id =str()
    new_internal_key_nr =str()
    
    while key != '\x1b': #
        key = msvcrt.getch()
        if key == '1': 
            print("Input new AES key (16 bytes):")
            new_aes_key = raw_input()
            if len(new_aes_key) != 32:
                print("AES key must be 16 bytes long")
            else:
                print("New AES key successfully entered.")
                globals.settings[0] = new_aes_key
                print_settings()
        elif key == '2':
            print("Input new AID (3 bytes hex):")
            new_aid = raw_input()
            if len(new_aid) != 6:
                print("AID must be 3 hex bytes long")
            else:
                print("New AID successfully entered.")
                globals.settings[1] = new_aid
                print_settings()
        elif key == '3':
            print("Input new AID key number (0 - 13)")
            new_aid_key_nr = raw_input()
            if int(new_aid_key_nr) < 0 or int(new_aid_key_nr) > 13:
                print("AID key number must be between 0 and 13")
            else:
                print("New AID key number successfully entered")
                globals.settings[2] = new_aid_key_nr
                print_settings()
        elif key == '4':
            print("Input new File ID  (0-31):")
            new_file_id = raw_input()
            if int(new_file_id) < 0 or int(new_file_id) > 31:
                print("File ID must be between 0 and 31")
            else:
                print("New File ID successfully entered")
                globals.settings[3] = new_file_id
                print_settings()
        elif key == '5':
            print("Input new internal key number (0 - 15):")
            new_internal_key_nr = raw_input()
            if int(new_internal_key_nr) < 0 or int(new_internal_key_nr) > 15:
                print("Internal key number must be between 0 and 15")
            else:
                print("New internal key number successfully entered")
                globals.settings[4] = new_internal_key_nr
                print_settings()
        elif key == '\x1b':
            print("Done with changing settings..back to main.")
            usage()
        else:
            print_settings()
            
    with open('config.txt', 'w') as f:
        f.write("AES key: " + globals.settings[0] + "\n")
        f.write("AID: " + globals.settings[1] + "\n")
        f.write("AID key number for auth: " + globals.settings[2] + "\n")
        f.write("File ID: " + globals.settings[3] + "\n")
        f.write("Internal key number: " + globals.settings[4] + "\n")
    
########################################################################## 
      
def usage():
    print(" +------------------------------------------------+")
    print(" |              uFR Desfire example               |")
    print(" +------------------------------------------------+")
    print(" --------------------------------------------------")
    print("  (0) - Change authentication mode")
    print("  (1) - Master key authentication")
    print("  (2) - Get card UID")
    print("  (3) - Format card")
    print("  (4) - DES to AES")
    print("  (5) - AES to DES")
    print("  (6) - Get free memory")
    print("  (7) - Set random ID")
    print("  (8) - Internal key lock")
    print("  (9) - Internal key unlock")
    print("  (a) - Set baud rate")
    print("  (b) - Get baud rate")
    print("  (c) - Store AES key into reader")
    print("  (d) - Change AES key")
    print("  (e) - Change key settings")
    print("  (f) - Get key settings")
    print("  (g) - Make application")
    print("  (h) - Delete application")
    print("  (j) - Make file")
    print("  (k) - Delete file")
    print("  (l) - Write Std file")
    print("  (m) - Read Std file")
    print("  (n) - Read Value file")
    print("  (o) - Increase Value file")
    print("  (p) - Decrease Value file")
    print("  (r) - Change config parameters\n");
    print(" --------------------------------------------------")
    
##########################################################################  
      
def menu(key):
    if key == '0':
        globals.internal_key = not globals.internal_key
        if globals.internal_key == False:
                print(" Authentication mode is set to PROVIDED KEY ")
        else:
                print(" Authentication mode is set to INTERNAL KEY ")
            
    elif key == '1':
        globals.master_authent_req = not globals.master_authent_req
        if globals.master_authent_req == False:
                print(" Master key authentication is not required ")
        else:
                print(" Master key authentication is now required ")
    elif key == "2":
            #print("GetDesfireUID()")
            GetCardUID()
    elif key == "3":
            #print("FormatCard()")
            FormatCard()
    elif key == "4":
            #print("DEStoAES()")
            DEStoAES()
    elif key == "5":
            #print("AEStoDES()")
            AEStoDES()
    elif key == "6":
            #print("GetFreeMemory()")
            GetFreeMemory()
    elif key == "7":
            #print("SetRandomID()")
            SetRandomID()
    elif key == "8":
            print("InternalKeysLock()")
            InternalKeysLock()
    elif key == "9":
            print("InternalKeysUnlock()")
            InternalKeysUnlock()
    elif key == "a":
            print("SetBaudRate()")
            SetBaudRate()
    elif key == "b":
            print("GetBaudRate()")
            GetBaudRate()
    elif key == "c":
            print("StoreKeyIntoReader()")
            StoreKeyIntoReader()
    elif key == "d":
            print("ChangeAESKey()")
            ChangeAESKey()
    elif key == "e":
            print("ChangeKeySettings")
            ChangeKeySettings()
    elif key == "f":
            print("GetKeySettings()")
            GetKeySettings()
    elif key == "g":
            print("MakeApplication()")
            MakeApplication()
    elif key == "h":
            print("DeleteApplication()")
            DeleteApplication()
    elif key == "j":
            print("MakeFile()")
            MakeFile()
    elif key == "k":
            print("DeleteFile()")
            DeleteFile()
    elif key == "l":
            print("WriteStdFile()")
            WriteStdFile()
    elif key == "m":
            print("ReadStdFile()")
            ReadStdFile()
    elif key == "n":
            print("ReadValueFile")
            ReadValueFile()
    elif key == "o":
            print("IncreaseValueFile()")
            IncreaseValueFile()
    elif key == "p":
            print("DecreaseValueFile()")
            DecreaseValueFile()
    elif key == "r":
            print("ChangeSettings()")
            ChangeSettings()
    elif key == "q":
            print('T E S T')
            
    elif key == "\x1b":
            print("Closing....")
    else:
            usage()
            
    print(" --------------------------------------------------");
        
##########################################################################

def ReaderOpenEx(reader_type, port_name, port_interface, arg):
    openReader = uFR.ReaderOpenEx
    openReader.argtypes = (c_uint32, c_char_p, c_uint32, c_void_p)
    openReader.restype = c_uint
    b = c_char_p(port_name.encode('utf-8'))
    return openReader(reader_type, b, port_interface, arg)       
    
##########################################################################

def ReaderOpen():
    openReader = uFR.ReaderOpen
    return openReader()
    
##########################################################################

def ReaderUISignal(light, sound):
    uiSignal = uFR.ReaderUISignal
    uiSignal.argtypes = (c_ubyte, c_ubyte)
    uiSignal.restype = c_uint
    uiSignal(light, sound)
    
##########################################################################

def ReaderClose():
    func = uFR.ReaderClose
    return func()

##########################################################################


if __name__ == '__main__':

    # For opening uFR Nano Online UDP mode use:
    # status = ReaderOpenEx(0, "ip_address:port_number", 85, 0)
    #
    # For opening uFR Nano Online TCP/IP mode use:
    # status = ReaderOpenEx(0, "ip address:port_number", 84, 0)
    #
    # For opening uFR Nano Online without reset/RTS on ESP32 - transparent mode 115200 use:
    # status = ReaderOpenEx(2, 0, 0, "UNIT_OPEN_RESET_DISABLE")
    input = str()
    print("---------------------------------------------")
    print("https://www.d-logic.net/nfc-rfid-reader-sdk/")
    print("---------------------------------------------")
    print("Desfire console example application version 1.0")
    print("---------------------------------------------")
    globals.initialize() #initializing global vars
    print("Choose reader opening mode:")
    print("1. Simple reader open")
    print("2. Advanced reader open")
    input = raw_input()
    input = int(input)
    print(input)
    if input == 1:
        status = ReaderOpen()
    else:
        print("Enter reader type:")
        reader_type = raw_input()
        reader_type = int(reader_type)
        
        print ("Enter port name:")
        port_name = raw_input()
        
        print("Enter port interface:")
        port_interface = raw_input()
        
        
        
        print("Enter additional argument:")
        arg = raw_input()
        
        
        if port_interface == "U":
            port_interface = 85
        elif port_interface == "T":
            port_interface = 84
        else:
            port_interface = int(port_interface)
            
        status = ReaderOpenEx(reader_type, port_name, port_interface, arg)
    
    # for uFR online example:
    # status = ReaderOpenEx(0, "192.168.1.101:8881", 85, 0)
    #status = ReaderOpenEx(0,"192.168.1.108",85,0)
    

    if status == 0:
        print("Status: " + ErrorCodes.UFCODER_ERROR_CODES[status])
        print("Result: Port successfully opened")
        print("---------------------------------------------")
        ReaderUISignal(1, 1)
    else:
        print("Status: " + ErrorCodes.UFCODER_ERROR_CODES[status])
        print("Result: Port not opened")
        print("---------------------------------------------")
        print("Press ENTER to quit")
        raw_input()
        sys.exit(1)

    key = str()    
    PrepareSettings()
    usage()    
    print("press ESC to exit.")
    
    while key != '\x1b': #
        key = msvcrt.getch()
        menu(key)
        
    ReaderClose()