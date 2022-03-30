import os
from time import sleep
from typing import Union, Tuple, List

import pandas as pd
import json

from tqdm import tqdm


class FileReader:

    def __init__(self):
        self.file_path = None

    def file_iterator(self, file_path, batch_size):
        """
        Iterate over a file in batches of a given size.
        """
        with open(file_path, 'r') as f:
            while True:
                batch = []
                for _ in range(batch_size):
                    line = f.readline()
                    if line:
                        batch.append(line)
                    else:
                        if batch:
                            yield batch
                        else:
                            return
                yield batch

    def get_file_size(self, file_path: str) -> int:
        """
        Get the size in B of a file.
        :param file_path:
        :return:
        """
        return os.path.getsize(file_path)

    def file_iterator_with_progress_bar(
            self,
            file_path: str,
            batch_size: int,
            progress_bar: bool = True
        ) -> Tuple[List[str], int]:
        """
        Iterate over a file in batches of a given size.
        :param file_path:
        :param batch_size:
        :param progress_bar:
        :return:
        """
        with open(file_path, 'r') as f:
            if progress_bar:
                pbar = tqdm(total=self.get_file_size(file_path))
            while True:
                batch = []
                for _ in range(batch_size):
                    line = f.readline()
                    if line:
                        batch.append(line)
                    else:
                        if batch:
                            yield batch, len(batch)
                        else:
                            return
                if progress_bar:
                    pbar.update(len(batch))
                yield batch, len(batch)

    def json_file_iterator(self, filename: str) -> dict:
        """
        Iterate over a json file.
        :param filename:
        :return:
        """
        f = open(filename, 'r')
        data = f.read()
        f.close()
        for element in json.loads(data):
            yield element
