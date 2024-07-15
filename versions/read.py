import csv
import os
from datetime import datetime

class CSVDataExtractor:
    def __init__(self, file_path):
        self.file_path = file_path
        self.extracted_data = None

    def extract_data(self):
        try:
            with open(self.file_path, 'r', newline='', encoding='utf-8') as csvfile:
                csv_reader = csv.reader(csvfile, delimiter=';')
                
                next(csv_reader)
                
                second_row = next(csv_reader)
                
                self.extracted_data = second_row[:4]
                
                return True
        except Exception as e:
            print(f"An error occurred while extracting data: {str(e)}")
            return False

    def get_extracted_data(self):
        return self.extracted_data

    def print_extracted_data(self):
        if self.extracted_data:
            print("Extracted Data:")
            print(f"Date: {self.extracted_data[0]}")
            print(f"File Identifier: {self.extracted_data[1]}")
            print(f"Version 1: {self.extracted_data[2]}")
            print(f"Version 2: {self.extracted_data[3]}")
        else:
            print("No data has been extracted yet.")

    @staticmethod
    def is_valid_date(date_string):
        try:
            datetime.strptime(date_string, '%d.%m.%Y')
            return True
        except ValueError:
            return False

def main():
    file_path = input("Enter the path to the CSV file: ")
    
    if not os.path.exists(file_path):
        print("File not found. Please enter a valid file path.")
        return
    
    extractor = CSVDataExtractor(file_path)
    if extractor.extract_data():
        print("Data extracted successfully.")
        extractor.print_extracted_data()
        
        # Validate the date
        extracted_data = extractor.get_extracted_data()
        if extracted_data and CSVDataExtractor.is_valid_date(extracted_data[0]):
            print("The extracted date is valid.")
        else:
            print("Warning: The extracted date is not valid or missing.")
    else:
        print("Failed to extract data from the CSV file.")

