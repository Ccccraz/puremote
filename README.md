# Puremote

puremote is a remote experiment status monitoring software designed based on RESTFUL API. It was originally designed to provide remote monitoring for the Incage project of PsychoUnity, but due to the use of web technology, it can now be used for various experimental design frameworks, such as: PyshoToolBox, PsychoPy or MonkeyLogic, etc.

## install

I strongly recommend you to use pipx to install puremote

### install with pipx

```bash
# install
pipx install puremote

# run app
puremote
```

### install with conda

```bash
# create a env
conda create -n puremote python=3.12

# activate env
conda activate puremote

# install uvicorn
pip install puremote

# run app
puremote
```

# Contribution
> *This project is built with PySide6, but it is planned to be refactored with Tauri in the future*