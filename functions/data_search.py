import pandas as pd
from config.log_config import logger

class dataSearcher:
    def __init__(self, df: pd.DataFrame):
        if not isinstance(df, pd.DataFrame):
            logger.error("Input is not a pandas DataFrame.")
            raise ValueError("Input is not a pandas DataFrame.")
        self.df = df
    
    def _search_data(self, df, **kwargs):
        try:
            # Make a copy to avoid modifying the original DataFrame and exclude the first three rows
            result_df = df.iloc[3:].copy()

            # Apply filters based on kwargs
            for key, value in kwargs.items():
                if key in result_df.columns:
                    result_df = result_df[result_df[key] == value]
                else:
                    logger.warning(f"Column '{key}' not found in the DataFrame. Skipping this filter.")

            # Check if any rows remain after filtering
            if result_df.empty:
                logger.info("No data matches the specified criteria.")
                return None

            logger.info(f"Found {len(result_df)} matching rows.")
            
            return result_df
        
        except Exception as e:
            logger.error(f"An error occurred during the search: {str(e)}")
            return None
    

""" # Example usage
record = {
    'Name': ['Ankit', 'Amit', 'Aishwarya', 'Priyanka', 'Priya', 'Shaurya'],
    'Age': [21, 19, 20, 18, 17, 21],
    'Stream': ['Math', 'Commerce', 'Science', 'Math', 'Math', 'Science'],
    'Percentage': [88, 92, 95, 70, 65, 78]
}

dataframe = pd.DataFrame(record)
searcher = DataFrameSearcher(dataframe)

# Search in single file
result_single = searcher.search_data_single_file(Name='Priyanka')
print(result_single)

# Search in multiple files (though for demonstration, it's the same method as single file)
result_multiple = DataFrameSearcher.search_data_multiple_files(dataframe, Name='Priyanka')
print(result_multiple) """
