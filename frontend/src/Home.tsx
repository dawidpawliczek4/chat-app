import { Avatar } from "@mui/material";
import useFetch from "./hooks/useFetch";
import { useEffect } from "react";
import { MEDIA_URL } from "./lib/urls";

function Home() {
  const { fetchData, data, error, isLoading } = useFetch([], "/server/select");

  useEffect(() => {
    fetchData();
  }, []);

  return (
    <div>
      {isLoading && <div>Loading...</div>}
      {error && <div>Error</div>}
      {data &&
        data.map((server: any) => {
          return (
            <div className="flex flex-row items-center" key={server.id}>
              <Avatar alt={server.name} src={`${MEDIA_URL}/${server.icon}`} />
              <div className="flex flex-col">
                <p className="font-semibold">{server.name}</p>
                <p>{server.category}</p>
              </div>
            </div>
          );
        })}
    </div>
  );
}

export default Home;
