import tkinter as tk
from tkinter import ttk, messagebox, StringVar
import requests
import json
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import pandas as pd
from datetime import datetime, timedelta
import os
from PIL import Image, ImageTk
import io
import matplotlib
matplotlib.use("TkAgg")
from matplotlib.figure import Figure
import numpy as np

class SpaceDataApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Space Data Visualization")
        self.root.geometry("1200x700")
        self.root.config(bg="#f0f0f0")
        
        # Set theme
        self.style = ttk.Style()
        self.style.theme_use("clam")
        self.style.configure("TFrame", background="#f0f0f0")
        self.style.configure("TButton", background="#4a7abc", foreground="black", font=("Arial", 10))
        self.style.configure("TLabel", background="#f0f0f0", foreground="#333333", font=("Arial", 10))
        self.style.configure("Heading.TLabel", background="#f0f0f0", foreground="#333333", font=("Arial", 14, "bold"))
        self.style.configure("TCombobox", font=("Arial", 10))
        
        # NASA API key
        self.nasa_api_key = "SwNFASswLUVy6UBkM7MGwimqKEpWgj9U3FR4HMx5"
        
        # Create main frames
        self.create_frames()
        
        # Create sidebar
        self.create_sidebar()
        
        # Create content area
        self.create_content_area()
        
        # Show home page by default
        self.show_home()
        
    def create_frames(self):
        # Main layout
        self.sidebar_frame = ttk.Frame(self.root, width=200, style="TFrame")
        self.sidebar_frame.pack(side=tk.LEFT, fill=tk.Y, padx=10, pady=10)
        
        self.content_frame = ttk.Frame(self.root, style="TFrame")
        self.content_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True, padx=10, pady=10)
        
    def create_sidebar(self):
        # App name
        ttk.Label(self.sidebar_frame, text="Space Data", font=("Arial", 16, "bold")).pack(pady=(0, 20))
        
        # Buttons
        buttons = [
            ("Home", self.show_home),
            ("NASA NEO Data", self.show_neo_page),
            ("NASA APOD", self.show_apod_page),
            ("Upcoming Launches", self.show_upcoming_launches),
            ("SpaceX Stats", self.show_spacex_stats),
            ("Space Agencies", self.show_space_agencies)
        ]
        
        for text, command in buttons:
            btn = ttk.Button(self.sidebar_frame, text=text, command=command, width=20)
            btn.pack(pady=5)
            
    def create_content_area(self):
        # Page title
        self.page_title = ttk.Label(self.content_frame, text="", style="Heading.TLabel")
        self.page_title.pack(pady=(0, 10), anchor=tk.W)
        
        # Content container
        self.content_container = ttk.Frame(self.content_frame, style="TFrame")
        self.content_container.pack(fill=tk.BOTH, expand=True)
        
        # Sub-menu container
        self.submenu_frame = ttk.Frame(self.content_container, style="TFrame")
        self.submenu_frame.pack(fill=tk.X, pady=(0, 10))
        
        # Visualization container
        self.visualization_frame = ttk.Frame(self.content_container, style="TFrame")
        self.visualization_frame.pack(fill=tk.BOTH, expand=True)
        
    def clear_content(self):
        # Clear submenu
        for widget in self.submenu_frame.winfo_children():
            widget.destroy()
            
        # Clear visualization
        for widget in self.visualization_frame.winfo_children():
            widget.destroy()
    
    def show_home(self):
        self.page_title.config(text="Space Visualization Dashboard")
        self.clear_content()
        
        # Welcome message
        welcome_frame = ttk.Frame(self.visualization_frame, style="TFrame")
        welcome_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        
        ttk.Label(welcome_frame, text="Welcome to Space Data Visualization", 
                 font=("Arial", 20, "bold")).pack(pady=(30, 20))
        
        ttk.Label(welcome_frame, text="Explore data from NASA, SpaceX, and other space agencies", 
                 font=("Arial", 14)).pack(pady=(0, 30))
        
        # Feature description
        features = [
            "NASA NEO Data - This refers to asteroids and comets whose orbits intersect or come close to the Earth's orbit.",
            "NASA APOD - Astronomy Picture of the Day with date selection",
            "Upcoming Launches - Details about upcoming space missions",
            "SpaceX Stats - Launch statistics and mission information",
            "Space Agencies - Information about various space organizations",
            "Keshav Aggarwal - 03914202022"
        ]
        
        for feature in features:
            ttk.Label(welcome_frame, text="• " + feature, font=("Arial", 12)).pack(anchor=tk.W, pady=5)
        
        ttk.Label(welcome_frame, text="Select an option from the sidebar to begin exploring", 
                 font=("Arial", 12, "italic")).pack(pady=(30, 10))
    
    def show_neo_page(self):
        self.page_title.config(text="NASA NEO (Near Earth Objects) Data")
        self.clear_content()
        
        # Dropdown for NEO visualization options
        ttk.Label(self.submenu_frame, text="Select Visualization:").pack(side=tk.LEFT, padx=(0, 10))
        
        neo_options = ["NEO Count by Date", "Hazardous vs Safe NEO"]
        neo_var = StringVar(value=neo_options[0])
        
        dropdown = ttk.Combobox(self.submenu_frame, textvariable=neo_var, values=neo_options, state="readonly", width=30)
        dropdown.pack(side=tk.LEFT)
        dropdown.bind("<<ComboboxSelected>>", lambda e: self.update_neo_visualization(neo_var.get()))
        
        # Date selection for NEO
        ttk.Label(self.submenu_frame, text="Start Date:").pack(side=tk.LEFT, padx=(20, 5))
        
        today = datetime.today()
        default_start = today - timedelta(days=7)
        
        start_date_var = StringVar(value=default_start.strftime("%Y-%m-%d"))
        start_date_entry = ttk.Entry(self.submenu_frame, textvariable=start_date_var, width=12)
        start_date_entry.pack(side=tk.LEFT)
        
        ttk.Label(self.submenu_frame, text="End Date:").pack(side=tk.LEFT, padx=(10, 5))
        
        end_date_var = StringVar(value=today.strftime("%Y-%m-%d"))
        end_date_entry = ttk.Entry(self.submenu_frame, textvariable=end_date_var, width=12)
        end_date_entry.pack(side=tk.LEFT)
        
        ttk.Button(self.submenu_frame, text="Fetch Data", 
                  command=lambda: self.update_neo_visualization(neo_var.get(), start_date_var.get(), end_date_var.get())).pack(side=tk.LEFT, padx=10)
        
        # Show initial visualization
        self.update_neo_visualization(neo_options[0])
        
    def update_neo_visualization(self, option, start_date=None, end_date=None):
        for widget in self.visualization_frame.winfo_children():
            widget.destroy()
            
        # If dates not provided, use defaults
        if not start_date or not end_date:
            today = datetime.today()
            end_date = today.strftime("%Y-%m-%d")
            start_date = (today - timedelta(days=7)).strftime("%Y-%m-%d")
            
        try:
            # Create visualization and table frames
            vis_container = ttk.Frame(self.visualization_frame)
            vis_container.pack(fill=tk.BOTH, expand=True)
            
            graph_frame = ttk.Frame(vis_container)
            graph_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
            
            table_frame = ttk.Frame(vis_container)
            table_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)
            
            # Fetch NEO data
            url = f"https://api.nasa.gov/neo/rest/v1/feed?start_date={start_date}&end_date={end_date}&api_key={self.nasa_api_key}"
            response = requests.get(url)
            data = response.json()
            
            # Process data
            neo_dates = []
            neo_counts = []
            hazardous_counts = []
            safe_counts = []
            
            for date in data["near_earth_objects"]:
                neo_dates.append(date)
                objects = data["near_earth_objects"][date]
                neo_counts.append(len(objects))
                
                # Count hazardous objects
                hazardous = sum(1 for obj in objects if obj["is_potentially_hazardous_asteroid"])
                hazardous_counts.append(hazardous)
                safe_counts.append(len(objects) - hazardous)
            
            # Create figure
            fig = Figure(figsize=(8, 5))
            ax = fig.add_subplot(111)
            
            # Create DataFrame for table
            if option == "NEO Count by Date":
                ax.bar(neo_dates, neo_counts, color="#4a7abc")
                ax.set_title("NEO Count by Date")
                ax.set_xlabel("Date")
                ax.set_ylabel("Count")
                ax.set_xticklabels(neo_dates, rotation=45)
                ax.grid(True, linestyle='--', alpha=0.7)
                
                # Table data
                table_data = {"Date": neo_dates, "NEO Count": neo_counts}
                df = pd.DataFrame(table_data)
                
            elif option == "Hazardous vs Safe NEO":
                # Total counts
                total_hazardous = sum(hazardous_counts)
                total_safe = sum(safe_counts)
                
                # Create pie chart
                ax.pie([total_hazardous, total_safe], 
                       labels=["Hazardous", "Safe"],
                       autopct='%1.1f%%',
                       colors=["#ff9999", "#66b3ff"],
                       explode=(0.1, 0))
                ax.set_title("Hazardous vs Safe NEO Distribution")
                
                # Table data
                table_data = {"Category": ["Hazardous", "Safe"], 
                             "Count": [total_hazardous, total_safe],
                             "Percentage": [f"{total_hazardous/(total_hazardous+total_safe)*100:.1f}%", 
                                           f"{total_safe/(total_hazardous+total_safe)*100:.1f}%"]}
                df = pd.DataFrame(table_data)
                
            # Create canvas
            canvas = FigureCanvasTkAgg(fig, master=graph_frame)
            canvas.draw()
            canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
            
            # Create table
            ttk.Label(table_frame, text=f"{option} Data", font=("Arial", 12, "bold")).pack(pady=(10, 5))
            
            # Table view with scrollbar
            table_container = ttk.Frame(table_frame)
            table_container.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
            
            # Create scrollbar
            scrolly = ttk.Scrollbar(table_container)
            scrolly.pack(side=tk.RIGHT, fill=tk.Y)
            
            # Create Treeview
            cols = list(df.columns)
            tree = ttk.Treeview(table_container, columns=cols, show="headings", yscrollcommand=scrolly.set)
            
            # Configure scrollbar
            scrolly.config(command=tree.yview)
            
            # Set column headings
            for col in cols:
                tree.heading(col, text=col)
                tree.column(col, width=100, anchor=tk.CENTER)
            
            # Insert data rows
            for i, row in df.iterrows():
                values = [row[col] for col in cols]
                tree.insert("", "end", values=values)
            
            tree.pack(fill=tk.BOTH, expand=True)
            
        except Exception as e:
            error_msg = f"Error retrieving NEO data: {str(e)}"
            messagebox.showerror("Data Error", error_msg)
    
    def show_apod_page(self):
        self.page_title.config(text="NASA Astronomy Picture of the Day")
        self.clear_content()
        
        # Date selection for APOD
        ttk.Label(self.submenu_frame, text="Select Date:").pack(side=tk.LEFT, padx=(0, 10))
        
        today = datetime.today()
        date_var = StringVar(value=today.strftime("%Y-%m-%d"))
        date_entry = ttk.Entry(self.submenu_frame, textvariable=date_var, width=12)
        date_entry.pack(side=tk.LEFT)
        
        ttk.Button(self.submenu_frame, text="View APOD", 
                  command=lambda: self.fetch_apod(date_var.get())).pack(side=tk.LEFT, padx=10)
        
        # Show current APOD
        self.fetch_apod(date_var.get())
    
    def fetch_apod(self, date):
        for widget in self.visualization_frame.winfo_children():
            widget.destroy()
            
        try:
            # Fetch APOD data
            url = f"https://api.nasa.gov/planetary/apod?date={date}&api_key={self.nasa_api_key}"
            response = requests.get(url)
            data = response.json()
            
            # Create container
            apod_frame = ttk.Frame(self.visualization_frame)
            apod_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
            
            # Display info
            info_frame = ttk.Frame(apod_frame)
            info_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=10)
            
            ttk.Label(info_frame, text=data["title"], font=("Arial", 16, "bold")).pack(anchor=tk.W, pady=(0, 10))
            ttk.Label(info_frame, text=f"Date: {data['date']}", font=("Arial", 12)).pack(anchor=tk.W, pady=(0, 5))
            
            # Create text widget for description with scrollbar
            desc_frame = ttk.Frame(info_frame)
            desc_frame.pack(fill=tk.BOTH, expand=True, pady=10)
            
            scrollbar = ttk.Scrollbar(desc_frame)
            scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
            
            text_widget = tk.Text(desc_frame, wrap=tk.WORD, height=15, width=50)
            text_widget.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
            text_widget.insert(tk.END, data["explanation"])
            text_widget.config(state=tk.DISABLED)
            
            scrollbar.config(command=text_widget.yview)
            text_widget.config(yscrollcommand=scrollbar.set)
            
            # Display image frame
            img_frame = ttk.Frame(apod_frame)
            img_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True, padx=10)
            
            # Handle different media types
            if data["media_type"] == "image":
                # Get image
                img_url = data["url"]
                img_data = requests.get(img_url).content
                
                try:
                    # Display image
                    img = Image.open(io.BytesIO(img_data))
                    
                    # Resize image to fit
                    img.thumbnail((400, 400))
                    photo = ImageTk.PhotoImage(img)
                    
                    label = ttk.Label(img_frame, image=photo)
                    label.image = photo  # Keep a reference
                    label.pack(pady=10)
                    
                except Exception as e:
                    ttk.Label(img_frame, text=f"Image could not be displayed: {str(e)}").pack(pady=10)
                    ttk.Label(img_frame, text=f"Image URL: {img_url}").pack(pady=10)
            
            else:
                ttk.Label(img_frame, text=f"Media Type: {data['media_type']}").pack(pady=10)
                ttk.Label(img_frame, text=f"URL: {data['url']}").pack(pady=10)
            
        except Exception as e:
            error_msg = f"Error retrieving APOD data: {str(e)}"
            messagebox.showerror("Data Error", error_msg)
    
    def show_upcoming_launches(self):
        self.page_title.config(text="Upcoming Space Launches")
        self.clear_content()
        
        # Dropdown for launch visualization options
        ttk.Label(self.submenu_frame, text="Select View:").pack(side=tk.LEFT, padx=(0, 10))
        
        launch_options = ["Upcoming Launches by Organization", "Launches by Location"]
        launch_var = StringVar(value=launch_options[0])
        
        dropdown = ttk.Combobox(self.submenu_frame, textvariable=launch_var, values=launch_options, state="readonly", width=30)
        dropdown.pack(side=tk.LEFT)
        dropdown.bind("<<ComboboxSelected>>", lambda e: self.update_launch_visualization(launch_var.get()))
        
        # Show initial visualization
        self.update_launch_visualization(launch_options[0])
    
    def update_launch_visualization(self, option):
        for widget in self.visualization_frame.winfo_children():
            widget.destroy()
            
        try:
            # Create visualization and table frames
            vis_container = ttk.Frame(self.visualization_frame)
            vis_container.pack(fill=tk.BOTH, expand=True)
            
            graph_frame = ttk.Frame(vis_container)
            graph_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
            
            table_frame = ttk.Frame(vis_container)
            table_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)
            
            # Fetch upcoming launches data
            url = "https://ll.thespacedevs.com/2.2.0/launch/upcoming/"
            headers = {"User-Agent": "Mozilla/5.0"}
            response = requests.get(url, headers=headers)
            data = response.json()
            
            launches = data.get("results", [])
            
            if option == "Upcoming Launches by Organization":
                # Process data
                organizations = {}
                dates = []
                
                for launch in launches:
                    org = launch.get("launch_service_provider", {}).get("name", "Unknown")
                    date = launch.get("net", "Unknown")[:10]  # Get only the date part
                    
                    if org in organizations:
                        organizations[org] += 1
                    else:
                        organizations[org] = 1
                        
                    dates.append(date)
                
                # Sort by number of launches
                sorted_orgs = {k: v for k, v in sorted(organizations.items(), key=lambda item: item[1], reverse=True)}
                
                # Create figure
                fig = Figure(figsize=(8, 5))
                ax = fig.add_subplot(111)
                
                # Create bar chart
                ax.bar(sorted_orgs.keys(), sorted_orgs.values(), color="#4a7abc")
                ax.set_title("Upcoming Launches by Organization")
                ax.set_xlabel("Organization")
                ax.set_ylabel("Number of Launches")
                ax.set_xticklabels(sorted_orgs.keys(), rotation=45, ha='right')
                ax.grid(True, linestyle='--', alpha=0.7)
                
                # Table data
                table_data = {"Organization": list(sorted_orgs.keys()), "Number of Launches": list(sorted_orgs.values())}
                df = pd.DataFrame(table_data)
                
            elif option == "Launches by Location":
                # Process data
                locations = {}
                location_details = {}
                
                for launch in launches:
                    location = launch.get("pad", {}).get("location", {}).get("name", "Unknown")
                    date = launch.get("net", "Unknown")
                    mission = launch.get("mission", {}).get("name", "Unknown Mission")
                    
                    if location in locations:
                        locations[location] += 1
                        location_details[location].append({"date": date, "mission": mission})
                    else:
                        locations[location] = 1
                        location_details[location] = [{"date": date, "mission": mission}]
                
                # Sort by number of launches
                sorted_locations = {k: v for k, v in sorted(locations.items(), key=lambda item: item[1], reverse=True)}
                
                # Get total launches for percentage calculation
                total_launches = sum(sorted_locations.values())
                
                # Create figure
                fig = Figure(figsize=(8, 5))
                ax = fig.add_subplot(111)
                
                # Create pie chart
                labels = [f"{loc} ({count})" for loc, count in sorted_locations.items()]
                sizes = sorted_locations.values()
                
                ax.pie(sizes, labels=labels, autopct='%1.1f%%', startangle=90)
                ax.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle
                ax.set_title("Upcoming Launches by Location")
                
                # Create table data with percentages
                table_data = {
                    "Location": list(sorted_locations.keys()),
                    "Count": list(sorted_locations.values()),
                    "Percentage": [f"{(count/total_launches)*100:.1f}%" for count in sorted_locations.values()]
                }
                df = pd.DataFrame(table_data)
            
            # Create canvas
            canvas = FigureCanvasTkAgg(fig, master=graph_frame)
            canvas.draw()
            canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
            
            # Create table
            ttk.Label(table_frame, text=f"{option} Data", font=("Arial", 12, "bold")).pack(pady=(10, 5))
            
            # Table view with scrollbar
            table_container = ttk.Frame(table_frame)
            table_container.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
            
            # Create scrollbar
            scrolly = ttk.Scrollbar(table_container)
            scrolly.pack(side=tk.RIGHT, fill=tk.Y)
            
            # Create Treeview
            cols = list(df.columns)
            tree = ttk.Treeview(table_container, columns=cols, show="headings", yscrollcommand=scrolly.set)
            
            # Configure scrollbar
            scrolly.config(command=tree.yview)
            
            # Set column headings
            for col in cols:
                tree.heading(col, text=col)
                tree.column(col, width=100, anchor=tk.CENTER)
            
            # Insert data rows
            for i, row in df.iterrows():
                values = [row[col] for col in cols]
                tree.insert("", "end", values=values)
            
            tree.pack(fill=tk.BOTH, expand=True)
            
        except Exception as e:
            error_msg = f"Error retrieving launch data: {str(e)}"
            messagebox.showerror("Data Error", error_msg)
    
    def show_spacex_stats(self):
        self.page_title.config(text="SpaceX Launch Statistics")
        self.clear_content()
        
        # Dropdown for SpaceX visualization options
        ttk.Label(self.submenu_frame, text="Select Visualization:").pack(side=tk.LEFT, padx=(0, 10))
        
        spacex_options = ["Launches by Year", "Launch Success Rate"]
        spacex_var = StringVar(value=spacex_options[0])
        
        dropdown = ttk.Combobox(self.submenu_frame, textvariable=spacex_var, values=spacex_options, state="readonly", width=30)
        dropdown.pack(side=tk.LEFT)
        dropdown.bind("<<ComboboxSelected>>", lambda e: self.update_spacex_visualization(spacex_var.get()))
        
        # Show initial visualization
        self.update_spacex_visualization(spacex_options[0])
    
    def update_spacex_visualization(self, option):
        for widget in self.visualization_frame.winfo_children():
            widget.destroy()
            
        try:
            # Create visualization and table frames
            vis_container = ttk.Frame(self.visualization_frame)
            vis_container.pack(fill=tk.BOTH, expand=True)
            
            graph_frame = ttk.Frame(vis_container)
            graph_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
            
            table_frame = ttk.Frame(vis_container)
            table_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)
            
            # Fetch SpaceX data
            url = "https://api.spacexdata.com/v4/launches"
            response = requests.get(url)
            launches = response.json()
            
            if option == "Launches by Year":
                # Process data
                years = {}
                
                for launch in launches:
                    year = launch.get("date_utc", "")[:4]  # Extract year from date
                    
                    if year in years:
                        years[year] += 1
                    else:
                        years[year] = 1
                
                # Sort by year
                sorted_years = {k: v for k, v in sorted(years.items())}
                
                # Create figure
                fig = Figure(figsize=(8, 5))
                ax = fig.add_subplot(111)
                
                # Create line chart
                ax.plot(sorted_years.keys(), sorted_years.values(), marker='o', linestyle='-', color="#4a7abc")
                ax.set_title("SpaceX Launches by Year")
                ax.set_xlabel("Year")
                ax.set_ylabel("Number of Launches")
                ax.grid(True, linestyle='--', alpha=0.7)
                
                # Table data
                table_data = {"Year": list(sorted_years.keys()), "Number of Launches": list(sorted_years.values())}
                df = pd.DataFrame(table_data)
                
            elif option == "Launch Success Rate":
                # Process data
                success_count = sum(1 for launch in launches if launch.get("success", False) is True)
                failure_count = sum(1 for launch in launches if launch.get("success", True) is False)
                
                # Create figure
                fig = Figure(figsize=(8, 5))
                ax = fig.add_subplot(111)
                
                # Create pie chart
                labels = ["Successful", "Failed"]
                sizes = [success_count, failure_count]
                colors = ["#4caf50", "#f44336"]
                
                ax.pie(sizes, labels=labels, autopct='%1.1f%%', startangle=90, colors=colors, explode=(0.1, 0))
                ax.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle
                ax.set_title("SpaceX Launch Success Rate")
                
                # Calculate total and percentages
                total = success_count + failure_count
                success_pct = (success_count / total) * 100 if total > 0 else 0
                failure_pct = (failure_count / total) * 100 if total > 0 else 0
                
                # Table data
                table_data = {
                    "Status": ["Successful", "Failed", "Total"],
                    "Count": [success_count, failure_count, total],
                    "Percentage": [f"{success_pct:.1f}%", f"{failure_pct:.1f}%", "100%"]
                }
                df = pd.DataFrame(table_data)
            
            # Create canvas
            canvas = FigureCanvasTkAgg(fig, master=graph_frame)
            canvas.draw()
            canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
            
            # Create table
            ttk.Label(table_frame, text=f"{option} Data", font=("Arial", 12, "bold")).pack(pady=(10, 5))
            
            # Table view with scrollbar
            table_container = ttk.Frame(table_frame)
            table_container.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
            
            # Create scrollbar
            scrolly = ttk.Scrollbar(table_container)
            scrolly.pack(side=tk.RIGHT, fill=tk.Y)
            
            # Create Treeview
            cols = list(df.columns)
            tree = ttk.Treeview(table_container, columns=cols, show="headings", yscrollcommand=scrolly.set)
            
            # Configure scrollbar
            scrolly.config(command=tree.yview)
            
            # Set column headings
            for col in cols:
                tree.heading(col, text=col)
                tree.column(col, width=100, anchor=tk.CENTER)
            
            # Insert data rows
            for i, row in df.iterrows():
                values = [row[col] for col in cols]
                tree.insert("", "end", values=values)
            
            tree.pack(fill=tk.BOTH, expand=True)
            
        except Exception as e:
            error_msg = f"Error retrieving SpaceX data: {str(e)}"
            messagebox.showerror("Data Error", error_msg)
    
    def show_space_agencies(self):
        self.page_title.config(text="Space Agencies Information")
        self.clear_content()
        
        # Dropdown for space agencies visualization options
        ttk.Label(self.submenu_frame, text="Select Visualization:").pack(side=tk.LEFT, padx=(0, 10))
        
        agency_options = ["Agencies by Country", "Agencies by Type"]
        agency_var = StringVar(value=agency_options[0])
        
        dropdown = ttk.Combobox(self.submenu_frame, textvariable=agency_var, values=agency_options, state="readonly", width=30)
        dropdown.pack(side=tk.LEFT)
        dropdown.bind("<<ComboboxSelected>>", lambda e: self.update_agency_visualization(agency_var.get()))
        
        # Show initial visualization
        self.update_agency_visualization(agency_options[0])
    
    def update_agency_visualization(self, option):
        for widget in self.visualization_frame.winfo_children():
            widget.destroy()
            
        try:
            # Create visualization and table frames
            vis_container = ttk.Frame(self.visualization_frame)
            vis_container.pack(fill=tk.BOTH, expand=True)
            
            graph_frame = ttk.Frame(vis_container)
            graph_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
            
            table_frame = ttk.Frame(vis_container)
            table_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)
            
            # Fetch space agencies data
            url = "https://ll.thespacedevs.com/2.2.0/agencies/"
            headers = {"User-Agent": "Mozilla/5.0"}
            response = requests.get(url, headers=headers)
            data = response.json()
            
            agencies = data.get("results", [])
            
            if option == "Agencies by Country":
                # Process data
                countries = {}
                
                for agency in agencies:
                    country = agency.get("country_code", "Unknown")
                    
                    if country in countries:
                        countries[country] += 1
                    else:
                        countries[country] = 1
                
                # Sort by number of agencies
                sorted_countries = {k: v for k, v in sorted(countries.items(), key=lambda item: item[1], reverse=True)}
                
                # Get top 10 countries for better visualization
                top_countries = {k: sorted_countries[k] for k in list(sorted_countries.keys())[:10]}
                
                # Create figure
                fig = Figure(figsize=(8, 5))
                ax = fig.add_subplot(111)
                
                # Create bar chart
                ax.bar(top_countries.keys(), top_countries.values(), color="#4a7abc")
                ax.set_title("Top Countries by Number of Space Agencies")
                ax.set_xlabel("Country Code")
                ax.set_ylabel("Number of Agencies")
                ax.grid(True, linestyle='--', alpha=0.7)
                
                # Table data for all countries
                table_data = {"Country Code": list(sorted_countries.keys()), 
                             "Number of Agencies": list(sorted_countries.values())}
                df = pd.DataFrame(table_data)
                
            elif option == "Agencies by Type":
                # Process data
                types = {}
                
                for agency in agencies:
                    agency_type = agency.get("type", "Unknown")
                    
                    if agency_type in types:
                        types[agency_type] += 1
                    else:
                        types[agency_type] = 1
                
                # Sort by number of agencies
                sorted_types = {k: v for k, v in sorted(types.items(), key=lambda item: item[1], reverse=True)}
                
                # Create figure
                fig = Figure(figsize=(8, 5))
                ax = fig.add_subplot(111)
                
                # Create pie chart
                labels = sorted_types.keys()
                sizes = sorted_types.values()
                
                ax.pie(sizes, labels=labels, autopct='%1.1f%%', startangle=90)
                ax.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle
                ax.set_title("Space Agencies by Type")
                
                # Table data
                table_data = {"Agency Type": list(sorted_types.keys()), 
                             "Count": list(sorted_types.values())}
                df = pd.DataFrame(table_data)
            
            # Create canvas
            canvas = FigureCanvasTkAgg(fig, master=graph_frame)
            canvas.draw()
            canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
            
            # Create table
            ttk.Label(table_frame, text=f"{option} Data", font=("Arial", 12, "bold")).pack(pady=(10, 5))
            
            # Table view with scrollbar
            table_container = ttk.Frame(table_frame)
            table_container.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
            
            # Create scrollbar
            scrolly = ttk.Scrollbar(table_container)
            scrolly.pack(side=tk.RIGHT, fill=tk.Y)
            
            # Create Treeview
            cols = list(df.columns)
            tree = ttk.Treeview(table_container, columns=cols, show="headings", yscrollcommand=scrolly.set)
            
            # Configure scrollbar
            scrolly.config(command=tree.yview)
            
            # Set column headings
            for col in cols:
                tree.heading(col, text=col)
                tree.column(col, width=100, anchor=tk.CENTER)
            
            # Insert data rows
            for i, row in df.iterrows():
                values = [row[col] for col in cols]
                tree.insert("", "end", values=values)
            
            tree.pack(fill=tk.BOTH, expand=True)
            
        except Exception as e:
            error_msg = f"Error retrieving space agencies data: {str(e)}"
            messagebox.showerror("Data Error", error_msg)

def main():
    root = tk.Tk()
    app = SpaceDataApp(root)
    root.mainloop()

if __name__ == "__main__":
    main()
        
    