import os
import time
import utils
import pandas as df
from alive_progress import alive_bar


# current_location = os.getcwd()
current_location = '/home/vangogh/Downloads/Compressed/db/k2-migrate/localhost-1/fixbugs_j3_k2_migrate'
# current_location = '/media/vangogh/084ad0f6-fe03-4469-aa8f-a69b6e9ec3ad/home/vangogh/utils/data/dataset'
all_files = os.listdir(current_location)
search_str1 = 'Racconti, guide e itinerar'
search_str2 = 'Colori su carta di riso'


def read_csv_data(path):
    # use single thread
    # or use multithread
    total_search = len(all_files)
    with alive_bar(total_search, dual_line=True, title='Run searching') as bar:
        for file in all_files:
            try:
                data = df.read_csv(os.path.join(path, file), dtype='object')
                data_df = df.DataFrame(data)
                if 'k2_items' in file:
                    print(len(data_df))
                all_columns = data_df.columns
                # with alive_bar(len(all_columns), dual_line=True, title='Run searching in column') as bar1:
                for column in all_columns:
                    if data[column].dtype == 'object' and data_df[column].str.contains(search_str2).any():
                        print(f'file: {file} - column: {column}')
                    # bar1()
            except RuntimeError as err:
                print(err)
            bar()


# read_csv_data(current_location)
# data = df.read_csv(os.path.join(current_location, 'coc2b_k2_categories.csv'))
# data_df = df.DataFrame(data)
# all_columns = data_df.columns
#
# for column in all_columns:
#     if data[column].dtype == 'object' and data_df[column].str.contains(search_str2).any():
#         print(f'in column: {column}')


data = df.read_csv(os.path.join('/home/vangogh/Downloads/Compressed/db', 'coc2b_k2_items-k2-migrate.csv'))
data_df = df.DataFrame(data)
print(len(data_df))