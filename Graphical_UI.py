import tkinter as tk
from tkinter import ttk, messagebox
import subprocess
import json

def run_scheduler(choice, processes, quantum=None):
    try:
        # Prepare the process input as JSON
        process_input = json.dumps({
            "choice": choice,
            "processes": processes,
            "quantum": quantum
        })
        # Run the scheduler as a subprocess
        result = subprocess.run(
            ['./implementation_main'],  # Make sure this executable is accessible
            input=process_input,
            text=True,
            capture_output=True,
            check=True
        )
        return result.stdout  # Return the output from the scheduler
    except subprocess.CalledProcessError as e:
        return f"Error: {e}"  # Handle any errors that occur during execution

def add_process():
    arrival_time = entry_arrival_time.get()
    burst_time = entry_burst_time.get()
    priority = entry_priority.get()

    # Validate that the input is numeric
    if not arrival_time.isdigit() or not burst_time.isdigit() or (priority and not priority.isdigit()):
        messagebox.showerror("Invalid input", "Please enter valid integers.")
        return

    # Append the process to the list of processes
    processes.append({
        "arrivalTime": int(arrival_time),
        "burstTime": int(burst_time),
        "priority": int(priority) if priority else None,
    })

    # Update the listbox to display the added process
    listbox_processes.insert(
        tk.END,
        f"Arrival: {arrival_time}, Burst: {burst_time}, Priority: {priority if priority else 'N/A'}"
    )

    # Clear the input fields
    entry_arrival_time.delete(0, tk.END)
    entry_burst_time.delete(0, tk.END)
    entry_priority.delete(0, tk.END)

def submit():
    choice = algo_choice.get().split(" ")[0]  # Get the selected algorithm choice
    quantum = entry_quantum.get() if choice == '4' else None  # Quantum for Round Robin

    result = run_scheduler(choice, processes, quantum)

    # Display the result in the text widget
    result_text.delete(1.0, tk.END)
    result_text.insert(tk.END, result)

# Create the main application window
root = tk.Tk()
root.title("CPU Scheduling Simulator")

# Algorithm selection
label_algo = tk.Label(root, text="Select Algorithm:")
label_algo.grid(row=0, column=0, padx=10, pady=10)
algo_choice = ttk.Combobox(root, values=[
    "1 - FCFS", 
    "2 - SJF", 
    "3 - Priority Preemptive", 
    "4 - Round Robin"
])
algo_choice.grid(row=0, column=1, padx=10, pady=10)
algo_choice.current(0)  # Set default selection

# Process input fields
label_arrival_time = tk.Label(root, text="Arrival Time:")
label_arrival_time.grid(row=1, column=0, padx=10, pady=10)
entry_arrival_time = tk.Entry(root)
entry_arrival_time.grid(row=1, column=1, padx=10, pady=10)

label_burst_time = tk.Label(root, text="Burst Time:")
label_burst_time.grid(row=2, column=0, padx=10, pady=10)
entry_burst_time = tk.Entry(root)
entry_burst_time.grid(row=2, column=1, padx=10, pady=10)

label_priority = tk.Label(root, text="Priority (if applicable):")
label_priority.grid(row=3, column=0, padx=10, pady=10)
entry_priority = tk.Entry(root)
entry_priority.grid(row=3, column=1, padx=10, pady=10)

# Button to add a process
button_add_process = tk.Button(root, text="Add Process", command=add_process)
button_add_process.grid(row=4, column=0, columnspan=2, pady=10)

# Listbox to display added processes
listbox_processes = tk.Listbox(root, height=10, width=50)
listbox_processes.grid(row=5, column=0, columnspan=2, padx=10, pady=10)

# Quantum input for Round Robin
label_quantum = tk.Label(root, text="Time Quantum (Round Robin only):")
label_quantum.grid(row=6, column=0, padx=10, pady=10)
entry_quantum = tk.Entry(root)
entry_quantum.grid(row=6, column=1, padx=10, pady=10)

# Submit button
button_submit = tk.Button(root, text="Submit", command=submit)
button_submit.grid(row=7, column=0, columnspan=2, pady=10)

# Text widget to display results
result_text = tk.Text(root, height=15, width=70)
result_text.grid(row=8, column=0, columnspan=2, padx=10, pady=10)

# Initialize the list of processes
processes = []

# Start the main event loop
root.mainloop()
