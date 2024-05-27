import useAxiosWithInterceptor from "../helpers/jwtintercepter";
import { useState } from "react";
import { BASE_URL } from "../lib/urls";

const useFetch = <T>(initialData: T[], apiURL: string) => {
  const axios = useAxiosWithInterceptor();
  const [data, setData] = useState<T[]>(initialData);
  const [error, setError] = useState<Error | null>(null);
  const [isLoading, setIsLoading] = useState<boolean>(false);

  const fetchData = async () => {
    setIsLoading(true);
    try {
      const response = await axios.get(`${BASE_URL}${apiURL}`);      
      setData(response.data);
      setIsLoading(false);
      setError(null);
      return data;
    } catch (error: any) {
      if (error.response && error.response.status === 400) {
        setError(new Error("400"));
      }
      setIsLoading(false);
      throw error;
    }
  };

  return { fetchData, data, error, isLoading };
};

export default useFetch;
