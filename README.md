# Password Generator

# Your Project Name

![Build Status](https://img.shields.io/github/actions/workflow/status/KevinCoppey/PasswordGenerator/python-app.yml?branch=main)
![Python Version](https://img.shields.io/badge/python-3.10%20%7C%203.11%20%7C%203.12-blue)
![Flake8](https://img.shields.io/badge/code%20style-flake8-blue)
![License](https://img.shields.io/github/license/KevinCoppey/PasswordGenerator)
![GitHub Last Commit](https://img.shields.io/github/last-commit/KevinCoppey/PasswordGenerator)


## Overview

This project is a **Password Generator Application** built using `tkinter` for the GUI, `Pillow` for image handling, and `secrets` for generating secure random passwords. It allows users to generate passwords with custom lengths and character compositions, including uppercase letters, lowercase letters, numbers, and symbols. The app also provides features like password strength evaluation, clipboard copy functionality, and visual notifications.

### Features:
- Customizable password length (8-20 characters)
- Options to include/exclude uppercase, lowercase, numbers, and symbols
- Password strength evaluation (Weak, Medium, High)
- Copy password to clipboard with a single click
- Notifications for successful clipboard copy
- Clipboard clears automatically after 60 seconds

## Requirements

To run this application, you will need the following dependencies:

### Python Version:
- Python 3.x

### Python Packages:
- `tkinter` (for GUI)
- `Pillow` (for image handling)
- `pyperclip` (for clipboard operations)

You can install all the necessary Python packages by running the following command after setting up a virtual environment.

### Installing Required Libraries

```bash
pip install -r requirements.txt
```

### `requirements.txt`

```txt
Pillow==9.2.0
pyperclip==1.8.2
```

## Installation

1. Clone the repository to your local machine.

   ```bash
   git clone https://github.com/your-repo/password-generator.git
   ```

2. Navigate to the project directory.

   ```bash
   cd password-generator
   ```

3. **(Optional)** Create a virtual environment for the project.

   ```bash
   python -m venv venv
   ```

4. Activate the virtual environment:

   - **Windows:**
     ```bash
     venv\Scripts\activate
     ```
   - **macOS/Linux:**
     ```bash
     source venv/bin/activate
     ```

5. Install the required packages using the `requirements.txt` file.

   ```bash
   pip install -r requirements.txt
   ```

## Running the Application

Once the environment is set up and the dependencies are installed, you can run the application using the following command:

```bash
python main.py
```

## How to Use the Application

1. **Select Password Length**: Adjust the slider to set the password length between 8 and 20 characters.
2. **Character Options**: Check the boxes for including uppercase letters, lowercase letters, numbers, and symbols in the password.
3. **Generate Password**: Click the `Generate` button to create a new password. The password will be displayed at the top of the application.
4. **Copy to Clipboard**: Click the copy button next to the generated password to copy it to the clipboard. A notification will confirm the action, and the clipboard will clear after 60 seconds.
5. **Password Strength**: The strength of the generated password will be displayed using a label (Weak, Medium, or High) and color-coded dots.

## Customization

- **Notification Behavior**: You can adjust the duration for which the notification is shown and the clipboard clearing time by modifying the following variables:
  - `NOTIFICATION_HIDE_AFTER` (default: 1000 ms)
  - `CLEAR_CLIPBOARD_AFTER` (default: 60000 ms)

## Files and Folders

- **main.py**: The main application code
- **requirements.txt**: Lists all the necessary dependencies
- **copy.png, success.png**: Images used in the application for notifications and the copy button

## Known Issues

- **Image paths**: Ensure the images (`copy.png`, `success.png`) are located in the root folder or provide the correct path in the `show_notification` and `create_frame1` functions.

## License

This project is licensed under the Apache2 License.

---