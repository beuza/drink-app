"""
Methods for DB communication
"""

from datetime import datetime, time, timedelta
from sqlalchemy import create_engine, TIMESTAMP, MetaData, Column, String, Integer, DateTime, Table, Boolean

import random

engine = create_engine('postgresql://sebi:beuza@v220200284142109433.supersrv.de:5432/hpapp')

"""
METHODS FOR VOTES
"""

def countVotes(cycle_id, user_id):
    """
    Zähl alle votes in einem Cycle pro user_id

    Gibt Liste mit der Anzahl zurück. Sortiert nach der user_id
    """
    counts = []
    for i in range(len(user_id)):
        with engine.connect() as connection:
            result = connection.execute(
                "select user_id from polls where cycle_id=" + str(cycle_id) + "AND voted_user_id = " + str(user_id[i]))
            res = 0
            for r in result:
                res = res + 1
        counts.append(res)
        connection.close()
    return counts

def hasVoted(cycle_id, user_id):
    """
    Gibt für eine user_id zu einem Zeitpunkt (cycle_id) an ob user schon gevotet hat
    """
    with engine.connect() as connection:
        result = connection.execute(
            "select voted_user_id from polls where user_id=" + str(user_id) + "and cycle_id=" + str(cycle_id))
        res = 0
        for r in result:
            res = 1
    connection.close()
    return res

def setVote(user_id, voted_user_id, cycle_id):
    """
    Vote abgeben. Beschreibt hierfür die votes Tabelle
    """
    with engine.connect() as connection:
        connection.execute(
            "insert into polls (user_id, cycle_id, voted_user_id) values (" + str(user_id) + "," + str(
                cycle_id) + "," + str(voted_user_id) + ")")
    connection.close()

def getVote(cycle_id, user_id):
    """
    Gibt den eigenen Vote zurück
    """
    with engine.connect() as connection:
        result = connection.execute(
            "select voted_user_id from polls where user_id=" + str(user_id) + "and cycle_id=" + str(cycle_id))
        for r in result:
            res = r[0]
    connection.close()
    return res

"""
METHODS FOR USERS
"""

def getUserID(device_id, event_id):
    """
    Gibt die eigene user_id bzgl. device_id und event_id zurück
    """
    with engine.connect() as connection:
        result = connection.execute(
            "select user_id from users where device_id=" + str(device_id) + "AND event_id = " + str(event_id))
        for r in result:
            res = r[0]
    connection.close()
    return res

def getEventUsersName(eventID):
    """
    Gibt die Usernamen zu einem Event (eventID) aus
    """
    with engine.connect() as connection:
        res = []
        result = connection.execute("select name from users where event_id=" + str(eventID))

        for r in result:
            res.append(r['name'])
    connection.close()

    return res

def getEventUserID(event_ids):
    """
    Gibt UserIDs aus für ein oder mehrere Events
    """
    print('getEventUserID')
    with engine.connect() as connection:
        res = []
        for e in event_ids:
            try:
                int(e)
                result = connection.execute("select user_id from users where event_id=" + str(e))
                for r in result:
                    res.append(r['user_id'])
            except ValueError:
                print('Value Error')

    connection.close()
    return res

def getEventUserID_request_form(event_ids):
    """
    Gibt UserIDs aus für ein oder mehrere Events
    """
    with engine.connect() as connection:
        res = []
        result = connection.execute("select user_id from users where event_id=" + str(event_ids))
        for r in result:
            res.append(r['user_id'])

    connection.close()
    return res

def creat_users(event_id, owner_device_id, user_name, is_admin):
    # Berechnet maximale user_id
    print('create_users')
    with engine.connect() as connection:
        result = connection.execute("select max(user_id) from users")
        for r in result:
            max_user_id = r[0]
    connection.close()

    new_user_id = max_user_id +1
    print(new_user_id)
    print(str(user_name))
    print(event_id)
    # Setzt neuen Admin
    if is_admin:
        with engine.connect() as connection:
            connection.execute(
                "insert into users (user_id, device_id, name, is_admin, is_active, event_id) values (" + str(new_user_id) + "," + str(
                    owner_device_id) + ",'" +  str(user_name) + "'," + "TRUE" + "," + "TRUE" + "," + str(event_id) + ")")
        connection.close()
    else:
        with engine.connect() as connection:
            connection.execute(
                "insert into users (user_id, device_id, name, is_admin, is_active, event_id) values (" + str(new_user_id) + "," + str(
                    owner_device_id) + ",'" +  str(user_name) + "'," + "FALSE" + "," + "TRUE" + "," + str(event_id) + ")")
        connection.close()


"""
METHODS FOR EVENTS
"""

def Invitation_keyExist(link):
    """
    Gibt den Einladungslink des Events anhand einer event_id aus
    """
    res = True
    with engine.connect() as connection:
        try:
            result = connection.execute("select invitation_key from events where invitation_key=" + str(link))
        except:
            res = False
    connection.close()

    return res

def getInvitation_key(event_id):
    """
    Gibt den Einladungslink des Events anhand einer event_id aus
    """
    with engine.connect() as connection:
        res = []
        for e in event_id:
            result = connection.execute("select invitation_key from events where event_id=" + str(e))

            for r in result:
                res.append(r['name'])

    connection.close()
    return res

def getEventID(link):
    """
    Gibt die EventId des Events anhand eines einladungslinks aus
    """
    print("getEventID")
    print(str(link))
    res = []
    with engine.connect() as connection:
        result = connection.execute("select event_id from events where invitation_key='" + str(link) +"'")
        for r in result:
            res.append(r['event_id'])
    connection.close()
    print(res[0])
    print("Finish")
    return res[0]

def getEvents(device_id):
    """
    Gibt alle event_id für eine device_id an
    """
    res = []
    with engine.connect() as connection:
        result = connection.execute("select event_id from users where device_id=" + str(device_id))
        for r in result:
            res.append(r['event_id'])
    connection.close()
    return res

def getEventNames(event_ids):
    """
    Gibt Namen der Events anhand einer/mehrere event_ids aus
    """
    with engine.connect() as connection:
        res = []
        for e in event_ids:
            result = connection.execute("select name from events where event_id=" + str(e))

            for r in result:
                res.append(r['name'])

    connection.close()
    return res

def getintoEvent(link, user_name, device_id):
    print("getintoEvent")
    event_id = getEventID(link=link)
    print(event_id)
    creat_users(event_id=event_id, owner_device_id=device_id, user_name=user_name, is_admin=False)

def create_event(gruppenname, owner_device_id, user_name, link):
    # Berechnet maximalen Zyklus
    with engine.connect() as connection:
        result = connection.execute("select max(event_id) from events")
        for r in result:
            max_event_id = r[0]
    connection.close()

    new_event_id = max_event_id + 1
    meta = MetaData(engine)
    table = Table('events', meta, Column('event_id', Integer, primary_key=True), Column('name', String), Column('owner_device_id', Integer), Column('invitation_key', String))
    #table = Table('events', meta, Column('event_id', Integer, primary_key=True), Column('name', String), Column('owner_device_id', Integer),Column('event_date_time', DateTime), Column('invitation_key', String))
    meta.create_all()
    #ins = table.insert().values(event_id=new_event_id, name=gruppenname, owner_device_id=owner_device_id, end_date_time=datetime.utcnow(), invitation_key="abs13")
    ins = table.insert().values(event_id=new_event_id, name=gruppenname, owner_device_id=owner_device_id, invitation_key=link)
    conn = engine.connect()
    conn.execute(ins)
    print('1')
    start_cycle(new_event_id)
    print('2')
    creat_users(event_id=new_event_id, owner_device_id=owner_device_id, user_name=user_name, is_admin=True)
    print('3')


"""
METHODS FOR CYCLES
"""

def start_cycle(event_id):
    # Berechnet maximalen Zyklus
    with engine.connect() as connection:
        result = connection.execute("select max(cycle_id) from cycles")
        for r in result:
            max_cycle_id = r[0]
    connection.close()

    # Erhöht Zyklus
    meta = MetaData(engine)
    table = Table('cycles', meta, Column('cycle_id', Integer, primary_key=True), Column('state', String),
                  Column('end_date_time', DateTime), Column('event_id', Integer))
    meta.create_all()
    ins = table.insert().values(cycle_id=max_cycle_id + 1, state='betting', end_date_time=datetime.utcnow(), event_id=event_id)
    conn = engine.connect()
    conn.execute(ins)

def getCurrentCycleTimestamp(cycle_id):
    """
    Gibt den gesetzten Timestamp vom aktuellen Cycle aus
    """

    with engine.connect() as connection:
        result = connection.execute("select end_date_time from cycles where cycle_id=" + str(cycle_id))
        for r in result:
            res = r[0]
    connection.close()
    return res

def getCurrentCycleID(event_id):
    """
    Gibt die aktuelle cycle_id eines events (event_id) zurück
    """
    with engine.connect() as connection:
        result = connection.execute("select max(cycle_id) from cycles where event_id=" + str(event_id))
        for r in result:
            res = r[0]
    connection.close()
    return res

def getCurrentCycleState(cycle_id):
    """
    Gibt den aktuell Status eines Cycles (cycle_id) zurück.
    """
    with engine.connect() as connection:
        result = connection.execute("select state from cycles where cycle_id=" + str(cycle_id))
        for r in result:
            res = r[0]
    connection.close()
    return res

def fromClosedToVoting(cycle_id):
    cycleTimestamp = getCurrentCycleTimestamp(cycle_id)
    # deadline am nächsten Tag um 8 Uhr.
    # TODO: sollte irgendwann variabel gestaltet werden.
    deadline = datetime.combine((cycleTimestamp + timedelta(days=1)).date(), time(hour=8, minute=0))
    diff = deadline - datetime.utcnow()

    if diff.days < 0:
        return True
    else:
        return False

def checkCycle(cycle_id, event_id, changeCycle):
    """
    Checkt den aktuellen Cycle. Falls nötig wird auf den nächste Cycle umgestellt.
    """
    user_IDs = getEventUserID_request_form(event_ids=event_id)
    votes = countVotes(cycle_id=cycle_id, user_id=user_IDs)
    currentCycleState = getCurrentCycleState(cycle_id=cycle_id)
    if currentCycleState == "betting" and sum(votes) == len(user_IDs):
        # Berechnet maximalen Zyklus
        print('fromBettingtoClosed')
        with engine.connect() as connection:
            result = connection.execute("select max(cycle_id) from cycles")
            for r in result:
                max_cycle_id = r[0]
        connection.close()

        # Erhöht Zyklus
        meta = MetaData(engine)
        table = Table('cycles', meta, Column('cycle_id', Integer, primary_key=True), Column('state', String), Column('end_date_time', DateTime), Column('event_id', Integer))
        meta.create_all()
        ins = table.insert().values(cycle_id=max_cycle_id+1, state='closed',end_date_time=datetime.utcnow(), event_id=event_id)
        conn = engine.connect()
        conn.execute(ins)

    elif fromClosedToVoting(cycle_id=cycle_id) and currentCycleState == 'closed':
        print('fromClosedToVoting')
        # Berechnet maximalen Zyklus
        with engine.connect() as connection:
            result = connection.execute("select max(cycle_id) from cycles")
            for r in result:
                max_cycle_id = r[0]
        connection.close()

        # Erhöht Zyklus
        meta = MetaData(engine)
        table = Table('cycles', meta, Column('cycle_id', Integer, primary_key=True), Column('state', String), Column('end_date_time', DateTime), Column('event_id', Integer))
        meta.create_all()
        ins = table.insert().values(cycle_id=max_cycle_id+1, state='voting',end_date_time=datetime.utcnow(), event_id=event_id)
        conn = engine.connect()
        conn.execute(ins)
    elif currentCycleState == 'voting' and changeCycle:
        print('fromVotingToBetting')
        # Berechnet maximalen Zyklus
        with engine.connect() as connection:
            result = connection.execute("select max(cycle_id) from cycles")
            for r in result:
                max_cycle_id = r[0]
        connection.close()

        # Erhöht Zyklus
        meta = MetaData(engine)
        table = Table('cycles', meta, Column('cycle_id', Integer, primary_key=True), Column('state', String), Column('end_date_time', DateTime), Column('event_id', Integer))
        meta.create_all()
        ins = table.insert().values(cycle_id=max_cycle_id+1, state='betting',end_date_time=datetime.utcnow(), event_id=event_id)
        conn = engine.connect()
        conn.execute(ins)


"""
METHODS FOR SWIGS
"""

def setSwigs(user_id, voted_user_id):
    """
    Schlücke verteilen. Beschreibt hierfür die swigs Tabelle
    Nur Einträge >0 werden berücksichtigt
    """
    with engine.connect() as connection:
        result = connection.execute("select swig_id from swigs where user_id = " + str(user_id) + " AND target_user_id IS NULL")
        for r in result:
            connection.execute("update swigs set target_user_id= " + str(voted_user_id) + " where swig_id=" + str(r[0]))
            return
#                "insert into swigs (swig_id, user_id, target_user_id, fulfilled) values (" + str(r[0]) + "," + str(
#                    user_id) + "," + str(voted_user_id) + "," + "FALSE" + ")")
    connection.close()

def checkOpenSwigs(user_id):
    """

    """
    openSwigs = True
    with engine.connect() as connection:
        result = connection.execute("select swig_id from swigs where user_id=" + str(user_id) + " AND target_user_id IS NULL")
        for r in result:
            openSwigs = False
    connection.close()
    return openSwigs

def checkSwigsDistributed(user_id):
    """
    Funktion prüft ob Schlücke schon verteilt wurden
    """
    SwigsDistributed = True
    with engine.connect() as connection:
        result = connection.execute("select swig_id from swigs where user_id=" + str(user_id) + " AND target_user_id IS NOT NULL AND fulfilled= FALSE")
        for r in result:
            SwigsDistributed = False
    connection.close()
    return SwigsDistributed

def setSwigsInitialy(user_id):
    """
    Setzt in der Datenbank die Anzahl der Schlücke, welche der User vergeben darf
    """
    with engine.connect() as connection:
        result = connection.execute("select max(swig_id) from swigs")
        for r in result:
            max_swig_id = r[0]
    connection.close()

    with engine.connect() as connection:
        # TODO cycle_id einfügen
        connection.execute("insert into swigs (swig_id, user_id, fulfilled) values (" + str(max_swig_id+1) + "," + str(user_id) + "," + "FALSE" + ")")
    connection.close()

def getNumberOfSwigsToSpread(user_id):
    """

    """
    amountOfOpenSwigs = 0
    with engine.connect() as connection:
        result = connection.execute("select swig_id from swigs where user_id=" + str(user_id) + " AND target_user_id IS NULL")
        for r in result:
            amountOfOpenSwigs = amountOfOpenSwigs+1
    connection.close()
    return amountOfOpenSwigs

"""
METHODS FOR QUOTE CALULATING
"""

def getDeviceIDs(event_id):
    """
    Gibt alle device_ids für eine event_id an
    """
    res = []
    with engine.connect() as connection:
        result = connection.execute("select device_id from users where event_id=" + str(event_id))
        for r in result:
            res.append(r['device_id'])
    connection.close()
    return res

def getVictories(device_ids):
    """
    Gibt alle Siege für mehrere device_ids an
    """
    # TODO
   # res = []
   # with engine.connect() as connection:
    #    result = connection.execute("select device_id from users where event_id=" + str(event_id))
     #   for r in result:
      #      res.append(r['device_id'])
    #connection.close()

    # Übergangslösung
    res = []

    for e in device_ids:
        res.append(random.randrange(0,10,1))

    return res



def getAttendance(device_ids):
    """
    Gibt alle Teilnahmen für mehrere device_ids an
    """
    res = []
    for e in device_ids:
        attendance = 0
        with engine.connect() as connection:
            result = connection.execute("select event_id from users where device_id=" + str(e))
            for r in result:
                attendance = attendance + 1
        connection.close()
        res.append(attendance)
    return res

def getAverageParticipants(device_ids):
    """
    Gibt den Durchschnitt aller Teilnehmer für mehrere device_ids an
    """
    res = []
    for e in device_ids:
        participants = 0
        index = 0
        with engine.connect() as connection:
            result = connection.execute("select event_id from users where device_id=" + str(e))
            for r in result:
                index = index + 1
                result_ = connection.execute("select user_id from users where event_id=" + str(r[0]))
                for rr in result_:
                    participants = participants + 1
        connection.close()
        res.append(participants/index)
    return res