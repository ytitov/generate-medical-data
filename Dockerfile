FROM openjdk:11
WORKDIR /usr/src/synthea
RUN git clone https://github.com/synthetichealth/synthea.git .
RUN ./run_synthea -p 10 \
	--exporter.csv.export true \
	--exporter.ccda.export true \
	--exporter.cpcds.export true \
	--exporter.fhir.bulk_data true \
  --exporter.fhir.use_us_core_ig true \
  --exporter.baseDirectory "./output/"
