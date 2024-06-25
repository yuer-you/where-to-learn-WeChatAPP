// pages/user/user.js
Page({
    /**
     * 页面的初始数据
     */
    data: {
        openid: null,
        username: '',
        userphotopath: '',
        day: null
    },

    /**
     * 生命周期函数--监听页面加载
     */
    onLoad: function (options) {
        const app = getApp()
        var openid = app.globalData.openid
        var username =  app.globalData.username
        var userphotopath = app.globalData.userphotopath
        var day = app.globalData.day
        this.setData({
            openid: openid,
            username: username,
            userphotopath: userphotopath,
            day: day
        })
    },
    
    // 跳转收藏教室页面
    collectClassroom: function (params) {
        wx.navigateTo({
          url: './collect/collect',
        })
    },

    // 跳转修改课表页面
    editSchedule: function (params) {
        wx.navigateTo({
          url: '../schedule/edit/edit',
        })
    },

    // 跳转修改头像和昵称页面
    editUser: function (params) {
        wx.navigateTo({
          url: './edituser/edituser',
        })
    },

    // 清除个人数据弹窗
    deleteData: function (params) {
        wx.showModal({
            title: '清除个人数据',
            content: '我们未收集过您的敏感信息（微信也不允许不经用户同意就收集）！\n\n个人数据为您设置的用户名、用户头像、收藏教室以及上传识别的课程表信息',
            confirmText: '确认删除',
            confirmColor: '#FC6060',

            // 开始删除
            complete: (res) => {        
                if (res.confirm) {
                    wx.showLoading({
                        title: '删除中...',
                    })
                    wx.request({
                        method: 'GET',
                        url: 'https://自己的网址/自己的储存路径/deleteData.py?openid=' + this.data.openid,
                        success: (res) => {
                            // console.log(res)
                            if (res.data === "success") {
                                wx.showModal({
                                    title: '清除个人数据',
                                    content: '删除成功',
                                    showCancel: false,
                                })
                            }
                            else {
                                wx.showModal({
                                    title: '清除个人数据',
                                    content: '删除失败',
                                    showCancel: false,
                                })
                            }
                        },
                        fail: (res) => {
                            wx.showModal({
                                title: '清除个人数据',
                                content: '请检查网络连接',
                                showCancel: false,
                            })
                        },
                        complete: function (params) {
                            wx.hideLoading();
                        }
                    })
                }
            }
        })
    },

    // 跳转关于页面
    about: function (params) {
        wx.navigateTo({
            url: './about/about',
          })
    },

    // 跳转教程页面
    teach: function (params) {
        wx.navigateTo({
            url: './teach/teach',
          })
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
        // 获取用户名
        const app = getApp()
        var username =  app.globalData.username
        var userphotopath = app.globalData.userphotopath
        this.setData({
            username: username,
            userphotopath: userphotopath
        })
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
