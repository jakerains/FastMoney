import tkinter as tk
from tkinter import ttk, messagebox, simpledialog
import time
import json

class GameBoard(tk.Toplevel):
    def __init__(self, master):
        super().__init__(master)
        self.title("Fast Money Game Board")
        self.attributes('-fullscreen', True)
        self.configure(bg="#00008B")
        
        self.setup_ui()
        self.total_score = 0

    def setup_ui(self):
        font_large = ("Arial", 48, "bold")
        font_medium = ("Arial", 36, "bold")
        bg_color = "#00008B"
        fg_color = "#FFFFFF"
        label_bg_color = "#000000"

        main_frame = tk.Frame(self, bg=bg_color)
        main_frame.place(relx=0.5, rely=0.5, anchor="center")

        self.player1_label = tk.Label(main_frame, text="", font=font_large, bg=bg_color, fg=fg_color)
        self.player1_label.grid(row=0, column=0, pady=(0, 20))

        self.player2_label = tk.Label(main_frame, text="Player 1", font=font_large, bg=bg_color, fg=fg_color)
        self.player2_label.grid(row=0, column=1, columnspan=2, pady=(0, 20))

        self.previous_answer_labels = []
        self.answer_labels = []
        self.score_labels = []
        for i in range(5):
            previous_answer_label = tk.Label(main_frame, text="", font=font_medium, bg=label_bg_color, fg=fg_color, width=20, anchor="w")
            previous_answer_label.grid(row=i+1, column=0, padx=10, pady=5, sticky="w")
            self.previous_answer_labels.append(previous_answer_label)

            answer_label = tk.Label(main_frame, text="", font=font_medium, bg=label_bg_color, fg=fg_color, width=30, anchor="w")
            answer_label.grid(row=i+1, column=1, padx=10, pady=5, sticky="ew")
            self.answer_labels.append(answer_label)
            
            score_label = tk.Label(main_frame, text="", font=font_medium, bg=label_bg_color, fg=fg_color, width=5)
            score_label.grid(row=i+1, column=2, padx=10, pady=5)
            self.score_labels.append(score_label)

        self.total_score_label = tk.Label(main_frame, text="TOTAL: 0", font=font_large, bg=bg_color, fg=fg_color)
        self.total_score_label.grid(row=6, column=0, columnspan=3, pady=20)

    def reveal_answer(self, index, text):
        self.animate_text(self.answer_labels[index], text)

    def animate_text(self, label, text):
        for i in range(len(text) + 1):
            label.config(text=text[:i])
            self.update()
            time.sleep(0.05)

    def reveal_score(self, index, score):
        self.score_labels[index].config(text=str(score))
        self.total_score += score
        self.update_total()

    def update_total(self):
        self.total_score_label.config(text=f"TOTAL: {self.total_score}")

    def reset_all(self):
        for label in self.previous_answer_labels + self.answer_labels + self.score_labels:
            label.config(text="")
        self.total_score = 0
        self.total_score_label.config(text="TOTAL: 0")
        self.player1_label.config(text="")
        self.player2_label.config(text="Player 1")

    def show_previous_answers(self, previous_answers):
        self.player1_label.config(text="Player 1")
        for label, answer in zip(self.previous_answer_labels, previous_answers):
            label.config(text=answer)
        self.update()

    def switch_to_player2(self):
        self.player1_label.config(text="")
        self.player2_label.config(text="Player 2")
        for label in self.answer_labels + self.score_labels:
            label.config(text="")
        self.update()

    def animate_previous_answers(self, previous_answers):
        self.player1_label.config(text="Player 1")
        for label in self.previous_answer_labels:
            label.config(text="")
        self.update()
        
        for i in range(max(len(s) for s in previous_answers)):
            for label, answer in zip(self.previous_answer_labels, previous_answers):
                if i < len(answer):
                    label.config(text=answer[:i+1])
            self.update()
            time.sleep(0.05)

class ControlPanel(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Fast Money Control Panel")
        self.geometry("1200x800")
        
        self.font_medium = ("Arial", 14)  # Define the font here
        
        self.game_board = GameBoard(self)
        self.all_questions = []
        self.current_question_index = 0
        self.current_player = 1
        self.player1_answers = []
        self.player1_score = 0
        self.player2_answers = []
        self.player2_score = 0
        self.original_questions = []
        self.skipped_questions = set()
        self.player_answer_labels = []

        self.setup_ui()

    def setup_ui(self):
        self.frame = tk.LabelFrame(self, text="Fast Money Control", font=self.font_medium)
        self.frame.pack(pady=10, padx=10, fill="both", expand=True)

        # Use self.font_medium for all buttons and labels
        tk.Label(self.frame, text="Questions and Answers:", font=self.font_medium).grid(row=0, column=0, padx=5, pady=5)
        self.questions_entry = tk.Text(self.frame, font=self.font_medium, height=10, width=60)
        self.questions_entry.grid(row=0, column=1, columnspan=3, padx=5, pady=5)

        load_questions_btn = tk.Button(self.frame, text="Load Questions", font=self.font_medium, command=self.load_questions)
        load_questions_btn.grid(row=1, column=1, columnspan=3, pady=10)

        # Current question display
        self.current_question_label = tk.Label(self.frame, text="", font=self.font_medium, wraplength=600)
        self.current_question_label.grid(row=2, column=0, columnspan=4, pady=10)

        # Answer options frame
        self.answer_frame = tk.Frame(self.frame)
        self.answer_frame.grid(row=3, column=0, columnspan=4, pady=10, sticky="w")

        # Custom answer entry and Next Question button
        tk.Label(self.frame, text="Custom Answer:", font=self.font_medium).grid(row=4, column=0, pady=5)
        self.custom_answer_entry = tk.Entry(self.frame, font=self.font_medium)
        self.custom_answer_entry.grid(row=4, column=1, columnspan=2, pady=5, sticky="ew")
        self.custom_answer_entry.bind("<Return>", self.on_custom_answer_enter)

        # Custom answer button
        self.custom_answer_btn = tk.Button(self.frame, text="Custom Answer", font=self.font_medium, command=self.mark_custom_answer)
        self.custom_answer_btn.grid(row=4, column=1, pady=5, padx=5, sticky="ew")

        # Next question button
        self.next_question_btn = tk.Button(self.frame, text="Next Question", font=self.font_medium, command=self.next_question)
        self.next_question_btn.grid(row=4, column=2, pady=5, padx=5, sticky="ew")

        self.skip_btn = tk.Button(self.frame, text="Skip", font=self.font_medium, command=self.skip_question)
        self.skip_btn.grid(row=4, column=3, pady=5, padx=5, sticky="ew")

        self.switch_player_btn = tk.Button(self.frame, text="Switch Player", font=self.font_medium, command=self.switch_player, state=tk.DISABLED)
        self.switch_player_btn.grid(row=5, column=1, columnspan=2, pady=10)

        # Player 1 frame
        self.player1_frame = tk.LabelFrame(self.frame, text="Player 1 Answers", font=self.font_medium)
        self.player1_frame.grid(row=0, column=4, rowspan=3, padx=10, pady=10, sticky="nsew")
        self.create_player_reveal_buttons(self.player1_frame, 1)

        # Player 2 frame
        self.player2_frame = tk.LabelFrame(self.frame, text="Player 2 Answers", font=self.font_medium)
        self.player2_frame.grid(row=0, column=4, rowspan=3, padx=10, pady=10, sticky="nsew")
        self.create_player_reveal_buttons(self.player2_frame, 2)
        self.player2_frame.grid_remove()  # Hide initially

        # Configure column weights
        self.frame.columnconfigure(4, weight=1)

        # Player answer display
        self.player_answer_frame = tk.Frame(self.frame)
        self.player_answer_frame.grid(row=0, column=5, rowspan=3, padx=10, pady=10, sticky="nw")

        # Total score display
        self.total_score_label = tk.Label(self.frame, text="Total Score: 0", font=self.font_medium)
        self.total_score_label.grid(row=6, column=1, columnspan=2, pady=10)

        # Add this new button at the end of the setup_ui method
        self.reset_all_btn = tk.Button(self.frame, text="Reset All", font=self.font_medium, command=self.reset_all)
        self.reset_all_btn.grid(row=7, column=1, columnspan=2, pady=10)

    def create_player_reveal_buttons(self, frame, player_num):
        for widget in frame.winfo_children():
            widget.destroy()

        self.player_reveal_buttons = []
        
        for i in range(5):
            reveal_frame = tk.Frame(frame)
            reveal_frame.pack(pady=5, fill='x')
            
            reveal_answer_btn = tk.Button(reveal_frame, text=f"Reveal Answer {i+1}", 
                                          command=lambda idx=i: self.reveal_player_answer(player_num, idx),
                                          width=15)  # Set a fixed width
            reveal_answer_btn.pack(side=tk.LEFT, padx=5)
            
            reveal_score_btn = tk.Button(reveal_frame, text=f"Reveal Score {i+1}", 
                                         command=lambda idx=i: self.reveal_player_score(player_num, idx),
                                         width=15)  # Set a fixed width
            reveal_score_btn.pack(side=tk.LEFT, padx=5)
            
            self.player_reveal_buttons.append((reveal_answer_btn, reveal_score_btn))

        # Add some padding at the bottom of the frame
        tk.Frame(frame).pack(pady=10)

    def load_questions(self):
        questions_text = self.questions_entry.get("1.0", tk.END).strip()
        questions = questions_text.split('\n')
        
        self.all_questions = []
        current_question = None
        for line in questions:
            line = line.strip()
            if line.startswith(('1.', '2.', '3.', '4.', '5.')):
                if current_question:
                    self.all_questions.append(current_question)
                current_question = {'question': line[3:].strip(), 'answers': []}
            elif line.startswith(('•', '-')):  # Check for both bullet points and dashes
                parts = line[1:].split(':')
                if len(parts) == 2:
                    answer, points = parts
                    current_question['answers'].append((answer.strip(), int(points.strip())))
        
        if current_question:
            self.all_questions.append(current_question)

        self.original_questions = self.all_questions.copy()
        self.current_question_index = 0
        self.update_question_display()
        messagebox.showinfo("Success", f"Loaded {len(self.all_questions)} questions successfully!")

    def update_question_display(self):
        if self.current_question_index < len(self.all_questions):
            question = self.all_questions[self.current_question_index]
            self.current_question_label.config(text=question['question'])
            
            # Clear previous answer options
            for widget in self.answer_frame.winfo_children():
                widget.destroy()

            self.answer_var = tk.StringVar()
            self.answer_radios = []

            for i, (answer, points) in enumerate(question['answers']):
                state = 'normal'
                if self.current_player == 2 and self.current_question_index < len(self.player1_answers):
                    player1_answer = self.player1_answers[self.current_question_index][0]
                    if player1_answer == answer:
                        state = 'disabled'
                radio = tk.Radiobutton(self.answer_frame, text=f"{answer} ({points})", 
                                       variable=self.answer_var, value=i, font=self.font_medium,
                                       command=self.on_answer_selected, state=state)
                radio.grid(row=i, column=0, sticky="w")
                self.answer_radios.append(radio)
            
            self.update_idletasks()
        else:
            self.current_question_label.config(text="No more questions")
            for widget in self.answer_frame.winfo_children():
                widget.destroy()

    def on_answer_selected(self):
        self.next_question()

    def on_custom_answer_enter(self, event):
        self.next_question()

    def save_current_answer(self):
        if self.current_question_index >= len(self.all_questions):
            return

        selected = self.answer_var.get()
        custom_answer = self.custom_answer_entry.get().strip()
        
        if selected:
            answer, points = self.all_questions[self.current_question_index]['answers'][int(selected)]
        elif custom_answer:
            answer = custom_answer
            points = 0
        else:
            return  # No answer provided, don't save anything

        if self.current_player == 1:
            while len(self.player1_answers) <= self.current_question_index:
                self.player1_answers.append(("Skipped", 0))
            self.player1_answers[self.current_question_index] = (answer, points)
        else:
            while len(self.player2_answers) <= self.current_question_index:
                self.player2_answers.append(("Skipped", 0))
            self.player2_answers[self.current_question_index] = (answer, points)
        
        self.update_player_answer_display()
        self.custom_answer_entry.delete(0, tk.END)

    def next_question(self):
        self.save_current_answer()
        
        if hasattr(self, 'enter_answer_btn'):
            self.enter_answer_btn.grid_remove()
        
        # Check if all questions have been answered
        current_answers = self.player1_answers if self.current_player == 1 else self.player2_answers
        all_answered = len(current_answers) == len(self.all_questions) and all(answer != "" for answer, _ in current_answers)
        
        if all_answered:
            if self.current_player == 1:
                self.player1_turn_completed()
            else:
                messagebox.showinfo("Game Over", "Both players have completed their turns!")
            return

        # Find the next unanswered question
        self.current_question_index += 1
        while self.current_question_index < len(self.all_questions):
            if self.current_question_index >= len(current_answers) or current_answers[self.current_question_index][0] == "":
                break
            self.current_question_index += 1

        if self.current_question_index < len(self.all_questions):
            self.update_question_display()
        else:
            # If we've reached the end, go back to find any unanswered questions
            self.current_question_index = 0
            while self.current_question_index < len(self.all_questions):
                if current_answers[self.current_question_index][0] == "":
                    self.update_question_display()
                    return
                self.current_question_index += 1
            
            # If we get here, all questions have been answered
            if self.current_player == 1:
                self.player1_turn_completed()
            else:
                messagebox.showinfo("Game Over", "Both players have completed their turns!")
                self.game_over()

    def player1_turn_completed(self):
        messagebox.showinfo("Player 1 Finished", "Player 1 has answered all questions. You can now enter custom answers, reveal answers, and scores.")
        self.switch_player_btn.config(state=tk.NORMAL)  # Enable the switch player button
        self.update_question_display()  # Clear the question display
        
        # Disable answer inputs
        for radio in self.answer_radios:
            radio.config(state=tk.DISABLED)
        self.custom_answer_entry.config(state=tk.DISABLED)
        self.skip_btn.config(state=tk.DISABLED)
        
        # Show custom answer entry buttons
        self.show_enter_custom_answer_buttons()

    def game_over(self):
        messagebox.showinfo("Game Over", "Both players have completed their turns. You can now reveal answers and scores.")
        self.switch_player_btn.config(state=tk.NORMAL)  # Enable the switch player button
        self.update_question_display()  # Clear the question display
        
        # Disable answer inputs
        for radio in self.answer_radios:
            radio.config(state=tk.DISABLED)
        self.custom_answer_entry.config(state=tk.DISABLED)
        self.skip_btn.config(state=tk.DISABLED)

    def clear_answer_selection(self):
        self.answer_var.set("")  # Clear the radio button selection
        self.custom_answer_entry.delete(0, tk.END)  # Clear the custom answer entry

    def reveal_player_answer(self, player_num, index):
        answers = self.player1_answers if player_num == 1 else self.player2_answers
        if index < len(answers):
            answer, _ = answers[index]
            self.game_board.reveal_answer(index, answer)
            self.player_answer_labels[index].config(text=f"P{player_num}: {answer}")

    def reveal_player_score(self, player_num, index):
        answers = self.player1_answers if player_num == 1 else self.player2_answers
        if index < len(answers):
            _, score = answers[index]
            self.game_board.reveal_score(index, score)
            current_text = self.player_answer_labels[index].cget("text")
            self.player_answer_labels[index].config(text=f"{current_text} ({score})")
            if player_num == 1:
                self.player1_score += score
            else:
                self.player2_score += score
            self.update_total_score()

    def switch_player(self):
        if self.current_player == 1:
            self.current_player = 2
            self.current_question_index = 0
            self.skipped_questions.clear()
            self.player2_answers = []  # Initialize as an empty list
            self.update_question_display()
            self.game_board.switch_to_player2()
            self.player1_frame.grid_remove()
            self.player2_frame.grid()
            
            # Clear the player answer display
            for label in self.player_answer_labels:
                label.destroy()
            self.player_answer_labels.clear()
            
            # Re-enable answer inputs
            for radio in self.answer_radios:
                radio.config(state=tk.NORMAL)
            self.custom_answer_entry.config(state=tk.NORMAL)
            self.skip_btn.config(state=tk.NORMAL)
            
            # Disable the switch player button again
            self.switch_player_btn.config(state=tk.DISABLED)
            
            # Add a button to reveal Player 1's answers
            self.reveal_player1_answers_btn = tk.Button(self.frame, text="Reveal Player 1 Answers", 
                                                        font=self.font_medium, command=self.reveal_player1_answers)
            self.reveal_player1_answers_btn.grid(row=3, column=4, pady=10)
        else:
            messagebox.showinfo("Game Over", "Both players have completed their turns!")
            self.player2_frame.grid_remove()
            # You might want to add code here to end the game or reset for a new game

    def reveal_player1_answers(self):
        answers = [answer for answer, _ in self.player1_answers]
        self.game_board.animate_previous_answers(answers)
        self.reveal_player1_answers_btn.grid_remove()  # Remove the button after revealing

    def update_total_score(self):
        total_score = self.player1_score + self.player2_score
        self.total_score_label.config(text=f"Total Score: {total_score}")
        self.game_board.total_score = total_score
        self.game_board.update_total()

    def reset_all(self):
        # Reset all game state variables
        self.current_question_index = 0
        self.current_player = 1
        self.player1_answers = []
        self.player1_score = 0
        self.player2_answers = []
        self.player2_score = 0
        self.skipped_questions.clear()

        # Clear the question display and answer options
        self.current_question_label.config(text="")
        for widget in self.answer_frame.winfo_children():
            widget.destroy()

        # Clear the custom answer entry
        self.custom_answer_entry.delete(0, tk.END)

        # Reset the total score display
        self.total_score_label.config(text="Total Score: 0")

        # Hide Player 2 frame and show Player 1 frame
        self.player2_frame.grid_remove()
        self.player1_frame.grid()

        # Clear and recreate reveal buttons for both players
        self.create_player_reveal_buttons(self.player1_frame, 1)
        self.create_player_reveal_buttons(self.player2_frame, 2)

        # Reset the game board
        self.game_board.reset_all()

        # Clear the questions and answers field
        self.questions_entry.delete("1.0", tk.END)
        
        # Clear the all_questions list
        self.all_questions = []

        # Clear player answer labels
        for label in self.player_answer_labels:
            label.destroy()
        self.player_answer_labels.clear()

        # Remove the "Reveal Player 1 Answers" button if it exists
        if hasattr(self, 'reveal_player1_answers_btn'):
            self.reveal_player1_answers_btn.grid_remove()

        # Disable the switch player button
        self.switch_player_btn.config(state=tk.DISABLED)

        # Ensure the main frame is visible and properly configured
        self.frame.update_idletasks()

        # Clear the player answer display
        self.update_player_answer_display()

        if hasattr(self, 'enter_answer_btn'):
            self.enter_answer_btn.grid_remove()

        messagebox.showinfo("Reset Complete", "Game has been reset successfully. Please load new questions to start a new game.")

    def skip_question(self):
        if self.current_question_index < len(self.all_questions):
            self.skipped_questions.add(self.current_question_index)
            
            # Add a placeholder for the skipped question
            current_answers = self.player1_answers if self.current_player == 1 else self.player2_answers
            while len(current_answers) <= self.current_question_index:
                current_answers.append(("Skipped", 0))
            
            self.update_player_answer_display()
            self.next_question()

    def get_player_answer(self, question):
        answers = self.player1_answers if self.current_player == 1 else self.player2_answers
        return next((a for a in answers if a[0] and a[0] in question['question']), None)

    def update_player_answer_display(self):
        # Clear existing labels
        for label in self.player_answer_labels:
            label.destroy()
        self.player_answer_labels.clear()
        
        answers = self.player1_answers if self.current_player == 1 else self.player2_answers
        for i, (answer, points) in enumerate(answers):
            if answer == "Skipped":
                text = f"P{self.current_player}: Question {i+1} Skipped"
            elif answer == "Custom Answer":
                text = f"P{self.current_player}: Question {i+1} Custom Answer (Not Entered)"
            else:
                text = f"P{self.current_player}: {answer} ({points})"
            new_label = tk.Label(self.player_answer_frame, text=text, font=self.font_medium, anchor="w")
            new_label.pack(pady=5)
            self.player_answer_labels.append(new_label)

    def mark_custom_answer(self):
        if self.current_question_index < len(self.all_questions):
            current_answers = self.player1_answers if self.current_player == 1 else self.player2_answers
            while len(current_answers) <= self.current_question_index:
                current_answers.append(("", 0))
            current_answers[self.current_question_index] = ("Custom Answer", 0)
            self.update_player_answer_display()
            self.show_enter_answer_button()
            self.next_question()

    def show_enter_answer_button(self):
        if hasattr(self, 'enter_answer_btn'):
            self.enter_answer_btn.grid_remove()
        self.enter_answer_btn = tk.Button(self.frame, text="Enter Custom Answer", font=self.font_medium, command=self.enter_custom_answer)
        self.enter_answer_btn.grid(row=4, column=3, pady=5, padx=5, sticky="ew")

    def enter_custom_answer(self):
        current_answers = self.player1_answers if self.current_player == 1 else self.player2_answers
        custom_answer = simpledialog.askstring("Custom Answer", f"Enter custom answer for Player {self.current_player}, Question {self.current_question_index + 1}:")
        if custom_answer:
            current_answers[self.current_question_index] = (custom_answer, 0)
            self.update_player_answer_display()
        else:
            # If the user cancels, revert to "Custom Answer"
            current_answers[self.current_question_index] = ("Custom Answer", 0)
        self.enter_answer_btn.grid_remove()

    def show_enter_custom_answer_buttons(self):
        custom_answer_frame = tk.Frame(self.frame)
        custom_answer_frame.grid(row=6, column=4, pady=10)
        
        for i in range(5):
            btn = tk.Button(custom_answer_frame, text=f"Enter Custom Answer {i+1}", 
                            command=lambda idx=i: self.enter_custom_answer(idx),
                            font=self.font_medium)
            btn.pack(pady=2)

    def enter_custom_answer(self, index):
        current_answers = self.player1_answers if self.current_player == 1 else self.player2_answers
        custom_answer = simpledialog.askstring("Custom Answer", f"Enter custom answer for Player {self.current_player}, Question {index + 1}:")
        if custom_answer:
            current_answers[index] = (custom_answer, 0)
            self.update_player_answer_display()
        else:
            # If the user cancels, revert to "Custom Answer"
            current_answers[index] = ("Custom Answer", 0)

control_panel = ControlPanel()
control_panel.mainloop()