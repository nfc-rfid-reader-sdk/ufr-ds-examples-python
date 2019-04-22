""" 
     
""" 
 
UFCODER_ERROR_CODES = {
    0x00 :'UFR_OK',
    0x01 :'UFR_COMMUNICATION_ERROR',
    0x02 :'UFR_CHKSUM_ERROR',
    0x03 :'UFR_READING_ERROR',
    0x04 :'UFR_WRITING_ERROR',
    0x05 :'UFR_BUFFER_OVERFLOW',
    0x06 :'UFR_MAX_ADDRESS_EXCEEDED',
    0x07 :'UFR_MAX_KEY_INDEX_EXCEEDED',
    0x08 :'UFR_NO_CARD',
    0x09 :'UFR_COMMAND_NOT_SUPPORTED',
    0x0A :'UFR_FORBIDEN_DIRECT_WRITE_IN_SECTOR_TRAILER',
    0x0B :'UFR_ADDRESSED_BLOCK_IS_NOT_SECTOR_TRAILER',
    0x0C :'UFR_WRONG_ADDRESS_MODE',
    0x0D :'UFR_WRONG_ACCESS_BITS_VALUES',
    0x0E :'UFR_AUTH_ERROR',
    0x0F :'UFR_PARAMETERS_ERROR',
    0x10 :'UFR_MAX_SIZE_EXCEEDED',

    0x70 :'UFR_WRITE_VERIFICATION_ERROR',
    0x71 :'UFR_BUFFER_SIZE_EXCEEDED',
    0x72 :'UFR_VALUE_BLOCK_INVALID',
    0x73 :'UFR_VALUE_BLOCK_ADDR_INVALID',
    0x74 :'UFR_VALUE_BLOCK_MANIPULATION_ERROR',
    0x75 :'UFR_WRONG_UI_MODE',
    0x76 :'UFR_KEYS_LOCKED',
    0x77 :'UFR_KEYS_UNLOCKED',
    0x78 :'UFR_WRONG_PASSWORD',
    0x79 :'UFR_CAN_NOT_LOCK_DEVICE',
    0x7A :'UFR_CAN_NOT_UNLOCK_DEVICE',
    0x7B :'UFR_DEVICE_EEPROM_BUSY',
    0x7C :'UFR_RTC_SET_ERROR',

    0x50 :'UFR_COMMUNICATION_BREAK',
    0x51 :'UFR_NO_MEMORY_ERROR',
    0x52 :'UFR_CAN_NOT_OPEN_READER',
    0x53 :'UFR_READER_NOT_SUPPORTED',
    0x54 :'UFR_READER_OPENING_ERROR',
    0x55 :'UFR_READER_PORT_NOT_OPENED',
    0x56 :'UFR_CANT_CLOSE_READER_PORT',

    0xA0 :'UFR_FT_STATUS_ERROR_1',
    0xA1 :'UFR_FT_STATUS_ERROR_2',
    0xA2 :'UFR_FT_STATUS_ERROR_3',
    0xA3 :'UFR_FT_STATUS_ERROR_4',
    0xA4 :'UFR_FT_STATUS_ERROR_5',
    0xA5 :'UFR_FT_STATUS_ERROR_6',
    0xA6 :'UFR_FT_STATUS_ERROR_7',
    0xA7 :'UFR_FT_STATUS_ERROR_8',
    0xA8 :'UFR_FT_STATUS_ERROR_9',

    0xFFFFFFFF :'MAX_UFR_STATUS',
}
