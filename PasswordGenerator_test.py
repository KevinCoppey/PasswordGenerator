import unittest
from unittest.mock import patch, MagicMock
from main import PasswordGeneratorApp  # Adjust import if needed

class TestPasswordGeneratorApp(unittest.TestCase):
    
    @classmethod
    def setUpClass(cls):
        # Initialize the app instance for all tests
        cls.app = PasswordGeneratorApp()

    @patch('tkinter.Tk', autospec=True)
    @patch('tkinter.Frame', autospec=True)
    @patch('tkinter.Label', autospec=True)
    @patch('tkinter.Button', autospec=True)
    def setUp(self, MockButton, MockLabel, MockFrame, MockTk):
        # Create instances of the mocked classes
        self.mock_tk = MockTk.return_value
        self.mock_frame = MockFrame.return_value
        self.mock_label = MockLabel.return_value
        self.mock_button = MockButton.return_value

        # Replace tkinter components with mocks in the app instance
        self.app.master = self.mock_tk
        self.app.frame1 = self.mock_frame
        self.app.label1 = self.mock_label
        self.app.generate_button = self.mock_button
        self.app.copy_button = self.mock_button
        
        # Set up mock behavior if needed
        self.mock_tk.configure_mock(**{'title.return_value': None})

    def test_generate_password_uppercase(self):
        """Test if password generation includes uppercase letters when checkbox is selected."""
        password = self.app.generate_password(10, True, False, False, False)
        self.assertTrue(any(c.isupper() for c in password))
        self.assertEqual(len(password), 10)

    def test_generate_password_lowercase(self):
        """Test if password generation includes lowercase letters when checkbox is selected."""
        password = self.app.generate_password(10, False, True, False, False)
        self.assertTrue(any(c.islower() for c in password))
        self.assertEqual(len(password), 10)

    def test_generate_password_numbers(self):
        """Test if password generation includes numbers when checkbox is selected."""
        password = self.app.generate_password(10, False, False, True, False)
        self.assertTrue(any(c.isdigit() for c in password))
        self.assertEqual(len(password), 10)

    def test_generate_password_symbols(self):
        """Test if password generation includes symbols when checkbox is selected."""
        password = self.app.generate_password(10, False, False, False, True)
        self.assertTrue(any(c in "!@#$%^&*(),.?\":{}|<>" for c in password))
        self.assertEqual(len(password), 10)

    def test_password_strength_weak(self):
        """Test the strength evaluation for a weak password."""
        password = "abc123"
        strength = self.app.evaluate_password_strength(password)
        self.assertEqual(strength, "WEAK")

    def test_password_strength_medium(self):
        """Test the strength evaluation for a medium password."""
        password = "abc123XYZ"
        strength = self.app.evaluate_password_strength(password)
        self.assertEqual(strength, "MEDIUM")

    def test_password_strength_high(self):
        """Test the strength evaluation for a high-strength password."""
        password = ",Lg@9IfxVLTg}.4+JSP4"
        strength = self.app.evaluate_password_strength(password)
        self.assertEqual(strength, "HIGH")

    @patch('pyperclip.copy')
    def test_clear_clipboard(self, mock_copy):
        """Test if the clipboard is cleared after a delay."""
        self.app.clear_clipboard()
        mock_copy.assert_called_once_with("")

    @patch('main.Notification')
    @patch('main.Image.open')
    @patch('main.ImageTk.PhotoImage')
    def test_show_notification(self, mock_image_tk, mock_image_open, mock_notification):
        """Test the show notification functionality."""
        mock_img_instance = MagicMock()
        mock_image_open.return_value = mock_img_instance
        mock_image_tk.return_value = mock_img_instance
        
        self.app.show_notification("Test notification", "success.png", (0, 0), (10, 10), ("Helvetica", 12), 20)
        
        mock_notification.assert_called_once()
        mock_notification.return_value.show_animation.assert_called_once()

if __name__ == '__main__':
    unittest.main()
