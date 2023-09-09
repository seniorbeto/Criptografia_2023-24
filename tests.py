import uuid
from src.system import server

sys = server.Server()
sys.create_user('user1', 'pass1')
sys.create_user('user2', 'pass2')
