# Data Engineer Code Challenge


## Provisioning

I cheated and use sqlite 3 for everything. This means that the only thing that need to be install is Python 3 and requests.

To setup create a venv and run:
```
pip3 install -r requirements.txt
python3 setup_db.py
python3 ingest_data.py
```

## Postcodes and distances
To find the two sites furthest apart I use a simple postcode table, taken from here
https://www.doogal.co.uk/ukpostcodes.php.

`setup_db.py` automatically grabs the zip file, unzips it, parses and loads the CSV. The zip
file is about 80MB large, so it will take a little while to download and process.

I use the postcode easting and northing to get an approximate location for each site (within a mile or two),
and then just use 1/2 a pythagoras to calculate distance (I didn't realise the sqlite has practically no maths
functions).

The [OS National Grid](https://en.wikipedia.org/wiki/Ordnance_Survey_National_Grid) is a flat map projection that is valid
other the UK (the reprojection error is tiny compared to error between actual site location and postcode cordinates). 
Because it's flat projection euclidean distance (using easting and northings) is a meaningful measure of distance, unlike 
on a spheric representation (lat/long).

Finally due to the lack of useful math functions in sqlite I don't return true distance, but a number that is quadratically
related to distance. This can be used to sort distances, but I need a sqrt function (which sqlite doesn't have 🤦‍♂️) to
calculate true distance. This would be trivial with Postgres, and even easier using Postgres with PostGIS.
