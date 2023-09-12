import unittest
from src.system import *

class TestServer(unittest.TestCase):
    def setUp(self):
        self.server = Server()
        self.server.delete_all_users()
        self.server.delete_all_cameras()
        self.server.create_user("user1", "password1")
        self.server.create_user("user2", "password2")
        self.server.create_camera("camera1", "user1")
        self.server.create_camera("camera2", "user2")

    def test_create_user(self):
        self.server.create_user("user3", "password3")
        self.assertEqual(len(self.server._Server__users), 3)
        self.assertEqual(self.server._Server__users[2].name, "user3")
        self.assertEqual(self.server._Server__users[2].password, "password3")

    def test_create_user_already_exists(self):
        with self.assertRaises(ValueError):
            self.server.create_user("user1", "password1")

    def test_create_camera(self):
        self.server.create_camera("camera3", "user1")
        self.assertEqual(len(self.server._Server__cameras), 3)
        self.assertEqual(self.server._Server__cameras[2].name, "camera3")
        self.assertEqual(self.server._Server__cameras[2].owner, "user1")

    def test_create_camera_already_exists(self):
        with self.assertRaises(ValueError):
            self.server.create_camera("camera1", "user1")

    def test_create_camera_invalid_owner(self):
        with self.assertRaises(ValueError):
            self.server.create_camera("camera3", "user3")

    def test_remove_camera(self):
        self.server.remove_camera("camera1", "user1")
        self.assertEqual(len(self.server._Server__cameras), 1)
        self.assertEqual(self.server._Server__cameras[0].name, "camera2")
        self.assertEqual(self.server._Server__cameras[0].owner, "user2")

    def test_remove_camera_not_found(self):
        with self.assertRaises(ValueError):
            self.server.remove_camera("camera3", "user1")

    def test_remove_camera_invalid_owner(self):
        with self.assertRaises(ValueError):
            self.server.remove_camera("camera1", "user2")

    def test_remove_user(self):
        self.server.remove_user("user1", "password1")
        self.assertEqual(len(self.server._Server__users), 1)
        self.assertEqual(self.server._Server__users[0].name, "user2")
        self.assertEqual(self.server._Server__users[0].password, "password2")

    def test_remove_user_not_found(self):
        with self.assertRaises(ValueError):
            self.server.remove_user("user3", "password3")

    def test_remove_user_wrong_password(self):
        with self.assertRaises(ValueError):
            self.server.remove_user("user1", "password2")

if __name__ == '__main__':
    unittest.main()