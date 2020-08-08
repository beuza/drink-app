from flask import Flask, render_template, session, redirect, url_for, flash, request

from flask_bootstrap import Bootstrap

from flask_datepicker import datepicker

import random
import string

from .db_communication import getEvents, getEventUsersName, getEventNames, getEventUserID, setVote, getCurrentCycleID, \
    getUserID, getCurrentCycleState, hasVoted, countVotes, checkCycle, getVote, setSwigs, create_event, \
    setSwigsInitialy, checkOpenSwigs, getNumberOfSwigsToSpread, checkSwigsDistributed, getInvitation_key, Invitation_keyExist,getintoEvent, getEventID, getDeviceIDs, getVictories, getAttendance, getAverageParticipants

app = Flask(__name__)
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

app.config['SECRET_KEY'] = 'TEST'
bootstrap = Bootstrap(app)


def setDeviceID():
    # Only for Test
    # Hier soll mal die Device_Id oder Email abgefragt werden
    global global_device_id
    global_device_id = str(1)

def __setVote__(flash_index):
    """
    Setzt Vote und checkt zugleich ob Cycle geändert werden muss
    """
    try:
        vote = request.form['vote']
        event_id = request.form['event_id']
        flash_index = "vote"
    except:
        flash_index = flash_index
        return flash_index

    cycle_id = getCurrentCycleID(event_id)
    user_id = getUserID(global_device_id, event_id)
    setVote(user_id=user_id, voted_user_id=vote, cycle_id=cycle_id)

    # Refresh Cycle if needed
    checkCycle(cycle_id=cycle_id, event_id=event_id, changeCycle=False)
    return flash_index

def __setSwigs__(flash_index):
    """
    Setzt Vote und checkt zugleich ob Cycle geändert werden muss
    """
    try:
        clicks = request.form['voting']
        event_id = request.form['event_id']
        flash_index = "slugs"
    except:
        flash_index = flash_index
        return flash_index

    user_id = getUserID(global_device_id, event_id)
    event_user_ids = getEventUserID(event_id)
    i = 0
    for swig in clicks:
        try:
            print(swig)
            swig = int(swig)
            if swig > 0:
                setSwigs(user_id=user_id, voted_user_id=event_user_ids[i])
            i = i + 1
        except ValueError:
            pass

    return flash_index
    # TODO: Hier muss notification für Trinker eingebaut werden
    # TODO: Es muss noch irgendwie erkennbar sein, ob die Schlücke schon verteilt wurden

def __getintoEvent__(falsh_index):
    """
    Erstellt neues Event
    """
    try:
        link = request.form['link']
        user_name = request.form['user_name']
        flash_index = "getintoEvent"
        getintoEvent(link=link, user_name=user_name, device_id=global_device_id)
    except:
        flash_index = falsh_index
        return flash_index
    return flash_index

def __createEvent__(flash):
    """
    Erstellt neues Event
    """
    try:
        gruppenname = request.form['gruppenname']
        user_name = request.form['user_name']
        flash_index = "create_event"
    except:
        flash_index = flash
        return flash_index

    create_event(gruppenname=gruppenname, owner_device_id=global_device_id, user_name=user_name, link="abs13")
    return flash_index

    # TODO: Hier muss notification für Trinker eingebaut werden

def getQuotes(device_ids):
    victories = getVictories(device_ids)
    attendes = getAttendance(device_ids)
    average_participants = getAverageParticipants(device_ids)

    eps = 1e-20
    factor = []
    for i in range(0,len(device_ids)):
        factor.append(attendes[i]/(victories[i]*average_participants[i]+eps))

    quote = [0] * len(device_ids)
    border = max(factor)-min(factor)
    for i in range(0,len(device_ids)-1):
        if border/3+min(factor) > factor[i]:
            quote[i] = 2
        elif 2*border/3+min(factor) > factor[i]:
            quote[i] = 3
        else:
            quote[i] = 4

    # Ordnet besten und schlechtesten HP-Kandidaten Quote zu
    quote[factor.index(min(factor))] = 1
    quote[factor.index(max(factor))] = 5
    return quote

def ___getNumberOfSwigsToSpread__(user_id, event_id, votes):
    device_ids = getDeviceIDs(event_id)
    quotes = getQuotes(device_ids=device_ids)
    print(user_id[votes.index(max(votes))])
    print(device_ids[votes.index(max(votes))])
    return quotes[votes.index(max(votes))]

def getNumberOfSwigsToDrink(user_id, event_id):
    # TODO
    res = random.randint(0,6)
    return res

def getOwnVote(votes, cycle_id, ownUser_id, user_id):
    """
    Returns 1 falls vote richtig
    sonst 0
    """
    winning_id = getVote(cycle_id, ownUser_id)
    res = 0

    if user_id[votes.index(max(votes))] == winning_id:
        res = 1

    return res

def checkVote(user_id, cycle_id):
    """
    Checkt für alle User (user_id) in einem Cycle (cycle_id) ob diese bereits gevotet haben
    """
    res = []
    for i in user_id:
        res.append(hasVoted(user_id=i, cycle_id=cycle_id))
    return res

@app.cli.command()
def test():
    """Run the unit tests"""
    import unittest
    tests = unittest.TestLoader().discover('tests')
    unittest.TextTestRunner(verbosity=2).run(tests)

@app.route('/', methods=['GET', 'POST'])
def index():
    setDeviceID()
    flash_index = 0
    res = getEvents(device_id=global_device_id)
    event_names = getEventNames(res)

    # TODO: Wurde auskommentiert, da es meiner Meinung nach an der falschen Stelle ist (Sebi)
    # Falls zuvor ein Event erstellt wurde
    #flash_index = __createEvent__(flash_index)
    flash_index = __getintoEvent__(flash_index)

    # Falls die Schlücke gespeichert werden
    flash_index = __setSwigs__(flash_index)

    # Falls gevoted wurde
    flash_index = __setVote__(flash_index)

    print(flash_index)
    # TODO amount of events muss irgendwie noch umgangen werden. Kann nicht die Lösung sein
    return render_template('index.html', amount_of_events=len(event_names), event_names=event_names, event_IDs=res,
                           flash_index=flash_index)

@app.route('/decision')
def decision():
    return render_template('decision.html')

@app.route('/swigsoverview/<event_id>', methods=['GET', 'POST'])
def swigsoverview(event_id):
    event_names = getEventNames(event_id)
    event_users = getEventUsersName(event_id)
    swigs = []
    for e in event_users:
        swigs.append(getNumberOfSwigsToDrink(e, event_id))
    return render_template('swigsoverview.html', event_name=event_names, event_users=event_users, amount_of_user=len(event_users), swigs=swigs)

@app.route('/decision-unclear')
def decisionUnclear():
    return render_template('decision-unclear.html')

@app.route('/event/<event_id>', methods=['GET', 'POST'])
def event(event_id):
    #TODO: Testing
    getQuotes(event_id)

    cycle_id = getCurrentCycleID(event_id)
    state = getCurrentCycleState(cycle_id)
    if state == 'closed':
        checkCycle(cycle_id=cycle_id, event_id=event_id, changeCycle=False)
        cycle_id = getCurrentCycleID(event_id)
        state = getCurrentCycleState(cycle_id)

    event_names = getEventNames(event_id)
    event_user = getEventUsersName(event_id)
    user_id = getEventUserID(event_id)
    own_id = getUserID(device_id=global_device_id, event_id=event_id)

    if state == 'betting':
        if hasVoted(user_id=own_id, cycle_id=cycle_id, ):
            isclosed = 0
            checkVoteList = checkVote(cycle_id=cycle_id, user_id=user_id)
            return render_template('decision-unclear.html', event_name=event_names, amount_of_user=len(event_user),
                                   event_users=event_user, checkVoteList=checkVoteList, isclosed=isclosed)
        else:
            return render_template('event.html', event_name=event_names, event_id=event_id, event_users=event_user,
                                   user_id=user_id, amount_of_user=len(event_user), state=state)

    elif state == 'voting':
        if hasVoted(user_id=getUserID(device_id=global_device_id, event_id=event_id), cycle_id=cycle_id):
            votes = countVotes(cycle_id=cycle_id, user_id=user_id)
            if sum(votes) == len(event_user):
                # ownVote ist 1 falls richtig sonst 0
                ownVote = getOwnVote(votes, cycle_id, own_id, user_id)

                # Wurden die Schlücke schon verteilt?
                if checkSwigsDistributed(user_id=own_id):
                    # Prüft ob User noch offene Schlücke hat TODO: Wo ist der unterschied zu oben?
                    if ownVote == 1 and checkOpenSwigs(own_id):
                        for i in range(1, ___getNumberOfSwigsToSpread__(user_id=user_id, event_id=event_id, votes=votes) + 1):
                            setSwigsInitialy(user_id=own_id)
                else:
                    ownVote = 2

                link = str("/give-slugs/" + event_id)
                return render_template('decision.html', amount_of_user=len(event_user), event_name=event_names,
                                       event_users=event_user, votes=votes, ownVote=ownVote, link=link)
            else:
                checkVoteList = checkVote(cycle_id=cycle_id, user_id=user_id)
                return render_template('decision-unclear.html', event_name=event_names, amount_of_user=len(event_user),
                                       event_users=event_user, checkVoteList=checkVoteList, isclosed=0)

        else:
            return render_template('event.html', event_name=event_names, event_id=event_id, event_users=event_user,
                                   user_id=user_id, amount_of_user=len(event_user), state=state)


    elif state == 'closed':
        isclosed = 1
        checkVoteList = checkVote(cycle_id=cycle_id, user_id=user_id)
        return render_template('decision-unclear.html', event_name=event_names, amount_of_user=len(event_user),
                               event_users=event_user, checkVoteList=checkVoteList, isclosed=isclosed)
    else:
        print('we got a problem')


@app.route('/create-HP', methods=['GET', 'POST'])
def createHP():
    return render_template('create-HP.html')

@app.route('/link-to-HP/<event_id>', methods=['GET', 'POST'])
def linktoHP(event_id):
    if event_id == str(0):
        link = ''.join(random.choice(string.ascii_lowercase) for i in range(5))
        while Invitation_keyExist(link):
            link = ''.join(random.choice(string.ascii_lowercase) for i in range(5))

        gruppenname = request.form['gruppenname']
        user_name = request.form['user_name']
        create_event(gruppenname=gruppenname, owner_device_id=global_device_id, user_name=user_name, link=link)
    else:
        link = getInvitation_key(event_id)
        user_name = getEventUsersName(event_id)

    return render_template('link-to-HP.html', user_name=user_name, link=link)


@app.route('/result')
def result():
    return render_template('result.html')


@app.route('/give-slugs/<event_id>', methods=['GET', 'POST'])
def giveSlugs(event_id):
    event_names = getEventNames(event_id)
    numberOfSwigsToSpread = getNumberOfSwigsToSpread(user_id=getUserID(device_id=global_device_id, event_id=event_id))
    event_users = getEventUsersName(event_id)
    evenet_user_ids = getEventUserID(event_id)
    openSwigs = 0
    for e in evenet_user_ids:
        if checkOpenSwigs(e):
            openSwigs = openSwigs +1
    print(openSwigs)
    print('giveSlugs')
    if openSwigs == 0:
        checkCycle(cycle_id=getCurrentCycleID(event_id), event_id=event_id, changeCycle=True)

    return render_template('give-slugs.html', event_id=event_id, event_name=event_names,
                           numberOfSlugsToSpread=numberOfSwigsToSpread,
                           event_users=event_users, amount_of_user=len(event_users))


@app.route('/invitation')
def invitation():
    return render_template('invitation.html')


@app.route('/invitation-accepted')
def invitationAccepted():
    return render_template('invitation-accepted.html')


if __name__ == '__main__':
    bootstrap = Bootstrap(app)
    bootstrap.run()
    # TODO wird glaub ich nicht mehr gebraucht
    datepicker(app)
