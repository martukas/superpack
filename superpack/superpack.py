#!/usr/bin/env python

import meta_package
from package_handler import HandlerWrapper
from superpack_widgets import SuperPackUI
from typing import List
from textual.app import App, ComposeResult
from textual.widgets import Header, Footer, TextLog
from rich.console import Console
import yaml
import sys


def read_manifest(file_path: str) -> List:
    file = open(file_path, "r")
    ret = [meta_package.MetaPackage.from_json(p) for p in yaml.unsafe_load(file)]
    file.close()
    return ret


class MyApp(App):

    TITLE = "SuperPack Meta-package Utility"
    CSS_PATH = "superpack.css"
    BINDINGS = [
        ("q", "quit", "Quit")
    ]

    manifest: List

    def __init__(self, manifest: List) -> None:
        super().__init__()
        self.manifest = manifest

    def compose(self) -> ComposeResult:
        yield Header()
        yield SuperPackUI()
        yield Footer()

    def on_mount(self) -> None:
        self.query_one(SuperPackUI).add_data(self.manifest)


if __name__ == "__main__":
    console = Console(markup=True, emoji=True)
    manifest = []
    if len(sys.argv) > 1:
        json_path = sys.argv[1]
        manifest = read_manifest(json_path)
    if len(sys.argv) > 2 and sys.argv[2] == "read":
        console.print(manifest)
        exit(0)
    force = len(sys.argv) > 2 and sys.argv[2] == "-f"
    HandlerWrapper(force=force).check_all(manifest)
    if len(sys.argv) > 2 and sys.argv[2] == "check":
        for package in manifest:
            console.print(str(package))
        exit(0)
    app = MyApp(manifest)
    app.run()
