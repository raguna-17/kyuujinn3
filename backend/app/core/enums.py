from enum import Enum

class UserRole(str, Enum):
    USER = "USER"
    COMPANY = "COMPANY"
    ADMIN = "ADMIN"


class RegisterRole(str, Enum):
    USER = "USER"
    COMPANY = "COMPANY"
    

class EmploymentType(str, Enum):
    FULL_TIME = "full_time"
    PART_TIME = "part_time"
    CONTRACT = "contract"
    INTERN = "intern"


class ApplicationStatus(str, Enum):
    APPLIED = "applied"
    REVIEWING = "reviewing"
    INTERVIEW = "interview"
    REJECTED = "rejected"
    ACCEPTED = "accepted"