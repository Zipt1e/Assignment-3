import tkinter as tk
from tkinter import ttk, messagebox
from googletrans import Translator, LANGUAGES
from gtts import gTTS
from pygame import mixer
import io

# Create a class for the Translator Application
class TranslatorApp(tk.Tk):
    def __init__(self):
        super().__init__()  # Initialize the main application window
        self.title("Universal Translator")  # Set the window title
        self.geometry("850x300")  # Set the window size
        self.configure(bg='#333333')  # Set the background color

        self.translator = Translator()  # Create a Translator object
        mixer.init()  # Initialize audio mixer for text-to-speech

        # Configure the style for buttons
        self.style = ttk.Style(self)
        self.style.configure('TButton', font=('Arial', 10), background='#4CAF50')  # Button styling

        self.create_widgets()  # Call a method to create UI elements
        self.create_decorative_panel()  # Placeholder for decorative elements

    # Method to create UI elements
    def create_widgets(self):
        # Source language selection
        self.src_lang_label = tk.Label(self, text="From Language:", bg='#333333', fg='#FFFFFF', font=("Arial", 12))
        self.src_lang_label.grid(row=0, column=0, padx=10, pady=10, sticky='w')  # Set position on the grid

        # Source language dropdown
        self.src_lang_var = tk.StringVar(self)
        self.src_languages = ['Auto-detect'] + sorted(list(LANGUAGES.values()))
        self.src_lang_dropdown = ttk.Combobox(self, textvariable=self.src_lang_var, values=self.src_languages, state="readonly", width=18)
        self.src_lang_dropdown.set("Auto-detect")  # Default to auto-detection
        self.src_lang_dropdown.grid(row=0, column=1, padx=10, pady=10, sticky='w')

        # Input text area
        self.input_text = tk.Text(self, height=10, width=50, bg="#484848", fg="#FFFFFF")  # Text area styling
        self.input_text.grid(row=1, column=0, columnspan=2, padx=10, pady=10)

        # Target language selection
        self.target_lang_label = tk.Label(self, text="To Language:", bg='#333333', fg='#FFFFFF', font=("Arial", 12))
        self.target_lang_label.grid(row=0, column=2, padx=10, pady=10, sticky='w')

        # Target language dropdown
        self.target_lang_var = tk.StringVar(self)
        self.target_languages = sorted(list(LANGUAGES.values()))
        self.target_lang_dropdown = ttk.Combobox(self, textvariable=self.target_lang_var, values=self.target_languages, state="readonly", width=18)
        self.target_lang_dropdown.grid(row=0, column=3, padx=10, pady=10, sticky='w')

        # Translated text area
        self.output_text = tk.Text(self, height=10, width=50, bg="#484848", fg="#FFFFFF")
        self.output_text.grid(row=1, column=2, columnspan=2, padx=10, pady=10)

        # Translate button
        self.translate_button = ttk.Button(self, text="Translate", command=self.translate_text, style='TButton')
        self.translate_button.grid(row=2, column=0, padx=10, pady=10, sticky='ew')

        # Speak button
        self.speak_button = ttk.Button(self, text="Speak Translation", command=self.speak_translated_text, style='TButton')
        self.speak_button.grid(row=2, column=1, padx=10, pady=10, sticky='ew')

        # Clear button
        self.clear_button = ttk.Button(self, text="Clear Texts", command=self.clear_texts, style='TButton')
        self.clear_button.grid(row=2, column=2, padx=10, pady=10, sticky='ew')

    # Method to translate text
    def translate_text(self):
        input_text = self.input_text.get("1.0", "end-1c").strip()
        src_lang = 'auto' if self.src_lang_var.get() == 'Auto-detect' else list(LANGUAGES.keys())[list(LANGUAGES.values()).index(self.src_lang_var.get().lower())]
        target_lang = list(LANGUAGES.keys())[list(LANGUAGES.values()).index(self.target_lang_var.get().lower())]
        if not input_text:
            messagebox.showerror("Error", "Please enter text to translate.")
            return
        translated_text = self.translator.translate(input_text, src=src_lang, dest=target_lang).text
        self.output_text.delete("1.0", tk.END)  # Clear output text area
        self.output_text.insert(tk.END, translated_text)  # Display translated text

    # Method to speak translated text
    def speak_translated_text(self):
        translated_text = self.output_text.get("1.0", "end-1c").strip()
        target_lang = list(LANGUAGES.keys())[list(LANGUAGES.values()).index(self.target_lang_var.get().lower())]
        if translated_text:
            try:
                tts = gTTS(text=translated_text, lang=target_lang, slow=False)
                fp = io.BytesIO()
                tts.write_to_fp(fp)
                fp.seek(0)
                mixer.music.load(fp)
                mixer.music.play()
                while mixer.music.get_busy():
                    self.update()
            except Exception as e:
                messagebox.showerror("Text-to-Speech Error", str(e))

    # Method to clear text areas
    def clear_texts(self):
        self.input_text.delete("1.0", tk.END)  # Clear input text area
        self.output_text.delete("1.0", tk.END)  # Clear output text area

    # Method to create decorative elements (placeholder)
    def create_decorative_panel(self):
        # This method can be used to add decorative elements if needed
        pass

if __name__ == "__main__":
    app = TranslatorApp()  # Create an instance of the TranslatorApp class
    app.mainloop()  # Start the main event loop
