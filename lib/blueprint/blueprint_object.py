import os
import json
import abc


def write_to_file(path: os.path, content) -> None:
    with open(path, "w") as file:
        json.dump(content, file, indent="\t")

def read_from_file(path: os.path) -> dict:
    with open(path, "r") as file:
        return json.load(file)

class BlueprintObject:
    def __init__(self) -> None:
        pass

    @abc.abstractmethod
    def __dict__(self) -> dict:
        raise NotImplementedError()

    def save(self, path: os.path) -> dict:
        write_to_file(path, self.__dict__())

    @abc.abstractmethod
    def load(self, path: os.path) -> dict:
        pass
    
