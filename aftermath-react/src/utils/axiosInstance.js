import axios from 'axios'

// This can be used to set defaults for all axios objects. baseURL will automatically be prepended to all endpoints
// Just import this variable instead of importing from the base axios library
const instance = axios.create({
    // Set address/port of target flask server
    baseURL:process.env.REACT_APP_API_URL + ':' + process.env.REACT_APP_API_PORT + '/',
    timeout: 10000,
    withCredentials: true

});

export default instance