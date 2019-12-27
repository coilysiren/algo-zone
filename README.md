# algo-zone

pronounced like "Auto Zone", a place for lynn to learn to software engineering

## Usage

Ensure that you have a working installation of every language [you see here](https://github.com/lynncyrin/algo-zone/tree/master/src), and then run

```
# in bash
./scripts/watch_tests.sh
```

## APIs

The repo is used like so:

- humans run => the _"test watcher script"_ which runs => the _"test manager script"_ which runs => the _"sort script"_
- github actions runs => the _"test manager script"_ which runs => the _"sort script"_

### test watcher script

watches your local directory for changes, and runs the tests in every language if changes are detected

#### usage / inputs:

```
./scripts/watch_tests.sh
```

### test manager script

given a language, runs each of that language's scripts on every input

#### usage / inputs:

```
./scripts/run_tests.sh $language
```

#### outputs:

- exit 0 if everything succeeds
- exit 1 if there is any failure in any test script

### sort script

given the name of randomized file and the name of a sorted file, sorts the randomized file in memory and compares that result against the sorted file

#### usage / inputs:

```
./src/$language/sort_$sortName $randomizedFile $sortedFile
```

#### outputs:

- exit 0 if sorted $randomizedFile is the same as $sortedFile
- exit 1 otherwise

#### ⚠️ gotchas ⚠️:

You should have at least 10x the RAM of the size of the largest file in `data/`. If you have less than that, your computer will OOM probably. _(TODO: very this, for entertainment purposes)_

## credits

First names from here => https://github.com/dominictarr/random-name/blob/master/first-names.txt
