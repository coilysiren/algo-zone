# algo-zone

pronounced like "auto zone", a place for figuring out algorithms

## Installation requirements

- python
- pipenv
- docker

## Usage

Run this once

```bash
pipenv sync
```

Then run any of these

```bash
# example CLI calls, run with as many args so you want
pipenv run tests
pipenv run tests $language $script $data
pipenv run tests python
pipenv run tests python insertion_sort
pipenv run tests python insertion_sort first_names
# "any" is a wildcard keyword
pipenv run tests python any first_names
```
