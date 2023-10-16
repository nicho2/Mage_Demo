# Mage Demo

This example tutorial shows you how to build an anomaly detection pipeline with Mage and InfluxDB. 

To view your Mage pipeline navigate to `localhost:6789`

This demo assumes you're using InfluxDB Cloud. 

## Generated Data 
This demo generates machine data (load, vibration, power, and temperature) for three machines (machine1, machine2, and machine3). To create anomalies, navigate to `localhost:5005` and click on a machine to toggle the anomaly creation. 

## Setup
Please make sure you have the following prerequisites before you begin:
- [Docker](https://docs.docker.com/get-docker/)
- [InfluxDB IOx](https://github.com/InfluxCommunity/InfluxDB-IOx-Quick-Starts#influxdb-iox)
- [Env file](https://github.com/InfluxCommunity/InfluxDB-IOx-Quick-Starts#env-file)

### InfluxCloud v3
To get started, you will need to create an InfluxDB IOx account. If you don't already have an account, you can sign up for free [here](https://cloud2.influxdata.com/signup). Once you have an account, you can create a new organization and bucket to store your data. You can find instructions on how to do this [here](https://docs.influxdata.com/influxdb/cloud/organizations/buckets/create-bucket/). Name your bucket `factory`.

### Env file
To connect Grafana to InfluxDB IOx, you will need to create an env file. With the top directory create a file called `.env`:
```bash
touch .env
```
This file will contain the following information:
```
export INFLUX_HOST=
export INFLUX_TOKEN=
export INFLUX_ORG=
export INFLUX_DATABASE= 
export MAGE_SLACK_WEBHOOK_URL=https://hooks.slack.com/services/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 
export MAGE_PROJECT_NAME=influx-magic
export MAGE_ENV=dev
```
**Note: make sure to specify your `INFLUX_HOST` without the protocal like so: `us-east-1-1.aws.cloud2.influxdata.com`**

**Additional Note: This webhook is for the InfluxData Slack. All notifications will land in the #notifications-testing channel there.**

## Run
To run, make sure to first source the env file:
```bash
source .env
```
Navigate to the quick start you would like to run and run the following command:
```bash
docker compose build
docker compose up -d magic
```

