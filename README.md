<h1>
  <div style="display: inline-block">
    <span>
      <img src="resources/UniversityLogo%20RGB_block_n_blue.png?raw=true" width="100" height="100" alt="UNR">
    </span>
    <div align="center">
      <span>CS-457 Database Management Systems</span>
    </div>
  </div>
</h1>
<span>
  <img src="https://github.com/Stehfyn/cs457/actions/workflows/release.yml/badge.svg" alt="Release">
</span>

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
