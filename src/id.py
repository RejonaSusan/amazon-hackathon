import pandas as pd
import os

def add_index_column(input_csv_path, output_csv_path):

    df = pd.read_csv(input_csv_path)
    df.insert(0, 'index', range(len(df)))
    df.to_csv(output_csv_path, index=False)

if __name__ == '__main__':
    input_csv_path = os.path.join("../dataset", "train.csv")
    output_csv_path = os.path.join("../dataset", "train2.csv")
    
    add_index_column(input_csv_path, output_csv_path)
