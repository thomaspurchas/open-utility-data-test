# Data Engineer Code Challenge

## The Tasks

Please read all parts before starting on the tasks.

In the data folder of this repository are a few csv files containing data about
fictional sites containing generators and consumers of electricity. Consumers
(import sites) are in the files named 'import-YYYYMMDD.csv' and generators
(export sites) are in the files named 'export-YYYYMMDD.csv' Where YYYYMMDD
gives the date of the file.

### Task 1

Write a script which can be run once to load the data into a database of your
choosing. You must do this in the date order of the files. Assume that the
information could be updated in the future with e.g. new contract dates,
updated Organisation name. For example if we have a new file with an updated
organisation name, the organisation name should be updated in the database.


### Task 2

From this database, write queries for the following:

1) The total number of meters (meter IDs) we have
2) The total number of hydro generator sites
3) The average installed capacity of solar generator sites
4) A list of the different generation types
5) A list of distinct organisations by their names and IDs.
6) All sites that will be out of contract by the 1st February 2018.
7) The total monthly estimated volumes of all import sites that are farms
8) (optional) The distance between the furthest generator and consumer


### Task 3 (bonus)

Write scripts to return the results of the queries above. You can choose to
have separate scripts for the tasks or have one script with multiple arguments.
Output the answers in whichever way you see fit (print to stdout, csv, json)
but please document how to run this.


## Provisioning

Picking the database is up to you, to allow you to use whatever tools you are
familiar with. However, we need to be able to run it to test the code once
submitted, so if installing the database (and other tools) requires something
more than an `apt get` or `pip install` please leave instructions on how we
should do this.

The easiest method for this would be a vagrantfile to provision your
environment (at least a pip requirements file would be good).
