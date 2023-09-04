// pages/index/index.js
const app=getApp()
Page({

    /**
     * 页面的初始数据
     */
    data: {
        // 收藏教室
        openid: null,
        bool_classroom: null,
        dayTime: [null, '早一', '早二', '中午', '下一', '下二', '晚一', '晚二'],
        classroomName: null,
        classroomState: null,
        buildingName: null,
        classroomNumber: null,

        // 今日课表
        bool_schedule: null,
        table: null,
        schedule_today: null,
        name_today: null,
            // 是否改变课表
        if_change_schedule: null,
        classdate: ['早一', '早二', '中午', '下一', '下二', '晚一', '晚二'],

        // 大家都爱去
        IndexList: [1,2,3,4,5,6,7,8,9,10],
        classroomRanking: null,
    },

    /**
     * 生命周期函数--监听页面加载
     */
    onLoad: function (options) {
        this.setData({
            openid: app.globalData.openid,
            bool_classroom: app.globalData.bool_classroom,
            bool_schedule: app.globalData.bool_schedule,
            table: app.globalData.table,
            if_change_schedule: app.globalData.if_change_schedule,
            classroomName: [app.globalData.classroom1, app.globalData.classroom2, app.globalData.classroom3],
            buildingName: [
                this.changeBuilding(app.globalData.classroom1),
                this.changeBuilding(app.globalData.classroom2),
                this.changeBuilding(app.globalData.classroom3)
            ],
            classroomNumber: [
                this.changeClassNumber(app.globalData.classroom1),
                this.changeClassNumber(app.globalData.classroom2),
                this.changeClassNumber(app.globalData.classroom3)
            ],
        })
        // 如果课表发生改变，则重新获取（应该，我也忘了）
        if (this.data.if_change_schedule == 0) {
            this.getScheduleToday()
        }
        // 如果有收藏教室，则获取
        if (this.data.bool_classroom) {
            this.getClassroomCollect(this.data.buildingName, this.data.classroomNumber)
        }
        this.getClassroomRanking()
    },

    // 获取收藏教室的教室状态
    getClassroomCollect: function (buildingName, classroomNumber) {
        const buildingName_json = JSON.stringify(buildingName)
        const classroomNumber_json = JSON.stringify(classroomNumber)
        wx.request({
            url: 'https://你的服务器网址/getClassroomCollect.py',
            data: {
                buildingName: buildingName_json,
                classroomNumber: classroomNumber_json
            },
            method: 'GET',
            success: (res) => {
                if (res.data.classroomState) {
                    this.setData({
                        classroomState: res.data.classroomState,
                        name_today: res.data.today_name
                    })
                    this.changeDay()    // 更改命名方式
                }
                console.log('教室状态', this.data.classroomState)
            }
        })
    },

    // 获取今日课表
    getScheduleToday: function () {
        wx.request({
            url: 'https://你的服务器网址/getScheduleToday.py?table=' + this.data.table,
            method: 'GET',
            success: (res) => {
                if (res.data.today_schedule) {
                    this.setData({
                        schedule_today: res.data.today_schedule,
                        name_today: res.data.today_name
                    })
                    this.changeDay()    // 更改命名方式
                    console.log('今日课表', this.data.schedule_today)
                    // console.log('星期', this.data.name_today)
                }
            }
        })
    },

    // 获取教室排名
    getClassroomRanking: function () {
        wx.request({
            url: 'https://你的服务器网址/getClassroomRanking.py',
            method: 'GET',
            success: (res) => {
                if (res.data.classroomRanking) {
                    this.setData({
                        classroomRanking: res.data.classroomRanking
                    })
                    console.log('教室排名', this.data.classroomRanking)
                }
            }
        })
    },

    // 中文命名星期
    changeDay: function () {
        switch (this.data.name_today) {
            case 0:
                this.setData({name_today: '星期一'})
                break
            case 1:
                this.setData({name_today: '星期二'})
                break
            case 2:
                this.setData({name_today: '星期三'})
                break
            case 3:
                this.setData({name_today: '星期四'})
                break
            case 4:
                this.setData({name_today: '星期五'})
                break
            case 5:
                this.setData({name_today: '星期六'})
                break
            case 6:
                this.setData({name_today: '星期日'})
                break
        }
    },

    // 获取库名
    changeBuilding: function (classroom) {
        if (classroom != null) {
            var letters = classroom.slice(0, 2)
            if (letters == 'SY') return 'sy'
            else if (letters == 'SX') return 'sx'
            else if (letters == 'SD') return 'sd'
            else if (letters == 'YF') return 'yf'
            else if (letters == 'DQ') return 'dq'
            else if (letters == '九教') return 'nine'
            else if (letters == '建艺') return 'art'
            else {
                letters = classroom.slice(0, 1)
                if (letters == 'Z') return 'z'
                else if (letters == '8') return 'eight'
                else  return False
            }
        } else return null
    },

    // 获取classroom列的值
    changeClassNumber: function (classroom) {
        if (classroom != null) {
            var number = classroom.match(/\d+/g);
            if (classroom.substring(0, 3) == '九教东') {
                number = '6' + number
            } else if (classroom.substring(0, 3) == '九教中') {
                number = '5' + number
            }
            number = number.map(Number)[0]
            return number
        } else return null
        
    },

    /**
     * 生命周期函数--监听页面初次渲染完成
     */
    onReady: function () {

    },

    /**
     * 生命周期函数--监听页面显示
     */
    onShow: function () {
        this.setData({
            openid: app.globalData.openid,
            bool_classroom: app.globalData.bool_classroom,
            bool_schedule: app.globalData.bool_schedule,
            table: app.globalData.table,
            if_change_schedule: app.globalData.if_change_schedule,
            classroomName: [app.globalData.classroom1, app.globalData.classroom2, app.globalData.classroom3],
            buildingName: [
                this.changeBuilding(app.globalData.classroom1),
                this.changeBuilding(app.globalData.classroom2),
                this.changeBuilding(app.globalData.classroom3)
            ],
            classroomNumber: [
                this.changeClassNumber(app.globalData.classroom1),
                this.changeClassNumber(app.globalData.classroom2),
                this.changeClassNumber(app.globalData.classroom3)
            ],
        })
        if (this.data.if_change_schedule == 0) {
            this.getScheduleToday()
        }
        if (this.data.bool_classroom) {
            this.getClassroomCollect(this.data.buildingName, this.data.classroomNumber)
        }
        this.getClassroomRanking()
    },

    /**
     * 生命周期函数--监听页面隐藏
     */
    onHide: function () {

    },

    /**
     * 生命周期函数--监听页面卸载
     */
    onUnload: function () {

    },

    /**
     * 页面相关事件处理函数--监听用户下拉动作
     */
    onPullDownRefresh: function () {

    },

    /**
     * 页面上拉触底事件的处理函数
     */
    onReachBottom: function () {

    },

    /**
     * 用户点击右上角分享
     */
    onShareAppMessage: function () {

    }

})