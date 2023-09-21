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

    def change_status(self, num, status):
        query = "UPDATE ticket SET status = %s WHERE num = %s"
        values = (status, num)
        self.db.execute_query(query, values)

    def num_exists(self, num):
        query = "SELECT num FROM ticket WHERE num = %s"
        result = self.db.execute_query(query, (num,))
        return bool(result)

    def add_status(self, user_id, com, cats, serialNum):
        query = "INSERT INTO ticket (userid, message, category, serial, ticket_status, ticket_answer) VALUES ('%d', '%s', '%s', '%s', 'Заявка отправлена', 'Ответа нет')" % (user_id, str(com), str(cats), str(serialNum))
        print(query)
        self.db.execute_query(query)

    def change_status(self, num, status):
        query = "UPDATE ticket SET status = %s WHERE num = %s"
        values = (status, num)
        self.db.execute_query(query, values)

    def add_ticket_card_reissue(self, client_id, client_form):
        query = "INSERT INTO ticket_card_reissue (client_id, client_form, ticket_status, ticket_answer) VALUES ('%s', '%s', 'Заявка отправлена', 'Ответа нет')" % (str(client_id), str(client_form))
        self.db.execute_query(query)

    def ticket_id_by_client_form(self, client_form):
        query = "SELECT ticket_id FROM ticket_card_reissue WHERE client_form = '%s'" % (str(client_form))
        result = self.db.execute_query(query)
        return result

    def delete_ticket_card_reissue(self, ticket_id):
        query = "UPDATE ticket_card_reissue SET ticket_status = 'closed' WHERE ticket_id = %d" % (int(ticket_id))
        self.db.execute_query(query)

    def delete_atm_ticket(self, ticket_id):
        query = "UPDATE ticket SET ticket_status = 'closed' WHERE ticket_id = %d" % (int(ticket_id))
        self.db.execute_query(query)

    def select_ticket_card_reissue(self, client_id):
        query = "SELECT * FROM ticket_card_reissue WHERE client_id = '%s'" % (str(client_id))
        result = self.db.execute_query(query)
        return result
    
    def select_atm_ticket(self, client_id):
        query = "SELECT * FROM ticket WHERE userid = '%s'" % (str(client_id))
        result = self.db.execute_query(query)
        return result
    
    def update_status_by_id(self, ticket_status, ticket_id):
        query = "UPDATE ticket_card_reissue SET ticket_status = '%s' WHERE ticket_id = %d" % (str(ticket_status), int(ticket_id))
        self.db.execute_query(query)

    def update_ticket_status_by_id(self, ticket_status, ticket_id):
        query = "UPDATE ticket SET ticket_status = '%s' WHERE ticket_id = %d" % (str(ticket_status), int(ticket_id))
        self.db.execute_query(query)

    def update_answer_by_id(self, ticket_answer, ticket_id):
        query = "UPDATE ticket_card_reissue SET ticket_answer = '%s' WHERE ticket_id = %d" % (str(ticket_answer), int(ticket_id))
        self.db.execute_query(query)

    def update_ticket_answer_by_id(self, ticket_answer, ticket_id):
        query = "UPDATE ticket SET ticket_answer = '%s' WHERE ticket_id = %d" % (str(ticket_answer), int(ticket_id))
        self.db.execute_query(query)

    def ticket_by_ticket_id(self, ticket_id):
        query = "SELECT * FROM ticket_card_reissue WHERE ticket_id = %d" % (int(ticket_id))
        result = self.db.execute_query(query)
        return result
    
    def atm_ticket_by_ticket_id(self, ticket_id):
        query = "SELECT * FROM ticket WHERE ticket_id = %d" % (int(ticket_id))
        result = self.db.execute_query(query)
        return result
    
    def get_last_num(self):
        query = "SELECT ticket_id FROM ticket"
        result = self.db.execute_query(query)
        last_num = result[len(result)-1]
        return last_num[0]


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
        query = "SELECT admin FROM admins WHERE admin = '%s'" % (str(user_id),)
        result = self.db.execute_query(query)
        print(result)
        return bool(len(result))
    
    def admin_by_state(self, state):
        query = "SELECT admin FROM admins WHERE State = '%s'" % (state,)
        result = self.db.execute_query(query)
        return result

    def add(self, name, num, user_id):
        query = "INSERT INTO user (Name, Phone, Id) VALUES ('%s', '%s', '%s')" % (name, num, str(user_id)) 
        self.db.execute_query(query)


class Atm:
    def __init__(self, db):
        self.db = db

    def get_all_atm_coordinates(self):
        query = "SELECT * FROM atm_location"
        result = self.db.execute_query(query)
        return result

    def unique_id_by_terminal(self, TerminalID):
        query = "SELECT UniqueID FROM atm WHERE TerminalID = '%s'" % (str(TerminalID))
        result = self.db.execute_query(query)
        return result

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
