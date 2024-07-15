import pandas as pd
import os

class CSVSheetReader:
    def __init__(self, file_path):
        self.file_path = file_path
        self.sheets = {}

    def read_csv_sheets(self):
        try:
            df = pd.read_csv(self.file_path)
            
            sheet_names = df.iloc[:, 0].unique()
            
            for sheet_name in sheet_names:
                sheet_df = df[df.iloc[:, 0] == sheet_name].iloc[:, 1:]
                
                # Reset index and set the first row as header
                sheet_df = sheet_df.reset_index(drop=True)
                sheet_df.columns = sheet_df.iloc[0]
                sheet_df = sheet_df.iloc[1:].reset_index(drop=True)
                
                # Store the DataFrame in the dictionary
                self.sheets[sheet_name] = sheet_df
        
            return True
        
        except Exception as e:
            print(f"An error occurred: {str(e)}")
            return False

    def get_sheet(self, sheet_name):
        return self.sheets.get(sheet_name)

    def get_all_sheets(self):
        return self.sheets

    def print_sheet_info(self):
        for sheet_name, df in self.sheets.items():
            print(f"\nSheet: {sheet_name}")
            print(df.head())
            print(f"Shape: {df.shape}")

def main():
    file_path = input("Enter the path to the CSV file: ")
    
    if not os.path.exists(file_path):
        print("File not found. Please enter a valid file path.")
        return
    
    reader = CSVSheetReader(file_path)
    if reader.read_csv_sheets():
        print(f"Successfully read {len(reader.get_all_sheets())} sheets from the CSV file.")
        reader.print_sheet_info()

