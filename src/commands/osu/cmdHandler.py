from _ownLibrary import *
from osu import *
from imageRecgonition import *
from database._database import *
from main import function
from commands.osu.pp_calculate import ppCalculator
from datetime import datetime, timedelta

class commandHandler():
    def handle_osulink(self, context):
        # Information required to be returned:
        """ 
        1. Osu username.
        2. Target_Channel_ID
        3. Error
        """

        Target_Channel_ID = context.channel.id
        Error = False
        osuUsername = False

        command_substring = "q.osulink"
        content = context.message.content.strip()
        content = content.replace(command_substring, "")

        if len(content) > 0:
            if ('"' in content or "'" in content) and len(content.split()) > 1:
                osuUsername = content.replace('"', "")
                osuUsername = content.replace("'", "")
                osuUsername = osuUsername.strip()

            elif len(content.split()) == 1 and not ('"' in content or "'" in content):
                osuUsername = content.strip()

            else:
                Error = f'Please follow the format: "" - for usernames with spaces, no "" for single word usernames' 

        else:
            Error = f"No username specified to link accounts."
        
        return osuUsername, Target_Channel_ID, Error


    def hamdle_recent(self, context, command_substring, mentioned):
        # Information required to be returned:
        """
        # Parameters
        `context`
            -> Context - Command Invoked context
        `command_substring`
            -> str - Command alias.
        `mentioned`
            -> ctx.message.raw_mentions
        # Returns:
        1. `osuUsername`
            -> Osu Username found in context.
        2. `Target_Channel_ID`
            -> Channel ID where the command was invoked.
        3. `authorId`
            -> Author ID of command invoker.
        4. `Error`
            -> Returns an Error code.
        """

        if command_substring == "q.rs": command_substring = "q.rs"
        else: command_substring = "q.recent"

        Target_Channel_ID = context.channel.id
        Error = False
        osuUsername = False

        content = context.message.content.strip()
        content = content.replace(command_substring, "")
        splitContent = content.split()

        if context.message.raw_mentions:
            authorId = context.message.raw_mentions[0]
        else:
            authorId = context.author.id
                    
        def checkUsername():
            osuUsername = False

            if len(splitContent) in [1, 3, 5]:
                if len(splitContent[0]) >= 3:
                    osuUsername = splitContent[0]

            return osuUsername
        

        if not mentioned:
            osuUsername = checkUsername()

            return osuUsername, Target_Channel_ID, authorId, Error
        
        else:
            return osuUsername, Target_Channel_ID, authorId, Error
    
    def handle_osuprofile(self, context, command_substring, mentioned):
        print("hello")
        Target_Channel_ID = context.channel.id
        Error = False
        osuUsername = False

        content = context.message.content.strip()
        content = content.replace(command_substring, "")
        splitContent = content.split()

        if context.message.raw_mentions:
            authorId = context.message.raw_mentions[0]
        else:
            authorId = context.author.id

        def checkUsername():
            osuUsername = False

            if len(splitContent) in [1, 3, 5]:
                if len(splitContent[0]) >= 3:
                    osuUsername = splitContent[0]
            
            return osuUsername
        
        if not mentioned:
            osuUsername = checkUsername()
            print(osuUsername)

            return osuUsername, Target_Channel_ID, authorId, Error

    def handle_top(self, context, command_substring, mentioned):
        # Information required to be returned:
        """
        Returns the following information.

        1. `osuUsername`
        2. `Target_Channel_ID`
        3. `authorId`
        4. `page`
        5. `index`
        6. `Error`
        """

        Target_Channel_ID = context.channel.id
        Error = False
        osuUsername = False
        page = False
        index = False

        content = context.message.content.strip()
        content = content.replace(command_substring, "")
        splitContent = content.split()

        if context.message.raw_mentions:
            authorId = context.message.raw_mentions[0]
        else:
            authorId = context.author.id

        def checkAlias():
            page, scoreindex = False, False
            aliases = ["-i", "-p"]

            pageFound = False
            scoreIndexFound = False


            if len(splitContent) >= 2:
                
                for index, word in enumerate(splitContent):

                    # Check if the word is pageAlias while the index if was found at, is not the last index.
                    if (word in aliases) and (index != len(splitContent) - 1):

                        if (word == "-p") and (splitContent[index+1].isdigit() is True) and (splitContent[index+1] in ["0", "1", "2", "3", "4", "5", "6", "7", "8", "9"]):
                            page = int(splitContent[index+1])*10

                            pageFound = True

                        if (word == "-i") and (splitContent[index+1].isdigit() is True):
                            scoreindex = int(splitContent[index+1])
                            if scoreindex == 0 or scoreindex > 100:
                                scoreindex = False
                                Error = "Score index should be between 1 and 100"
                            else:
                                scoreIndexFound = True


            if scoreIndexFound and pageFound:
                Error = "Can't combine pages and index, either a page or a score index."

            else: 
                Error = False

            return page, scoreindex, Error
                    
        def checkUsername():
            osuUsername = False

            if len(splitContent) in [1, 3, 5]:
                if len(splitContent[0]) >= 3:
                    osuUsername = splitContent[0]

            return osuUsername
        

        if not mentioned:
            page, index, Error = checkAlias()
            osuUsername = checkUsername()
            return osuUsername, Target_Channel_ID, authorId, page, index, Error
        
        else:
            page, index, Error = checkAlias()
            return osuUsername, Target_Channel_ID, authorId, page, index, Error


        

cmdHandler = commandHandler()

        