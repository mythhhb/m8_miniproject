from datetime import datetime, timedelta
from models import Book, Magazine, ReferenceBook
from storage import save_data


class LibraryManager:
    def __init__(self, items, members, loans):
        self.items = items
        self.members = members
        self.loans = loans

    def add_item(self, item):
        if item.item_id in self.items:
            print("item id already exists")
            return

        self.items[item.item_id] = item
        self.save()
        print("item added successfully")

    def add_member(self, member):
        if member.member_id in self.members:
            print("member id already exists")
            return

        self.members[member.member_id] = member
        self.save()
        print("member added successfully")

    def borrow_item(self, member_id, item_id):
        if member_id not in self.members:
            print("member not found")
            return

        if item_id not in self.items:
            print("item not found")
            return

        member = self.members[member_id]
        item = self.items[item_id]

        if not item.available:
            print("item is already issued")
            return

        if isinstance(item, ReferenceBook):
            print("reference books cannot be borrowed")
            return

        if not member.can_borrow():
            print("borrowing limit reached")
            return

        issue_date = datetime.now()
        due_date = issue_date + timedelta(days=item.loan_period_days())

        item.issue_item()
        member.add_loan(item_id)

        loan = {
            "member_id": member_id,
            "item_id": item_id,
            "issue_date": issue_date.strftime("%Y-%m-%d"),
            "due_date": due_date.strftime("%Y-%m-%d")
        }

        self.loans.append(loan)
        self.save()
        print("borrow successful")
        print("due date:", loan["due_date"])

        if hasattr(member, "send_notice"):
            member.send_notice("Your item has been issued successfully.")

    def return_item(self, member_id, item_id):
        found_loan = None

        for loan in self.loans:
            if loan["member_id"] == member_id and loan["item_id"] == item_id:
                found_loan = loan
                break

        if found_loan is None:
            print("active loan not found")
            return

        due_date = datetime.strptime(found_loan["due_date"], "%Y-%m-%d").date()
        today = datetime.now().date()
        overdue_days = (today - due_date).days

        if overdue_days < 0:
            overdue_days = 0

        fine = self.calculate_fine(overdue_days)

        self.items[item_id].return_item()
        self.members[member_id].remove_loan(item_id)
        self.loans.remove(found_loan)

        self.save()

        print("item returned successfully")
        print("overdue days:", overdue_days)
        print("fine: Rs.", fine)

    @staticmethod
    def calculate_fine(overdue_days):
        return overdue_days * 5

    def show_items(self):
        print("\n===== ALL LIBRARY ITEMS =====")
        if not self.items:
            print("no items found")

        for item in self.items.values():
            print(item.item_id, "|", item.title, "|", type(item).__name__,
                  "| Available:", item.available)

    def show_available_items(self):
        print("\n===== AVAILABLE ITEMS =====")
        for item in self.items.values():
            if item.available:
                print(item.item_id, "|", item.title)

    def show_loans(self):
        print("\n===== ACTIVE LOANS =====")
        if not self.loans:
            print("no active loans")

        for loan in self.loans:
            print(loan["item_id"], "|", loan["member_id"],
                  "| Due:", loan["due_date"])

    def show_overdue_loans(self):
        print("\n===== OVERDUE LOANS =====")
        today = datetime.now().date()
        found = False

        for loan in self.loans:
            due_date = datetime.strptime(loan["due_date"], "%Y-%m-%d").date()

            if due_date < today:
                found = True
                print(loan["item_id"], "|", loan["member_id"],
                      "| Due:", loan["due_date"])

        if not found:
            print("no overdue loans")

    def show_members(self):
        print("\n===== MEMBERS =====")
        for member in self.members.values():
            print(member.member_id, "|", member.name,
                  "| Borrowed items:", member.active_loan_count)

    def show_reports(self):
        self.show_items()
        self.show_available_items()
        self.show_loans()
        self.show_overdue_loans()
        self.show_members()

    def save(self):
        save_data(self.items, self.members, self.loans)
