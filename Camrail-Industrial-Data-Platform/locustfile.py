from locust import HttpUser, task, between
import random

class CamrailLoadTest(HttpUser):
    # Entreprise Load Test Configuration (Point 7)
    wait_time = between(0.1, 1.0)
    
    @task
    def predict_endpoint(self):
        headers = {"X-API-KEY": "entreprise_secret_key_2026", "Content-Type": "application/json"}
        payload = {
            "loco_id": f"LOCO_{random.randint(100, 999)}",
            "flow_rate": random.uniform(300, 500),
            "pressure": random.uniform(2.5, 5.0),
            "vibration": random.uniform(1.0, 6.0),
            "temperature": random.uniform(50.0, 95.0)
        }
        
        with self.client.post("/predict", json=payload, headers=headers, catch_response=True) as response:
            if response.status_code == 200:
                response.success()
            else:
                response.failure(f"Failed with status: {response.status_code}")
