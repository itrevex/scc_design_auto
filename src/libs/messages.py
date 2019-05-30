import sys

class Messages:
    '''
    Possible errors and warnings

    These are given to the user to make decisions
    '''

    CONTINUE = "Do you wish to continue? y/n \n"
    DEEPER_SECTION = "%s specified for %s is deeper than the beam"

    def __init__(self, message):
        pass

    @staticmethod
    def promptUser():
        print()
        response = input(Messages.CONTINUE)
        if (response.lower() == 'yes' or response.lower() == 'y' or response == ""):
            #continue to detail with the errors
            pass
        else:
            print()
            print("Program terminated")
            sys.exit()

    @staticmethod
    def showWarning(message):
        print()
        print(message)
        Messages.promptUser()
        
    @staticmethod
    def w(TAG, *arg):
        print()
        print("Tag: ", TAG)
        print(*arg)

    @staticmethod
    def i(TAG, *arg):
        print()
        print("Tag: ", TAG)
        print(*arg)

    @staticmethod
    def d(TAG, *arg):
        print()
        print("Tag: ", TAG)
        print(*arg)

    @staticmethod
    def continuePrompt(message):
        print()
        input(message)

    @staticmethod
    def showError(message):
        print()
        print("ERROR!")
        print(message)
        print()
        print("Program terminated")
        sys.exit()
