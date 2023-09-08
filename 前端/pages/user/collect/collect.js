// pages/collect/collect.js
// 本部分的核心因为是抄的，所以直接重复三遍，没有经过修改

const app = getApp()
Page({

    /**
     * 页面的初始数据
     */
    data: {
        openid: null,
        // 一级
        multiArray1: [['无', '思源楼', '思源西楼', '思源东楼', '逸夫楼', '机械楼', '九教', '东区一教', '十七教（建艺）', '八教（装修中）'], []],
        multiArray2: [['无', '思源楼', '思源西楼', '思源东楼', '逸夫楼', '机械楼', '九教', '东区一教', '十七教（建艺）', '八教（装修中）'], []],
        multiArray3: [['无', '思源楼', '思源西楼', '思源东楼', '逸夫楼', '机械楼', '九教', '东区一教', '十七教（建艺）', '八教（装修中）'], []],
        multiIndex1: [0, 0],
        multiIndex2: [0, 0],
        multiIndex3: [0, 0],

        // 二级
        buildingData: [
            ['无'],
            ['SY101', 'SY102', 'SY103', 'SY104', 'SY105', 'SY106', 'SY107', 'SY108', 'SY109', 'SY201', 'SY202', 'SY203', 'SY204', 'SY205', 'SY206', 'SY207', 'SY208', 'SY209', 'SY210', 'SY301', 'SY302', 'SY303', 'SY304', 'SY305', 'SY306', 'SY307', 'SY308', 'SY309', 'SY401', 'SY402', 'SY403', 'SY404', 'SY405', 'SY406', 'SY407', 'SY408', 'SY409', 'SY410', 'SY411', 'SY412'],
            ['SX101', 'SX105', 'SX106', 'SX107', 'SX201', 'SX202', 'SX203', 'SX204', 'SX205', 'SX302', 'SX303', 'SX304', 'SX305', 'SX401', 'SX402', 'SX403', 'SX404', 'SX405', 'SX406', 'SX407', 'SX501', 'SX502', 'SX503', 'SX504', 'SX505', 'SX506', 'SX507'],
            ['SD102', 'SD103', 'SD104', 'SD106', 'SD107', 'SD108', 'SD201', 'SD202', 'SD203', 'SD205', 'SD206', 'SD207'],
            ['YF104', 'YF106', 'YF108', 'YF204', 'YF205', 'YF207', 'YF208', 'YF209', 'YF301', 'YF302', 'YF303', 'YF304', 'YF305', 'YF307', 'YF308', 'YF309', 'YF310', 'YF312', 'YF313', 'YF401', 'YF403', 'YF404', 'YF406', 'YF408', 'YF409', 'YF410', 'YF411', 'YF413', 'YF414', 'YF415', 'YF501', 'YF503', 'YF504', 'YF505', 'YF507', 'YF508', 'YF509', 'YF510', 'YF512', 'YF513', 'YF514', 'YF601', 'YF603', 'YF604', 'YF606', 'YF608', 'YF609', 'YF610', 'YF611', 'YF613', 'YF614', 'YF615', 'YF东701', 'YF东702', 'YF东703', 'YF东705', 'YF东706'],
            ['Z101', 'Z104', 'Z105', 'Z106', 'Z107', 'Z108', 'Z109', 'Z201', 'Z204', 'Z207', 'Z305', 'Z306', 'Z307', 'Z308', 'Z309', 'Z310'],
            ['九教东102', '九教201', '九教203', '九教中102'],
            ['DQ102', 'DQ103', 'DQ104', 'DQ105', 'DQ106', 'DQ107', 'DQ108', 'DQ110', 'DQ202', 'DQ203', 'DQ204', 'DQ205', 'DQ206', 'DQ208', 'DQ209', 'DQ210', 'DQ212', 'DQ213', 'DQ214', 'DQ215', 'DQ216', 'DQ302', 'DQ303', 'DQ304', 'DQ305', 'DQ306', 'DQ308', 'DQ309', 'DQ310', 'DQ311', 'DQ312', 'DQ313', 'DQ314', 'DQ402', 'DQ403', 'DQ404', 'DQ405', 'DQ406', 'DQ408', 'DQ409', 'DQ410', 'DQ412', 'DQ413', 'DQ414', 'DQ415', 'DQ505', 'DQ510'],
            ['建艺202', '建艺203', '建艺204', '建艺205', '建艺206', '建艺207', '建艺208', '建艺209', '建艺211'],
            ['8103', '8104', '8105', '8108', '8109', '8201', '8202', '8203', '8204', '8205', '8207', '8208']
        ],
        old_classroom: null,
    },

    /**
     * 生命周期函数--监听页面加载
     */
    onLoad() {
        const selectedBuilding = this.data.buildingData[0];
        const multiArray1 = this.data.multiArray1;
        multiArray1[1] = selectedBuilding;
        const multiArray2 = this.data.multiArray2;
        multiArray2[1] = selectedBuilding;
        const multiArray3 = this.data.multiArray3;
        multiArray3[1] = selectedBuilding;
        this.setData({
            multiArray1: multiArray1,
            multiArray2: multiArray2,
            multiArray3: multiArray3,
            openid: app.globalData.openid,
            old_classroom: [
                this.no_empty(app.globalData.classroom1),
                this.no_empty(app.globalData.classroom2),
                this.no_empty(app.globalData.classroom3)
            ]
        });
    },

    // input1
    bindMultiPickerChange1: function (e) {
        this.setData({
            multiIndex1: e.detail.value,
        });
        console.log(this.data.multiIndex1)
    },
    bindMultiPickerColumnChange1: function (e) {
        const column = e.detail.column;
        const valueIndex = e.detail.value;
    
        if (column === 0) {
            const selectedBuilding = this.data.buildingData[valueIndex];
            const multiArray = this.data.multiArray1;
            multiArray[1] = selectedBuilding;
    
            this.setData({
                multiArray1: multiArray
            });
        }
    },
    delete1: function () {
        const initialIndex = [0, 0]; // 设置初始索引
        const initialBuildingData = this.data.buildingData[0]; // 设置初始第二列数据
        const multiArray = this.data.multiArray1;
        multiArray[1] = initialBuildingData;

        this.setData({
            multiIndex1: initialIndex,
            multiArray1: multiArray
        });
    },

    // input2
    bindMultiPickerChange2: function (e) {
        this.setData({
            multiIndex2: e.detail.value,
        });
        console.log(this.data.multiIndex2)
    },
    bindMultiPickerColumnChange2: function (e) {
        const column = e.detail.column;
        const valueIndex = e.detail.value;
    
        if (column === 0) {
            const selectedBuilding = this.data.buildingData[valueIndex];
            const multiArray = this.data.multiArray2;
            multiArray[1] = selectedBuilding;
    
            this.setData({
                multiArray2: multiArray
            });
        }
    },
    delete2: function () {
        const initialIndex = [0, 0]; // 设置初始索引
        const initialBuildingData = this.data.buildingData[0]; // 设置初始第二列数据
        const multiArray = this.data.multiArray2;
        multiArray[1] = initialBuildingData;

        this.setData({
            multiIndex2: initialIndex,
            multiArray2: multiArray
        });
    },

    // input3
    bindMultiPickerChange3: function (e) {
        this.setData({
            multiIndex3: e.detail.value,
        });
        console.log(this.data.multiIndex3)
    },
    bindMultiPickerColumnChange3: function (e) {
        const column = e.detail.column;
        const valueIndex = e.detail.value;
    
        if (column === 0) {
            const selectedBuilding = this.data.buildingData[valueIndex];
            const multiArray = this.data.multiArray3;
            multiArray[1] = selectedBuilding;
    
            this.setData({
                multiArray3: multiArray
            });
        }
    },
    delete3: function () {
        const initialIndex = [0, 0]; // 设置初始索引
        const initialBuildingData = this.data.buildingData[0]; // 设置初始第二列数据
        const multiArray = this.data.multiArray3;
        multiArray[1] = initialBuildingData;

        this.setData({
            multiIndex3: initialIndex,
            multiArray3: multiArray
        });
    },

    // 提交修改
    changeClass: function (change_classroom, history_classroom) {
        const change_classroom_json = JSON.stringify(change_classroom);
        const history_classroom_json = JSON.stringify(history_classroom);
        wx.showLoading({
            title: '修改中...',
        })
        wx.request({
            url: 'https://你的服务器网址/changeClassroom.py',
            data: {
                openid: this.data.openid,
                change_classroom: change_classroom_json,
                history_classroom: history_classroom_json
            },
            method: 'GET',
            success: (res) => {
                if(res.data.update_users_classroom_success && res.data.update_all_classroom_success && res.data.update_bool_classroom_success) {
                    wx.showToast({
                        title: '修改成功',
                        icon: 'success',
                        duration: 2000
                    })
                    app.globalData.classroom1 = change_classroom[0]
                    app.globalData.classroom2 = change_classroom[1]
                    app.globalData.classroom3 = change_classroom[2]
                    if (change_classroom[0] || change_classroom[1] || change_classroom[2]) {
                        app.globalData.bool_classroom = 1
                    } else {
                        app.globalData.bool_classroom = 0
                    }
                    console.log('修改成功：', res.data.message)
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

    // 修改提交内容
    if_empty: function (class_value) {
        if (class_value == '无') {
            class_value = null
        }
        return class_value
    },

    // 修改提交内容
    no_empty: function (class_value) {
        if (class_value == null) {
            return '无'
        } else {
            return class_value
        }
    },
    
    // 表单提交
    formSubmit() {
        const classroom1 = this.if_empty(this.data.multiArray1[1][this.data.multiIndex1[1]])
        const classroom2 = this.if_empty(this.data.multiArray2[1][this.data.multiIndex2[1]])
        const classroom3 = this.if_empty(this.data.multiArray3[1][this.data.multiIndex3[1]])
        const change_classroom = [classroom1, classroom2, classroom3]
        const history_classroom = [app.globalData.classroom1, app.globalData.classroom2, app.globalData.classroom3]
        var change = 0
        for (let i = 0; i < 3; i++) {
            if (change_classroom[i] !== history_classroom[i]) {
                change = 1
            }
          }
        if (change) {
            this.changeClass(change_classroom, history_classroom)
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
        this.setData({
            old_classroom: [
                this.no_empty(app.globalData.classroom1),
                this.no_empty(app.globalData.classroom2),
                this.no_empty(app.globalData.classroom3)
            ]
        });
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