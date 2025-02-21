from typing import List
import json
import pandas as pd


class FileProcessor:
    def __init__(self, file_path: str, output_path: str) -> None:
        self._file_path = file_path
        self.output_path = output_path

    def remote_csv_to_json(self, url: str, columns: List[str], name: str) -> None:
        name = name.replace(",", "").strip()
        df = pd.read_csv(url, usecols=columns)
        result = df.to_json(orient="values")
        output = {}
        for key, value in json.loads(result):
            current_value = output.get(key, None)
            if current_value is None:
                output[key] = value
            if type(current_value) is str:
                output[key] = [value, current_value]
            if type(current_value) is list:
                output[key].append(value)

        with open(f"{self.output_path}/{name}.json", "a") as json_file:
            json_file.write(json.dumps(output))
