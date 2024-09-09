import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk
import pyperclip as pyclip
import string
import re
import secrets

NOTIFICATION_HIDE_AFTER = 1000
CLEAR_CLIPBOARD_AFTER = 60000

class Notification(tk.Frame):
    def __init__(self, master, width, height, bg, image, text, img_pad, text_pad, font, y_pos):
        super().__init__(master, bg=bg, width=width, height=height)
        self.pack_propagate(0)
        
        self.y_pos = y_pos
        self.master = master
        self.width = width

        right_offset = 8
        self.cur_x = self.master.winfo_width()
        self.x = self.cur_x - (self.width + right_offset)

        img_label = tk.Label(self, image=image, bg=bg)
        img_label.image = image
        img_label.pack(side="left", padx=img_pad[0])

        message = tk.Label(self, text=text, font=font, bg=bg, fg="black")
        message.pack(side="left", padx=text_pad[0])

        self.place(x=self.cur_x, y=self.y_pos)

        # Schedule the notification to hide after 3 seconds
        self.hide_after = NOTIFICATION_HIDE_AFTER
        self.after(self.hide_after, self.hide_animation)

        # Update position during window resize
        self.master.bind("<Configure>", self.update_position)

    def show_animation(self):
        if self.cur_x > self.x:
            self.cur_x -= 1
            self.place(x=self.cur_x, y=self.y_pos)
            self.after(5, self.show_animation)


    def hide_animation(self):
        if self.cur_x < self.master.winfo_width():
            self.cur_x += 1
            self.place(x=self.cur_x, y=self.y_pos)
            self.after(1, self.hide_animation)
        else:
            self.master.unbind("<Configure>")  # Unbind the event
            self.destroy()

    
    def update_position(self, event=None):
        self.x = self.master.winfo_width() - (self.width + 8)
        self.place(x=self.x, y=self.y_pos)


class PasswordGeneratorApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Password Generator")
        self.eval('tk::PlaceWindow . center')
        self.geometry("500x600")
        self.configure(bg='#2E073F')
        self.minsize(500, 600)
        
        self.animation_in_progress = False
        self.frame1 = None
        
        self.create_widgets()

    def create_widgets(self):
        # Frame 2 = Counter and Slider
        self.frame2 = tk.Frame(self, bg="#7A1CAC")
        self.frame2.pack(fill=tk.BOTH, expand=True, pady=20, padx=20)

        # Create a Frame to hold the labels and slider
        self.inner_frame = tk.Frame(self.frame2, bg="#7A1CAC")
        self.inner_frame.pack(fill=tk.X, expand=True)

        self.label2 = tk.Label(self.inner_frame, text="Character Length", bg="#7A1CAC", fg="white")
        self.label2.pack(side=tk.LEFT, padx=20)

        self.counter_label = tk.Label(self.inner_frame, text="8", bg="#7A1CAC", fg="white")
        self.counter_label.pack(side=tk.RIGHT, padx=20)

        self.slider = ttk.Scale(self.frame2, orient="horizontal", command=self.update_counter, from_=int(self.counter_label.cget("text")), to=20)
        self.slider.set(8)
        self.slider.pack(side=tk.TOP, fill=tk.X, padx=20, pady=10)

        # Frame for checkboxes
        self.checkbox_frame = tk.Frame(self.frame2, bg="#7A1CAC")
        self.checkbox_frame.pack(side=tk.TOP, fill=tk.X, pady=(10, 0))

        # Configure grid in checkbox_frame
        self.checkbox_frame.columnconfigure(0, weight=1, uniform="checkbox")
        self.checkbox_frame.columnconfigure(1, weight=3, uniform="label")

        # Variables for checkboxes
        self.checkbox1_var = tk.BooleanVar(value=False)
        self.checkbox2_var = tk.BooleanVar(value=False)
        self.checkbox3_var = tk.BooleanVar(value=False)
        self.checkbox4_var = tk.BooleanVar(value=False)

        # Create checkboxes and labels
        self.checkbox1_label, _ = self.create_checkbox(self.checkbox_frame, self.checkbox1_var, "Include Uppercase Letters", 0,)
        self.checkbox2_label, _ = self.create_checkbox(self.checkbox_frame, self.checkbox2_var, "Include Lowercase Letters", 1)
        self.checkbox3_label, _ = self.create_checkbox(self.checkbox_frame, self.checkbox3_var, "Include Numbers", 2)
        self.checkbox4_label, _ = self.create_checkbox(self.checkbox_frame, self.checkbox4_var, "Include Symbols", 3)

        # Bind checkbox updates to a method that checks if any are selected
        self.checkbox1_var.trace_add("write", self.update_generate_button_state)
        self.checkbox2_var.trace_add("write", self.update_generate_button_state)
        self.checkbox3_var.trace_add("write", self.update_generate_button_state)
        self.checkbox4_var.trace_add("write", self.update_generate_button_state)

        # Frame for password strength with border
        self.strength_frame = tk.Frame(self.frame1, bg="#7A1CAC", relief="solid", borderwidth=2)

        # Create labels for password strength with adjusted color for opacity effect
        self.strength_label = tk.Label(self.strength_frame, text="Strength", fg="lightgray", bg="#7A1CAC")
        self.strength_label.pack(side=tk.LEFT, padx=20, pady=5)

        # Create dot indicators for strength next to the strength label
        self.dots = []
        for i in range(3):
            dot = tk.Label(self.strength_frame, text="●", fg="gray", bg="#7A1CAC", font=("", 12))
            dot.pack(side=tk.RIGHT, padx=2, pady=5)
            self.dots.append(dot)

        self.strength_value = tk.Label(self.strength_frame, text="WEAK", fg="white", bg="#7A1CAC")
        self.strength_value.pack(side=tk.RIGHT, padx=20, pady=5)

        # Create the Generate button
        self.generate_button = tk.Button(self.frame2, text="Generate", command=self.on_generate_click, highlightbackground="#7A1CAC")
        self.generate_button.pack(side=tk.BOTTOM, pady=10, fill=tk.X, padx=10)

        # Initially disable the Generate button since no checkbox is selected
        self.generate_button.config(state=tk.DISABLED)

        # Bind the resize functions to the <Configure> events of the frames
        self.frame2.bind("<Configure>", self.resize_widgets_frame2)

    def create_checkbox(self, frame, var, text, row):
        checkbox = tk.Checkbutton(frame, variable=var, bg="#7A1CAC", fg="white", activebackground="#5B3A9B")
        checkbox.grid(row=row, column=0, sticky="w", padx=10, pady=5)
        label = tk.Label(frame, text=text, bg="#7A1CAC", fg="white")
        label.grid(row=row, column=1, sticky="w", padx=10, pady=5)
        return checkbox, label

    def resize_widgets_frame2(self, event):
        """Resize text and widgets in frame2 based on window size."""
        new_font_size = min(self.frame2.winfo_width() // 20, self.frame2.winfo_height() // 20)
        new_font_size = max(new_font_size, 10)
        
        self.label2.config(font=("", new_font_size))
        self.counter_label.config(font=("", new_font_size))
        self.update_checkbox_fonts(new_font_size)
        self.update_strength_fonts(new_font_size)
        self.update_button_font(new_font_size)

    def update_generate_button_state(self, *args):
        """Enable or disable the Generate button based on checkbox states and change the cursor."""
        if any([self.checkbox1_var.get(), self.checkbox2_var.get(), self.checkbox3_var.get(), self.checkbox4_var.get()]):
            self.generate_button.config(state=tk.NORMAL, cursor="hand2")  # Enable button and set cursor to hand2
        else:
            self.generate_button.config(state=tk.DISABLED, cursor="arrow")  # Disable button

    def create_frame1(self):
        """Create and configure frame1."""
        self.frame1 = tk.Frame(self, bg="#7A1CAC")
        self.frame1.pack(fill=tk.BOTH, expand=True, pady=20, padx=20)

        # Configure grid in frame1
        self.frame1.columnconfigure(0, weight=1)  # Password label will stick to the left
        self.frame1.columnconfigure(1, weight=0)  # Copy button will stick to the right

        # Create the password label
        self.label1 = tk.Label(self.frame1, text="", bg="#7A1CAC", fg="white", font=("Helvetica", 30))
        self.label1.grid(row=0, column=0, padx=(10, 0), pady=10, sticky="w")

        # Create the copy button
        self.copy_image = Image.open("copy.png")
        self.copy_image = self.copy_image.resize((30, 30), Image.Resampling.LANCZOS)
        self.copy_image = ImageTk.PhotoImage(self.copy_image)
        
        self.copy_button = tk.Label(self.frame1, image=self.copy_image, bg="#7A1CAC")
        self.copy_button.bind("<Button-1>", self.on_image_click)
        self.copy_button.grid(row=0, column=1, padx=(0, 10), pady=10, sticky="e")  # Align to the right and add padding

        # Bind cursor change on hover
        self.copy_button.bind("<Enter>", self.on_copy_hover)
        self.copy_button.bind("<Leave>", self.on_copy_leave)
        
        self.strength_frame.pack(side=tk.TOP, fill=tk.X, pady=20, padx=20)

        self.frame1.bind("<Configure>", self.align_center)

    def on_copy_hover(self, event):
        """Change cursor to hand2 when hovering over the copy button."""
        self.copy_button.config(cursor="hand2")

    def on_copy_leave(self, event):
        """Change cursor back to default when leaving the copy button."""
        self.copy_button.config(cursor="")


    def align_center(self, event=None):
        """Align password label and copy button to the center vertically."""
        self.frame1.update_idletasks()
        frame1_height = self.frame1.winfo_height()
        label1_height = self.label1.winfo_height()
        copy_button_height = self.copy_button.winfo_height()
        max_height = max(label1_height, copy_button_height)
        extra_padding = (frame1_height - max_height) // 2

        self.label1.grid_configure(pady=(extra_padding, 10))
        self.copy_button.grid_configure(pady=(extra_padding, 10))

    def update_counter(self, value):
        """Update the counter label based on the slider value."""
        self.counter_label.config(text=str(int(float(value))))

    def update_checkbox_fonts(self, font_size):
        """Update font size for checkboxes."""
        for checkbox in [self.checkbox1_label, self.checkbox2_label, self.checkbox3_label, self.checkbox4_label]:
            checkbox.config(font=("", font_size))
    
    def update_strength_fonts(self, font_size):
        """Update font size for strength indicators."""
        self.strength_label.config(font=("", font_size))
        for dot in self.dots:
            dot.config(font=("", font_size))
        self.strength_value.config(font=("", font_size))
    
    def update_button_font(self, font_size):
        """Update font size for the Generate button."""
        self.generate_button.config(font=("", font_size))
    
    def on_image_click(self, event):
        """Handle the copy button click event."""
        password = self.label1.cget("text")
        if password:
            pyclip.copy(password)
            self.show_notification("Password copied to clipboard!", "success.png", (0, 0), (10, 10), ("Helvetica", 12), self.winfo_height() - 80)
        
        # Clear the clipboard after 5 seconds
        self.after(CLEAR_CLIPBOARD_AFTER, self.clear_clipboard)
    
    def clear_clipboard(self):
        """Clear the clipboard content."""
        pyclip.copy("")  # Clear clipboard by copying an empty string
    
    def show_notification(self, text, image_path, img_pad, text_pad, font, y_pos):
        """Display a notification on the screen at the top-right corner."""
        img = Image.open(image_path)
        img = ImageTk.PhotoImage(img.resize((30, 30), Image.Resampling.LANCZOS))
        
        # Call the Notification class and place it at the top-right corner
        Notification(self, 300, 50, "white", img, text, img_pad, text_pad, font, 20).show_animation()  # y_pos = 20 for top-right corner

    
    def on_generate_click(self):
        """Handle the click event on the generate button."""
        if self.frame1 is None:
            # Create frame1 only when Generate is clicked
            self.create_frame1()

        length = int(self.slider.get())
        include_uppercase = self.checkbox1_var.get()
        include_lowercase = self.checkbox2_var.get()
        include_numbers = self.checkbox3_var.get()
        include_symbols = self.checkbox4_var.get()
        
        password = self.generate_password(length, include_uppercase, include_lowercase, include_numbers, include_symbols)
        self.label1.config(text=password)
        self.update_password_strength(self.evaluate_password_strength(password))
        
        print("Generate button clicked! New password:", password)

    def generate_password(self, length, uppercase, lowercase, numbers, symbols):
        """Generate a random password based on selected criteria."""
        if length < 1:
            return ""

        character_set = ""
        password = []

        # Ensure at least one character from each selected category
        if uppercase:
            password.append(secrets.choice(string.ascii_uppercase))
            character_set += string.ascii_uppercase
        if lowercase:
            password.append(secrets.choice(string.ascii_lowercase))
            character_set += string.ascii_lowercase
        if numbers:
            password.append(secrets.choice(string.digits))
            character_set += string.digits
        if symbols:
            password.append(secrets.choice(string.punctuation))
            character_set += string.punctuation

        # Add remaining characters to meet the desired length
        while len(password) < length:
            password.append(secrets.choice(character_set))

        # Shuffle the password list to prevent predictable order
        secrets.SystemRandom().shuffle(password)

        return ''.join(password)


    def evaluate_password_strength(self, password):
        """Evaluate the strength of the generated password."""
        # Check for presence of different types of characters
        has_uppercase = bool(re.search(r'[A-Z]', password))
        has_lowercase = bool(re.search(r'[a-z]', password))
        has_digit = bool(re.search(r'[0-9]', password))
        has_symbol = bool(re.search(r'[!@#$%^&*(),.?":{}|<>]', password))
        
        # Count the types of characters present
        character_types = sum([has_uppercase, has_lowercase, has_digit, has_symbol])
        
        # Determine password strength based on character types and length
        if len(password) >= 12 and character_types == 4:
            return "HIGH"
        elif len(password) >= 9 and character_types >= 3:
            return "MEDIUM"
        else:
            return "WEAK"

    def update_password_strength(self, strength):
        """Update the password strength indicators based on the strength."""
        # Define the color and text for each strength level
        strength_levels = {
            "WEAK": ("red", 1),
            "MEDIUM": ("orange", 2),
            "HIGH": ("green", 3)
        }

        # Set the color and text for each dot based on strength level
        color, count = strength_levels.get(strength, ("gray", 0))

        for i, dot in enumerate(self.dots):
            if i < count:
                dot.config(fg=color)
            else:
                dot.config(fg="gray")
        
        # Update the strength label text
        self.strength_value.config(text=strength)

if __name__ == "__main__":
    app = PasswordGeneratorApp()
    app.mainloop()
