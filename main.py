from flask import Flask, request, jsonify, send_file, send_from_directory
import pandas as pd
from datetime import datetime
import base64

app = Flask(__name__,static_folder='build')


@app.route('/')
def home():
    return send_from_directory('build',"index.html")

@app.route('/transfer', methods=['POST'])
def get_columns():
    x = int(request.args.get('startyear'))
    y = int(request.args.get('endyear'))
    # print(x)
    if 'file' not in request.files:
        return jsonify({'error': 'No file Send with key "file"'}), 400
    
    file = request.files['file']
    if file.filename == '':
        return jsonify({'error': 'No selected file'}), 400
    # file = 'dfs.xlsx'
    try:
        # Read Excel file
        df = pd.read_excel(file)
        # Get list of columns
        columns = df.columns.tolist()
        df.groupby(["Rank "])["Rank "].count().index
        df.fillna(False,inplace=True)
        df.isnull().sum()
        df = df[df["Rank "].notna()]
        df["Posting year"] = df["Posting year"].astype(int)
        df = df[(df["Posting year"] >= x) & (df["Posting year"] <= y)]
        columns = df.to_json(orient='records')
        mask = (df["Rank "].str.contains("LF", na=False) |
            df["Rank "].str.contains("LF ", na=False) |
            df["Rank "].str.contains("LF  ", na=False) |
            df["Rank "].str.contains("LF (D) ", na=False) |
            df["Rank "].str.contains("LF B", na=False)
        )
        df_LF = df[mask]
        columns = df_LF.shape
        mask1 = (
            df["Rank "].str.contains("FO", na=False) |
            df["Rank "].str.contains("FO ", na=False) |
            df["Rank "].str.contains("FO(B)", na=False) |
            df["Rank "].str.contains("F0", na=False)
        )
        # Apply the boolean mask to filter the DataFrame
        df_FO = df[mask1]

        mask2 = (
            df["Rank "].str.contains("FM", na=False)
        )

        # Apply the boolean mask to filter the DataFrame
        df_FM = df[mask2]
        # df_LF["date of posting "] = pd.to_datetime(df_LF["date of posting "], format='%d.%m.%Y', errors='coerce')

        # Calculate the difference between "date of posting" and the current date
        # current_date = datetime.now()
        # df_LF["posting_age"] = (current_date - df_LF["date of posting "]).dt.days
        # df_LF=df_LF[df_LF["posting_age"]>=1826]
        df_LF=df_LF[["NAME","Station "]]
        # Assuming you have a DataFrame named df_LF with columns 'index', 'NAME', and 'Station '
        df_LF['New_Station'] = ""
        # Create a dictionary to keep track of the counts of each station in 'Station'
        station_counts = df_LF['Station '].value_counts().to_dict()
        # Iterate through the DataFrame
        for index, row in df_LF.iterrows():
            name = row['NAME']
            current_station = row['Station ']
            # Exclude the current station from the available stations
            available_stations = df_LF[df_LF['Station '] != current_station]['Station '].tolist()
            # Remove stations that have reached their count limit
            available_stations = [station for station in available_stations if station_counts.get(station, 0) > 0]
            # Assign a new station from the available stations
            new_station = pd.Series(available_stations).sample(1).iloc[0]
            # Update the DataFrame with the new station
            df_LF.at[index, 'New_Station'] = new_station
            # Update the counts dictionary
            station_counts[new_station] -= 1
        
        
        # Convert "date of posting" to datetime format
        # df_FO["date of posting "] = pd.to_datetime(df_FO["date of posting "], format='%d.%m.%Y', errors='coerce')

        # Calculate the difference between "date of posting" and the current date
        # current_date = datetime.now()
        # df_FO["posting_age"] = (current_date - df_FO["date of posting "]).dt.days

        # Filter out postings older than 5 years (1826 days)
        # df_FO = df_FO[df_FO["posting_age"] >= 1826]

        # Select only the "NAME" and "Station" columns
        df_FO = df_FO[["NAME", "Station "]]

        # Create a new column to store the assigned stations
        df_FO['New_Station'] = ""

        # Create a dictionary to keep track of the counts of each station in 'Station'
        station_counts = df_FO['Station '].value_counts().to_dict()

        # Iterate through the DataFrame
        for index, row in df_FO.iterrows():
            current_station = row['Station ']

            # Exclude the current station from the available stations
            available_stations = df_FO[df_FO['Station '] != current_station]['Station '].tolist()

            # Remove stations that have reached their count limit
            available_stations = [station for station in available_stations if station_counts.get(station, 0) > 0]

            # Assign a new station from the available stations
            new_station = pd.Series(available_stations).sample(1).iloc[0]

            # Update the DataFrame with the new station
            df_FO.at[index, 'New_Station'] = new_station

            # Update the counts dictionary
            station_counts[new_station] -= 1

        # Display the updated DataFrame
        # df_FM["date of posting "] = pd.to_datetime(df_FM["date of posting "], format='%d.%m.%Y', errors='coerce')

        # Calculate the difference between "date of posting" and the current date
        # current_date = datetime.now()
        # df_FM["posting_age"] = (current_date - df_FM["date of posting "]).dt.days

        # Filter out postings older than 5 years (1826 days)
        # df_FM = df_FM[df_FM["posting_age"] >= 1826]

        # Select only the "NAME" and "Station" columns
        df_FM = df_FM[["NAME", "Station "]]

        # Create a new column to store the assigned stations
        df_FM['New_Station'] = ""

        # Create a dictionary to keep track of the counts of each station in 'Station'
        station_counts = df_FM['Station '].value_counts().to_dict()

        # Iterate through the DataFrame
        for index, row in df_FM.iterrows():
            current_station = row['Station ']

            # Exclude the current station from the available stations
            available_stations = df_FM[df_FM['Station '] != current_station]['Station '].tolist()

            # Remove stations that have reached their count limit
            available_stations = [station for station in available_stations if station_counts.get(station, 0) > 0]

            # Assign a new station from the available stations
            new_station = pd.Series(available_stations).sample(1).iloc[0]

            # Update the DataFrame with the new station
            df_FM.at[index, 'New_Station'] = new_station

            # Update the counts dictionary
            station_counts[new_station] -= 1

        # Display the updated DataFrame
        df_LF.to_excel("LF_Data.xlsx",index=False)
        df_FO.to_excel("FO_Data.xlsx",index=False)
        df_FM.to_excel("FM_Data.xlsx",index=False)

        columns = df_FM.to_json(orient='records')
        server_url = request.url_root
        lf_url = server_url + 'download_file/LF_Data.xlsx'
        fo_url = server_url + 'download_file/FO_Data.xlsx'
        fm_url = server_url + 'download_file/FM_Data.xlsx'
        output = {'LF_file' : lf_url,
                  'FO_file' : fo_url,
                  'FM_file' : fm_url}

        return jsonify(output)
    except Exception as e:
        # print(e)
        return jsonify({'error': str(e)}),500

@app.route('/download_file/<file>', methods=['GET'])
def download_file(file):
    # Replace 'your_file_path.txt' with the path to the file you want to download
    file_path = file
    try:
        # Send the file as a response
        return send_file(file_path, as_attachment=True)
    except FileNotFoundError:
        return "File not found"



# if __name__ == '__main__':
#     app.run(debug=True)
