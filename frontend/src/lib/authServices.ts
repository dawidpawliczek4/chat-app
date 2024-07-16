import axios from "axios";
import { store } from "../store/store";
import { useRouter } from "vue-router";

export const getUserIdFromToken = (token: string) => {
  const tokenParts = token.split(".");
  const encodedPayload = tokenParts[1];
  const decodedPayload = atob(encodedPayload);
  const payloadData = JSON.parse(decodedPayload);
  const userId = payloadData.user_id;
  return userId;
};

export const getUserDetails = async () => {
  try {
    const userId = localStorage.getItem("userId");
    const accessToken = localStorage.getItem("access");

    const response = await axios.get(
      `http://localhost:8000/api/account/?user_id=${userId}`,
      {
        headers: {
          Authorization: `Bearer ${accessToken}`,
        },
      }
    );

    const userDetails = response.data;
    localStorage.setItem("username", userDetails.username);

    store.setIsAuthenticated(true);
  } catch (error) {
    alert("Error fetching user details");
    console.error(error);

    store.setIsAuthenticated(false);
  }
};

export const logout = () => {
  store.setIsAuthenticated(false);
  localStorage.removeItem("access");
  localStorage.removeItem("refresh");
  localStorage.removeItem("userId");
  localStorage.removeItem("username");
  const router = useRouter();
  router.push("/login");
};

export const refreshAccessToken = async () => {
  try {
    const refreshToken = localStorage.getItem("refresh");

    const response = await axios.post(
      "http://localhost:8000/api/token/refresh/",
      {
        refresh: refreshToken,
      }
    );

    const accessToken = response.data.access;
    localStorage.setItem("access", accessToken);
  } catch (error) {
    console.error(error);
  }
};

export const register = async (username: string, password: string) => {
  const response = await axios.post("http://localhost:8000/api/register/", {
    username,
    password,
  });
};
