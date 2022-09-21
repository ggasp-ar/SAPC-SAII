from datetime import datetime
import pprint

def debugPrint(x,spot):
    now = datetime.now()
    current_time = now.strftime("%H:%M:%S")
    print('----------- [{}] Start of DebugPrint at {} -------\n'.format(current_time,spot))
    pprint.pprint(x)
    print("\n----------- End of DebugPrint -------")

def fetchAll(db, sql):
    cursor = db.connection.cursor()
    cursor.execute(sql)
    temp_data = cursor.fetchall()
    field_names = [i[0] for i in cursor.description]
    cursor.close()
    results=[]
    for r in temp_data:
        data={}
        i=0
        for c in field_names:
            data[c]=r[i]
            i+=1
        results.append(data)
    return results
    
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
