import axios from "axios";

export const useAxiosWithInterceptor = () => {
  const axiosInstance = axios.create();

  axiosInstance.interceptors.request.use(
    (config) => {
      const accessToken = localStorage.getItem("access");
      if (accessToken) {
        config.headers.Authorization = `Bearer ${accessToken}`;
      }
      return config;
    },
    (error) => {
      return Promise.reject(error);
    }
  );

  axiosInstance.interceptors.response.use(
    (response) => {
      return response;
    },
    async (error) => {
      const originalRequest = error.config;
      if (error.response.status === 401 && !originalRequest._retry) {
        originalRequest._retry = true;
        const refreshToken = localStorage.getItem("refresh");
        if (refreshToken) {
          try {
            const response = await axios.post(
              "http://localhost:8000/api/token/refresh/",
              {
                refresh: refreshToken,
              }
            );
            const newAccessToken = response.data.access;
            localStorage.setItem("access", newAccessToken);
            return axiosInstance(originalRequest);
          } catch (error) {
            console.error("Error refreshing token");
            console.error(error);
            alert("Error refreshing token");
          }
        }
      }
      return Promise.reject(error);
    }
  );

  return axiosInstance;
};
