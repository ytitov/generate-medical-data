#/bin/bash
NUM_PATIENTS=$1
echo generating data for $NUM_PATIENTS number of patients
docker run -it --rm \
	--mount type=bind,source="$(pwd)"/sample_data,target=/usr/src/synthea/outputdata \
  gen-synthea-data:latest \
	./run_synthea -p $NUM_PATIENTS \
		--exporter.csv.export false \
		--exporter.ccda.export true \
		--exporter.cpcds.export false \
		--exporter.fhir.bulk_data true \
	  --exporter.fhir.use_us_core_ig true \
  	--exporter.baseDirectory "./outputdata/"
echo running sudo chown to $(whoami) so you can edit the files
sudo chown $(whoami) ./sample_data -R
