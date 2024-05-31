import requests

print("Number of requests: \n")

number_of_requests = int(input())

for i in range(number_of_requests):
  response = requests.get('http://localhost:8080/', verify=True)
  if response.status_code == 200:
    print(response.text)
  else:
    print(f"Error: Server returned status code {response.status_code}")
