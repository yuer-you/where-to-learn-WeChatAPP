// pages/schedule/mine/mine.js
const app = getApp()
Component({
    /**
     * 组件的属性列表
     */
    properties: {

    },

    /**
     * 组件的初始数据
     */
    data: {
        classdate: ['上午第一节', '上午第二节', '中午', '下午第一节', '下午第二节', '晚上第一节', '晚上第二节'],
        table: '',
        schedule: null,
        bool_schedule: 0,
        if_change_schedule: null,
    },

    lifetimes: {
        // 在页面第一次创建时
        created: function () {
            this.setData({
                bool_schedule: app.globalData.bool_schedule,
                table: app.globalData.table,
                schedule: app.globalData.schedule,
                if_change_schedule: app.globalData.if_change_schedule,
            })
            // 当用户上传课表并且课表内容为空是时
            if (this.data.bool_schedule && (this.data.schedule == null)) {
                this.getSchedule()
            }
        },

        // 在页面显示时
        attached: function () {
            this.setData({
                schedule: app.globalData.schedule,
                if_change_schedule: app.globalData.if_change_schedule,
            })
            // 当用户上传课表并且课表更改时
            if (this.data.bool_schedule && this.data.if_change_schedule) {
                this.getSchedule()
            }
        }
    },

    /**
     * 组件的方法列表
     */
    methods: {
        // 获取课表内容
        getSchedule: function (params) {
            wx.showLoading({
                title: '加载中...',
            })
            wx.request({
                url: 'https://smallapp.easternlake.site/wx/getSchedule.py?table=' + this.data.table,
                method: 'GET',
                success: (res) => {
                    if (res.data.schedule) {
                        this.setData({
                            schedule: res.data.schedule,
                            if_change_Schedule: 0,
                        })
                        app.globalData.schedule = this.data.schedule
                        app.globalData.if_change_schedule = this.data.if_change_schedule
                        console.log('加载成功：', res.data.schedule)
                    } else {
                        wx.showToast({
                            title: '加载错误',
                            icon: 'error',
                            duration: 2000
                        })
                    }
                },
                complete: function (params) {
                    wx.hideLoading();
                }
            })
        }
    }
})
