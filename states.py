
from aiogram.dispatcher.filters.state import StatesGroup, State


class UserStates(StatesGroup):
    Registration = State()
    Complaint = State()
    Q3 = State()
    Q4 = State()
    Q5 = State()
    Q6 = State()
    Q7 = State()
    Q8 = State()
    Q9 = State()
    Q10 = State()
    Q11 = State()
    Q12 = State()
    Q13 = State()
    Exist = State()
    NotExist = State()
    Location = State()
    card_reissue = State()
    admin_group_status = State()
    admin_group_answer = State()
    wait = State()
    admin_group_ticket_status = State()
    admin_group_ticket_answer = State()
    
    