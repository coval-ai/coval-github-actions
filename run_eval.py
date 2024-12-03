import os
import json
import requests
import time


class RunEval:
    def __init__(self):
        self.api_key = os.getenv("COVAL_API_KEY")
        if not self.api_key:
            raise ValueError("COVAL_API_KEY environment variable is required")
            
        self.organization_id = os.getenv("ORGANIZATION_ID")
        if not self.organization_id:
            raise ValueError("ORGANIZATION_ID environment variable is required")
            
        self.dataset_id = os.getenv("DATASET_ID")
        if not self.dataset_id:
            raise ValueError("DATASET_ID environment variable is required")

        self.test_set_name = os.getenv("TEST_SET_NAME")
        if not self.test_set_name:
            raise ValueError("TEST_SET_NAME environment variable is required")

        try:
            self.config = json.loads(os.getenv("CONFIG"))
        except json.JSONDecodeError as e:
            raise ValueError(f"Invalid JSON in CONFIG environment variable: {str(e)}")
            
        self.created_by = os.getenv("CREATED_BY", "Github Action")
        self.run_status_url = 'https://api.coval.dev/eval/run'
        
    def get_run_status_api(self, run_id):
        """
        This function gets the status of the run from the API.
        """
        config = {"run_id": run_id}
        headers = {
            "Content-Type": "application/json",
            "x-api-key": self.api_key,
        }

        try:
            response = requests.get(self.run_status_url, params=config, headers=headers)
            response.raise_for_status()
            result = response.json()
            return result.get('status')
        except requests.exceptions.RequestException as e:
            print(f"Request Exception: {str(e)}")
            if hasattr(e, 'response'):
                print(f"Error Response Status Code: {e.response.status_code}")
                print(f"Error Response Headers: {json.dumps(dict(e.response.headers), indent=2)}")
                print(f"Error Response Body: {e.response.text}")
            return None

    def _wait_for_run_to_complete(self, run_id, max_wait_time=600, check_interval=60):
        """
        This function waits for the run to complete by periodically checking its status.
        """
        start_time = time.time()

        while time.time() - start_time < max_wait_time:
            status = self.get_run_status_api(run_id)

            if status == "COMPLETED":
                print(f"Job completed successfully. Run ID: {run_id}")
                return
            elif status == "FAILED":
                raise Exception(f"Job failed. Run ID: {run_id}")
            elif status is None:
                raise Exception(f"Failed to get status for Run ID: {run_id}")

            print(f"Current status: {status}. Waiting {check_interval} seconds before next check...")
            time.sleep(check_interval)

        raise TimeoutError(f"Job timed out after {max_wait_time} seconds. Final status: {status}")

    def run(self):
        """
        This function triggers a new run and waits for the run to finish.
        """
        headers = {
            "Content-Type": "application/json",
            "x-api-key": self.api_key
        }
     
        self.config.setdefault("organization_id", self.organization_id)
        self.config.setdefault("dataset_id", self.dataset_id)
        self.config.setdefault("created_by", self.created_by)
        self.config.setdefault("test_set_name", self.test_set_name)
        self.config.setdefault("created_by", self.created_by)
        
        api_url = 'https://api.coval.dev/eval'

        try:
            response = requests.post(api_url, json=self.config, headers=headers)
            response.raise_for_status()
            result = response.json()
            run_id = result['run_id']

            if not run_id:
                raise ValueError("Failed to get run_id from API response")

            # Wait for the job to finish
            self._wait_for_run_to_complete(run_id)

        except requests.exceptions.RequestException as e:
            print(f"Request Exception: {str(e)}")
            if hasattr(e, 'response'):
                print(f"Error Response Status Code: {e.response.status_code}")
                print(f"Error Response Headers: {json.dumps(dict(e.response.headers), indent=2)}")
                print(f"Error Response Body: {e.response.text}")
            raise Exception(f"API request failed: {str(e)}")

if __name__ == "__main__":
    RunEval().run()

