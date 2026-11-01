from abc import ABC, abstractmethod


class LibraryItem(ABC):
    def __init__(self, item_id, title):
        self.item_id = item_id
        self.title = title
        self._available = True

    @property
    def available(self):
        return self._available

    def issue_item(self):
        self._available = False

    def return_item(self):
        self._available = True

    @abstractmethod
    def loan_period_days(self):
        pass


class Book(LibraryItem):
    def loan_period_days(self):
        return 14


class Magazine(LibraryItem):
    def loan_period_days(self):
        return 7


class ReferenceBook(LibraryItem):
    def loan_period_days(self):
        return 0


class Member:
    library_name = "My College Library"
    max_active_loans_default = 3

    def __init__(self, member_id, name, borrowing_limit=None):
        self.member_id = member_id
        self.name = name

        if borrowing_limit is None:
            self.borrowing_limit = Member.max_active_loans_default
        else:
            self.borrowing_limit = borrowing_limit

        self._active_loans = []

    @property
    def active_loan_count(self):
        return len(self._active_loans)

    def add_loan(self, item_id):
        self._active_loans.append(item_id)

    def remove_loan(self, item_id):
        if item_id in self._active_loans:
            self._active_loans.remove(item_id)

    def can_borrow(self):
        return self.active_loan_count < self.borrowing_limit

    @classmethod
    def set_default_limit(cls, limit):
        cls.max_active_loans_default = limit


class StudentMember(Member):
    def __init__(self, member_id, name, borrowing_limit=2):
        super().__init__(member_id, name, borrowing_limit)


class ResearchStudent(StudentMember):
    def __init__(self, member_id, name, borrowing_limit=4):
        super().__init__(member_id, name, borrowing_limit)


class FacultyMember(Member):
    def __init__(self, member_id, name, borrowing_limit=5):
        super().__init__(member_id, name, borrowing_limit)


class NotificationMixin:
    def send_notice(self, message):
        print("NOTICE:", message)


class NotifiedMember(Member, NotificationMixin):
    # Member comes first in the method resolution order.
    # NotificationMixin provides the send_notice() method.
    pass
