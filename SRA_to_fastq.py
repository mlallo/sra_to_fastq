import subprocess
import os

#Directories for SRA and FASTQ files
sra_download_directory = "/gpfs/home/ml9675/becklab_ML/projects/mds/data/input/20241023mds_bulkrnaseq_SRA"
fastq_output_directory = "/gpfs/home/ml9675/becklab_ML/projects/mds/data/output/20241023mds_bulkrnaseq_fastq"

os.makedirs(sra_download_directory, exist_ok=True)
os.makedirs(fastq_output_directory, exist_ok=True)

#Path to the SRR accession list file
srr_acc_list_path = "/SRR_Acc_List.txt"

#Load SRR IDs from the file
def load_srr_ids(file_path):
    with open(file_path, 'r') as file:
        srr_ids = [line.strip() for line in file if line.strip()]
    return srr_ids

#Function to download SRA files and convert to FASTQ
def download_and_convert_sra_to_fastq(srr_ids):
    for sra_id in srr_ids:
        print(f"Currently downloading: {sra_id}")
        
        #Specify the exact output path for the SRA file
        sra_file_path = os.path.join(sra_download_directory, f"{sra_id}.sra")
        prefetch_cmd = f"prefetch {sra_id} --output-file {sra_file_path}"
        print(f"Running command: {prefetch_cmd}")
        
        try:
            result = subprocess.run(prefetch_cmd, shell=True, check=True, capture_output=True, text=True)
            print(result.stdout)
            print(f"Downloaded {sra_id} successfully.")
        except subprocess.CalledProcessError as e:
            print(f"Error downloading {sra_id}: {e.stderr}")
            continue

        #Confirm that the file exists before trying to convert
        if not os.path.isfile(sra_file_path):
            print(f"File {sra_file_path} not found after download, skipping conversion.")
            continue

        #Convert to FASTQ using fastq-dump
        fastq_dump_cmd = f"fastq-dump --gzip --skip-technical --readids --read-filter pass --dumpbase --split-3 --outdir {fastq_output_directory} {sra_file_path}"
        print(f"Running command: {fastq_dump_cmd}")
        
        try:
            result = subprocess.run(fastq_dump_cmd, shell=True, check=True, capture_output=True, text=True)
            print(result.stdout)
            print(f"Converted {sra_id} to FASTQ successfully.")
        except subprocess.CalledProcessError as e:
            print(f"Error converting {sra_id} to FASTQ: {e.stderr}")

#Execute
srr_ids = load_srr_ids(srr_acc_list_path)
if srr_ids:
    print(f"Found {len(srr_ids)} SRR IDs.")
    download_and_convert_sra_to_fastq(srr_ids)
else:
    print("No valid SRR IDs found.")

print('SRA Download Complete!')
