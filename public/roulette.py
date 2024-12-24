import tkinter as tk
from tkinter import messagebox, ttk
import random
import math
from time import time
from PIL import Image, ImageTk, ImageDraw

class ModernRouletteGUI:
    def __init__(self, root):
        self.root = root
        self.setup_window()
        self.initialize_game_variables()
        self.load_resources()
        self.create_gui_elements()
        
    def setup_window(self):
        """Set up the main window with a modern dark theme"""
        self.root.title("Premium Casino Roulette")
        # Set dark theme
        self.style = ttk.Style()
        self.style.theme_use('clam')
        self.style.configure(".", background="#1a1a1a", foreground="white")
        self.style.configure("TButton", padding=6, relief="flat", background="#2d2d2d")
        self.style.configure("TLabel", padding=6, background="#1a1a1a", foreground="white")
        self.style.configure("TFrame", background="#1a1a1a")
        self.root.geometry("1400x900")
        self.root.configure(bg="#1a1a1a")

    def initialize_game_variables(self):
        self.balance = 1000
        self.bet_amount = 0
        self.selected_chip = None
        self.spinning = False
        self.wheel_angle = 0
        self.ball_angle = 0
        self.ball_radius = 180
        self.spin_speed = 10
        self.ball_speed = 15
        self.slow_down_factor = 0.99
        self.numbers = [0, 32, 15, 19, 4, 21, 2, 25, 17, 34, 6, 27,
                       13, 36, 11, 30, 8, 23, 10, 5, 24, 16,
                       33, 1, 20, 14, 31, 9, 22, 18,
                       29, 7, 28, 12, 35, 3, 26]
        self.colors = ["green"] + ["red", "black"] * 18
        self.wheel_center = (250, 250)
        self.bets = []

    def load_resources(self):
        """Load images and other resources"""
        self.chip_images = {}
        chip_colors = {
            10: "blue",
            50: "purple",
            100: "black",
            200: "orange",
            500: "darkgoldenrod"
        }
        for value, color in chip_colors.items():
            image = Image.new("RGBA", (50, 50), (255, 255, 255, 0))
            draw = ImageDraw.Draw(image)
            draw.ellipse((0, 0, 50, 50), fill=color, outline="black")
            draw.text((25, 25), str(value), fill="white" if color != "white" else "black", anchor="mm")
            self.chip_images[value] = ImageTk.PhotoImage(image)

    def create_gui_elements(self):
        self.create_labels()
        main_frame = ttk.Frame(self.root)
        main_frame.pack(fill=tk.BOTH, expand=True)

        top_frame = ttk.Frame(main_frame, padding=10)
        top_frame.pack(side=tk.TOP, fill=tk.X, padx=20, pady=20)

        self.balance_label = ttk.Label(top_frame, 
                                    text=f"Kontostand: {self.balance} €",
                                    font=("Arial", 16))
        self.balance_label.pack(side=tk.LEFT, padx=10)
        
        self.bet_label = ttk.Label(top_frame,
                                text=f"Wetteinsatz: {self.bet_amount} €",
                                font=("Arial", 16))
        self.bet_label.pack(side=tk.LEFT, padx=10)
        
        self.result_label = ttk.Label(top_frame, text="",
                                   font=("Arial", 16))
        self.result_label.pack(side=tk.LEFT, padx=10)

        chip_frame = ttk.Frame(top_frame)
        chip_frame.pack(side=tk.RIGHT, padx=10)
        
        self.create_chips(chip_frame)

        main_content_frame = ttk.Frame(main_frame, padding=10)
        main_content_frame.pack(side=tk.TOP, fill=tk.BOTH, expand=True, padx=20, pady=20)

        canvas_frame = ttk.Frame(main_content_frame, padding=10)
        canvas_frame.pack(side=tk.LEFT, padx=20, pady=20)
        
        self.canvas = tk.Canvas(canvas_frame, width=500, height=500, 
                              bg="#1a1a1a", highlightthickness=0)
        self.canvas.pack()
        
        betting_frame = ttk.Frame(main_content_frame, padding=10)
        betting_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True, padx=20, pady=20)
        
        self.create_wheel()
        self.create_betting_board(betting_frame)
        self.create_spin_button()

    def create_labels(self):
        ttk.Label(self.root, text="Premium Casino Roulette", 
                font=("Arial", 24, "bold")).pack(pady=10)

    def create_wheel(self):
        self.canvas.delete("all")  # Clear everything

        # Draw outer ring
        self.canvas.create_oval(50, 50, 450, 450, 
                              fill="saddlebrown", 
                              tags="wheel")
        
        # Draw inner circle
        self.canvas.create_oval(70, 70, 430, 430, 
                              fill="darkgreen", 
                              tags="wheel")

        # Draw numbers and pockets
        for i, number in enumerate(self.numbers):
            angle = math.radians(i * (360 / 37) + self.wheel_angle)
            r = 180  # Radius for numbers
            x = self.wheel_center[0] + r * math.cos(angle)
            y = self.wheel_center[1] + r * math.sin(angle)
            
            # Create pocket markers
            pocket_size = 20
            self.canvas.create_oval(x - pocket_size/2, y - pocket_size/2,
                                  x + pocket_size/2, y + pocket_size/2,
                                  fill=self.colors[i],
                                  tags="wheel")
            
            # Draw numbers
            self.canvas.create_text(x, y, 
                                  text=str(number),
                                  fill="white",
                                  font=("Arial", 10, "bold"),
                                  tags="numbers")

        # Draw the ball
        ball_x = self.wheel_center[0] + self.ball_radius * math.cos(math.radians(self.ball_angle))
        ball_y = self.wheel_center[1] + self.ball_radius * math.sin(math.radians(self.ball_angle))
        self.canvas.create_oval(ball_x - 5, ball_y - 5,
                              ball_x + 5, ball_y + 5,
                              fill="white",
                              tags="ball")

        # Draw center decoration
        self.canvas.create_oval(240, 240, 260, 260,
                              fill="gold",
                              tags="wheel")

        # Draw spokes
        for i in range(37):
            angle = math.radians(i * (360 / 37) + self.wheel_angle)
            x1 = self.wheel_center[0] + 200 * math.cos(angle)
            y1 = self.wheel_center[1] + 200 * math.sin(angle)
            x2 = self.wheel_center[0] + 220 * math.cos(angle)
            y2 = self.wheel_center[1] + 220 * math.sin(angle)
            self.canvas.create_line(x1, y1, x2, y2, fill="gold", width=2, tags="wheel")

        # Draw inner ring
        self.canvas.create_oval(100, 100, 400, 400, 
                              outline="gold", width=4, 
                              tags="wheel")

        # Draw inner circle decoration
        self.canvas.create_oval(220, 220, 280, 280,
                              fill="darkred", outline="gold", width=2,
                              tags="wheel")

    def create_betting_board(self, frame):
        board_frame = ttk.Frame(frame)
        board_frame.pack(pady=10)

        # Create number buttons
        for i in range(12):
            for j in range(3):
                number = 1 + i + j * 12
                color = "red" if number in self.numbers[1::2] else "black"
                btn = ttk.Button(board_frame, text=str(number), style="TButton",
                                command=lambda n=number: self.place_bet("number", n))
                btn.grid(row=i, column=j, padx=5, pady=5)

        # Create zero button
        zero_btn = ttk.Button(board_frame, text="0", style="TButton",
                            command=lambda: self.place_bet("number", 0))
        zero_btn.grid(row=0, column=3, rowspan=3, padx=5, pady=5)

        # Create special bet buttons
        special_bets = [
            ("1st 12", "lightgray", 12, 0),
            ("2nd 12", "lightgray", 12, 1),
            ("3rd 12", "lightgray", 12, 2),
            ("1-18", "lightgray", 13, 0),
            ("Even", "lightgray", 13, 1),
            ("Red", "red", 13, 2),
            ("Black", "black", 13, 3),
            ("Odd", "lightgray", 13, 4),
            ("19-36", "lightgray", 13, 5)
        ]

        for text, color, row, col in special_bets:
            btn = ttk.Button(board_frame, text=text, style="TButton",
                            command=lambda t=text: self.place_special_bet(t))
            btn.grid(row=row, column=col, padx=5, pady=5)

    def create_chips(self, frame):
        ttk.Label(frame, text="Wählen Sie einen Chip:",
                font=("Arial", 14)).pack(side=tk.LEFT, padx=10)
        
        self.chip_values = [10, 50, 100, 200, 500]
        self.chips = []
        
        for value in self.chip_values:
            chip = tk.Button(frame, image=self.chip_images[value], command=lambda v=value: self.select_chip(v), bd=0)
            chip.pack(side=tk.LEFT, padx=5)
            self.chips.append(chip)

    def create_spin_button(self):
        self.spin_button = ttk.Button(self.root, text="Drehen",
                                   command=self.confirm_bet,
                                   style="TButton")
        self.spin_button.pack(pady=20)

    def select_chip(self, value):
        if self.balance >= value:
            self.selected_chip = value
            self.bet_amount += value
            self.bet_label.config(text=f"Wetteinsatz: {self.bet_amount} €")
        else:
            messagebox.showwarning("Warnung", "Nicht genügend Guthaben!")

    def confirm_bet(self):
        if not self.bets:
            messagebox.showwarning("Warnung", "Bitte platzieren Sie eine Wette.")
            return

        confirm = messagebox.askyesno("Bestätigung", f"Sie setzen {self.bet_amount} €. Fortfahren?")
        if confirm:
            self.spin_wheel()

    def place_bet(self, bet_type, bet_value):
        if self.selected_chip is None:
            messagebox.showwarning("Warnung", "Bitte wählen Sie einen Chip aus.")
            return

        self.bets.append((bet_type, bet_value, self.selected_chip))
        self.selected_chip = None
        self.bet_label.config(text=f"Wetteinsatz: {self.bet_amount} €")

    def place_special_bet(self, bet_type):
        if bet_type == "0":
            self.place_bet("number", 0)
        elif bet_type == "1st 12":
            self.place_bet("dozen", "1-12")
        elif bet_type == "2nd 12":
            self.place_bet("dozen", "13-24")
        elif bet_type == "3rd 12":
            self.place_bet("dozen", "25-36")
        elif bet_type == "1-18":
            self.place_bet("high_low", "1-18")
        elif bet_type == "19-36":
            self.place_bet("high_low", "19-36")
        elif bet_type == "Even":
            self.place_bet("parity", "gerade")
        elif bet_type == "Odd":
            self.place_bet("parity", "ungerade")
        elif bet_type == "Red":
            self.place_bet("color", "rot")
        elif bet_type == "Black":
            self.place_bet("color", "schwarz")

    def spin_wheel(self):
        if self.spinning:
            return
            
        self.spinning = True
        self.spin_button.config(state="disabled")
        self.result_label.config(text="")
        
        self.wheel_angle = 0
        self.ball_angle = 0
        self.ball_radius = 180
        self.spin_speed = 10
        self.ball_speed = 15

        self.spin_start_time = time()
        self.final_number = random.randint(0, 36)
        self.final_angle = self.numbers.index(self.final_number) * (360 / 37)
        
        self.animate_spin()

    def animate_spin(self):
        current_time = time() - self.spin_start_time
        
        self.wheel_angle += self.spin_speed
        self.wheel_angle %= 360
        
        self.ball_angle += self.ball_speed
        self.ball_angle %= 360
        
        if current_time > 2:
            self.spin_speed *= self.slow_down_factor
            self.ball_speed *= self.slow_down_factor
            
            if self.ball_radius > 140:
                self.ball_radius -= 0.5

        self.create_wheel()

        if self.spin_speed > 0.01:
            self.root.after(20, self.animate_spin)
        else:
            self.finish_spin()

    def finish_spin(self):
        # Synchronize the ball angle with the final number
        self.ball_angle = self.final_angle

        winning_number = self.final_number
        winning_color = "grün" if winning_number == 0 else "schwarz" if winning_number % 2 == 0 else "rot"
        
        self.result_label.config(text=f"Die Kugel landet auf: {winning_number} ({winning_color})")
        
        total_winnings = self.calculate_winnings(winning_number, winning_color)
        
        if total_winnings > 0:
            self.balance += total_winnings
            messagebox.showinfo("Gewonnen!", f"Sie haben gewonnen! {total_winnings}€")
        else:
            self.balance -= self.bet_amount
            messagebox.showinfo("Verloren", "Leider verloren. Viel Glück beim nächsten Mal!")

        self.update_display()
        self.reset_game_state()

    def calculate_winnings(self, winning_number, winning_color):
        total_winnings = 0
        for bet_type, bet_value, bet_amount in self.bets:
            if bet_type == "number" and bet_value == winning_number:
                total_winnings += bet_amount * 35
            elif bet_type == "color" and bet_value == winning_color:
                total_winnings += bet_amount * 2
            elif bet_type == "parity" and ((bet_value == "gerade" and winning_number % 2 == 0) or
                                           (bet_value == "ungerade" and winning_number % 2 == 1)):
                total_winnings += bet_amount * 2
            elif bet_type == "dozen" and ((bet_value == "1-12" and 1 <= winning_number <= 12) or
                                          (bet_value == "13-24" and 13 <= winning_number <= 24) or
                                          (bet_value == "25-36" and 25 <= winning_number <= 36)):
                total_winnings += bet_amount * 3
            elif bet_type == "high_low" and ((bet_value == "1-18" and 1 <= winning_number <= 18) or
                                             (bet_value == "19-36" and 19 <= winning_number <= 36)):
                total_winnings += bet_amount * 2

        return total_winnings

    def update_display(self):
        self.balance_label.config(text=f"Kontostand: {self.balance} €")
        self.bet_label.config(text=f"Wetteinsatz: {self.bet_amount} €")

    def reset_game_state(self):
        self.bet_amount = 0
        self.selected_chip = None
        self.spinning = False
        self.spin_button.config(state="normal")
        self.bets.clear()

if __name__ == "__main__":
    root = tk.Tk()
    app = ModernRouletteGUI(root)
    root.mainloop()