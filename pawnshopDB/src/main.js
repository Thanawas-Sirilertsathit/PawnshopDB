import "./assets/main.css";
import { createApp } from "vue";
import App from "./App.vue";
import VueLazyload from "vue3-lazyload";
import VueDatePicker from "@vuepic/vue-datepicker";
import router from "./router";
import "./styles/styles.css";
import "@vuepic/vue-datepicker/dist/main.css";
import "highlight.js/styles/stackoverflow-dark.css";

const app = createApp(App).mount("#app");
app.component("VueDatePicker", VueDatePicker);
const placeholderAvatar = require("./assets/no_avatar.png");
app.use(VueLazyload, {
  preLoad: 1.3,
  error: placeholderAvatar,
  loading: placeholderAvatar,
  attempt: 3,
  log: false,
});
app.use(router).mount("#app");
