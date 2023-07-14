import serial
from smllib import SmlStreamReader

def parse(): 
    obis_arr = {
        '0100000000FF': ['1-0:0.0.0*255', 'Seriennummer'],
        '0100010700FF': ['1-0:1.7.0*255', 'Momentane Wirkleistung Bezug'],
        '0100020700FF': ['1-0:2.7.0*255', 'Momentane Wirkleistung Lieferung'],
        '0100010801FF': ['1-0:1.8.1*255', 'Wirk-Energie Tarif 1 Bezug'],
        '0100020801ff': ['1-0:2.8.1*255', 'Wirk-Energie Tarif 1 Lieferung'],
        '0100010802FF': ['1-0:1.8.2*255', 'Wirk-Energie Tarif 2 Bezug'],
        '0100020802ff': ['1-0:2.8.2*255', 'Wirk-Energie Tarif 2 Lieferung'],
        '0100010803FF': ['1-0:1.8.3*255', 'Wirk-Energie Tarif 3 Bezug'],
        '0100020803FF': ['1-0:2.8.3*255', 'Wirk-Energie Tarif 3 Lieferung'],
        '8181C78203FF': ['129-129:199.130.3*255', 'Hersteller-ID'],
        '8181C78205FF': ['129-129:199.130.5*255', 'Public-Key'],
        '01000F0700FF': ['1-0:15.7.0*255', 'Active Power'],
        '0100010800FF': ['1-0:1.8.0*255', 'Wirkarbeit Bezug Total: Zaehlerstand'],
        '0100000009FF': ['1-0:0.0.9*255', 'Geraeteeinzelidentifikation'],
        '00006001FFFF': ['0-0:60.1.255*255', 'Fabriknummer'],
        '0100100700ff': ['1-0:16.7.0*255', 'aktuelle Wirkleistung'],
        '0100000009ff': ['1-0:0.0.9*255', 'Geräteeinzelidentifikation'],
        '0100010800ff': ['1-0:1.8.0*255', 'Zählerstand Total'],
        '0100010801ff': ['1-0:1.8.1*255', 'Zählerstand Tarif 1'],
        '0100010802ff': ['1-0:1.8.2*255', 'Zählerstand Tarif 2'],
        '0100020800ff': ['1-0:2.8.0*255', 'Wirkenergie Total'],
    }
    
    ser = serial.Serial(
        port='/dev/ttyUSB0',
        baudrate=9600,  
        parity=serial.PARITY_NONE,
        stopbits=serial.STOPBITS_ONE,
        bytesize=serial.EIGHTBITS
    )
    
    
    # Open the connection
    ser.isOpen()

    stream = SmlStreamReader()
    while True:
        byte = ser.read()
        stream.add(byte)
        sml_frame = stream.get_frame()
      
 
        if sml_frame is not None:
          
            obis_values = sml_frame.get_obis()
      
            print([ (obis_arr[obisvalue.obis][1], obisvalue.obis, obisvalue.value) for obisvalue in obis_values])

           # parsed_msgs = sml_frame.parse_frame()
           # for msg in parsed_msgs:
                # check if message_body is SmlGetListResponse
                #if msg.message_body.__class__.__name__ == 'SmlGetListResponse':
               #     print(msg.message_body.val_list)
                 #   print(msg.message_body.format_msg())
         


if __name__ == "__main__":
    parse()
