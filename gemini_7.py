"""
Class to read exported Gemini 7 Surface Area Analyzer XLS File
2022, Ramanan Pitchumani
"""

from typing import List, Dict, Any
import pandas as pd

class Gemini7:

    def __init__(self, path_xls: str):

        self.path_xls = path_xls
        self.df = pd.read_excel(
            self.path_xls,
            sheet_name=0,
            header=None,
            skiprows=0,
            engine="xlrd")

        self.get_sample_information()
        self.get_surface_areas()

    def get_sample_information(self):

        dict_sample = self.get_adjacent_value(self.df[[0, 1]], "Sample:")
        self.sample = list(dict_sample.values())[0]

        dict_operator = self.get_adjacent_value(self.df[[0, 1]], "Operator:")
        self.operator = list(dict_operator.values())[0]

        dict_grade = self.get_adjacent_value(self.df[[0, 1]], "Grade:")
        self.grade = list(dict_grade.values())[0]

        dict_lot = self.get_adjacent_value(self.df[[0, 1]], "Lot:")
        self.lot = list(dict_lot.values())[0]

    def get_surface_areas(self):

        dict_bet = self.get_adjacent_value(self.df,
                                           "BET Surface Area:")

        self.bet = float(list(dict_bet.values())[0].split(" ")[0])

        dict_single_point = self.get_adjacent_value_containing(
            self.df,
            "Single point surface area at p")

        self.single_point = float(
            list(dict_single_point.values())[0].split(" ")[0])

    """
    Utility Functions
    """
    def get_positions_of_value(self,
                               df_object: pd.DataFrame,
                               value: Any) -> List[Dict]:

        """ Get index positions of value in dataframe i.e. dfObj."""
        list_positions = list()

        # Get bool dataframe with True at positions where the given value exists
        result = df_object.isin([value])

        # Get list of columns that contains the value
        series_object = result.any()
        column_names = list(series_object[series_object == True].index)

        # Iterate over list of columns and fetch the rows indexes where value exists
        for col in column_names:

            rows = list(result[col][result[col] == True].index)

            for row in rows:

                list_positions.append((row, col))

        # Return a list of tuples indicating the positions of value in the dataframe
        return list_positions

    def get_adjacent_value(self,
                           df_object: pd.DataFrame,
                           value: Any) -> Any:

        list_position = self.get_positions_of_value(df_object, value)

        result_dict = {}
        if len(list_position) == 1:

            result_dict = {
                df_object.iloc[list_position[0][0], list_position[0][1]]:
                    df_object.iloc[list_position[0][0], list_position[0][1]+1]
            }

            return result_dict

        else:

            return result_dict

    def get_adjacent_value_containing(self,
                                      df_object: pd.DataFrame,
                                      value: Any) -> Any:

        df_contains = df_object.apply(
            lambda col:col.str.contains(value, na=False, case=True), axis=1)

        stacked_positions = df_contains.stack()

        list_position = stacked_positions[stacked_positions].index.tolist()

        result_dict = {}

        if len(list_position) == 1:

            result_dict = {
                df_object.iloc[list_position[0][0], list_position[0][1]]:
                    df_object.iloc[list_position[0][0], list_position[0][1]+1]
            }

            return result_dict

        else:

            return result_dict
