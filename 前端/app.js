// app.js
App({
  onLaunch() {
    this.openid()
  },

  // 全局变量
  globalData: {
    openid: '',
    table: '',  // 规范化后的openid，充当用户文件夹名和数据库名
    day: null,  // 使用天数
    username: '微信用户',   // 用户昵称
    userphotopath: '',  // 用户头像
    bool_schedule: 0,   // 用户是否上传课表
    bool_classroom: 0,  // 用户是否收藏教室
    time_ocr: 3,    // 识别剩余次数
    classroom1: '', // 收藏教室1
    classroom2: '', // 收藏教室2
    classroom3: '', // 收藏教室3
    schedule: null, // 课表内容
    if_change_schedule: 0,  // 课表是否变化
  },

  // 获取openid；判断用户是否建表，否就建表；返回表名
  openid: function (params) {
    wx.login({
        success: (res) => {
            // console.log(res.code); // 先login得到code
            if (res.code) {
                const url = 'https://你的服务器的网址/openid.py?js_code=' + res.code; // 用来获取opendi、table等
                wx.request({
                    url: url,
                    method: 'GET',
                    success: (res) => {
                        console.log(res.data)
                        if (res.data && res.data.openid) {
                            // 在这里处理获取到的openid
                            this.globalData.openid = res.data.openid
                            this.globalData.table = res.data.table  // 用户课表表名称
                            this.globalData.day = res.data.day
                            this.globalData.username = res.data.username
                            this.globalData.bool_schedule = res.data.bool_schedule
                            this.globalData.classroom1 = res.data.star_classroom_1
                            this.globalData.classroom2 = res.data.star_classroom_2
                            this.globalData.classroom3 = res.data.star_classroom_3
                            this.globalData.bool_classroom = res.data.bool_classroom
                            this.globalData.time_ocr = res.data.time_ocr
                            if (res.data.photo) {
                                // 在指定路径下获取用户头像
                                this.globalData.userphotopath = 'https://你的服务器的网址/image/' + this.globalData.table + '/1.png'
                            } else {
                                // 默认头像
                                this.globalData.userphotopath = 'https://mmbiz.qpic.cn/mmbiz/icTdbqWNOwNRna42FI242Lcia07jQodd2FJGIYQfG0LAJGFxM4FbnQP6yfMxBgJ0F3YRqJCJ1aPAK2dQagdusBZg/0'
                            }
                            // console.log('文件夹：', res.data.folder)    // 1：创建成功   0：已经创建   2：未知错误
                            // console.log('头像路径：', this.globalData.userphotopath)
                            // console.log('openid', this.globalData.openid)
                            // console.log('table', this.globalData.table)
                            // console.log('day', this.globalData.day)
                            // console.log('username', this.globalData.username)
                            // console.log('bool_schedule', this.globalData.bool_schedule)
                            // console.log('classroom1', this.globalData.classroom1)
                            // console.log('classroom2', this.globalData.classroom2)
                            // console.log('classroom3', this.globalData.classroom3)
                            // console.log('bool_classroom', this.globalData.bool_classroom)
                            // console.log('time_ocr', this.globalData.time_ocr)
                        } else {
                            console.error('获取OpenID失败');
                        }
                    },
                    fail: function (error) {
                        console.error('请求失败', error);
                    }
                });
            } else {
                console.error('登录失败', res.errMsg);
            }
        },
        fail: function (error) {
            console.error('登录失败', error);
        }
    });
  },
})
