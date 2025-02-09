import tkinter as tk
from tkinter import messagebox
import csv
import random
from PIL import Image, ImageTk

def load_questions(filename):
    with open(filename, 'r') as file:
        reader = csv.DictReader(file)
        questions = []
        for row in reader:
            try:
                row['Level'] = int(row['Level'])
                questions.append(row)
            except (ValueError, KeyError):
                print(f"Skipping invalid row: {row}")
    return questions

class MillionaireGame:
    def __init__(self, root, questions):
        self.root = root
        self.questions = questions
        self.current_level = 1
        self.lifelines = {'50-50': True, 'swap': True, 'jump-the-question': True}
        self.current_question = None
        self.answers = []
        self.timer = None
        self.setup_ui()

    def setup_ui(self):
        self.root.title('Who Wants to Be a Millionaire')
        self.root.configure(bg='#282c34')
        self.root.resizable(False, False)

        main_frame = tk.Frame(self.root, bg='#282c34')
        main_frame.pack(padx=20, pady=20)

        left_frame = tk.Frame(main_frame, bg='#282c34')
        left_frame.pack(side='left', padx=10)

        right_frame = tk.Frame(main_frame, bg='#282c34')
        right_frame.pack(side='right', padx=20)

        self.question_label = tk.Label(
            left_frame,
            text='',
            wraplength=400,
            justify='center',
            font=('Copperplate Gothic', 16), bg='#282c34', fg='white',
            height=4
        )
        self.question_label.pack(pady=20)

        self.answer_buttons = []
        answer_frame = tk.Frame(left_frame, bg='#282c34')
        answer_frame.pack(pady=20)
        for i in range(2):
            for j in range(2):
                btn = tk.Button(
                    answer_frame,
                    text='',
                    width=25,
                    height=2,
                    command=lambda index=len(self.answer_buttons): self.check_answer(index)
                )
                btn.grid(row=i, column=j, padx=20, pady=10)
                self.answer_buttons.append(btn)

        self.timer_bar = tk.Canvas(left_frame, height=10, bg='#3b3f45')
        self.timer_bar.pack(fill='y', pady=5)

        self.lifeline_frame = tk.Frame(right_frame, bg='#282c34')
        self.lifeline_frame.pack(pady=20)
        self.lifeline_images = {
            '50-50': ImageTk.PhotoImage(Image.open('images/50-50.png').resize((50, 50))),
            'swap': ImageTk.PhotoImage(Image.open('images/swap.png').resize((50, 50))),
            'jump-the-question': ImageTk.PhotoImage(Image.open('images/jump_the_question.png').resize((50, 50)))
        }
        self.fifty_fifty_btn = tk.Button(self.lifeline_frame, image=self.lifeline_images['50-50'],
                                         command=self.use_fifty_fifty, bd=0)
        self.fifty_fifty_btn.pack(side='left', padx=10)
        self.swap_btn = tk.Button(self.lifeline_frame, image=self.lifeline_images['swap'], command=self.use_swap, bd=0)
        self.swap_btn.pack(side='left', padx=10)
        self.jump_the_question_btn = tk.Button(self.lifeline_frame, image=self.lifeline_images['jump-the-question'],
                                         command=self.use_jump_the_question, bd=0)
        self.jump_the_question_btn.pack(side='left', padx=10)

        progress_box = tk.Frame(right_frame, bg='#3b3f45', bd=2, relief='groove')
        progress_box.pack(pady=20)
        self.progress_frame = tk.Frame(progress_box, bg='#3b3f45')
        self.progress_frame.pack(pady=5)
        self.progress_labels = []
        money_values = ['1.000.000', '500.000', '250.000', '125.000', '64.000', '32.000', '16.000', '8.000', '4.000',
                        '2.000', '1.000', '500', '300', '200', '100']
        for i in range(15):
            level_lbl = tk.Label(self.progress_frame, text=f'{15 - i}', bg='#3b3f45', fg='white',
                                 font=('Copperplate Gothic', 12), anchor='w', width=10)
            ammount_lbl = tk.Label(self.progress_frame, text=f'{money_values[i]}', bg='#3b3f45', fg='white',
                                   font=('Copperplate Gothic', 12), anchor='e', width=10)

            level_lbl.grid(row=i, column=0, padx=10, pady=5, sticky='w')
            ammount_lbl.grid(row=i, column=1, padx=10, pady=5, sticky='e')

            self.progress_labels.append([level_lbl, ammount_lbl])

        self.next_question()

    def next_question(self):
        if self.current_level > 15:
            self.show_win_message()
            return

        level_questions = [q for q in self.questions if int(q['Level']) == self.current_level]
        self.current_question = random.choice(level_questions)

        self.question_label.config(text=self.current_question['Question'])
        self.answers = [self.current_question['CorrectAnswer'],
                        self.current_question['Incorrect1'],
                        self.current_question['Incorrect2'],
                        self.current_question['Incorrect3']]
        random.shuffle(self.answers)

        for i, answer in enumerate(self.answers):
            self.answer_buttons[i].config(text=answer)

        for i, (level_lbl, ammount_lbl) in enumerate(self.progress_labels):
            if i == 15 - self.current_level:
                level_lbl.config(bg='orange')
                ammount_lbl.config(bg='orange')
            else:
                level_lbl.config(bg='#3b3f45')
                ammount_lbl.config(bg='#3b3f45')

        self.start_timer()

    def show_win_message(self):
        response = messagebox.askyesno('Congratulations!', 'You win! Would you like to play again?')
        if response:
            self.restart_game()
        else:
            self.root.quit()

    def start_timer(self):
        if self.timer:
            self.root.after_cancel(self.timer)

        self.timer_bar.delete('all')
        self.timer_bar.create_rectangle(0, 0, 400, 10, fill='green', tags='timer')
        self.update_timer(400, 30)

    def update_timer(self, width, time_left):
        if time_left <= 0:
            messagebox.showerror('Time\'s Up!', 'You ran out of time.')
            self.root.quit()
            return

        new_width = width - (400 / 30)
        self.timer_bar.coords('timer', 0, 0, new_width, 10)
        self.timer = self.root.after(1000, self.update_timer, new_width, time_left - 1)

    def check_answer(self, index):
        if self.timer:
            self.root.after_cancel(self.timer)

        if self.answers[index] == self.current_question['CorrectAnswer']:
            self.current_level += 1
            self.next_question()
        else:
            self.show_game_over()

    def show_game_over(self):
        response = messagebox.askyesno('Incorrect!', 'Game Over. Would you like to play again?')
        if response:
            self.restart_game()
        else:
            self.root.quit()

    def restart_game(self):
        self.current_level = 1
        self.lifelines = {'50-50': True, 'swap': True, 'jump-the-question': True}
        self.fifty_fifty_btn.config(state='normal', bg='#282c34')
        self.swap_btn.config(state='normal', bg='#282c34')
        self.jump_the_question_btn.config(state='normal', bg='#282c34')

        self.next_question()

    def use_fifty_fifty(self):
        if not self.lifelines['50-50']:
            messagebox.showwarning('Lifeline Used', 'You have already used this lifeline.')
            return
        self.lifelines['50-50'] = False
        self.fifty_fifty_btn.config(state='disabled', bg='gray')
        incorrect_answers = [ans for ans in self.answers if ans != self.current_question['CorrectAnswer']]
        random.shuffle(incorrect_answers)
        incorrect_to_remove = incorrect_answers[:2]
        for btn in self.answer_buttons:
            if btn.cget('text') in incorrect_to_remove:
                btn.config(text='')

    def use_swap(self):
        if not self.lifelines["swap"]:
            messagebox.showwarning("Lifeline Used", "You have already used this lifeline.")
            return

        self.lifelines["swap"] = False
        self.swap_btn.config(state="disabled", bg="gray")

        level_questions = [q for q in self.questions if int(q['Level']) == self.current_level]

        level_questions = [q for q in level_questions if q != self.current_question]

        if not level_questions:
            messagebox.showwarning("No Other Questions", "No other questions available at this level.")
            return

        self.current_question = random.choice(level_questions)

        self.question_label.config(text=self.current_question['Question'])
        self.answers = [self.current_question['CorrectAnswer'],
                        self.current_question['Incorrect1'],
                        self.current_question['Incorrect2'],
                        self.current_question['Incorrect3']]
        random.shuffle(self.answers)

        for i, answer in enumerate(self.answers):
            self.answer_buttons[i].config(text=answer)

    def use_jump_the_question(self):
        if not self.lifelines['jump-the-question']:
            messagebox.showwarning('Lifeline Used', 'You have already used this lifeline.')
            return

        self.lifelines['jump-the-question'] = False
        self.jump_the_question_btn.config(state='disabled', bg='gray')

        if self.timer:
            self.root.after_cancel(self.timer)
            self.timer = None

        self.current_level += 1
        if self.current_level > 15:
            messagebox.showinfo('Congratulations!', 'You win!')
            return

        self.next_question()


if __name__ == '__main__':
    questions = load_questions('qna.csv')
    root = tk.Tk()
    game = MillionaireGame(root, questions)
    root.mainloop()