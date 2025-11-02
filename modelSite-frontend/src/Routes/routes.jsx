import axios from 'axios';

const API_BASE_URL = 'http://127.0.0.1:8000'; 

const fetchDataFromFastAPI = async (data) => {
  try {
    const response = await axios.get(`${API_BASE_URL}/${data}`);
    return response.data;
  } catch (error) {
    console.error('Error connecting to FastAPI backend:', error);
    throw error;
  }
};

const signup = async (username, password) => {
  try {
    const response = await axios.post(`${API_BASE_URL}/signup`, {
      username,
      password,
    });

    return response.data;
  } catch (error) {
    console.error("Error logging in:", error);
    throw error;
  }
}

const loginUser = async (username, password) => {
  try {
    const response = await axios.post(`${API_BASE_URL}/login`, {
      username,
      password,
    });

    return response;
  } catch (error) {
    console.error("Error logging in:", error);
    throw error;
  }
};

const runModel = async (model, formData) => {
  try {
    const response = await axios.post(`${API_BASE_URL}/${model}`, formData, {
      headers: { "Content-Type": "multipart/form-data" },
    });
    
    console.log(response.data)
    return response.data;
  } catch (error) {
    console.error(`Error running ${model}:`, error);
    throw error;
  }
};


const router_functions = {
  fetchDataFromFastAPI,
  loginUser,
  runModel,
  signup
}

export default router_functions;