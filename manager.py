import datetime
import socket
from flask import Flask, render_template, jsonify
import psutil
from sense_hat import SenseHat
import time
import mysql.connector
import threading
import mysql.connector
import datetime

DB_CONFIG = {
    'user': 'root',
    'password': 'csi4160project',
    'host': '34.27.202.36',
    'database': 'sensorvals'
}

def create_win_loss_table_if_not_exists():
    conn = mysql.connector.connect(**DB_CONFIG)
    cursor = conn.cursor()
    query = """
    CREATE TABLE IF NOT EXISTS WIN_LOSS_TBL (
        X_WINS INT,
        O_WINS INT,
        TIES INT,
        AI_wins INT,
        WINRATE_EASY_PLAYER INT,
        WINRATE_EASY_AI INT,
        WINRATE_MID_PLAYER INT,
        WINRATE_MID_AI INT,
        WINRATE_HARD_PLAYER INT,
        WINRATE_HARD_AI INT,
        GAMES_PLAYED INT,
        IPADDRESS VARCHAR(255) PRIMARY KEY,
        WHEN_OCCUR TIMESTAMP
    )
    """
    cursor.execute(query)
    _ = cursor.fetchall()
    conn.commit()
    cursor.close()
    conn.close()



'''
stats = {
    "X_wins": 0,
    "O_wins": 0,
    "AI_wins": 0,
    "WINRATE_EASY_PLAYER": 0,
    "WINRATE_EASY_AI":0,
    "WINRATE_MID_PLAYER": 0,
    "WINRATE_MID_AI":0,
    "WINRATE_HARD_PLAYER": 0,
    "WINRATE_HARD_AI":0,
    "ties": 0,
    "games_played": 0,
    
}
'''
#this is for sending win info to sql server
My_hostname = socket.gethostname()
My_IP = socket.gethostbyname(My_hostname)

app = Flask(__name__)
sense = SenseHat()

DB_CONFIG = {
    'user': 'root',
    'password': 'csi4160project',
    'host': '34.27.202.36', #public IP from your cloud SQL instance on GCP
    'database': 'sensorvals'
}


'''
table 2's config:
CREATE TABLE WIN_LOSS_TBL (
    X_WINS INT,
    O_WINS INT,
    TIES INT ,
    AI_wins INT,
    WINRATE_EASY_PLAYER INT,
    WINRATE_EASY_AI INT,
    WINRATE_MID_PLAYER INT,
    WINRATE_MID_AI INT,
    WINRATE_HARD_PLAYER INT,
    WINRATE_HARD_AI INT,
    GAMES_PLAYED INT,
    IPADDRESS VARCHAR2(255) PRIMARY KEY,
    WHEN_OCCUR TIMESTAMP
);
'''

def regain_win_from_cloud(stats):
    global My_IP

    create_win_loss_table_if_not_exists()

    conn = mysql.connector.connect(**DB_CONFIG)
    cursor = conn.cursor()

    # Fetch any previous results before starting new queries
    cursor.execute("SHOW TABLES")
    _ = cursor.fetchall()

    query = """
    SELECT X_WINS, O_WINS, TIES, AI_wins, WINRATE_EASY_PLAYER, WINRATE_EASY_AI, 
    WINRATE_MID_PLAYER, WINRATE_MID_AI, WINRATE_HARD_PLAYER, WINRATE_HARD_AI, 
    GAMES_PLAYED FROM WIN_LOSS_TBL WHERE IPADDRESS = %s
    """
    cursor.execute(query, (My_IP,))
    result = cursor.fetchall()

    if not result:
        print("downloaded Cloud SQL winrate successfully, none found")
        cursor.close()
        conn.close()
        return stats

    # There should not be more than one result due to IPADDRESS being a primary key
    result_actual = result[0]

    # Ensure to match the indices with the actual number of selected columns
    stats["X_wins"] = int(result_actual[0])
    stats["O_wins"] = int(result_actual[1])
    stats["ties"] = int(result_actual[2])
    stats["AI_wins"] = int(result_actual[3])
    stats["WINRATE_EASY_PLAYER"] = int(result_actual[4])
    stats["WINRATE_EASY_AI"] = int(result_actual[5])
    stats["WINRATE_MID_PLAYER"] = int(result_actual[6])
    stats["WINRATE_MID_AI"] = int(result_actual[7])
    stats["WINRATE_HARD_PLAYER"] = int(result_actual[8])
    stats["WINRATE_HARD_AI"] = int(result_actual[9])
    stats["games_played"] = int(result_actual[10])

    print("downloaded Cloud SQL winrate successfully")
    cursor.close()
    conn.close()
    return stats




def get_uptime_for_sql():
    #Format for mysql database in "hh:mm:ss"
    with open('/proc/uptime', 'r') as f:
        uptime_seconds = int(float(f.readline().split()[0]))
    hours = uptime_seconds // 3600
    minutes = (uptime_seconds % 3600) // 60
    seconds = uptime_seconds % 60
    return f"{hours:02}:{minutes:02}:{seconds:02}"


def upload_win_to_cloud_sql(stats):
    try:
        global My_IP

        print("1" + str(stats))

        conn = mysql.connector.connect(**DB_CONFIG)
        cursor = conn.cursor()
        query = "SELECT * FROM WIN_LOSS_TBL WHERE IPADDRESS = %s"
        cursor.execute(query, (My_IP,))
        result = cursor.fetchall()

        print("2")

        if len(result) != 0:
            query = "DELETE FROM WIN_LOSS_TBL WHERE IPADDRESS = %s"
            cursor.execute(query, (My_IP,))

        print(str(stats))
        X_WINS = stats.get("X_wins", 0)
        O_WINS = stats.get("O_wins", 0)
        TIES = stats.get("ties", 0)
        AI_wins = stats.get("AI_wins", 0)
        games_played = stats.get("games_played", 0)
        WINRATE_EASY_PLAYER = stats.get("WINRATE_EASY_PLAYER", 0)
        WINRATE_EASY_AI = stats.get("WINRATE_EASY_AI", 0)
        WINRATE_MID_PLAYER = stats.get("WINRATE_MID_PLAYER", 0)
        WINRATE_MID_AI = stats.get("WINRATE_MID_AI", 0)
        WINRATE_HARD_PLAYER = stats.get("WINRATE_HARD_PLAYER", 0)
        WINRATE_HARD_AI = stats.get("WINRATE_HARD_AI", 0)
        WHEN_OCCUR = datetime.datetime.now()

        print("3")

        query = """
        INSERT INTO WIN_LOSS_TBL (X_WINS, O_WINS, TIES, AI_wins, WINRATE_EASY_PLAYER, 
        WINRATE_EASY_AI, WINRATE_MID_PLAYER, WINRATE_MID_AI, WINRATE_HARD_PLAYER, 
        WINRATE_HARD_AI, games_played, IPADDRESS, WHEN_OCCUR) 
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s);
        """
        values = (X_WINS, O_WINS, TIES, AI_wins, WINRATE_EASY_PLAYER, WINRATE_EASY_AI, 
                  WINRATE_MID_PLAYER, WINRATE_MID_AI, WINRATE_HARD_PLAYER, WINRATE_HARD_AI, 
                  games_played, My_IP, WHEN_OCCUR)

        for x in values:
            print(str(x))

        cursor.execute(query, values)
        print("4")

        conn.commit()
        print("Uploaded to Cloud SQL successfully")
        cursor.close()
        conn.close()
    except Exception as e:
        print(f"Error uploading data: {e}")
        upload_win_to_cloud_sql(stats)



#Function to upload sensor data to Cloud SQL
def upload_to_cloud_sql():
    print("Thread started...") #Test to see if function is running
    while True:
        try:
            print("Reading sensor data...")  # Check if this prints
            #Read sensor data
            cpu = psutil.cpu_percent(interval=1)
            #print(f"CPU: {cpu}")  #Testing purposes
            memory = psutil.virtual_memory().percent
            #print(f"Memory: {memory}")#Testing purposes
            disk = psutil.disk_usage('/').percent
            #print(f"Disk: {disk}")#Testing purposes
            temperature = sense.get_temperature()
            #print(f"Temperature: {temperature}")#Testing purposes
            humidity = sense.get_humidity()
            #print(f"Humidity: {humidity}")#Testing purposes
            pressure = sense.get_pressure()
            #print(f"Pressure: {pressure}")#Testing purposes
            uptime =  get_uptime_for_sql()
            #print(f"Uptime: {uptime}")#Testing purposes
            

            #Connect to the Cloud SQL database
            #Test database connection
            print("Attempting to connect to Cloud SQL...")
            conn = mysql.connector.connect(**DB_CONFIG)
            print("Connected to Cloud SQL")

            cursor = conn.cursor()

            #Insert sensor data into the table
            print("Inserting data into database...")
            query = "INSERT INTO sensor_entries (cpu, memory, disk, temp, humidity, pressure, uptime) VALUES (%s, %s, %s, %s, %s, %s, %s);"
            values = (cpu, memory, disk, temperature, humidity, pressure, uptime)
            cursor.execute(query, values)

            #Commit and close connection
            conn.commit()
            print("Uploaded to Cloud SQL successfully")
            cursor.close()
            conn.close()

        except Exception as e:
            print(f"Error uploading data: {e}")

        time.sleep(1800)  #Upload data every 5 seconds

#Start background thread for data upload
threading.Thread(target=upload_to_cloud_sql, daemon=True).start()


# Serve the index page for the game
@app.route('/')
def index():
    # Example default stats (you can modify these values or update dynamically)
    stats = {
        'Xwins': 0,          # Default value for X wins
        'O_wins': 0,          # Default value for O wins
        'ties': 0,            # Default value for ties
        'games_played': 0     # Default value for games played
    }

    # Example current player and board (could be dynamic)
    current_player = "X"
    board = [["" for _ in range(3)] for _ in range(3)]  # Empty board (3x3)

    # Pass the stats, current player, and board to the template
    return render_template('index.html', current_player=current_player, stats=stats, board=board)

# Serve the system monitor page
@app.route('/monitor')
def monitor():
    return render_template('monitor.html')

# Monitor resources: CPU, RAM, and Storage
@app.route('/monitor_resources', methods=['GET'])
def monitor_resources():
    cpu_usage = psutil.cpu_percent(interval=1)
    memory_info = psutil.virtual_memory()
    memory_usage = {
        "total": memory_info.total,
        "used": memory_info.used,
        "free": memory_info.free,
        "percent": memory_info.percent
    }
    disk_info = psutil.disk_usage('/')
    disk_usage = {
        "total": disk_info.total,
        "used": disk_info.used,
        "free": disk_info.free,
        "percent": disk_info.percent
    }

    resource_info = {
        "cpu_usage": cpu_usage,
        "memory_usage": memory_usage,
        "disk_usage": disk_usage
    }

    return jsonify(resource_info)

# Monitor Sense HAT sensors: Temperature, Humidity, and Pressure
@app.route('/monitor_sensors', methods=['GET'])
def monitor_sensors():
    temperature = sense.get_temperature()
    humidity = sense.get_humidity()
    pressure = sense.get_pressure()

    sensor_data = {
        "temperature": temperature,
        "humidity": humidity,
        "pressure": pressure
    }

    return jsonify(sensor_data)

# System uptime monitoring
@app.route('/uptime', methods=['GET'])
def get_uptime():
    with open('/proc/uptime', 'r') as f:
        uptime_seconds = float(f.readline().split()[0])
    uptime_info = {
        "uptime_seconds": uptime_seconds,
        "uptime_hours": uptime_seconds / 3600
    }
    return jsonify(uptime_info)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, threaded=True)
