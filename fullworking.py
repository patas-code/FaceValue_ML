## ------------------------ STEP 0) IMPORT LIBRARIES---------------------------------------------
from pyfirmata2 import Arduino, util
import numpy as np
import pandas as pd
import time
import pickle
import joblib
from keras.models import load_model
import serial
import sys
import time
import os
import matplotlib as plt
import inspect

import pyfirmata2
import time

def test_connection():
    PORT = 'COM6'  # Change this
    
    try:
        print(f"Attempting to connect to {PORT}...")
        board = pyfirmata2.Arduino(PORT)
        time.sleep(2)
        
        print("✓ Connected successfully!")
        
        # List available pins
        print("\nAvailable pins:")
        print(f"Digital pins: {len(board.digital)}")
        print(f"Analog pins: {len(board.analog)}")
        
        # Show analog pin references
        print("\nAnalog pin references:")
        for i in range(len(board.analog)):
            print(f"  board.analog[{i}] = A{i}")
        
        # Test reading from A0
        print("\nTesting analog pin A0...")
        a0 = board.analog[0]
        a0.enable_reporting()
        
        for i in range(5):
            value = a0.read()
            print(f"  Reading {i+1}: {value}")
            time.sleep(0.5)
        
        board.exit()
        print("\n✓ Test completed successfully!")
        
    except Exception as e:
        print(f"✗ Error: {e}")

if __name__ == "__main__":
    test_connection()