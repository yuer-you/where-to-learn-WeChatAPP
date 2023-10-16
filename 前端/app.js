// app.js
App({
    onLaunch() {
        this.openid()
    },

    // 全局变量
    globalData: {
        // 是否加载完成
        loadingCollect: false,
        loadingToday: false,
        loadingRanking: false,

        // 全部数据
        openid: '',
        table: '',
        day: null,
        username: '微信用户',
        userphotopath: '',
        bool_schedule: 0,
        bool_classroom: 0,
        // 识别剩余次数
        time_ocr: 3,
        classroom1: '',
        classroom2: '',
        classroom3: '',
        // 课表内容
        schedule: null,
        // 课表是否变化
        if_change_schedule: 0,

        // 以下为index函数必用变量
        // 收藏教室
        dayTime: [null, '早一', '早二', '中午', '下一', '下二', '晚一', '晚二'],
        classroomName: null,
        classroomState: null,
        buildingName: null,
        classroomNumber: null,
        // 今日课表
        schedule_today: null,
        name_today: null,
        classdate: ['早一', '早二', '中午', '下一', '下二', '晚一', '晚二'],
        // 大家都爱去
        IndexList: [1,2,3,4,5,6,7,8,9,10],
        classroomRanking: null,
    },

    // 使用回调函数
    setLaunchCallback: function (callback) {
        this.launchCallback = callback;
    },

    // 获取openid；判断用户是否建表，否就建表；返回表名
    openid: function (params) {
        wx.login({
            success: (res) => {
                // console.log(res.code); // 先login得到code
                if (res.code) {
                    const url = 'https://smallapp.easternlake.site/wx/openid.py?js_code=' + res.code; // 用来获取opendi、table
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
                                    this.globalData.userphotopath = 'https://smallapp.easternlake.site/wx/image/' + this.globalData.table + '/1.png'
                                } else {
                                    this.globalData.userphotopath = 'https://mmbiz.qpic.cn/mmbiz/icTdbqWNOwNRna42FI242Lcia07jQodd2FJGIYQfG0LAJGFxM4FbnQP6yfMxBgJ0F3YRqJCJ1aPAK2dQagdusBZg/0'
                                }

                                this.globalData.classroomName =  [
                                    this.globalData.classroom1,
                                    this.globalData.classroom2,
                                    this.globalData.classroom3
                                ]
                                this.globalData.buildingName = [
                                    this.changeBuilding(this.globalData.classroom1),
                                    this.changeBuilding(this.globalData.classroom2),
                                    this.changeBuilding(this.globalData.classroom3)
                                ]
                                this.globalData.classroomNumber = [
                                    this.changeClassNumber(this.globalData.classroom1),
                                    this.changeClassNumber(this.globalData.classroom2),
                                    this.changeClassNumber(this.globalData.classroom3)
                                ]
                                this.index(
                                    this.globalData.if_change_schedule,
                                    this.globalData.bool_classroom,
                                    this.globalData.buildingName,
                                    this.globalData.classroomNumber,

                                    // 能力和时间有限，只能出此下策，等我考完研再来修这个Bug
                                    setTimeout(() => {
                                        this.launchCallback && this.launchCallback()
                                    }, 1500), // 1500 毫秒
                                )

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

    // index页综合函数
    index: function (if_change_schedule, bool_classroom, buildingName, classroomNumber) {
        if (if_change_schedule == 0) {
            this.getScheduleToday()
        }
        if (bool_classroom) {
            this.getClassroomCollect(buildingName, classroomNumber)
        }
        this.getClassroomRanking()
    },

    // 获取收藏教室的教室状态
    getClassroomCollect: function (buildingName, classroomNumber) {
        const buildingName_json = JSON.stringify(buildingName)
        const classroomNumber_json = JSON.stringify(classroomNumber)
        wx.request({
            url: 'https://smallapp.easternlake.site/wx/getClassroomCollect.py',
            data: {
                buildingName: buildingName_json,
                classroomNumber: classroomNumber_json
            },
            method: 'GET',
            success: (res) => {
                if (res.data.classroomState) {
                    this.globalData.classroomState = res.data.classroomState
                    this.globalData.name_today = res.data.today_name
                    this.changeDay()    // 更改命名方式
                }
                console.log('教室状态', this.globalData.classroomState)
            }
        })
    },

    // 获取今日课表
    getScheduleToday: function () {
        wx.request({
            url: 'https://smallapp.easternlake.site/wx/getScheduleToday.py?table=' + this.globalData.table,
            method: 'GET',
            success: (res) => {
                if (res.data.today_schedule) {
                    this.globalData.schedule_today = res.data.today_schedule
                    this.globalData.name_today = res.data.today_name
                    this.changeDay()    // 更改命名方式
                    console.log('今日课表', this.globalData.schedule_today)
                    // console.log('星期', this.data.name_today)
                }
            }
        })
    },

    // 获取教室排名
    getClassroomRanking: function () {
        wx.request({
            url: 'https://smallapp.easternlake.site/wx/getClassroomRanking.py',
            method: 'GET',
            success: (res) => {
                if (res.data.classroomRanking) {
                    this.globalData.classroomRanking = res.data.classroomRanking
                    console.log('教室排名', this.globalData.classroomRanking)
                }
            }
        })
    },

    // 中文命名星期
    changeDay: function () {
        switch (this.globalData.name_today) {
            case 0:
                this.globalData.name_today = '星期一'
                break
            case 1:
                this.globalData.name_today = '星期二'
                break
            case 2:
                this.globalData.name_today = '星期三'
                break
            case 3:
                this.globalData.name_today = '星期四'
                break
            case 4:
                this.globalData.name_today = '星期五'
                break
            case 5:
                this.globalData.name_today = '星期六'
                break
            case 6:
                this.globalData.name_today = '星期日'
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
                else return false
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
    }
})
