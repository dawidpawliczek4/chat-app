import { createRouter, createWebHistory } from "vue-router";
import { createApp } from "vue";
import "./style.css";
import ChannelView from "./components/ChannelView.vue";
import LoginForm from "./components/LoginForm.vue";
import App from "./App.vue";
import RegisterForm from "./components/RegisterForm.vue";
import Layout from "./components/Layout.vue";
import ServerView from "./components/ServerView.vue";
import CreateServerView from "./components/CreateServerView.vue";

const routes = [
  {
    path: "/",
    component: Layout,
    beforeEnter: (to: any, from: any, next: any) => {
      if (localStorage.getItem("isAuthenticated") === "true") {
        next();
      } else {
        next("/login");
      }
    },
    children: [
      {
        path: ":serverId",
        component: ServerView,
        children: [
          {
            path: ":channelId",
            component: ChannelView,
          },
        ],
      },
    ],
  },
  { path: "/login", component: LoginForm },
  { path: "/register", component: RegisterForm },
  { path: "/create-server", component: CreateServerView },
];

const router = createRouter({
  history: createWebHistory(),
  routes,
});

createApp(App).use(router).mount("#app");
