import unittest
from app.config import Config

class TestConfig(unittest.TestCase):
    def test_resolution_mapping(self):
        # Kiểm tra resolution 480p
        Config.VIDEO_QUALITY = "480p"
        res = Config.get_video_resolution()
        self.assertEqual(res, (854, 480))

        # Kiểm tra resolution 720p
        Config.VIDEO_QUALITY = "720p"
        res = Config.get_video_resolution()
        self.assertEqual(res, (1280, 720))

    def test_color_parsing(self):
        # Kiểm tra parsing màu RGBA
        self.assertEqual(len(Config.TEXT_COLOR), 4)
        for val in Config.TEXT_COLOR:
            self.assertTrue(0 <= val <= 255)

if __name__ == '__main__':
    unittest.main()
