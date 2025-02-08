from enum import Enum


class Module(str, Enum):
    AUTH = "AUTH"
    DATABASE = "DATABASE"
    CACHE = "CACHE"
    NETWORK = "NETWORK"
    PAYMENT = "PAYMENT"
    REGISTRATION = "REGISTRATION"
    SECURITY = "SECURITY"
