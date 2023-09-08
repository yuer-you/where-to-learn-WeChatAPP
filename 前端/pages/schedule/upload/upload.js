// pages/schedule/upload/upload.js
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
        openid: null,
        table: '',

        // hidden参数
        imageLoad: false,
        readRequest: true,
        serverLoad: true,

        // 图片本地路径
        photoPath: '',
        time_ocr: null,
    },

    /**
     * 组件的方法列表
     */
    methods: {
        // 图片要求
        photoRequest: function () {
            wx.showModal({
                title: '图片要求',
                content: '我们只接受PC端（电脑）mis系统内课表的“全屏”截图，若为拍屏或课表不完整，则无法识别。每人每天可识别3次，识别一次大约需要20~30s\n\n教程\n\n一、打开“mis”网站 → 打开“教务系统”页面 → 打开“本学期课表”页面\n\n二、将页面缩放（缩放快捷键(Windows)：Ctrl + 鼠标滚轮）至不用滚动页面即可完全展示的程度。\n\n三、使用微信截图（Alt + A）或系统自带截图功能，全屏截图，后将截图通过微信发送至手机，并将其保存至手机。\n\n四、点击“选择图片上传”按钮，选择上传刚刚保存的图片',
                showCancel: false,
                complete: (res) => {            
                    if (res.confirm) {
                        this.setData({readRequest: false})
                    }
                }
            })
        },

        // 选择图片并展示并上传
        photoUpload: function () {
            wx.chooseMedia({
                count: 1,
                mediaType: ['image'],
                sourceType: ['album'],
                sizeType: ['original'],
                success: (res) => {
                    this.setData({
                        photoPath: res.tempFiles[0].tempFilePath,
                        serverLoad: false,
                        imageLoad: true,
                        openid: app.globalData.openid,
                        table: app.globalData.table,
                        time_ocr: app.globalData.time_ocr
                    })
                    // console.log(this.data.photoPath)
                    // 上传服务器
                    wx.showLoading({
                        title: '上传中...',
                    })
                    wx.uploadFile({
                        filePath: this.data.photoPath,
                        name: 'image',
                        formData: {
                            'openid': this.data.openid,
                            'photoname': 'schedule'
                        },
                        url: 'https://你的服务器网址/downLoadPhoto.py',
                        success: (res) => {
                            console.log('上传成功：',res.data)
                        },
                        fail: (res) => {
                            console.log('上传失败：',res.statusCode)
                        },
                        complete: function (params) {
                            wx.hideLoading();
                        }
                    })
                }
            })
        },

        // 识别、返回结果
        photoOCR: function () {
            if (this.data.time_ocr > 0) {
                wx.showLoading({
                    title: '识别中...',
                })
                wx.request({
                    url: 'https://你的服务器网址/ocr.py?table=' + this.data.table,
                    method: 'GET',
                    success: (res) => {
                        // console.log(res.data)
                        if (res.data.success) {
                            // 识别次数-1
                            wx.request({
                                url: 'https://你的服务器网址/time_ocr&bool_schedule.py?openid=' + this.data.openid,
                                method: 'GET',
                                success: (res) => {
                                    if (res.data.time_ocr_success && res.data.bool_schedule_success) {
                                        this.setData({time_ocr: this.data.time_ocr - 1})
                                        app.globalData.bool_schedule = 1
                                        app.globalData.if_change_schedule = 1
                                    }
                                    wx.showToast({
                                        title: '识别成功',
                                        icon: 'success',
                                        duration: 2000
                                    })
                                    console.log('识别成功')
                                }
                            })
                        } else if (res.data.error) {
                            wx.showToast({
                                title: '识别错误',
                                icon: 'error',
                                duration: 2000
                            })
                            console.log('识别错误')
                        } else {
                            wx.showModal({
                                title: '图片格式错误',
                                content: '请通过电脑截取课表页面',
                                showCancel: false,
                            })
                            console.log('格式错误')
                        }
                        console.log(res)
                    },
                    complete: function (params) {
                        wx.hideLoading();
                    }
                })
            } else {
                wx.showModal({
                    title: '',
                    content: '今日识别次数已用完',
                    showCancel: false,
                })
            }
            
        }
    }
})
