import tkinter as tk
from tkinter import messagebox
import random
import pygame
from pygame.locals import *

class CatchTheBallGame:
    def __init__(self, master):
        self.master = master
        self.master.title("Catch the Ball Game")

        self.canvas_width = 400
        self.canvas_height = 400

        self.canvas = tk.Canvas(self.master, width=self.canvas_width, height=self.canvas_height, bg='black')
        self.canvas.pack()

        self.bar_width = 80
        self.bar_height = 10
        self.bar_x = self.canvas_width // 2 - self.bar_width // 2
        self.bar_y = self.canvas_height - self.bar_height - 10
        self.bar = self.canvas.create_rectangle(self.bar_x, self.bar_y, self.bar_x + self.bar_width, self.bar_y + self.bar_height, fill='white')

        self.score = 0
        self.score_label = tk.Label(self.master, text=f"Score: {self.score}", fg='white', bg='black')
        self.score_label.pack()

        self.ball_radius = 10
        self.ball = None
        self.ball_speed = 5
        #bar speed
        self.bar_speed = 25 

        self.game_over = False

        self.move_left_flag = False
        self.move_right_flag = False

        self.master.bind("<Left>", self.start_move_left)
        self.master.bind("<Right>", self.start_move_right)
        self.master.bind("<KeyRelease-Left>", self.stop_move_left)
        self.master.bind("<KeyRelease-Right>", self.stop_move_right)

        self.load_music()
        self.load_game_over_sound()
        self.start_game()

    def load_music(self):
        pygame.mixer.init()
        pygame.mixer.music.load("Starman Theme.mp3")  # Background music file
        pygame.mixer.music.play(-1)  # -1 for loop

    def load_game_over_sound(self):
        self.game_over_sound = pygame.mixer.Sound("death.mp3")  # Game over sound file

    def start_game(self):
        self.create_ball()
        self.move_ball()
        self.move_bar()
        self.check_color_change()

    def create_ball(self):
        if not self.game_over:
            x = random.randint(self.ball_radius, self.canvas_width - self.ball_radius)
            self.ball = self.canvas.create_oval(x - self.ball_radius, 0, x + self.ball_radius, self.ball_radius * 2, fill='white')

    def move_ball(self):
        if not self.game_over:
            self.canvas.move(self.ball, 0, self.ball_speed)
            ball_coords = self.canvas.coords(self.ball)
            bar_coords = self.canvas.coords(self.bar)
            if ball_coords[3] >= bar_coords[1] and ball_coords[2] >= bar_coords[0] and ball_coords[0] <= bar_coords[2]:
                self.score += 1
                self.score_label.config(text=f"Score: {self.score}")
                self.canvas.delete(self.ball)
                self.create_ball()
                self.increase_speed()
            elif ball_coords[3] >= self.canvas_height:
                self.game_over = True
                self.end_game()

            self.master.after(50, self.move_ball)

    def increase_speed(self):
        self.ball_speed += 1

    def start_move_left(self, event):
        if not self.game_over:
            self.move_left_flag = True

    def start_move_right(self, event):
        if not self.game_over:
            self.move_right_flag = True

    def stop_move_left(self, event):
        self.move_left_flag = False

    def stop_move_right(self, event):
        self.move_right_flag = False

    def move_bar(self):
        if not self.game_over:
            if self.move_left_flag and self.bar_x > 0:
                self.canvas.move(self.bar, -self.bar_speed, 0)
                self.bar_x -= self.bar_speed
            if self.move_right_flag and self.bar_x + self.bar_width < self.canvas_width:
                self.canvas.move(self.bar, self.bar_speed, 0)
                self.bar_x += self.bar_speed

            self.master.after(100, self.move_bar)

    def check_color_change(self):
        if self.score % 5 == 0:
            self.change_color_scheme()

    def change_color_scheme(self):
        bg_color = self.canvas.cget('bg')
        if bg_color == 'black':
            bg_color = "black"

    def end_game(self):
        pygame.mixer.music.stop()
        self.game_over_sound.play()
        messagebox.showinfo("Game Over", f"Your final score is: {self.score}")
        self.score_label.config(text="Game Over!")


def main():
    root = tk.Tk()
    game = CatchTheBallGame(root)
    root.mainloop()

if __name__ == "__main__":
    main()
