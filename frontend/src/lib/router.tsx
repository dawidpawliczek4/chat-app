import { createBrowserRouter } from "react-router-dom";
import Home from "../Home";
import Server from "../components/Server";

export const router = createBrowserRouter([
  {
    path: "/",
    element: <Home />,
    children: [],
  },
  {
    path: "/server",
    element: <Server />,
    children: [],
  },
]);
