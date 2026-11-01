from models import (
    Book, Magazine, ReferenceBook, StudentMember,
    ResearchStudent, FacultyMember, NotifiedMember
)
from storage import load_data
from library_service import LibraryManager


items, members, loans = load_data()
library = LibraryManager(items, members, loans)


def add_item():
    print("\n1. Book")
    print("2. Magazine")
    print("3. Reference Book")

    choice = input("enter item type: ")
    item_id = input("enter item id: ")
    title = input("enter title: ")

    if choice == "1":
        item = Book(item_id, title)
    elif choice == "2":
        item = Magazine(item_id, title)
    elif choice == "3":
        item = ReferenceBook(item_id, title)
    else:
        print("invalid choice")
        return

    library.add_item(item)


def add_member():
    print("\n1. Student")
    print("2. Research Student")
    print("3. Faculty")
    print("4. Notified Member")

    choice = input("enter member type: ")
    member_id = input("enter member id: ")
    name = input("enter member name: ")

    if choice == "1":
        member = StudentMember(member_id, name)
    elif choice == "2":
        member = ResearchStudent(member_id, name)
    elif choice == "3":
        member = FacultyMember(member_id, name)
    elif choice == "4":
        member = NotifiedMember(member_id, name)
    else:
        print("invalid choice")
        return

    library.add_member(member)


while True:
    print("\n========== LIBRARY MANAGEMENT ==========")
    print("1. Add library item")
    print("2. Register member")
    print("3. Borrow item")
    print("4. Return item")
    print("5. View reports")
    print("6. Exit")

    ch = input("enter your choice: ")

    if ch == "1":
        add_item()

    elif ch == "2":
        add_member()

    elif ch == "3":
        member_id = input("enter member id: ")
        item_id = input("enter item id: ")
        library.borrow_item(member_id, item_id)

    elif ch == "4":
        member_id = input("enter member id: ")
        item_id = input("enter item id: ")
        library.return_item(member_id, item_id)

    elif ch == "5":
        library.show_reports()

    elif ch == "6":
        library.save()
        print("thank you")
        break

    else:
        print("invalid choice")
