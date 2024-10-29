# Puremote

puremote is a remote experiment status monitoring software designed based on RESTFUL API. It was originally designed to provide remote monitoring for the Incage project of PsychoUnity, but due to the use of web technology, it can now be used for various experimental design frameworks, such as: PyshoToolBox, PsychoPy or MonkeyLogic, etc.

## install

### install with uv

```bash
# clone this repo
git clone https://github.com/Ccccraz/puremote.git

cd puremote
```

```bash
# setup env
uv sync

# run app
uv run main
```

### install with conda
```bash
# clone this repo
git clone https://github.com/Ccccraz/puremote.git

cd puremote
```

```bash
# setup env
conda create -n puremote python=3.12
conda activate puremote

# install dependency
pip install .

# run app
python ./src/puremote/__init__.py
```

# Contribution
> *This project is built with PySide6, but it is planned to be refactored with Tauri in the future*