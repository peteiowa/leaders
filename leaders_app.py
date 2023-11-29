
import random
import tkinter as tk
import time
from datetime import datetime, timedelta

from selenium import webdriver

class TimerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Leaders")

        self.is_running = False
        self.start_time = None
        self.elapsed_time = 0
        self.visit_counter = 0
        
        
        self.visit_counter_label = tk.Label(self.root, text="Visits counter: 0", font=("Arial", 12))
        self.visit_counter_label.pack(pady=10,padx=30)
                
        self.next_visit_label = tk.Label(self.root, text="Time to Next Visit:", font=("Arial", 10))
        self.next_visit_time_label = tk.Label(self.root, text="", font=("Arial", 10))

        self.timer_label = tk.Label(self.root, text="Running time: 0 min", font=("Arial", 10))
        self.timer_label.pack(pady=10)
                  
        self.min_label = tk.Label(self.root, text="Minimum (10-59):")
        self.min_label.pack()
        
        self.min_entry = tk.Entry(self.root)
        self.min_entry.insert(tk.END, '25') 
        self.min_entry.pack()

        self.max_label = tk.Label(self.root, text="Maximum (11-60):")
        self.max_label.pack()
        
        self.max_entry = tk.Entry(self.root)
        self.max_entry.insert(tk.END, '45') 
        self.max_entry.pack()
        
        self.start_stop_button = tk.Button(self.root, text="Start",font=("Arial", 10), command=self.start_stop_timer,width=10,height=2)
        self.start_stop_button.pack(pady=10)
               
        
    def start_stop_timer(self):
        if not self.is_running:
            self.is_running = True
            self.start_time = time.time() - self.elapsed_time
            self.start_stop_button.config(text="Stop")
            self.launchBrowser()
            self.next_visit_label.pack(pady=5)
            self.next_visit_time_label.pack(pady=5)
            self.update_timer()
        else:
            self.is_running = False
            self.start_stop_button.config(text="Start")
            self.next_visit_label.pack_forget() # hide
            self.next_visit_time_label.pack_forget()

    def update_timer(self):
        if self.is_running:
            self.elapsed_time = time.time() - self.start_time
            self.timer_label.config(text=f"Runing: {int(self.elapsed_time/60)} min.")
            self.root.after(60*1000, self.update_timer)  # Update every second
            
    def generate_random_number(self):
        random_minutes = 33
        min_value = int(self.min_entry.get()) 
        max_value = int(self.max_entry.get()) 
        
        if self.is_valid_input(self.min_entry.get(), 10, 59) is False:
            self.min_entry.delete(0)
            self.min_entry.insert(0, '25') 
            min_value = 25
            
        if self.is_valid_input(self.max_entry.get(), 11, 60) is False:
            self.max_entry.delete(0)
            self.max_entry.insert(0, '45') 
            max_value = 45
        
        if min_value < max_value:
            random_minutes = random.randint(min_value, max_value)
        else:
            self.min_entry.delete(0)
            self.min_entry.insert(0, '25') 
            self.max_entry.delete(0)
            self.max_entry.insert(0, '45') 
           
        return random_minutes 
            
    def prepare_next_visit_time(self):
        random_minutes = self.generate_random_number()
        # print(f"Random number of minutes: {random_minutes}")
        current_time = datetime.now()
        time_to_next_visit = current_time + timedelta(minutes=random_minutes)
        formatted_time = time_to_next_visit.strftime("%d-%m-%Y %H:%M:%S")
        self.next_visit_time_label.config(text=f"{formatted_time}")
        return random_minutes * 60 * 1000
    
    def is_valid_input(self, value, min_val, max_val):
        if value.isdigit():
            num_value = int(value)
            return min_val <= num_value <= max_val
        return False
    
    def launchBrowser(self):
        if self.is_running:
            options = webdriver.ChromeOptions()
            options.add_argument("disable-infobars")
            # options.add_argument('--ignore-certificate-errors')
            options.add_argument("--incognito")
            options.add_experimental_option('excludeSwitches', ['enable-logging'])
            urls = [
                "https://equalleadership.eu",
                "https://equalleadership.eu/news",
                "https://equalleadership.eu/about"
            ]
            url = random.choice(urls)
            driver = webdriver.Chrome(options=options)
            driver.get(url)    
           
            
            self.visit_counter=self.visit_counter+1
            self.visit_counter_label.config(text=f"Visits counter: {int(self.visit_counter)}")
            next_visit_time = self.prepare_next_visit_time()
            time.sleep(4) # Let the user actually see something!
            driver.quit()
            

            self.root.after(next_visit_time,self.launchBrowser)
                         


def main():
    root = tk.Tk()
    app = TimerApp(root)
    root.mainloop()

if __name__ == "__main__":
    main()