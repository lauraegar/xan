import requests
from locust import HttpUser, task, between

class LoginUser(HttpUser):
    wait_time = between(1, 10)  # Simulates user think-time

    @task
    def login(self):
        response = self.client.post("/bpapi/rest/security/session", json={
            "username": "USERNAME",
            "password": "PASSWORD"
        })

        # Optional assertions
        if response.status_code != 200:
            print(f"Login failed: {response.status_code}")
        else:
            auth_token = response.json().get("session-token")
            if not auth_token:
                print("Login success, but no token returned.")

   
