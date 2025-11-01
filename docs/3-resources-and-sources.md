# Part 1: Using `resources` and `sources` to structure data extraction

In the previous part, we saw a simple example of using `dlt` to load data into a `duckdb` database. While that example was straightforward, we can do better.

## A primer on iterators and generators

An important concept in Python that `dlt` leverages is the idea of iterators and generators. These constructs allow for efficient looping over data without the need to load everything into memory at once.

- An **iterator** is an object that implements the iterator protocol, which consists of the methods `__iter__()` and `__next__()`. An iterator allows you to traverse through all the elements of a collection, such as a list or a set, one at a time.
- A **generator** is a special type of iterator that is defined using a function and the `yield` keyword. Generators allow you to produce a sequence of values over time, rather than computing them all at once and storing them in memory.

Here's a simple example of a generator function that yields numbers from 0 to n-1:

```python
def count_up_to(n):
    count = 0
    while count < n:
        yield count
        count += 1
```

You can use this generator like this:

```python
for number in count_up_to(5):
    print(number)
```

This will output:

```text
0
1
2
3
4
```

Generators are particularly useful when dealing with large datasets or streams of data, as they allow you to process one item at a time without loading everything into memory.

However, Generators can only be iterated once. After they are exhausted, they cannot be reused. If you need to iterate over the data multiple times, you will need to create a new generator instance each time.

```ipython
>>> my_gen_5 = count_up_to(5)

>>> my_gen_5
<generator object count_up_to at 0x71aa29e4bb80>

>>> [num for num in my_gen_5]
[0, 1, 2, 3, 4]

>>> [num for num in my_gen_5]
[]
```

## Rewriting our previous example using a generator

Let's rewrite our previous example using a generator function to produce the data. This will allow us to handle larger datasets more efficiently.

```python linenums="1"
--8<-- "dlt_tutorial/1_sample_pipeline_basic.py:sample_data"
```

We can now pass this generator function to our `dlt` pipeline:

```python linenums="1" hl_lines="10"
--8<-- "dlt_tutorial/1_sample_pipeline_basic.py:pipeline"
```

This time, however, we are printing the result of the `pipeline.run()` method, which returns a `LoadInfo` object containing details about the loading process.

```python linenums="1" hl_lines="10"
--8<-- "dlt_tutorial/1_sample_pipeline_basic.py:load_info"
```

You can run this script in the same way as before

```bash
$ python dlt_tutorial/1_sample_pipeline_basic.py
Running pipeline...
Done
Load info:
Pipeline sample_pipeline load step completed in 0.28 seconds
1 load package(s) were loaded to destination duckdb and into dataset sample_data
The duckdb destination used duckdb:////home/diego/Code/playground/dlt-tutorial/sample_pipeline.duckdb location to store data
Load package 1762003350.048731 is LOADED and contains no failed jobs
```

!!! tip "What is the load info?"

    The load info provides details about the loading process, including the time taken, the number of load packages, and the destination where the data was stored. It also indicates whether there were any failed jobs during the loading process.

!!! tip "Using generators with dlt"

    `dlt` works better if the generator yields dictionaries in batches, see <https://dlthub.com/docs/reference/performance#yield-pages-instead-of-rows>

## Using `resources` and `sources`

- A [resource](https://dlthub.com/docs/general-usage/glossary#resource) is an ([optionally async](https://dlthub.com/docs/reference/performance#parallelism-within-a-pipeline)) function that **yields data**. To create a resource, we add the `@dlt.resource` decorator to that function.
- A [source](https://dlthub.com/docs/general-usage/source) is a function decorated with `@dlt.source` that returns one or more resources.

At its most basic implementation, a `resource` is implemented by decorating our data generator function with `@dlt.resource`:

```python linenums="1" hl_lines="1"
--8<-- "dlt_tutorial/2_sample_pipeline_sources_resources.py:sample_data"
```

A `source` is created by defining a function that returns the resource:

```python linenums="1" hl_lines="1 3"
--8<-- "dlt_tutorial/2_sample_pipeline_sources_resources.py:sample_source"
```

We can then use this source in our pipeline:

```python linenums="1" hl_lines="8"
--8<-- "dlt_tutorial/2_sample_pipeline_sources_resources.py:pipeline"
```

## What changed?

`dlt` automatically generates configuration **specs** for functions decorated with `@dlt.source`, `@dlt.resource`, and `@dlt.destination`

For example, it allows now for **[injecting configuration values](https://dlthub.com/docs/general-usage/credentials/setup)**

## Injecting configuration values

We can modify our source function to accept a configuration parameter:

```python linenums="1" hl_lines="2"
--8<-- "dlt_tutorial/2b_sample_pipeline_sources_resources_with_config.py:sample_source"
```

This parameter can now be set using environment variables, configuration files, or command-line arguments when running the pipeline.

```bash
$ MY_CUSTOM_PARAMETER="pythonchile" python dlt_tutorial/2b_sample_pipeline_sources_resources_with_config.py
Custom parameter value: pythonchile
Running pipeline...
Done
...
```

Alternatively, we can set the parameter in a configuration file located at `.dlt/config.toml`:

```toml
[sample_pipeline]
my_custom_parameter = "baz"
```

Running the pipeline now will use the value from the configuration file:

```bash
$ python dlt_tutorial/2b_sample_pipeline_sources_resources_with_config.py
Custom parameter value: baz
Running pipeline...
Done
...
```

!!! tip "dlt searches for values in multiple places in an specific order"

    See <https://dlthub.com/docs/general-usage/credentials/setup#how-dlt-looks-for-values> for more information on how `dlt` searches for configuration values.

## Wrapping up

In this part, we learned about iterators and generators in Python, and how they can be used to efficiently handle data in `dlt` pipelines. We also introduced the concepts of `resources` and `sources`, which help structure data extraction in a more modular way.

In the next part, we will change to a postgres destination and see how to handle more complex loading patterns.
