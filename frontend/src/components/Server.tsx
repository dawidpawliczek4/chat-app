import { useState } from "react";
import useWebSocket from "react-use-websocket";

const Server = ({}) => {
  const [newMessage, setNewMessage] = useState<string[]>([]);
  const [message, setMessage] = useState<string>("");
  const [serverId, setServerId] = useState<string>("1");
  const [channelId, setChannelId] = useState<string>("1");

  const socketUrl = `ws://localhost:8000/${serverId}/${channelId}`;

  const { sendJsonMessage, lastMessage, readyState } = useWebSocket(socketUrl, {
    onOpen: () => console.log("opened"),
    onClose: () => console.log("closed"),
    onError: () => console.log("error"),
    onMessage: (msg) => {
      const data = JSON.parse(msg.data);
      setNewMessage((prev) => [...prev, data.message]);
    },
  });

  return (
    <div>
      {newMessage.map((msg, index) => (
        <div key={index}>{msg}</div>
      ))}

      <form action="">
        <label htmlFor="">
          Enter Message:{" "}
          <input
            type="text"
            value={message}
            onChange={(e) => setMessage(e.target.value)}
          />
        </label>
        <button
          type="submit"
          onClick={(e) => {
            e.preventDefault();
            sendJsonMessage({ message: message });
            setMessage("");
          }}
        >
          Send
        </button>
      </form>

      <div>
        <label htmlFor="">
          Change server id
          <input
            type="text"
            value={serverId}
            onChange={(e) => setServerId(e.target.value)}
          />
        </label>
      </div>

      <div>
        <label htmlFor="">
          Change channel id
          <input
            type="text"
            value={channelId}
            onChange={(e) => setChannelId(e.target.value)}
          />
        </label>
      </div>

    </div>
  );
};

export default Server;
