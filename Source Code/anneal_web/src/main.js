// The Vue build version to load with the `import` command
// (runtime-only or standalone) has been set in webpack.base.conf with an alias.
import Vue from 'vue'
import App from './App'
import router from './router'
import Cookies from 'js-cookie'
import './assets/css/globalCSS.css';//引入全局css

Vue.config.productionTip = false

//引用element-ui
import ElementUI from 'element-ui'
import 'element-ui/lib/theme-chalk/index.css'
Vue.use(ElementUI, {
  size: Cookies.get('size') || 'medium', // set element-ui default size
})
//引入echarts
import * as echarts from 'echarts';
Vue.prototype.$echarts = echarts

//引入axios
import axios from 'axios' //注意这行
Vue.prototype.$http = axios; //注意这行
Vue.prototype.$axios = axios;
global.axios = axios;  //设置一个全局axios便于调用
axios.defaults.headers.post['Content-Type'] = 'application/json;charset=UTF-8';

import Heatmap from 'heatmap.js'
Vue.use(Heatmap)

/* eslint-disable no-new */
new Vue({
  el: '#app',
  router,
  components: { App },
  template: '<App/>'
})
