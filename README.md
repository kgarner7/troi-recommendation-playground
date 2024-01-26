# Introduction

This project is part of ListenBrainz' open source music recommendation efforts with an API-first
philiosophy. API-first means that user do no need to download a lot of data before they
can start working with Troi -- all the needed data should ideally live in online APIs, making
it very easy for someone to get started hacking on music recommendations.

## Features

The troi engine features the following concepts:

1. A pipelined architecture for creating playlists from any number of sources.
2. Data sources that fetch data from APIs and feed the data into the troi pipelines.
3. Pipeline elements that are connected together are called Patches. Troi includes a number of built-in patches.
4. The largest patch implements ListenBrainz radio that can generate "radio style" playlists based on one or more
artists, tags, user statistics, user recommendations, LB playlists and MB collections.
5. Generated playlists are output in the JSPF format, the JSON version of XPSF playlists.


## Data-sets

To accomplish this goal, we, the MetaBrainz Foundation, have created and hosted a number of data-sets
that can be accessed as a part of this project. For instance, the more stable APIs are hosted on our
[Labs API page](https://labs.api.listenbrainz.org).

ListenBrainz offers a number of data sets:

1. Collaborative filtered recordings that suggest what recordings a user should listen to based on
their previous listening habits.
2. User statistics that were derived from users recent listening habits.
3. Listening stats that can be used as a measure of popularity.
4. Similarity data for artists and recordings

We will continue to build and host more datasets as time passes. If an API endpoint becomes useful to
a greater number of people we will elevate these API endpoints to officially supported endpoints
that we ensure are up to date on online at all times.

The project is named after [Deanna Troi](https://en.wikipedia.org/wiki/Deanna_Troi).

## DocumentationV

Full documentation for Troi is available at [troi.readthedocs.org](https://troi.readthedocs.org).

## Installation for end users

So far we've not uploaded Troi bundles to PyPi -- please use the installation instructions for developers
below.

## Installation for Development

**Linux and Mac**

```
virtualenv -p python3 .ve
source .ve/bin/activate
pip3 install .[tests]
troi --help
```

**Windows**

```
virtualenv -p python .ve
.ve\Scripts\activate.bat
pip install .[tests]
troi --help
```

## Basic commands

List available patches:

    troi list

Generate a playlist using a patch:

    troi playlist --print [patch-name]

If the patch requires arguments, running it with no arguments will print a usage statement, e.g.

    $ troi playlist --print area-random-recordings
    Usage: area-random-recordings [OPTIONS] AREA START_YEAR END_YEAR
   
      Generate a list of random recordings from a given area.
   
      AREA is a MusicBrainz area from which to choose tracks.
      START_YEAR is the start year.
      END_YEAR is the end year.
   
    Options:
      --help  Show this message and exit.

## Running tests

```
troi test
troi test -v
troi test -v <file to test>
```

## Building Documentation

To build the documentation locally:

    pip install .[docs]
    cd docs
    make clean html
