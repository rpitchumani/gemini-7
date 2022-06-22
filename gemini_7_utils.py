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