#!/usr/bin/env python

from enum import Enum
import yaml


class MetaPackage:

    class Type(Enum):
        none = 0
        posix = 1
        powershell = 2
        apt = 3
        snap = 4
        winget = 5

        def __str__(self):
            return f'{self.name}'

    def __init__(self):
        self.id: str = ""
        self.category: str = ""
        self.installed: bool = False
        self.description: str = ""
        self.type: MetaPackage.Type = MetaPackage.Type.none
        self.check_script: str = ""
        self.install_script: str = ""

    @staticmethod
    def from_yaml(data: yaml):
        ret = MetaPackage()
        ret.id = data["id"]
        ret.description = data["descr"]
        ret.category = data["category"]
        ret.type = MetaPackage.Type[data["type"]]
        if "check" in data:
            ret.check_script = data["check"]
        if "install" in data:
            ret.install_script = data["install"]
        return ret

    def __repr__(self) -> str:
        return "%s(id=%r, category=%r, installed=%r, type=%r, description=%r, " \
               "check_script=%r, install_script=%r)" % \
            (self.__class__.__name__,
             self.id,
             self.category,
             self.installed,
             self.type,
             self.description,
             self.check_script,
             self.install_script)

    def __str__(self) -> str:
        return \
                f"{self.id:>20} " + \
                (":heavy_check_mark:" if self.installed else " ") + \
                f" {repr(self.description):>40} {str(self.category):<12}" + \
                f" {str(self.type)}[{repr(self.check_script)}, {repr(self.install_script)}]"
