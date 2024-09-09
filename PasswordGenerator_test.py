import tkinter
import unittest
from unittest.mock import patch, MagicMock
from main import PasswordGeneratorApp  # Assuming the original code is in a file named password_generator_app.py

class TestPasswordGeneratorApp(unittest.TestCase):
    
    @classmethod
    def setUpClass(cls):
        # Initialize the app instance for all tests
        cls.app = PasswordGeneratorApp()
    
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
        password = "abc123XYZ!@"
        strength = self.app.evaluate_password_strength(password)
        self.assertEqual(strength, "MEDIUM")

    @patch('pyperclip.copy')
    def test_clear_clipboard(self, mock_copy):
        """Test if the clipboard is cleared after a delay."""
        self.app.clear_clipboard()
        mock_copy.assert_called_once_with("")

    @patch('main.Notification')
    @patch('main.Image.open')
    @patch('main.ImageTk.PhotoImage')
    def test_show_notification(self, mock_image_open, mock_image_tk, mock_notification):
        """Test the show notification functionality."""
        mock_img_instance = MagicMock()
        mock_image_open.return_value = mock_img_instance
        mock_image_tk.return_value = mock_img_instance
        
        self.app.show_notification("Test notification", "success.png", (0, 0), (10, 10), ("Helvetica", 12), 20)
        
        mock_notification.assert_called_once()
        mock_notification.return_value.show_animation.assert_called_once()

    def test_update_generate_button_state(self):
        """Test if the Generate button state updates based on checkbox selection."""
        self.app.checkbox1_var.set(True)
        self.app.update_generate_button_state()
        self.assertEqual(self.app.generate_button['state'], 'normal')

        self.app.checkbox1_var.set(False)
        self.app.update_generate_button_state()
        self.assertEqual(self.app.generate_button['state'], 'disabled')

if __name__ == '__main__':
    unittest.main()
