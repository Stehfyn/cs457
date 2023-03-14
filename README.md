![Tests](https://github.com/Stehfyn/cs457/actions/workflows/release.yml/badge.svg)

## Requirements
- [Python 3.9+](https://www.python.org/downloads/release/python-390/)

## Install

First, clone the repository and cd into `cs457`:
```
git clone https://github.com/stehfyn/cs457.git && cd cs457
```

Then, we run `bootstrap.py` to ensure pip, install virtualenv if necessary, and setup the virtualenv:

```
<python> ./scripts/bootstrap.py
```

Next, we activate `virtualenv` depending on system:

```
./venv/Scripts/activate.bat
or
./venv/Scripts/activate
```

Finally, one can run:
```
<python> ./src/main.py gui
```
and should see:

![](common/gui.png?raw=true)
