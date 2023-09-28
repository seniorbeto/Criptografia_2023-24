from src.api import ServerAPI

api = ServerAPI()
api.server.clear_server()

api.register("user1", "pass1")
api.register("user2", "pass2")

api.login("user1", "pass1")
api.upload_photo("test.png")

api.login("user2", "pass2")
api.upload_photo("test.png")

api.logout()
api.upload_photo("test.png")