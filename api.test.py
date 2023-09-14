from src.api import ServerAPI

api = ServerAPI()
api.server.clear_server()
api.create_user("user1", "pass1")
api.create_camera("cam1", "user1")
api.upload_photo("test.png", "cam1", "user1")
print(api.get_images(-1, "user1", "cam1"))