import json
import datetime as dt
import urllib
import pickle
import os
import time

# NOTE 

# There are 2 folders which go along with this script which contain the level
# and rainfall data downloaded. Care should be taken not to delete these folders 
# and if modifications need to be made to the files within the folders it is
# highly recomended that a backup of the folder is made. Once the whold system 
# is set up to run continuously a zipped daily backup module should be written
# to keep a set length of backups in case of accidental or deliberate deletion
# or coruption of the data files. It may also be worth developing a script that 
# removes and archives data nolonger used by the model to reduce the backup file 
# sizes.

def create(folder, gauge_id):
    """
    Generates a new ".pkl" file containing an empty dictionary. If the specified 
    file path exists already it will not delete and create a new empty one and 
    instead prints an error.
    """
    
    p = folder + "/" + str(gauge_id) + ".pkl"
    
    if os.path.isfile(p) == False:
        record = {}
        f = open(p,"wb")
        pickle.dump(record,f, protocol=-1)
        f.close()
        print("File Created Succesfully")
    else:
        print("Error: File Already Exists - Manual Delete Required")
    
    return


def sepa_rainfall(gauge_id=115343):
    
    """
    Reads the latest SEPA rainfall records from the website and updates the
    .pkl dictionary record file for a given sepa rainfall gauge id. The output
    is timestamped by utc time and the rainfall for any given timestamp occurs
    in the hour before the given timestamp.
    """

    record_file = "sepa_rain_gauge/" + str(gauge_id) + ".pkl"
    url = "https://apps.sepa.org.uk/rainfall/api/Hourly/" + str(gauge_id) + "?all=true"
        
    response = urllib.request.urlopen(url)
    
    j_dict = json.loads(response.read().decode())
    
    record = pickle.load(open(record_file, "rb"))
    
    for i in j_dict:
        record.update({dt.datetime.strptime(i['Timestamp'], '%d/%m/%Y %H:%M:%S'):float(i['Value'])})
    
    print("SEPA_RAIN", gauge_id, len(record), max(record), min(record))
            
    f = open(record_file,"wb")
    pickle.dump(record,f, protocol=-1)
    f.close()
    
    return


def sepa_level(gauge_id):
    """
    Reads the latest SEPA level records from the website and updates the .pkl 
    dictionary record file for a given sepa level gauge id. The output is 
    timestamped by utc time.
    """
    
    record_file = "sepa_level_gauge/" + str(gauge_id) + ".pkl"
    url = "http://apps.sepa.org.uk/database/riverlevels/" + str(gauge_id) + "-SG.csv"
    
    response = urllib.request.urlopen(url).read().decode().split('\n')[7:-1]
    
    record = pickle.load(open(record_file, "rb"))
    
    for line in response:
        line = line.split(',')
        record.update({dt.datetime.strptime(line[0], '%d/%m/%Y %H:%M:%S'):float(line[1])})
    
    print("SEPA_LEVEL", gauge_id, len(record), max(record), min(record))
    
    f = open(record_file,"wb")
    pickle.dump(record,f, protocol=-1)
    f.close()
    
    return

level_gauges = {116011:"Nevis@Claggan",
                234247:"Muick@Invermuick",
                14888:"Leny@Anie",
                371579:"North Esk (Tayside)@Inveriscandye",
                133168:"Water of Minnoch@Minnoch Bridge",
                8295:"Tay@Kenmore",
                14951:"Lyon@Comrie Bridge",
                14935:"Tay@Pitnacree",
                14963:"Tummel@Pitlochry",
                8402:"Braan@Hermitage",
                14936:"Tay@Caputh"}

rain_gauges = {115343:"Glen Nevis",
               367371:"Glenmuick No2",
               14926:"Invermark",
               369554:"Waterside Perth",
               116007:"Upper Monachlye",
               15172:"Strathyre",
               115521:"Brigton"}


def data_download(level_gauges, rain_gauges, download_interval=6):
    """
    To avoid server overload on the SEPA servers a flexible request delay has been
    added which adapts the delay between each request such that the delay is 20 times 
    the time taken to download and process the response from the server. If the server
    is experienceing heavy loads then it will increase the delay so as to reduce the 
    load on the server. The download interval is the number of hours between starting 
    a new set of downloads. If all the downloads take longer than the download 
    interval then it will imediatly start a new set of downloads once the last set 
    has finished.
    """
    while True:
        time_start = time.clock()
        #LEVEL GAUGES
        for key in level_gauges.keys():
            try:
                t_s = time.clock()
                sepa_level(key)
                t = (time.clock() - t_s)*20
                print(t)
                time.sleep(t)
            except Exception as e:
                print(e)
        
        #RAINFALL GAUGES
        for key in rain_gauges.keys():
            try:
                t_s = time.clock()
                sepa_rainfall(key)
                t = (time.clock() - t_s)*20
                print(t)
                time.sleep(t)
            except Exception as e:
                print(e)
        
        delay = (download_interval*3600)-(time.clock() - time_start)
        
        if delay < 0:
            delay = 0
        
        time.sleep(delay)
        
data_download(level_gauges, rain_gauges)
