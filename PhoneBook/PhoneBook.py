from Contact import Contact
import re

book = []
def _addFile(name):
    try:
        files = open(name)
        for line in files:
            obj = line.split(',')
            if _regular(obj[1]):
                phone = Contact(obj[0],obj[1],obj[2])
                book.append(phone)
        files.close()
        print 'Your Phone book were loaded'
        print type(book)
    except:
        print 'PHONE BOOK DOES NOT EXIST'
def _printAll():
    if len(book) == 0:
        print 'The Phone Book is empty'
    else:
        book.sort(key=lambda contact: contact.name)
        for obj in book:
            print 'Name: ' + str(obj.name), 'Phone: ' + str(obj.phone_number), 'Log: ' + str(obj.count_calls)

def _addPar(name, phone):
    empty = False
    if _regular(phone):
        contact = Contact(name,phone,0)
        book.append(contact)
        empty = True
    if empty:
        print 'Contact saved'
    else:
        print 'Contact not saved'

def _deletePar(name):
    empty = False
    i = 0
    while i < len(book):
        if book[i].name == name:
            book.remove(book[i])
            empty = True
            break
        i+=1
    if empty:
        print 'Deleted'
    else:
        print 'Contact does not exist'

def _findNumber(name):
    i = 0
    phone = ''
    while i < len(book):
        if book[i].name == name:
            phone = book[i].phone_number
            break
        i+=1
    if phone == '':
        print 'Contact does not exist'
    else:
        print phone

def _callPhone(phoneNumber):
    i = 0
    complete = False
    while i < len(book):
        if book[i].phone_number == phoneNumber:
            cant = int(book[i].count_calls)
            cant +=1
            book[i].count_calls = str(cant)
            complete = True
            break
        i+=1
    if complete:
        print 'Called done'
    else:
        print 'Contact does not exist'

def _logCalls():
    if len(book) == 0:
        print 'The Phone Book is empty'
    else:
        book.sort(key=lambda contact: int(contact.count_calls), reverse = True)
        i = 0
        cont = 0
        while i < len(book) and cont != 5:
            print book[i].name,book[i].phone_number,book[i].count_calls
            i+=1
            cont +=1
  
def _regular(phone):
    if re.match('(0|\\+359|00359)(87|88|89)([2-9]{1})([0-9]{6})$',phone):
        return True
    return False








