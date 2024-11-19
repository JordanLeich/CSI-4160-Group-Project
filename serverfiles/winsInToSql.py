import mysql.connector

def fetchDataGlobal(strType):
    # get the globle win rates, for that specific type
    cursor.execute("SELECT "+ strType + " FROM WIN_DATA;"   )
    #example "SELECT OWINS FROM WIN_DATA;"
    # Fetch the results
    results = cursor.fetchall()
    totalType = 0
    for row in results:
        totalType += row
    return totalType
# Database connection parameters
def fetchDataLocal(strType, strUser):
    # get the globle win rates, for that specific type
    cursor.execute("SELECT "+ strType + " FROM WIN_DATA WHERE  WHERE SOURCE = " + strUser + ";"   )
    #example "SELECT OWINS FROM WIN_DATA WHERE SOURCE =  127.0.0.1;"
    # Fetch the results
    results = cursor.fetchall()
    totalType = 0
    for row in results:
        totalType += row
    return totalType
# Database connection parameters
config = {
    'user': 'MILESTONE3',
    'password': 'csi4160#',
    'host': 'localhost',  # or '127.0.0.1'
    'database': 'WINTRACKER'
}
datatypes = (
    'OWINS',
    'XWINS',
    'TIES',
)
globaldata = [0,0,0]
personaldata = [0,0,0]
personalsource = ""
#we need to get the user's ip address, how?

def mainFunction():
    try:
        #we need to establish this connection's info first any ideas?
        # Establishing a connection
        conn = mysql.connector.connect(**config)
        if conn.is_connected():
            print('Connected to MySQL database')

        # Create a cursor object
        cursor = conn.cursor()
        """
        format for table is:
        WIN_DATA (
        SOURCE VARCHAR(12),
        ISONLINE BOOL,
        OWINS INT(),
        XWINS INT(),
        TIES INT(),);
        we can use isonline in place of the boolean check for bots if we do not do multiplayer
        """
        tempint = 0
        # get the globle win rates,
        for strType in datatypes:
            globaldata[tempint] = fetchDataGlobal(strType)
            tempint += 1
        #now we get the specific user's associated ip'sdata
        
        tempint = 0
        # get the globle win rates,
        for strType in datatypes:
            globaldata[tempint] = fetchDataLocal(strType, personalsource)
            tempint += 1

    except mysql.connector.Error as err:
        print(f"Error: {err}")

    finally:
        # Closing the connection
        cursor.close()
        conn.close()
