import unittest
from unittest.mock import patch, mock_open, MagicMock
import AutoDUCKS as ducks


class TestAutoDUCKS(unittest.TestCase):

    def test_readConfig_returns_dict(self):
        mock_csv = "numberoftimes,5\ncount,100\nfilename,testfile\n"

        with patch("builtins.open", mock_open(read_data=mock_csv)):
            config = ducks.readConfig("AutoMateConfig.csv")

        self.assertIsInstance(config, dict)
        self.assertEqual(config["numberoftimes"], "5")

        self.assertEqual(config.get("filename"), "testfile")

    def test_lastConfigUsed_writes_csv(self):
        config = {
            "numberoftimes": 3,
            "count": 500,
            "filename": "run_test",
            "filepath": "C:/data"
        }

        with patch("builtins.open", mock_open()) as mocked_file:
            ducks.lastConfigUsed(config)

            mocked_file.assert_called_once_with(
                "userConfig.csv", mode="w", newline=""
            )

            handle = mocked_file()

            self.assertTrue(handle.write.called)
            self.assertGreaterEqual(handle.write.call_count, 2)

    @patch("pytesseract.image_to_string")
    @patch("pyautogui.screenshot")
    def test_getNumberFromScreen_parses_digits(self, mock_screenshot, mock_ocr):
        fake_image = MagicMock()
        fake_image.convert.return_value = fake_image

        mock_screenshot.return_value = fake_image
        mock_ocr.return_value = "Count: 12345"

        result = ducks.getNumberFromScreen((0, 0, 100, 100))

        self.assertEqual(result, 12345)
        self.assertIsInstance(result, int)

    @patch("pyautogui.locateCenterOnScreen")
    def test_scrCoor_finds_coordinates(self, mock_locate):
        mock_locate.return_value = (100, 200)

        coords = ducks.scrCoor("test.png")

        self.assertEqual(coords, (100, 200))
        self.assertIsNotNone(coords)

    @patch("pyautogui.click")
    @patch("pyautogui.write")
    @patch("pyautogui.hotkey")
    @patch("pyautogui.press")
    @patch("time.sleep")
    @patch.object(ducks, "getNumberFromScreen")
    @patch.object(ducks, "scrCoor")
    def test_executeProgram_runs_one_cycle(
        self,
        mock_scrCoor,
        mock_getNumber,
        mock_sleep,
        mock_press,
        mock_hotkey,
        mock_write,
        mock_click
    ):
        mock_getNumber.return_value = 100
        mock_scrCoor.side_effect = [(50, 50), (60, 60), (70, 70)]

        ducks.executeProgram(
            numberOfTimes=1,
            count=50,
            fileName="test",
            region=(0, 0, 10, 10),
            filepath="/tmp"
        )

        self.assertTrue(mock_click.called)
        self.assertTrue(mock_write.called)


if __name__ == "__main__":
    unittest.main()
