#!/usr/bin/env python

from meta_package import MetaPackage
from package_handler import HandlerWrapper
from typing import List
from textual.app import Widget, ComposeResult
from textual.widgets import Tabs, Tab, Static, Button, Label
import os


class PackageWidget(Static):

    def __init__(
            self,
            data: MetaPackage,
            *,
            name: str | None = None,
            id: str | None = None,
            classes: str | None = None,
            disabled: bool = False,
    ):
        super().__init__(name=name, id=id, classes=classes, disabled=disabled)
        self.package = data
        if self.package.installed:
            self.add_class("installed")

    def compose(self) -> ComposeResult:
        id_checked = self.package.id
        if self.package.installed:
            id_checked = ":heavy_check_mark: " + id_checked
        yield Label(id_checked, id="pkg_id")
        yield Label(self.package.description, id="pkg_descr")
        yield Button("Install", id="install")
        yield Label(self.package.install_script, id="pkg_script")


class PackageList(Widget):
    def new_data(self, data: List):
        for cb in self.query(PackageWidget):
            cb.remove()
        for package in data:
            self.mount(PackageWidget(package))
        self.refresh()


class SuperPackUI(Widget):

    manifest: List = {}
    handlers = HandlerWrapper()

    def compose(self) -> ComposeResult:
        yield Tabs()
        yield PackageList()

    def on_button_pressed(self, event: Button.Pressed) -> None:
        package = event.button.parent.package
        if os.name == "posix":
            driver = self.app._driver
            driver.stop_application_mode()
            self.handlers.install(package)
            driver.start_application_mode()
        elif os.name == "nt":
            self.handlers.install(package)
        self.handlers.check(event.button.parent.package)
        if event.button.parent.package.installed:
            event.button.parent.add_class("installed")
            event.button.parent.refresh()

    def on_tabs_tab_activated(self, event: Tabs.TabActivated) -> None:
        cbl = self.query_one(PackageList)
        if event.tab is None:
            # When the tabs are cleared, event.tab will be None
            cbl.visible = False
        else:
            cbl.visible = True
            category = event.tab.id
            packages = [v for v in self.manifest if v.category == category]
            cbl.new_data(packages)

    def add_data(self, manifest: List) -> None:
        self.manifest = manifest
        cats = set(p.category for p in self.manifest)
        tabs = self.query_one(Tabs)
        tabs.clear()
        for cat in sorted(cats):
            tabs.add_tab(Tab(cat, id=cat))
        self.query_one(Tabs).focus()
