# miniFB.py
#
# Author: Aaron Stevens (azs@bu.edu), Biken Maharjan (bm181354@bu.edu) 
#
# Description:
# a simple application which simulates the core social networking
# features of Facebook:
#   creating/updating user profiles;
#   adding friends;
#   creating and viewing status messages.

import time
import sqlite3 as db

#####################################################################################
#Done
def getDBConnectionAndCursor():
    """
    This helper function establishes a connection to the database 
    and returns connection and cursor objects.
    """

    # connect to the database
    conn = db.connect('./miniFB.db')
        
    # obtain a cursor object
    cursor = conn.cursor()
    # return connection and cursor objects to calling context

    return conn, cursor

################################################################################
#Done
def displayUserList():
    
    """
    Displays a list of all users from the profiles database.
    """
    

    print()
    print("Display user list.")
    
    
    ## Your Code Here!
    ## display a list of user id, firstname, lastname, email (no activities)
    
    conn, cursor = getDBConnectionAndCursor()
    #SQL query
    sql = '''SELECT * FROM profiles'''

    
    cursor.execute(sql)
    results = cursor.fetchall()

    #connection closed
    cursor.close()
    conn.commit()
    conn.close()
    
    # prints out all the information for all USERS 
    for row in results:
        user_id, firstname, lastname, email, act = row
        print("ID:\t%s\t%s\t%s\t%s" %(user_id, firstname, lastname, email))
        userid = user_id
        
################################################################################
#done        
def showProfilePage():
    """
    Displays the profile page for a single user.
    """
 
    print()
    print("Showing a profile page.")

    profileID = int(input("Enter profile ID: "))
    
    ## Your Code Here!
    ## show the content of the profile for the record with idNum
    ## show all the fields in a decent format
    
    #connection
    conn, cursor = getDBConnectionAndCursor()
    id = (profileID, )
    
    # SQL query 
    sql = '''SELECT * FROM profiles WHERE profileid = ? '''

    print()
    print("Display user list.")
    cursor.execute(sql,id)
    results = cursor.fetchall()

    #connection closed
    cursor.close()
    conn.commit()
    conn.close()
    
    # prints out all the information for a single user determined by profileID
    
    for row in results:
        user_id, firstname, lastname, email, activities = row
        print("ID:\t%s\t%s\t%s\t%s\t%s" %(user_id, firstname, lastname, email,activities))

################################################################################
#DONE
def createProfile():
    """
    Create a new profile, and store the record in the profiles table.
    """
    print()
    print("Create a new profile.")
    firstName = input("Enter First Name: ")
    lastName = input("Enter Last Name: ")
    email = input("Enter Email Address: ")
    activities = input("Enter Activities: ")

    
    ## Your Code Here!
    ## insert a new record into the database with this info.
    ## make sure you find the next unused profileID before inserting.
    
    #connection
    conn, cursor = getDBConnectionAndCursor()

    #for ID
    ######
    sql_one = '''SELECT max(profileID) FROM profiles'''
    cursor.execute(sql_one)
    # returns a tuple
    rowcount = cursor.fetchone()
    ######
    
    # rowcount contains the current max{profileID}
    parameters = (rowcount[0]+1,firstName,lastName,email,activities)
    
    sql = '''INSERT INTO profiles VALUES(?,?,?,?,?) '''

    cursor.execute(sql,parameters)
    rowcount = cursor.rowcount
    
    cursor.close
    conn.commit()
    conn.close()
    return rowcount

    

################################################################################
#DONE
def updateProfile():
    """
    Update a profile, to change the email or activities.
    """
    print()
    print("Update a profile.")

    profileID = int(input("Enter profile ID: "))
    email = input("Enter Email Address: ")
    activities = input("Enter Activities: ")
    
    ## Your Code Here!
    ## make update to the database for the record with this profileID
    
    conn, cursor = getDBConnectionAndCursor()
    sql = '''UPDATE profiles SET activities = ?,email = ? WHERE profileid = ?  '''

    # user can decides to change email and profileID. If changes are made then sql query will
    # update the database. If end-user inputs the same email ID or activities then it remains the same despite
    # of query.
    
    parameters = (activities,email,profileID)
    cursor.execute(sql,parameters)
    rowcount = cursor.rowcount
    
    cursor.close
    conn.commit()
    conn.close()
    
    return rowcount


################################################################################
def showFriends():
    """
    Displays a list of all friends for a single user.
    """
 
    print()
    print("Show friends.")
    
    profileID = int(input("For whom to list friends? Enter profile ID: "))

    #######
    conn, cursor = getDBConnectionAndCursor()
    
    # SQL query that display friends' name of [profileID]
    sql = '''SELECT firstname,lastname FROM profiles JOIN friends ON profiles.profileid = friends.friendid AND friends.profileid = ?'''

    parameters = (profileID,)
    cursor.execute(sql,parameters)
    results = cursor.fetchall()
    
    # Display all the Friends
    print("FRIENDLIST: ")
    for row in results:
        firstname,lastname = row
        print("\t%s\t%s" %(firstname, lastname))
    
    cursor.close
    conn.commit()
    conn.close()

################################################################################
def addFriend():
    
    """
    Add (create) a friend relationship between two users.
    """

    print()
    print("Add a friend.")

    profileID = int(input("Who is adding the friend? Enter profile ID: "))
    friendID = int(input("Who is the friend? Enter profile ID: "))
    
    ## Your Code Here!
    ## insert a record to friends table with both profileID numbers
    conn, cursor = getDBConnectionAndCursor()
    #SQL Query
    sql = '''INSERT INTO friends VALUES (?,?)'''
    
    parameters = (profileID,friendID)
    cursor.execute(sql,parameters)
    rowcount = cursor.rowcount
    cursor.close
    conn.commit()
    conn.close()
    return rowcount


################################################################################
def showStatusMessages():
    """
    Displays a list of status messages for a single user's friends.
    """
 
    print()
    print("Show status messages.")

    profileID = int(input("For whom should we find status updates? Enter a profile ID: "))
  

    ## Your Code Here!
    ## Query 'friends' table to find all friends's idNumbers for this profileID

    conn, cursor = getDBConnectionAndCursor()
    sql = '''SELECT status.profileid,message FROM status JOIN friends ON status.profileid = friends.friendid AND friends.profileid = ?'''
    parameters = (profileID,)
    cursor.execute(sql,parameters)
    results = cursor.fetchall()
    
    # display all the status of [profileID]'s Friends.
    print("MESSAGE: ")
    for row in results:
        profileid,status = row
        print("\tID:%s STATUS:  \t%s" %(profileid,status))
    
    cursor.close
    conn.commit()
    conn.close()

    
################################################################################
def writeStatusMessage():
    """
    Compose a new status message and record it to the status table..
    """

    print()
    print("Write a status message.")

    profileID = int(input("Who is writing the status message? Enter a profile ID: "))
    message = input("What are you doing right now? ")

    tm = time.localtime()
    nowtime = '%04d-%02d-%02d %02d:%02d:%02d' % tm[0:6]


    ## Your Code Here!
    ## do an insert into the status table with this status message
    conn, cursor = getDBConnectionAndCursor()
    sql = '''INSERT INTO status VALUES (?,?,?)'''
    
    parameters = (profileID,nowtime,message)
    cursor.execute(sql,parameters)
    rowcount = cursor.rowcount
    cursor.close
    conn.commit()
    conn.close()
    return rowcount
    
################################################################################
if __name__ == "__main__":

    # a main program loop:

    choice = "foo"

    while choice.lower()[0] != "q":

        print("""
    MiniFacebook: Please select an option:
    (d) display user list       (f) show friends
    (p) show profile page       (a) add friend
    (c) create profile          (s) show status messages
    (u) update profile          (w) write status message
    (q) quit the application
    """)
        
        choice = input("> ")

        if choice.lower()[0] == "d":

            displayUserList()
            
        elif choice.lower()[0] == "p":

            showProfilePage()

        elif choice.lower()[0] == "c":

            createProfile()

        elif choice.lower()[0] == "u":
            
            updateProfile()

        elif choice.lower()[0] == "f":

            showFriends()

        elif choice.lower()[0] == "a":

            addFriend()

        elif choice.lower()[0] == "s":

            showStatusMessages()

        elif choice.lower()[0] == "w":

            writeStatusMessage()

        # end of the loop

print("Goodbye!")
        
