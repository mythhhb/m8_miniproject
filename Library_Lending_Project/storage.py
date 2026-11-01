import json
import os
from datetime import datetime


def save_data(items, members, loans):
    data = {
        "items": [],
        "members": [],
        "loans": loans
    }

    for item in items.values():
        if isinstance(item, Book):
            item_type = "Book"
        elif isinstance(item, Magazine):
            item_type = "Magazine"
        else:
            item_type = "ReferenceBook"

        data["items"].append({
            "item_id": item.item_id,
            "title": item.title,
            "item_type": item_type,
            "available": item.available
        })

    for member in members.values():
        if isinstance(member, ResearchStudent):
            member_type = "ResearchStudent"
        elif isinstance(member, StudentMember):
            member_type = "StudentMember"
        elif isinstance(member, FacultyMember):
            member_type = "FacultyMember"
        elif isinstance(member, NotifiedMember):
            member_type = "NotifiedMember"
        else:
            member_type = "Member"

        data["members"].append({
            "member_id": member.member_id,
            "name": member.name,
            "borrowing_limit": member.borrowing_limit,
            "member_type": member_type,
            "active_loans": member._active_loans
        })

    with open("data.json", "w") as file:
        json.dump(data, file, indent=4)


def load_data():
    from models import (
        Book, Magazine, ReferenceBook, Member,
        StudentMember, ResearchStudent, FacultyMember,
        NotifiedMember
    )

    items = {}
    members = {}
    loans = []

    if not os.path.exists("data.json"):
        return items, members, loans

    try:
        with open("data.json", "r") as file:
            data = json.load(file)

        for item_data in data.get("items", []):
            item_type = item_data.get("item_type")

            if item_type == "Book":
                item = Book(item_data["item_id"], item_data["title"])
            elif item_type == "Magazine":
                item = Magazine(item_data["item_id"], item_data["title"])
            else:
                item = ReferenceBook(item_data["item_id"], item_data["title"])

            if item_data.get("available") is False:
                item.issue_item()

            items[item.item_id] = item

        for member_data in data.get("members", []):
            member_type = member_data.get("member_type")
            member_id = member_data["member_id"]
            name = member_data["name"]
            limit = member_data["borrowing_limit"]

            if member_type == "ResearchStudent":
                member = ResearchStudent(member_id, name, limit)
            elif member_type == "StudentMember":
                member = StudentMember(member_id, name, limit)
            elif member_type == "FacultyMember":
                member = FacultyMember(member_id, name, limit)
            elif member_type == "NotifiedMember":
                member = NotifiedMember(member_id, name, limit)
            else:
                member = Member(member_id, name, limit)

            member._active_loans = member_data.get("active_loans", [])
            members[member.member_id] = member

        loans = data.get("loans", [])

    except (json.JSONDecodeError, KeyError, TypeError):
        print("Data file has some problem. Starting with empty records.")
        return {}, {}, []

    return items, members, loans


# Imports are kept here so the save function can identify each class.
from models import (
    Book, Magazine, ReferenceBook, StudentMember,
    ResearchStudent, FacultyMember, NotifiedMember
)
