import requests
import json
import time
import csv
import pandas
import smtplib
import config
from email.message import EmailMessage
from datetime import datetime



def get_data(request_url):
    print('requesting from:')
    print(request_url)
    response = requests.get(request_url)
    print(response.status_code)
    print(response.json())
    return response.json()

def send_email(subject, msg):
    try:
        server = smtplib.SMTP('smtp.gmail.com:587')
        server.ehlo()
        server.starttls()
        server.login(config.EMAIL_ADDRESS, config.PASSWORD)
        message = 'Subject:{}\n\n{}'.format(subject, msg)
        server.sendmail(config.EMAIL_ADDRESS, config.EMAIL_ADDRESS, message)
        server.quit()
        print("Success: Email sent!")
    except Exception as e:
        print("Email failed to send.")
        print(e)

def get_csv_file(timestamp, filename='printerdata_masterfileR1B'):
    fullFileName = ""
    fullFileName += str(timestamp)
    fullFileName += ('.csv')
    f1 = open(fullFileName, 'w', newline='')
    return f1 

def close_csv_file(fileHandle):
    fileHandle.flush()
    fileHandle.close()

def print_headers(f1):
        HEADERS = [
        'datetime_cleaned',
        'datetime_finished',
        'datetime_started',
        'name',
        'progress',
        # 'reprint_original_uuid',
        'result',
        'source',
        # 'source_application',
        'source_user',
        'state',
        'time_elapsed',
        'time_total',
        # 'uuid',
        'bed-pre_heat-active',
        'bed-temperature-current',
        'bed-temperature-target',
        # 'extruder-1-active-material-GUID',
        # 'extruder-1-active-material-guid',
        'extruder-1-feeder-acceleration',
        'extruder-1-feeder-jerk',
        'extruder-1-feeder-max_speed',
        # 'extruder-1-hotend-id',
        'extruder-1-hotend-offset-state',
        'extruder-1-hotend-offset-x',
        'extruder-1-hotend-offset-y',
        'extruder-1-hotend-offset-z',
        # 'extruder-1-hotend-serial',
        # 'extruder-1-hotend-statistics-last_material_guid',
        'extruder-1-hotend-statistics-material_extruded',
        'extruder-1-hotend-statistics-max_temperature_exposed',
        'extruder-1-hotend-statistics-time_spent_hot',
        'extruder-1-hotend-current-temperature',
        'extruder-1-hotend-target-temperature',
        # 'extruder-2-hotend-active_material_GUID',
        # 'extruder-2-hotend-active_material_guid',
        'extruder-2-hotend-active_material-length_remaining',
        'extruder-2-hotend-feeder-accelaration',
        'extruder-2-hotend-feeder-jerk',
        'extruder-2-hotend-feeder-max_speed',
        # 'extruder-2-hotend-id',
        # 'extruder-2-hotend-offset-state',
        'extruder-2-hotend-offset-x',
        'extruder-2-hotend-offset-y',
        'extruder-2-hotend-offset-z',
        # 'extruder-2-hotend-serial',
        # 'extruder-2-hotend-statistics-last_material_guid',
        'extruder-2-hotend-statistics-material_extruded',
        'extruder-2-hotend-statistics-max_temperature_exposed',
        'extruder-2-hotend-statistics-time_spent_hot',
        'extruder-2-hotend-current-temperature',
        'extruder-2-hotend-target-temperature',
        'heads-fan',
        'heads-jerk-x',
        'heads-jerk-y',
        'heads-jerk-z',
        'heads-max_speed-x',
        'heads-max_speed-y',
        'heads-max_speed-z',
        'heads-position-x',
        'heads-position-y',
        'heads-position-z',
        'led-brightness',
        'led-hue',
        'led-saturation',
        'network-ethernet-connected',
        'network-ethernet-enabled',
        'network-wifi-connected',
        'network-wifi-enabled',
        'network-wifi-mode',
        'network-wifi-ssid',
        'status',
        # 'historic_data_datetime_cleaned',
        # 'historic_data_datetime_finished',
        # 'historic_data_datetime_started',
        # 'historic_data_name',
        # 'historic_data_reprint_original_uuid',
        # 'historic_data_result',
        # 'historic_data_source',
        # 'historic_data_time_elapsed',
        # 'historic_data_time_estimated',
        # 'historic_data_time_total',
        # 'historic_data_uuid',
        ]

        writer = csv.writer(f1)
        writer.writerow(HEADERS)
        f1.flush()



if __name__ == "__main__":
    urls = ['http://10.43.212.102/api/v1/print_job','http://10.43.212.102/api/v1/printer','http://10.43.212.102/api/v1/history/print_jobs']
    REST_API_URL = 'https://api.powerbi.com/beta/bc876b21-f134-4c12-a265-8ed26b7f0f3b/datasets/19c4f461-2a1e-4af9-a3cd-c02a45a68f58/rows?key=ikJ3S87x7IN%2BpYFnfNCrafmsG%2BPhw7pCNog4irkvgbPefjgjoWUUqlInTrzrUOi2hVEfdE8nNZleFpBIVLtShg%3D%3D'

    start_time = time.time()
    end_time = time.time()

    CSV_data = {}
    #open file
    # loop to get data from the machine
    row_count = 0
    f1 = None
    #while end_time-start_time < 43300:
    while True:
        if f1 is None:
            f1 = get_csv_file(end_time)
            writer = csv.writer(f1)
            print_headers(f1)
        if row_count == 3000:
            f1.flush()
            f1.close()
            f1 = get_csv_file(start_time)
            writer = csv.writer(f1)
            print_headers(f1)
            row_count = 0
        row_count += 1

        data_raw = []
        for i in range(1):
            json_data = get_data(urls[0])
            #print(json_data,type(json_data))
            
            url0_data = [
                json_data.get('datetime_cleaned','not here'),
                json_data.get('datetime_finished','not here'),
                json_data.get('datetime_started','not here'),
                json_data.get('name','not here'),
                json_data.get('progress','not here'),
                # json_data.get('reprint_original_uuid','not here'),
                json_data.get('result', 'not here'),
                json_data.get('source','not here'),
                # json_data.get('source_appliction','not here'),
                json_data.get('source_user','not here'),
                json_data.get('state','not here'),
                json_data.get('time_elapsed', 'not here'),
                json_data.get('time_total','not here'),
                # json_data.get('uuid','not here')
            ]
            #add code
            CSV_data['datetime_cleaned'] = json_data.get('datetime_cleaned')
            CSV_data['datetime_finished'] = json_data.get('datetime_finished')
            CSV_data['datetime_started'] = json_data.get('datetime_started')
            CSV_data['name'] = json_data.get('name')
            CSV_data['progress'] = json_data.get('progress')
            # CSV_data['reprint_original_uuid'] = json_data.get('reprint_original_uuid')
            CSV_data['result'] = json_data.get('result')
            CSV_data['source'] = json_data.get('source')
            # CSV_data['source_application'] = json_data.get('source_appliction')
            CSV_data['source_user'] = json_data.get('source_user')
            CSV_data['state'] = json_data.get('state')
            CSV_data['time_elapsed'] = json_data.get('time_elapsed')
            CSV_data['time_total'] =  json_data.get('time_total')
            # CSV_data['uuid'] = json_data.get('uuid')

            if CSV_data['progress'] == 0.10:
                send_email("Print Job Progress ALERT!","Your Printer has approximately completed 10 percent of current print job, please check to see if everything is running smoothly.")
            if CSV_data['progress'] == 0.25:
                send_email("Print Job Progress ALERT!","Your Printer has approximately completed 25 percent of current print job, please check to see if everything is running smoothly.")
            if CSV_data['progress'] == 0.50:
                send_email("Print Job Progress ALERT!","Your Printer has approximately completed 50 percent of current print job, please check to see if everything is running smoothly.")
            if CSV_data['progress'] == 0.75:
                send_email("Print Job Progress ALERT!","Your Printer has approximately completed 75 percent of current print job, please check to see if everything is running smoothly.")
            if CSV_data['progress'] == 0.100:
                send_email("Print Job Progress ALERT!","Your Printer has approximately completed 100 percent of current print job, please check to see if print job was successful.")

            data_raw.append(url0_data)
            print('Raw data -', data_raw)

            json_data = get_data(urls[1])
            url1_data = [
                json_data['bed']['pre_heat']['active'],
                json_data['bed']['temperature']['current'], 
                json_data['bed']['temperature']['target'], 
                # json_data['heads'][0]['extruders'][0]['active_material']['GUID'],
                # json_data['heads'][0]['extruders'][0]['active_material']['guid'],
                json_data['heads'][0]['extruders'][0]['feeder']['acceleration'],
                json_data['heads'][0]['extruders'][0]['feeder']['jerk'],
                json_data['heads'][0]['extruders'][0]['feeder']['max_speed'],
                # json_data['heads'][0]['extruders'][0]['hotend']['id'],
                json_data['heads'][0]['extruders'][0]['hotend']['offset']['state'],
                json_data['heads'][0]['extruders'][0]['hotend']['offset']['x'],
                json_data['heads'][0]['extruders'][0]['hotend']['offset']['y'],
                json_data['heads'][0]['extruders'][0]['hotend']['offset']['z'],
                # json_data['heads'][0]['extruders'][0]['hotend']['serial'],
                # json_data['heads'][0]['extruders'][0]['hotend']['statistics']['last_material_guid'],
                json_data['heads'][0]['extruders'][0]['hotend']['statistics']['material_extruded'],
                json_data['heads'][0]['extruders'][0]['hotend']['statistics']['max_temperature_exposed'],
                json_data['heads'][0]['extruders'][0]['hotend']['statistics']['time_spent_hot'],
                json_data['heads'][0]['extruders'][0]['hotend']['temperature']['current'],
                json_data['heads'][0]['extruders'][0]['hotend']['temperature']['target'],
                # json_data['heads'][0]['extruders'][1]['active_material']['GUID'],
                # json_data['heads'][0]['extruders'][1]['active_material']['guid'],
                json_data['heads'][0]['extruders'][1]['active_material']['length_remaining'],
                json_data['heads'][0]['extruders'][1]['feeder']['acceleration'],
                json_data['heads'][0]['extruders'][1]['feeder']['jerk'],
                json_data['heads'][0]['extruders'][1]['feeder']['max_speed'],
                # json_data['heads'][0]['extruders'][1]['hotend']['id'],
                # json_data['heads'][0]['extruders'][1]['hotend']['offset']['state'],
                json_data['heads'][0]['extruders'][1]['hotend']['offset']['x'],
                json_data['heads'][0]['extruders'][1]['hotend']['offset']['y'],
                json_data['heads'][0]['extruders'][1]['hotend']['offset']['z'],
                json_data['heads'][0]['extruders'][1]['hotend']['serial'],
                # json_data['heads'][0]['extruders'][1]['hotend']['statistics']['last_material_guid'],
                # json_data['heads'][0]['extruders'][1]['hotend']['statistics']['material_extruded'],
                json_data['heads'][0]['extruders'][1]['hotend']['statistics']['max_temperature_exposed'],
                json_data['heads'][0]['extruders'][1]['hotend']['statistics']['time_spent_hot'],
                json_data['heads'][0]['extruders'][1]['hotend']['temperature']['current'],
                json_data['heads'][0]['extruders'][1]['hotend']['temperature']['target'],
                json_data['heads'][0]['fan'],
                json_data['heads'][0]['jerk']['x'],
                json_data['heads'][0]['jerk']['y'],
                json_data['heads'][0]['jerk']['z'],
                json_data['heads'][0]['max_speed']['x'],
                json_data['heads'][0]['max_speed']['y'],
                json_data['heads'][0]['max_speed']['z'],
                json_data['heads'][0]['position']['x'],
                json_data['heads'][0]['position']['y'],
                json_data['heads'][0]['position']['z'],
                json_data['led']['brightness'],
                json_data['led']['hue'],
                json_data['led']['saturation'],
                json_data['network']['ethernet']['connected'],
                json_data['network']['ethernet']['enabled'],
                json_data['network']['wifi']['connected'],
                json_data['network']['wifi']['enabled'],
                json_data['network']['wifi']['mode'],
                json_data['network']['wifi']['ssid'],
                json_data['status']
            ]
            #add code
            CSV_data['bed-pre_heat-active'] = json_data['bed']['pre_heat']['active']
            CSV_data['bed-temperature-current'] = json_data['bed']['temperature']['current']
            CSV_data['bed-temperature-target'] = json_data['bed']['temperature']['target']
            # CSV_data['extruder-1-active-material-GUID'] = json_data['heads'][0]['extruders'][0]['active_material']['GUID']
            # CSV_data['extruder-1-active-material-guid'] = json_data['heads'][0]['extruders'][0]['active_material']['guid']
            CSV_data['extruder-1-feeder-acceleration'] = json_data['heads'][0]['extruders'][0]['feeder']['acceleration']
            CSV_data['extruder-1-feeder-jerk'] = json_data['heads'][0]['extruders'][0]['feeder']['jerk']
            CSV_data['extruder-1-feeder-max_speed'] = json_data['heads'][0]['extruders'][0]['feeder']['max_speed']
            # CSV_data['extruder-1-hotend-id'] = json_data['heads'][0]['extruders'][0]['hotend']['id']
            CSV_data['extruder-1-hotend-offset-state'] = json_data['heads'][0]['extruders'][0]['hotend']['offset']['state']
            CSV_data['extruder-1-hotend-offset-x'] = json_data['heads'][0]['extruders'][0]['hotend']['offset']['x']
            CSV_data['extruder-1-hotend-offset-y'] = json_data['heads'][0]['extruders'][0]['hotend']['offset']['y']
            CSV_data['extruder-1-hotend-offset-z'] = json_data['heads'][0]['extruders'][0]['hotend']['offset']['z']
            # CSV_data['extruder-1-hotend-serial'] = json_data['heads'][0]['extruders'][0]['hotend']['serial']
            # CSV_data['extruder-1-hotend-statistics-last_material_guid'] = json_data['heads'][0]['extruders'][0]['hotend']['statistics']['last_material_guid']
            CSV_data['extruder-1-hotend-statistics-material_extruded'] = json_data['heads'][0]['extruders'][0]['hotend']['statistics']['material_extruded']
            CSV_data['extruder-1-hotend-statistics-max_temperature_exposed'] = json_data['heads'][0]['extruders'][0]['hotend']['statistics']['max_temperature_exposed']
            CSV_data['extruder-1-hotend-statistics-time_spent_hot'] = json_data['heads'][0]['extruders'][0]['hotend']['statistics']['time_spent_hot']
            CSV_data['extruder-1-hotend-current-temperature'] = json_data['heads'][0]['extruders'][0]['hotend']['temperature']['current']
            CSV_data['extruder-1-hotend-target-temperature'] = json_data['heads'][0]['extruders'][0]['hotend']['temperature']['target']
            # CSV_data['extruder-2-hotend-active_material_GUID'] = json_data['heads'][0]['extruders'][1]['active_material']['GUID']
            # CSV_data['extruder-2-hotend-active_material_guid'] = json_data['heads'][0]['extruders'][1]['active_material']['guid']
            CSV_data['extruder-2-hotend-active_material-length_remaining'] = json_data['heads'][0]['extruders'][1]['active_material']['length_remaining']
            CSV_data['extruder-2-hotend-feeder-acceleration'] = json_data['heads'][0]['extruders'][1]['feeder']['acceleration']
            CSV_data['extruder-2-hotend-feeder-jerk'] = json_data['heads'][0]['extruders'][1]['feeder']['jerk']
            CSV_data['extruder-2-hotend-feeder-max_speed'] = json_data['heads'][0]['extruders'][1]['feeder']['max_speed']
            # CSV_data['extruder-2-hotend-id'] = json_data['heads'][0]['extruders'][1]['hotend']['id']
            # CSV_data['extruder-2-hotend-offset-state'] = json_data['heads'][0]['extruders'][1]['hotend']['offset']['state']
            CSV_data['extruder-2-hotend-offset-x'] = json_data['heads'][0]['extruders'][1]['hotend']['offset']['x']
            CSV_data['extruder-2-hotend-offset-y'] = json_data['heads'][0]['extruders'][1]['hotend']['offset']['y']
            CSV_data['extruder-2-hotend-offset-z'] = json_data['heads'][0]['extruders'][1]['hotend']['offset']['z']
            # CSV_data['extruder-2-hotend-serial'] = json_data['heads'][0]['extruders'][1]['hotend']['serial']
            # CSV_data['extruder-2-hotend-statistics-last_material_guid'] = json_data['heads'][0]['extruders'][1]['hotend']['statistics']['last_material_guid']
            CSV_data['extruder-2-hotend-statistics-material_extruded'] = json_data['heads'][0]['extruders'][1]['hotend']['statistics']['material_extruded']
            CSV_data['extruder-2-hotend-statistics-max_temperature_exposed'] = json_data['heads'][0]['extruders'][1]['hotend']['statistics']['max_temperature_exposed']
            CSV_data['extruder-2-hotend-statistics-time_spent_hot'] = json_data['heads'][0]['extruders'][1]['hotend']['statistics']['time_spent_hot']
            CSV_data['extruder-2-hotend-current-temperature'] = json_data['heads'][0]['extruders'][1]['hotend']['temperature']['current']
            CSV_data['extruder-2-hotend-target-temperature'] = json_data['heads'][0]['extruders'][1]['hotend']['temperature']['target']
            CSV_data['heads-fan'] = json_data['heads'][0]['fan']
            CSV_data['heads-jerk-x'] = json_data['heads'][0]['jerk']['x']
            CSV_data['heads-jerk-y'] = json_data['heads'][0]['jerk']['y']
            CSV_data['heads-jerk-z'] = json_data['heads'][0]['jerk']['z']
            CSV_data['heads-max_speed-x'] = json_data['heads'][0]['max_speed']['x']
            CSV_data['heads-max_speed-y'] = json_data['heads'][0]['max_speed']['y']
            CSV_data['heads-max_speed-z'] = json_data['heads'][0]['max_speed']['z']
            CSV_data['heads-position-x'] = json_data['heads'][0]['position']['x']
            CSV_data['heads-position-y'] = json_data['heads'][0]['position']['y']
            CSV_data['heads-position-z'] = json_data['heads'][0]['position']['z']
            CSV_data['led-brightness'] = json_data['led']['brightness']
            CSV_data['led-hue'] = json_data['led']['hue']
            CSV_data['led-saturation'] = json_data['led']['saturation']
            CSV_data['network-ethernet-connected'] = json_data['network']['ethernet']['connected']
            CSV_data['network-ethernet-enabled'] = json_data['network']['ethernet']['enabled']
            CSV_data['network-wifi-connected'] = json_data['network']['wifi']['connected']
            CSV_data['network-wifi-enabled'] = json_data['network']['wifi']['enabled']
            CSV_data['network-wifi-mode'] = json_data['network']['wifi']['mode']
            CSV_data['network-wifi-ssid'] = json_data['network']['wifi']['ssid']
            CSV_data['status'] = json_data['status']
            
            #add the if block to send emails here
            if CSV_data['bed-temperature-current'] == 60:
                send_email("Bed Temperature Green ALERT! ","Printer is at recommended bed temperture, it has a 90 percent success rate. Please Check to see if you would like to continue print")
            if CSV_data['bed-temperature-current'] == 75:
                send_email("Bed Temperature Green ALERT! ","Printer is at recommended bed temperture, it has a 98 percent success rate. Please Check to see if you would like to continue print")
            if CSV_data['bed-temperature-current'] == 90:
                send_email("Bed Temperature Green ALERT! ","Printer is at recommended bed temperture, it has a 90 percent success rate. Please Check to see if you would like to continue print") 
            if CSV_data['bed-temperature-current'] == 50:
                send_email("Bed Temperature Yellow ALERT! ","Printer is not at recommended bed temperture, it has a 70 percent success rate. Please Check to see if you would like to continue print")
            if CSV_data['bed-temperature-current'] == 55:
                send_email("Bed Temperature Yellow ALERT! ","Printer is not at recommended bed temperture, it has a 80 percent success rate. Please Check to see if you would like to continue print")
            if CSV_data['bed-temperature-current'] == 59:
                send_email("Bed Temperature Yellow ALERT! ","Printer is not at recommended bed temperture, it has a 89 percent success rate. Please Check to see if you would like to continue print")                  
            if CSV_data['bed-temperature-current'] == 100:
                send_email("Bed Temperature Yellow ALERT! ","Printer is not at recommended bed temperture, it has a 70 percent success rate. Please Check to see if you would like to continue print")
            if CSV_data['bed-temperature-current'] == 95:
                send_email("Bed Temperature Yellow ALERT! ","Printer is not at recommended bed temperture, it has a 80 percent success rate. Please Check to see if you would like to continue print")
            if CSV_data['bed-temperature-current'] == 91:
                send_email("Bed Temperature Yellow ALERT! ","Printer is not at recommended bed temperture, it has a 89 percent success rate. Please Check to see if you would like to continue print")
            if CSV_data['bed-temperature-current'] == 49:
                send_email("Bed Temperature RED ALERT! ","Printer is far off fromm recommended bed temperture, it has a 69 percent success rate. Please Check to see if you would like to continue print")
            if CSV_data['bed-temperature-current'] == 45:
                send_email("Bed Temperature RED ALERT! ","Printer is far off from recommended bed temperture, it has a 65 percent success rate. Please Check to see if you would like to continue print")
            if CSV_data['bed-temperature-current'] == 40:
                send_email("Bed Temperature RED ALERT! ","Printer is far off from recommended bed temperture, it has a 60 percent success rate. Please Check to see if you would like to continue print")      
            if CSV_data['bed-temperature-current'] == 101:
                send_email("Bed Temperature RED ALERT! ","Printer is far off fromm recommended bed temperture, it has a 69 percent success rate. Please Check to see if you would like to continue print")
            if CSV_data['bed-temperature-current'] == 105:
                send_email("Bed Temperature RED ALERT! ","Printer is far off from recommended bed temperture, it has a 65 percent success rate. Please Check to see if you would like to continue print")
            if CSV_data['bed-temperature-current'] == 110:
                send_email("Bed Temperature RED ALERT! ","Printer is far off from recommended bed temperture, it has a 60 percent success rate. Please Check to see if you would like to continue print") 
            if CSV_data['extruder-1-hotend-current-temperature'] == 230:
                send_email("Extruder 1 Green ALERT!","Printer is at recommended extruder temperture it has a 90 percent success rate. Please Check to see if you would like to continue print")  
            if CSV_data['extruder-1-hotend-current-temperature'] == 245:
                send_email("Extruder 1 Green ALERT!","Printer is at recommended extruder temperture it has a 98 percent success rate. Please Check to see if you would like to continue print")
            if CSV_data['extruder-1-hotend-current-temperature'] == 260:
                send_email("Extruder 1 Green ALERT!","Printer is at recommended extruder temperture it has a 90 percent success rate. Please Check to see if you would like to continue print")                      
            if CSV_data['extruder-1-hotend-current-temperature'] == 229:
                send_email("Extruder 1 Yellow ALERT!","Printer is not at recommended extruder temperture it has a 89 percent success rate. Please Check to see if you would like to continue print")  
            if CSV_data['extruder-1-hotend-current-temperature'] == 225:
                send_email("Extruder 1 Yellow ALERT!","Printer is not at recommended extruder temperture it has a 80 percent success rate. Please Check to see if you would like to continue print")
            if CSV_data['extruder-1-hotend-current-temperature'] == 220:
                send_email("Extruder 1 Yellow ALERT!","Printer is not at recommended extruder temperture it has a 70 percent success rate. Please Check to see if you would like to continue print")  
            if CSV_data['extruder-1-hotend-current-temperature'] == 261:
                send_email("Extruder 1 Yellow ALERT!","Printer is not at recommended extruder temperture it has a 89 percent success rate. Please Check to see if you would like to continue print")  
            if CSV_data['extruder-1-hotend-current-temperature'] == 265:
                send_email("Extruder 1 Yellow ALERT!","Printer is not at recommended extruder temperture it has a 80 percent success rate. Please Check to see if you would like to continue print")
            if CSV_data['extruder-1-hotend-current-temperature'] == 270:
                send_email("Extruder 1 Yellow ALERT!","Printer is not at recommended extruder temperture it has a 70 percent success rate. Please Check to see if you would like to continue print")  
            if CSV_data['extruder-1-hotend-current-temperature'] == 219:
                send_email("Extruder 1 Red ALERT!","Printer is far from the recommended extruder temperture it has a 69 percent success rate. Please Check to see if you would like to continue print")  
            if CSV_data['extruder-1-hotend-current-temperature'] == 215:
                send_email("Extruder 1 Red ALERT!","Printer is far from the recommended extruder temperture it has a 65 percent success rate. Please Check to see if you would like to continue print")
            if CSV_data['extruder-1-hotend-current-temperature'] == 210:
                send_email("Extruder 1 Red ALERT!","Printer is far from the recommended extruder temperture it has a 60 percent success rate. Please Check to see if you would like to continue print")  
            if CSV_data['extruder-1-hotend-current-temperature'] == 271:
                send_email("Extruder 1 Red ALERT!","Printer is far from the recommended extruder temperture it has a 69 percent success rate. Please Check to see if you would like to continue print")  
            if CSV_data['extruder-1-hotend-current-temperature'] == 275:
                send_email("Extruder 1 Red ALERT!","Printer is far from the recommended extruder temperture it has a 65 percent success rate. Please Check to see if you would like to continue print")
            if CSV_data['extruder-1-hotend-current-temperature'] == 280:
                send_email("Extruder 1 Red ALERT!","Printer is far from the recommended extruder temperture it has a 60 percent success rate. Please Check to see if you would like to continue print")  
            if CSV_data['extruder-2-hotend-current-temperature'] == 215:
                send_email("Extruder 2 Green ALERT!","Printer is at recommended extruder temperture it has a 90 percent success rate. Please Check to see if you would like to continue print") 
            if CSV_data['extruder-2-hotend-current-temperature'] == 223:
                send_email("Extruder 2 Green ALERT!","Printer is at recommended extruder temperture it has a 98 percent success rate. Please Check to see if you would like to continue print")
            if CSV_data['extruder-2-hotend-current-temperature'] == 230:
                send_email("Extruder 2 Green ALERT!","Printer is at recommended extruder temperture it has a 90 percent success rate. Please Check to see if you would like to continue print")
            if CSV_data['extruder-2-hotend-current-temperature'] == 214:
                send_email("Extruder 2 Yellow ALERT!","Printer is not at recommended extruder temperture it has a 89 percent success rate. Please Check to see if you would like to continue print")  
            if CSV_data['extruder-2-hotend-current-temperature'] == 210:
                send_email("Extruder 2 Yellow ALERT!","Printer is not at recommended extruder temperture it has a 80 percent success rate. Please Check to see if you would like to continue print")
            if CSV_data['extruder-2-hotend-current-temperature'] == 205:
                send_email("Extruder 2 Yellow ALERT!","Printer is not at recommended extruder temperture it has a 70 percent success rate. Please Check to see if you would like to continue print")
            if CSV_data['extruder-2-hotend-current-temperature'] == 231:
                send_email("Extruder 2 Yellow ALERT!","Printer is not at recommended extruder temperture it has a 89 percent success rate. Please Check to see if you would like to continue print")  
            if CSV_data['extruder-2-hotend-current-temperature'] == 236:
                send_email("Extruder 2 Yellow ALERT!","Printer is not at recommended extruder temperture it has a 80 percent success rate. Please Check to see if you would like to continue print")
            if CSV_data['extruder-2-hotend-current-temperature'] == 241:
                send_email("Extruder 2 Yellow ALERT!","Printer is not at recommended extruder temperture it has a 70 percent success rate. Please Check to see if you would like to continue print") 
            if CSV_data['extruder-2-hotend-current-temperature'] == 204:
                send_email("Extruder 2 Red ALERT!","Printer is far off from the recommended extruder temperture it has a 69 percent success rate. Please Check to see if you would like to continue print")  
            if CSV_data['extruder-2-hotend-current-temperature'] == 199:
                send_email("Extruder 2 Red ALERT!","Printer is far off from the recommended extruder temperture it has a 65 percent success rate. Please Check to see if you would like to continue print")
            if CSV_data['extruder-2-hotend-current-temperature'] == 196:
                send_email("Extruder 2 Red ALERT!","Printer is far off from the recommended extruder temperture it has a 60 percent success rate. Please Check to see if you would like to continue print")
            if CSV_data['extruder-2-hotend-current-temperature'] == 242:
                send_email("Extruder 2 Red ALERT!","Printer is far off from the recommended extruder temperture it has a 69 percent success rate. Please Check to see if you would like to continue print")  
            if CSV_data['extruder-2-hotend-current-temperature'] == 247:
                send_email("Extruder 2 Red ALERT!","Printer is far off from the recommended extruder temperture it has a 65 percent success rate. Please Check to see if you would like to continue print")
            if CSV_data['extruder-2-hotend-current-temperature'] == 251:
                send_email("Extruder 2 Red ALERT!","Printer is far off from the recommended extruder temperture it has a 60 percent success rate. Please Check to see if you would like to continue print")    

            data_raw.append(url1_data)
            print('Raw data -', data_raw)
            

            # json_data = get_data(urls[2])
            # url2_data = [
            #     #  json_data[0]['datetime_cleaned'],
            #     #  json_data[0]['datetime_finished'],
            #     #  json_data[0]['datetime_started'],
            #      json_data[0]['name'],
            #      json_data[0]['reprint_original_uuid'],
            #      json_data[0]['result'],
            #      json_data[0]['source'],
            #      json_data[0]['time_elapsed'],
            #      json_data[0]['time_estimated'],
            #      json_data[0]['time_total'],
            #      json_data[0]['uuid']
            #  ]

            # #add code
            # # CSV_data['historic_data_datetime_cleaned'] = json_data[0]['datetime_cleaned']
            # # CSV_data['historic_data_datetime_finished'] = json_data[0]['datetime_finished']
            # # CSV_data['historic_data_datetime_started'] =  json_data[0]['datetime_started']
            # CSV_data['historic_data_name'] = json_data[0]['name']
            # CSV_data['historic_data_reprint_original_uuid'] = json_data[0]['reprint_original_uuid']
            # CSV_data['historic_data_result'] =  json_data[0]['result']
            # CSV_data['historic_data_source'] = json_data[0]['source']
            # CSV_data['historic_data_time_elapsed'] = json_data[0]['time_elapsed']
            # CSV_data['historic_data_time_estimated'] = json_data[0]['time_estimated']
            # CSV_data['historic_data_time_total'] = json_data[0]['time_total']
            # CSV_data['historic_data_uuid'] =  json_data[0]['uuid']
            

            # data_raw.append(url2_data)
            # print('Raw data -', data_raw)

        # datetime_cleaned = url0_data[0]
        # print(datetime_cleaned)
        # datetime_object = datetime.strptime(datetime_cleaned, "%Y-%m-%dT%H:%M:%S") if datetime_cleaned else None
        # url0_data[0] = datetime_object
        # datetime_finished = url0_data[1]
        # datetime_object = datetime.strptime(datetime_finished, "%Y-%m-%dT%H:%M:%S") if datetime_finished else None
        # url0_data[1] = datetime_object
        # print(url0_data)
        # datetime_started = url0_data[0]
        # print(datetime_started)
        # datetime_object = datetime.strptime(datetime_started, "%Y-%m-%dT%H:%M:%S") if datetime_started else None
        # url0_data[2] = datetime_object
        # datetime_cleaned  = url2_data[0]
        # datetime_object = datetime.strptime(datetime_cleaned, "%Y-%m-%dT%H:%M:%S") if datetime_cleaned else None
        # url2_data[0] = datetime_object
        # datetime_finished = url2_data[1]
        # datetime_object = datetime.strptime(datetime_finished, "%Y-%m-%dT%H:%M:%S") if datetime_finished else None
        # url2_data[1] = datetime_object
        # datetime_started = url2_data[2]
        # datetime_object = datetime.strptime(datetime_started, "%Y-%m-%dT%H:%M:%S") if datetime_started else None
        # url2_data[2] = datetime_object


        # this line will tell you the data type of the datetime object (string)
        print(type(url0_data[0]))

        end_time = time.time()
        
        '''
        print("start")
        print(type(url0_data),url0_data)
        print(type(url1_data),url1_data)
        print("end")
        '''
        # combining data from multiple lists into one list
        # all_data = url0_data.extend(url1_data)
        all_data = []
        all_data.extend(url0_data)
        all_data.extend(url1_data)
        # all_data.extend(url2_data)
        # print("+++++++++++++++++")
        # print("all_data length: "+str(len(all_data)))
        #i = url0_data.extend(url1_data)
        #print(i)
        #print("prd",inter)
        #all_data = inter
        #print("debugging",all_data)
        

         # stop here 
        
        data_df = pandas.DataFrame(CSV_data,index=[0])
        json_data = bytes(data_df.to_json(orient='records'), encoding='utf-8')
        print('JSON dataset', json_data)
        print("+++++++++++++++++++++++")
        print("all_data length:"+str(len(all_data)))


        # Post the data on the Power BI API

        json_data_CSV = json.dumps(CSV_data)
        print("DEBUG ?????")
        print(json_data_CSV)
        req = requests.post(urls[0], json_data_CSV)
        req = requests.post(urls[1], json_data_CSV)
        req = requests.post(urls[2], json_data_CSV)
        req = requests.post(REST_API_URL,json_data_CSV)
        print(all_data)
        print("******************************")
        # all_data.extend()
        print(type(f1))
        csv.writer(f1).writerow(all_data)
        print('Data Posted in CSV')
        print('Data Posted in Power BI API')