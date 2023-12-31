import Vue from 'vue'
import Router from 'vue-router'
//引用Result页面
import Result from '@/components/Result'

Vue.use(Router)

export default new Router({
  routes: [//定义routes路由的集合，数组类型
    //单个路由均为对象类型，path代表的是路径，component代表组件
    {
      path: '/',
      name: 'Result',
      component: Result
    }
  ]
})
