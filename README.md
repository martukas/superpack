# SuperPack 

Think of this as a self-curated multi-platform Ninite for both Windows and Linux. if you find yourself performing a lot of boilerplate installs on every new system, this, in conjunction with something like [dotbot](https://github.com/anishathalye/dotbot/) might be the right solution for you. 

---

## Motivation

This solves my particular use case:
* installing same or similar sets of programs on fresh machines
* dealing with different package managers, such as `apt`, `snap`, `winget`, with subtly different syntax, and not caring to remember which package resides where
* the need to build and install from source, with custom scripts rather than using an existing package manager
* something like Ninite seems outdated and does not provide some programs I need
* I need to do this in both Linux and Windows
* I sometimes need to do this in CLI only, e.g. on a remote machine, without a window manager
* I want to curate my own list of programs I will likely need, and keep them categorized in my own way

## Limitations

It does NOT in any way adapt packages from one OS to another. 

It does NOT provide any all-encompassing repository nor does it search the wrapped repositories for existing packages.  It's your responsibility to find the packages you need and describe them in your own manifest.

Currently, this utility is only adapted for and tested on:
* Ubuntu
* Windows 10 with PowerShell7

The architecture should be flexible enough to add handlers for other systems and package managers with minimal modification.

### Windows

Additional caveats for Windows systems. 

You will need to:
* Run `Set-ExecutionPolicy RemoteSigned` to allow the running of `ps1` scripts
* Install most recent PowerShell with `winget install -e --id Microsoft.PowerShell`


## Running

You may test it out with the minimal example manifests included in this repo.

**In Ubuntu**
```shell
pipenv run python ./superpack/superpack.py ./examples/ubuntu.json
```

**In Windows 10**
```powershell
pipenv run python ./superpack/superpack.py .\examples\packages.json
```

If you try to run this from something like ConEmu, the UI library may not render correctly, so it's recommended you run it from a vanilla `pwsh` terminal. If you need to integrate this command into some install script that you might run from funky places, you can always force the creation of a new terminal with the following:
```powershell
Start-Process pwsh -WindowStyle Maximized -ArgumentList "-Command & {pipenv run python ./superpack/superpack.py .\examples\packages.json}"
```

### Options

In addition to the manifest path, you may also add the following keywords for special debug behavior:
* `read` - will only read the manifest and quit immediately, just to test that it parses right
* `-f` - will force the HandlerWrapper to load all package handlers, including ones not compatible with the detected OS
* `check` - will load the manifest and check for the installation status of all packages and then quit immediately, without running the UI

## Package definitions

You should create a JSON file with some package definitions like the ones found in the [examples](examples) directory. For example, a package definition looks like:

```json
{
    "id": "dummy",
    "descr": "Dummy test package",
    "category": "xtras",
    "type": "posix",
    "check": "which nonexistentscript",
    "install": "./examples/custom.sh test"
}
```

### id

The identifier should be unique, and in case of packages that are wrappers/references to other package management systems, this "id" should be the actual package name. This will save you the time and effort of having to define "check" and "install" commands, as those will be generated for you.

### descr

Description field. Make this informative and useful.

### category

Category for sorting the packages into tabs in the UI. Watch out for escape characters that may trip up the UI library.

### type
This should be one of the valid `MetaPackage.Type` Enum values, which at this time is one of:
* posix
* powershell
* apt
* snap
* winget

For the 2 shell types -- `posix` and `powershell` -- the values of "check" and "install" will be used as commands with an invocation of the appropriate shell. Avoid multi-line commands. Instead, create a custom shell script, like the ones you see under [examples](examples).

For the wrapped package managers, i.e. `apt`, `snap` and `winget`, you the `id` field will be used with boilerplate check and installation commands. If there are additional steps on top of the expected standard installation method, you may also provide an additional script to run in "install", which the particular handler will run afterward. Otherwise, "install" may be left empty.

### check

This will only be run for `posix` and `powershell` packages. As such, it is of use for custom packages of your own design. This script answers whether the said package has been installed. This could be a check for the presence of an executable, or anything that you consider good evidence.
* If the package is PRESENT, the script should return a NON-EMPTY string
* if the package is NOT present, it should return an EMPTY string.

### install

If non-empty, commands in this field will be run when attempting to install the package. This script will always be run for `posix` and `powershell` types. For types referencing existing package management systems, this script will be delegated to the "parent" shell system, i.e.
* apt -> posix
* snap -> posix
* winget -> powershell


## Implementation

I am using mostly [textual](https://github.com/textualize/textual/) for the TUI, and a bit of [rich](https://github.com/Textualize/rich) for some debug output.

## Roadmap

Here are some features/ideas I would like to implement if I ever get around to it:
* Add scroll bars to pages
* make uninstall/remove possible
* install multiple packages at once, after marking them as targets in UI
* one package definition can reference multiple alternative managers, so that e.g. one manifest can be kept for all possible systems
* define packages in yml instead of json? 
* Function to update/upgrade some or all packages
* Support for macOS
* Support for other Linux distros

Help is welcome.
