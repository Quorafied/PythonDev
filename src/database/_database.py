from _ownLibrary import *

class ownDatabase():
    """ Connect to the database and define a cursor on instantiation """
    def __init__(self):
        self.conn = sqlite3.connect('data.db')
        self.c = self.conn.cursor()
        self.create_UsersTable()


    """ Commit and close the connection """
    def closeConnection(self):
        self.conn.commit()
        self.conn.close()

    """ Commit changes """
    def commitChanges(self):
        self.conn.commit()

    """ Create variables table """
    def create_UsersTable(self):
        self.c.execute("""
        CREATE TABLE IF NOT EXISTS
        users (
            discord_user_id INTEGER NOT NULL,
            osu_username VARCHAR(32) NOT NULL
        )
        """)

        self.commitChanges()
    
    """ Associate usernames """
    def associateUsernames(self, discordId):
        
        self.c.execute("""
        SELECT osu_username
        FROM users
        WHERE discord_user_id = ?""",
        (discordId, ))

        username = self.c.fetchall()
        
        return False if (len(username) == 0 or len(username) > 1) else username[0][0]

        
    """ Link discord users to osu usernames """
    def linkUsers(self, discordId, username):
        oldUsername = self.associateUsernames(discordId)
        if oldUsername is not False:
            print(oldUsername)
            if oldUsername == username:
                return "Existing"
            else:
                self.c.execute("""
                UPDATE users
                SET osu_username = ?
                WHERE discord_user_id = ?""", (username, discordId))

                self.commitChanges()
                return True
                
        else:
            self.c.execute("""
            INSERT INTO users
            (
                discord_user_id,
                osu_username
            )
            VALUES (
            ?, ?
            )""", (discordId, username))
        
            self.commitChanges()
            return True
db = ownDatabase()

class foxcraftDatabase():
    def __init__(self):
        self.conn = sqlite3.connect("C:/Users/Cosmin/Documents/Code/MinecraftInfo/data.db")
        self.c = self.conn.cursor()
    
    def closeConnection(self):
        self.conn.close()

    def commitChanges(self):
        self.conn.commit()

    def show_auctionHouse(self):
        self.c.execute("""SELECT * FROM auction_house""")
        rows = self.c.fetchall()

        if len(rows) == 0:
            return False
        
        return rows
    
    def show_last_listing(self):
        self.c.execute("""SELECT * FROM update_table""")
        rows = self.c.fetchall()
        return rows
    
    
foxDB = foxcraftDatabase()