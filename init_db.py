#!/usr/bin/env python
# coding: utf-8

# Part 1: Data Management - Initialize SQLite Database

import sqlite3
import pandas as pd

# Read raw CSV
celldf = pd.read_csv('cell-count.csv')

# Create (or overwrite) the SQLite database
conn = sqlite3.connect('cell_count.db')

# Load the full dataset into a table called 'cell_counts'
celldf.to_sql('cell_counts', conn, if_exists='replace', index=False)

print(f"Database initialized: cell_count.db")
print(f"  Table 'cell_counts': {len(celldf)} rows, {len(celldf.columns)} columns")

conn.close()
