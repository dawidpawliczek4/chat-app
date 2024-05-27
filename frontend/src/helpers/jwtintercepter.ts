import axios, { AxiosInstance } from "axios";
import { useNavigate } from "react-router-dom";
import { BASE_URL } from "../lib/urls";

const useAxiosWithInterceptor = (): AxiosInstance => {
  const navigate = useNavigate();
  const axiosInstance = axios.create({
    baseURL: BASE_URL,
  });

  //   axiosInstance.interceptors.request.use(
  //     (config) => {
  //       const token = localStorage.getItem("token");
  //       if (token) {
  //         config.headers.Authorization = `Bearer ${token}`;
  //       }
  //       return config;
  //     },
  //     (error) => {
  //       return Promise.reject(error);
  //     }
  //   );

  axiosInstance.interceptors.response.use(
    (response) => {
      return response;
    },
    (error) => {
      if (error.response.status === 403) {
        navigate("/login");        
      }
    }
  );

  return axiosInstance;
};

export default useAxiosWithInterceptor;
