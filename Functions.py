
from ctypes import c_uint32, c_char_p, c_void_p, c_uint, c_ubyte, windll, byref, POINTER
#from ctypes import *
import sys
import array
import ErrorCodes
import msvcrt
from desfire_example import *
import globals

#################################################################

DESFIRE_KEY_SETTINGS = {

'DESFIRE_KEY_SET_CREATE_WITH_AUTH_SET_CHANGE_KEY_CHANGE' : 0x09,
'DESFIRE_KEY_SET_CREATE_WITHOUT_AUTH_SET_CHANGE_KEY_CHANGE' : 0x0F,
'DESFIRE_KEY_SET_CREATE_WITH_AUTH_SET_NOT_CHANGE_KEY_CHANGE' : 0x01,
'DESFIRE_KEY_SET_CREATE_WITHOUT_AUTH_SET_NOT_CHANGE_KEY_CHANGE' : 0x07,
'DESFIRE_KEY_SET_CREATE_WITH_AUTH_SET_CHANGE_KEY_NOT_CHANGE' : 0x08,
'DESFIRE_KEY_SET_CREATE_WITHOUT_AUTH_SET_CHANGE_KEY_NOT_CHANGE' : 0x0E,
'DESFIRE_KEY_SET_CREATE_WITH_AUTH_SET_NOT_CHANGE_KEY_NOT_CHANGE' : 0x00,
'DESFIRE_KEY_SET_CREATE_WITHOUT_AUTH_SET_NOT_CHANGE_KEY_NOT_CHANGE' : 0x06,
} 
#################################################################

DESFIRE_ERROR_CODES = {
	
    0xBB7  : 'READER_ERROR',				    #// 2999 [dec]
	0xBB8  : 'NO_CARD_DETECTED',				    #// 3000 [dec]
	0xBB9  : 'CARD_OPERATION_OK',				#// 3001 [dec]
	0xBBA  : 'WRONG_KEY_TYPE',					#// 3002 [dec]
	0xBBB  : 'KEY_AUTH_ERROR',					#// 3003 [dec]
	0xBBC  : 'CARD_CRYPTO_ERROR',			#// 3004 [dec]
	0xBBD  : 'READER_CARD_COMM_ERROR',			#// 3005 [dec]
	0xBBE  : 'PC_READER_COMM_ERROR',		    #// 3006 [dec]
	0xBBF  : 'COMMIT_TRANSACTION_NO_REPLY',    #// 3007 [dec]
	0x0BC0 : 'COMMIT_TRANSACTION_ERROR',	    #// 3008 [dec]
	0x0C0C : 'DESFIRE_CARD_NO_CHANGES',
	0x0C03 : 'DESFIRE_CARD_OUT_OF_EEPROM_ERROR',
	0x0C1C : 'DESFIRE_CARD_ILLEGAL_COMMAND_CODE',
	0x0C1E : 'DESFIRE_CARD_INTEGRITY_ERROR',
	0x0C40 : 'DESFIRE_CARD_NO_SUCH_KEY',
	0x0C7E : 'DESFIRE_CARD_LENGTH_ERROR',
	0x0C9D : 'DESFIRE_CARD_PERMISSION_DENIED',
	0x0C93 : 'DESFIRE_CARD_PARAMETER_ERROR',
	0x0CA0 : 'DESFIRE_CARD_APPLICATION_NOT_FOUND',
	0x0CA1 : 'DESFIRE_CARD_APPL_INTEGRITY_ERROR',
	0x0CAE : 'DESFIRE_CARD_AUTHENTICATION_ERROR',
	0x0CAF : 'DESFIRE_CARD_ADDITIONAL_FRAME',
	0x0CBE : 'DESFIRE_CARD_BOUNDARY_ERROR',
	0x0CC1 : 'DESFIRE_CARD_PICC_INTEGRITY_ERROR',
	0x0CCA : 'DESFIRE_CARD_COMMAND_ABORTED',
	0x0CCD : 'DESFIRE_CARD_PICC_DISABLED_ERROR',
	0x0CCE : 'DESFIRE_CARD_COUNT_ERROR',
	0x0CDE : 'DESFIRE_CARD_DUPLICATE_ERROR',
	0x0CEE : 'DESFIRE_CARD_EEPROM_ERROR_DES',
	0x0CF0 : 'DESFIRE_CARD_FILE_NOT_FOUND',
	0x0CF1 : 'DESFIRE_CARD_FILE_INTEGRITY_ERROR', 
}

####################################################################
def GetCardUID():

    aes_key_nr = c_ubyte()
    aid = c_uint32()
    aid_key_nr = c_ubyte()
    uid = (c_ubyte * 11)()
   
    card_uid_len = c_ubyte() 
    card_status = c_uint32()
    exec_time = c_uint32()
    
    aes_key_nr = int(globals.settings[4])
    aid = int(globals.settings[1])
    aid_key_nr = int(globals.settings[2])
    
    c = str() #used for printing out UID
    
    if globals.internal_key is False:
    
        pk_key = (c_ubyte * 16)()
        if PrepareKey(pk_key) != False:
            pk_key = PrepareKey(pk_key)
        else:
            print("Wrong AES key in config.txt")
            return
        
        getUidFunc = uFR.uFR_int_GetDesfireUid_PK
        getUidFunc.argtypes = [(c_ubyte * 16),c_uint32, c_ubyte, c_ubyte*11, POINTER(c_ubyte), POINTER(c_uint),POINTER(c_uint)]
        
        status = getUidFunc(pk_key, aid, aid_key_nr, uid, byref(card_uid_len), byref(card_status), byref(exec_time))
            
        if card_status.value == 3001:
            print("CARD UID : ")
            for n in range(7):
                c +=  '%0.2x' % uid[n] + ':'
            print(c.upper()[:-1])
            print("Function status: " + ErrorCodes.UFCODER_ERROR_CODES[status])
            print("Card status: " + DESFIRE_ERROR_CODES[card_status.value])       
            print("Exec time: " + str(exec_time.value) + " ms.")
            card_status = 0
            exec_time = 0
        else:
            print("Function status: " + ErrorCodes.UFCODER_ERROR_CODES[status])
            print("Card status: " + DESFIRE_ERROR_CODES[card_status.value])   
    else:
        
        status = uFR.uFR_int_GetDesfireUid(aes_key_nr, aid, aid_key_nr, uid, byref(card_uid_len), byref(card_status), byref(exec_time))
        
        if card_status.value == 3001:
            for n in range(7):
                c +=  '%0.2x' % uid[n] + ':'
            print(c.upper()[:-1])
            print("Function status: " + ErrorCodes.UFCODER_ERROR_CODES[status])
            print("Card status: " + DESFIRE_ERROR_CODES[card_status.value])       
            print("Exec time: " + str(exec_time.value) + " ms.")
        else:
            print("Function status: " + ErrorCodes.UFCODER_ERROR_CODES[status])
            print("Card status: " + DESFIRE_ERROR_CODES[card_status.value])
        
    return status


#################################################################

def FormatCard(): 

    aes_key_nr = c_ubyte()
    card_status = c_uint32()
    exec_time = c_uint32()  

    aes_key_nr = int(globals.settings[2])
    
    if globals.internal_key == False:
        
        pk_key = (c_ubyte * 16)()
        if PrepareKey(pk_key) != False:
            pk_key = PrepareKey(pk_key)
        else:
            print("Wrong AES key in config.txt")
            return
        
        formatCardFunc = uFR.uFR_int_DesfireFormatCard_PK
        formatCardFunc.argtypes = [(c_ubyte * 16), POINTER(c_uint),POINTER(c_uint)]
        
        status = formatCardFunc(pk_key, byref(card_status), byref(exec_time))
        
        if card_status.value == 3001:
            print("Card successfully formatted.")
            print("Function status: " + ErrorCodes.UFCODER_ERROR_CODES[status])
            print("Card status: " + DESFIRE_ERROR_CODES[card_status.value])  
            print("Exec time: " + str(exec_time.value) + " ms.")
            card_status = 0
            exec_time = 0
        else:
            print("Card format failed.")
            print("Function status: " + ErrorCodes.UFCODER_ERROR_CODES[status])
            print("Card status: " + DESFIRE_ERROR_CODES[card_status.value])  
            print("Exec time: " + str(exec_time.value) + " ms.")
    else: 
        
        formatCardFunc = uFR.uFR_int_DesfireFormatCard
        formatCardFunc.argtypes = [c_ubyte, POINTER(c_uint),POINTER(c_uint)]
        
        status = formatCardFunc(aes_key_nr, byref(card_status), byref(exec_time))
        
        if card_status.value == 3001:
            print("Card successfully formatted.")
            print("Function status: " + ErrorCodes.UFCODER_ERROR_CODES[status])
            print("Card status: " + DESFIRE_ERROR_CODES[card_status.value])  
            print("Exec time: " + str(exec_time.value) + " ms.")
            card_status = 0
            exec_time = 0
        else:
            print("Card format failed.")
            print("Function status: " + ErrorCodes.UFCODER_ERROR_CODES[status])
            print("Card status: " + DESFIRE_ERROR_CODES[card_status.value])  
            print("Exec time: " + str(exec_time.value) + " ms.")

#################################################################

def DEStoAES():

    funcDEStoAES = uFR.DES_to_AES_key_type
    
    status = funcDEStoAES()
    print(status)
    if status == 0:
            print("Key type changed to AES")
            print("New AES key is 00000000000000000000000000000000")
            print("Function status: " + ErrorCodes.UFCODER_ERROR_CODES[status])
    else:
        print("Key type change failed.")
        print("Function status: " + ErrorCodes.UFCODER_ERROR_CODES[status])

#################################################################

def AEStoDES():

    funcAEStoDES = uFR.AES_to_DES_key_type
    
    status = funcAEStoDES()
    if status == 0:
            print("Key type changed to DES")
            print("New DES key is 0000000000000000 ")
            print("Function status: " + ErrorCodes.UFCODER_ERROR_CODES[status])
    else:
        print("Key type change failed.")
        print("Function status: " + ErrorCodes.UFCODER_ERROR_CODES[status])
        
#################################################################

def GetFreeMemory():

    getFreeMemFunc = uFR.uFR_int_DesfireFreeMem
    getFreeMemFunc.argtypes = [POINTER(c_uint),POINTER(c_uint),POINTER(c_uint)]
    free_mem = c_uint32()
    card_status = c_uint32()
    exec_time = c_uint32()    
    
    status = getFreeMemFunc(byref(free_mem), byref(card_status), byref(exec_time))
    
    if status == 0:
        print("Available memory: " + str(free_mem.value) + " bytes.")
        print("Function status: " + ErrorCodes.UFCODER_ERROR_CODES[status])
        print("Card status: " + DESFIRE_ERROR_CODES[card_status.value])  
        print("Exec time: " + str(exec_time.value) + " ms.")
        card_status = 0
        exec_time = 0
    else:
        print("Function status: " + ErrorCodes.UFCODER_ERROR_CODES[status])
        print("Card status: " + DESFIRE_ERROR_CODES[card_status.value])  
        
#################################################################

def SetRandomID():

    card_status = c_uint32()
    exec_time = c_uint32()  
    
    aes_key_nr = int(globals.settings[4])
     #pk
    if globals.internal_key == False:
        pk_key = (c_ubyte * 16)()
        if PrepareKey(pk_key) != False:
            pk_key = PrepareKey(pk_key)
        else:
            print("Wrong AES key in config.txt")
            return
        
        setRandomIdFunc = uFR.uFR_int_DesfireSetConfiguration_PK
        setRandomIdFunc.argtypes = [(c_ubyte * 16), c_ubyte, c_ubyte, POINTER(c_uint), POINTER(c_uint)]
        
        status = setRandomIdFunc(pk_key, 1, 0, byref(card_status), byref(exec_time))
        
        if status == 0:
            print("Function status: " + ErrorCodes.UFCODER_ERROR_CODES[status])
            print("Card status: " + DESFIRE_ERROR_CODES[card_status.value])        
            print("Exec time: " + str(exec_time.value) + " ms.")
            card_status = 0
            exec_time = 0
        else:
            print("Function status: " + ErrorCodes.UFCODER_ERROR_CODES[status])
            print("Card status: " + DESFIRE_ERROR_CODES[card_status.value])  
            card_status = 0
            exec_time = 0
    else: #rk
    
        setRandomIdFunc = uFR.uFR_int_DesfireSetConfiguration
        
        status = setRandomIdFunc(aes_key_nr, 1, 0, byref(card_status), byref(exec_time))
        
        if card_status.value == 3001:
            print("Function status: " + ErrorCodes.UFCODER_ERROR_CODES[status])
            print("Card status: " + DESFIRE_ERROR_CODES[card_status.value])        
            print("Exec time: " + str(exec_time.value) + " ms.")
            card_status = 0
            exec_time = 0
        else:
            print("Function status: " + ErrorCodes.UFCODER_ERROR_CODES[status])
            print("Card status: " + DESFIRE_ERROR_CODES[card_status.value])  
            card_status = 0
            exec_time = 0
#################################################################

def InternalKeysLock():
    print("Input password (8 characters):")
    password = raw_input()
    pw_len = len(password)
    if pw_len != 8:
        print("Password must be 8 characters long")
    else:
        pw_array = (c_ubyte*8)()
        pw_array = (ctypes.c_ubyte * 8)(*[ctypes.c_ubyte(ord(c)) for c in password[:8]])
            
        internalKeysLockFunc = uFR.ReaderKeysLock
        internalKeysLockFunc.argtypes = [(c_ubyte*8)]
        status = internalKeysLockFunc(pw_array)
        if status == 0:
            print("Internal keys locked")
        else:
            print("Failed, status: " + ErrorCodes.UFCODER_ERROR_CODES[status])
            
####################################################################
 
def InternalKeysUnlock():
    print("Input password (8 characters):")
    password = raw_input()
    #password = list(password)
    pw_len = len(password)
    if pw_len != 8:
        print("Password must be 8 characters long")
    else:
        pw_array = (c_ubyte*8)()
        pw_array = (ctypes.c_ubyte * 8)(*[ctypes.c_ubyte(ord(c)) for c in password[:8]])

        internalKeysUnlockFunc = uFR.ReaderKeysUnlock        
        internalKeysUnlockFunc.argtypes = [(c_ubyte*8)]
        status = internalKeysUnlockFunc(pw_array)
        if status == 0:
            print("Internal keys unlocked")
        else:
            print("Failed, status: " + ErrorCodes.UFCODER_ERROR_CODES[status]) 
                       
####################################################################

def GetBaudRate():
    
    tx_speed = c_ubyte()
    rx_speed = c_ubyte()
    
    getBaudRateFunc = uFR.GetSpeedParameters
    getBaudRateFunc.argtypes = [POINTER(c_ubyte), POINTER(c_ubyte)]
    
    status = getBaudRateFunc(byref(tx_speed), byref(rx_speed))
    
    if status == 0:
        if tx_speed.value == 0:
            print("TX baud rate = 106 kbps;")
        elif tx_speed.value == 1:
            print("TX baud rate = 212 kbps;")
        elif tx_speed.value == 2:
            print("TX baud rate = 424 kbps;")
        elif tx_speed.value == 3:
            print("TX baud rate = 848 kbps;")
            
        if rx_speed.value == 0:
            print("RX baud rate = 106 kbps;")
        elif rx_speed.value == 1:
            print("RX baud rate = 212 kbps;")
        elif rx_speed.value == 2:
            print("RX baud rate = 424 kbps;")
        elif rx_speed.value == 3:
            print("RX baud rate = 848 kbps;")
            
#################################################################

def SetBaudRate():

    tx_speed = c_ubyte()
    rx_speed = c_ubyte()
    
    print("Enter value for setting transmit rate (tx speed)")
    print("0 - 106 kbps")
    print("1 - 212 kbps")
    print("2 - 424 kbps")
    print("3 - 848 kbps")
    
    tx_speed = raw_input()
    
    print("Enter value for setting transmit rate (rx speed)")
    print("0 - 106 kbps")
    print("1 - 212 kbps")
    print("2 - 424 kbps")
    print("3 - 848 kbps")
    
    rx_speed = raw_input()
     
    tx_speed = c_char(tx_speed)
    rx_speed = c_char(rx_speed)
    
    setBaudRateFunc = uFR.SetSpeedPermanently
    setBaudRateFunc.argtypes=[c_char, c_char]
    
    status = setBaudRateFunc(tx_speed, rx_speed)
    
    if status == 0:
        print("Operation completed. Status: " +  ErrorCodes.UFCODER_ERROR_CODES[status])
    else:
        print("Communication error")
        print("setSpeedPermanently(): " + ErrorCodes.UFCODER_ERROR_CODES[status])
        
#################################################################

def StoreKeyIntoReader():

    card_status = c_uint32()
    exec_time = c_uint32()
    
    print(" Input AES key number (0 - 15): ")
    key_no = raw_input()
    key_no = c_ubyte(int(key_no))
 
    print("Enter key you want to write into reader:")
    key = raw_input()
    key = key.upper()
    key = ConvertInputKeyToAesKey(key)
    
    storeKeyFunc = uFR.uFR_int_DesfireWriteAesKey
    storeKeyFunc.argtypes = [c_ubyte, (c_ubyte*16)]
    status = 0
    status = storeKeyFunc(key_no.value, key)
    
    if status == 0:
        print("Function status: " + ErrorCodes.UFCODER_ERROR_CODES[status])
        print("Card status: " + DESFIRE_ERROR_CODES[card_status.value])         
        print("Exec time: " + str(exec_time.value) + " ms.")
        card_status = 0
        exec_time = 0
    else:
        print("Function status: " + ErrorCodes.UFCODER_ERROR_CODES[status])
        print("Card status: " + DESFIRE_ERROR_CODES[card_status.value])  
        card_status = 0
        exec_time = 0
    
#################################################################

def ChangeKeySettings():
 
    card_status = c_uint32()
    exec_time = c_uint32()
    
    aid = int(globals.settings[1])
    aes_key_nr = int(globals.settings[4])
    
    temp = 0
    
    setting = c_ubyte()
    choice = str()
    
    print(" Choose key settings:")
    print(" 0 - No settings")
    print(" 1 - Settings not changeable anymore")
    print(" 2 - Create or delete application with master key authentication")
    print(" 3 - Master key not changeable anymore")
    print(" 4 - Settings not changeable anymore and create or delete application with master key")
    print(" 5 - Settings and master key not changeable anymore")
    print(" 6 - Create and delete application with master key and master key is not changeable anymore")
    print(" 7 - Settings not changeable anymore, create or delete application with master key")
    print("     master key is not changeable anymore")
    
    choice = raw_input()
        
    if choice == '1':
        temp |= 0x04       
    elif choice == '2':
        temp |= 0x02
    elif choice == '3':
        temp |= 0x01
    elif choice == '4':
        temp |= 0x04
        temp |= 0x02
    elif choice == '5':
        temp |= 0x04
        temp |= 0x01
    elif choice == '6':
        temp |= 0x02
        temp |= 0x01
    elif choice == '7':
        temp |= 0x04
        temp |= 0x02
        temp |= 0x01
        
    #################
    
    if temp == 0:
        setting = DESFIRE_KEY_SETTINGS['DESFIRE_KEY_SET_CREATE_WITHOUT_AUTH_SET_CHANGE_KEY_CHANGE']
        
    elif temp == 1:
        setting = DESFIRE_KEY_SETTINGS['DESFIRE_KEY_SET_CREATE_WITHOUT_AUTH_SET_CHANGE_KEY_NOT_CHANGE']
     
    elif temp == 2:
        setting = DESFIRE_KEY_SETTINGS['DESFIRE_KEY_SET_CREATE_WITH_AUTH_SET_CHANGE_KEY_CHANGE']
       
    elif temp == 3:
        setting = DESFIRE_KEY_SETTINGS['DESFIRE_KEY_SET_CREATE_WITH_AUTH_SET_CHANGE_KEY_NOT_CHANGE']
      
    elif temp == 4:
        setting = DESFIRE_KEY_SETTINGS['DESFIRE_KEY_SET_CREATE_WITHOUT_AUTH_SET_NOT_CHANGE_KEY_CHANGE']
       
    elif temp == 5:
        setting = DESFIRE_KEY_SETTINGS['DESFIRE_KEY_SET_CREATE_WITHOUT_AUTH_SET_NOT_CHANGE_KEY_NOT_CHANGE']
      
    elif temp == 6:
        setting = DESFIRE_KEY_SETTINGS['DESFIRE_KEY_SET_CREATE_WITH_AUTH_SET_NOT_CHANGE_KEY_CHANGE']
      
    elif temp == 7:
        setting = DESFIRE_KEY_SETTINGS['DESFIRE_KEY_SET_CREATE_WITH_AUTH_SET_NOT_CHANGE_KEY_NOT_CHANGE']
               
    #########################
    
    if globals.internal_key == False:
        pk_key = (c_ubyte * 16)()
        if PrepareKey(pk_key) != False:
            pk_key = PrepareKey(pk_key)
        else:
            print("Wrong AES key in config.txt")
            return
        
        changeKeySettingsFunc = uFR.uFR_int_DesfireChangeKeySettings_PK
        changeKeySettingsFunc.argtypes = [(c_ubyte * 16), c_uint32, c_ubyte, POINTER(c_uint32), POINTER(c_uint32)]
        status = changeKeySettingsFunc(pk_key, aid, setting, byref(card_status), byref(exec_time))
        
        if card_status.value == 3001:
            print("Function status: " + ErrorCodes.UFCODER_ERROR_CODES[status])
            print("Card status: " + DESFIRE_ERROR_CODES[card_status.value])       
            print("Exec time: " + str(exec_time.value) + " ms.")
            card_status = 0
            exec_time = 0
        else:
            print("Function status: " + ErrorCodes.UFCODER_ERROR_CODES[status])
            print("Card status: " + DESFIRE_ERROR_CODES[card_status.value])  
            card_status = 0
            exec_time = 0
    else: 
        
        changeKeySettingsFunc = uFR.uFR_int_DesfireChangeKeySettings        
        status = changeKeySettingsFunc(aes_key_nr, aid, setting, byref(card_status), byref(exec_time))
        
        if card_status.value == 3001:
            print("Change of keys settings successfull.")
            print("Function status: " + ErrorCodes.UFCODER_ERROR_CODES[status])
            print("Card status: " + DESFIRE_ERROR_CODES[card_status.value])        
            print("Exec time: " + str(exec_time.value) + " ms.")
            card_status = 0
            exec_time = 0
        else:
            print("Change of keys settings failed.")
            print("Function status: " + ErrorCodes.UFCODER_ERROR_CODES[status])
            print("Card status: " + DESFIRE_ERROR_CODES[card_status.value]) 
            card_status = 0
            exec_time = 0
            
#################################################################
            
def GetKeySettings():
    
    card_status = c_uint32()
    exec_time = c_uint32()
    
    setting = c_ubyte()        
    max_key_nr = c_ubyte()    
    
    aid = int(globals.settings[1])
    aes_key_nr = int(globals.settings[4])    
    
    set_temp = 0
    
    set_not_changeable = bool()
    create_with_master = bool()
    master_not_changeable = bool()
    
    if globals.internal_key == False:
        pk_key = (c_ubyte * 16)()
        if PrepareKey(pk_key) != False:
            pk_key = PrepareKey(pk_key)
        else:
            print("Wrong AES key in config.txt")
            return
        
        getKeySettingsFunc = uFR.uFR_int_DesfireGetKeySettings_PK
        
        getKeySettingsFunc.argtypes = [(c_ubyte * 16), c_uint32, POINTER(c_ubyte), POINTER(c_ubyte), POINTER(c_uint32), POINTER(c_uint32)]
        status = getKeySettingsFunc(pk_key, aid, byref(setting), byref(max_key_nr), byref(card_status), byref(exec_time))
    else:    
        getKeySettingsFunc = uFR.uFR_int_DesfireGetKeySettings
        
        getKeySettingsFunc.argtypes = [c_ubyte, c_uint32, POINTER(c_ubyte), POINTER(c_ubyte), POINTER(c_uint32), POINTER(c_uint32)]
        status = getKeySettingsFunc(aes_key_nr, aid, byref(setting), byref(max_key_nr), byref(card_status), byref(exec_time))
    
        
    if card_status.value == 3001:
        print("Operation completed")
        print("Function status is: " + ErrorCodes.UFCODER_ERROR_CODES[status])
        print("Card status: " + DESFIRE_ERROR_CODES[card_status.value])
        print("Execution time: " + str(exec_time.value) + " ms")
        print("Maximal number of keys into application: " + str(max_key_nr.value))        
        
        setting.value &= 0x0F
        
        if setting.value == DESFIRE_KEY_SETTINGS['DESFIRE_KEY_SET_CREATE_WITHOUT_AUTH_SET_CHANGE_KEY_CHANGE']:
            set_temp = 0
        elif setting.value == DESFIRE_KEY_SETTINGS['DESFIRE_KEY_SET_CREATE_WITHOUT_AUTH_SET_CHANGE_KEY_NOT_CHANGE']:
            set_temp = 1
        elif setting.value == DESFIRE_KEY_SETTINGS['DESFIRE_KEY_SET_CREATE_WITH_AUTH_SET_CHANGE_KEY_CHANGE']:
            set_temp = 2 
        elif setting.value == DESFIRE_KEY_SETTINGS['DESFIRE_KEY_SET_CREATE_WITH_AUTH_SET_CHANGE_KEY_NOT_CHANGE']:
            set_temp = 3
        elif setting.value == DESFIRE_KEY_SETTINGS['DESFIRE_KEY_SET_CREATE_WITHOUT_AUTH_SET_NOT_CHANGE_KEY_CHANGE']:
            set_temp = 4
        elif setting.value == DESFIRE_KEY_SETTINGS['DESFIRE_KEY_SET_CREATE_WITHOUT_AUTH_SET_NOT_CHANGE_KEY_NOT_CHANGE']:
            set_temp = 5
        elif setting.value == DESFIRE_KEY_SETTINGS['DESFIRE_KEY_SET_CREATE_WITH_AUTH_SET_NOT_CHANGE_KEY_CHANGE']:
            set_temp = 6
        elif setting.value == DESFIRE_KEY_SETTINGS['DESFIRE_KEY_SET_CREATE_WITH_AUTH_SET_NOT_CHANGE_KEY_NOT_CHANGE']:
           set_temp = 7
        else: 
            print('settings unknown')
      
        if set_temp & 0x04:
            set_not_changeable = True
        else:
            set_not_changeable = False
        if set_temp & 0x02:
            create_with_master = True
        else:
            create_with_master = False

        if set_temp & 0x01:
            master_not_changeable = True
        else:
            master_not_changeable = False
            
        if set_not_changeable == True and create_with_master == True and master_not_changeable == True:           
            print("7 - Settings not changable anymore, create or delete application with master key, master key is not changeable anymore")
                
        elif set_not_changeable == False and create_with_master == True and master_not_changeable == True:            
            print("6 - Create and delete application with master key and master key is not changable anymore")
         
        elif set_not_changeable == True and create_with_master == False and master_not_changeable == True:            
            print("5 - Settings and master key not changable anymore")
            
        elif set_not_changeable == True and create_with_master == True and master_not_changeable == False:            
            print("4 - Settings not changeable anymore and create or delete application with master key")
           
        elif set_not_changeable == False and create_with_master == False and master_not_changeable == True:            
            print("3 - Master key not changeable anymore")
            
        elif set_not_changeable == False and create_with_master == True and master_not_changeable == False:            
            print("2 - Create or delete application with master key authentication")
            
        elif set_not_changeable == True and create_with_master == False and master_not_changeable == False:            
            print("1 - Settings not changeable anymore")
            
        elif set_not_changeable == False and create_with_master == False and master_not_changeable == False:           
            print("0 - No settings set.")
           

    else:
         print("Error occurred")
         print("Function status is: " + ErrorCodes.UFCODER_ERROR_CODES[status])
         print("Card status: " + DESFIRE_ERROR_CODES[card_status.value])
         
#################################################################

def ChangeAESKey():

    card_status = c_uint32()
    exec_time = c_uint32()
    
    aid = int(globals.settings[1])    
    aid_key_nr_auth = int(globals.settings[2])
    aes_key_nr = int(globals.settings[4])    
    
    print("Input old AES key (16 bytes): ")
    old_aes_key = raw_input()
    old_aes_key = old_aes_key.upper()
    if len(old_aes_key) != 32:
        print("Old AES key must be 16 bytes long")
    else:
        old_aes_key = ConvertInputKeyToAesKey(old_aes_key)
    
    print("Input new AES key (16 bytes): ")
    new_aes_key = raw_input()
    new_aes_key = new_aes_key.upper()
    
    if len(new_aes_key) != 32:
        print("new AES key must be 16 bytes long")
    else:
        new_aes_key = ConvertInputKeyToAesKey(new_aes_key)
            
    print("Enter AID key number you wish to change:")
    aid_key_nr = raw_input()
    aid_key_nr = c_ubyte(int(aid_key_nr))
    #print(aid_key_nr)
    
    if globals.internal_key == False:
        pk_key = (c_ubyte * 16)()
        if PrepareKey(pk_key) != False:
            pk_key = PrepareKey(pk_key)
        else:
            print("Wrong AES key in config.txt")
            return
        
        changeAESKeyFunc = uFR.uFR_int_DesfireChangeAesKey_PK
        changeAESKeyFunc.argtypes = [(c_ubyte*16), c_uint32, c_ubyte, (c_ubyte*16), c_ubyte, (c_ubyte*16), POINTER(c_uint32), POINTER(c_uint32)]
        status = changeAESKeyFunc(pk_key, aid, aid_key_nr_auth, new_aes_key, aid_key_nr, old_aes_key, byref(card_status), byref(exec_time))
    else:
        changeAESKeyFunc = uFR.uFR_int_DesfireChangeAesKey
        changeAESKeyFunc.argtypes = [c_ubyte, c_uint32, c_ubyte, (c_ubyte*16), c_ubyte, (c_ubyte*16), POINTER(c_uint32), POINTER(c_uint32)]
        status = changeAESKeyFunc(aes_key_nr, aid, aid_key_nr_auth, new_aes_key, aid_key_nr, old_aes_key, byref(card_status), byref(exec_time))
    
    print("Operation completed")
    print("Function status is: " + ErrorCodes.UFCODER_ERROR_CODES[status])
    print("Card status: " + DESFIRE_ERROR_CODES[card_status.value])
    print("Execution time: " + str(exec_time.value) + " ms")
    
#################################################################    
    
def MakeApplication():
 
    card_status = c_uint32()
    exec_time = c_uint32()
        
    setting = c_ubyte()        
    max_key_nr = c_ubyte()
   
    aid = int(globals.settings[1])       
    aes_key_nr = int(globals.settings[4]) 
        
    temp = 0
        
    print("Input AID number (3 bytes hex): ")
    aid = raw_input()
    aid = int(aid)
        
    print("Input maximal key number: ")
    max_key_nr = raw_input()
    max_key_nr = int(max_key_nr)
        
    print("aid -> " + str(aid))
    print("key nr -> " + str(max_key_nr))
        
    print(" Choose application settings:")
    print(" 0 - No settings")
    print(" 1 - Settings not changeable anymore")
    print(" 2 - Create or delete application with master key authentication")
    print(" 3 - Master key not changeable anymore")
    print(" 4 - Settings not changeable anymore and create or delete application with master key")
    print(" 5 - Settings and master key not changeable anymore")
    print(" 6 - Create and delete application with master key and master key is not changeable anymore")
    print(" 7 - Settings not changeable anymore, create or delete application with master key")
    print("     master key is not changeable anymore")
        
    choice = raw_input()
            
    if choice == '1':
        temp |= 0x04       
    elif choice == '2':
        temp |= 0x02
    elif choice == '3':
        temp |= 0x01
    elif choice == '4':
        temp |= 0x04
        temp |= 0x02
    elif choice == '5':
        temp |= 0x04
        temp |= 0x01
    elif choice == '6':
        temp |= 0x02
        temp |= 0x01
    elif choice == '7':
        temp |= 0x04
        temp |= 0x02
        temp |= 0x01
        
    #################
    
    if temp == 0:
        setting = DESFIRE_KEY_SETTINGS['DESFIRE_KEY_SET_CREATE_WITHOUT_AUTH_SET_CHANGE_KEY_CHANGE']
        
    elif temp == 1:
        setting = DESFIRE_KEY_SETTINGS['DESFIRE_KEY_SET_CREATE_WITHOUT_AUTH_SET_CHANGE_KEY_NOT_CHANGE']
        
    elif temp == 2:
        setting = DESFIRE_KEY_SETTINGS['DESFIRE_KEY_SET_CREATE_WITH_AUTH_SET_CHANGE_KEY_CHANGE']
        
    elif temp == 3:
        setting = DESFIRE_KEY_SETTINGS['DESFIRE_KEY_SET_CREATE_WITH_AUTH_SET_CHANGE_KEY_NOT_CHANGE']
        
    elif temp == 4:
        setting = DESFIRE_KEY_SETTINGS['DESFIRE_KEY_SET_CREATE_WITHOUT_AUTH_SET_NOT_CHANGE_KEY_CHANGE']
       
    elif temp == 5:
        setting = DESFIRE_KEY_SETTINGS['DESFIRE_KEY_SET_CREATE_WITHOUT_AUTH_SET_NOT_CHANGE_KEY_NOT_CHANGE']
        
    elif temp == 6:
        setting = DESFIRE_KEY_SETTINGS['DESFIRE_KEY_SET_CREATE_WITH_AUTH_SET_NOT_CHANGE_KEY_CHANGE']
        
    elif temp == 7:
        setting = DESFIRE_KEY_SETTINGS['DESFIRE_KEY_SET_CREATE_WITH_AUTH_SET_NOT_CHANGE_KEY_NOT_CHANGE']
        
        
    #########################
    
    if globals.internal_key == False:
        pk_key = (c_ubyte*16)()
        pk_key = PrepareKey(pk_key)
    else:
        aes_key_nr = int(globals.settings[4])
        
    if globals.master_authent_req == True:
        if globals.internal_key == True:
            makeApplicationFunc = uFR.uFR_int_DesfireCreateAesApplication
            status = makeApplicationFunc(aes_key_nr, aid, setting, max_key_nr, byref(card_status), byref(exec_time))
                
        else:
            makeApplicationFunc = uFR.uFR_int_DesfireCreateAesApplication_PK
            makeApplicationFunc.argtypes = [(c_ubyte*16), c_uint32, c_ubyte, c_ubyte, POINTER(c_uint32),POINTER(c_uint32)]
            status = makeApplicationFunc(pk_key, aid, setting, max_key_nr, byref(card_status), byref(exec_time))
    else:
        makeApplicationFunc = uFR.uFR_int_DesfireCreateAesApplication_no_auth
        status = makeApplicationFunc(aid, setting, max_key_nr, byref(card_status), byref(exec_time))
        
        
    if card_status.value == 3001:    
        print("Desfire Application created successfully.")
        print("Function status: " + ErrorCodes.UFCODER_ERROR_CODES[status])
        print("Card status: " + DESFIRE_ERROR_CODES[card_status.value])        
        print("Exec time: " + str(exec_time.value) + " ms.")
        card_status = 0
        exec_time = 0
    else:
        print("Desfire Application created failed.")
        print("Function status: " + ErrorCodes.UFCODER_ERROR_CODES[status])
        print("Card status: " + DESFIRE_ERROR_CODES[card_status.value])        
        print("Exec time: " + str(exec_time.value) + " ms.")
        card_status = 0
        exec_time = 0

#################################################################        
        
def DeleteApplication():

    card_status = c_uint32()
    exec_time = c_uint32()
    
    print("Input AID to delete (3 bytes hex): ")
    aid = raw_input()
    aid = int(aid)
    
    if globals.internal_key == False:
        pk_key = (c_ubyte*16)()
        pk_key = PrepareKey(pk_key)
        
    else:
        aes_key_nr = int(globals.settings[4])
        
    if globals.internal_key == False:
        deleteApplicationFunc = uFR.uFR_int_DesfireDeleteApplication_PK
        deleteApplicationFunc.argtypes = [(c_ubyte*16), c_uint32, POINTER(c_uint32), POINTER(c_uint32)]
        status = deleteApplicationFunc(pk_key, aid, byref(card_status), byref(exec_time))
        
    else:
        deleteApplicationFunc = uFR.uFR_int_DesfireDeleteApplication
        status = deleteApplicationFunc(aes_key_nr, aid, byref(card_status), byref(exec_time))
        
    if card_status.value == 3001:    
        print("Desfire Application deleted successfully.")
        print("Function status: " + ErrorCodes.UFCODER_ERROR_CODES[status])
        print("Card status: " + DESFIRE_ERROR_CODES[card_status.value])        
        print("Exec time: " + str(exec_time.value) + " ms.")
        card_status = 0
        exec_time = 0
    else:
        print("Desfire Application deletion failed.")
        print("Function status: " + ErrorCodes.UFCODER_ERROR_CODES[status])
        print("Card status: " + DESFIRE_ERROR_CODES[card_status.value])        
        print("Exec time: " + str(exec_time.value) + " ms.")
        card_status = 0
        exec_time = 0
 
################################################################# 
        
def MakeFile():

    card_status = c_uint32()
    exec_time = c_uint32()
    
    communication_settings = c_ubyte()
    
    aes_key_nr = c_uint32()
    aid = int(globals.settings[1])
    
    file_size = c_uint32()
    file_id = c_uint32()    
    
    lower_limit = c_uint32()
    upper_limit = c_uint32()
    value = c_uint32()
    
    limited_credit_enabled = c_ubyte()
    free_get_choice = c_ubyte()
    
    print("Input File ID: ")
    file_id = raw_input()
    file_id = int(file_id)
    
    
    print("Choose communication mode:")
    print("1 -PLAIN")
    print("2 - MACKED")
    print("3 - ENCIPHERED")
    
    communication_settings = raw_input()
    communication_settings = int(communication_settings)
    
    print("Choose file type:")
    print("1 - Standard data file")
    print("2 - Value file")
    
    file_choice = raw_input()
    file_choice = int(file_choice)
    
    if file_choice < 1 or file_choice > 2:
        print('nope')
        return
    else:    
        file_choice = int(file_choice)
    
    print("Enter Read key number:")
    read_key_nr = raw_input()
    read_key_nr = int(read_key_nr)
    
    print("Enter Write key number:")
    write_key_nr = raw_input()
    write_key_nr = int(write_key_nr)
    
    print("Enter Read/Write key number:")
    read_write_key_nr = raw_input()
    read_write_key_nr = int(read_write_key_nr)
    
    
    print("Enter Change key number:")
    change_key_nr = raw_input()
    change_key_nr = int(change_key_nr)
    
    
    if globals.internal_key == False:
        pk_key = (c_ubyte*16)()
        pk_key = PrepareKey(pk_key)
        
    else:
        aes_key_nr = int(globals.settings[4])
        
        
    if file_choice == 1:
        print("Enter size of the file you wish to create: ")
        file_size = raw_input()
        file_size = int(file_size)

        
    else:
        print("Enter lower limit of your Value file: ")
        lower_limit = raw_input()
        lower_limit = int(lower_limit)
        
        print("Enter upper limit of your Value file: ")
        upper_limit = raw_input()
        upper_limit = int(upper_limit)
        
        print("Enter value of your Value file:")
        value = raw_input()
        value = int(value)
        
        print("Do you wish to enable Limited credit?")
        print("1 - Yes")
        print("2 - No")
        limited_credit_enabled = raw_input()
        limited_credit_enabled = int(limited_credit_enabled)
        
        print("Do you wish to enable Free get value?")
        print("1 - Yes")
        print("2 - No")
        free_get_choice = raw_input()
        free_get_choice = int(free_get_choice)       
    
    if globals.master_authent_req == True:
        if globals.internal_key == True:
            if file_choice == 1:
                print("File_choice == uFR.uFR_int_DesfireCreateStdDataFile")
                makeFileFunc = uFR.uFR_int_DesfireCreateStdDataFile
                makeFileFunc.argtypes = [c_ubyte, c_uint32, c_uint32, c_uint32, c_uint32, c_uint32, c_uint32, c_uint32, c_ubyte, POINTER(c_uint32), POINTER(c_uint32)]
                status = makeFileFunc(aes_key_nr, aid, file_id, file_size, read_key_nr, write_key_nr, read_write_key_nr, change_key_nr, communication_settings, byref(card_status), byref(exec_time))
                if card_status.value == 3001:
                    print("Desfire Create uFR_int_DesfireCreateStdDataFile successfull.")
                    
            else:
                makeValueFileFunc = uFR.uFR_int_DesfireCreateValueFile
                makeValueFileFunc.argtypes = [c_ubyte, c_uint32, c_uint32, c_uint32, c_uint32, c_uint32, c_uint32, c_uint32, c_uint32, c_uint32, c_uint32, c_ubyte, POINTER(c_uint32), POINTER(c_uint32)]
                status = makeValueFileFunc(aes_key_nr, aid, file_id, lower_limit, upper_limit, value, limited_credit_enabled, read_key_nr, write_key_nr, read_write_key_nr, change_key_nr, communication_settings, byref(card_status), byref(exec_time))
                if card_status.value == 3001:
                    print("Desfire Create uFR_int_DesfireCreateValueFile_PK successfull.")
                                
        else: ##PK
            if file_choice == 1:
                print("File_choice == uFR.uFR_int_DesfireCreateStdDataFile_PK")
                makeFileFunc = uFR.uFR_int_DesfireCreateStdDataFile_PK
                makeFileFunc.argtypes = [(c_ubyte*16), c_uint32, c_uint32, c_uint32, c_uint32, c_uint32, c_uint32, c_uint32, c_ubyte, POINTER(c_uint32), POINTER(c_uint32)]
                status = makeFileFunc(pk_key, aid, file_id, file_size, read_key_nr, write_key_nr, read_write_key_nr, change_key_nr, communication_settings, byref(card_status), byref(exec_time))
                if card_status.value == 3001:
                    print("Desfire uFR_int_DesfireCreateStdDataFile_PK successfull.")
                    
            else:
                makeValueFileFunc = uFR.uFR_int_DesfireCreateValueFile_PK
                makeValueFileFunc.argtypes = [(c_ubyte*16), c_uint32, c_uint32, c_uint32, c_uint32, c_uint32, c_uint32, c_uint32, c_uint32, c_uint32, c_uint32, c_ubyte, POINTER(c_uint32), POINTER(c_uint32)]
                status = makeValueFileFunc(pk_key, aid, file_id, lower_limit, upper_limit, value, limited_credit_enabled, read_key_nr, write_key_nr, read_write_key_nr, change_key_nr, communication_settings, byref(card_status), byref(exec_time))
                if card_status.value == 3001:
                    print("Desfire uFR_int_DesfireCreateValueFile_PK successfull.")
           
    else:
        if file_choice == 1:
            print("File_choice == uFR.uFR_int_DesfireCreateStdDataFile_no_auth")
            makeFileFunc = uFR.uFR_int_DesfireCreateStdDataFile_no_auth
            makeFileFunc.argtypes = [c_uint32, c_uint32, c_uint32, c_uint32, c_uint32, c_uint32, c_uint32, c_ubyte, POINTER(c_uint32), POINTER(c_uint32)]
            status = makeFileFunc(aid, file_id, file_size, read_key_nr, write_key_nr, read_write_key_nr, change_key_nr, communication_settings, byref(card_status), byref(exec_time))
            if card_status.value == 3001:
                print("Desfire Create uFR_int_DesfireCreateStdDataFile_no_auth successfull.")
        
        else:
            makeValueFileFunc = uFR.uFR_int_DesfireCreateValueFile_no_auth
            makeValueFileFunc.argtypes = [c_uint32, c_uint32, c_uint32, c_uint32, c_uint32, c_uint32, c_uint32, c_uint32, c_uint32, c_uint32, c_ubyte, POINTER(c_uint32), POINTER(c_uint32)]
            status = makeValueFileFunc(pk_key, aid, file_id, lower_limit, upper_limit, value, limited_credit_enabled, read_key_nr, write_key_nr, read_write_key_nr, change_key_nr, communication_settings, byref(card_status), byref(exec_time))
            if card_status.value == 3001:
                print("Desfire Create uFR_int_DesfireCreateValueFile_no_auth successfull.")
        
        
    print("Function status: " + ErrorCodes.UFCODER_ERROR_CODES[status])
    print("Card status: " + DESFIRE_ERROR_CODES[card_status.value])        
    print("Exec time: " + str(exec_time.value) + " ms.")
    card_status = 0
    exec_time = 0    
    
#################################################################    
    
def DeleteFile():
    
    card_status = c_uint32()
    exec_time = c_uint32()
    
    aid = int(globals.settings[1])
    
    print("Enter File ID for deletion: ")
    file_no = raw_input()
    file_no = int(file_no)
    
    if globals.internal_key == False:
        pk_key = (c_ubyte*16)()
        pk_key = PrepareKey(pk_key)
    else:
        aes_key_nr = int(globals.settings[4])

    
    if globals.master_authent_req == True:
        if globals.internal_key == True:
            deleteFileFunc = uFR.uFR_int_DesfireDeleteFile
            deleteFileFunc.argtypes = [c_ubyte, c_uint32, c_uint32, POINTER(c_uint32), POINTER(c_uint32)]
            status = deleteFileFunc(aes_key_nr, aid, file_no, byref(card_status), byref(exec_time))
            if card_status.value == 3001:
                print("Desfire uFR_int_DesfireDeleteFile successfull.")
        
        else: 
            deleteFileFunc = uFR.uFR_int_DesfireDeleteFile_PK
            deleteFileFunc.argtypes = [(c_ubyte*16), c_uint32, c_uint32, POINTER(c_uint32), POINTER(c_uint32)]
            status = deleteFileFunc(pk_key, aid, file_no, byref(card_status), byref(exec_time))
            if card_status.value == 3001:
                print("Desfire uFR_int_DesfireDeleteFile successfull.")
        
    else:
        deleteFileFunc = uFR.uFR_int_DesfireDeleteFile_no_auth
        deleteFileFunc.argtypes = [c_uint32, c_uint32, POINTER(c_uint32), POINTER(c_uint32)]
        status = deleteFileFunc(aid, file_no, byref(card_status), byref(exec_time))
        if card_status.value == 3001:
            print("Desfire uFR_int_DesfireDeleteFile_no_auth successfull.")
        
    print("Function status: " + ErrorCodes.UFCODER_ERROR_CODES[status])
    print("Card status: " + DESFIRE_ERROR_CODES[card_status.value])        
    print("Exec time: " + str(exec_time.value) + " ms.")
    card_status = 0
    exec_time = 0    
        
#################################################################        
  
def ReadValueFile():

    card_status = c_uint32()
    exec_time = c_uint32()    
    
    aid = int(globals.settings[1])   
    aid_key_nr = int(globals.settings[2])
    file_id = int(globals.settings[3])    
    
    communication_settings = c_ubyte()    
    value = c_ubyte()        
  
    
    if globals.internal_key == False:
        pk_key = (c_ubyte*16)()
        pk_key = PrepareKey(pk_key)
        
    else: 
        aes_key_nr = int(globals.settings[4])     
    
    print("Choose communication mode:")
    print("1 - PLAIN.")
    print("2 - MACKED.")
    print("3 - ENCIPHERED.")
    
    communication_settings = raw_input()
    communication_settings = int(communication_settings)
    
    if globals.master_authent_req == True:
        if globals.internal_key == True:
            readValueFunc = uFR.uFR_int_DesfireReadValueFile
            readValueFunc.argtypes = [c_ubyte, c_uint32, c_uint32, c_uint32, c_ubyte, POINTER(c_ubyte), POINTER(c_uint32), POINTER(c_uint32)]
            status = readValueFunc(aes_key_nr, aid, aid_key_nr, file_id, communication_settings, byref(value), byref(card_status), byref(exec_time))
        else:
           readValueFunc = uFR.uFR_int_DesfireReadValueFile_PK
           readValueFunc.argtypes = [(c_ubyte*16), c_uint32, c_uint32, c_uint32, c_ubyte, POINTER(c_ubyte), POINTER(c_uint32), POINTER(c_uint32)]
           status = readValueFunc(pk_key, aid, aid_key_nr, file_id, communication_settings, byref(value), byref(card_status), byref(exec_time))
    else:
        readValueFunc = uFR.uFR_int_DesfireReadValueFile_no_auth
        readValueFunc.argtypes = [c_uint32, c_uint32, c_uint32, c_ubyte, POINTER(c_ubyte), POINTER(c_uint32), POINTER(c_uint32)]
        status = readValueFunc(aid, aid_key_nr, file_id, communication_settings, byref(value), byref(card_status), byref(exec_time))

    print("Function status: " + ErrorCodes.UFCODER_ERROR_CODES[status])
    print("Card status: " + DESFIRE_ERROR_CODES[card_status.value])        
    print("Execution time: " + str(exec_time.value) + " ms.")
    card_status = 0
    exec_time = 0    
    print("Value: " + str(value.value))
                      
#################################################################

def IncreaseValueFile():
    
    card_status = c_uint32()
    exec_time = c_uint32()    
    
    aid = int(globals.settings[1])    
    aid_key_nr = int(globals.settings[2])
    file_id = int(globals.settings[3])
    
    communication_settings = c_ubyte()    
    value = c_ubyte()        
  
      
    if globals.internal_key == False:
        pk_key = (c_ubyte*16)()
        pk_key = PrepareKey(pk_key)
        
    else: 
        aes_key_nr = int(globals.settings[4])
   
    print("Choose communication mode:")
    print("1 - PLAIN.")
    print("2 - MACKED.")
    print("3 - ENCIPHERED.")
    
    communication_settings = raw_input()
    communication_settings = int(communication_settings)
    
    print("Value for increasing: ")
    value = raw_input()
    value = int(value)    
    
    if globals.master_authent_req == True:
        if globals.internal_key == True:
            readValueFunc = uFR.uFR_int_DesfireIncreaseValueFile
            readValueFunc.argtypes = [c_ubyte, c_uint32, c_uint32, c_uint32, c_ubyte, c_ubyte, POINTER(c_uint32), POINTER(c_uint32)]
            status = readValueFunc(aes_key_nr, aid, aid_key_nr, file_id, communication_settings, value, byref(card_status), byref(exec_time))
        else:
           readValueFunc = uFR.uFR_int_DesfireIncreaseValueFile_PK
           readValueFunc.argtypes = [(c_ubyte*16), c_uint32, c_uint32, c_uint32, c_ubyte, c_ubyte, POINTER(c_uint32), POINTER(c_uint32)]
           status = readValueFunc(pk_key, aid, aid_key_nr, file_id, communication_settings, value, byref(card_status), byref(exec_time))
    else:
        readValueFunc = uFR.uFR_int_DesfireIncreaseValueFile_no_auth
        readValueFunc.argtypes = [c_uint32, c_uint32, c_uint32, c_ubyte, c_ubyte, POINTER(c_uint32), POINTER(c_uint32)]
        status = readValueFunc(aid, aid_key_nr, file_id, communication_settings, value, byref(card_status), byref(exec_time))

    print("Function status: " + ErrorCodes.UFCODER_ERROR_CODES[status])
    print("Card status: " + DESFIRE_ERROR_CODES[card_status.value])        
    print("Execution time: " + str(exec_time.value) + " ms.")
    card_status = 0
    exec_time = 0    
    print("Value increased by: " + str(value))
                 
#################################################################
                 
def DecreaseValueFile():
    
    card_status = c_uint32()
    exec_time = c_uint32()    
    
    aid = int(globals.settings[1])    
    aid_key_nr = int(globals.settings[2])
    file_id = int(globals.settings[3])
    
    communication_settings = c_ubyte()    
    value = c_ubyte()        
  
      
    if globals.internal_key == False:
        pk_key = (c_ubyte*16)()
        pk_key = PrepareKey(pk_key)
        
    else: 
        aes_key_nr = int(globals.settings[4])
   
    print("Choose communication mode:")
    print("1 - PLAIN.")
    print("2 - MACKED.")
    print("3 - ENCIPHERED.")
    
    communication_settings = raw_input()
    communication_settings = int(communication_settings)
    
    print("Value for increasing: ")
    value = raw_input()
    value = int(value)   
    
    if globals.master_authent_req == True:
        if globals.internal_key == True:
            readValueFunc = uFR.uFR_int_DesfireDecreaseValueFile
            readValueFunc.argtypes = [c_ubyte, c_uint32, c_uint32, c_uint32, c_ubyte, c_ubyte, POINTER(c_uint32), POINTER(c_uint32)]
            status = readValueFunc(aes_key_nr, aid, aid_key_nr, file_id, communication_settings, value, byref(card_status), byref(exec_time))
        else:
           readValueFunc = uFR.uFR_int_DesfireDecreaseValueFile_PK
           readValueFunc.argtypes = [(c_ubyte*16), c_uint32, c_uint32, c_uint32, c_ubyte, c_ubyte, POINTER(c_uint32), POINTER(c_uint32)]
           status = readValueFunc(pk_key, aid, aid_key_nr, file_id, communication_settings, value, byref(card_status), byref(exec_time))
    else:
        readValueFunc = uFR.uFR_int_DesfireDecreaseValueFile_no_auth
        readValueFunc.argtypes = [c_uint32, c_uint32, c_uint32, c_ubyte, c_ubyte, POINTER(c_uint32), POINTER(c_uint32)]
        status = readValueFunc(aid, aid_key_nr, file_id, communication_settings, value, byref(card_status), byref(exec_time))

    print("Function status: " + ErrorCodes.UFCODER_ERROR_CODES[status])
    print("Card status: " + DESFIRE_ERROR_CODES[card_status.value])        
    print("Execution time: " + str(exec_time.value) + " ms.")
    card_status = 0
    exec_time = 0    
    print("Value increased by: " + str(value))
                       
#################################################################            
            
def WriteStdFile():

    card_status = c_uint32()
    exec_time = c_uint32()    
    
    aid = int(globals.settings[1])    
    aid_key_nr = int(globals.settings[2])
    file_id = int(globals.settings[3])
    length = c_uint32()
    communication_settings = c_ubyte() 
      
    if globals.internal_key == False:
        pk_key = (c_ubyte*16)()
        pk_key = PrepareKey(pk_key)
        
    else: 
        aes_key_nr = int(globals.settings[4])
   
    print("Choose communication mode:")
    print("1 - PLAIN.")
    print("2 - MACKED.")
    print("3 - ENCIPHERED.")
    
    communication_settings = raw_input()
    communication_settings = int(communication_settings)
    
    file_length = os.stat("write.txt").st_size
    file = open("write.txt", 'r')
    with open('write.txt', 'r') as file:
        file_data = file.read().replace('\n', '')
    #print(file_data)
   
    data = (c_ubyte*file_length)()
    for x in range(file_length):
        data[x] = int(file_data[x], 16)
   
    
    if globals.master_authent_req == True:
        if globals.internal_key == True:
            writeStdFileFunc = uFR.uFR_int_DesfireWriteStdDataFile
            writeStdFileFunc.argtypes= [c_ubyte, c_uint32, c_uint32, c_uint32, c_uint32, c_uint32, c_ubyte, (c_ubyte*file_length), POINTER(c_uint32), POINTER(c_uint32)]
            status = writeStdFileFunc(aes_key_nr, aid, aid_key_nr, file_id, 0, file_length, communication_settings, data, byref(card_status), byref(exec_time))
        else: 
            writeStdFileFunc = uFR.uFR_int_DesfireWriteStdDataFile_PK
            writeStdFileFunc.argtypes= [(c_ubyte*16), c_uint32, c_uint32, c_uint32, c_uint32, c_uint32, c_ubyte, (c_ubyte*file_length), POINTER(c_uint32), POINTER(c_uint32)]
            status = writeStdFileFunc(pk_key, aid, aid_key_nr, file_id, 0, file_length, communication_settings, data, byref(card_status), byref(exec_time))
        
    else:
        writeStdFileFunc = uFR.uFR_int_DesfireWriteStdDataFile_no_auth
        writeStdFileFunc.argtypes= [c_uint32, c_uint32, c_uint32, c_uint32, c_uint32, c_ubyte, (c_ubyte*file_length), POINTER(c_uint32), POINTER(c_uint32)]
        status = writeStdFileFunc(aid, aid_key_nr, file_id, 0, file_length, communication_settings, data, byref(card_status), byref(exec_time))
    
    if card_status.value == 3001:
        print("Std file data write successfull")
    
    print("Function status: " + ErrorCodes.UFCODER_ERROR_CODES[status])
    print("Card status: " + DESFIRE_ERROR_CODES[card_status.value])        
    print("Execution time: " + str(exec_time.value) + " ms.")        
                  
def ReadStdFile():
   
    card_status = c_uint32()
    exec_time = c_uint32()    
    
    aid = int(globals.settings[1])    
    aid_key_nr = int(globals.settings[2])
    file_id = int(globals.settings[3])
    length = c_uint32()
    communication_settings = c_ubyte() 
    
    data = (c_ubyte*10000)()
      
    if globals.internal_key == False:
        pk_key = (c_ubyte*16)()
        pk_key = PrepareKey(pk_key)
        
    else: 
        aes_key_nr = int(globals.settings[4])
        
        
        
    print("Input file length to read")
    file_length = raw_input()
    file_length = int(file_length)
   
    print("Choose communication mode:")
    print("1 - PLAIN.")
    print("2 - MACKED.")
    print("3 - ENCIPHERED.")
    
    communication_settings = raw_input()
    communication_settings = int(communication_settings)
   
    if globals.master_authent_req == True:
        if globals.internal_key == True:
            writeStdFileFunc = uFR.uFR_int_DesfireReadStdDataFile
            writeStdFileFunc.argtypes= [c_ubyte, c_uint32, c_uint32, c_uint32, c_uint32, c_uint32, c_ubyte, (c_ubyte*10000), POINTER(c_uint32), POINTER(c_uint32)]
            status = writeStdFileFunc(aes_key_nr, aid, aid_key_nr, file_id, 0, file_length, communication_settings, data, byref(card_status), byref(exec_time))
        else: 
            writeStdFileFunc = uFR.uFR_int_DesfireReadStdDataFile_PK
            writeStdFileFunc.argtypes= [(c_ubyte*16), c_uint32, c_uint32, c_uint32, c_uint32, c_uint32, c_ubyte, (c_ubyte*10000), POINTER(c_uint32), POINTER(c_uint32)]
            status = writeStdFileFunc(pk_key, aid, aid_key_nr, file_id, 0, file_length, communication_settings, data, byref(card_status), byref(exec_time))
        
    else:
        writeStdFileFunc = uFR.uFR_int_DesfireReadStdDataFile_no_auth
        writeStdFileFunc.argtypes= [c_uint32, c_uint32, c_uint32, c_uint32, c_uint32, c_ubyte, (c_ubyte*10000), POINTER(c_uint32), POINTER(c_uint32)]
        status = writeStdFileFunc(aid, aid_key_nr, file_id, 0, file_length, communication_settings, data, byref(card_status), byref(exec_time))
    
    if card_status.value == 3001:
        print("Std file data read successfull")
    
    print("Function status: " + ErrorCodes.UFCODER_ERROR_CODES[status])
    print("Card status: " + DESFIRE_ERROR_CODES[card_status.value])        
    print("Execution time: " + str(exec_time.value) + " ms.")    
   
    f = open('read.txt', 'w')
    for x in range(file_length):
        hex_str = ('%x' % data[x]).upper()
        #f.write(('0x%02x' % data[x]).upper())
        f.write(hex_str)
   
   
   
   
   
   
            
            