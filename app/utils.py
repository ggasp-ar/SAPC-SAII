from datetime import datetime

def debugPrint(x,spot):
    now = datetime.now()
    current_time = now.strftime("%H:%M:%S")
    print('----------- [{}] Start of DebugPrint at {} -------\n'.format(current_time,spot))
    print(x)
    print("\n----------- End of DebugPrint -------")

def fetchAll(db, sql):
    cursor = db.connection.cursor()
    cursor.execute(sql)
    data = cursor.fetchall()
    cursor.close()
    return data
    
def fetchOne(db, sql):
    data={}
    cursor = db.connection.cursor()
    cursor.execute(sql)
    temp_data = cursor.fetchone()
    i=0
    field_names = [i[0] for i in cursor.description]
    for c in field_names:
        data[c]=temp_data[i]
        i+=1
    cursor.close()
    return data
