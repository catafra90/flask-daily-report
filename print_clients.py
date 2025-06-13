import importlib
import mock_data

importlib.reload(mock_data)  # force reloading updated module
from mock_data import mock_clients

print("Script is running")
from mock_data import mock_clients

print("📋 Client List:")
print("-" * 30)

for client in mock_clients:
    print(f"Name:  {client['name']}")
    print(f"Phone: {client['phone']}")
    print(f"Email: {client['email']}")
    print("-" * 30)
