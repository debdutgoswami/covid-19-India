[![HitCount](http://hits.dwyl.io/debdutgoswami/covid-india.svg)](http://hits.dwyl.io/debdutgoswami/covid-india)

# COVID-19 India

Python package for providing data for the `COVID-19` cases in India. This can provide data both online as well as offline.

## requirements

For running this, you need to have `python3` installed on your system.

## Features

This works both `online` as well as `offline`.

## Installation

For windows

```
pip install covid-india
```

For linux and Mac

```
pip3 install covid-india
```

## Example

1. All the states

    ```
    from covid_india import states
    print(states.getdata())
    ```

    This returns a `json` object which contains the datas of all the states in India.

2. Specific state

    ```
    from covid_india import states
    print(states.getdata('West Bengal'))
    ```

    This returns a `json` object containing only the datas of West Bengal.

*If you use this package offline, you will get a timestamp along with the data stating when it was last updated.*

# PyPi

COVID 19 INDIA: [PyPi](https://pypi.org/project/covid-india/)



