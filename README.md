# installation

- requires at least Python version 3.10
- run:
```bash
pip install -r requirements.txt
```

# web interface

![how the web interface should look like](app-sample "the web interface (example)")

launch the web interface with (from the root folder):
```bash
flask run
```
then open the url shown on the terminal (probably [http://127.0.0.1:5000](http://127.0.0.1:5000))


# CLI program

run by passing the name of the config file as an argument:
```
python tongues3.py conf/tent.json
```

## config file

- the entry `config["images"]["period_colours"]` can be the name of a matplotlib colour map such as:
    - viridis
    - plasma
    - inferno
    - magma
    - cividis


# testing

in the root folder, run:
```bash
pytest
```
(if necessary do a `export PYTHONPATH='pwd'` beforehand)
