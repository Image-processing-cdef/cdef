import { Client, Storage } from "appwrite";

const client = new Client();

const storage = new Storage(client);

client
    .setEndpoint('https://cloud.appwrite.io/v1') // Your API Endpoint
    .setProject('67176323003bf16cbd3f') // Your project ID
;

const result = storage.getFileDownload('6720d05c00113044676a', '67213398000058c39dd6');

console.log(result); // Resource URL
