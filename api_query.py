import requests

class AdministrationModule:
    async def get_user(telegram_user_id):
        url = "http://10.231.202.221:7010/user/"
        params = {
            "telegram_user_id": telegram_user_id
        }
        response = requests.get(url, params=params)

        if response.status_code == 200:
            return response.json()
        else: 
            return None
        
    async def add_user(name, mobile, telegram_user_id):
        url = "http://10.231.202.221:7010/user/"
        params = {
            "name": name,
            "mobile": mobile,
            "telegram_user_id": telegram_user_id
        }
        response = requests.post(url, params=params)

        if response.status_code == 200:
            return response.json()
        else: 
            return None
        
class FeedbackModule:
    async def add_feedback(feedback_data):
        url = "http://10.231.202.221:7010/feedback/"
        response = requests.post(url, params=feedback_data)
        print(response.json())

    async def update_answer(answer_by_admin, current_ticket):
        url = "http://10.231.202.221:7010/feedback/" + str(current_ticket) + "/answer"
        params = {
            "answer": answer_by_admin
        }
        response = requests.put(url, params=params)
        print(response.json())

    async def update_status(feedback_id = None, status = None):
        url = "http://10.231.202.221:7010/feedback/" + str(feedback_id) + "/status"
        params = {
            "status": status
        }
        response = requests.put(url, params=params)
        print(response.json())

    async def get_feedback(feedback_id=None):
        url = "http://10.231.202.221:7010/feedback/" + str(feedback_id)
        response = requests.get(url)
        if response.status_code == 200:
            return response.json()
        else: 
            return None


