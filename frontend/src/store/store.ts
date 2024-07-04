import { reactive } from "vue";

const isAuthenticated = localStorage.getItem("isAuthenticated") === "true";

export const store = reactive({
  isAuthenticated: isAuthenticated,
  setIsAuthenticated(value: boolean) {
    this.isAuthenticated = value;
    localStorage.setItem("isAuthenticated", value.toString());
  },
});
