# Initialize all libraries
from pyfirmata2 import Arduino
import time
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import os
import sys

# Auto start port so we don't have to look for it and be cringe 
PORT = Arduino.AUTODETECT
pin = 0  # Default pin, will be changed to a different pin for each signal being collected 

# Create CSV file for all each EMG lead signal data, start with forehead but change as each EMG signal lead changes/is being measured 
forehead = "forehead.csv"
rcheek = "rcheek.csv"
lcheek = "lcheek.csv"
ljaw = "ljaw.csv"
rjaw = "rjaw.csv"

# Analog printer class with pandas because deepseek wanted me to use some nasty other library and I only know pandas ngl
class AnalogPrinterWithPandas:
    def __init__(self, csv_filename="forehead.csv"):
        # Sampling rate: 10Hz --> this means that 10 samples will be collected per second. Change this if necessary to make look like the model-trained emg signal 
        self.samplingRate = 10
        self.timestamp = 0
        self.board = Arduino(PORT)
        self.csv_filename = csv_filename
        self.data = {"Time": [], "Voltage": []}
        self.start_time = None
        
    def start(self):
        # Connect to Arduino
        self.board.analog[pin].register_callback(self.myPrintCallback)
        self.board.samplingOn(1000 / self.samplingRate)
        self.board.analog[pin].enable_reporting()
        self.start_time = time.time()
        
    def myPrintCallback(self, data):
        # Convert Arduino data (0-1) to voltage (assuming 5V reference)
        # Arduino ADC: 0-1023 = 0-5000 mv therefore multiple by 0.05 to get into mV format yayayay
        voltage = data * 0.05
        
        # Calculate elapsed time
        elapsed_time = time.time() - self.start_time
        
        # Print to console
        print(f"{elapsed_time:.3f}, {voltage:.4f}V")
        
        # Store data
        self.data["Time"].append(elapsed_time)
        self.data["Voltage"].append(voltage)
        
    def save_to_csv(self):
        """Save data to CSV using pandas"""
        if not self.data["Time"]:
            print("No data to save!")
            return
            
        df = pd.DataFrame(self.data)
        
        # Check if file exists
        if os.path.exists(self.csv_filename):
            try:
                existing_df = pd.read_csv(self.csv_filename)
                # Append new data to existing file
                df = pd.concat([existing_df, df], ignore_index=True)
                mode = 'appended to'
            except:
                # If there's an error reading existing file, overwrite
                mode = 'overwritten'
        else:
            mode = 'created new'
        
        # Save to CSV
        df.to_csv(self.csv_filename, index=False)
        print(f"\nSaved {len(self.data['Time'])} samples to {self.csv_filename} ({mode})")
        
        return df
        
    def plot_data(self, df=None):
        """Plot the collected EMG data"""
        if df is None:
            if not self.data["Time"]:
                print("No data to plot!")
                return
            df = pd.DataFrame(self.data)
        
        plt.figure(figsize=(12, 6))
        
        # Plot 1: Full signal
        plt.subplot(2, 1, 1)
        plt.plot(df['Time'], df['Voltage'], 'b-', linewidth=1, alpha=0.8)
        plt.xlabel('Time (seconds)')
        plt.ylabel('Voltage (mV)')
        plt.title('Forehead EMG Signal - Full View')
        plt.grid(True, alpha=0.3)
        
        # Plot 2: Zoomed in view (last 2 seconds or full if less than 2 seconds)
        plt.subplot(2, 1, 2)
        if df['Time'].max() > 2:
            mask = df['Time'] >= (df['Time'].max() - 2)
            zoom_df = df[mask]
        else:
            zoom_df = df
            
        plt.plot(zoom_df['Time'], zoom_df['Voltage'], 'r-', linewidth=1.5, alpha=0.8)
        plt.xlabel('Time (seconds)')
        plt.ylabel('Voltage (V)')
        plt.title('Forehead EMG Signal - Zoomed View (Last 2 seconds)')
        plt.grid(True, alpha=0.3)
        
        plt.tight_layout()
        return plt
        
        
    def stop(self):
        """Stop data collection and save data"""
        self.board.samplingOff()
        time.sleep(0.1)  # Small delay to ensure all callbacks are processed
        self.board.exit()
        
        # Save data to CSV
        df = self.save_to_csv()
        

        # Plot the data
        if df is not None and len(df) > 0:
            plt = self.plot_data(df)
            
            # Ask user if they want to save the plot
            save_plot = input("\nDo you want to save the plot? (y/n): ").lower()
            if save_plot == 'y':
                plot_filename = "forehead_plot.png"
                plt.savefig(plot_filename, dpi=150, bbox_inches='tight')
                print(f"Plot saved as '{plot_filename}'")
            
            # Show the plot
            plt.show()
            
            # Ask if user wants to view the data
            view_data = input("\nDo you want to view the first few rows of data? (y/n): ").lower()
            if view_data == 'y':
                print("\nFirst 10 rows of data:")
                print(df.head(10).to_string())
        
        print("\nData collection complete!")

# Main execution
def main():
    print("\nInstructions for the operator :")
    print("1. Make sure Arduino is connected with StandardFirmata uploaded or else this won't work.")
    print("2. EMG sensor should be connected to analog pin A1-5 AND there should be a ground electrode on the wrist.")
    print("3. Keep your face relaxed until prompted")
    print("4. Scrunch your face when you see 'SCRUNCH', this will happen 5 times")
    
    # Set pin for forehead (A1 = pin 1 in pyfirmata), this will change each scrunch so we get all 5 sensors' data
    global pin
    pin = 1
    
    # Create analog printer instance, input filename to save data into
    analogPrinter = AnalogPrinterWithPandas(csv_filename)
    
    try:
        # Wait for user to be ready
        input("\nPress Enter when you are ready to begin...") # get user input
        print("\nStarting in 3 seconds")
        time.sleep(1)
        print("\n3!")
        time.sleep(1)
        print("\n2!")
        time.sleep(1)
        print("\n1!")
        time.sleep(1)

        # Relax phase (5 seconds) we can cut around this to get a better signal but this is fine for a nice curve
        print("\n" + "="*20)
        print("RELAX - Keep face neutral")
        print("="*20)
        analogPrinter.start()
        time.sleep(2)
        
        # Scrunch phase 1 
        print("\n" + "="*20)
        print("SCRUNCH!")
        print("="*20)
        time.sleep(3)
        
        # Relax again
        print("\n" + "="*20)
        print("RELAX - Return to neutral")
        print("="*20)
        time.sleep(2)

        # Scrunch phase 2
        pin=2
        print("\n" + "="*20)
        print("SCRUNCH!")
        print("="*20)
        time.sleep(3)
        
        # Relax again
        print("\n" + "="*20)
        print("RELAX - Return to neutral")
        print("="*20)
        time.sleep(2)
        
        # Scrunch phase 3
        pin=3
        print("\n" + "="*20)
        print("SCRUNCH!")
        print("="*20)
        time.sleep(3)
        
        # Relax again
        print("\n" + "="*20)
        print("RELAX - Return to neutral")
        print("="*20)
        time.sleep(2)

        # Scrunch phase 4
        pin=4 
        print("\n" + "="*20)
        print("SCRUNCH!")
        print("="*20)
        time.sleep(3)
        
        # Relax again
        print("\n" + "="*20)
        print("RELAX - Return to neutral")
        print("="*20)
        time.sleep(2)

        # Scrunch phase 5
        pin=5
        print("\n" + "="*20)
        print("SCRUNCH!")
        print("="*20)
        time.sleep(3)
        
        # Relax again
        print("\n" + "="*20)
        print("RELAX - Return to neutral")
        print("="*20)
        time.sleep(2)

    except KeyboardInterrupt:
        print("\n\nData collection interrupted by user!")
    except Exception as e:
        print(f"\nError during data collection: {e}")
    finally:
        # Always stop properly
        analogPrinter.stop()

if __name__ == "__main__":
    main()
