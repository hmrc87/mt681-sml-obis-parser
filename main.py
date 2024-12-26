import datetime
import serial
from smllib import SmlStreamReader
from prometheus_client import CollectorRegistry,Counter, Gauge, push_to_gateway
import argparse
from rich import print

def parse(skip_prometheus): 
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
    
    print(ser.name)

    # Open the connection
    ser.isOpen()
    
    stream = SmlStreamReader()
    framereceived = False
    while framereceived == False:
        byte = ser.read(20)
        stream.add(byte)
        # print the byte converted to hex
        print(byte.hex())
        sml_frame = stream.get_frame()

        if sml_frame is not None:
            obis_values = sml_frame.get_obis()
            timestamp = datetime.datetime.utcnow().strftime('%Y-%m-%dT%H:%M:%SZ')
            data = [(timestamp, obis_arr[obisvalue.obis][1], obisvalue.obis, obisvalue.value) for obisvalue in obis_values]
            print (data)
            framereceived = True
            
            if not skip_prometheus:
                insert_data(data)
 
            
def insert_data(data):

    registry = CollectorRegistry()

# Aktuelle Wirkleistung
    g = Gauge('mt681_current_power', 'aktuelle Wirkleistung', registry=registry)
    
    values = [item[3] for item in data if item[1] == 'aktuelle Wirkleistung']
    value = values[0] if values else None
    
    if value is not None:
	    print("Aktuelle WIrkleistung mt681_current_power: {value}"+ value))
        g.set(value)
        push_to_gateway('localhost:9091', job='mt681', registry=registry)
        print("pushed to prometheus")

# Zählerstand Total
    c = Counter('mt681_meter_reading_total', 'Zählerstand total', registry=registry)

    values = [item[3] for item in data if item[1] == 'Zählerstand Total']
    value = values[0] if values else None

    if value is not None:
        c._value.set(value)
        push_to_gateway('localhost:9091', job='mt681', registry=registry)
        print("pushed to prometheus")

    
    

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Process some integers.")
    parser.add_argument("--skip_prometheus", help="skip pushing to Prometheus", action="store_true")
    args = parser.parse_args()
    
    parse(args.skip_prometheus)
