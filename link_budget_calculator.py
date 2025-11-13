import tkinter as tk
from tkinter import ttk, messagebox
import math
import numpy as np
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import (
    FigureCanvasTkAgg,
    NavigationToolbar2Tk
)
class LinkBudgetCalculator(tk.Tk):
    """
    An interactive GUI application for calculating the maximum communication
    distance based on link budget parameters.

    The user provides transmitter power, gains, losses, frequency,
    receiver sensitivity, and a path loss exponent. The application
    calculates the maximum achievable distance.
    """
    def __init__(self):
        super().__init__()
        self.title("Link Budget Distance Calculator")
        self.geometry("1050x600")
        self.resizable(True, True)

        # Style configuration
        style = ttk.Style(self)
        style.configure("TLabel", padding=5, font=('Helvetica', 10))
        style.configure("TEntry", padding=5, font=('Helvetica', 10))
        style.configure("TButton", padding=5, font=('Helvetica', 10, 'bold'))
        style.configure("Header.TLabel", font=('Helvetica', 12, 'bold'))
        style.configure("Result.TLabel", font=('Helvetica', 11, 'bold'), foreground='blue')
        style.configure("Small.TButton", padding=(1, 1), font=('Helvetica', 8))

        self.input_vars = {}
        self.result_km_var = tk.StringVar(value="---")
        self.result_m_var = tk.StringVar(value="---")
        self.result_mi_var = tk.StringVar(value="---")
        self.result_ft_var = tk.StringVar(value="---")
        self.fspl_exponent_var = tk.DoubleVar(value=2.0)
        self.model_choice_var = tk.StringVar(value="1km")

        self.fig = None
        self.ax = None
        self.canvas = None
        self.create_widgets()
        self.calculate_distance() # Perform initial calculation and plot

    def create_widgets(self):
        """Creates and arranges all the GUI widgets in the main window."""
        # Main layout frames
        left_frame = ttk.Frame(self, padding="10")
        left_frame.pack(side=tk.LEFT, fill=tk.Y, padx=(10,0), pady=10)

        right_frame = ttk.Frame(self, padding="10")
        right_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True, padx=10, pady=10)

        # --- Input Fields ---
        # Use a separate frame for inputs for better organization
        input_frame = ttk.LabelFrame(left_frame, text="Parameters", padding="10")
        input_frame.pack(fill=tk.X)

        # Inputs with +/- steppers
        stepper_inputs = {
            "Transmit Power (dBm)": "20",
            "Transmit Antenna Gain (dBi)": "2",
            "Transmit Cable Loss (dB)": "1",
            "Receiver Antenna Gain (dBi)": "2",
            "Receiver Cable Loss (dB)": "1",
            "Receiver Sensitivity (dBm)": "-95",
        }
        # Plain entry inputs
        plain_inputs = {
            "Frequency (MHz)": "2400",
        }

        # --- Create Input Widgets ---
        row_counter = 0
        all_inputs = {**stepper_inputs, **plain_inputs}

        for label_text, default_value in all_inputs.items():
            label = ttk.Label(input_frame, text=label_text)
            label.grid(row=row_counter, column=0, sticky="w", padx=5, pady=5)

            var = tk.StringVar(value=default_value)
            self.input_vars[label_text] = var

            if label_text in stepper_inputs:
                # Create a frame to hold entry and buttons
                stepper_frame = ttk.Frame(input_frame)
                stepper_frame.grid(row=row_counter, column=1, sticky="e")

                entry = ttk.Entry(stepper_frame, textvariable=var, width=10)
                entry.bind("<KeyRelease>", self._on_input_change)
                entry.pack(side=tk.LEFT, padx=(0, 5))

                # Use a lambda to capture the `var` for each button
                plus_button = ttk.Button(stepper_frame, text="+", width=2, style="Small.TButton", command=lambda v=var: self._increment_value(v, 0.2))
                plus_button.pack(side=tk.LEFT)
                minus_button = ttk.Button(stepper_frame, text="-", width=2, style="Small.TButton", command=lambda v=var: self._increment_value(v, -0.2))
                minus_button.pack(side=tk.LEFT)
            else: # For plain inputs like Frequency
                entry = ttk.Entry(input_frame, textvariable=var, width=15)
                entry.bind("<KeyRelease>", self._on_input_change)
                entry.grid(row=row_counter, column=1, sticky="e", padx=5, pady=5)

            row_counter += 1

        # --- FSPL Exponent Slider ---
        fspl_label = ttk.Label(input_frame, text="FSPL Exponent (2-10)")
        fspl_label.grid(row=row_counter, column=0, sticky="w", padx=5, pady=10)

        slider_frame = ttk.Frame(input_frame)
        slider_frame.grid(row=row_counter, column=1, sticky="ew", padx=5, pady=10)

        fspl_slider = ttk.Scale(slider_frame, from_=2.0, to=10.0, orient=tk.HORIZONTAL, variable=self.fspl_exponent_var, command=self._on_slider_change)
        fspl_slider.pack(side=tk.LEFT, expand=True, fill=tk.X)

        self.fspl_value_label = ttk.Label(slider_frame, text=f"{self.fspl_exponent_var.get():.2f}", width=5)
        self.fspl_value_label.pack(side=tk.LEFT, padx=(5, 0))
        row_counter += 1

        # --- Calculation Button ---
        calc_button = ttk.Button(input_frame, text="Calculate Distance & Update Plot", command=self.calculate_distance)
        calc_button.grid(row=row_counter, column=0, columnspan=2, pady=10)

        # --- Model Selection Radio Buttons ---
        model_frame = ttk.LabelFrame(left_frame, text="Path Loss Model", padding="10")
        model_frame.pack(fill=tk.X, pady=10)
        
        rb1 = ttk.Radiobutton(model_frame, text="Classic Model (1 km reference)", variable=self.model_choice_var, value="1km", command=self.calculate_distance)
        rb1.pack(anchor=tk.W)
        rb2 = ttk.Radiobutton(model_frame, text="Log-distance Model (1m reference)", variable=self.model_choice_var, value="1m", command=self.calculate_distance)
        rb2.pack(anchor=tk.W)


        # --- Result Display ---
        results_display_frame = ttk.LabelFrame(right_frame, text="Maximum Communication Distance", padding="10")
        results_display_frame.pack(fill=tk.X, pady=(0, 10))

        # Create labels and value displays for each unit
        result_units = {
            "Kilometers:": self.result_km_var,
            "Meters:": self.result_m_var,
            "Miles:": self.result_mi_var,
            "Feet:": self.result_ft_var,
        }
        
        for i, (text, var) in enumerate(result_units.items()):
            ttk.Label(results_display_frame, text=text, font=('Helvetica', 10)).grid(row=i, column=0, sticky="w", padx=5, pady=2)
            ttk.Label(results_display_frame, textvariable=var, style="Result.TLabel").grid(row=i, column=1, sticky="w", padx=5, pady=2)

        results_display_frame.columnconfigure(1, weight=1)

        # --- Matplotlib Plot ---
        plot_frame = ttk.Frame(right_frame)
        plot_frame.pack(fill=tk.BOTH, expand=True)

        self.fig = Figure(figsize=(6, 4), dpi=100)
        self.ax = self.fig.add_subplot(111)

        self.canvas = FigureCanvasTkAgg(self.fig, master=plot_frame)
        self.canvas.draw()
        # Note: The toolbar packs itself, so we only need to pack the canvas widget
        # self.canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=True)

        toolbar = NavigationToolbar2Tk(self.canvas, plot_frame)
        toolbar.update()
        self.canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=True)

    def _increment_value(self, var: tk.StringVar, amount: float):
        """Helper function to increment/decrement a value in an Entry."""
        try:
            current_value = float(var.get())
            new_value = current_value + amount
            var.set(f"{new_value:.1f}")
            self.calculate_distance()
        except ValueError:
            # Handle cases where the entry is empty or not a number
            pass

    def _on_slider_change(self, value):
        """Rounds slider value to 0.1, updates label, and recalculates."""
        # Round the raw slider value to one decimal place to create 0.1 increments
        rounded_value = round(float(value), 1)
        self.fspl_exponent_var.set(rounded_value)

        self.fspl_value_label.config(text=f"{rounded_value:.2f}")
        self.calculate_distance()

    def _on_input_change(self, event=None):
        """Callback for when an entry value is changed by typing."""
        self.calculate_distance()

    def update_plot(self, max_path_loss, freq_mhz, current_n, current_dist_ft, model_choice):
        """Updates the matplotlib plot with new data."""
        self.ax.clear()

        n_values = np.linspace(2, 10, 100)

        if model_choice == "1m":
            # 1-meter reference model
            # d_m = 10 ^ ((PL - 20log10(f) + 27.55) / (10n))
            log_term_numerator = max_path_loss - 20 * math.log10(freq_mhz) + 27.55
            distances_m = 10 ** (log_term_numerator / (10 * n_values))
            distances_km = distances_m / 1000
        else:
            # 1-km reference model
            # d_km = 10^((PL - 20log10(f) - 32.44) / (10n))
            log_term_numerator = max_path_loss - 20 * math.log10(freq_mhz) - 32.44
            distances_km = 10 ** (log_term_numerator / (10 * n_values))

        # Convert to feet for plotting
        distances_ft = distances_km * 1000 * 3.28084

        self.ax.plot(n_values, distances_ft, label="Max Distance vs. FSPL Exponent")
        self.ax.plot(current_n, current_dist_ft, 'ro') # Mark the current point
        self.ax.set_xlabel("FSPL Path Loss Exponent (n)")
        self.ax.set_ylabel("Maximum Distance (ft)")
        self.ax.set_title("Impact of Path Loss Exponent on Range")
        self.ax.grid(True, which='both', linestyle='--')
        self.ax.legend()
        self.fig.tight_layout()
        self.canvas.draw()

    def calculate_distance(self):
        """
        Performs the link budget calculation and updates the result display.
        It reads all input values, validates them, computes the distance,
        and displays it in the GUI.
        """
        try:
            # --- Gather and validate inputs ---
            p_tx = float(self.input_vars["Transmit Power (dBm)"].get())
            g_tx = float(self.input_vars["Transmit Antenna Gain (dBi)"].get())
            l_tx = float(self.input_vars["Transmit Cable Loss (dB)"].get())
            freq_mhz = float(self.input_vars["Frequency (MHz)"].get())
            g_rx = float(self.input_vars["Receiver Antenna Gain (dBi)"].get())
            l_rx = float(self.input_vars["Receiver Cable Loss (dB)"].get())
            p_rx_sensitivity = float(self.input_vars["Receiver Sensitivity (dBm)"].get())
            n = self.fspl_exponent_var.get()
            model_choice = self.model_choice_var.get()

            if not (2.0 <= n <= 10.0):
                messagebox.showerror("Input Error", "FSPL Exponent must be between 2 and 10.")
                return
            if freq_mhz <= 0:
                messagebox.showerror("Input Error", "Frequency must be a positive number.")
                return

            # --- Link Budget Calculation ---
            # Received Power = Tx Power + Gains - Losses
            # At max distance, Received Power = Receiver Sensitivity
            # p_rx_sensitivity = p_tx + g_tx + g_rx - l_tx - l_rx - fspl
            # Therefore, max allowable path loss (FSPL) is:
            max_path_loss = p_tx + g_tx + g_rx - l_tx - l_rx - p_rx_sensitivity

            if max_path_loss < 0:
                for var in [self.result_km_var, self.result_m_var, self.result_mi_var, self.result_ft_var]:
                    var.set("Link cannot be established.")
                return

            # --- FSPL to Distance Calculation ---
            if model_choice == "1m":
                # Using 1-meter reference model: PL(d) = (20log10(f) - 27.55) + 10n*log10(d_m)
                # Rearranging for d_m:
                log_term = (max_path_loss - 20 * math.log10(freq_mhz) + 27.55) / (10 * n)
                current_distance_m = 10 ** log_term
                current_distance_km = current_distance_m / 1000
            else:
                # Using 1-km reference model: PL(d) = 20log10(f) + 10n*log10(d_km) + 32.44
                log_term = (max_path_loss - 20 * math.log10(freq_mhz) - 32.44) / (10 * n)
                current_distance_km = 10 ** log_term

            # --- Unit Conversions ---
            current_distance_m = current_distance_km * 1000
            current_distance_mi = current_distance_km * 0.621371
            current_distance_ft = current_distance_m * 3.28084

            # --- Update Result Display ---
            self.result_km_var.set(f"{current_distance_km:.2f}")
            self.result_m_var.set(f"{current_distance_m:.2f}")
            self.result_mi_var.set(f"{current_distance_mi:.2f}")
            self.result_ft_var.set(f"{current_distance_ft:.2f}")

            # --- Update Plot ---
            self.update_plot(max_path_loss, freq_mhz, n, current_distance_ft, model_choice)

        except ValueError:
            # Suppress pop-up errors during dynamic updates for a smoother experience
            # messagebox.showerror("Input Error", "Please ensure all inputs are valid numbers.")
            pass
        except Exception as e:
            messagebox.showerror("Error", f"An unexpected error occurred: {e}")
if __name__ == "__main__":
    app = LinkBudgetCalculator()
    app.mainloop()
