from .Database import UserManager
Database = UserManager()
print(Database.get_all_users())
__all__ = ["Database"]
