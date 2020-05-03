# Wheeler's Wort Works
A rebuild of Wheeler's Beer Engine written in Python with continuous updates

## Windows
If you are unsure of your system architecture (64-bit or 32-bit)
#### Using a release build (64-bit only)

First head to the [release page](https://github.com/jimbob88/wheelers-wort-works/releases "Release Files"), and download the latest `exe.win-amd64-3.6.zip`.
Unzip the file with File Explorer and you should have a new folder named `exe.win-amd64-3.6`, on opening this folder you may see another folder named exe.win-amd64-3.6 if so simply open this and continue.

Now simply Double-Click the `main.exe` file - if this fails try opening it again once more. If this fails again post an issue at the [issues page](https://github.com/jimbob88/wheelers-wort-works/issues) or move onto the next area.

#### Running from source (32-bit or 64-bit)

Download the latest addition of Wheeler's Wort Works [here](https://github.com/jimbob88/wheelers-wort-works/archive/master.zip "Latest ZIP File"), then unzip
the `wheelers-wort-works-master.zip` file with File Explorer and you should have a new folder named `wheelers-wort-works-master`, on opening this folder you may see another folder named wheelers-wort-works-master if so simply open this and continue.

If Python isn't installed follow [this handy guide](https://realpython.com/installing-python/ "Real Python Guide to installing Python3") then continue to the next step.

After you have python installed either Double-Click the `main.py` file found in `wheelers-wort-works-master`, if this fails Right-Click and edit with Idle, then press `F5`, you should be greeted by the Beer Engine Screen.

## Linux
#### Ubuntu or Debian
If you're running Ubuntu (or an Ubuntu Variant i.e. Xubuntu, Lubuntu, Kubuntu) or Debian it is recommended to install the  latest _.deb_ file.  Then open a terminal (typically with `Ctrl+Alt+T`).

Download the file, navigate to your download folder typically `~/Downloads/` by running the command `cd ~/Downloads`. Then run the command `sudo apt-get install ./wheelers-wort-works_2.4.2_all.deb`.
If this command fails, attempt to install the file with:
```
sudo apt install ./wheelers-wort-works-ce_0.2_all.deb
```
It is also recommended to run the command `sudo wheelers-wort-works --coreupdate` so as to get the most out of Wheeler's Wort Works - it is recommended to run this command whenever an update is released on Github (Perhaps getting in the habit of updating once or twice per week).
#### Other
Download the latest addition of Wheeler's Wort Works [here](https://github.com/jimbob88/wheelers-wort-works/archive/master.zip "Latest ZIP File"), then unzip
the `wheelers-wort-works-master.zip` file with your Archive Manager of choice and you should have a new folder named `wheelers-wort-works-master`, on opening this folder you may see another folder named wheelers-wort-works-master if so simply open this and continue.

If Python isn't installed follow [this simple guide](https://docs.aws.amazon.com/cli/latest/userguide/install-linux-python.html "Amazon AWS guide") then continue to the next step.

Open a terminal (typically with `Ctrl+Alt+T`), and cd into your `wheelers-wort-works-master` folder, then open with `python main.py`.

## MacOS
I personally do not own a Mac machine so cannot verify this works or build for it - if can make builds for me contact me at _blackburnfjames@gmail.com_.
#### MacOSx
Download the latest addition of Wheeler's Wort Works [here](https://github.com/jimbob88/wheelers-wort-works/archive/master.zip "Latest ZIP File"), then unzip
the `wheelers-wort-works-master.zip` file with your Archive Manager of choice and you should have a new folder named `wheelers-wort-works-master`, on opening this folder you may see another folder named wheelers-wort-works-master if so simply open this and continue.

If Python isn't installed follow [this simple guide](https://docs.python-guide.org/starting/install3/osx/ "OSX Guide") then continue to the next step.

Open a terminal, and cd into your `wheelers-wort-works-master` folder, then open with `python3 main.py` or `python main.py` - python3 is thoroughly recommended over python2 (PIP drops support for python2 January 1st 2020).

## Using Wheeler's Wort Works Command Line Interface
Wheeler's Wort Works now comes built-in with the ability to control certain areas through the command line - things such as mode, the ability to update and the ability to open a `.berf` or `.berfx`.

A general idea of each command is provided with the help command:
```bash
$ wheelers-wort-works -h
usage: main.py [-h] [-f FILE] [-u] [-U] [-l] [-d]

Arguments

optional arguments:
  -h, --help            show this help message and exit
  -f FILE, --file FILE  The file to open `--file file_name.berf[x]` (default:
                        None)
  -u, --update          Using the current `update.py`, download the latest
                        GitHub files (default: False)
  -U, --coreupdate      Pull `update.py` from GitHub, then download the latest
                        GitHub files (default: False)
  -l, --local           Use the local mode (default: False)
  -d, --deb             Use the debian mode (only use on a Debian/Ubuntu
                        system) (default: False)

```

##### `-f FILE, --file FILE`
The file option is used to open Wheeler's Wort Works with a `.berfx` or `.berf`. So the UNIX command `wheelers-wort-works --file No\ Name.berf` opens Wheeler's Wort Works with No Name.berf open.

##### `-u, --update`
This updates your current setup from the master branch on GitHub. It uses your current `update.py` and isn't thoroughly recommended to run unless you are attempting to save data. The following is much more recommended.

##### `-U, --coreupdate`
This is the recommended way to update your install of Wheeler's Wort Works as it pulls the latest update file from GitHub (this means updates should work better and have less chance of breaking) and is used in the following syntax.
**Linux(Ubuntu/Debian)**
```bash
sudo wheelers-wort-works --coreupdate
```
**Source**
```bash
python main.py --coreupdate
```
**NOTE:** `--coreupdate` deprecates `--coreupdate save`

##### `-l, --local`
Use the local directory to place configuration files (e.g. `hop_data.txt`, `grist_data.txt` etc.) and use the local directory for a recipe area.

##### `-d, --deb`
Use `~/.config/Wheelers-Wort-Works` to place configuration files (e.g. `hop_data.txt`, `grist_data.txt` etc.) and use `~/.config/Wheelers-Wort-Works/recipes` for a recipe area.

**NOTE:** Errors will occur if `logo.png` doesn't exist in the following location: `/usr/include/wheelers-wort-works/logo.png` This should ONLY be done when running `--deb`
