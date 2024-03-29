#!/bin/python3
import argparse
import subprocess
import os


parser = argparse.ArgumentParser(description='Wrap a notification inside the api gw request and send it')
parser.add_argument('--cpus', default='.25', type=str, help='number of cpus to pass to docker')
parser.add_argument('--out-dir', required=True, type=str, help='output directory')
parser.add_argument('--config-file', default="synthea.properties", type=str, help='output directory')
parser.add_argument('--build-image', default=False, action='store_true', help='Build image, only need to do this once')
parser.add_argument('--num-patients', type=int, help='Total number of patients to generate', default=20)
parser.add_argument('--seed', type=str, help='Seed from which to generate patients', default="21")
parser.add_argument('--state', type=str, help='Patients state', default="Nebraska")
parser.add_argument('--city', type=str, help='Patients city', default="Omaha")
parser.add_argument('--gen-csv', default=False, action='store_true', help='Generate CSVs')
parser.add_argument('--gen-ccda', default=False, action='store_true', help='Generate CCDA')
parser.add_argument('--gen-cpcds', default=False, action='store_true', help='Generate CPCDS')
parser.add_argument('--gen-fhir', default=False, action='store_true', help='Generate FHIR')
parser.add_argument('--gen-fhir-us-core-ig', default=True, action='store_true', help='Generate using FHIR US Core IG')

args = parser.parse_args()
print(args)

out_dir = os.path.abspath(args.out_dir)
config_folder = os.path.abspath("./config")
config_file = args.config_file 

list_files = subprocess.run(["mkdir", out_dir, "-p"])
subprocess.run(["chmod", "o+rw", out_dir])
docker_build = ["docker", "build", "-t", "gen-synthea-data:latest", "."]
if args.build_image is True:
    subprocess.run(docker_build)
docker_run = [
        "docker", "run", "-it", "--rm",
        #"-u $(id -u):$(id -g)",
        "--mount", f'type=bind,source={out_dir},target=/usr/src/synthea/outputdata',
        "--mount", f'type=bind,source={config_folder},target=/syntheaconfig',
        f'--cpus="{args.cpus}"',
        "gen-synthea-data:latest", "./run_synthea",
        "-c", f'/syntheaconfig/{config_file}',
        "-s", f'{args.seed}',
        "-p", f'{args.num_patients} {args.state} {args.city}',
        "--exporter.baseDirectory", "./outputdata/",
        ]
# check for FHIR
docker_run += ["--exporter.fhir.export"]
if args.gen_fhir is True:
    docker_run += ["true"]
else:
    # also turn off contradicting features
    args.gen_fhir_us_core_ig = False
    docker_run += ["false"]

docker_run += ["--exporter.csv.export"]
if args.gen_csv is True:
    docker_run += ["true"]
else:
    docker_run += ["false"]
docker_run += ["--exporter.ccda.export"]
if args.gen_ccda is True:
    docker_run += ["true"]
else:
    docker_run += ["false"]
docker_run += ["--exporter.cpcds.export"]
if args.gen_cpcds is True:
    docker_run += ["true"]
else:
    docker_run += ["false"]
docker_run += ["--exporter.fhir.bulk_data", "true"]
docker_run += ["--exporter.fhir.use_us_core_ig"]
if args.gen_fhir_us_core_ig is True:
    docker_run += ["true"]
else:
    docker_run += ["false"]

print(docker_run)
subprocess.run(" ".join(docker_run), shell=True, check=True)
print(f'You will need to run: `sudo chown $(whoami) {out_dir} -R` to fix permissions')
