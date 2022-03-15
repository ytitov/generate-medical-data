# Synthetic data generation
- uses synthea project to generate source data: `git clone https://github.com/synthetichealth/synthea.git`
- easiest thing to do is to use the supplied python script to generate the data: `./generate-patients.py`
    example: `./generate-patients.py --num-patients 20 --out-dir ./test --build-image`

# Generate fhir r4, ccda, csv, cpcds data
If you are interested in how the data is generated, read through this section.  For a more comprehensive guide please visit the original repository mentioned above.
## 1. ensure you build the docker image
The image built will pull the most recent codebase.  The repo is actively maintained and evolving.  See instructions under Docker section.
## 2. run the program and populate output table
```base
./run_synthea -p 10 \
	--exporter.csv.export true \
	--exporter.ccda.export true \
	--exporter.cpcds.export true \
	--exporter.fhir.bulk_data true \
	--exporter.fhir.use_us_core_ig true \
	--exporter.baseDirectory "./output/"
  --generate.payers.selection_behavior = random \
  --generate.insurance.mandate.year = 2006 \
  --generate.insurance.mandate.occupation = 0.2
```
Note that generating payers doesn't work.  Have not had time to look this up, but it would be very useful.

## 3. copy to S3 if desired
`aws s3 cp ./output-data s3://kpi-datapipeline/synthea/10000 --recursive`

# Generate FHIR R4 data
## example
- generate for 10 patients
- bulk data option is for ndjson
- `exporter.fhir.use_us_core_ig true`
	- generate a population that exports FHIR according to the US Core R4 Implementation Guide profiles.
```bash
./run_synthea -p 10 \
	--exporter.fhir.bulk_data true \
	--exporter.fhir.use_us_core_ig true \
	--exporter.baseDirectory "./fhirbulkdata/"
```
## notable options
- `exporter.fhir.transaction_bundle = true`
	- generate transaction bundles
- `exporter.hospital.fhir.export = true`
	- Exporting Hospital Provider data in separate file.
	- seems to export less resources

# Generate CSV data
The data generated is good for testing against custom schemas that we have to deal with pretty regularly.  Look [here](https://github.com/synthetichealth/synthea/wiki/CSV-File-Data-Dictionary) for the schema documentaion.
```base
./run_synthea -p 10 \
	--exporter.csv.export true \
  --exporter.baseDirectory "./output-csv/"
```

# Docker
if you want to generate your own dataset for local usage, I have included a Dockerfile.  The build takes a bit, and also runs a small export, so the build is saved in order to make subsequent runs much quicker.

- `docker build -t gen-synthea-data:latest .` to generate the image
- use the `./gen_data_with_image.sh` bash script with a parameter to generate how many ever patients you want: `./gen_data_with_image.sh 20` to generate 20 patients
- Otherwise you can run your own commands:
```
docker run -it --rm \
	--mount type=bind,source="$(pwd)"/sample_data,target=/usr/src/synthea/outputdata \
  gen-synthea-data \
	./run_synthea -p 10 \
		--exporter.csv.export true \
		--exporter.baseDirectory "./outputdata/"
```
- if you want to play around inside the environment you can create and enter the container: `docker run -it --rm gen-synthea-data /bin/bash`
