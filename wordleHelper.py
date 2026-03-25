# WORDLE HELPER GUI
# Zaheer Dhalla

import tkinter as tk
from tkinter import ttk, messagebox
import json


class WordleHelperGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Wordle Helper")
        self.root.resizable(False, False)

        # Load words
        with open("5letterWords.json", "r") as f:
            self.five_letter_words = json.load(f)

        # Track out of place letters across iterations
        self.out_of_place_letters = [[], [], [], [], []]

        self.setup_ui()

    def setup_ui(self):
        # Main frame
        main_frame = ttk.Frame(self.root, padding="20")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))

        # Title
        title_label = ttk.Label(main_frame, text="Wordle Helper", font=("Helvetica", 18, "bold"))
        title_label.grid(row=0, column=0, columnspan=2, pady=(0, 20))

        # Known letters input
        ttk.Label(main_frame, text="Known Letters (position + letter, . for unknown):").grid(row=1, column=0, sticky=tk.W, pady=5)
        self.known_entry = ttk.Entry(main_frame, width=10, font=("Helvetica", 14))
        self.known_entry.grid(row=1, column=1, pady=5)
        self.known_entry.insert(0, ".....")

        # Used letters input
        ttk.Label(main_frame, text="Used Letters (in word, position unknown, . for gaps):").grid(row=2, column=0, sticky=tk.W, pady=5)
        self.used_entry = ttk.Entry(main_frame, width=10, font=("Helvetica", 14))
        self.used_entry.grid(row=2, column=1, pady=5)

        # Excluded letters input
        ttk.Label(main_frame, text="Excluded Letters (not in word):").grid(row=3, column=0, sticky=tk.W, pady=5)
        self.excluded_entry = ttk.Entry(main_frame, width=10, font=("Helvetica", 14))
        self.excluded_entry.grid(row=3, column=1, pady=5)

        # Buttons frame
        buttons_frame = ttk.Frame(main_frame)
        buttons_frame.grid(row=4, column=0, columnspan=2, pady=15)

        self.find_button = ttk.Button(buttons_frame, text="Find Words", command=self.find_words)
        self.find_button.grid(row=0, column=0, padx=5)

        self.reset_button = ttk.Button(buttons_frame, text="Reset", command=self.reset)
        self.reset_button.grid(row=0, column=1, padx=5)

        # Results area
        ttk.Label(main_frame, text="Potential Words:", font=("Helvetica", 12, "bold")).grid(row=5, column=0, sticky=tk.W, pady=(10, 5))

        # Results listbox with scrollbar
        results_frame = ttk.Frame(main_frame)
        results_frame.grid(row=6, column=0, columnspan=2, sticky=(tk.W, tk.E, tk.N, tk.S), pady=5)

        self.results_listbox = tk.Listbox(results_frame, height=15, width=40, font=("Helvetica", 12))
        self.results_listbox.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        scrollbar = ttk.Scrollbar(results_frame, orient=tk.VERTICAL, command=self.results_listbox.yview)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.results_listbox.config(yscrollcommand=scrollbar.set)

        # Count label
        self.count_label = ttk.Label(main_frame, text="", font=("Helvetica", 10))
        self.count_label.grid(row=7, column=0, columnspan=2, pady=5)

        # Status bar for out-of-place letters
        self.status_label = ttk.Label(main_frame, text="", font=("Helvetica", 9), foreground="blue")
        self.status_label.grid(row=8, column=0, columnspan=2, pady=(5, 0))

    def find_words(self):
        known = self.known_entry.get().lower()
        used_letters = self.used_entry.get().lower()
        excluded_letters = self.excluded_entry.get().lower()

        # Validate input
        if len(known) != 5:
            messagebox.showerror("Invalid Input", "Known letters must be exactly 5 characters.")
            return

        # Build known positions dict
        known_positions = {}
        for index, letter in enumerate(known):
            if letter != '.':
                known_positions[index] = letter

        potential_words = []

        for word in self.five_letter_words:
            valid = True

            # Check used letters and out-of-place tracking
            for i in range(len(used_letters)):
                if used_letters[i] not in word and used_letters[i] != '.':
                    valid = False

                if used_letters[i] != '.':
                    if used_letters[i] not in self.out_of_place_letters[i]:
                        self.out_of_place_letters[i].append(used_letters[i])

                if word[i] in self.out_of_place_letters[i]:
                    valid = False

            # Check excluded letters
            for letter in excluded_letters:
                if letter in word:
                    valid = False

            # Check known positions
            for key, letter in known_positions.items():
                if word[key] != letter:
                    valid = False

            if valid:
                potential_words.append(word)

        # Update results
        self.results_listbox.delete(0, tk.END)
        for word in potential_words:
            self.results_listbox.insert(tk.END, word.upper())

        self.count_label.config(text=f"{len(potential_words)} words found")
        

    def reset(self):
        """Reset all state and clear the UI."""
        self.out_of_place_letters = [[], [], [], [], []]
        self.known_entry.delete(0, tk.END)
        self.known_entry.insert(0, ".....")
        self.used_entry.delete(0, tk.END)
        self.excluded_entry.delete(0, tk.END)
        self.results_listbox.delete(0, tk.END)
        self.count_label.config(text="")
        self.status_label.config(text="")


def main():
    root = tk.Tk()
    app = WordleHelperGUI(root)
    root.mainloop()


if __name__ == "__main__":
    main()
