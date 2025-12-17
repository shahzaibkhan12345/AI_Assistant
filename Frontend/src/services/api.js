// frontend/src/services/api.js

import axios from 'axios';

// Create an Axios instance with a base URL and other default settings
const apiClient = axios.create({
  baseURL: 'http://127.0.0.1:8000', // Your FastAPI backend URL
  headers: {
    'Content-Type': 'application/json',
  },
});

// Function to generate a post
export const generatePost = async (postData) => {
  try {
    const response = await apiClient.post('/api/v1/posts/generate', postData);
    return response.data; // Return the data from the response
  } catch (error) {
    console.error("Error generating post:", error);
    throw error; // Re-throw the error to be handled by the component
  }
};
// Function to get all posts
export const getAllPosts = async () => {
  try {
    const response = await apiClient.get('/api/v1/posts/');
    return response.data; // The response will be an array of posts
  } catch (error) {
    console.error("Error fetching posts:", error);
    throw error;
  }
};
// Function to publish a post
export const publishPost = async (postId) => {
  try {
    const response = await apiClient.post(`/api/v1/posts/${postId}/publish`);
    return response.data; // Return the success message
  } catch (error) {
    console.error("Error publishing post:", error);
    // We can get a more specific error message from the response
    const errorMessage = error.response?.data?.detail || 'Failed to publish post.';
    throw new Error(errorMessage);
  }
};