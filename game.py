import tkinter as tk
from tkinter import messagebox
import random

class RockPaperScissors:
    def __init__(self, root):
        self.root = root
        self.root.title("Rock Paper Scissors")
        self.root.geometry("500x600")
        self.root.configure(bg='#f0f0f0')
        
        # Game variables
        self.choices = ['Rock', 'Paper', 'Scissors']
        self.player_score = 0
        self.computer_score = 0
        
        # Create GUI elements
        self.create_widgets()
        
    def create_widgets(self):
        # Title
        title_label = tk.Label(self.root, text="Rock Paper Scissors", 
                              font=('Arial', 24, 'bold'), bg='#f0f0f0', fg='#2c3e50')
        title_label.pack(pady=20)
        
        # Score frame
        score_frame = tk.Frame(self.root, bg='#f0f0f0')
        score_frame.pack(pady=10)
        
        self.player_score_label = tk.Label(score_frame, text=f"Player: {self.player_score}", 
                                          font=('Arial', 14), bg='#f0f0f0', fg='#27ae60')
        self.player_score_label.pack(side=tk.LEFT, padx=20)
        
        self.computer_score_label = tk.Label(score_frame, text=f"Computer: {self.computer_score}", 
                                            font=('Arial', 14), bg='#f0f0f0', fg='#e74c3c')
        self.computer_score_label.pack(side=tk.LEFT, padx=20)
        
        # Choice buttons frame
        button_frame = tk.Frame(self.root, bg='#f0f0f0')
        button_frame.pack(pady=30)
        
        # Create choice buttons with images (using text instead of images for simplicity)
        self.rock_btn = tk.Button(button_frame, text="✊ Rock", font=('Arial', 16), 
                                 command=lambda: self.play_game('Rock'),
                                 bg='#3498db', fg='white', width=10, height=2)
        self.rock_btn.pack(side=tk.LEFT, padx=10)
        
        self.paper_btn = tk.Button(button_frame, text="✋ Paper", font=('Arial', 16), 
                                  command=lambda: self.play_game('Paper'),
                                  bg='#2ecc71', fg='white', width=10, height=2)
        self.paper_btn.pack(side=tk.LEFT, padx=10)
        
        self.scissors_btn = tk.Button(button_frame, text="✌️ Scissors", font=('Arial', 16), 
                                     command=lambda: self.play_game('Scissors'),
                                     bg='#e67e22', fg='white', width=10, height=2)
        self.scissors_btn.pack(side=tk.LEFT, padx=10)
        
        # Result display frame
        result_frame = tk.Frame(self.root, bg='#f0f0f0')
        result_frame.pack(pady=20)
        
        # Player choice display
        self.player_choice_label = tk.Label(result_frame, text="Your choice: ", 
                                           font=('Arial', 14), bg='#f0f0f0')
        self.player_choice_label.pack()
        
        # Computer choice display
        self.computer_choice_label = tk.Label(result_frame, text="Computer's choice: ", 
                                            font=('Arial', 14), bg='#f0f0f0')
        self.computer_choice_label.pack()
        
        # Result message
        self.result_label = tk.Label(self.root, text="Make your choice!", 
                                   font=('Arial', 18, 'bold'), bg='#f0f0f0', fg='#2c3e50')
        self.result_label.pack(pady=20)
        
        # Reset button
        reset_btn = tk.Button(self.root, text="Reset Game", font=('Arial', 12), 
                             command=self.reset_game, bg='#95a5a6', fg='white')
        reset_btn.pack(pady=10)
        
    def play_game(self, player_choice):
        computer_choice = random.choice(self.choices)
        
        # Update choice displays
        self.player_choice_label.config(text=f"Your choice: {player_choice}")
        self.computer_choice_label.config(text=f"Computer's choice: {computer_choice}")
        
        # Determine winner
        result = self.determine_winner(player_choice, computer_choice)
        
        # Update scores and display
        if result == "win":
            self.player_score += 1
            self.result_label.config(text="You Win! 🎉", fg='#27ae60')
        elif result == "lose":
            self.computer_score += 1
            self.result_label.config(text="Computer Wins! 😢", fg='#e74c3c')
        else:
            self.result_label.config(text="It's a Tie! 🤝", fg='#f39c12')
        
        # Update score labels
        self.player_score_label.config(text=f"Player: {self.player_score}")
        self.computer_score_label.config(text=f"Computer: {self.computer_score}")
        
    def determine_winner(self, player, computer):
        if player == computer:
            return "tie"
        
        winning_combinations = {
            'Rock': 'Scissors',
            'Paper': 'Rock',
            'Scissors': 'Paper'
        }
        
        if winning_combinations[player] == computer:
            return "win"
        else:
            return "lose"
    
    def reset_game(self):
        self.player_score = 0
        self.computer_score = 0
        self.player_score_label.config(text=f"Player: {self.player_score}")
        self.computer_score_label.config(text=f"Computer: {self.computer_score}")
        self.player_choice_label.config(text="Your choice: ")
        self.computer_choice_label.config(text="Computer's choice: ")
        self.result_label.config(text="Make your choice!", fg='#2c3e50')

if __name__ == "__main__":
    root = tk.Tk()
    game = RockPaperScissors(root)
    root.mainloop()