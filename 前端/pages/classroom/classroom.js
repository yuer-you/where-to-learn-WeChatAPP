// pages/classroom/classroom.js
import { formatTime } from "../../utils/util"

// classroom全局变量：whichIndex为classroom的数组序号，whichDate为日期。（方便后面编程，可以删除）
var whichIndex
var whichDate

Page({
    /**
     * 页面的初始数据
     */
    data: {
        // 教室选择
        array: ['思源楼', '思源西楼', '思源东楼', '逸夫楼', '机械楼', '九教', '东区一教', '十七教（建艺）', '八教'],
        array_submit: ['sy', 'sx', 'sd', 'yf', 'z', 'nine', 'dq', 'art', 'eight'],
        index: 0,

        // 获取当前日期
        currentDate: formatTime(new Date()),

        // 教室状态
        state: null,
        classroom: [
            ['SY101', 'SY102', 'SY103', 'SY104', 'SY105', 'SY106', 'SY107', 'SY108', 'SY109', 'SY201', 'SY202', 'SY203', 'SY204', 'SY205', 'SY206', 'SY207', 'SY208', 'SY209', 'SY210', 'SY301', 'SY302', 'SY303', 'SY305', 'SY306', 'SY307', 'SY308', 'SY309', 'SY401', 'SY402', 'SY403', 'SY405', 'SY406', 'SY407', 'SY408', 'SY410', 'SY411', 'SY412'],
            ['SX101', 'SX105', 'SX106', 'SX107', 'SX201', 'SX202', 'SX203', 'SX204', 'SX205', 'SX302', 'SX303', 'SX304', 'SX305', 'SX401', 'SX402', 'SX403', 'SX404', 'SX405', 'SX406', 'SX407', 'SX501', 'SX502', 'SX503', 'SX504', 'SX505', 'SX506', 'SX507'],
            ['SD102', 'SD103', 'SD104', 'SD106', 'SD107', 'SD108', 'SD201', 'SD202', 'SD203', 'SD205', 'SD206', 'SD207'],
            ['YF104', 'YF106', 'YF108', 'YF204', 'YF205', 'YF207', 'YF208', 'YF209', 'YF301', 'YF302', 'YF303', 'YF304', 'YF305', 'YF307', 'YF308', 'YF309', 'YF310', 'YF312', 'YF313', 'YF401', 'YF403', 'YF404', 'YF406', 'YF408', 'YF409', 'YF410', 'YF411', 'YF413', 'YF414', 'YF415', 'YF501', 'YF503', 'YF504', 'YF505', 'YF507', 'YF508', 'YF509', 'YF510', 'YF512', 'YF513', 'YF514', 'YF601', 'YF603', 'YF604', 'YF606', 'YF608', 'YF609', 'YF610', 'YF611', 'YF613', 'YF614', 'YF615', 'YF东701', 'YF东702', 'YF东703', 'YF东705', 'YF东706'],
            ['Z101', 'Z104', 'Z105', 'Z106', 'Z107', 'Z108', 'Z109', 'Z201', 'Z204', 'Z207', 'Z305', 'Z306', 'Z307', 'Z308', 'Z309', 'Z310'],
            ['九教东102', '九教201', '九教203', '九教中102'],
            ['DQ102', 'DQ103', 'DQ104', 'DQ105', 'DQ106', 'DQ107', 'DQ108', 'DQ110', 'DQ202', 'DQ203', 'DQ204', 'DQ205', 'DQ206', 'DQ208', 'DQ209', 'DQ210', 'DQ212', 'DQ213', 'DQ214', 'DQ215', 'DQ216', 'DQ302', 'DQ303', 'DQ304', 'DQ305', 'DQ306', 'DQ308', 'DQ309', 'DQ310', 'DQ311', 'DQ312', 'DQ313', 'DQ314', 'DQ402', 'DQ403', 'DQ404', 'DQ405', 'DQ406', 'DQ408', 'DQ409', 'DQ410', 'DQ412', 'DQ413', 'DQ414', 'DQ415', 'DQ505', 'DQ510'],
            ['建艺202', '建艺203', '建艺204', '建艺205', '建艺206', '建艺207', '建艺208', '建艺209', '建艺211'],
            ['8103', '8104', '8105', '8108', '8109', '8201', '8202', '8203', '8204', '8205', '8207', '8208']
        ]
    },

    /**
     * 生命周期函数--监听页面加载
     */
    onLoad: function (options) {
        whichIndex=this.data.index
        whichDate=this.data.currentDate
    },

    // 教学楼选择器
    bindPickerChange: function(e) {
        whichIndex=e.detail.value
        this.setData({
          index: e.detail.value,
        })
    },

    // 时间选择器
    bindDateChange: function(e) {
        // console.log('选择日期', e.detail.value)
        whichDate=e.detail.value
        this.setData({
            currentDate: e.detail.value
        })
    },

    // 格式化时间 2023-03-03 --> 2023.3.3
    removeLeadingZerosFromDate: function(dateString) {
        function removeLeadingZero(part) {
            if (part.startsWith("0") && part.length > 1) {
                return part.substring(1);
            }
            return part;
        }
        dateString = dateString.replace(/-/g, '.')
        const parts = dateString.split('.');
        const cleanedParts = parts.map(part => removeLeadingZero(part));
        return cleanedParts.join('.');
    },

    // 获取教室状态
    search: function(building, data) {
        wx.showLoading({
            title: '查询中...',
        })
        wx.request({
            url: 'https://你的服务器网址/gcs.py?building=' + building + '&data=' + data,
            method: 'GET',
            success: (res) => {
                this.setData({state: null})
                // 我也忘了这个if else是干嘛的了...
                if (res.data.length) {
                    this.setData({state: res.data})
                } else {
                    let empty = []
                    for (var i = 0; i < this.data.classroom[whichIndex].length; i++) {
                        empty[i] = []
                    }
                    for (var i = 0; i < this.data.classroom[whichIndex].length; i++) {
                        for (var j = 0; j < 7; j++) {
                            empty[i][j] = 2
                        }
                    }
                    this.setData({
                        state: empty
                    })
                }
                console.log("state：", this.data.state)
            },
            complete: function (params) {
                wx.hideLoading();
            }
        })
    },

    // 表单提交
    formSubmit(e) {
        this.setData({whichIndex: this.data.index})
        // 本想使用dataform向后端传递数据，但是最终还是分别传输，所以这里的dataform没有用，可以删除
        var dataForm={};
        dataForm.date=this.removeLeadingZerosFromDate(whichDate)
        dataForm.building=this.data.array_submit[whichIndex]
        console.log(dataForm.building, dataForm.date)
        this.search(dataForm.building, dataForm.date)
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