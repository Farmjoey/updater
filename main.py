import tkinter as tk
from tkinter import ttk
import pyautogui
import time
import json
import os
import keyboard
import threading

try:
    import customtkinter as ctk
    USE_CTK = True
except ImportError:
    USE_CTK = False

class ItemScheduler:
    def __init__(self, root):
        self.root = root
        self.root.title("Item Scheduler")
        self.root.geometry("550x750") 
        self.root.resizable(True, True)
        

        self.bg_color = "#2c3e50"
        self.fg_color = "#ecf0f1"
        self.accent_color = "#3498db"
        
        if not USE_CTK:
            self.root.configure(bg=self.bg_color)
        

        self.status_var = tk.StringVar()
        self.status_var.set("Ready")
        

        self.animation_active = False
        self.animation_frames = ["⚡", "⚡⚡", "⚡⚡⚡", "⚡⚡", "⚡"]
        self.animation_index = 0
        

        self.data_file = "items.json"
        self.items = self.load_items()
        
        self.create_widgets()
    
    def load_items(self):
        if os.path.exists(self.data_file):
            try:
                with open(self.data_file, 'r') as f:
                    return json.load(f)
            except:
                return []
        return []
    
    def save_items(self):
        with open(self.data_file, 'w') as f:
            json.dump(self.items, f)
    
    def create_widgets(self):

        if USE_CTK:
            main_container = ctk.CTkFrame(self.root)
        else:
            main_container = tk.Frame(self.root, bg=self.bg_color)
        main_container.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        

        if USE_CTK:
            title_frame = ctk.CTkFrame(main_container)
        else:
            title_frame = tk.Frame(main_container, bg=self.bg_color)
        title_frame.pack(pady=10, fill=tk.X)
        
        if USE_CTK:
            self.animation_label = ctk.CTkLabel(
                title_frame, 
                text="", 
                font=("Helvetica", 18)
            )
            self.animation_label.pack(side=tk.LEFT, padx=10)
            
            title_label = ctk.CTkLabel(
                title_frame, 
                text="Item Scheduler", 
                font=("Helvetica", 22, "bold")
            )
        else:
            self.animation_label = tk.Label(
                title_frame, 
                text="", 
                font=("Helvetica", 18),
                bg=self.bg_color,
                fg="#f39c12"
            )
            self.animation_label.pack(side=tk.LEFT, padx=10)
            
            title_label = tk.Label(
                title_frame, 
                text="Item Scheduler", 
                font=("Helvetica", 22, "bold"),
                bg=self.bg_color,
                fg=self.fg_color
            )
        title_label.pack(pady=10)
        

        if USE_CTK:
            quick_label = ctk.CTkLabel(
                main_container,
                text="Quick Access:",
                font=("Helvetica", 12, "bold")
            )
        else:
            quick_label = tk.Label(
                main_container,
                text="Quick Access:",
                font=("Helvetica", 12, "bold"),
                bg=self.bg_color,
                fg=self.fg_color
            )
        quick_label.pack(anchor=tk.W, padx=15, pady=(10, 5))
        
        if USE_CTK:
            top_frame = ctk.CTkFrame(main_container)
        else:
            top_frame = tk.Frame(main_container, bg=self.bg_color)
        top_frame.pack(pady=5, padx=15, fill=tk.X)
        

        button_width = 100 if USE_CTK else 10
        
        if USE_CTK:
            clear_inventory_button = ctk.CTkButton(
                top_frame, 
                text="🧹 Clear", 
                width=button_width,
                fg_color="#e67e22",
                hover_color="#d35400",
                command=lambda: self.run_command("clearinventory", 0)
            )
            give_m1911_button = ctk.CTkButton(
                top_frame, 
                text="🔫 Gun", 
                width=button_width,
                fg_color="#9b59b6",
                hover_color="#8e44ad",
                command=lambda: self.run_command("m1911", 1)
            )
            give_goldenskateboard_button = ctk.CTkButton(
                top_frame, 
                text="🛹 Golden", 
                width=button_width,
                fg_color="#f1c40f",
                hover_color="#f39c12",
                text_color="#000000",
                command=lambda: self.run_command("goldenskateboard", 1)
            )
        else:
            clear_inventory_button = tk.Button(
                top_frame, 
                text="🧹 Clear", 
                width=button_width,
                command=lambda: self.run_command("clearinventory", 0),
                bg="#e67e22",
                fg=self.fg_color
            )
            give_m1911_button = tk.Button(
                top_frame, 
                text="🔫 Gun", 
                width=button_width,
                command=lambda: self.run_command("m1911", 1),
                bg="#9b59b6",
                fg=self.fg_color
            )
            give_goldenskateboard_button = tk.Button(
                top_frame, 
                text="🛹 Golden", 
                width=button_width,
                command=lambda: self.run_command("goldenskateboard", 1),
                bg="#f1c40f",
                fg="#000000"
            )
        
        clear_inventory_button.pack(side="left", padx=5, pady=5)
        give_m1911_button.pack(side="left", padx=5, pady=5)
        give_goldenskateboard_button.pack(side="left", padx=5, pady=5)
        

        if USE_CTK:
            add_label = ctk.CTkLabel(
                main_container,
                text="Add New Item:",
                font=("Helvetica", 12, "bold")
            )
        else:
            add_label = tk.Label(
                main_container,
                text="Add New Item:",
                font=("Helvetica", 12, "bold"),
                bg=self.bg_color,
                fg=self.fg_color
            )
        add_label.pack(anchor=tk.W, padx=15, pady=(15, 5))
        
        if USE_CTK:
            add_frame = ctk.CTkFrame(main_container)
        else:
            add_frame = tk.Frame(main_container, bg=self.bg_color)
        add_frame.pack(pady=5, fill=tk.X, padx=15)
        
        if USE_CTK:
            item_label = ctk.CTkLabel(
                add_frame, 
                text="Item Name:",
                width=80
            )
            self.item_entry = ctk.CTkEntry(add_frame, width=300, placeholder_text="Enter item name...")
            add_button = ctk.CTkButton(
                add_frame,
                text="Add Item",
                width=100,
                command=self.add_item
            )
        else:
            item_label = tk.Label(
                add_frame, 
                text="Item Name:", 
                bg=self.bg_color, 
                fg=self.fg_color,
                width=10
            )
            self.item_entry = tk.Entry(add_frame, width=40)
            add_button = tk.Button(
                add_frame,
                text="Add Item",
                command=self.add_item,
                bg=self.accent_color,
                fg=self.fg_color,
                padx=10
            )
        
        item_label.pack(side=tk.LEFT, padx=5, pady=5)
        self.item_entry.pack(side=tk.LEFT, padx=5, pady=5, expand=True, fill=tk.X)
        add_button.pack(side=tk.LEFT, padx=5, pady=5)
        

        if USE_CTK:
            list_label = ctk.CTkLabel(
                main_container,
                text="Your Items:",
                font=("Helvetica", 12, "bold")
            )
        else:
            list_label = tk.Label(
                main_container,
                text="Your Items:",
                font=("Helvetica", 12, "bold"),
                bg=self.bg_color,
                fg=self.fg_color
            )
        list_label.pack(anchor=tk.W, padx=15, pady=(15, 5))
        

        if USE_CTK:
            list_frame = ctk.CTkFrame(main_container)
        else:
            list_frame = tk.Frame(main_container, bg=self.bg_color)
        list_frame.pack(pady=5, fill=tk.BOTH, expand=True, padx=15)
        

        if USE_CTK:
            self.items_canvas = tk.Canvas(list_frame, bg="#2b2b2b", highlightthickness=0)
        else:
            self.items_canvas = tk.Canvas(list_frame, bg="#34495e", highlightthickness=0)
        

        if USE_CTK:
            self.items_frame = tk.Frame(self.items_canvas, bg="#2b2b2b")
        else:
            self.items_frame = tk.Frame(self.items_canvas, bg="#34495e")
        

        self.items_canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        

        self.canvas_window = self.items_canvas.create_window((0, 0), window=self.items_frame, anchor=tk.NW)
        

        self.items_frame.bind("<Configure>", self._on_frame_configure)
        list_frame.bind("<Configure>", self._on_list_frame_configure)
        

        self.items_canvas.bind_all("<MouseWheel>", self._on_mousewheel)  
        self.items_canvas.bind_all("<Button-4>", self._on_mousewheel)    
        self.items_canvas.bind_all("<Button-5>", self._on_mousewheel)    
        

        self.update_item_list()
        

        if USE_CTK:
            settings_frame = ctk.CTkFrame(main_container)
        else:
            settings_frame = tk.Frame(main_container, bg=self.bg_color)
        settings_frame.pack(pady=5, padx=15, fill=tk.X)
        
        if USE_CTK:
            key_label = ctk.CTkLabel(
                settings_frame,
                text="Special Key:",
                width=80
            )
            self.special_key = tk.StringVar(value="æ")
            self.key_entry = ctk.CTkEntry(settings_frame, width=50, textvariable=self.special_key)
            

            qty_label = ctk.CTkLabel(
                settings_frame,
                text="Default Quantity:",
                width=120
            )
            self.default_qty = tk.StringVar(value="20")
            self.qty_entry = ctk.CTkEntry(settings_frame, width=50, textvariable=self.default_qty)
        else:
            key_label = tk.Label(
                settings_frame,
                text="Special Key:",
                bg=self.bg_color,
                fg=self.fg_color,
                width=10
            )
            self.special_key = tk.StringVar(value="æ")
            self.key_entry = tk.Entry(settings_frame, textvariable=self.special_key, width=5)
            

            qty_label = tk.Label(
                settings_frame,
                text="Default Quantity:",
                bg=self.bg_color,
                fg=self.fg_color,
                width=15
            )
            self.default_qty = tk.StringVar(value="20")
            self.qty_entry = tk.Entry(settings_frame, textvariable=self.default_qty, width=5)
        
        key_label.pack(side=tk.LEFT, padx=5, pady=5)
        self.key_entry.pack(side=tk.LEFT, padx=5, pady=5)
        qty_label.pack(side=tk.LEFT, padx=(20, 5), pady=5)
        self.qty_entry.pack(side=tk.LEFT, padx=5, pady=5)
        

        if USE_CTK:
            status_frame = ctk.CTkFrame(self.root, height=25)
        else:
            status_frame = tk.Frame(self.root, bg="#1a252f", height=25)
        status_frame.pack(side=tk.BOTTOM, fill=tk.X)
        
        if USE_CTK:
            status_label = ctk.CTkLabel(
                status_frame,
                textvariable=self.status_var,
                anchor="w",
                padx=10,
                pady=2
            )
        else:
            status_label = tk.Label(
                status_frame,
                textvariable=self.status_var,
                bg="#1a252f",
                fg=self.fg_color,
                anchor=tk.W,
                padx=10,
                pady=2
            )
        status_label.pack(fill=tk.X)
    
    def _on_frame_configure(self, event):

        self.items_canvas.configure(scrollregion=self.items_canvas.bbox("all"))
    
    def _on_list_frame_configure(self, event):

        self.items_canvas.itemconfig(self.canvas_window, width=event.width)
    
    def _on_mousewheel(self, event):

        if event.num == 4 or event.delta > 0:  
            self.items_canvas.yview_scroll(-1, "units")
        elif event.num == 5 or event.delta < 0:  
            self.items_canvas.yview_scroll(1, "units")
    
    def update_item_list(self):
 
        for widget in self.items_frame.winfo_children():
            widget.destroy()
        

        for i, item in enumerate(self.items):

            if USE_CTK:
                item_row = tk.Frame(self.items_frame, bg="#2b2b2b")
            else:
                item_row = tk.Frame(self.items_frame, bg="#34495e")
            item_row.pack(fill=tk.X, padx=5, pady=2)
            

            if USE_CTK:
                label_bg = "#2b2b2b"
                label_fg = "white"
            else:
                label_bg = "#34495e"
                label_fg = self.fg_color
                
            item_label = tk.Label(
                item_row,
                text=item,
                font=("Helvetica", 12),
                anchor=tk.W,
                bg=label_bg,
                fg=label_fg,
                padx=5
            )
            item_label.pack(side=tk.LEFT, fill=tk.X, expand=True)
            

            if USE_CTK:
                exec_btn = tk.Button(
                    item_row,
                    text="Execute",
                    bg="#2ecc71",
                    fg="white",
                    padx=8,
                    pady=2,
                    bd=0,
                    command=lambda item=item: self.run_command(item, int(self.default_qty.get()))
                )
            else:
                exec_btn = tk.Button(
                    item_row,
                    text="Execute",
                    bg="#2ecc71",
                    fg="white",
                    padx=8,
                    pady=2,
                    bd=0,
                    command=lambda item=item: self.run_command(item, int(self.default_qty.get()))
                )
            exec_btn.pack(side=tk.RIGHT, padx=(5, 0))
            

            if USE_CTK:
                remove_btn = tk.Button(
                    item_row,
                    text="Remove",
                    bg="#e74c3c",
                    fg="white",
                    padx=8,
                    pady=2,
                    bd=0,
                    command=lambda item=item: self.remove_specific_item(item)
                )
            else:
                remove_btn = tk.Button(
                    item_row,
                    text="Remove",
                    bg="#e74c3c",
                    fg="white",
                    padx=8,
                    pady=2,
                    bd=0,
                    command=lambda item=item: self.remove_specific_item(item)
                )
            remove_btn.pack(side=tk.RIGHT, padx=5)
    
    def start_animation(self):
        if not self.animation_active:
            self.animation_active = True
            self.animate()
    
    def stop_animation(self):
        self.animation_active = False
        self.animation_label.configure(text="")
    
    def animate(self):
        if self.animation_active:
            self.animation_label.configure(text=self.animation_frames[self.animation_index])
            self.animation_index = (self.animation_index + 1) % len(self.animation_frames)
            self.root.after(150, self.animate)
    
    def update_status(self, message):
        self.status_var.set(message)
        self.root.update_idletasks()
    
    def add_item(self):
        item_name = self.item_entry.get().strip()
        if item_name:
            if item_name not in self.items:

                self.start_animation()
                
                self.items.append(item_name)
                self.save_items()
                self.update_item_list()
                self.item_entry.delete(0, tk.END)
                self.update_status(f"Added item: {item_name}")
                

                self.root.after(1000, self.stop_animation)
            else:
                self.update_status(f"Item '{item_name}' already exists")
        else:
            self.update_status("Please enter an item name")
    
    def remove_specific_item(self, item_name):

        self.start_animation()
        
        self.items.remove(item_name)
        self.save_items()
        self.update_item_list()
        self.update_status(f"Removed item: {item_name}")
        

        self.root.after(1000, self.stop_animation)
    
    def remove_item(self):

        self.update_status("Use the Remove button next to the item")
    
    def execute_command(self):

        self.update_status("Use the Execute button next to the item")
    
    def run_command(self, item_name, quantity):

        self.start_animation()
        
        self.update_status(f"Executing command for: {item_name}")
        

        threading.Thread(target=self._execute_command_thread, args=(item_name, quantity)).start()
    
    def _execute_command_thread(self, item_name, quantity):
        try:

            window = pyautogui.getWindowsWithTitle("Schedule I")
            
            if window:

                window[0].activate()
                time.sleep(1)  
                

                special_key = self.special_key.get()
                keyboard.press_and_release(special_key)
                time.sleep(0.5)
                

                if quantity > 0:
                    command = f"give {item_name} {quantity}"
                else:
                    command = f"{item_name}" 
                
                pyautogui.write(command)
                time.sleep(0.2)
                pyautogui.press('enter')
                

                self.root.after(0, lambda: self.update_status(f"Command executed: {command}"))
            else:

                self.root.after(0, lambda: self.update_status("Error: Could not find 'Schedule I' window"))
                
        except Exception as e:

            self.root.after(0, lambda: self.update_status(f"Error: {str(e)}"))
        

        self.root.after(1000, self.stop_animation)

if __name__ == "__main__":
    if USE_CTK:
        ctk.set_appearance_mode("dark")
        ctk.set_default_color_theme("blue")
        root = ctk.CTk()
    else:
        root = tk.Tk()
    
    app = ItemScheduler(root)
    root.mainloop()