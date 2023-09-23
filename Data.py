
import pandas as pd
import sqlite3

# Read the excel table and load it into pandas
mydata = pd.read_excel('data.xlsx', header=None)
mydata.columns = mydata.iloc[0]  # Set the first row as column headers
mydata = mydata[1:]  # Remove the first row

# Connect to MySQL database
conn = sqlite3.connect('database.db')
    
#Insert dataframe into the database
mydata.to_sql('Insuarance', conn, if_exists='replace', index=False)


conn.close()