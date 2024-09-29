from sseclient import SSEClient

messages = SSEClient("http://localhost:4203/api/trial")
for msg in messages:
    print(msg.data)
