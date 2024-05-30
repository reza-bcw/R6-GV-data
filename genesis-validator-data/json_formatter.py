import json
import os

# Set the value for the BondedStake variable
BONDED_STAKE_VARIABLE = 2

# Get the current directory
current_directory = os.getcwd()

# List all files in the current directory
all_files = os.listdir(current_directory)

# Exclude template.json from the list of files
all_files = [file for file in all_files if file != "template.json"]

# Filter the remaining list to include only JSON files
json_files = [file for file in all_files if file.endswith('.json')]

combined_data = []

for file_path in json_files:
    with open(file_path, 'r') as file:
        data = json.load(file)
        
        for entry in data.get("genesisValidatorData", []):
            filtered_entry = {key: value for key, value in entry.items() if key not in ["validatorAddress", "ownershipProof"]}
            if filtered_entry:  # Only append non-empty dictionaries
                formatted_entry = {
                    "Treasury": f'common.HexToAddress("{filtered_entry.get("treasury")}")',
                    "OracleAddress": f'common.HexToAddress("{filtered_entry.get("oracleAddress")}")',
                    "ConsensusKey": f'common.Hex2Bytes("{filtered_entry.get("consensusKey")}")',
                    "Enode": f'"{filtered_entry.get("enode")}"',
                    "BondedStake": f'Ntn{BONDED_STAKE_VARIABLE}'
                }
                combined_data.append(formatted_entry)

# Write the combined data to a new JSON file
with open('combined.json', 'w') as outfile:
    outfile.write("[\n")
    for i, entry in enumerate(combined_data):
        outfile.write("    {\n")
        outfile.write(f'        "Treasury": {entry["Treasury"]},\n')
        outfile.write(f'        "OracleAddress": {entry["OracleAddress"]},\n')
        outfile.write(f'        "ConsensusKey": {entry["ConsensusKey"]},\n')
        outfile.write(f'        "Enode": {entry["Enode"]},\n')
        outfile.write(f'        "BondedStake": {entry["BondedStake"]}\n')
        if i < len(combined_data) - 1:
            outfile.write("    },\n")
        else:
            outfile.write("    }\n")
    outfile.write("]\n")

print("Combined JSON data saved to 'combined.json'.")
