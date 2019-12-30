# algo-zone

pronounced like "auto zone", a place for figuring out algorithms

## Usage

Ensure that you have a working installation of every language [you see here](https://github.com/lynncyrin/algo-zone/tree/master/src), and then run

```
# in bash
./scripts/watch_tests.sh
```

## APIs

The repo is used like so:

- humans run => the _"test watcher script"_ which runs => the _"test manager script"_ which runs => the _"sort script"_
- GitHub actions runs => the _"test manager script"_ which runs => the _"sort script"_

### **test watcher script**

🚧 this script hasn't been created yet 🚧

watches your local directory for changes, and runs the tests in every language if changes are detected

#### ⚙️ usage

```
./scripts/watch_tests.sh
```

### **test manager script**

given a language, runs each of that language's scripts on every input

#### ⚙️ usage

```
./scripts/run_tests.sh $language
```

#### 📥 inputs

- arg 1 - $language, the language to run tests for (optional, default to python)

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
