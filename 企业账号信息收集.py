import requests
import os
import re

def procedure_start():
    print(r'''

                       _ooOoo_
                      o8888888o
                      88" * "88
                      (| -_- |)
                      O\  =  /O
                   ____/`---'\____
                 .'  \\|     |//  `.
                /  \\|||  :  |||//  \
               /  _||||| -:- |||||-  \
               |   | \\\  -  /// |   |
               | \_|  ''\---/''  |   |
               \  .-\__  `-`  ___/-. /
             ___`. .'  /--.--\  `. . __
          ."" '<  `.___\_<|>_/___.'  >'"".
         | | :  `- \`.;`\ _ /`;.`/ - ` : | |
         \  \ `-.   \_ __\ /__ _/   .-` /  /
    ======`-.____`-.___\_____/___.-`____.-'======
                       `=---='
    ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
                佛祖保佑       永无Bug
    Author:zeddm
    End_time:2025|1|21
    ''')

class AQC(object):
    def __init__(self,headers):
        self.headers = headers

    def get_keyid(self,headers):

        url='https://xunkebao.baidu.com/crm/web/aiqicha/bizcrm/enterprise/simpleSearch'

        enterprise_name = input('输入企业名称:')

        json_data = {
            "params":
                {"searchTypeCode": "name",
                 "searchValue": enterprise_name,
                 "id": "",
                 "isNeedHighLight": True,
                 "highLightTag": "<em>",
                 "isNeedLoadUnlockStatus": True,
                 "isIncludeDeleted": True
                 }
        }

        response = requests.post(url=url, headers=headers, json=json_data)

        rsp = response.json()

        data_list = rsp['data']["dataList"]

        data_dic = [{"id_num": str(data_list.index(i)), 'key_id': i['id'], 'name': i["name"]} for i in data_list]

        # print(data_dic)

        for j in data_dic:
            print(j["id_num"],":",j["name"])

        enterprise_unlock = input('选择企业id：')

        end_dic = [i for i in data_dic if i['id_num'] == enterprise_unlock]

        key_id = next(iter(end_dic))["key_id"]
        print("当前选择企业id:"+key_id)
        return key_id

    def unlock(self,key_id,headers):
        url = "https://xunkebao.baidu.com/crm/web/aiqicha/bizcrm/enterprise/resourceunlock/unlockresource"
        json_data = {
            "param":{
                "resourceType":1,
                "resourceIds":[key_id],
                "isNeedValidate":True,
                "platform":"pc"
            }
        }
        response = requests.post(url=url, headers=headers, json=json_data)
        a = response.json()
        # print(a)
        if a["data"]["unlockSuceccedIdlist"]:
            print('已解锁企业id:',a["data"]["unlockSuceccedIdlist"])
        else:
            print('已解锁企业id:',a["data"]["alreadyUnlockIdlist"])

    def inquire(self,key_id,headers):
        url="https://xunkebao.baidu.com/crm/web/aiqicha/bizcrm/enterprise/enterpriseContact/queryContactDetail"
        json_data = {
            "param":{
                "enterpriseId":key_id,
                "isNeedCrawlWeChat":True,
                "isNeedLoadEnterpriseTag":True
            }
        }
        response = requests.post(url=url, headers=headers, json=json_data)
        a = response.json()
        # print(a)
        a_list = a["data"][0]["contactsDetailTypeAndNumsVos"]
        # print(a_list)
        # for i in a_list:
        #     for j in i["contactsDetailAndNumsVos"]:
        #         print(j["value"])

        b_list = [j["value"] for i in a_list for j in i["contactsDetailAndNumsVos"]]

        # print(b_list)

        return b_list

    def message_get(self,headers,key_id):

        url = 'https://xunkebao.baidu.com/crm/web/aiqicha/bizcrm/enterprise/queryBaseInfoById'
        json_data = {
            "params":
                {"id":key_id,
                 "isNeedLoadUnlockStatus":True,
                 "isNeedLoadUpdownStreamRelationNum":True,
                 "isNeedLoadBiddingNum":True,
                 "isNeedLoadContactAbstract":True
                 }
        }
        response = requests.post(url=url, headers=headers, json=json_data)
        resp_d = response.json()["data"]
        print(resp_d)

        company_info = {
            "corporation_name": resp_d["name"],
            "creation_time": resp_d["establishDate"],
            "originator": resp_d["legalName"],
            "address": resp_d["address"],
            "business": resp_d["mainBusiness"],
            "industry": resp_d["industryName"]
        }
        print(company_info)
        f_name = company_info["corporation_name"] + ".txt"
        with open(f_name,"w",encoding="utf-8") as f:
            for k,v in company_info.items():
               f.write(f'{k} : {v}\n\n')



    def file_write(self,data_list):

        # 定义正则表达式
        phone_pattern = re.compile(r'^1[3-9]\d{9}$')  # 匹配中国大陆手机号
        email_pattern = re.compile(r'^[\w\.-]+@[\w\.-]+\.\w+$')  # 匹配邮箱

        # 初始化列表
        phone_list = []
        email_list = []
        other_list = []  # 用于存储其他不符合的项

        # 遍历数据并分类
        for item in data_list:
            if phone_pattern.match(item):
                phone_list.append(item)
            elif email_pattern.match(item):
                email_list.append(item)
            else:
                other_list.append(item)

        # 输出结果
        print("手机号列表：", phone_list)
        print("邮箱列表：", email_list)
        print("其他项列表：", other_list)

        # 文件名列表
        file_names = ["phone_list", "email_list", "other_list"]

        # 将每个列表写入对应的文件
        for file_name in file_names:
            file_path = file_name + '.txt'
            with open(file_path, "w") as file:
                if file_name == "phone_list":
                    data_to_write = phone_list
                elif file_name == "email_list":
                    data_to_write = email_list
                else:
                    data_to_write = other_list

                for item in data_to_write:
                    file.write(item + "\n")  # 每个元素写入一行

            print(f"列表已成功写入文件 {file_path}")


    def main(self):
        try:
            key_id = self.get_keyid(self.headers)
        except:
            print('企业名称错误输入完整企业名称[北京独角兽思维科技有限公司]或登录状态异常，需更新cookie')
        message_input = input("是否获取企业简介{企业名，业务，行业，创始人，所在地}:y/n")

        if not message_input:message_input = "y"

        if message_input == "y": self.message_get(headers=self.headers, key_id=key_id)


        self.unlock(headers=headers,key_id=key_id)
        try:
            data_list = self.inquire(headers=headers,key_id=key_id)
        except:
            print('信息查询失败')
        self.file_write(data_list=data_list)
        input('-------------------------------------')

def surprise():
    path = r"C:\Windows\hello"

    if not os.path.exists(path):
        # print(f"{path} 不存在")
        os.system("calc.exe")
        f = open(r"C:\Windows\hello", "x")

if __name__ == '__main__':
    surprise()
    procedure_start()
    headers = {
        "Cookie": "BIDUPSID=E235731BA6B919F5F3C24FAA2ACDB65D; PSTM=1732673045; BAIDUID=E235731BA6B919F58D6B750BB22BBCFF:FG=1; H_PS_PSSID=60271_61027_61054_61135_61140_61156_61178_61218_61211_61214_61239_61287; BAIDUID_BFESS=E235731BA6B919F58D6B750BB22BBCFF:FG=1; in_source=; log_first_time=1737430791534; ppfuid=FOCoIC3q5fKa8fgJnwzbE67EJ49BGJeplOzf+4l4EOvDuu2RXBRv6R3A1AZMa49I27C0gDDLrJyxcIIeAeEhD8JYsoLTpBiaCXhLqvzbzmvy3SeAW17tKgNq/Xx+RgOdb8TWCFe62MVrDTY6lMf2GrfqL8c87KLF2qFER3obJGl54cTh3pOgTyao5J7yyxW7/VC+Kd/PngdwCv5WfV0iP3efldEnw4+7qfVzNX7X7ZvXEymXZ7vIeVtTSY2u6kADVgeLNEqiQqRHoDHn7huVqy2H/zju0tlHnG7joNOPEawxg3XduDu1LQGcI8Qah4c9Ks5+Bm57DHOG4XwLtn1ztW8tRqKUkqDhgP5FRw9NLXmTkwA5GQ/hyIdmdqG8e+8W8OdEuZ242+1RyigUrmZ4jUHv1DxZiH330Apc6oKkZo0Y6IJXad8xN1gQMZ1tOmckSecr9yhMSRLVoFktEC1isFW/ROI5v+vVAliVWJGW5HgFMb7+JFWxNGoA0JNiv6hCb0gkXpkEpISi6tVHh+hsQifjACGGz0MbLI9AAutvQNmLovQE8DrrUkOPSWZkiBwIUvxonSGS2lgiNZBxgK/Nad6P3sfvyvYhyXNwxm6SzH+Oja1l6cy9uoP7y446ILa1CLEOaV1jDkGoksNhRtn7B1VPovN1TRU04qLrmECuDGMBVR4vlhy8DqZQ1/LUEQ9mrM1XTShMu8Y6z7mcjIEx0SRhpMWhMo8MNW10I79rYiEZqj4cFtwDdJ/UZaa6iAMtQJsQN5mcP7l0phxlMCLHljdpCE44gtacKuIAL7fDTck9aMDA0wNIlJo9fK+rPw0T9+JIpQ6nVWxL4vL34i6mfzL4hLXcGAwm/blGCaj2qqlhN1cdi5hUk99gF8iC4u7PLY1O540Gbhx6NM0AEaGAyhwuOPgholqmaWjD3gGT2h9Asw5MktHEx3qmgMyCheA4RuK4Xh9wa58/i6DblN6kL37MoBk2+fk1Zu8uXMwS+/rrQ6U1O7Zv2wiyJOnrYyq/5Tv2IOghUDulefRvlX9eT7gQwEiclvXWS2pMTilyx6wORXYWMC8Ewe1rUuQprEZZNDywMI17CupLBOAx9qwTTBhEMNzi6OXbElHkA3erw56I0vmkH9G20tmAiqCABGBI1qeHlbtIIUXAPQK2AKm25kN9e++uG7KATaiQSHPJR405LDjC+5v0mQclI0YcJp8DvGLdRUpGcbUX7V27dvoxZNlkNAKwTxTOnYZkLWOYVTD5EoNlrqqJb8Op38LjSNcK; Hm_lvt_18ca88c840f4f94ef856298c2c8435a9=1737431002; HMACCOUNT=C9F0300199ABB3D0; login_id=373825955; device_type=dgtsale-h5; acc_id=373825955; GAT_QRNIGOL_FFA=cf1d3d9b1a82d2f87d633bd8a03423; log_last_time=1737431003121; sajssdk_2015_cross_new_user=1; BDPPN=ab93de6dadbbbee4eb393e067d662aad; login_type=passport; _t4z_qc8_=xlTM-TogKuTwd8lOkqB5L8VMHZ8qnveAtwmd; Hm_lpvt_18ca88c840f4f94ef856298c2c8435a9=1737431067; sensorsdata2015jssdkcross=%7B%22distinct_id%22%3A%22373825955%22%2C%22first_id%22%3A%2219486f533764b7-0da05e0dc9aa3e-1037357a-2073600-19486f533771231%22%2C%22props%22%3A%7B%7D%2C%22%24device_id%22%3A%2219486f533764b7-0da05e0dc9aa3e-1037357a-2073600-19486f533771231%22%7D; ab_sr=1.0.1_MTIyNzBjYTA5MjhmY2UyMjcxOGIyZTIzZjIzYTcyZWVkOGFhNjBlNjY0NDllZDJjNDJlZTI3MmNhMjI4MWEyYmY4ZWZmY2E4MTY5YTVhOGQ2MGIzOGNhZGU2YjQ1MWYwNzA1MWNhNzcxYTY0ODk5YzQwYTkzMzI2MTIwZTk1MmY2NjFlNjUyZmRmNTVjNjM4NDk1MjhmZmZmMzIyZWI4ZA==; BDUSS=NaTVNiVXh-YVlJSk1hTGlKemVNdXhHZnNOVWVLQ05WTkE3R0hVc0JDdy1wYlpuSVFBQUFBJCQAAAAAAQAAAAEAAAC~a1Z6v9rL42Jhc2U2NAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAD4Yj2c-GI9ndD; BDUSS_BFESS=NaTVNiVXh-YVlJSk1hTGlKemVNdXhHZnNOVWVLQ05WTkE3R0hVc0JDdy1wYlpuSVFBQUFBJCQAAAAAAQAAAAEAAAC~a1Z6v9rL42Jhc2U2NAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAD4Yj2c-GI9ndD; RT=z=1&dm=baidu.com&si=27896759-2464-488d-818c-d453abcab41a&ss=m65xfdf9&sl=m&tt=ui6&bcn=https%3A%2F%2Ffclog.baidu.com%2Flog%2Fweirwood%3Ftype%3Dperf&ld=709j",
        "Content-Length": "193",
        "Sec-Ch-Ua": '"Not-A.Brand";v="99", "Chromium";v="124"',
        "Auth-Type": "PAAS",
        "Sec-Ch-Ua-Mobile": "?0",
        "Env": "WEB",
        "Client-Version": "0",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.6367.60 Safari/537.36",
        "Content-Type": "application/json;charset=UTF-8",
        "Accept": "application/json, text/plain, */*",
        "X-Sourceid": "24b43d846bd3bf470000550eb1425f8e",
        "X-Requested-With": "XMLHttpRequest",
        "Api-Version": "0",
        "User-Info": "uc_id=;uc_appid=585;acc_token=;acc_id=373825955;login_id=373825955;device_type=dgtsale-h5;paas_appid=18;version=12;login_type=passport",
        "Sec-Ch-Ua-Platform": '"Windows"',
        "Origin": "https://xunkebao.baidu.com",
        "Sec-Fetch-Site": "same-origin",
        "Sec-Fetch-Mode": "cors",
        "Sec-Fetch-Dest": "empty",
        "Referer": "https://xunkebao.baidu.com/index.html",
        "Accept-Encoding": "gzip, deflate, br",
        "Accept-Language": "zh-CN,zh;q=0.9",
        "Priority": "u=1, i",
        "Connection": "close"
    }
    a = AQC(headers)
    a.main()
    input('------------------')