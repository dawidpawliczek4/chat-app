import { createRouter, createWebHistory } from "vue-router";
import { createApp } from "vue";
import "./style.css";
import HomeView from "./components/HomeView.vue";
import LoginForm from "./components/LoginForm.vue";
import App from "./App.vue";

const routes = [
  { path: "/", component: HomeView },
  { path: "/login", component: LoginForm },
];

const router = createRouter({
  history: createWebHistory(),
  routes,
});

createApp(App).use(router).mount("#app");
