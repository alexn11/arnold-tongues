# run the prog

```
python tongues3.py conf/tent.json
```

## config

- the entry `config["images"]["period_colours"]` can be the name of a matplotlib colour map such as:
    - viridis
    - plasma
    - inferno
    - magma
    - cividis

# running the tests

in root dir:
```bash
export PYTHONPATH=`pwd`
pytest
```