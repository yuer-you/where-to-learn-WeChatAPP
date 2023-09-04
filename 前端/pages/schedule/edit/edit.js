// pages/schedule/edit/edit.js
const app = getApp()
var whichDayIndex
var whichClassIndex
Component({
    /**
     * 组件的属性列表
     */
    properties: {

    },

    // 组件所在的页面被展示时执行
    lifetimes: {
        attached: function () {
            whichDayIndex=this.data.dayIndex
            whichClassIndex=this.data.classIndex
            this.setData({
                schedule: app.globalData.schedule,
                table: app.globalData.table,
                classname: app.globalData.schedule[whichClassIndex][whichDayIndex][0],
                weeklong: app.globalData.schedule[whichClassIndex][whichDayIndex][1],
                teacher: app.globalData.schedule[whichClassIndex][whichDayIndex][2],
                classroom: app.globalData.schedule[whichClassIndex][whichDayIndex][3],
            })
        }
    },

    /**
     * 组件的初始数据
     */
    data: {
        schedule: null,
        table: '',
        // 星期选择
        dayArray: ['星期一', '星期二', '星期三', '星期四', '星期五', '星期六', '星期日'],
        dayIndex: 0,

        // 节数选择
        classArray: ['上午第一节', '上午第二节', '中午', '下午第一节', '下午第二节', '晚上第一节', '晚上第二节'],
        classIndex: 0,

        // input输入
        classname: '',
        weeklong: '',
        classroom: '',
        teacher: '',
    },

    /**
     * 组件的方法列表
     */
    methods: {
        // 星期选择器
        bindDayChange: function(e) {
            // console.log('选择星期', e.detail.value)
            whichDayIndex=e.detail.value
            if (this.data.schedule[whichClassIndex][whichDayIndex]) {
                this.setData({
                    dayIndex: e.detail.value,
                    classname: this.data.schedule[whichClassIndex][whichDayIndex][0],
                    weeklong: this.data.schedule[whichClassIndex][whichDayIndex][1],
                    teacher: this.data.schedule[whichClassIndex][whichDayIndex][2],
                    classroom: this.data.schedule[whichClassIndex][whichDayIndex][3],
                })
            } else {
                this.setData({
                    dayIndex: e.detail.value,
                    classname: '',
                    weeklong: '',
                    teacher: '',
                    classroom: '',
                })
            }
            
        },

        // 节数选择器
        bindClassChange: function(e) {
            // console.log('选择节数', e.detail.value)
            whichClassIndex=e.detail.value
            if (this.data.schedule[whichClassIndex][whichDayIndex]) {
                this.setData({
                    classIndex: e.detail.value,
                    classname: this.data.schedule[whichClassIndex][whichDayIndex][0],
                    weeklong: this.data.schedule[whichClassIndex][whichDayIndex][1],
                    teacher: this.data.schedule[whichClassIndex][whichDayIndex][2],
                    classroom: this.data.schedule[whichClassIndex][whichDayIndex][3],
                })
            } else {
                this.setData({
                    classIndex: e.detail.value,
                    classname: '',
                    weeklong: '',
                    teacher: '',
                    classroom: '',
                })
            }
            
        },

        // input提交
        bindClassnameInput: function (e) {
            // console.log('课程名称', e.detail)
            this.setData({
                classname: e.detail.value
            })
        },
        bindWeekInput: function (e) {
            // console.log('持续周数', e.detail)
            this.setData({
                weeklong: e.detail.value
            })
        },
        bindClassroomInput: function (e) {
            // console.log('上课教室', e.detail)
            this.setData({
                classroom: e.detail.value
            })
        },
        bindTeacherInput: function (e) {
            // console.log('教师姓名', e.detail)
            this.setData({
                teacher: e.detail.value
            })
        },

        // 提交修改
        changeSchedule: function (table, whichDayIndex, whichClassIndex, classname, weeklong, teacher, classroom) {
            wx.showLoading({
                title: '修改中...',
            })
            wx.request({
                url: 'https://你的服务器网址/changeSchedule.py',
                data: {
                    table: table,
                    day: whichDayIndex,
                    class: whichClassIndex,
                    classname: classname,
                    weeklong: weeklong,
                    teacher: teacher,
                    classroom: classroom
                },
                method: 'GET',
                success: (res) => {
                    if (res.data.success) {
                        wx.showToast({
                            title: '修改成功',
                            icon: 'success',
                            duration: 2000
                        })
                        console.log('修改成功：', res.data.message)
                        app.globalData.if_change_schedule = 1
                    } else {
                        wx.showToast({
                            title: '修改失败',
                            icon: 'error',
                            duration: 2000
                        })
                        console.log('修改失败：', res.data.message)
                    }
                },
                complete: function () {
                    wx.hideLoading();
                }
            })
        },

        // 表单提交
        formSubmit(e) {
            this.changeSchedule(this.data.table, whichDayIndex, whichClassIndex, this.data.classname, this.data.weeklong, this.data.teacher, this.data.classroom)
        },
    }
})
