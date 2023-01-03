import pandas as pd
import numpy as np
import os
import seaborn as sb
import matplotlib.pyplot as plt
from tabulate import tabulate
from pandas.plotting import scatter_matrix
import os
import shutil
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd

PATH_DATA = 'dataset'
PATH_RESULT = 'result'
PATH_RESULT_TEXT = os.path.join(PATH_RESULT, 'result_text')
PATH_PLOT = os.path.join(PATH_RESULT, 'plot_data')
os.makedirs(PATH_RESULT_TEXT, exist_ok=True)
os.makedirs(PATH_PLOT, exist_ok=True)
FILE_RESULT = 'wine.txt'


# save picture
def save_fig(fig_id, tight_layout=True, fig_extension='png', resolution=300):
    path = os.path.join(PATH_PLOT, fig_id + '.' + fig_extension)
    print('Saving figure', fig_id)
    if tight_layout:
        plt.tight_layout()
    plt.savefig(path, format=fig_extension, dpi=resolution)


# write result to file
def save_result(file_name, result, mode):
    with open(PATH_RESULT_TEXT + '/' + file_name, mode=mode) as file:
        file.write(result + '\n======================================================================\n')
        print('File saved:', PATH_RESULT_TEXT + '/' + file_name)


def create_data_folder():
    # Create folder dataset
    os.makedirs('dataset', exist_ok=True)
    # Check file
    only_files = [f for f in os.listdir() if os.path.isfile(os.path.join(f))]
    # Remove file in folder dataset
    for file in only_files:
        format_file = file.split('.')[-1].lower()
        if format_file == 'csv':
            print(file)
            if os.path.exists(file):
                shutil.move(file, 'dataset')
                print('Move success!')
        else:
            pass


create_data_folder()


def read_data():
    data_red = pd.read_csv('dataset/winequality_red.csv')
    data_white = pd.read_csv('dataset/winequality_white.csv')

    data_red['type'] = 'red'
    data_white['type'] = 'white'
    data_merge = np.concatenate([data_red, data_white], axis=0)
    data_df = pd.DataFrame(data_merge, columns=data_red.columns)
    data_df.to_csv('{}/winequality.csv'.format(PATH_DATA), index=False, header=True)

    return data_red, data_white, data_df


# ------------------------------------------|
# Visualize data by text information
# ------------------------------------------|
def visualize_data(data, save=True, main_attr='quality'):
    info = data.info()
    head = data.head
    describe = data.describe()
    corr = data.corr()[main_attr].sort_values(ascending=False)
    if save:
        save_result(FILE_RESULT, 'data.info():\n' + str(info), 'a+')
        save_result(FILE_RESULT, 'data.head():\n' + str(head), 'a+')
        save_result(FILE_RESULT, 'data.describe():\n' + str(describe), 'a+')
        save_result(FILE_RESULT, 'correlation among attrs:\n' + str(corr), 'a+')
    print(info, '\n', head, '\n', describe, '\n', corr)


# Correlation between many attrs vs Main attr
def corr_main_attr(data, save=True, main_attr='quality'):
    corr = data.corr()[main_attr].sort_values(ascending=False)
    content = 'Correlation num attr vs ' + str(main_attr)
    if save:
        save_result(FILE_RESULT, content + '\n' + str(corr), 'a+')
    return corr


# Correlation between One attr vs Main attr
# Related to FactorPlot
def corr_one_vs_main_attr(data, attr, content, save=True, main_attr='quality'):
    corr = data[[attr, main_attr]].groupby([attr]).mean()
    if save:
        save_result(FILE_RESULT, content + '\n' + str(corr), 'a+')
    print(corr)
    return corr


# Count value attr
def value_counts(data, attr):
    print(data[attr].value_counts())
    return data[attr].value_counts()


# attr and main attr rate
def rate_attr_vs_main(data, attr, main_attr='quality'):
    print(data[[attr, main_attr]].groupby([attr]).mean())
    return data[[attr, main_attr]].groupby([attr]).mean()


# Check null values
def check_null(data, save=True):
    null = data.isnull().sum()
    if save:
        save_result(FILE_RESULT, 'Null values:\n' + str(null), 'a+')
    print(null)


# --------------------------------------------------------------|
# Visualize data by Plotting
# 1. Plot Numerical values
# --------------------------------------------------------------|
# Correlation scatter matrix between num values
def plot_scatter_matrix(data, save=True):
    scatter_matrix(data, figsize=(20, 10))
    plt.title('num_val_scatter_matrix')
    if save:
        save_fig('num_val_scatter_matrix')
    plt.show()


# Plot heatmap matrix Correlation between num Values
def plot_heatmap_corr(data, save=True):
    plt.figure(figsize=(13, 6))
    sb.heatmap(data.corr(), annot=True, fmt='.2f', cmap='coolwarm')
    plt.title('Heatmap_num_values')
    if save:
        save_fig('Heatmap_num_values')
    plt.show()


# Plot scatter matrix an Attr vs Main attr
def plot_attr_vs_main(data, attr, save=True, main_attr='quality'):
    data.plot(kind='scatter', x=attr, y=main_attr, alpha=.2)
    plt.title(attr + '_vs_' + main_attr + '_scatter_matrix')
    if save:
        save_fig(attr + '_vs_' + main_attr + '_scatter_matrix')
    plt.show()


# Explore attr vs Main attr
def plot_factor_attr_vs_main(data, attr, kind='bar',  main_attr='quality', save=True):
    factor = sb.factorplot(x=attr, y=main_attr, data=data,
                  kind=kind, size=6, palette='muted')
    factor.despine(left=True)
    factor.set_ylabels(main_attr)
    plt.title(attr + '_vs_' + main_attr + '_' + kind)
    if save:
        save_fig(attr + '_vs_' + main_attr + '_' + kind)
    plt.show()


# Explore facetGrid attr vs Main attr
def plot_facet_grid(data, attr, save=True, main_attr='quality'):
    facet_grid = sb.FacetGrid(data, col=main_attr)
    facet_grid.map(sb.distplot, attr)  # displot: draw line bounding bar, poinplot: draw point and line
    plt.title(attr + '_vs_' + main_attr + '_facetGrid')
    if save:
        save_fig(attr + '_vs_' + main_attr + '_facetGrid')
    plt.show()


# Plot histogram
def plot_histogram_all_attr(data, save=True):
    data.hist(figsize=(20, 10))
    plt.title('plot_histogram')
    if save:
        save_fig('plot_histogram')
    plt.show()


# Plot histogram with one Attr
def plot_histogram_one_attr(data, attr, save=True):
    data[attr].hist()
    plt.title(attr + '_histogram')
    if save:
        save_fig(attr + '_histogram')
    plt.show()


# Explore attr distribution
def plot_attr_distribution(data, attr, save=True, main_attr='quality'):
    kdep = sb.kdeplot(data[attr][(data[main_attr] == 0) & (data[attr].notnull())], color='Red', shade=True)
    kdep = sb.kdeplot(data[attr][(data[main_attr] == 1) & (data[attr].notnull())], ax=kdep, color='Blue', shade=True)
    kdep.set_xlabel(attr)
    kdep.set_ylabel('Frequency')
    kdep.legend(['Not quality', 'quality'])
    plt.title(attr + '_kdepPlot_distribution')
    if save:
        save_fig(attr + '_kdepPlot_distribution')
    plt.show()


# Explore One attr vs Main attr by Other attr
def plot_factor_attr_vs_main_by_other(data, attr, by_attr, save=True, main_attr='quality'):
    factor = sb.factorplot(x=attr, y=main_attr, hue=by_attr,
                           data=data, size=5, kind='bar',
                           palette='muted')
    factor.despine(right=True)
    factor.set_ylabels('Survival Probability')
    plt.title(attr + '_' + main_attr + '_by_' + by_attr + '_factorPlot')
    if save:
        save_fig(attr + '_' + main_attr + '_by_' + by_attr + '_factorPlot')
    plt.show()


# Explore
def plot_factor_count(data, attr, save=True, main_attr='quality'):
    factor = sb.factorplot(attr, col=main_attr, data=data,
                           size=6, kind='count', palette='muted')
    factor.despine(left=True)
    plt.title(attr + '_vs_' + main_attr + '_factorPlot')
    if save:
        save_fig(attr + '_vs_' + main_attr + '_factorPlot')
    plt.show()


# ------------------------------------------|
# Categorical values Plot
# ------------------------------------------|
def plot_bar_attr_vs_main(data, attr, save=True, main_attr='quality'):
    bar = sb.barplot(x=attr, y=main_attr, data=data)
    bar.set_ylabel(main_attr)
    plt.title(attr + '_vs_' + main_attr + '_barPlot')
    if save:
        save_fig(attr + '_vs_' + main_attr + '_barPlot')
    plt.show()


# Plot count value
def plot_count(data, attr, save=True):
    count = sb.countplot(x=attr, data=data)
    plt.setp(count.get_xticklabels(), rotation=45)
    plt.title(attr + '_count_plot')
    if save:
        save_fig(attr + '_count_plot')
    plt.show()


# attr histogram depending on 1 attr
def plot_facet_grid_2attrs(data, attr, save=True, main_attr='quality'):
    grid = sb.FacetGrid(data, col=main_attr)
    grid.map(plt.hist, attr, bins=15)
    # plt.title('facet_grid_{}_vs_{}'.format(attr, main_attr), fontsize=7)
    if save:
        save_fig('facet_grid_{}_vs_{}'.format(attr, main_attr))
    plt.show()


# attr histogram depending on 2 attrs
def plot_facet_grid_3attrs(data, attr, attr1, save=True, attr2='quality'):
    grid = sb.FacetGrid(data, col=attr2, row=attr1, size=2.2, aspect=1.6)
    grid.map(plt.hist, attr, alpha=.5, bins=20)
    # grid.add_legend()
    if save:
        save_fig('facet_grid_{}_vs_{}_and_{}'.format(attr, attr1, attr2))
    plt.show()


# func.plot_count(dataset, 'Title')
# func.plot_bar_attr_vs_main(dataset, 'Title')
# count = sb.countplot(dataset['Title'])
# count.set_xticklabels(['Master', 'Miss/Ms/Mme/Mlle/Mrs', 'Mr', 'Rare'])
# plt.title('Count..')
# func.save_fig('Count_title_plot')
# plt.show()

# bar_plot = sb.barplot(x='Title', y='quality', data=dataset)
# bar_plot.set_xticklabels(['Master', 'Miss-Mrs', 'Mr', 'Rare'])
# plt.title('Survival probability between Male and Female')
# func.save_fig('Survival probability between Male and Female')
# plt.show()

# Line 158 in c3_titanic_redo_kaggle.py
# sb.countplot('Cabin', data=dataset, order=['A', 'B', 'C', 'D', 'E', 'F', 'G', 'T', 'X'])
# func.save_fig('cabin_count_plot')
# plt.show()

# factor = sb.factorplot(x='Cabin', y='quality', data=dataset,
#                        kind='bar', size=10, order=['A', 'B', 'C', 'D', 'E', 'F', 'G', 'T', 'X'])
# factor.set_ylabels('Survival Probability')
# func.save_fig('Cabin_and_survival_probability_factor_plot1')
# plt.show()
