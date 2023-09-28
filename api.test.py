from src.api import ServerAPI
import datetime

api = ServerAPI()
api.server.clear_server()

api.register("user1", "pass1")
api.register("user2", "pass2")

api.login("user1", "pass1")
api.upload_photo("test.png")

api.login("user2", "pass2")
api.upload_photo("test.png")

api.logout()

print("sacando imagenes genericas")
print(api.get_images(10))
print("     De user1: ", api.get_images(10))

print("logeando a user1")
api.login("user1", "pass1")
now = datetime.datetime.now()
print("     Del dia de hoy del usuario", api.get_images(10, date=now.strftime("%Y/%m/%d")))

