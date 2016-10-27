# lixdc
User interface for data collection at LIX beam line.


## lixdc configuration

Lixdc requires the following configuration information:

```
amostra_host: localhost
amostra_port: 7772
base_path: /Users/hugoslepicka/data
```


This configuration information can live in up to four different places, as
defined in the docstring of the `load_configuration` function in
 `lixdc/conf.py`. In order of increasing precedence:

1. The conda environment
  - CONDA_ENV/etc/{name}.yaml (if CONDA_ETC_env is defined)
1. At the system level
  - /etc/{name}.yml
1. In the user's home directory
  - ~/.config/{name}/connection.yml
1. Environmental variables
  - {PREFIX}_{FIELD}

where

  - {name} is lixdc
  - {PREFIX} is LIXDC and {FIELD} is one of {amostra_host, amostra_port, base_path}
