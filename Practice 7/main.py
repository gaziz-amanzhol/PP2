from config.config import load_config
from db.dbConnector import DBConnector
from db.PhoneBook import PhoneBook
db = DBConnector()
db.createTable()

while True:
    print("[1] GET ALL USERS")
    print("[2] INSERT NEW USER")
    print("[3] INSERT MANY USERS")
    print("[4] GET USERS BY LIMIT AND OFFSET")
    print("[5] DELETE USER")
    print("[0] EXIT")

    choice = int(input())
    if choice == 0:
        break
    elif choice == 1:
        all_records = db.getAllRecords()
        for user in all_records:
            print(user)
    elif choice == 2:
        first_name = input("Enter first name\n")
        last_name = input("Enter last name\n")
        phone = input("Enter phone\n")
        new_user = PhoneBook(0, first_name, last_name, phone)
        if (not db.isUserExist(new_user)):
            db.addNewUser(new_user)
        else:
            db.update(new_user)
    elif choice == 3:
        users = []
        amount = int(input("HOW MANY USERS YOU WANT TO ADD?\n"))
        for i in range(amount):
            first_name = input("Enter first name\n")
            last_name = input("Enter last name\n")
            phone = input("Enter phone\n")
            new_user = PhoneBook(0, first_name, last_name, phone)
            users.append(new_user)
        incorrect_users = db.insertManyUsers(users)
        if len(incorrect_users) > 0:
            print("INCORRECT USERS ARE ")
            for user in incorrect_users:
                print(user)
    elif choice == 4:
        limit = int(input("ENTER LIMIT\t"))
        offset = int(input("ENTER OFFSET\t"))
        all_users = db.getLimitOffset(limit, offset)
        for user in all_users:
            print(user)
    elif choice == 5:
        name_phone = input("ENTER NAME OR PHONE\n")
        if(len(name_phone) == 12 and name_phone[1:].isdigit()):
            db.deleteUserByPhone(name_phone)
        else:
            db.deleteUserByFirstName(name_phone)
