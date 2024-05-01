import axios from 'axios';

const BASE_URL = "http://127.0.0.1:5000"

export function uploadImage(file) {
    return axios.post(`${BASE_URL}/upload`, file)
}

export function generateDehazeImage(filename){
    return axios.get(`${BASE_URL}/generate/${filename}`)
}
