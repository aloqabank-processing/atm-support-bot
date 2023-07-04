from db import Database


class Ticket:
    def __init__(self, db):
        self.db = db

    def exists(self, num):
        query = "SELECT num FROM ticket WHERE num = %s"
        result = self.db.execute_query(query, (num,))
        return bool(result)

    def add(self, user_id, message, category, serial):
        query = "INSERT INTO ticket (userid, message, category, serial) VALUES (%s, %s, %s, %s)"
        values = (user_id, message, category, serial)
        self.db.execute_query(query, values)
        self.db.commit()

    def change_status(self, num, status):
        query = "UPDATE ticket SET status = %s WHERE num = %s"
        values = (status, num)
        self.db.execute_query(query, values)
        self.db.commit()

    def num_exists(self, num):
        query = "SELECT num FROM ticket WHERE num = %s"
        result = self.db.execute_query(query, (num,))
        return bool(result)

    def add_status(self, user_id, com, cats, serialNum):
        query = "INSERT INTO ticket (userid, message, category, serial) VALUES (%s, %s, %s, %s)"
        values = (user_id, com, cats, serialNum)
        self.db.execute_query(query, values)
        self.db.commit()

    def change_status(self, num, status):
        query = "UPDATE ticket SET status = %s WHERE num = %s"
        values = (status, num)
        self.db.execute_query(query, values)
        self.db.commit()


class User:
    def __init__(self, db):
        self.db = db

    def info(self, user_id):
        query = "SELECT * FROM user WHERE Id = %s"
        result = self.db.execute_query(query, (user_id,))
        return result

    def exists(self, user_id):
        query = "SELECT Id FROM user WHERE Id = %s"
        result = self.db.execute_query(query, (user_id,))
        return bool(result)

    def admin_exists(self, user_id):
        query = "SELECT admin FROM admins WHERE admin = %s"
        result = self.db.execute_query(query, (user_id,))
        return bool(result)
    
    def admin_by_state(self, state):
        query = "SELECT admin FROM admins WHERE State = '%s'"
        result = self.db.execute_query(query, (state,))
        return bool(result)

    def add(self, name, num, user_id):
        query = "INSERT INTO user (Name, Phone, Id) VALUES (%s, %s, %s)"
        values = (name, num, user_id)
        self.db.execute_query(query, values)
        self.db.commit()


class Atm:
    def __init__(self, db):
        self.db = db

    def create(self, unique_id, state, terminal_id, type, model, location):
        query = "INSERT INTO atm (UniqueID, State, TerminalID, Type, Model, Location) VALUES (%s, %s, %s, %s, %s, %s)"
        values = (unique_id, state, terminal_id, type, model, location)
        self.db.execute_query(query, values)
        self.db.commit()

    def read(self, unique_id):
        query = "SELECT * FROM atm WHERE UniqueID = %s"
        result = self.db.execute_query(query, (unique_id,))
        return result

    def update(self, unique_id, state, terminal_id, type, model, location):
        query = "UPDATE atm SET State = %s, TerminalID = %s, Type = %s, Model = %s, Location = %s WHERE UniqueID = %s"
        values = (state, terminal_id, type, model, location, unique_id)
        self.db.execute_query(query, values)
        self.db.commit()

    def delete(self, unique_id):
        query = "DELETE FROM atm WHERE UniqueID = %s"
        self.db.execute_query(query, (unique_id,))
