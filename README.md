# algo-zone

pronounced like "auto zone", a place for figuring out algorithms

## Installation requirements

- python
- pipenv (from python)
- rust

## Usage

```
pipenv sync && pipenv run tests
```

## Interface docs

### **test manager script**

given a language, runs each of that language's scripts on every input

#### ⚙️ usage

```
./scripts/run_tests.sh $language
```

#### 📥 inputs

- arg 1 - $language, the language to run tests for (optional, defaults to python)

#### 🚚 outputs

- exit 0 if everything succeeds
- exit 1 if there is any failure in any test script

### **sort scripts**

given the name of randomized file and the name of a sorted file, sorts the randomized file in memory and compares that result against the sorted file

#### 📥 inputs

- arg 1 - the path to a randomized file
- arg 2 - the path to write the script output file

## credits

First names from here => https://github.com/dominictarr/random-name/blob/master/first-names.txt
