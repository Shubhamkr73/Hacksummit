import tkinter as tk
from tkinter import messagebox, ttk
from datetime import datetime
import threading
import time

class SimpleTrespassingApp:
    def __init__(self):
        # Create the main window manually
        self.root = tk.Tk()
        self.root.title("Trespassing Detection")
        self.root.geometry("800x600")
        self.setup_ui()
        
    def setup_ui(self):
        # Simple header
        header = tk.Frame(self.root, bg="#1e3a8a", padx=10, pady=10)
        header.pack(fill="x")
        
        tk.Label(
            header, 
            text="Trespassing Detection System", 
            font=("Arial", 18, "bold"),
            fg="white",
            bg="#1e3a8a"
        ).pack()
        
        # Main content - split into two panels
        content = tk.PanedWindow(self.root, orient=tk.HORIZONTAL)
        content.pack(fill="both", expand=True, padx=10, pady=10)
        
        # Left panel - Camera setup
        left_frame = tk.LabelFrame(content, text="Camera Setup", padx=10, pady=10)
        content.add(left_frame)
        
        # Number of cameras
        camera_frame = tk.Frame(left_frame)
        camera_frame.pack(fill="x", pady=5)
        
        tk.Label(camera_frame, text="Number of cameras:").pack(side="left")
        self.num_cameras = tk.Spinbox(camera_frame, from_=1, to=10, width=5)
        self.num_cameras.pack(side="left", padx=5)
        
        tk.Button(
            camera_frame, 
            text="Update", 
            bg="#2563eb", 
            fg="white",
            command=self.update_cameras
        ).pack(side="left", padx=5)
        
        # Camera list container
        self.camera_container = tk.Frame(left_frame)
        self.camera_container.pack(fill="both", expand=True, pady=10)
        
        # Save button
        tk.Button(
            left_frame, 
            text="Save Configuration", 
            bg="#10b981", 
            fg="white",
            padx=10,
            pady=5,
            command=self.save_config
        ).pack(pady=10)
        
        # Right panel - Monitoring
        right_frame = tk.LabelFrame(content, text="Monitoring", padx=10, pady=10)
        content.add(right_frame)
        
        # Control buttons
        control_frame = tk.Frame(right_frame)
        control_frame.pack(fill="x", pady=5)
        
        self.start_button = tk.Button(
            control_frame, 
            text="Start Monitoring", 
            bg="#10b981", 
            fg="white",
            padx=10,
            pady=5,
            command=self.toggle_monitoring
        )
        self.start_button.pack(side="left", padx=5)
        
        tk.Button(
            control_frame, 
            text="Test Alert", 
            bg="#f59e0b", 
            fg="white",
            padx=10,
            pady=5,
            command=self.test_alert
        ).pack(side="left", padx=5)
        
        # Status
        status_frame = tk.Frame(right_frame)
        status_frame.pack(fill="x", pady=10)
        
        tk.Label(status_frame, text="Status:").pack(side="left")
        self.status_var = tk.StringVar(value="Not Monitoring")
        tk.Label(status_frame, textvariable=self.status_var, fg="red").pack(side="left", padx=5)
        
        # Log area
        tk.Label(right_frame, text="System Logs:").pack(anchor="w")
        self.log_area = tk.Text(right_frame, height=15, width=40)
        self.log_area.pack(fill="both", expand=True)
        
        # Initialize
        self.is_monitoring = False
        self.cameras = []
        self.camera_entries = []
        self.update_cameras()
        self.add_log("System initialized")
    
    def update_cameras(self):
        # Clear existing entries
        for widget in self.camera_container.winfo_children():
            widget.destroy()
        
        try:
            num = int(self.num_cameras.get())
        except:
            num = 1
            
        self.camera_entries = []
        
        # Create camera entries
        for i in range(num):
            frame = tk.Frame(self.camera_container)
            frame.pack(fill="x", pady=2)
            
            tk.Label(frame, text=f"Camera {i+1}:").pack(side="left")
            name_entry = tk.Entry(frame, width=15)
            name_entry.pack(side="left", padx=5)
            name_entry.insert(0, f"Camera {i+1}")
            
            tk.Label(frame, text="URL:").pack(side="left", padx=5)
            url_entry = tk.Entry(frame, width=30)
            url_entry.pack(side="left")
            
            self.camera_entries.append((name_entry, url_entry))
        
        self.add_log(f"Updated to {num} cameras")
    
    def save_config(self):
        self.cameras = []
        for name_entry, url_entry in self.camera_entries:
            name = name_entry.get()
            url = url_entry.get()
            if name and url:
                self.cameras.append((name, url))
        
        count = len(self.cameras)
        self.add_log(f"Saved {count} camera configurations")
        messagebox.showinfo("Saved", f"{count} cameras configured")
    
    def toggle_monitoring(self):
        if not self.is_monitoring:
            if not self.cameras:
                messagebox.showwarning("Warning", "No cameras configured")
                return
                
            self.is_monitoring = True
            self.start_button.config(text="Stop Monitoring", bg="#ef4444")
            self.status_var.set("Monitoring Active")
            self.add_log("Monitoring started")
            
            # Start monitoring thread
            threading.Thread(target=self.run_monitoring, daemon=True).start()
        else:
            self.is_monitoring = False
            self.start_button.config(text="Start Monitoring", bg="#10b981")
            self.status_var.set("Not Monitoring")
            self.add_log("Monitoring stopped")
    
    def run_monitoring(self):
        while self.is_monitoring:
            # Simulate detection (in real app, this would check camera feeds)
            time.sleep(5)
            if self.is_monitoring and datetime.now().second % 20 == 0:
                self.add_log("⚠️ ALERT: Trespassing detected!", is_alert=True)
    
    def test_alert(self):
        self.add_log("⚠️ TEST ALERT: This is a test alert", is_alert=True)
        messagebox.showinfo("Test", "Test alert generated")
    
    def add_log(self, message, is_alert=False):
        timestamp = datetime.now().strftime("%H:%M:%S")
        log_entry = f"[{timestamp}] {message}\n"
        
        self.log_area.configure(state="normal")
        
        if is_alert:
            self.log_area.insert("end", log_entry, "alert")
            self.log_area.tag_configure("alert", foreground="red", font=("Arial", 10, "bold"))
        else:
            self.log_area.insert("end", log_entry)
            
        self.log_area.configure(state="disabled")
        self.log_area.see("end")
    
    def run(self):
        self.root.mainloop()

# Create and run the application
if __name__ == "__main__":
    app = SimpleTrespassingApp()
    app.run()