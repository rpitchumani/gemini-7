"""
Utility Functions which work together with the Gemini 7 Class
"""

from typing import List, Dict, Any
import os
import glob
from pathlib import Path
import datetime
from tqdm import tqdm
import re

from gemini_7 import Gemini7


def get_gemini_7_file_list(gemini7_path: str) -> List:

    gemini7_sa_pattern = "*SA.XLS"

    gemini7_sa_files = glob.glob(os.path.join(gemini7_path,
                                              gemini7_sa_pattern))

    return gemini7_sa_files


def get_gemini_7_data_from_list(sa_files: List) -> List[Dict]:

    re_pattern_sample_id = "(L|R\d\d\d\d\d\d\d\d-\d\d\d\S?)"
    list_gemini7_data = []

    for sa_file in tqdm(sa_files):

        sa_pathlib = Path(sa_file)
        sa_stem = sa_pathlib.stem

        gem = Gemini7(sa_file)

        file_name_id = re.findall(re_pattern_sample_id, sa_stem)[0]

        try:
            if gem.grade != gem.grade:
                grade_id = ""
            else:
                grade_id = re.findall(re_pattern_sample_id, gem.grade)[0]

            dict_gemini7_data = {
                "file_path": sa_file,
                "file_name": sa_stem,
                "grade": gem.grade.strip(),
                "operator": gem.operator,
                "bet": gem.bet,
                "single point": gem.single_point,
                "lot": gem.lot.strip(),
                "file_name_id": file_name_id,
                "grade_id": grade_id
            }

            list_gemini7_data.append(dict_gemini7_data)

        except Exception as e:
            ...

    return list_gemini7_data
