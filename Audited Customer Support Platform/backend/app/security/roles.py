from enum import Enum

class Role(str,  Enum):
    ADMIN = "admin"
    QA = "qa"
    AGENT = "agent"
    CUSTOMER = "customer"