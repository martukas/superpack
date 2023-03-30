#!/usr/bin/env python

from meta_package import MetaPackage
import shell_wrapper
from typing import List
import os


class PosixHandler:
    type = MetaPackage.Type.posix

    @staticmethod
    def run(script: str) -> None:
        shell_wrapper.run_interactive_posix(script)

    @staticmethod
    def install(package: MetaPackage) -> None:
        PosixHandler.run(package.install_script)

    @staticmethod
    def check(package: MetaPackage) -> None:
        package.installed = len(shell_wrapper.run_get_posix(package.check_script)) > 0

    @staticmethod
    def check_all(packages: List[MetaPackage]) -> None:
        for package in packages:
            if package.type == MetaPackage.Type.posix:
                PosixHandler.check(package)


class AptHandler:
    type = MetaPackage.Type.apt

    @staticmethod
    def install(package: MetaPackage) -> None:
        script = f"sudo apt --install-suggests install {package.id}"
        if package.install_script:
            script += " && " + package.install_script
        PosixHandler.run(script)

    @staticmethod
    def check(package: MetaPackage) -> None:
        all_packages = [
            a.split()
            for a in shell_wrapper.run_get_posix("dpkg --get-selections").split('\n')
            if len(a)
        ]
        package.installed = any(t[0] == package.id and t[-1] == "install" for t in all_packages)

    @staticmethod
    def check_all(packages: List[MetaPackage]) -> None:
        all_packages = [
            a.split()
            for a in shell_wrapper.run_get_posix("dpkg --get-selections").split('\n')
            if len(a)
        ]
        for package in packages:
            if package.type == MetaPackage.Type.apt:
                package.installed = any(t[0] == package.id and t[-1] == "install" for t in all_packages)


class SnapHandler:
    type = MetaPackage.Type.snap

    @staticmethod
    def install(package: MetaPackage) -> None:
        script = f"snap install {package.id}"
        if package.install_script:
            script += " && " + package.install_script
        PosixHandler.run(script)

    @staticmethod
    def check(package: MetaPackage) -> None:
        ret = shell_wrapper.run_get_posix(f"snap list")
        package.installed = package.id in ret

    @staticmethod
    def check_all(packages: List[MetaPackage]) -> None:
        all_packages = shell_wrapper.run_get_posix("snap list")
        for package in packages:
            if package.type == MetaPackage.Type.snap:
                package.installed = package.id in all_packages


class PowerShellHandler:
    type = MetaPackage.Type.powershell

    @staticmethod
    def run(script: str) -> None:
        commands = [script,
                    "Write-Host ' '",
                    "Write-Host -NoNewLine 'Press any key to continue...'",
                    "$null = $Host.UI.RawUI.ReadKey('NoEcho,IncludeKeyDown')"]
        shell_wrapper.run_interactive_pwsh(";".join(commands))

    @staticmethod
    def install(package: MetaPackage) -> None:
        PowerShellHandler.run(package.install_script)

    @staticmethod
    def check(package: MetaPackage) -> None:
        package.installed = len(shell_wrapper.run_get_pwsh(package.check_script)) > 0

    @staticmethod
    def check_all(packages: List[MetaPackage]) -> None:
        for package in packages:
            if package.type == MetaPackage.Type.powershell:
                PowerShellHandler.check(package)


class WingetHandler:
    type = MetaPackage.Type.winget

    @staticmethod
    def install(package: MetaPackage) -> None:
        script = f"winget install -e --id {package.id}"
        if package.install_script:
            script += "; " + package.install_script
        PowerShellHandler.run(script)

    @staticmethod
    def check(package: MetaPackage) -> None:
        ret = shell_wrapper.run_get_pwsh(f"winget list -q {package.id}")
        package.installed = package.id in ret

    @staticmethod
    def check_all(packages: List[MetaPackage]) -> None:
        all_packages = shell_wrapper.run_get_pwsh("winget list")
        for package in packages:
            if package.type == MetaPackage.Type.winget:
                package.installed = package.id in all_packages


class HandlerWrapper:
    def __init__(self, force: bool = False):
        self.handlers = {}
        if os.name == "posix" or force:
            self.handlers[AptHandler.type] = AptHandler
            self.handlers[SnapHandler.type] = SnapHandler
            self.handlers[PosixHandler.type] = PosixHandler
        if os.name == "nt" or force:
            self.handlers[PowerShellHandler.type] = PowerShellHandler
            self.handlers[WingetHandler.type] = WingetHandler

    def check(self, package: MetaPackage) -> None:
        package.installed = False
        if package.type in self.handlers:
            self.handlers[package.type].check(package)

    def check_all(self, packages: List[MetaPackage]) -> None:
        for handler in self.handlers.values():
            handler.check_all(packages)

    def install(self, package: MetaPackage) -> None:
        if package.type not in self.handlers:
            return
        self.handlers[package.type].install(package)
