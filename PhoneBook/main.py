from PhoneBook import _addPar,_printAll,_addFile,_deletePar,_findNumber,_callPhone,_logCalls
import os

def menu():
    print ""
    print "---------PHONE BOOK---------"
    print "Select the option: "
    print "\t1 - Add contact"
    print "\t2 - Find contact"
    print "\t3 - Show contacts"
    print "\t4 - Delete contact"
    print "\t5 - Call Phone"
    print "\t6 - Load PhoneBook"
    print "\t7 - Show call logs"
    print "\t9 - Exit"

while True:
    menu()
    optionMenu = raw_input("Option >> ")

    if optionMenu=="1":
        name = raw_input("Please, insert the name of the contact: ")
        phone_number = raw_input("Please, insert the phone number: ")
        _addPar(name,phone_number)
        

    elif optionMenu=="2":
        name = raw_input("Please, insert the name of the contact: ")
        _findNumber(name)
        raw_input("Press ENTER to continue")

    elif optionMenu=="3":
        _printAll()
        raw_input("Press ENTER to continue")

    elif optionMenu=="4":
        name = raw_input("Please, insert the name of the contact: ")
        _deletePar(name)

    elif optionMenu=="5":
        phone_number = raw_input("Please, insert the phone number: ")
        _callPhone(phone_number)

    elif optionMenu == "6":
        name_file = raw_input("Please, insert the name of the file: ")
        item = name_file + '.txt'
        _addFile(item)

    elif optionMenu == "7":
        _logCalls()
        raw_input("Press ENTER to continue")

    elif optionMenu=="9":
        break

    else:
        print ""
        raw_input("Incorrect Option ...\nPress ENTER to continue")
