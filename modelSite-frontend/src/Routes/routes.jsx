import axios from 'axios';

const API_BASE_URL = 'http://localhost:8000'; 

const fetchDataFromFastAPI = async (data) => {
  try {
    const response = await axios.get(`${API_BASE_URL}/${data}`);
    return response.data;
  } catch (error) {
    console.error('Error connecting to FastAPI backend:', error);
    throw error;
  }
};

const loginUser = async (username, password) => {
  console.log(username, password)
  try {
    const response = await axios.get(`${API_BASE_URL}/login`);

    return response.data
  } catch (error){
    console.error("Error getting login info");
    throw error;
  }
}

const router_functions = {
  fetchDataFromFastAPI,
  loginUser
}

export default router_functions;