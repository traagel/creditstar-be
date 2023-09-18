import random

import requests

# Define the API endpoint
API_ENDPOINT = "http://127.0.0.1:5000/api/v1/data/users/<int:client_id>/predict"

# Generate 200 random user IDs (adjust the range according to your actual user ID range)
user_ids = random.sample(range(1, 1000), 200)  # Assuming user IDs range from 1 to 1000

# Fetch predictions for each user ID and store results
results = {}
for user_id in user_ids:
    response = requests.get(API_ENDPOINT.replace('<int:client_id>', str(user_id)))

    # Check if the request was successful
    if response.status_code == 200:
        outcome = response.json().get("outcome", None)
        if outcome is not None:
            results[user_id] = "Loan Approved" if outcome == 1 else "Loan Denied"
        else:
            results[user_id] = "Error in prediction"
    else:
        results[user_id] = f"API Error: {response.status_code}"

# Print the results
for user_id, outcome in results.items():
    print(f"User ID: {user_id} -> {outcome}")
