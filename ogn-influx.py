from ogn.client import AprsClient
from ogn.parser import parse, ParseError
from datetime import datetime
import influxdb_client
from influxdb_client.client.write_api import SYNCHRONOUS

# Init InfluxDB Python Client
token="XXXXXXXXXXXXX"
org="HOME"
bucket="ogntelemetry"
url="http://192.168.0.123:8086"
influx_client = influxdb_client.InfluxDBClient(
    url=url,
    token=token,
    org=org
)
write_api = influx_client.write_api(write_options=SYNCHRONOUS)

# Which Fields to write to INflux
aprs_status_fields=['cpu_load','free_ram','total_ram','ntp_error','rt_crystal_correction','cpu_temp','senders_visible','senders_total','rec_crystal_correction','rec_crystal_correction_fine','rec_input_noise','senders_signal','senders_messages']

def parse_status(aprsin):
    print(aprsin)
    #print(type(aprsin))

def write_influx(aprsin):
    if aprsin['aprs_type']=='status':
        if "name" in aprsin.keys():
            rxname=aprsin['name']
        else:
            rxname='notfound'

        for fieldname in aprs_status_fields:
            if fieldname in aprsin.keys():
                #print(rxname + " " + fieldname + " " + str(aprsin[fieldname]))
                p = influxdb_client.Point("receivers").tag("name",rxname).field(fieldname,aprsin[fieldname])
                write_api.write(bucket=bucket, org=org, record=p)

def process_beacon(raw_message):
    try:
        beacon = parse(raw_message)
        #print('Received {aprs_type}: {raw_message}'.format(**beacon))
        #parse_status(beacon)
        write_influx(beacon)
    except ParseError as e:
        print('Error, {}'.format(e.message))
    except NotImplementedError as e:
        print('{}: {}'.format(e, raw_message))

#aclient = AprsClient(aprs_user='N0CALL',aprs_filter='b/YBEV/YNRG/YCUN')
aclient = AprsClient(aprs_user='N0CALL',aprs_filter='b/YARA/YBEV/YBLA/YBLA2/YBSS2/YBSS3/YCTM/YHSM/YKEP/YKRY/YKUW/YLAB/YMBT/YMCF/YMGF/YNRG/YNRG1/YNRM/YRYW/YSCN/YSTW2/YSTW4/YSTW5/YSTW6/YSTW7/YSTW9/YKEP2/YTEM/YTOC/YTOC2/YWCK/YWKW')
aclient.connect()

try:
    aclient.run(callback=process_beacon, autoreconnect=True)
except KeyboardInterrupt:
    print('\nStop ogn gateway')
    aclient.disconnect()
