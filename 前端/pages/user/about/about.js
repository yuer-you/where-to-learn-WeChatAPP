// pages/about/about.js
Page({

    /**
     * 页面的初始数据
     */
    data: {

    },

    /**
     * 生命周期函数--监听页面加载
     */
    onLoad(options) {

    },

    // 复制内容
    bindCopyGithub: function (params) {
        wx.setClipboardData({
            data: 'https://github.com/yuer-you'
        })
    },

    // 复制内容
    bindCopyQQ: function (params) {
        wx.setClipboardData({
            data: '731312679'
        })
    },

    // 复制内容
    bindCopyQQEmail: function (params) {
        wx.setClipboardData({
            data: '970750948@qq.com'
        })
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