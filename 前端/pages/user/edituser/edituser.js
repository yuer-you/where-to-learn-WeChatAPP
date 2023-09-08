// pages/edituser/edituser.js
var app_ = getApp()
const noPhotoUrl = 'https://mmbiz.qpic.cn/mmbiz/icTdbqWNOwNRna42FI242Lcia07jQodd2FJGIYQfG0LAJGFxM4FbnQP6yfMxBgJ0F3YRqJCJ1aPAK2dQagdusBZg/0'
Page({

    /**
     * 页面的初始数据
     */
    data: {
        userphotopath: '',
        openid: null,
        username: '',
    },

    /**
     * 生命周期函数--监听页面加载
     */
    onLoad(options) {
        const app = getApp()
        var openid = app.globalData.openid
        var username =  app.globalData.username
        var userphotopath = app.globalData.userphotopath
        this.setData({
            openid: openid,
            username: username,
            userphotopath: userphotopath
        })
    },

    // 获取本地用户头像路径
    onChooseAvatar(e) {
        const userphotopath = e.detail.avatarUrl
        this.setData({
            userphotopath: userphotopath,
        })
        // console.log(userphotopath)
        // console.log(this.data.userphotopath)
    },

    // 提交修改
    formSubmit(e){
        const username = e.detail.value.nickname
        const userphotopath = this.data.userphotopath
        
        // 判断昵称是否为空
        if (username == '' || username == null) {
            wx.showModal({
                title: '修改昵称',
                content: '昵称不能为空',
                showCancel: false,
            })
        } else {
            app_.globalData.username = username
            // console.log('openid', this.data.openid)
            // console.log('username', app_.globalData.username)

            // 用户名修改
            wx.request({
                method: 'GET',
                url: 'https://你的服务器网址/saveUsername.py?openid=' + this.data.openid + '&username=' + username,
                success: (res) => {
                    wx.showToast({
                        title: '修改成功',
                    })
                },
                fail: (res) => {
                    wx.showToast({
                        title: '修改失败',
                    })
                    console.log(res)
                }
            })

            if (this.data.userphotopath != noPhotoUrl) {
                app_.globalData.userphotopath = userphotopath
                // 头像图片上传
                wx.uploadFile({
                    filePath: this.data.userphotopath,
                    name: 'image',
                    formData: {
                        'openid': this.data.openid,
                        'photoname': '1'
                    },
                    url: 'https://你的服务器网址/downLoadPhoto.py',
                    success: (res) => {
                        console.log('成功：',res.data)
                    },
                    fail: (res) => {
                        console.log('失败：',res.statusCode)
                    }
                })
            }
        }
    },

    /**
     * 生命周期函数--监听页面初次渲染完成
     */
    onReady() {

    },

    /**
     * 生命周期函数--监听页面显示
     */
    onShow() {

    },

    /**
     * 生命周期函数--监听页面隐藏
     */
    onHide() {

    },

    /**
     * 生命周期函数--监听页面卸载
     */
    onUnload() {

    },

    /**
     * 页面相关事件处理函数--监听用户下拉动作
     */
    onPullDownRefresh() {

    },

    /**
     * 页面上拉触底事件的处理函数
     */
    onReachBottom() {

    },

    /**
     * 用户点击右上角分享
     */
    onShareAppMessage() {

    }
})