import pandas as pd
from argparse import ArgumentParser

parser = ArgumentParser()
parser.add_argument("-f", "--file", dest="filepath",
                    help="Where is the old csv file")

parser.add_argument("-i", "--id", dest="idcolumn",
                    help="The name of the column with the ID's")

parser.add_argument("-p", "--phone", dest="phonecolumn",
                    help="The name of the column with the phone numbers")

parser.add_argument("-e", "--email", dest="emailcolumn",
                    help="The name of the column with the email addresses")

args = parser.parse_args()

if __name__ == '__main__':

    class UserInfo():
        def __init__(self, ID, Field, FieldCount):
            self.ID = ID
            self.Field = Field
            self.FieldCount = FieldCount

    usersMails = []
    usersPhones = []

    def countEmails(ID):
        emailcount = 0
        for user in usersMails:
            if user.ID == ID:
                emailcount += 1
        return emailcount

    def countPhones(ID):
        phonecount = 0
        for user in usersPhones:
            if user.ID == ID:
                phonecount += 1
        return phonecount

    def checkIDPositionInMails(ID):
        for i in range(len(usersMails)):
            if usersMails[i].ID == ID:
                return i
        return -1

    def checkIDPositionInPhones(ID):
        for i in range(len(usersPhones)):
            if usersPhones[i].ID == ID:
                return i
        return -1

    def clearMoreThanThreeEmailsByUser():
        for user in usersMails:
            while countEmails(user.ID) > 3:
                usersMails.pop(checkIDPositionInMails(user.ID))

    def clearMoreThanThreePhonesByUser():
        for user in usersPhones:
            while countPhones(user.ID) > 3:
                usersPhones.pop(checkIDPositionInPhones(user.ID))

    # Read the excel file to use
    PATH = args.filepath
    IDCOLUMN = args.idcolumn
    PHONECOLUMN = args.phonecolumn
    EMAILCOLUMN = args.emailcolumn
    SHEET = 'Contactos'

    oldEx = pd.read_excel(PATH, sheet_name=SHEET)

    # get the ids, emails and phones without repetitions
    idList = oldEx[IDCOLUMN].unique().tolist()
    emailList = oldEx[EMAILCOLUMN].unique().tolist()
    phoneList = oldEx[PHONECOLUMN].unique().tolist()

    # add emails to the email list
    for id in idList:
        for email in emailList:
            if email in oldEx[oldEx[IDCOLUMN] == id][EMAILCOLUMN].values:
                usersMails.insert(0, UserInfo(id, email, oldEx[oldEx[IDCOLUMN] == id][EMAILCOLUMN].value_counts()[email]))

    # add phones to the phones list
    for id in idList:
        for phone in phoneList:
            if phone in oldEx[oldEx[IDCOLUMN] == id][PHONECOLUMN].values:
                usersPhones.insert(0, UserInfo(id, phone, oldEx[oldEx[IDCOLUMN] == id][PHONECOLUMN].value_counts()[phone]))

    # organize the emails and phones lists by least repetitions to delete the least repeated
    usersMails.sort(key=lambda x: x.FieldCount, reverse=False)
    usersPhones.sort(key=lambda x: x.FieldCount, reverse=False)

    # remove emails and phones with more than three repetitions
    clearMoreThanThreeEmailsByUser()
    clearMoreThanThreePhonesByUser()

    # remove the emails and phones columns from the oldEx dataframe
    oldEx.drop(columns=[EMAILCOLUMN], inplace=True)
    oldEx.drop(columns=[PHONECOLUMN], inplace=True)

    # create a new dataframe with the same columns and rows as the new dataframe without ID repetitions
    newEx = pd.DataFrame(oldEx)
    newEx.drop_duplicates(subset=[IDCOLUMN], inplace=True)

    # organize the emails and phones lists by highest repetitions to take first the most repeated
    usersMails.sort(key=lambda x: x.FieldCount, reverse=True)
    usersPhones.sort(key=lambda x: x.FieldCount, reverse=True)

    # add the emails and phones columns to the new dataframe
    for id in idList:
        aux = 1;
        while checkIDPositionInMails(id) != -1:
            newEx.loc[newEx[IDCOLUMN] == id, 'Email_' + str(aux)] = usersMails[checkIDPositionInMails(id)].Field
            usersMails.pop(checkIDPositionInMails(id))
            aux += 1

    for id in idList:
        aux = 1;
        while checkIDPositionInPhones(id) != -1:
            newEx.loc[newEx[IDCOLUMN] == id, 'Teléfono_' + str(aux)] = usersPhones[checkIDPositionInPhones(id)].Field
            usersPhones.pop(checkIDPositionInPhones(id))
            aux += 1

    # save the new dataframe to a csv file
    newEx.to_csv('newF.csv', index=False, encoding="latin1")

    print('Done!')
