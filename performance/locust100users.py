from locust import HttpUser, TaskSet, task, between
import random
import string

# Simulate 100 different users 
def generate_user(index):
    return {
        "username": f"user{index}",
        "password": "some complicated password"
    }

# excute log in behaviour
class UserBehavior(TaskSet):
    @task
    def login(self):
        user_data = generate_user(self.user_index)
        self.client.post("/login", json=user_data)

class WebsiteUser(HttpUser):
    tasks = [UserBehavior]
    wait_time = between(0, 0)  # No wait time to simulate simultaneous logins
    user_index = 0

    def on_start(self):
        # Assign a unique user index for each simulated user
        if not hasattr(self.environment, "user_count"):
            self.environment.user_count = 0

        self.user_index = self.environment.user_count
        self.environment.user_count += 1