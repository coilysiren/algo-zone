# algo-zone

pronounced like "auto zone", a place for figuring out algorithms

## Installation Prereqs

- python
- docker

## Usage

Install the required dependencies:

```bash
pip install invoke pyyaml
```

Then run any of the algos:

```bash
invoke test $language $script
invoke test python insertion_sort
invoke test python any # "any" is a wildcard keyword
invoke test rust   selection_sort
```

You will get output like so:

```bash
$ invoke test python any

docker run ...
  ⏱  ./src/python/sort_builtin.py on ./data/sort_input_0.txt ran for 0.5 seconds
  🟢 ./src/python/sort_builtin.py on ./data/sort_input_0.txt succeeded
docker run ...
  ⏱  ./src/python/sort_bubble_sort.py on ./data/sort_input_0.txt ran for 0.51 seconds
  🟢 ./src/python/sort_bubble_sort.py on ./data/sort_input_0.txt succeeded
docker run ...
  ⏱  ./src/python/sort_selection_sort.py on ./data/sort_input_0.txt ran for 0.58 seconds
  🟢 ./src/python/sort_selection_sort.py on ./data/sort_input_0.txt succeeded
docker run ...
  ⏱  ./src/python/sort_insertion_sort.py on ./data/sort_input_0.txt ran for 0.52 seconds
  🟢 ./src/python/sort_insertion_sort.py on ./data/sort_input_0.txt succeeded

✨ script run success ✨
```

_(note: I will likely not bother to update the above example when the output changes in minor ways)_

## New Languages

Adding new languages is a multi-step process, wherein you have to adapt each language to use parent python script's API. Which is to say, `tasks.py` expects every language to operate in roughly the same way, so each language needs modification to give them some uniformity of behavior. algo-zone was implemented in python first, so expect languages to be easier to add the more similar they are to python.

The broad steps to adding a language, are:

- Add it to `config.yml`. The only truly "required" keys are the `dockerImage` and `scriptInvoker`. Everything else is about modifying the languages to behave in a uniform manner. Your new language will likely require its own new special one-off key, like rust needing `useShortScriptName`.
- Create a folder in `src/`. If you're lucky, then you can get away with `src/` only needing the source file. The first source file you will want to add is `sort_builtin`. Every `sort_builtin` file just calls the language's native sorting function. You will also of course want to add any necessary language metadata, like `go.mod` or `Cargo.toml`.
- Handle any special cases. There are always special cases. I can only imagine this repo running out of special cases once it has 10+ languages. Some existing special cases include:

  - Languages that simply do not have a way to say "run this one individual language file inside this folder". `golang` has this. The workaround was to make every file be a "test" file.
  - Compiled languages each require a special something. `rust` specifically requires the target scripts to be mentioned in its manifest file (`Cargo.toml`). This can result in confusion if you add a new algo but forget to add it to the manifest file.

The most important thing to understand is: you need to figure out how to get your language to execute some code in a specific file. It its weird and complicated, when you add your new special case handling code to `tasks.py`. After that, you should be able to do:

```bash
invoke test cobol insertion_sort
```

Which will spin up a docker container for your brand new fancy language. The tests run inside that docker container. That docker container will be expecting a file as output, look at the existing language examples to get an idea of what this means.

Overall you should expect this process to take a few hours. It's hard getting all these languages to play nice with each other!!!
