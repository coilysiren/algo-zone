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
pipenv run tests $language $script_name $data
pipenv run tests python
pipenv run tests python sort_insertion_sort
pipenv run tests python sort_insertion_sort first_names_shortened
```
