# 每日健康打卡

## 注意事项

* 请遵守公司相关规定，注意保护公司和个人信息。使用本程序导致的一切后果由使用者自行自担。
* 本程序不对提交内容做任何检查，无法处理表单项目之间的依赖关系，请根据表单页面实际情况正确填写。

## 本地运行 / 测试

1. 运行 `./template.py 'https://example.com/form-url' >answer.txt` 生成应答模版
2. 编辑应答文件 `answer.txt` 的内容
3. 运行 `./checkin.py answer.txt` 进行打卡

## 每日自动打卡

1. 在本地完成打卡测试
2. 上传应答文件（例如以应答文件的内容新建 Private Gist）
3. fork 本项目并添加 `ANSWER_URL` secret，填入应答文件网址
4. 观察 GitHub Actions 运行情况（push 触发 / cron 触发，北京时间每天早上 08:30）
5. 如果收到 Actions 运行失败的通知，请及时生成新的应答模版并更新应答文件

## 应答文件格式

* 前三行分别为表单 URL、表单 UUID、schema 版本号，请不要修改。
* 后续为表单内容，每行由表单项目标识符和 raw JSON 格式的值组成。空行、以 `#` 开头的行会被忽略。请根据需要去除 `#` 并填写表单内容。

### 特殊字段类型

* DateField 值为 [UNIX 时间戳（单位：毫秒）](https://tool.chinaz.com/tools/unixtime.aspx)
* 数据源自独立 DataSource 的 SelectField / CascadeSelectField，在应答模版中没有给出可能的取值，请自行抓包
* CitySelectField，在应答模版中只给出了“北京/北京市”对应值，其它地区可以自行抓包或参考 [js](https://gist.github.com/zhangyoufu/12a0d8a52e4035e4fb99993aa8ce5d97)
* AttachmentField 暂不支持

## 应答文件样例

```
https://example.com/form-url
FORM-ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789
version 123

# 生态公司
selectField_k5szl4ww "北京涨停科技有限公司"

# 姓名
textField_k5s487t3 "张三"

# 工号
textField_k5s4dbuk "12345"

# 手机号
textField_k5s487t5 "13812345678"

# 所在部门
textField_k5s4dbum "没有部门"

# ● 目前健康状况
radioField_k5rn1jqa "健康"

# 接触的人中是否有疑似症状？（冠状病毒检测结果为阳性或尚在等待检测结果或在等待冠状病毒检测中）
radioField_k5rs02y5 "否"

# ● 目前所在城市
citySelectField_k5rn1jq3 ["310000", "310100"]

# ● 过去14天是否在湖北省停留（包含转机转车路过）
radioField_k5rvbnyu "否"

# ● 过去14天是否有接待过来自湖北的客户、亲友及其他
radioField_k5tt2wz2 "否"

# ● 过去14天是否在韩国、日本、意大利、浙江温州或台州停留（包含转机转车路过）
radioField_k635ql6m "否"

# ● 过去14天是否有接待过来自韩国、日本、意大利、浙江温州或台州的客户、亲友及其他（如果是共同居住的亲友，共同居住日期已经满14天且一切健康，请选择"否"）
radioField_k635ql6o "否"

# ● 是否已返回或从未离开工作园区所在城市
radioField_k65z096r "14天内从未离开"

# ● 过去14天是否有共同居住者（家属或合租者）从其他城市返回情况
radioField_k6abcmjk "否"
```

## TODO

* 表单项模糊匹配，跨版本兼容
* 非公开表单
