import pandas as pd
import numpy as np
import sys


class Describe:
    """
    Class that computes descriptive statistics for a given dataset.
    It includes the following statistics, calculated on object initialization:
    - count
    - missing values
    - mean
    - variance
    - standard deviation
    - minimum
    - 25th percentile
    - 50th percentile (median)
    - 75th percentile
    - interquartile range
    - maximum
    - mode
    - kurtosis
    """

    def __init__(self, data):
        """
        Constructor:
        - Initializes the data
        - Initializes the stats dictionary
        - Calls all the functions to calculate the statistics
        """
        self.data = data
        numeric_cols = data.select_dtypes(include=[np.number]).columns
        self.stats = {col: {}
                      for col in numeric_cols if col != "Hogwarts House"}
        self.get_count()
        self.get_missing_values()
        self.get_mean()
        self.get_var()
        self.get_std()
        self.get_min()
        self.get_25()
        self.get_50()
        self.get_75()
        self.get_iqr()
        self.get_max()
        self.get_mode()
        self.get_kurtosis()

    def get_count(self):
        """
        Finds the number of non-NaN values in every column.
        """
        for col in self.stats:
            data_col = self.data[col].dropna()
            self.stats[col]["count"] = data_col.shape[0]

    def get_missing_values(self):
        """
        Finds the number of NaN values (%) in every column.
        """
        for col in self.stats:
            data_col = self.data[col]
            count = data_col.shape[0]
            missing_values = count - self.stats[col]["count"]
            self.stats[col]["missing(%)"] = round(
                missing_values / count * 100, 6)

    def get_mean(self):
        """
        Finds the mean of every column.
        """
        for col in self.stats:
            data_col = self.data[col].dropna()
            mean = sum(data_col) / self.stats[col]["count"]
            self.stats[col]["mean"] = round(mean, 6)

    def get_var(self):
        """
        Finds the variance of every column.
        We use the Bessel's correction to calculate the sample variance.
        """
        for col in self.stats:
            data_col = self.data[col].dropna()
            mean = sum(data_col) / self.stats[col]["count"]
            variance = sum([(i - mean)**2 for i in data_col]) / \
                (self.stats[col]["count"] - 1)
            self.stats[col]["var"] = round(variance, 6)

    def get_std(self):
        """
        Finds the standard deviation of every column.
        """
        for col in self.stats:
            variance = self.stats[col]["var"]
            self.stats[col]["std"] = np.sqrt(variance).round(6)

    def get_min(self):
        """
        Finds the minimum value of every column.
        """
        for col in self.stats:
            self.stats[col]["min"] = self.data[col][0]
            for i in self.data[col]:
                if not np.isnan(i):
                    if i < self.stats[col]["min"]:
                        self.stats[col]["min"] = round(i, 6)

    def get_25(self):
        """
        Finds the 25th percentile of every column.
        """
        for col in self.stats:
            data_col = self.data[col].dropna()
            data_col = data_col.sort_values().reset_index(drop=True)
            value = ((self.stats[col]["count"]) - 1) * 0.25
            if value % 1 == 0:
                value = int(value)
                quartile = data_col[value]
            else:
                lower_value = int(value)
                upper_value = lower_value + 1
                interpolation = value - lower_value
                quartile = (data_col[lower_value] * (1 - interpolation)
                            ) + (data_col[upper_value] * interpolation)
            quartile = round(quartile, 6)
            self.stats[col]["25%"] = quartile

    def get_50(self):
        """
        Finds the 50th percentile of every column.
        """
        for col in self.stats:
            data_col = self.data[col].dropna()
            data_col = data_col.sort_values().reset_index(drop=True)
            value = ((self.stats[col]["count"]) - 1) * 0.50
            if value % 1 == 0:
                value = int(value)
                quartile = data_col[value]
            else:
                lower_value = int(value)
                upper_value = lower_value + 1
                interpolation = value - lower_value
                quartile = (data_col[lower_value] * (1 - interpolation)
                            ) + (data_col[upper_value] * interpolation)
            quartile = round(quartile, 6)
            self.stats[col]["50%"] = quartile

    def get_75(self):
        """
        Finds the 75th percentile of every column.
        """
        for col in self.stats:
            data_col = self.data[col].dropna()
            data_col = data_col.sort_values().reset_index(drop=True)
            value = ((self.stats[col]["count"]) - 1) * 0.75
            if value % 1 == 0:
                value = int(value)
                quartile = data_col[value]
            else:
                lower_value = int(value)
                upper_value = lower_value + 1
                interpolation = value - lower_value
                quartile = (data_col[lower_value] * (1 - interpolation)
                            ) + (data_col[upper_value] * interpolation)
            quartile = round(quartile, 6)
            self.stats[col]["75%"] = quartile

    def get_max(self):
        """
        Finds the maximum value of every column.
        """
        for col in self.stats:
            self.stats[col]["max"] = self.data[col][0]
            for i in self.data[col]:
                if not np.isnan(i):
                    if i > self.stats[col]["max"]:
                        self.stats[col]["max"] = round(i, 6)

    def get_mode(self):
        """
        Finds the mode of every column.
        """
        for col in self.stats:
            data_col = self.data[col].dropna()
            data_col = data_col.sort_values().reset_index(drop=True)
            mode = data_col[0]
            count = 0
            max_count = 0
            for i in range(1, len(data_col)):
                if data_col[i] == data_col[i - 1]:
                    count += 1
                else:
                    if count > max_count:
                        max_count = count
                        mode = data_col[i - 1]
                    count = 0
            self.stats[col]["mode"] = mode

    def get_iqr(self):
        """
        Finds the interquartile range of every column.
        It's less sensible to extreme values than the standard deviation.
        """
        for col in self.stats:
            self.stats[col]["iqr"] = self.stats[col]["75%"] - \
                self.stats[col]["25%"]

    def get_kurtosis(self):
        """
        Finds the kurtosis of every column.
        - If kurtosis > 3, the distribution is leptokurtic (more peaked).
        - If kurtosis < 3, the distribution is platykurtic (less peaked).
        - If kurtosis = 3, the distribution is mesokurtic (Gauss).
        """
        for col in self.stats:
            data_col = self.data[col].dropna()
            mean = self.stats[col]["mean"]
            std = self.stats[col]["std"]
            kurtosis = sum([((i - mean) / std)**4 for i in data_col]) / \
                self.stats[col]["count"]
            self.stats[col]["kurtosis"] = round(kurtosis, 6)

    def find_max_width(self, items):
        """
        Finds the maximum width of a list of strings.
        """
        max_width = 0
        for item in items:
            if len(item) > max_width:
                max_width = len(item)
        return max_width

    def print_stats(self):
        """
        Prints the statistics in a pretty format.
        """
        first_col = next(iter(self.stats))
        stats_headers = list(self.stats[first_col].keys())
        stats_data = {}
        for col in self.stats:
            stats_data[col] = []
            for stat in stats_headers:
                value = self.stats[col].get(stat, 'NaN')
                if isinstance(value, float) or isinstance(value, int):
                    stats_data[col].append(f"{value:.6f}")
                else:
                    stats_data[col].append(str(value))

        columns = list(self.stats.keys())
        cols_per_row = 3

        for i in range(0, len(columns), cols_per_row):
            selected_columns = columns[i:i + cols_per_row]
            col_widths = []
            for col in selected_columns:
                max_width = self.find_max_width([col] + stats_data[col])
                col_widths.append(max_width)
            column_headers = [""] + selected_columns
            header_row = "".join(
                [f"{column_headers[j]:<{col_widths[j-1] + 2}}"
                    for j in range(1, len(column_headers))])
            print(f"{'':<15}{header_row}")
            for stat in stats_headers:
                row_data = [f"{stat:<15}"]
                for j, col in enumerate(selected_columns):
                    formatted_stat = f"{stats_data[col][stats_headers.index(stat)]:<{col_widths[j] + 2}}"
                    row_data.append(formatted_stat)
                print("".join(row_data))
            print("-" * 60)


def load_dataset(path):
    """
    Loads a dataset from a given path and returns it as a pandas DataFrame.
    """
    return pd.read_csv(path)


def main(arg):
    """
    Main function:
    - Loads the dataset
    - Creates a Describe object for the dataset
    - Prints the statistics
    """
    data = load_dataset(arg[1])
    myDescribe = Describe(data)
    myDescribe.print_stats()


if __name__ == "__main__":
    """
    Main entry point of the program:
    - Checks that the user has provided a dataset
    - Checks that the dataset is a .csv file
    - Calls the main function
    """
    sys.tracebacklimit = 0
    assert len(sys.argv) == 2, "Usage: python describe.py <your_dataset.csv>"
    assert sys.argv[1].endswith(".csv"), "Dataset must be a .csv file"
    main(sys.argv)
