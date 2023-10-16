// pages/user/teach/teach.js
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

    adLoad() {
        console.log('Banner 广告加载成功')
    },
    adError(err) {
        console.log('Banner 广告加载失败', err)
    },
    adClose() {
        console.log('Banner 广告关闭')
    },

    // 跳转教程1页面
    classroomState: function (params) {
        wx.navigateTo({
          url: './classroomState/classroomState',
        })
    },

    // 跳转教程2页面
    scheduleAbout: function (params) {
        wx.navigateTo({
          url: './scheduleAbout/scheduleAbout',
        })
    },

    // 跳转教程3页面
    collectAbout: function (params) {
        wx.navigateTo({
          url: './collectAbout/collectAbout',
        })
    },

    // 跳转教程4页面
    userAbout: function (params) {
        wx.navigateTo({
          url: './userAbout/userAbout',
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