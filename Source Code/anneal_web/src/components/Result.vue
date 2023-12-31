<template>
  <div class="content-wrapper">
    <div class="module-wrapper">
      <div class="titleline">
        罩式炉特殊钢种的智能化退火系统
      </div>
    </div>

    <div class="module-wrapper">
      <el-row :gutter="40">
        <el-col :span="300">
          <el-form label-width="80px">
            <el-form-item label="退火材料" prop="material">
              <el-select v-model="material_search" style="width:120px" placeholder="请选择退火材料">
                <el-option
                  v-for="item in material_options"
                  :key="item.value"
                  :label="item.label"
                  :value="item.value">
                </el-option>
              </el-select>
            </el-form-item>
          </el-form>
        </el-col>
        <el-col :span="300">
          <el-form :rules="inputInfo" ref="form" :model="form" label-width="155px">
            <el-form-item prop="thickness" label="请输入材料厚度(mm)">
              <el-input v-model.trim="form.thickness" style="width:150px" clearable />
            </el-form-item>
          </el-form>
        </el-col>
        <el-col :span="300">
          <el-button type="primary" @click="toFit" :loading="toFit_loading">生成退火线</el-button>
        </el-col>
      </el-row>
    </div>

    <div class="module-wrapper">
      <el-row :gutter="50">
        <el-col :span="12">
<!--          退火线绘制模块-->
          <el-card class="box-card">
            <div id="FuncAnneal" class="issue_chart" >
            </div>
            <div class="module-wrapper">
              <el-steps :active="step" align-center>
                <el-step
                  v-for="(gas_steps, index) in gas_steps"
                  :key="index"
                  :title="gas_steps.title"
                  :description="gas_steps.description"
                >
                </el-step>
              </el-steps>
            </div>
          </el-card>
        </el-col>
        <el-col :span="12">
<!--          罩式炉温度场显示模块-->
          <el-card class="box-card">
            <div class="module-wrapper">
              <div id="heatmap">
                <img src="../assets/img/stove.png" style="width:100%; height: 100%">
              </div>
            </div>
            <div class="module-wrapper">
              <el-row :gutter="80">
                <el-col :span="200">
                  <el-button type="primary" @click="lastStep" :loading="lastStep_loading" :disabled="lastStep_disabled">上个阶段</el-button>
                </el-col>
                <el-col :span="200">
                  <el-button type="primary" @click="nextStep" :loading="nextStep_loading" :disabled="nextStep_disabled">下个阶段</el-button>
                </el-col>
              </el-row>
            </div>
          </el-card>
        </el-col>
      </el-row>
    </div>

    <div class="module-wrapper">
      <div>
        <el-button type="text">说明文档</el-button>
      </div>
    </div>

  </div>

</template>

<script>
  import * as echarts from 'echarts';
  import axios from "axios";
  import Heatmap from 'heatmap.js'
  export default {
    name: 'Result',
    data () {
      return {
        baseURL:'http://127.0.0.1:8000/',
        material_options: [{
          value: '1',
          label: '硅钢'
        }],
        material_search: '1',

        form: {
          thickness:'',
        },

        // 添加el-form-item里input中的输入规则，必须有prop来标注
        inputInfo: {
          thickness: [
            { required: true, message: '请输入材料厚度', trigger: 'blur' }
          ],
        },

        first_heat_time: 1,
        second_heat_time: 0.5,
        third_heat_time: 34.67,
        first_cool_time: 12,
        second_cool_time: 10,
        third_cool_time: 7,
        fourth_cool_time: 30,
        anneal_line_point: {
          first: 0.0,
          second: 0.0,
          third: 0.0,
        },

        gas_steps: [{
          title: '阶段一',
          description: '氮气：1.5；氢气：4.5',
        }, {
          title: '阶段二',
          description: '氮气：2.0；氢气：6.0',
        }, {
          title: '阶段三',
          description: '氮气：0.0；氢气：6.0',
        }, {
          title: '阶段四',
          description: '氮气：1.5；氢气：4.5'
        }, {
          title: '阶段五',
          description: '氮气：6.0；氢气：0.0',
        }],

        x_data:[],

        optionFunc: {
          title: {
            text: '厚度XXmm的XX卷退火线',
            left: 'center'
          },
          // 设置折线图的大小
          grid: { //调整图表上下左右位置
            top:'18%',
            left: '1%',
            right: '13%',
            bottom: '0%',
            // width:'auto',
            // height:'auto',
            containLabel: true
          },
          // 具体点击or鼠标放在某一项上 所展示的样式内容
          tooltip: {
            trigger: 'item',   // axis   item   none三个值
            confine: true
          },
          // 左上侧分类条形符
          legend: {
            orient: 'vertical',
            left: 'left',
            // data: ['退火线'],// 数组
          },
          xAxis: {
            //type: 'time',   // 还有其他的type，可以去官网喵两眼哦
            boundaryGap: false,
            data: [0,10,20,30,40,50,60,70,80,90,100],   // x轴数据，需要从数据库获取
            name: '时间/h',   // x轴名称
            // x轴名称样式
            // nameTextStyle: {
            //   fontWeight: 500,
            //   fontSize: 15,
            // },
            // axisTick: {
            //   interval:(index)=>{
            //     let b=[0,2,4,1,3,8,7,4,3,3,7]
            //     for(let i in b){
            //       if(index === b[i]){
            //         return true
            //       }
            //     }
            //     return false
            //   }
            // },
            // axisLabel: {
            //   formatter: (item,index)=>{
            //     let a= ['0', '20', '60', '3', '4', '5', '6']
            //     let b=[0,1,5,8,17,25,30,34,37,44]
            //     for(let i in b){
            //       if(index === b[i]){
            //         return a[i]
            //       }
            //     }
            //     return ''
            //   }
            // },
          },
          yAxis: {
            type: 'value',
            name: '温度/°C',   // y轴名称
            // y轴名称样式
            nameTextStyle: {
              fontWeight: 500,
              fontSize: 15
            },
            axisLine: {
              show: true, //设置竖线是否显示
            },
            axisTick: { show: false }, //是否显示刻度线
          },
          // 折线图类型以及数据
          series: [ // 数组类型，y轴数据
            {
              name: '退火线',
              type: 'line',
              itemStyle: {
                color: '#848484'
              },
              data: [0, 550, 550, 650, 650, 1170, 1170, 1000, 850, 700, 380],// 要从数据库中获取
            },
          ]
        },
        FuncAnneal: {},

        step: 0,
        toFit_loading: false,
        lastStep_loading: false,
        lastStep_disabled: true,
        nextStep_loading: false,
        nextStep_disabled: true,

        outer_cover_x1:158,
        outer_cover_y1:119,
        outer_cover_x2:360,
        outer_cover_y2:360,
        inner_cover_x1:185,
        inner_cover_y1:167,
        inner_cover_x2:300,
        inner_cover_y2:420,
      }
    },
    created() {},
    mounted() {
      this.optionFunc.xAxis.data = [0,10,20,30,40,50,60,70,80,90,100]
      //在了解echarts绘制机制，echarts图形只绘制一次,且绘制时自动获取父级大小填写宽度，考虑让echarts延迟绘制使用setTimeout。
      //即必须给时间先获取父级组件大小
      setTimeout(()=>{
        this.drawFuncAnneal()
        this.heatMap()
      })
    },
    methods: {
      drawFuncAnneal() {
        //必须先获取数据再画图，只有这样图才能正确获得数据然后渲染出。而且画图的代码必须写在then里面，后米啊米可以加图的样式
        this.chartPay = echarts.init(document.getElementById('FuncAnneal'))
        this.chartPay.setOption(this.optionFunc, true)
        // this.chartPay.resize()
      },
      toFit(){
        console.log(ssss)
        const ssss = 'hhh'
        //判空
        this.$refs['form'].validate((valid) => {
          if (valid) {
            let postData={
              "id":this.material_search,
              "material":this.material_options[this.material_search-1].label,
              "thickness":Number(this.form.thickness)
            }
            axios.post(this.baseURL+'bpDeep/',postData)
              .then((response)=>{
                this.toFit_loading = true
                this.lastStep_disabled = true
                this.nextStep_disabled = false
                this.step = 0
                this.$message.success("成功")
                this.anneal_line_point = response.data.data
                console.log(this.anneal_line_point)
                this.optionFunc.xAxis.data = [0, parseFloat((this.first_heat_time).toFixed(2)), parseFloat((this.first_heat_time+this.anneal_line_point.first).toFixed(2)),
                  parseFloat((this.first_heat_time+this.anneal_line_point.first+this.second_heat_time).toFixed(2)),
                  parseFloat((this.first_heat_time+this.anneal_line_point.first+this.second_heat_time+this.anneal_line_point.second).toFixed(2)),
                  parseFloat((this.first_heat_time+this.anneal_line_point.first+this.second_heat_time+this.anneal_line_point.second+this.third_heat_time).toFixed(2)),
                  parseFloat((this.first_heat_time+this.anneal_line_point.first+this.second_heat_time+this.anneal_line_point.second+this.third_heat_time+this.anneal_line_point.third).toFixed(2)),
                  parseFloat((this.first_heat_time+this.anneal_line_point.first+this.second_heat_time+this.anneal_line_point.second+this.third_heat_time+this.anneal_line_point.third+this.first_cool_time).toFixed(2)),
                  parseFloat((this.first_heat_time+this.anneal_line_point.first+this.second_heat_time+this.anneal_line_point.second+this.third_heat_time+this.anneal_line_point.third+this.first_cool_time+this.second_cool_time).toFixed(2)),
                  parseFloat((this.first_heat_time+this.anneal_line_point.first+this.second_heat_time+this.anneal_line_point.second+this.third_heat_time+this.anneal_line_point.third+this.first_cool_time+this.second_cool_time+this.third_cool_time).toFixed(2)),
                  parseFloat((this.first_heat_time+this.anneal_line_point.first+this.second_heat_time+this.anneal_line_point.second+this.third_heat_time+this.anneal_line_point.third+this.first_cool_time+this.second_cool_time+this.third_cool_time+this.fourth_cool_time).toFixed(2))]
                console.log(this.optionFunc.xAxis.data)
                this.optionFunc.title.text = '厚度为'+this.form.thickness+'mm的'+this.material_options[this.material_search-1].label+'卷退火线'
                this.drawFuncAnneal();
                this.gas_steps[0].title = '0~'+this.optionFunc.xAxis.data[4]+'h'
                this.gas_steps[1].title = this.optionFunc.xAxis.data[4]+'~'+this.optionFunc.xAxis.data[5]+'h'
                this.gas_steps[2].title = this.optionFunc.xAxis.data[5]+'~'+this.optionFunc.xAxis.data[7]+'h'
                this.gas_steps[3].title = this.optionFunc.xAxis.data[7]+'~'+this.optionFunc.xAxis.data[9]+'h'
                this.gas_steps[4].title = this.optionFunc.xAxis.data[9]+'~'+this.optionFunc.xAxis.data[10]+'h'
                this.toFit_loading = false
              }).catch((error)=>{
              this.$message.error("失败")
            })
          } else {
            this.$message.error('不能为空！')
          }
        })
      },

      heatMap() {
        var heatmapInstance = Heatmap.create({
          container: document.getElementById('heatmap')
        });
        var points = [];
        var max = 3;
        // var point_01 = {
        //   x:200,//x轴位置
        //   y:150,//y轴位置
        //   value:5,
        //   radius:50//热力点半径大小
        // }
        // var point_02 = {
        //   x:250,
        //   y:250,
        //   value:5,
        //   radius:50
        // }
        // var point_03 = {
        //   x:300,
        //   y:180,
        //   value:5,
        //   radius:50
        // }
        // var point_04 = {
        //   x:300,
        //   y:320,
        //   value:5,
        //   radius:50
        // }
        // points.push(point_01);
        // points.push(point_02);
        // points.push(point_03);
        // points.push(point_04);
        for(let x=this.outer_cover_x1;x<=this.outer_cover_x2;x+=5){
          var point_top={
            x:x,
            y:119,
            value:1,
            radius:30
          }
          var point_btm={
            x:x,
            y:360,
            value:1,
            radius:30
          }
          points.push(point_top)
          points.push(point_btm)
        }
        for(let y=this.outer_cover_y1;y<=this.outer_cover_y2;y+=5){
          var point_left={
            x:158,
            y:y,
            value:1,
            radius:30
          }
          var point_right={
            x:360,
            y:y,
            value:1,
            radius:30
          }
          points.push(point_left)
          points.push(point_right)
        }
        var data = {
          max: max,
          data: points
        }
        // 因为data是一组数据,web切图报价所以直接setData
        heatmapInstance.setData(data)
      },

      lastStep() {
        if(this.step>0){
          this.lastStep_loading = true
          this.lastStep_disabled = false
          this.nextStep_disabled = false
          this.step--
          //功能
          this.lastStep_loading = false
        } else {
          this.lastStep_disabled = true
        }

      },
      nextStep() {
        if(this.step<this.gas_steps.length){
          this.nextStep_loading = true
          this.nextStep_disabled = false
          this.lastStep_disabled = false
          this.step++
          //功能
          this.nextStep_loading = false
        } else {
          this.nextStep_disabled = true
        }
      },
    }
  }
</script>


<style scoped>
  .box-card {
    height: 700px;
  }
  .issue_chart {
    height: 500px;
  }
</style>
