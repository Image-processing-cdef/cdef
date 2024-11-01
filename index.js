// import { Client, Storage,ID } from "appwrite";

// const client = new Client()
//     .setEndpoint('https://cloud.appwrite.io/v1')
//     .setProject('67176323003bf16cbd3f');

// const storage = new Storage(client);

// const promise = storage.createFile(
//     '6720d05c00113044676a',
//     ID.unique(),
//     document.getElementById('uploader').files[0]
// );

// promise.then(function (response) {
//     console.log(response); // Success
// }, function (error) {
//     console.log(error); // Failure
// });
import { Client, Storage, ID } from 'appwrite';
import fs from 'fs';

const client = new Client();
client
    .setEndpoint('https://cloud.appwrite.io/v1') // Your Appwrite endpoint
    .setProject('67176323003bf16cbd3f'); // Your Appwrite project ID

const storage = new Storage(client);

// Example function to upload a file
async function uploadFile(filePath) {
    try {
        const fileBuffer = fs.readFileSync(filePath); // Read the file from disk
        const result = await storage.createFile(
            '6720d05c00113044676a',  // Bucket ID
            ID.unique(),         // Generate a unique ID for the file
            new File([fileBuffer], "uploadedFileName")  // Wrap in a File object
        );
        console.log("File uploaded successfully:", result);
    } catch (error) {
        console.error("Error uploading file:", error);
    }
}

// Call the function with the path to your file
uploadFile('C:/Users/karti/OneDrive/Documents/New folder/four.png');
