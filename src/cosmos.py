from dotenv import load_dotenv

from azure.data.tables import TableServiceClient
from azure.identity import DefaultAzureCredential

import json
import os

def getLastRequestCharge(c):
    return c.client_connection.last_response_headers["x-ms-request-charge"]


def runDemo(writeOutput):
    load_dotenv()

    # <create_client>
    endpoint = os.getenv("CONFIGURATION__AZURECOSMOSDB__ENDPOINT")
    if not endpoint:
        raise EnvironmentError("Azure Cosmos DB for Table account endpoint not set.")

    credential = DefaultAzureCredential()

    client = TableServiceClient(endpoint=endpoint, credential=credential)
    # </create_client>

    tableName = os.getenv("CONFIGURATION__AZURECOSMOSDB__TABLENAME", "cosmicworks-products")
    table = client.get_table_client(tableName)

    writeOutput(f"Get table:\t{table.table_name}")

    new_entity = {
        "RowKey": "aaaaaaaa-0000-1111-2222-bbbbbbbbbbbb",
        "PartitionKey": "gear-surf-surfboards",
        "Name": "Yamba Surfboard",
        "Quantity": 12,
        "Sale": False,
    }
    created_entity = table.upsert_entity(new_entity)

    writeOutput(f"Upserted entity:\t{created_entity}")

    new_entity = {
        "RowKey": "bbbbbbbb-1111-2222-3333-cccccccccccc",
        "PartitionKey": "gear-surf-surfboards",
        "Name": "Kiama Classic Surfboard",
        "Quantity": 4,
        "Sale": True,
    }
    created_entity = table.upsert_entity(new_entity)
    writeOutput(f"Upserted entity:\t{created_entity}")

    existing_entity = table.get_entity(
        row_key="aaaaaaaa-0000-1111-2222-bbbbbbbbbbbb",
        partition_key="gear-surf-surfboards",
    )

    writeOutput(f"Read entity id:\t{existing_entity['RowKey']}")
    writeOutput(f"Read entity:\t{existing_entity}")

    category = "gear-surf-surfboards"
    filter = f"PartitionKey eq '{category}'"
    entities = table.query_entities(query_filter=filter)

    result = []
    for entity in entities:
        result.append(entity)

    output = json.dumps(result, indent=True)

    writeOutput("Found entities:")
    writeOutput(output, isCode=True)
