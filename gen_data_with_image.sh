#/bin/bash
NUM_PATIENTS=$1
echo generating data for $NUM_PATIENTS number of patients
docker run -it --rm \
  # -u $(id -u):$(id -g) \ # could not figure out how to do this right
  --mount type=bind,source="$(pwd)"/sample_data,target=/usr/src/synthea/outputdata \
  gen-synthea-data:latest \
  ./run_synthea -p $NUM_PATIENTS \
  --exporter.csv.export false \
  --exporter.ccda.export true \
  --exporter.cpcds.export false \
  --exporter.fhir.bulk_data true \
  --exporter.fhir.use_us_core_ig true \
  --exporter.baseDirectory "./outputdata/" \
  --generate.payers.selection_behavior = random \
  --generate.insurance.mandate.year = 2006 \
  --generate.insurance.mandate.occupation = 0.2
echo running sudo chown to $(whoami) so you can edit the files
sudo chown $(whoami) ./sample_data -R
