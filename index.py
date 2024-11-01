from appwrite.client import Client
from appwrite.services.storage import Storage
from appwrite.exception import AppwriteException
from appwrite.id import ID # Corrected import statement

# Initialize the Appwrite client
client = Client()

# Set up client with your Appwrite project details
(client
    .set_endpoint('https://cloud.appwrite.io/v1')  # Your Appwrite endpoint
    .set_project('67176323003bf16cbd3f')       # Your project ID
    .set_key('standard_27d81950ea80941e3161da22e8b4b66fd794d919dfe962a75894d05e2e05fe4338b56652d503ec5caa6dfd7e99ffcd55051b33a34be9ee1c90f6b5d6c5f1e5cb040e9fe3e5817eb9dd83afa8d00f89f55f3c6a6e667cb3c0ef3a78f642a96c42265d36ee5118f6069fcf0dccfa02ecea0c5a7780cf20b35aa0cd65983183cdc3')              # Your API key
)

# Initialize Storage service
storage = Storage(client)

# Create a new bucket
try:
    bucket = storage.create_bucket(
        bucket_id=ID.unique(),    # Unique bucket ID, or 'unique()' to auto-generate
        name='img',            # Bucket name

    )
    print(f'Bucket created: {bucket}')
except AppwriteException as e:
    print(f'Error: {e}')
