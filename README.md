py3_fn_pipeline
===============

An experiment to implement shell pipes like processing in python.
Requires python3 for the the way uses excetions


###Example
cat pipes3.py | wc -w can be written as:

word_count = Pipeline(read_file).chain(count_words).apply('./pipes3.py')


print(word_count)


