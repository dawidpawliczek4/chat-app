export interface Message {
  sender: string;
  content: string;
  timestamp: string;
}

export type Channel = {
  id: number;
  name: string;
};

export type Server = {
  id: number;
  name: string;
  icon?: string;
};
