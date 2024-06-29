# zpy 2024.5.10
import requests
import json
import pandas as pd

def get_page_content(page_num):
    request_url = f'https://www.ihchina.cn/getProject.html?province=&rx_time=&type=&cate=&keywords=&category_id=16&limit=10&p={page_num}'
    headers = {
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.131 Safari/537.36'
    }
    response = requests.get(request_url, headers=headers, timeout=10)
    response.encoding = 'utf-8'
    if response.status_code == 200:
        return response.text
    else:
        return None

# 初始化空的
all_data = pd.DataFrame()

# 页面总数
total_pages = 100

# 每一页
for page_num in range(1, total_pages + 1):
    print(f'从 page {page_num}进行数据抓取')
    json_data = get_page_content(str(page_num))
    if json_data:
        data = json.loads(json_data)
        df = pd.DataFrame(data['list'], columns=['title', 'type', 'province', 'content'])
        all_data = pd.concat([all_data, df], ignore_index=True)
    else:
        print(f"抓取失败，当前是 page {page_num}")

# 保存
excel_path = 'output_data.xlsx'
all_data.to_excel(excel_path, index=False, engine='openpyxl')

print("All data has been successfully saved to the Excel file:", excel_path)


# import pandas as pd
#
# # 读取xlsx文件
# df = pd.read_excel('output_data1.xlsx')
#
# # 打开一个新的txt文件
# with open('outdata.txt', 'w', encoding='utf-8') as f:
#     # 遍历xlsx文件的每一行
#     for index, row in df.iterrows():
#         # 获取第一列和第二列的内容
#         title = row.iloc[0]
#         type = row.iloc[1]
#         province = row.iloc[2]
#         description = row.iloc[3]
#
#         # 写入到txt文件
#         f.write(f'非遗名称：{title}，所属类型：{type}，所属省份：{province}，简介：{description}\n')
