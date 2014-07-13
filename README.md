py3_fn_pipeline
===============

An experiment to implement shell pipes like processing in python.
Requires python3 for the way it uses exceptions


###Example:
cat pipes3.py | wc -w can be written as:

word_count = Pipeline(read_file).chain(count_words).apply('./pipes3.py')


print(word_count)


where read_file is a function that takes a file path name as param and returns a string

count_words takes a string as input and returns the number of words it contains
