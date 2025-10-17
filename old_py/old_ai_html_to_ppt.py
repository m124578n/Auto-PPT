# AI 驅動的 HTML → PPTX 生成器
# 流程：內容分析 → 生成 HTML → 瀏覽器預覽 → 轉換 PPTX

import base64
import json
import os
from pathlib import Path
from typing import Any, Dict, List

from dotenv import load_dotenv
from google import genai
from google.genai import types

load_dotenv()
# ==================== 配置 ====================
API_KEY = os.getenv("GEMINI_API_KEY")

# 文字內容
TEXT_CONTENT = """
APP獨享！日本黑部立山絕景
輸碼【Hokuriku1000】現折1千
開啟
不操作ATM、不提供任何資料、不回撥可疑電話。如接獲可疑來電，請立即掛斷電話，並撥打165防詐騙專線。
查看詳情
預防詐騙聲明啟事
關閉
Close Icon
Liontravel Logo
Global Icon
繁體中文
TWD
下載APP
企業專區
同業登入
我的訂單
Arrow Down Icon
會員訂單查詢
訪客訂單查詢
折扣碼管理
我的收藏
我的評論
常用旅客名單
會員帳號管理
會員服務
旅客滿意度
會員登入
國外團
國外旅遊
日本
韓國
中國大陸
香港/澳門
泰國
馬來西亞/新加坡
越南
印尼
菲律賓
吳哥窟
澳洲
紐西蘭
中亞/南亞
中東
非洲
美國
加拿大
中南美/南極
關島/帛琉
中西歐
東歐/巴爾幹半島
南/北歐
主題旅遊
璽品旅遊
郵輪旅遊
台灣團
台灣旅遊
北基宜
桃竹苗
中彰投
雲嘉南
高屏
小琉球
花東
綠島｜蘭嶼
澎金馬
環島
大人囝仔聚樂部
離島假期
鐵道旅遊
大人囝仔聚樂部
天天出發
山林旅遊
天天出發
迷你團小車旅遊
山林旅遊
主題遊
國外主題
璽品旅遊
郵輪旅遊
國外鐵道
山林旅遊
運動旅遊
海島旅遊
ClubMed
高爾夫
單車
冒險
節慶
美食
建築
馬拉松
攝影
登山健行
藝術
生態
人文遺產
親子旅遊
達人
滑雪
九州七星
中南美洲
南極
島嶼玩家
台灣主題
台灣鐵道
山林旅遊
特殊體驗
原民旅遊
司馬庫斯｜不老部落｜武界部落｜新光部落｜更多部落
山林旅遊
森林遊樂區｜百岳登山｜步道健行
農業旅遊
茶｜米｜花｜果｜蔬｜酒｜漁
更多體驗
建築｜攝影｜美食｜Club Med
更多體驗
小孩放電趣｜冬/夏令營｜網美養成計畫｜閨蜜饗渡假｜毛孩趴趴走｜銀髮樂活
鐵道旅遊
鳴日號｜藍皮解憂號｜阿里山火車｜兩鐵｜台鐵｜高鐵
郵輪旅遊
世界郵輪
運動休閒
單車｜馬拉松｜露營｜水上活動
客製小包團
自由行
高鐵假期
國外自由行
香港自由行
台灣自由行
高鐵假期
機票
訂房
國外訂房
台灣訂房
票券
簽證
各地出發(不顯示)
中部出發
國外旅遊
台灣旅遊
桃竹苗
中彰投
雲嘉南
高屏.小琉球
花東.綠島
離島
環島
北基宜
南部出發
國外旅遊
台灣旅遊
桃竹苗
中彰投
雲嘉南
高屏.小琉球
花東.綠島
離島
環島
北基宜
赴台旅遊
中文
English
日本語
한국어
中部出發(不顯示)
台灣
北基宜
桃竹苗
中彰投
雲嘉南
高屏.小琉球
花東.綠島
離島
環島
南部出發(不顯示)
台灣
北基宜
桃竹苗
中彰投
雲嘉南
高屏.小琉球
花東.綠島
離島
環島
台灣郵輪
團體旅遊(不顯示)
雄獅璽品
精緻旅程
4-10人
經典旅程
10-16人
奧捷
德瑞
法國
義大利
葡萄牙
克羅埃西亞
東南亞
國外團體旅遊
重磅回歸
日本
峇里島
中南美洲 . 南極
(秘魯 | 玻利維亞 | 智利 | 阿根廷| 巴西 | 古巴 | 墨西哥)
日本嚴選
越南/緬甸
中西歐
(英國 | 法國 | 荷比盧 | 德國 | 瑞士 | 奧地利)
韓國
菲律賓
南北歐
(西班牙 | 葡萄牙 | 希臘 | 義大利 | 挪威 | 冰島 | 芬蘭)
韓國嚴選
吳哥窟
東歐 . 俄羅斯
(捷克 | 匈牙利 | 波蘭 | 克羅埃西亞 | 俄羅斯 | 波羅的海)
大陸港澳
美國
中東
(土耳其 | 杜拜 | 伊朗 | 以色列 | 約旦)
泰國
加拿大
中南亞
(印度 | 尼泊爾 | 斯里蘭卡 | 不丹 | 中亞五國)
馬來西亞
澳洲
非洲
(埃及｜摩洛哥｜南非｜突尼西亞｜肯亞｜模里西斯)
新加坡
紐西蘭
太平洋小島
(關島 | 帛琉 | 馬爾地夫 | 大溪地)
台灣團體旅遊
北基宜
桃竹苗
中彰投
雲嘉南
高雄屏東
花東
離島
環島
大人囝仔
天天出發
迷你團小車旅遊
國外團體(備份)
台灣團體（備份
台灣旅遊
北基宜
澎金馬
桃竹苗
環島
中彰投
雲嘉南
高屏
小琉球
花東
綠島｜蘭嶼
大人囝仔聚樂部
天天出發
迷你團小車旅遊
各地出發(備份)
中部出發
國外旅遊
台灣旅遊
南部出發
國外旅遊
台灣旅遊
台中出發
國外旅遊
台灣旅遊
高雄出發
國外旅遊
台灣旅遊
省最大北陸旅遊｜立山雪壁絕景x粉紅芝櫻花毯！合掌村.兼六園.打卡秘境～奈良井宿.犬山城.信州牛壽喜燒.福朋喜來登溫泉六日
搜尋
團體旅遊
出發地
不限
關鍵字
出發區間
只找成行
只找可報名
搜尋
熱門搜尋
連假旅遊預定
關鍵字搜尋
目的地搜尋
雄獅首頁
國外團體
省最大北陸旅遊｜立山雪壁絕景x粉紅芝櫻花毯！合掌村.兼六園.打卡秘境～奈良井宿.犬山城.信州牛壽喜燒.福朋喜來登溫泉六日
出發地
不限
國外旅遊
台北
松山/桃園機場
台中
台南
高雄
台灣旅遊
不限
北北基
桃竹苗
中彰投
雲嘉南
高屏
宜花東
關鍵字
出發區間
只找成行
本公司「成行」之旅遊產品，係指報名參加人數已達出發標準，但產品出發前若遇有以下情事，將依旅遊定型化契約書取消： 一、不可抗力、不可歸責於雙方當事人之事由，如颱 風、海嘯、地震、洪災等不可抗力之天然災害；或罷工、戰亂抗爭、官方封閉旅遊地區、重大疫情等不可歸責之人為因素。 二、「成行」之旅遊產品所遊覽地區或國家，經外交部領事事務局或交通部觀光局或其他官方單位列為橙色警示、或紅色警示。
只找可報名
熱門搜尋
連假旅遊預定
關鍵字搜尋
目的地搜尋
比較
收藏
省最大北陸旅遊｜立山雪壁絕景x粉紅芝櫻花毯！合掌村.兼六園.打卡秘境～奈良井宿.犬山城.信州牛壽喜燒.福朋喜來登溫泉六日
溫泉飯店
特色料理
花季
櫻花季
行程1
產品代碼
25JP512CI-T
成行
本公司「已成行」之旅遊團體，係指報名參加人數已達出發標準，但團體出發前若遇有以下情事，將依定型化契約書取消出發：
一、不可抗力、不可歸責於雙方當事人之事由，如颱風、海嘯、地震、洪災等不可抗力之天然災害；或罷工、戰亂抗爭、官方封閉旅遊地區、重大疫情等不可歸責之人為因素。
二、「已成行」之旅遊團體所遊覽地區或國家，經外交部領事事務局或交通部觀光局或其他官方單位列為橙色警示、或紅色警示。
可賣
席次
28
去程
2025/05/12 (一)
共6天
回程
2025/05/17 (六)
刷卡好康
TWD 47,900
人/起
選擇出發日期
費用說明
報名
列表顯示
選擇出發日期
2025年5月
只找成行
出發日期
行程
成行狀態
可賣
席次
價格
2025/05/12 (一)
成行
報名
席次
28
TWD 47,900
出發日期
行程
成行狀態
可賣
席次
價格
2025/05/14 (三)
報名
17
席次
28
TWD 46,900
出發日期
行程
成行狀態
可賣
席次
價格
2025/05/15 (四)
報名
17
席次
28
TWD 47,900
出發日期
行程
成行狀態
可賣
席次
價格
2025/05/17 (六)
報名
17
席次
28
TWD 47,900
出發日期
行程
成行狀態
可賣
席次
價格
2025/05/18 (日)
成行
候補
席次
28
TWD 45,900
出發日期
行程
成行狀態
可賣
席次
價格
2025/05/19 (一)
成行
報名
席次
30
TWD 43,900
出發日期
行程
成行狀態
可賣
席次
價格
2025/05/21 (三)
成行
報名
席次
37
TWD 45,900
出發日期
行程
成行狀態
可賣
席次
價格
2025/05/26 (一)
成行
報名
12
席次
28
TWD 45,900
出發日期
行程
成行狀態
可賣
席次
價格
2025/05/31 (六)
成行
報名
10
席次
28
TWD 44,900
只找成行
2025年
5月
10
11
12
成行
47,900+
報名
13
14
46,900+
報名
15
47,900+
報名
16
17
47,900+
報名
18
成行
45,900+
候補
19
成行
43,900+
報名
20
21
成行
45,900+
報名
22
23
24
25
26
成行
45,900+
報名
27
28
29
30
31
成行
44,900+
報名
參考航班
航班時間僅為參考，最終確定之使用航班，以說明會資料為準！
查看團體航班規定
去程
2025/05/12(一)
中華航空
17:15
TPE
桃園機場
2h50m
21:05
NGO
名古屋中部機場
回程
2025/05/17(六)
中華航空
09:55
NGO
名古屋中部機場
3h0m
11:55
TPE
桃園機場
航班時間僅為參考，最終確定之使用航班，以說明會資料為準！
航班詳情
「可賣」或「席次」均非最終成行人數，僅為本公司機位或庫存量，「可賣」或「席次」數量將會因供需或旅客取消與否而有增減。
成行人數仍應以實際銷售結果為準。
更新時間：
2024/12/28 20:31:17
☆ 北陸年度限定 震撼２個月 ☆
★ 立山黑部雪壁奇景ｘ粉紅芝櫻花毯 ★
特別安排：
★ 特別安排搭乘六項交通工具～
登上【立山黑部】漫步雪牆森呼吸
~壯闊開山，快來感受大自然療癒力量。
★ 期間限定！天空花迴廊【２０２５茶臼山高原芝櫻祭】
~ 特別安排搭乘纜車飽覽一整片粉紅芝櫻花毯。
★ 打卡秘境景點・跟團最方便～【奈良井宿】
日本最長的宿場－完整保留江戶時代的傳統建築與風情
★ 世界文化遺產【白川鄉合掌村】、日本三大名園【兼六園】
~來到北陸中部最不能錯過的必訪景點。
★ 日本國寶【犬山城】
~最古老１２座天守之一～木曾川及城下町的絕美景致盡收眼底！
★ 【三光稻荷神社】
~日本中部知名的「洗錢」神社，祈求結緣、財運能量ＵＰ！的人氣景點。
特色餐食：
★信州牛&長野地產菇菇壽喜燒御膳
★岐阜名物~朴葉味噌燒飛驒牛料理
**不同出發日期之售價皆不相同，售價以出發日為主，正確售價請洽詢您的業務人員。
**《優惠僅限全程參團》，舉凡湊票、JOIN TOUR、嬰兒不適用此優惠，且不得與其他優惠活動、折價券併用。
★【漫步立山大雪谷】
( 2025年4月15日 - 6月25日 期間限定)
每年入冬之後，國立公園因為積雪過深而選在十一月底的時候封山，到了翌年四月底五月初才開山，讓民眾再度重遊這片淨土。轉換六種不同的交通工具，方完成遊歷立山黑部的阿爾卑斯之路，嘗試了最多元化的玩法。而初春的立山，有超過二十公尺高的「雪壁」景觀，漫步其中，感受大自然的壯闊雄大，一趟行程走下來，只有不斷的驚訝聲與讚嘆聲。
※註：2025年4月起， 【立山隧道無軌電車】將改為【立山隧道電氣巴士】。
★【利用六種交通工具登上立山黑部峽谷連峰】
1.立山車站→美女平
【立山電動纜車1.3KM，7分鐘】
2.美女平→彌陀原→天狗平→室堂(海拔2450公尺)
【立山高原巴士23KM，50分鐘】
3.室堂→立山主峰→大觀峰
【立山隧道電氣巴士3.7KM，10分鐘】
4.大觀峰→黑部平
【空中纜車1.7KM，7分鐘】
5.黑部平→黑部湖→黑部水壩
【黑部登山纜車0.8KM，5分鐘＋徒步0.6KM走過水壩上方，15分鐘】
6.黑部水壩→扇澤
【關電隧道電氣巴士6.1KM，16分鐘】
※立山至室堂區間交通如卡旺季時期，會依行程流暢度為主，改為搭乘【臨時直通巴士】
★保證入住2晚～萬豪集團系列～中部國際機場喜來登福朋飯店(Four Points by Sheraton Nagoya)
地理位置優越，距名古屋中部國際機場僅須徒步約５分鐘。擁有超凡品味的現代化客房、採美式風格設計附有酒吧、撞球台、健身房等設施。保證25平米房間，享受客房舒適大空間。
★特別安排期間限定【茶臼山高原芝櫻祭】～搭乘纜車俯瞰４０萬株粉紅芝櫻地毯★
芝櫻祭預計：５月中旬至６月上旬
★花期盛開時節極其短暫，圖片僅供參考。如遇天候因素導致未如預期綻放或提前結束花期，仍會依原行程前往景點參觀，敬請了解。★
★特別安排米其林三星景點推薦～白川鄉★
★特別安排米其林三星景點推薦～兼六園★
★打卡秘境～日本最長宿場【奈良井宿】★
千本格子的民宅和商店並列林立，漫步在充滿江戶時代氛圍的街道中
★日本最古老的木造天守～國寶【犬山城】★
是江戶時代12座現存天守中最古老者，也與姬路城、松本城、彥根城和松江城並列日本五大國寶天守。
★財運・戀愛運聖地【三光稻荷神社】~迷你千鳥居★
★特別安排～
信州牛&長野地產菇菇壽喜燒御膳
★岐阜名物~朴葉味噌燒飛驒牛料理
餐食照片僅為示意圖，實際請依現場安排為主。
＊因逢黑部立山開山旺季期間，本行程交通住宿及旅遊點儘量忠於原行程，有時會因人潮及飯店確認關係，行程前後更動或互換觀光點或住宿地區順序調整，如遇特殊情況如船、交通阻塞、觀光點休假、住宿飯店調整或其它不可抗力之因素，行程安排以當地為主，並請於報名時特別留意。
＊＊ 行程備註說明 ＊＊
＊ 本行程最低出團人數為16人以上（含）。
＊ 使用合法營業用綠牌車，安排專業、親切、貼心的資深導遊為您服務。
＊ 日本國土交通省於平成24年6月(2012年)發布最新規定，每日行車時間不得超過10小時（以自車庫實際發車時間為計算基準），
以有效防止巴士司機因過(疲)勞駕駛所衍生之交通狀況。 （資料來源：日本國土交通省）
＊ 日本飯店並無實際星級分等，本網頁所顯現之分級，為目前旅遊市場之一般認定，並參考台灣及日本兩地間數個訂房網站資訊後所給予之客觀綜合分級，
且各網站之評量標準及角度各有不同，難以單一網頁所載資訊做為最終評鑑，敬請瞭解。
＊ 本行程交通、住宿、及旅遊點儘量忠於原行程；若遇特殊情況如船、交通阻塞、觀光景點休假、住宿飯店調整或因季節的交替及飯店確認的關係，
以及其他不可抗拒因素所影響時，行程順序會稍作調整或互換觀光景點，行程安排將以當地為主，敬請見諒。
＊ 行程中設定的餐食，皆因應防疫做相關餐食安排調整。
＊ 台灣與日本兩地間的飲食文化多有不同，日本的多數素食者可食用蔥、薑、蒜、辣椒、奶蛋甚至柴魚或肉汁高湯所熬煮的餐飲，為尊重台灣素食貴賓的飲食習慣，
在避免使用上述食材的前提下，各餐廳多以各式蔬菜、豆腐等食材搭配漬物料理的定食或鍋物提供給素食貴賓，且當地購買全素食品也相當不易，故建議前往日本
旅遊的貴賓，如有需要請自行事先準備素食品，以備不時之需。
◆房型備註說明◆
＊ 住宿酒店皆已(二人一室)為主，保障您旅遊的品質。
＊ 本行程可配房，如欲需求單人房，請洽業務確認加價費用。
＊ 若為一大人或一大人加一嬰兒參加，請洽業務確認加價費用。
＊ 日本房型除和式房外，皆為兩張小床，一大床房型可需求但無法保證，如需求到請洽業務確認加價費用。
＊ 日本房型除和式房外，少有三人房型，三人房型如下:(A.)一大床+一沙發床 (B.)二小床+一沙發床 (C.)一大床+一小床....可需求但無法保證。
若無需求到三人房時，請分一人出來配房，或指定單人房補單人房差，請洽業務確認加價費用，敬請見諒！
＊ 第一晚及第五晚之飯店【中部國際機場喜來登福朋飯店】全館無三人房，若單人參團或落單旅客，請分一人出來配房或補單人房差需求單人房，請洽業務確認加價費用，敬請見諒！
每日行程
Daily Itinerary
完整行程
精簡行程
DAY
台北
名古屋中部國際機場→飯店
今日帶著輕鬆的心情集合於台灣桃園國際機場，辦理出境手續後，搭乘豪華客機直接飛往日本中部第一大城【名古屋】；名古屋市由於位於東京和大阪之間、因此又有『中京』之稱。憑著地理位置的優勢加上水力發電，市內的重工業得到重要的發展，計有飛機工業、機械製造業及造船業。名古屋氣候宜人、水源充足、故此是日本的商業運輸中心。
特別說明：
第一晚及第五晚入住之【中部國際機場喜來登福朋飯店(Four Points by Sheraton Nagoya) 】
全館無三人房，若單人參團或落單旅客，請分一人出來配房或需求單人房補單人房差，無法配房或需求單人房者，請洽業務確認加價費用，敬請見諒！
餐食
早餐
溫暖的家
午餐
溫暖的家
晚餐
機上精緻簡餐
旅館
★保證入住~名古屋中部國際機場喜來登福朋飯店(Four Points by Sheraton Nagoya)
DAY
世界文化遺產【白川鄉合掌村】～童話世界中的薑餅屋街道→日本三大名園之一【兼六園】～金澤城跡～石川門→金澤 或 富山
餐食
早餐
飯店內早餐
午餐
朴葉味噌燒飛驒牛料理 或 白川鄉土風味套
晚餐
北陸海鮮料理 或 自助餐 或 飯店內晚餐
旅館
富山EXCEL東急 或 富山全日空 或 金澤MYSTAYS系列飯店 或 金澤VISTA 或 金澤皇冠假日飯店 或 同級
白川鄉合掌村
下車參觀
白川鄉與五箇山合掌造聚落，在台灣被通稱為合掌村或白川鄉合掌村，這是位於日本飛驒地區白川鄉(岐阜縣)與五箇山(富山縣)之間的5座合掌造聚落總稱，於1995年12月被聯合國教科文組織登錄成為世界文化遺產，其中以荻町的規模最大也最為出名，至今仍完整保留113棟合掌造建築，每年冬季雪景相當美麗夢幻，被喻為「冬日的童話村」。 合掌造是日本一種特殊民宅形式，起源於300年前居民為了適應山谷環境而設計，純木造建築不使用一根鐵釘，全以卡榫與結繩固定，並以茅草舖頂，60度斜角的正三角形屋頂除了可以抵禦強風，還能乘載厚重積雪並讓其自然崩落，每隔30、40年必須更換屋頂茅草，屆時需動員全村上百人一同協助、費時兩天才能完成。 在白川鄉裡規模最大的荻町，目前保有113棟合掌造建築，觀光方面也最為充實，有超過20間民宿、50間特產店與餐廳，遊客可走訪境內體積最大的重要文化遺產「和田家」、明善寺鄉土館、生活資料館等景點，或是順著山坡登上城山展望台，眺望整個聚落；而每年冬季在特定日子舉行的點燈儀式，更是吸引大批遊客前往參與，相當熱門。
兼六園
入內參觀
位於日本石川縣金澤市的兼六園，是日本極少數兼具寬廣腹地及美景的林泉迴遊式的大庭園，原是17世紀中期加賀藩藩主前田家在金澤城外郭建造的私人庭園，名為「蓮池庭」。這座庭園占地約3萬坪，耗時180年才建成，隨處可見的創意與巧思，映襯著春夏秋冬的不同風情，是江戶時期的代表性庭園，與茨城縣水戶市的偕樂園、岡山縣岡山市的後樂園並稱日本三大名園，也是日本國家指定的特別名勝。 兼六園之名出自中國宋朝詩人李格非的《洛陽名園記》，其內述的「宏大、幽邃、人力、蒼古、水泉、眺望」正好是兼六園的6種特質，然而這座園林不僅此而已，它會隨天氣晴雨、四季變換而產生不同景觀，如春櫻、夏綠、秋楓、冬雪，而初春時競相綻放的梅花也是一絕，逾5000株花木與小橋、飛瀑、石燈籠、亭台、曲水、霞池…等，都值得一一細賞。
收起行程內容
DAY
立山連峰【電動纜車】→美女平【高原巴士】→室堂（立山主峰）【隧道無軌電車】→大觀峰【空中纜車】→黑部平【黑部地下纜車】→黑部湖【徒步】→黑部水庫【關電隧道電氣巴士】→扇澤
★特別安排：利用六種交通工具欣賞立山黑部峽谷連峰之美★
【特別說明】
★【雪之大谷WALK】預定開放期間為 4月15日～6月25日。
★ 2025年，立山上各項活動的預定開放期間如下：(確實日期，請以
官方網站公告
為主)
★ 於4、5、6、9、10、11月份出發的貴賓，請注意本日行程會在海拔約3000公尺左右的高山地區停留約2小時，請務必攜帶禦寒衣物、手套、圍巾等。
★ 為保護黑部立山的自然生態環境，在交通及用餐部份多受限制。立山上所提供的餐食，皆以精緻簡樸日式料理為主。
★ 如遇旺季，以行程流暢度為主，午餐有可能會改為山下用餐或簡易式餐盒帶往山上用餐，敬請了解。
★ 旺季期間，立山至室堂間之交通依據官方的調度狀況，會有可能改為搭乘【臨時直通巴士】，敬請了解。
★ 特別提醒：若有不吃「鰻魚」之旅客，將改雞肉風味餐 或 其他套餐。請務必於出發前七天告知，恕無法接受當日變更。
餐食
早餐
飯店內早餐
午餐
立山鰻魚飯風味餐 或 日式風味套餐 或 簡易便當
晚餐
飯店內總匯自助餐 或 迎賓會席料理
旅館
安曇野ambient飯店 或 大町溫泉 黑部觀光 或 立山王子 或 信濃大町黑四全日空假日渡假酒店 或 同級
立山黑部阿爾卑斯路線
特別安排
< 2025年4月起 >
今日進入北陸旅程的精華重點，乘車經由
【富山】
前往立山國立公園，前往享有「日本阿爾卑斯山」美名的【立山黑部】，將近9公里的路程，全程使用各式環保交通工具翻山越嶺，讓您在清淨的空氣中，感受時時刻刻變化的立山風貌。首先從立山驛搭乘【電動纜車】到美女平，從立山車站搭乘電動纜車，約七分鐘即可到達標高差502公尺的美女平車站；在這裡有被稱之為美女杉的杉樹，傳說在女人不得進入立山的時代，有位尼姑因破壞規定強行登山觸怒了神明，後被降罪懲罰變成了杉樹。隨後改搭【高原巴士～電力車】到室堂，在高原巴士行駛的五十分鐘間，您可沿途欣賞原始森林與高原廣大景色，抵達室堂後，立山三山的雄山、淨土山、別山將聳立於眼前。室堂平也是立山黑部阿爾卑斯山脈路線觀光的中心地，因眾多慕名而來的遊客或登山客而生機蓬勃。在室堂還可品嚐日本名水之一的立山水，此處也是照相留影的最佳之處。再經由堂室改搭【立山隧道電氣巴士】，穿越海拔三千公尺的立山連峰至大觀峰，於此瞭望山谷美景；隨後乘坐【空中纜車】至黑部平，長達1.7公里約搭乘7分鐘的立山空中纜車，以無支柱直跨方式，聯結兩大山岳。接著乘坐【黑部登山纜車】至黑部峽谷，與黑部湖之間用5分鐘可達的全線地下式黑部電車相聯結。抵達後可徒步觀賞日本最高的黑部水壩（高186公尺、長492公尺的日本最大級水庫），其建構之宏偉，令人瞠目結舌；6月至10月之間，不時還有水庫洩洪，水勢非常壯觀；再轉搭【關電隧道電氣巴士】經過全長6.1公里，東洋第一的山洞隧道到達扇澤站，完成這一趟精彩的立山黑部之旅。
收起行程內容
DAY
保留江戶時代原貌～日本最長的宿場～打卡秘境【奈良井宿】→★天空花迴廊～【茶臼山高原芝櫻祭】～搭乘纜車俯瞰40萬株粉紅芝櫻地毯！→自由夜訪名古屋市區商圈
★特別安排：期間限定 （5月中旬至6月上旬）～【茶臼山高原芝櫻祭】～搭乘纜車俯瞰粉紅芝櫻地毯！
【備註說明】
如遇天候因素(下雨或颳風或氣溫異常...等)，導致芝櫻凋謝或未綻開，仍會依原行程前往景點純欣賞。芝櫻季預測期間：5月中旬至6月上旬。實際請依
茶臼山高原官方網站
公告為主，敬請知悉。
餐食
早餐
飯店內早餐
午餐
★特別安排～信州牛&長野地產菇菇壽喜燒御膳
晚餐
方便購物，敬請自理
旅館
名古屋VISTA飯店 或 名古屋MYSTAYS系列飯店 或 DORMYINN名古屋榮飯店 或 名鐵小牧飯店 或 名古屋萬怡酒店 或同級
奈良井宿
下車參觀
​中山道為江戶時代（1603—1868），連接江戶（東京）和首都（京都）的重要的街道，而奈良井宿則是中山道之中的驛站之一。中山道67個宿場當中，奈良井宿無論從江戶測(東側)的板橋宿場為起點算起第34個宿場，還是京側(西側)的守山宿算來，都是第34個宿場，正好位於中山道上的中間位置。這裡彷彿時光凍結，完整保留了江戶時代的傳統建築與濃濃風情，猶如深山中的古代聚落般，故被選為國家重要傳統的建造物群保存地區。奈良井宿為最長的宿場街道，全長約有1.2公里，被稱為「奈良井千軒」，為木曾十一宿中最熱鬧的住宿小鎮。現在除了一般民宅外，還有古色古香的民宿、餐廳、咖啡店、傳統工藝、紀念品店等店家，是一條充滿魅力又可遠離塵囂的秘境老街。
茶臼山高原芝櫻季
下車參觀
【茶臼山高原～芝櫻之丘】愛知縣內最高峰茶臼山，這裡可遙望南阿爾卑斯山脈。在海拔1,358米的萩太郎山的山頂附近延伸著色彩艷麗的芝櫻地毯。這裡2007年開始種植芝櫻，現在面積已達22,000平方米，一望無垠的大地上40萬株芝櫻盛開，非常壯觀。粉紅、白色、淡藍、藍紫等，顏色和形狀各異的6種芝櫻織染出美麗無比的空中花卉走廊，絕對值得一看。
【特別說明】茶臼山高原～芝櫻祭預定期間為5月中旬～6月上旬(依官方網站公告為準)。芝櫻祭因天候狀況影響，舉辦日期會略有調整，若行程當日遇花況不佳無法如期觀賞時，則改前往【惠那峡遊船】體驗，則不另退費，敬請了解。
榮町商圈 或 名古屋車站商圈
自由活動
【名古屋中央塔樓】高245公尺，51層樓，是名古屋中部地區最大的購物商城，有高島屋百貨，三省堂書店，東急手創館，著名餐廳街等；到了晚上，這裡的夜色就像是一幅360度的廣角圖，讓人彷彿置身於散發著寶石光芒，多彩絢麗的海洋中，極具魅力。同時也是是遊樂休閒中心，有各種酒館餐廳、電玩店、保齡球場、名品店、日常用品店、大型百貨公司等，著名的地下街有各種專賣店、精品店、日式及西式餐廳。 或【榮町商圈】周邊有許多大型百貨公司、各式餐廳、專賣店，並有名古屋最大型的地下街，裡面有服飾、名品、書籍、文具、唱片等商品專賣店，以及各式餐館和紀念品店，林林總總的商店，種類繁多應有盡有，並可遠望名古屋塔。
收起行程內容
DAY
日本三大神宮～草薙神劍供俸地【熱田神宮】→免稅店→財運・戀愛運聖地【三光稻荷神社】～迷你千鳥居→犬山城下町【昭和橫丁】散策 →世界最大～巨型招財貓商場【常滑AEON MALL】
餐食
早餐
飯店內早餐
午餐
犬山鄉土風味餐 或 日式定食套餐
晚餐
方便購物，敬請自理
旅館
★保證入住~名古屋中部國際機場喜來登福朋飯店(Four Points by Sheraton Nagoya)
熱田神宮
下車參觀
愛知縣名古屋市的熱田神宮，為祭祀日本神話中三大神器「草薙神劍(天叢雲劍)」而創立的神社，擁有上千年歷史，為當地信仰中心，地方慣稱「熱田sama(熱田様)」、「宮」，現今主祀神即為神劍神格化之熱田大神，另也供奉天照大神、日本武尊、宮簀媛命等神明，社境內林蔭蓊鬱、環境幽靜，並闢設有寶物館、資料館、文化古蹟龍影閣等。 坐落在名古屋市區的熱田神宮，其創建與日本神話息息相關，相傳在第12代日本天皇景行天皇在位期間，日本武尊持草薙神劍平定東國，而後將神劍託付給妻子宮簀媛命，在其於伊勢國能褒野遇難後，宮簀媛命遂遵照其遺願在熱田建神社祭祀並以神劍鎮守，由於草薙劍被視為皇室象徵，熱田神宮在日本皇室間占有重要地位。 熱田神社境約占6萬坪，以本宮與別宮為中心，境內樹林環繞，有樹齡千年的大楠樹，還有據說是織田信長出征桶狹間戰役時在神宮祈禱而打勝仗後所捐贈的「信長壁」，這是把土和石灰用油凝固後夾著瓦片製成的牆壁，與京都三十間堂的太閤壁、西宮神社的大練壁並稱為日本三大壁；此外還有典藏皇室與民眾捐贈的4千多件藝品的「寶物館」等等。旅客來到這裡除了參拜買御守外，神社近70餘個大大小小的慶典活動也值得體驗參與。
【免稅店】
入內參觀
(停留時間約一小時)店裡有琳瑯滿目的日本製商品任您選購，還有安排中文解說店員為您服務，如對商品有不明白的地方，店員會親切的為您解答及服務，因此您可安心採買選購您所需要的商品。
犬山城
入內參觀
三光稻荷神社
下車參觀
大型購物中心AEON MALL
自由活動
日本大型購物廣場，館內彙集眾多商品及日常百貨用品，
還可在著名的時尚品牌店、藥妝店購物，還有日本人氣餐廳、大型美食廣場享受日料和其他美味料理。
是一個方便逛街、享用美食，並可滿足血拚樂趣的購物廣場。
收起行程內容
DAY
飯店→日本海上機場之一【名古屋中部國際機場】
桃園國際機場
早餐後，前往建於伊勢灣人工島上的【名古屋中部國際機場】，這個機場在2005年2月啟用後，每天都吸引近6萬人，來此搭機、接送機，甚至逛街。在辦完手續後，機場內還有傳統建築模樣的飲食商店街，流行名品店，免稅菸酒化妝品等，您可在機場內自由輕鬆的選購。
隨後搭乘豪華客機飛返溫暖的家～台灣，結束此次日本愉快難忘的旅遊。
餐食
早餐
飯店內早餐
午餐
機上簡餐
晚餐
溫暖的家
旅館
溫暖的家
防疫規範
Epidemic Prevention Norms
•• 出國旅遊防疫安全 ••
1. 如有身體不適症狀，應審慎評估是否參團，並建議依個人需求自行配戴口罩。
2. 本公司依規定投保旅行業責任保險，並遵守交通部觀光局訂定之相關措施及國內防疫規範。
3. 出境旅客建議投保海外醫療險等相關保險，以因應染疫衍生之相關費用。
4. 本公司遵守旅行當地國家之各項防疫措施，倘無法配合當地之防疫措施，請勿報名參團。
5. 本公司將協助確認行程內安排之餐飲業、旅宿業、觀光遊樂業、交通運輸業皆遵循旅遊目的地國家防疫管制措施，妥適安排行程。
6. 出國前，請至疾病管制署全球資訊網查詢國際疫情資訊及防疫建議，或於出國前4至6週前往「旅遊醫學門診」接受評估。
7. 旅途中或返國時，曾有發燒、腹瀉、出疹或呼吸道不適等疑似傳染病症狀，請於入境時主動告知機場檢疫人員；返國後21天內，若有身體不適，請盡速就醫，並告知醫師旅遊史及接觸史。
8. 傳染病預防措施：
（1） 用肥皂勤洗手、吃熟食、喝瓶裝水。
（2） 有呼吸道症狀應配戴口罩。
（3） 噴防蚊液，避免蚊蟲叮咬。
（4） 不接觸禽鳥、犬貓及野生動物。
※更多旅遊醫學相關資訊請查詢疾病管制署全球資訊網https://www.cdc.gov.tw「國際旅遊與健康」專區，或撥打防疫專線1922（國外可撥+886-800-001922）。
查看完整資訊
安全守則
Safety Rules
～為了您在本次旅遊中本身的安全，我們特別請您遵守下列事項，這是我們應盡告知的責任，也是保障您的權益～
◆特殊旅客參團注意事項◆
若有行動不便、慢性疾病、年滿70歲以上之貴賓，請主動告知。 為考量旅客自身之旅遊安全及行程順暢度，並顧及同團其他團員之遊覽權益， 行動不便之貴賓，需與能獨立照顧您之家人或友人同行，並經公司評估，方始接受報名。 若報名付訂金後臨時告知，將收取相關必要費用，敬請見諒。
◆貼心提醒◆
1. 搭乘飛機時，請隨時扣緊安全帶，以免亂流影響安全。
2. 貴重物品請託放至飯店保險箱，如需隨身攜帶切勿離手，小心扒手在身旁。
3. 住宿飯店時請隨時將房門扣上安全鎖，以策安全；勿在燈上晾衣物；勿在床上吸煙，聽到警報器響, 請由緊急出口迅速離開。
4. 游泳池未開放時請勿擅自入池游泳，並切記勿單獨入池。
5. 搭乘船隻請務必穿著救生衣。
6. 搭乘快艇請扶緊把手或坐穩，勿任意移動。
7. 海邊戲水請勿超越安全警戒線。
8. 搭乘車時請勿任意更換座位，頭、手請勿伸出窗外，上下車時注意來車方向以免發生危險。
9. 搭乘纜車時請依序上下，聽從工作人員指揮。
10. 團體需一起活動，途中若要離隊需徵得領隊同意以免發生意外。
11. 夜間或自由活動時間若需自行外出，請告知領隊或團友，並應特別注意安全。
12. 行走雪地及陡峭之路請謹慎小心。
13. 切勿在公共場合露財，購物時也勿當眾清數鈔票。
14. 遵守領隊所宣布的觀光區、餐廳、飯店、遊樂設施等各種場所的注意事項。
15. 泡溫泉有一定的限制與規則，先了解其中限制，才能泡得健康美麗，又不失禮於日本人。泡溫泉須知如下：
●空腹、飲酒後或剛用餐完畢時不要入浴。
●泡湯要全裸入浴，穿著泳裝或圍著毛巾都是不對的方式，會破壞溫泉水質。
●泡湯前須先清洗身體，溫泉畔都設有衛浴設施；溫泉的鹼性相當強，部份旅客因體質可能會造成皮膚不適。
●孕婦、心臟病、皮膚病或皮膚上有傷口者不要泡湯，激烈運動後、熬夜隔天不要猛然泡湯，可能會造成休克。
●不常泡溫泉者，最好泡攝氏41度以下的溫泉，否則可能會造成身體不適；為避免突然浸入溫泉可能引發腦貧血的危險，浸泡前先以熱水淋濕頭部或身體。
●泡溫泉時間以15分鐘為限，避免皮膚的水分油份流失，如果感覺不適，趕快起來沖個冷水。
●泡湯後，身體儘量採用自然乾燥的方式，不要用毛巾擦拭，以保留皮膚上的溫泉成分。
●身上有紋身者，不能到大浴場泡溫泉。
16. 台灣與日本兩地間的飲食文化多有不同，尊重台灣素食貴賓的飲食習慣，各餐廳多以蔬菜、豆腐等食材搭配漬物料理的定食或鍋物提供給素食貴賓，日本素食者可食用蔥、薑、蒜、辣椒、蛋奶，湯底也大多使用柴魚或大骨高湯熬煮。
※因當地購買全素食品也相當不易，故建議前往日本旅遊的貴賓，如有需要請自行事先準備素食品，以備不時之需。
17. 餐廳調理限制較嚴謹，恐難以對應臨時之更改，若因宗教及過敏因素而有餐食禁忌者(茹素、不吃牛、豬、生魚片、過敏甲殼類、蛋奶等)請於報名時告知業務專員，我們將盡可能為你調整。其餘個人飲食喜好因素，因受限餐廳選擇，恕無法調整。
18. 自2025年3月1日起，多家航空公司為確保飛航安全，規定行動電源在航程中全程禁止使用及充電。為了保障您的權益，請於出發前留意各航空公司對行動電源及電子產品的攜帶與使用規定。
查看完整資訊
團體航班規定事項
Group Flight Rules
【中華航空公司】
一.《機位加價升等商務艙規定》
1.團體機票規定:機位不接受加價升等商務艙。如需商務艙，請自行開立【個人機票】。
二.《行李規則》
1.托運行李:依航空公司之規定，每人可免費托運一件２３公斤內之行李，指甲刀、剪刀等刀具類，請置放於大行李箱，請勿置放貴重值錢之物品及相機等易受損之物件於欲托運之行李內。
2.隨身行李:建議除托運行李外，另可帶一件手提行李(７公斤)，以便置放隨身貴重物品等。
3.因飛航安全問題，目前航空公司要求旅客個別托運自己的行李，請依領隊說明至指定櫃檯托運。
（乳液狀物品若帶上飛機，每瓶只能100CC，且需置放在透明夾鍊袋內，建議置放於拖運行李中就沒限制；若要攜帶手機及電器用品的鋰電池，請置放於隨身包包中，不能置放於托運行李中）。
★詳細說明請參考官網:https://www.china-airlines.com/tw/zh/fly/prepare-for-the-fly/baggage/baggage-rules##%E8%A8%97%E9%81%8B%E8%A1%8C%E6%9D%8E%E7%9B%B8%E9%97%9C%E8%B3%87%E8%A8%8A
三.《脫隊》
1.團體機票需【團進團出，不可延回】。
四.《其它》
1.北海道(千歲或函館)航線之團體機票，一經開立後皆無法辦理退票。
2.旺季期間(農曆春節及暑假)之團體機票一經開票後，不得更改行程、姓名及辦理退票。
3.非旺季期間之日本線(北海道除外)團體機票一經開立後若需辦理退票，需收退票手續費，價錢須另外詢價，請洽您的業務，謝謝。
4.團體機票無預先劃位，亦無法指定，座位安排係由航空公司調度，同行者座位不一定能相鄰，敬請見諒！
5.嬰兒之定義為回程未滿兩歲者，若去程未滿兩歲而回程滿兩歲，不適用嬰兒價錢須另外詢價，請洽您的業務，謝謝。
6.嬰兒席次相關注意事項：
因受飛行考量及法規限制，每航班及艙等有可收受嬰兒數量上限。即日起，如有嬰兒同行者，請於報名時通知業務並確認能否取得席次及開票作業，並同時提供開票的名單及出生年月日，航空公司將以入名單順序受理，額滿即不再受理。
●取得席次～直接完成開票作業，如取消將有費用產生。
●未取得席次～嬰兒及同行大人１名者可直接退回訂金。
查看完整資訊
旅遊資訊
Travel Information
簽證
保險
小費
電話
電壓時差
◆簽證◆
1. 從台灣出發，持他國護照自日本返台者，需持有以下附件證明，以備日本航空公司櫃台及台灣海關入關查驗(二擇一)：
1.台灣居留證或台灣入境簽證
2.預定自台灣返回他國之機票
(例：從台灣出發，持美國護照前往日本者，自日本出境回台灣時，在日本航空公司櫃台辦理check in手續，以及台灣海關入關時，需出示台灣居留證或台灣護照，或從台灣返回美國之機票以備查驗。)
2. 日本新入境審查手續將於本（96）年11月20日起實施，前往日本旅客入境時需提供本人指紋和拍攝臉部照片並接受入境審查官之審查，拒絕配合者將不獲准入境，敬請瞭解。
3. 為避免出國當天出現無法出境的情況，在此特別請您務必再次檢查、確認您的護照。
◆護照相關須知◆
1. 護照不得有汙(破)損、缺頁、擅自增刪、塗改、加蓋圖戳、或擅貼貼紙。
2. 護照效期須至少有「自返國日起算六個月以上」之效期。
3. 特殊身份(例：軍警人員、役男...等)及出國須申請許可之職業，出國前請務必經相關單位申請「出境許可」並於出國當日攜帶相關文件備查。
4. 所持有之中華民國身分證登載內容已變更者（包括：姓名、身分證字號、出生日期、受管制入出境身分等），而與原有護照登載內容不同時，或持照人之相貌變更，與護照照片不符時，皆須重新申辦護照，始可出國。
5. 所持護照如曾向警政單位申報遺失備案者，則原護照已無效，須重新申辦護照，始可出國。
6. 雙重國籍或非中華民國國籍者：關於護照、簽證相關規定之說明，均係針對持中華民國護照之旅客，若貴賓擁有雙重國籍、或持非中華民國護照者，請先自行辦理並查明所持護照入境「旅遊地」及再次入境台灣之簽證及相關規定；如您具備前述情況者，請於報名時即告知您的服務人員前述資訊。（注意：部份國家需為IC晶片護照才能免簽，請務必留意）
7. 雙重國籍者，請務必攜帶2本護照。
8. 役男為年滿十九歲之當年一月一日起，至屆滿三十六歲當年十二月三十一日止，尚未當兵者，出國須申請備查許可，可於出國前一個月內，於役男短期出境線上申請作業系統申請出國備查許可。
免簽國家/地區一覽表 (日文)(英文)：
https://www.mofa.go.jp/mofaj/toko/visa/tanki/novisa.html#notice08
簽證
保險
小費
電話
電壓時差
收藏
比較
列印
紀錄
門市服務據點
赴台旅遊
旅遊資訊
聯盟平台
菁英招募
企業永續
投資人專區
聯絡雄獅
訂購諮詢
台北：
02-8793-9000
(24小時服務專線)
桃園：
03-347-6699
台中：
04-3702-3279
台南：
06-703-0250
高雄：
07-213-7799
雄獅璽品/郵輪旅遊/中南美南極/運動旅遊：
02-8793-9608
高爾夫：
02-7746-3988
認識雄獅
關於雄獅
訂購須知
交易安全
隱私權政策
網站導覽
關係企業
美國雄獅網
加拿大雄獅網
香港雄獅網
日本雄獅網
欣聯航
雄獅通運
集團網群
日華旅遊
雄獅嚴選
欣傳媒
傑森整合行銷
立即追蹤
訂購諮詢專線
台灣台北市114內湖區石潭路151號
旅遊產品由 雄獅旅行社股份有限公司 提供
代表人：王文傑
聯絡人：黃信川
統一編號：04655091
代表號：
02-8793-9000
電子郵箱：
customerservice@liontravel.com
綜合旅行社 交觀綜字 2016號
品保協會會員93字第北0541號
Copyright© LION TRAVEL SERVICE CO., LTD.
All Rights Reserved
選擇出發日期
只找成行
2025年
5月
10
11
12
成行
47,900+
報名
13
14
46,900+
報名
15
47,900+
報名
16
17
47,900+
報名
18
成行
45,900+
候補
19
成行
43,900+
報名
20
21
成行
45,900+
報名
22
23
24
25
26
成行
45,900+
報名
27
28
29
30
31
成行
44,900+
報名
選擇出發日期
2025年5月
只找成行
出發日期
行程
成行狀態
可賣
席次
價格
2025/05/12 (一)
成行
報名
席次
28
TWD 47,900
出發日期
行程
成行狀態
可賣
席次
價格
2025/05/14 (三)
報名
17
席次
28
TWD 46,900
出發日期
行程
成行狀態
可賣
席次
價格
2025/05/15 (四)
報名
17
席次
28
TWD 47,900
出發日期
行程
成行狀態
可賣
席次
價格
2025/05/17 (六)
報名
17
席次
28
TWD 47,900
出發日期
行程
成行狀態
可賣
席次
價格
2025/05/18 (日)
成行
候補
席次
28
TWD 45,900
出發日期
行程
成行狀態
可賣
席次
價格
2025/05/19 (一)
成行
報名
席次
30
TWD 43,900
出發日期
行程
成行狀態
可賣
席次
價格
2025/05/21 (三)
成行
報名
席次
37
TWD 45,900
出發日期
行程
成行狀態
可賣
席次
價格
2025/05/26 (一)
成行
報名
12
席次
28
TWD 45,900
出發日期
行程
成行狀態
可賣
席次
價格
2025/05/31 (六)
成行
報名
10
席次
28
TWD 44,900
CloseIcon
訂購諮詢專線
訂購諮詢
台北 (24小時服務專線)
Phone Call Icon
02-8793-9000
桃園
Phone Call Icon
03-347-6699
台中
Phone Call Icon
04-3702-3279
台南
Phone Call Icon
06-703-0250
高雄
Phone Call Icon
07-213-7799
璽品旅遊
郵輪旅遊
中南美南極
運動旅遊
Phone Call Icon
02-8793-9608
高爾夫
Phone Call Icon
02-7746-3988
Cookies 設定：
為確保網站正常運行並為您提供更好的網站體驗。點擊「同意」或繼續使用網站，即表示您同意放置所有的Cookie，如不同意請關閉本網站。如需更多有關Cookie的資訊，請查閱我們的
隱私保護政策
同意
出發地
國外旅遊
台北
松山/桃園機場
台中
台南
高雄
台灣旅遊
不限
北北基
桃竹苗
中彰投
雲嘉南
高屏
宜花東
關鍵字
確定
以關鍵字優先搜尋，請輸入景點或城市區域。

"""

USE_IMAGES = False


# ==================== HTML 生成器（升級版）====================
class AdvancedHTMLGenerator:
    """進階 HTML 演示文稿生成器"""
    
    def __init__(self):
        self.slides = []
        
    def generate_from_ai_json(self, ai_data: Dict, image_metadata: Dict) -> str:
        """從 AI JSON 生成完整 HTML"""
        
        # 解析幻燈片
        for slide_data in ai_data.get('slides', []):
            slide_type = slide_data.get('slide_type', 'text_content')
            slide_html = self._create_slide_html(slide_data, slide_type, image_metadata)
            self.slides.append(slide_html)
        
        # 生成完整 HTML
        return self._build_full_html(ai_data.get('title', '演示文稿'))
    
    def _create_slide_html(self, data: Dict, slide_type: str, image_metadata: Dict) -> str:
        """根據類型創建幻燈片 HTML"""
        
        if slide_type == 'opening':
            return self._opening_slide(data)
        elif slide_type == 'section_divider':
            return self._section_slide(data)
        elif slide_type == 'text_content':
            return self._content_slide(data)
        elif slide_type == 'image_with_text':
            return self._image_text_slide(data, image_metadata)
        elif slide_type == 'full_image':
            return self._full_image_slide(data, image_metadata)
        elif slide_type == 'closing':
            return self._closing_slide(data)
        else:
            return self._content_slide(data)
    
    def _opening_slide(self, data: Dict) -> str:
        """開場頁"""
        title = data.get('title', '')
        subtitle = data.get('subtitle', '')
        
        return f"""
        <div class="slide slide-opening">
            <div class="slide-content">
                <h1 class="main-title">{title}</h1>
                {f'<p class="subtitle">{subtitle}</p>' if subtitle else ''}
            </div>
        </div>
        """
    
    def _section_slide(self, data: Dict) -> str:
        """章節分隔頁"""
        section_title = data.get('section_title', '')
        
        return f"""
        <div class="slide slide-section">
            <div class="slide-content">
                <h2 class="section-title">{section_title}</h2>
                <div class="decoration-line"></div>
            </div>
        </div>
        """
    
    def _content_slide(self, data: Dict) -> str:
        """純文字內容頁"""
        title = data.get('title', '')
        bullets = data.get('bullets', [])
        indent_levels = data.get('indent_levels', [0] * len(bullets))
        
        bullets_html = ""
        for bullet, level in zip(bullets, indent_levels):
            indent_class = f"indent-{level}" if level > 0 else ""
            bullets_html += f'<li class="{indent_class}">{bullet}</li>\n'
        
        return f"""
        <div class="slide slide-content">
            <div class="slide-content">
                <h2 class="slide-title">{title}</h2>
                <ul class="bullet-list">
                    {bullets_html}
                </ul>
            </div>
        </div>
        """
    
    def _image_text_slide(self, data: Dict, image_metadata: Dict) -> str:
        """圖文混合頁"""
        title = data.get('title', '')
        image_id = data.get('image_id', '')
        text = data.get('text', '')
        layout = data.get('layout', 'horizontal')
        
        # 獲取圖片路徑（使用相對路徑或絕對路徑）
        img_src = ""
        if image_id in image_metadata:
            img_src = image_metadata[image_id]['path']
        
        layout_class = "layout-vertical" if layout == "vertical" else "layout-horizontal"
        
        return f"""
        <div class="slide slide-content">
            <div class="slide-content">
                <h2 class="slide-title">{title}</h2>
                <div class="image-text-container {layout_class}">
                    <div class="image-box">
                        <img src="{img_src}" alt="">
                    </div>
                    <div class="text-box">
                        <p>{text.replace(chr(10), '<br>')}</p>
                    </div>
                </div>
            </div>
        </div>
        """
    
    def _full_image_slide(self, data: Dict, image_metadata: Dict) -> str:
        """大圖展示頁"""
        title = data.get('title', '')
        image_id = data.get('image_id', '')
        caption = data.get('caption', '')
        
        # 獲取圖片路徑（使用相對路徑或絕對路徑）
        img_src = ""
        if image_id in image_metadata:
            img_src = image_metadata[image_id]['path']
        
        return f"""
        <div class="slide slide-content">
            <div class="slide-content">
                <h2 class="slide-title">{title}</h2>
                <div class="full-image-container">
                    <img src="{img_src}" alt="">
                    {f'<p class="caption">{caption}</p>' if caption else ''}
                </div>
            </div>
        </div>
        """
    
    def _closing_slide(self, data: Dict) -> str:
        """結尾頁"""
        closing_text = data.get('closing_text', '謝謝觀看')
        subtext = data.get('subtext', '')
        
        return f"""
        <div class="slide slide-closing">
            <div class="slide-content">
                <h1 class="closing-title">{closing_text}</h1>
                {f'<p class="closing-subtext">{subtext}</p>' if subtext else ''}
            </div>
        </div>
        """
    
    def _image_to_base64(self, image_path: str) -> str:
        """圖片轉 base64"""
        try:
            with open(image_path, 'rb') as f:
                return base64.b64encode(f.read()).decode('utf-8')
        except Exception as e:
            print(f"⚠️ 圖片轉換失敗 {image_path}: {e}")
            return ""
    
    def _build_full_html(self, title: str) -> str:
        """構建完整 HTML 文檔"""
        return f"""
<!DOCTYPE html>
<html lang="zh-TW">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{title}</title>
    <style>
        * {{
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }}
        
        body {{
            font-family: '微軟正黑體', 'Microsoft JhengHei', 'Helvetica Neue', Arial, sans-serif;
            background: linear-gradient(135deg, #1e3c72 0%, #2a5298 100%);
            min-height: 100vh;
            padding: 20px;
        }}
        
        .presentation-container {{
            max-width: 1200px;
            margin: 0 auto;
        }}
        
        .slide {{
            width: 100%;
            aspect-ratio: 4 / 3;
            background: white;
            margin-bottom: 30px;
            box-shadow: 0 10px 40px rgba(0,0,0,0.3);
            border-radius: 12px;
            overflow: hidden;
            position: relative;
            display: none;
        }}
        
        .slide.active {{
            display: block;
            animation: slideIn 0.5s ease-out;
        }}
        
        @keyframes slideIn {{
            from {{
                opacity: 0;
                transform: translateY(20px);
            }}
            to {{
                opacity: 1;
                transform: translateY(0);
            }}
        }}
        
        .slide-content {{
            padding: 60px 80px;
            height: 100%;
            display: flex;
            flex-direction: column;
        }}
        
        /* 開場頁 */
        .slide-opening {{
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            display: flex;
            align-items: center;
            justify-content: center;
        }}
        
        .slide-opening .slide-content {{
            display: flex;
            flex-direction: column;
            align-items: center;
            justify-content: center;
            width: 100%;
            height: 100%;
        }}
        
        .slide-opening .main-title {{
            font-size: 64px;
            font-weight: bold;
            color: white;
            text-align: center;
            margin-bottom: 30px;
            text-shadow: 3px 3px 6px rgba(0,0,0,0.3);
        }}
        
        .slide-opening .subtitle {{
            font-size: 32px;
            color: rgba(255,255,255,0.95);
            text-align: center;
        }}
        
        /* 章節頁 */
        .slide-section {{
            background: linear-gradient(135deg, #4682b4 0%, #2c5f8d 100%);
            display: flex;
            align-items: center;
            justify-content: center;
        }}
        
        .slide-section .slide-content {{
            display: flex;
            flex-direction: column;
            align-items: center;
            justify-content: center;
            width: 100%;
            height: 100%;
        }}
        
        .slide-section .section-title {{
            font-size: 56px;
            font-weight: bold;
            color: white;
            text-align: center;
            padding: 40px;
        }}
        
        .decoration-line {{
            width: 200px;
            height: 4px;
            background: white;
            margin: 30px auto;
            border-radius: 2px;
        }}
        
        /* 內容頁 */
        .slide-content .slide-title {{
            font-size: 42px;
            font-weight: bold;
            color: #2c3e50;
            margin-bottom: 40px;
            padding-bottom: 20px;
            border-bottom: 4px solid #4682b4;
        }}
        
        .bullet-list {{
            list-style: none;
            padding: 0;
        }}
        
        .bullet-list li {{
            font-size: 28px;
            color: #34495e;
            margin: 25px 0;
            padding-left: 50px;
            position: relative;
            line-height: 1.6;
        }}
        
        .bullet-list li:before {{
            content: "▶";
            position: absolute;
            left: 0;
            color: #4682b4;
            font-size: 24px;
        }}
        
        .bullet-list li.indent-1 {{
            padding-left: 100px;
            font-size: 24px;
            color: #555;
        }}
        
        .bullet-list li.indent-1:before {{
            content: "▸";
            left: 50px;
            font-size: 20px;
        }}
        
        /* 圖文混合 */
        .image-text-container {{
            display: grid;
            gap: 40px;
            flex: 1;
        }}
        
        .image-text-container.layout-horizontal {{
            grid-template-columns: 1fr 1fr;
        }}
        
        .image-text-container.layout-vertical {{
            grid-template-rows: auto auto;
        }}
        
        .image-box {{
            display: flex;
            align-items: center;
            justify-content: center;
        }}
        
        .image-box img {{
            max-width: 100%;
            max-height: 100%;
            object-fit: contain;
            border-radius: 8px;
            box-shadow: 0 4px 15px rgba(0,0,0,0.2);
        }}
        
        .text-box {{
            display: flex;
            align-items: center;
        }}
        
        .text-box p {{
            font-size: 24px;
            color: #2c3e50;
            line-height: 1.8;
        }}
        
        /* 大圖展示 */
        .full-image-container {{
            flex: 1;
            display: flex;
            flex-direction: column;
            align-items: center;
            justify-content: center;
        }}
        
        .full-image-container img {{
            max-width: 90%;
            max-height: 70%;
            object-fit: contain;
            border-radius: 12px;
            box-shadow: 0 8px 20px rgba(0,0,0,0.25);
        }}
        
        .caption {{
            margin-top: 20px;
            font-size: 20px;
            color: #7f8c8d;
            text-align: center;
        }}
        
        /* 結尾頁 */
        .slide-closing {{
            background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%);
            display: flex;
            align-items: center;
            justify-content: center;
        }}
        
        .slide-closing .slide-content {{
            display: flex;
            flex-direction: column;
            align-items: center;
            justify-content: center;
            width: 100%;
            height: 100%;
        }}
        
        .slide-closing .closing-title {{
            font-size: 64px;
            font-weight: bold;
            color: white;
            text-align: center;
            margin-bottom: 30px;
        }}
        
        .slide-closing .closing-subtext {{
            font-size: 28px;
            color: rgba(255,255,255,0.95);
            text-align: center;
        }}
        
        /* 導航控制 */
        .nav-controls {{
            position: fixed;
            bottom: 40px;
            left: 50%;
            transform: translateX(-50%);
            background: rgba(0,0,0,0.7);
            padding: 15px 30px;
            border-radius: 50px;
            display: flex;
            gap: 20px;
            align-items: center;
            backdrop-filter: blur(10px);
        }}
        
        .nav-controls button {{
            background: white;
            border: none;
            padding: 12px 24px;
            border-radius: 25px;
            cursor: pointer;
            font-size: 16px;
            font-weight: bold;
            color: #2c3e50;
            transition: all 0.3s;
        }}
        
        .nav-controls button:hover {{
            background: #4682b4;
            color: white;
            transform: scale(1.05);
        }}
        
        .nav-controls button:disabled {{
            opacity: 0.5;
            cursor: not-allowed;
        }}
        
        .slide-counter {{
            color: white;
            font-size: 16px;
            font-weight: bold;
            min-width: 80px;
            text-align: center;
        }}
        
        /* 響應式 */
        @media (max-width: 768px) {{
            .slide-content {{
                padding: 30px 40px;
            }}
            
            .slide-opening .main-title {{
                font-size: 40px;
            }}
            
            .image-text-container.layout-horizontal {{
                grid-template-columns: 1fr;
            }}
        }}
    </style>
</head>
<body>
    <div class="presentation-container">
        {''.join(self.slides)}
    </div>
    
    <div class="nav-controls">
        <button id="prevBtn">◀ 上一張</button>
        <span class="slide-counter"><span id="currentSlide">1</span> / <span id="totalSlides">0</span></span>
        <button id="nextBtn">下一張 ▶</button>
    </div>
    
    <script>
        let currentSlide = 0;
        const slides = document.querySelectorAll('.slide');
        const totalSlides = slides.length;
        
        const prevBtn = document.getElementById('prevBtn');
        const nextBtn = document.getElementById('nextBtn');
        const currentSlideSpan = document.getElementById('currentSlide');
        const totalSlidesSpan = document.getElementById('totalSlides');
        
        totalSlidesSpan.textContent = totalSlides;
        
        function showSlide(n) {{
            slides.forEach((slide, i) => {{
                slide.classList.remove('active');
                if (i === n) {{
                    slide.classList.add('active');
                }}
            }});
            
            currentSlideSpan.textContent = n + 1;
            prevBtn.disabled = n === 0;
            nextBtn.disabled = n === totalSlides - 1;
        }}
        
        function nextSlide() {{
            if (currentSlide < totalSlides - 1) {{
                currentSlide++;
                showSlide(currentSlide);
            }}
        }}
        
        function prevSlide() {{
            if (currentSlide > 0) {{
                currentSlide--;
                showSlide(currentSlide);
            }}
        }}
        
        prevBtn.addEventListener('click', prevSlide);
        nextBtn.addEventListener('click', nextSlide);
        
        document.addEventListener('keydown', (e) => {{
            if (e.key === 'ArrowRight' || e.key === ' ') {{
                e.preventDefault();
                nextSlide();
            }} else if (e.key === 'ArrowLeft') {{
                e.preventDefault();
                prevSlide();
            }}
        }});
        
        // 初始化
        if (totalSlides > 0) {{
            showSlide(0);
        }}
    </script>
</body>
</html>
        """


# ==================== 主程序 ====================
def main():
    print("🎨 AI 驅動的 HTML → PPTX 生成器")
    print("=" * 60)
    
    # 初始化 AI 客戶端
    client = genai.Client(api_key=API_KEY)
    
    # 載入圖片
    image_files = []
    image_metadata = {}
    
    if USE_IMAGES and os.path.exists("downloaded_images"):
        print("\n📸 載入圖片資源...")
        for index, file in enumerate(sorted(os.listdir("downloaded_images"))):
            if file.endswith(('.jpg', '.jpeg', '.png')):
                image_file = client.files.upload(file=f"downloaded_images/{file}")
                print(f"   ✓ 上傳圖片 {index + 1}: {file}")
                
                image_id = f"img_{index+1:02d}"
                image_files.append(image_file)
                image_metadata[image_id] = {
                    "filename": file,
                    "path": f"downloaded_images/{file}",
                    "gemini_file": image_file,
                    "index": index + 1,
                }
    
    image_list_info = "\n".join(
        [f"- {img_id}: {data['filename']}" for img_id, data in image_metadata.items()]
    ) if image_metadata else "無圖片資源（純文字簡報）"

    # AI 生成簡報結構
    print("\n🤖 AI 分析內容並生成簡報結構...")
    
    prompt = f"""請分析以下內容，生成一個結構化的演示文稿（適合 HTML 格式）。

**文字內容**：
{TEXT_CONTENT}

**可用圖片**：
{image_list_info}

**輸出 JSON 格式**：
{{
  "title": "簡報標題",
  "topic": "簡報主題",
  "slides": [
    {{
      "slide_type": "opening",
      "title": "主標題",
      "subtitle": "副標題"
    }},
    {{
      "slide_type": "section_divider",
      "section_title": "章節名稱"
    }},
    {{
      "slide_type": "text_content",
      "title": "頁面標題",
      "bullets": ["要點1", "要點2"],
      "indent_levels": [0, 0]
    }},
    {{
      "slide_type": "image_with_text",
      "title": "標題",
      "image_id": "img_01",
      "text": "說明文字",
      "layout": "horizontal"
    }},
    {{
      "slide_type": "full_image",
      "title": "標題",
      "image_id": "img_02",
      "caption": "圖片說明"
    }},
    {{
      "slide_type": "closing",
      "closing_text": "謝謝觀看",
      "subtext": "期待與您同行"
    }}
  ]
}}

**要求**：
1. 自動分析內容，識別2-4個主題
2. 每個主題有章節分隔頁
3. 合理安排圖片（如有）
4. 總共10-15張幻燈片
"""
    
    response = client.models.generate_content(
        model="gemini-2.5-flash",
        config=types.GenerateContentConfig(
            response_mime_type="application/json",
        ),
        contents=[prompt, *image_files]
    )
    
    print("   ✓ AI 分析完成")
    print(f"   📊 Token 使用：{response.usage_metadata}")
    
    # 解析 AI 回應
    try:
        ai_data = json.loads(response.text)
        
        print(f"\n📋 簡報資訊：")
        print(f"   標題：{ai_data.get('title', '')}")
        print(f"   主題：{ai_data.get('topic', '')}")
        print(f"   幻燈片數量：{len(ai_data.get('slides', []))}")
        
        # 生成 HTML
        print("\n🎨 生成 HTML 演示文稿...")
        html_gen = AdvancedHTMLGenerator()
        html_content = html_gen.generate_from_ai_json(ai_data, image_metadata)
        
        # 保存 HTML
        html_filename = f"{ai_data['topic'].replace(' ', '_')}_presentation.html"
        with open(html_filename, 'w', encoding='utf-8') as f:
            f.write(html_content)
        
        print(f"   ✓ HTML 已保存：{html_filename}")
        print(f"\n🌐 請在瀏覽器中打開：")
        print(f"   file://{os.path.abspath(html_filename)}")
        
        # 保存 JSON（供轉換 PPTX 使用）
        json_filename = f"{ai_data['topic'].replace(' ', '_')}_data.json"
        with open(json_filename, 'w', encoding='utf-8') as f:
            json.dump(ai_data, f, ensure_ascii=False, indent=2)
        
        print(f"\n💾 數據已保存：{json_filename}")
        print(f"   （可用於後續轉換為 PPTX）")
        
        print("\n" + "=" * 60)
        print("✅ 生成完成！")
        print("💡 提示：")
        print("   - 在瀏覽器中預覽 HTML")
        print("   - 使用方向鍵或點擊按鈕切換幻燈片")
        print("   - 稍後可以轉換為 PPTX 格式")
        print("=" * 60)
        
    except json.JSONDecodeError as e:
        print(f"\n❌ JSON 解析錯誤：{e}")
        print(f"原始回應：{response.text}")
    except Exception as e:
        print(f"\n❌ 發生錯誤：{e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    main()
