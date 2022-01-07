from cryptography.fernet import Fernet

key = b'' #Not provided For Security Purposes
f = Fernet(key)

authHost = (f.decrypt(b'gAAAAABfu5yuuA6QWZca-LzNcBzKZ5iS-2KgYlfGRWLbeoylzXrFltLnhtIJVYlcKeXzDbe1wlp1IxTElwXAVYE5Oqfw7XO3cQ==')).decode()
authUser = (f.decrypt(b'gAAAAABfu5zNQOhDcfpgNkZTrVV35BU0txoT1bu6jl77hK_O2bKCIgLvuDdD3uOw9aOkmtEuCmI7uRRqtGhpa5KS0MDM3fykHA==')).decode()
authPasswd = (f.decrypt(b'')).decode()#Not Provided for Security Purposes
authDb = authUser

authEmail = (f.decrypt(b'gAAAAABfyNKiBYnP1CTJEo8S4rl60_0BbpLg8YMBAp4PjA4A9zoyjM1tUGfUTQ7N5PnqVzs6uQkPvVk6mKJF1rr8MpX9aV0ZohQoUoWm7JT0ooyHeZwdu2s=')).decode()
authEmailPasswd = (f.decrypt(b'')).decode()#Not Provided for Security Purposes