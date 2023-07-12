#!/bin/bash

# Run influx bucket list and parse the output
influx bucket list | awk '
BEGIN {
    # Skip the header line
    getline
}
{
    # Extract the values
    bucket_id = $1
    database_name = $2

    # Construct and run the influx v1 dbrp create command
    cmd = "influx v1 dbrp create --db " database_name " --rp " database_name " --bucket-id " bucket_id " --default"
    system(cmd)
}'