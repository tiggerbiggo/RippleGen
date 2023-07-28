import tkinter as tk
from PIL import Image, ImageTk
import random
from SinImaGenClean import make_random_image, animate_phase

# This is the script that makes the GUI.
# You set the image size and the GUI grid width and height
# If you use larger images you have to make the grid smaller
# or else you won't be able to click the refresh button!

class ImageGridApp:
    
    
    def __init__(self, root):
        self.root = root
        self.image_count = 60
        self.buttons = []
        self.images = []
        self.image_size = (256, 256)
        self.grid_x = 3
        self.grid_y = 3
        
        for _ in range(self.grid_x * self.grid_y):
            image, params = make_random_image(self.image_size)
            self.images.append((image, params))

        self.create_grid()

    def create_grid(self):
        for i in range(self.grid_x):
            for j in range(self.grid_y):
                idx = i * self.grid_x + j
                image, params = self.images[idx]

                img = ImageTk.PhotoImage(image)
                button = tk.Button(self.root, image=img, command=lambda n=idx: self.animate(n))
                button.image = img
                button.grid(row=i, column=j)
                self.buttons.append(button)

        # Randomize button
        randomize_btn = tk.Button(self.root, text="Randomize", command=self.randomize_images)
        randomize_btn.grid(row=self.grid_y, column=0, columnspan=4)

    def animate(self, idx):
        _, params = self.images[idx]
        animate_phase(params, self.image_count, self.image_size)

    def randomize_images(self):
        self.images = []
        for _ in range(self.grid_x * self.grid_y):  # Change this number for a different grid size
            image, params = make_random_image(self.image_size)
            self.images.append((image, params))

        # Update the grid with the new images
        for i in range(self.grid_x):
            for j in range(self.grid_y):
                idx = i * self.grid_x + j
                image, params = self.images[idx]
                img = ImageTk.PhotoImage(image)
                self.buttons[idx].config(image=img)
                self.buttons[idx].image = img

if __name__ == "__main__":
    root = tk.Tk()
    root.title("Image Grid App")
    app = ImageGridApp(root)
    root.mainloop()
