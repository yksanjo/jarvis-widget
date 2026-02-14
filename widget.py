#!/usr/bin/env python3
"""
Jarvis Widget - Floating Desktop Assistant
A lightweight, always-on-top desktop widget
"""

import tkinter as tk
from tkinter import ttk, messagebox
import json
import os
from datetime import datetime
from typing import List, Dict, Any

# Data storage
DATA_FILE = os.path.expanduser("~/.jarvis_widget_data.json")

class JarvisWidget:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("🤖 Jarvis")
        self.root.geometry("300x400")
        self.root.attributes('-topmost', True)  # Always on top
        self.root.configure(bg='#1E1E1E')
        
        # Make window draggable
        self.x = 0
        self.y = 0
        
        self.data = self.load_data()
        self.setup_ui()
        
    def load_data(self) -> Dict[str, Any]:
        """Load data from JSON file"""
        if os.path.exists(DATA_FILE):
            try:
                with open(DATA_FILE, 'r') as f:
                    return json.load(f)
            except:
                pass
        return {"tasks": [], "messages": []}
    
    def save_data(self):
        """Save data to JSON file"""
        with open(DATA_FILE, 'w') as f:
            json.dump(self.data, f, indent=2)
    
    def setup_ui(self):
        """Setup the UI components"""
        # Title bar
        title_frame = tk.Frame(self.root, bg='#2D2D2D', cursor='fleur')
        title_frame.pack(fill=tk.X)
        title_frame.bind('<Button-1>', self.start_move)
        title_frame.bind('<B1-Motion>', self.do_move)
        
        title_label = tk.Label(
            title_frame, 
            text="🤖 Jarvis Widget",
            bg='#2D2D2D',
            fg='#FFFFFF',
            font=('Arial', 10, 'bold')
        )
        title_label.pack(side=tk.LEFT, padx=10, pady=5)
        
        close_btn = tk.Button(
            title_frame,
            text='✕',
            bg='#2D2D2D',
            fg='#FFFFFF',
            bd=0,
            command=self.root.destroy,
            font=('Arial', 10)
        )
        close_btn.pack(side=tk.RIGHT, padx=5)
        
        # Task input
        input_frame = tk.Frame(self.root, bg='#1E1E1E')
        input_frame.pack(fill=tk.X, padx=10, pady=10)
        
        self.task_entry = tk.Entry(
            input_frame,
            bg='#3D3D3D',
            fg='#FFFFFF',
            bd=0,
            insertbackground='#FFFFFF'
        )
        self.task_entry.pack(fill=tk.X)
        self.task_entry.bind('<Return>', self.add_task)
        
        add_btn = tk.Button(
            input_frame,
            text='+ Add Task',
            bg='#4A90D9',
            fg='#FFFFFF',
            bd=0,
            command=self.add_task,
            font=('Arial', 9)
        )
        add_btn.pack(fill=tk.X, pady=(5, 0))
        
        # Tasks list
        list_frame = tk.Frame(self.root, bg='#1E1E1E')
        list_frame.pack(fill=tk.BOTH, expand=True, padx=10)
        
        tasks_label = tk.Label(
            list_frame,
            text="📋 Tasks",
            bg='#1E1E1E',
            fg='#FFFFFF',
            font=('Arial', 10, 'bold')
        )
        tasks_label.pack(anchor=tk.W)
        
        self.tasks_listbox = tk.Listbox(
            list_frame,
            bg='#2D2D2D',
            fg='#FFFFFF',
            bd=0,
            highlightthickness=0,
            selectbackground='#4A90D9'
        )
        self.tasks_listbox.pack(fill=tk.BOTH, expand=True)
        self.refresh_tasks()
        
        # Chat input
        chat_frame = tk.Frame(self.root, bg='#1E1E1E')
        chat_frame.pack(fill=tk.X, padx=10, pady=10)
        
        self.chat_entry = tk.Entry(
            chat_frame,
            bg='#3D3D3D',
            fg='#FFFFFF',
            bd=0,
            insertbackground='#FFFFFF'
        )
        self.chat_entry.pack(fill=tk.X)
        self.chat_entry.bind('<Return>', self.send_chat)
        
        send_btn = tk.Button(
            chat_frame,
            text='💬 Send',
            bg='#4A90D9',
            fg='#FFFFFF',
            bd=0,
            command=self.send_chat,
            font=('Arial', 9)
        )
        send_btn.pack(fill=tk.X, pady=(5, 0))
    
    def start_move(self, event):
        """Start window drag"""
        self.x = event.x
        self.y = event.y
    
    def do_move(self, event):
        """Move window"""
        deltax = event.x - self.x
        deltay = event.y - self.y
        x = self.root.winfo_x() + deltax
        y = self.root.winfo_y() + deltay
        self.root.geometry(f'+{x}+{y}')
    
    def add_task(self, event=None):
        """Add a new task"""
        title = self.task_entry.get().strip()
        if not title:
            return
        
        task = {
            "id": len(self.data["tasks"]) + 1,
            "title": title,
            "status": "pending",
            "created": datetime.now().isoformat()
        }
        self.data["tasks"].append(task)
        self.save_data()
        self.task_entry.delete(0, tk.END)
        self.refresh_tasks()
    
    def refresh_tasks(self):
        """Refresh tasks list"""
        self.tasks_listbox.delete(0, tk.END)
        for task in self.data["tasks"][:5]:  # Show only first 5
            status = "✅" if task["status"] == "completed" else "⬜"
            self.tasks_listbox.insert(tk.END, f"{status} {task['title']}")
    
    def send_chat(self, event=None):
        """Send chat message"""
        message = self.chat_entry.get().strip()
        if not message:
            return
        
        # Add user message
        self.data["messages"].append({
            "role": "user",
            "content": message,
            "timestamp": datetime.now().isoformat()
        })
        
        # Simulated response (connect to Ollama in production)
        responses = [
            f"I understand: '{message}'. How can I help?",
            f"Got it! Working on '{message}' now.",
            f"Message received! What else can I do?",
        ]
        import random
        response = random.choice(responses)
        
        self.data["messages"].append({
            "role": "assistant",
            "content": response,
            "timestamp": datetime.now().isoformat()
        })
        
        self.save_data()
        self.chat_entry.delete(0, tk.END)
        
        # Show notification
        messagebox.showinfo("🤖 Jarvis", response)
    
    def run(self):
        """Run the widget"""
        self.root.mainloop()

def main():
    widget = JarvisWidget()
    widget.run()

if __name__ == "__main__":
    main()
