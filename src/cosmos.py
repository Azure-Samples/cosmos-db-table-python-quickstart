# <imports>
from azure.identity import DefaultAzureCredential
from azure.data.tables import TableServiceClient

# </imports>

import json


def runDemo(endpoint, table_name, writeOutput):
    # <create_client>
    # Retrieves an Azure Storage token instead of Azure Cosmos DB for Table
    credential = DefaultAzureCredential()

    client = TableServiceClient(endpoint, credential=credential)

    table = client.get_table_client(table_name)
    # </create_client>
    writeOutput(f"Get table:\t{table.table_name}")

    # <create_entity>
    new_entity = {
        "RowKey": "70b63682-b93a-4c77-aad2-65501347265f",
        "PartitionKey": "gear-surf-surfboards",
        "Name": "Yamba Surfboard",
        "Quantity": 12,
        "Sale": False,
    }
    created_entity = table.upsert_entity(new_entity)
    # </create_entity>
    writeOutput(f"Upserted entity:\t{created_entity}")

    new_entity = {
        "RowKey": "25a68543-b90c-439d-8332-7ef41e06a0e0",
        "PartitionKey": "gear-surf-surfboards",
        "Name": "Kiama Classic Surfboard",
        "Quantity": 4,
        "Sale": True,
    }
    created_entity = table.upsert_entity(new_entity)
    writeOutput(f"Upserted entity:\t{created_entity}")

    # <read_item>
    existing_item = table.get_entity(
        row_key="70b63682-b93a-4c77-aad2-65501347265f",
        partition_key="gear-surf-surfboards",
    )
    # </read_item>
    writeOutput(f"Read entity id:\t{existing_item.row_key}")
    writeOutput(f"Read entity:\t{existing_item}")

    # <query_items>
    category = "gear-surf-surfboards"
    filter = f"PartitionKey eq '{category}'"
    entities = table.query_entities(query_filter=filter)
    # </query_items>
    # <parse_results>
    output = json.dumps(entities, indent=True)
    # </parse_results>
    writeOutput("Found entities:")
    writeOutput(output, isCode=True)
