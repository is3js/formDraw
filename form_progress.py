#!/usr/bin/env python
# coding: utf-8
# pip install panel


import ipywidgets as widgets
from ipywidgets import Layout

import datetime
from datetime import timedelta

from IPython.display import HTML
from IPython.display import display, clear_output, Markdown

import sqlite3
import pandas as pd
import numpy as np

db_path = "./disease_easy.db"
con = sqlite3.connect(db_path)
try:
    disease = pd.read_sql("SELECT * FROM disease",
                   con,
                   index_col='index' # sqlite3 db에 데이터번호는 default로 "index"칼럼으로 가져오는데, 차라리 인덱스로 주자.
                   )
    v_disease_search_list = (disease['상병코드'] + '  :  ' + disease['상병명']).values.tolist()
    v_disease_search_list = np.unique(v_disease_search_list).tolist()
    con.close()
except:
    con.close()
    raise ValueError(db_path)
    

yc_category_dict = {
# 중성어혈
    '중성어혈' : [
        '1vial', 
        '0.5cc',
        ],

# 섬수
    '경근이완약침' : [
        '1vial',
        ],
    # for 자보 외래
    '교정약침' : [
        '1vial',
    ],
    
# 척추신 3cc -> 신경근
    '신경근이완약침' : [
        '복합1부위',
        '복합2부위',
        '복합F',
        ],
    
# 근이완 0.1cc
    '특수이완약침' : [
        '1부위',
        '2부위',
    ],
    

    '봉독약침' : [
        'B4-eBV (분리정제봉독, 200,000:1)',
# 봉독: BV2 (200,000:1) 
#1vial 당 2ml이상 (봉독 2%) - 견부 및 상지부 등에 시행. 진통 및 소염의 작용.'
        
        'B1-BV (봉약침 5%, 20,000:1)',
#1vial 당 2mL이상
#melittin 0.1mg/ml
#20,000:1
        
        'B2-BV (봉약침 10%, 10,000:1)',
# melittin 0.2mg/ml
# 10,000:1 

        'SBV 50 (봉약침 25%, 4,000:1)',
#melittin 0.5 mg/ml 로 배합된 약침
#4,000:1 
# 아피톡신 대용 
    ]   
}
yc_str_dict = {
# 중성
    '중성어혈' : "진통 및 소염의 작용.",
# 섬수
    '경근이완약침' : "중성어혈 및 봉독 약침액을 상병에 따른 경혈점 및 Td.에 시행함. 해당 부위 근긴장 완화를 통한 통증 개선 목적.",
# 섬수 for 자보 외래
    '교정약침' : "진통 및 소염의 작용.",
# 척추신 3cc -> 신경근
    '신경근이완약침' : "척추신 3cc. 신경근 주변의 근육과 연조직에 대한 이완을 통한 신경학적 증상의 개선 목적.",
# 근이완 0.1cc
    '특수이완약침' : " 근이완 0.1cc. 근육을 이완시킬 수 있는 경혈에 대해 약침액을 자입하는 것이며, 진통, 근육이완의 효과. 요부의 적응 경혈에 자입. ",
# 봉독 
    '봉독약침' : "진통 및 소염의 작용.",
}
pe_detail_dict = {
    # 일반
    "S/H" : " : ",
    "[Medi]" : " ",
    "sensory" : "(-/-)",
    "motor" : "(-/-)",
    # ROS
    "A/N/V/D/C" : "(-/-/-/-/-)",
    "C/S/R": "(-/-/-)",
    # 국소통증
    'Pain/Td': "(+/+) on ", 
    'local redness/swelling/heating/bruise' : "(-/-/-/-)",
    "paresthesia" : " on ", 
    "NRS" : " : ",
    # 경추부
    'Compression test': "(+)",
    "Spurling's test": "(+)" ,
    "Distraction test":"(+)", 
    "Valsalva test":"(+)",
    "Swallowing test":"(+)",
    "Hoffman sign":"(+)", 
    "Finger escape sign":"(+)",
    
    #'흉추부' 
    "Beevor's sign" : "(+)", 
    "Sternal compression test":"(+)", 
    
    #'요추부' 
    "SLR test" :"(45/45)", 
    "Bragard's sign":"(+/+)", 
    "Lasegue's sign" :"(+)", 
    "Well leg raise test":"(+)", 
    "Milgram test":"(+/+)",
    "Schober test":"(+/+)",
    "Hoover test":"(+)",
    
    #"견관절" 
    "Apley Scratch test":"(+/+)",
    "Drop arm test":"(+/+)", 
    "Empty can test":"(+/+)",
    "Yergason test":"(+/+)",
    "Speed test":"(+/+)",
    "Shoulder apprehension test":"(+/+)", 
    "Adson test":"(+/+)",
    "Hawkins test":"(+/+)", 
    "Neer test":"(+/+)",
        
    #"주관절" 
    "Tennis Elbow test":"(+)",
    "Gold Elbow test":"(+)",
    "Test for Ligamentous stability":"(+)",
        
    #"완관절" 
    "Finkelstein test":"(+)",
    "Phalen's test":"(+/+)",
    "Tinel's sign at wrist":"(+)",
    
    #"고관절/천장관절"
    "Thomas test":"(+/+)", 
    "Log roll test" : "(+/+)",
    "Patrick test" : "(+/+)",
    "Gaenslen's test" : "(+/+)",
    "Trendelenburg sign" : "(+/+)",
    "Ober test" : "(+/+)",
    
    
    #"슬관절" 
    "Anterior&posterior draw sign":"(+/+)", 
    "Lachman test":"(+/+)", 
    "Varus/Valgus stress test":"(+/+)",
    "McMurray's test":"(+/+)",
    "Apley's compression test":"(+/+)", 
    "Apley's distraction test":"(+/+)",
    "Patello-femoral grinding test":"(+/+)", 
        
    #"족관절" 
    "Ankle anterior drawer test":"(+/+)",
    "Ankle inversion stress test":"(+/+)",
    "Thomson test":"(+/+)", 
    "Homan's test":"(+/+)", 
}
pe_category_dict = {
    '일반' : [
        "S/H",
        "[Medi]",
        "sensory",
        "motor",
    ],
    'ROS' : [
        "A/N/V/D/C",
        "C/S/R",
    ],
    
    '국소통증' : [
        'Pain/Td', 'local redness/swelling/heating/bruise',
        "paresthesia", 
        "NRS",
    ],
		
	'경추' : [
        'Compression test',  "Spurling's test" ,"Distraction test",
        "Valsalva test",
        "Swallowing test",
        "Hoffman sign", "Finger escape sign",
		],	
		
	'흉추부' : [
        "Beevor's sign", 
        "Sternal compression test", 
		],
    
    '요추부' : [
        "SLR test", "Bragard's sign", "Lasegue's sign", "Well leg raise test", "Milgram test",
        "Schober test",
        "Hoover test",
		],
    
    "견관절" : [
        "Apley Scratch test",
        "Drop arm test", "Empty can test",
        "Yergason test","Speed test",
        "Shoulder apprehension test", 
        "Adson test",
        "Hawkins test", "Neer test",
    ],
    
    "주관절" : [
        "Tennis Elbow test",
        "Gold Elbow test",
        "Test for Ligamentous stability",
    ],
    
    "완관절" : [
        "Finkelstein test",
        "Phalen's test","Tinel's sign at wrist",
    ],
    
    "고관절/천장관절" : [
        "Thomas test", "Log roll test",
        "Patrick test",
        "Gaenslen's test",
        "Trendelenburg sign",
        "Ober test",
    ],
    
    "슬관절" : [
        "Anterior&posterior draw sign", "Lachman test", "Varus/Valgus stress test",
        "McMurray's test","Apley's compression test", "Apley's distraction test",
        "Patello-femoral grinding test", 
    ],
    
    "족관절" : [
        "Ankle anterior drawer test","Ankle inversion stress test",
        "Thomson test", "Homan's test", 
    ],
}
chuna_category_dict = {
	'추나' : [
        '단순-경추부/흉추부', 
        '단순-요추부/골반부',
        '복잡-경추부/흉추부', 
        '복잡-요추부/골반부',
        '시행하지 않음.'
		],
		
	'도인운동요법' : [
			'도인1부위-경항부',
            '도인1부위-요추부',
            '도인2부위-경항부and요추부'
		],
}
chuna_str_dict={
    '시행하지 않음.' : "- 추나치료 : -\n"
    ,
    '단순-경추부/흉추부': """- 추나치료 : 단순, 경추부 및 흉추부 시행, 경추와 흉추의 부정렬 교정 및 근육 재교육
             앙와위 경추 JS 신연 교정기법 / 가동제한 변위 
             앙와위 경추 신연기법 (수건이용) / 신연제한 변위 
             앙와위 경추 교정기법 / 가동, 신연, 회전제한 변위 
             복와위 하부흉추 두상골 교정기법 / 비중립성 굴곡변위
""", 
    '단순-요추부/골반부': """- 추나치료 : 단순, 요추부 및 골반부 시행, 요추의 부정렬 교정, 골반부 근육 재교육
             복와위 요천관절 신연기법 / 신연제한 
             복와위 장골 교정기법 / 장골 전방, 후방 회전 변위 
             복와위 하지거상 장골 교정기법 / 장골 후방 회전 변위 
             복와위 천골 굴곡 신전변위 교정기법 / 천골 굴곡 신전 변위 
             복와위 천골 측굴회전변위 교정기법 / 천골 측굴회전 변위
""", 
    '복잡-경추부/흉추부': """- 추나치료 : 복잡, 경추부 및 흉추부 시행, 경추와 흉추의 부정렬 교정 및 근육 재교육
             앙와위 경추 JS 신연 교정기법 / 가동제한 변위 
             앙와위 경추 신연기법 (수건이용) / 신연제한 변위 
             앙와위 경추 교정기법 / 가동, 신연, 회전제한 변위 
             복와위 하부흉추 두상골 교정기법 / 비중립성 굴곡변위
""", 
    '복잡-요추부/골반부': """- 추나치료 : 복잡, 요추부 및 골반부 시행, 요추의 부정렬 교정, 골반부 근육 재교육
             복와위 요천관절 신연기법 / 신연제한 
             복와위 장골 교정기법 / 장골 전방, 후방 회전 변위 
             복와위 하지거상 장골 교정기법 / 장골 후방 회전 변위 
             복와위 천골 굴곡 신전변위 교정기법 / 천골 굴곡 신전 변위 
             복와위 천골 측굴회전변위 교정기법 / 천골 측굴회전 변위
""", 
    '도인1부위-경항부': """- 도인운동요법 : 경항부-승모근, 경항부-후경부근 근육이완, 강화 및 재교육 운동 실시
                 근육 긴장으로 1) 관절가동범위 제한, 2) 지속적인 해당부위 통증, 3) 일상생활 불편 등 문제 있음.
                 자가운동교육을 통한 기능회복이 적절한 치료법일 것으로 판단.
""", 
    '도인1부위-요추부': """- 도인운동요법 : 요추부-요방형근, 요추부-이상근 근육이완, 강화 및 재교육 운동 실시
                 근육 긴장으로 1) 관절가동범위 제한, 2) 지속적인 해당부위 통증, 3) 일상생활 불편 등 문제 있음.
                 자가운동교육을 통한 기능회복이 적절한 치료법일 것으로 판단.
""", 

    '도인2부위-경항부and요추부': """- 도인운동요법 : 경항부-승모근,후경부근 and 요추부-요방형근,이상근 근육이완, 강화 및 재교육 운동 실시
                 근육 긴장으로 인한 1) ROM 제한, 2) 지속되는 통증, 3) 일상생활 불편 등 문제 있음.
                 자가운동교육을 통한 기능회복이 적절한 치료법일 것으로 판단. 
""", 
}
bj_category_dict = {

	'기혈음양진액변증' : [
			'혈어증', '혈허증', '기체증', '기허증', '상기', '음허증', '양허증', '기혈양허증', '음양양허증',
		],
		
	'기타병증' : [
			'울증', '비증-행비' , '비증-통비' , '비증-착비' , '위증' , '마목불인', '곽란', '항강', '역절풍', '산후풍',
		],	
		
	'한의병증' : [
			'풍한증', '풍열증', '풍습증', '한습증', '습열증',
		],
		
	'육경병증' : [
			'태양병증', '양명병증', '소양병증', '태음병증', '소음병증', '궐음병증',
		],
	
	'삼초위기영혈변증' : [
			'위분증', '기분증' , '영분증', '혈분증' ,
		],
}
bj_code_str_dict={
##### 기혈음양진액병증
    '혈어증': [ 'U612',
    """
[변증진단] 혈어증(血瘀證) 
[변증소견] 局部疼痛腫脹, 刺痛据按, 口唇靑紫, 皮膚瘀斑 / 舌靑紫瘀點 / 脈澁沈細

"""],
	'혈허증': [   'U610',
    """
[변증진단] 혈허증(血虛證)
[변증소견] 眼瞼口唇蒼白, 爪甲淡白, 頭暈眼花 / 舌質淡苔薄 / 脈細無力 

"""],
	'기체증': [   'U603',
    """
[변증진단] 기체증(氣滯證)
[변증소견] 胸脇脹悶, 腰背疼痛, 痛無定處 / 舌苔薄 / 脈弦 

"""],
	'기허증': [   'U600',
    """
[변증진단] 기허증(氣虛證) 
[변증소견] 呼吸氣短, 身疲乏力, 少氣懶言 / 舌淡 / 脈細無力 

"""],
	'상기': [   'U508',
    """
[변증진단] 상기(上氣)
[변증소견] 脘腹疼痛, 喘咳上氣, 嘔吐脇痛 / 舌苔膩 / 脈弦滑 

"""],
	'음허증': [  'U620' ,
    """
[변증진단] 음허증(陰虛證)
[변증소견] 潮熱盜汗, 五心煩熱 / 舌紅少苔 / 脈細數 

"""],
	'양허증': [   'U621',
    """
[변증진단] 양허증(陽虛證)
[변증소견] 畏寒肢冷, 倦怠無力, 自汗 / 舌質淡白 / 脈虛沈弱 

"""],
	'기혈양허증': [   'U624',
    """
[변증진단] 기혈양허증(氣血兩虛證)
[변증소견] 面色蒼白, 身疲乏力, 食無味, 頭暈眼花 / 舌淡嫩 / 脈細弱無力 

"""],
	'음양양허증': [   'U625',
    """
[변증진단] 음양양허증(陰陽兩虛證)
[변증소견] 畏寒肢冷, 自汗盜汗, 午後潮熱 / 舌質痿嫩 / 脈細數無力

"""],
#### 한의병증
	'풍한증': [  'U500' ,
    """
[변증진단] 풍한증(風寒證)
[변증소견] 惡寒發熱, 舌苔白膩, 脈浮 

"""],
	'풍열증': [   'U501',
    """
[변증진단] 풍열증(風熱證 )
[변증소견] 惡熱, 口渴, 舌紅苔黃 

"""],
	'풍습증': [   'U502',
    """
[변증진단] 풍습증(風濕證)
[변증소견] 身重, 關節疼痛屈伸不利, 脈滑數, 舌紅苔白厚 

"""],
	'한습증': [   'U503',
    """
[변증진단] 한습증(寒濕證)
[변증소견] 惡寒, 四肢冷, 消化不利, 腹脹泄瀉, 脈沈滑, 舌淡苔白膩 

"""],
	'습열증': [   'U504',
    """
[변증진단] 습열증(濕熱證)
[변증소견] 身熱不暢, 渴不多飮, 脘腹脹悶, 午後熱甚, 頭脹頭重, 脈沈細數, 舌紅胎黃膩滯

"""],
#### 기타병증
	'울증': [   'U221' ,
    """
[변증진단] 울증(鬱證)
[변증소견] 心下痞滿, 胸滿, 脈沈重無力, 大小便不利 

"""],
	'비증-행비': [   'U238',
    """
[변증진단] 비증(痺證) - 행비(行痺)
[변증소견] 肢體關節痛無定處, 脈浮數, 舌淡苔白 

"""],
	'비증-통비': [   'U238',
    """
[변증진단] 비증(痺證) - 통비(痛痺)
[변증소견] 肢體關節痛一點定處, 寒氣勝, 脈浮滑, 舌苔薄白 

"""],
	'비증-착비': [   'U238',
    """
[변증진단] 비증(痺證) - 착비(着痺)
[변증소견] 一處固定不忍痛, 濕氣勝, 脈沈滑, 舌苔白膩 

"""],
	'위증': [   'U239',
    """
[변증진단] 위증(痿證)
[변증소견] 四肢痿軟無力, 脈沈細, 舌苔薄白  

"""],
	'마목불인': [   'U242',
    """
[변증진단] 마목불인(麻木不仁)
[변증소견] 四肢不仁痲木, 血虛勝, 脈細數, 舌質紅絳微黃  

"""],
	'곽란': [   'U284',
    """
[변증진단] 곽란(霍亂)
[변증소견] 鬱熱寒氣感陰陽錯亂, 心下痞, 脈浮滑, 舌苔白厚膩 

"""],
	'항강': [   'U303',
    """
[변증진단] 항강(項强)
[변증소견] 脈浮滑, 頸項强, 舌質淡紅 

"""],
	'역절풍': [   'U304',
    """
[변증진단] 역절풍(歷節風)
[변증소견] 短氣, 自汗, 四肢無力, 頭眩, 四肢百節疼痛屈伸不利, 脈浮細, 舌尖紅 

"""],
	'산후풍': [   'U327',
    """
[변증진단] 산후풍(産後風)
[변증소견] 關節肢體疼痛, 重着痲木, 脈弦細滑, 舌淡紅

"""],
#### 육경병증
	'태양병증': [   'U52',
    """
[변증진단] 태양병증(太陽病證)
[변증소견] 頭項强痛, 惡寒, 脈浮緊, 舌淡苔白

"""],
	'양명병증': [   'U53',
    """
[변증진단] 양명병증(陽明病證)
[변증소견] 渴欲飮水, 發熱, 腹滿, 痛据按, 煩燥, 舌苔黃燥, 脈沈實有力 

"""],
	'소양병증': [   'U54',
    """
[변증진단] 소양병증(少陽病證)
[변증소견] 食慾不振, 寒熱往來, 目眩, 胸脇苦滿, 心煩, 脇痛, 脈弦, 舌苔薄白 

"""],
	'태음병증': [   'U55',
    """
[변증진단] 태음병증(太陰病證)
[변증소견] 腹滿而吐, 食不下, 自利, 口不渴, 脈沈滑, 舌苔白厚 

"""],
	'소음병증': [   'U56',
    """
[변증진단] 소음병증(少陰病證)
[변증소견] 四肢逆冷, 下利淸穀, 汗出亡陽, 脈微細, 舌紅少苔 

"""],
	'궐음병증': [   'U57',
    """
[변증진단] 궐음병증(厥陰病證)
[변증소견] 嘔吐下利, 心身無力, 手足厥寒, 脈細欲絶, 舌紅少苔

"""],
#### 삼초위기영혈변증
	'위분증': [   'U594',
    """
[변증진단] 위분증(衛分證)
[변증소견] 發熱, 微惡寒, 口乾不欲飮, 身重, 脈浮數, 舌苔偏膩 

"""],
	'기분증': [   'U595',
    """
[변증진단] 기분증(氣分證)
[변증소견] 頭重, 心下痞, 嘔吐泄瀉, 發熱無惡寒, 脈浮數, 舌苔黃 

"""],
	'영분증': [   'U596',
    """
[변증진단] 영분증(營分證)
[변증소견] 身熱夜甚, 口乾咽燥, 不眠, 脈細數, 舌質紅 

"""],
	'혈분증': [   'U597',
    """
[변증진단] 혈분증(血分證)
[변증소견] 高熱, 不眠, 譫語, 出血, 脈細數, 舌苔暗紫

"""],
}
hjr_dict={
    
    '경항부' : [
        '풍지,대추/견료,극천/척추간내침술:신주',
        '풍지,대추/견료,극천/관절내침술:곡지',
        '풍지,대추/견료,극천/:척추간내침술:풍부',
        '분구침술',
            ], #
    '두부' : [
        '백회,합곡/내관,외관/관절내침술:견우',
        
        '분구침술',
        ], 
    
    '견부' : [
        '견정,대추/견료,극천/관절내침술:견우',
        '척택,양릉천/곡지,수삼리/관절내침술:견우',
        
        '분구침술',
        ], 
    '견관절부':[
        '견정,행간/음릉천,양릉천/관절내침술:견우',
        
        '분구침술',
    ],
    '경견부' : [
        '견정,대추/견료,극천/관절내침술:견우', 
        '견정,대추/견료,극천/척추간내침술:풍부', 
        '경문,견정/견료,극천/??', 
        '풍지,견정/견료,극천/관절내침술:견우', 
        '풍지,견정/견료,극천/척추간내침술:대추',
        '풍지,견정/견료,극천/척추간내침술:신주',  
        '풍지,대추/견료,극천/척추간내침술:신주',
        '분구침술',
    ],
    '경견부+요부' : [
        '견정,요양/풍부,풍지/??',
        '분구침술',
    ], 
    '경견부+상지부' : [
        '풍지,견정/견료,극천/관절내침술:견우',  
        '분구침술',
    ],
    '견비부' : [
        '풍지,견정/견료,극천/관절내침술:견우',
        '척택,양릉천/곡지,수삼리/척추간내침술:명문',
        
        '분구침술',
    ],
    '견배부' : [
        '풍지,견정/견료,극천/관절내침술:견우',
        '견정,대추/견료,극천/척추간내침술:신주',  
        '분구침술',
    ],
    '견배부+상지부' : [
        '예풍,노수/내관,외관/??',
        '분구침술',
    ], # 
    '흉배부' : [
        '척택,양릉천/곡지,수삼리/??',
        '분구침술',
            ], # 
    '배부' : [
        '풍문,견정/견료,극천/??',
        '분구침술',],
    
    '협륵부' : [
        '담수,견정/곡지,수삼리/관절내침술:노수',
        '분구침술',],
    '요부' : [
        '신수,구허/곤륜,태계/척추간내침술:명문',
        '신수,환도/곤륜,태계/척추간내침술:명문',
        '신수,구허/곤륜,태계/척추간내침술:요양관',
        '신수,환도/곤륜,태계/척추간내침술:요양관',  
        '분구침술',
    ],
    '요부+하지부' : [
        '신수,구허/곤륜,태계/',  
        '분구침술',
    ],
    '요부+슬부' : [
        '신수,구허/곤륜,태계/관절내침술:슬안',
        
        '분구침술',
    ],
    '요배부' : [
        '신수,환도/곤륜,태계/척추간내침술:요양관', 
        '신수,구허/곤륜,태계/관절내침술:환도',
        '분구침술',
    ],
    '요둔부' : [
        '신수,구허/곤륜,태계/관절내침술:환도', 
        '신수,환도/곤륜,태계/척추간내침술:명문', 
        '신수,환도/곤륜,태계/척추간내침술:요양관', 
        '분구침술',
    ],
    '요둔부+하지부' : [
        '신수,환도/곤륜,태계/척추간내침술:명문', 
        '분구침술',
    ],
    #[1+2] 공손내관/곡지삼리
    #     [1+2]   용천아문/곤륜태계
    # [1+2]   지실구허/곤륜태계
    '상지부' : [
        '태연,태백/합곡,후계/관절내침술:곡지',
        '척택,양릉천/곤륜,태계/관절내침술:소해',
        '척택,양릉천/곡지,수삼리/관절내침술:소해',
        '수삼리,태충/내관,외관/관절내침술:양계',
        '구허,양지/합곡,후계/관절내침술:곡지',
        '합곡,행간/곤륜,태계/관절내침술:곡지',
        
        '분구침술',
            ],
    '주관절부' : [
        '곡지,수삼리/합곡,후계/관절내침술:양곡',
        '양지,구허/내관,외관/관절내침술:양계',
        '척택,양릉천/곡지,수삼리/관절내침술:소해',
        '분구침술',
            ],
    '완관절부' : [
        '곡지,삼리/후계,합곡/관절내침술:곡지',
        '곡지,삼리/후계,합곡/관절내침술:양지',
        '분구침술',
    ], 
    
    '완관절부+상지부' : [
        '경거,구허/합곡,후계/관절내침술:곡지', 
        '분구침술',
    ], 
    '수부' : [
        '구허,양지/합곡,후계/관절내침술:양계',        
        '분구침술',
    ], 
    '복부' : [
        '중완,족삼리/음릉천,양릉천/복강내침술:상완',
        '중완,관원/곡지,수삼리/복강내침술:기해',
        '분구침술',
    ],    
    '하지부' : [
        '독비,합곡/음릉천,양릉천/관절내침술:슬안',
        '외관,구허/곤륜,태계/관절내침술:중봉',
        '외관,구허/합곡,후계/관절내침술:신맥',
        '외관,구허/현종,삼음교/관절내침술:조해',
        '곡지,족삼리/곤륜,태계/관절내침술:신맥',
        '곡지,족삼리/현종,삼음교/관절내침술:신맥',
        '합곡,양릉천/후계,합곡/관절내침술:양계',
        '합곡,양릉천/현종,삼음교/관절내침술:신맥',
        '합곡,양릉천/현종,삼음교/관절내침술:구허',
        '분구침술',    
    ],
    '서혜부' : [
      '신수,환도/곤륜,태계/척추간내침술:요양관',
       '외관,구허/곤륜,태계/관절내침술:중봉',  
        '분구침술',
    ],
    '하지부+족관절부' : [
        '지실,구허/곤륜,태계/관절내침술:중봉',  
        '분구침술',
    ],
    '슬부' : [
        '독비,합곡/음릉천,양릉천/관절내침술:슬안',
        '곡지,족삼리/음릉천,양릉천/관절내침술:슬안',
        '곡지,족삼리/합곡,후계/관절내침술:양곡',
        '곡지,독비/음릉천,양릉천/관절내침술:슬안',
        '합곡,양릉천/현종,삼음교/관절내침술:슬안',
        '합곡,양릉천/현종,삼음교/관절내침술:독비',
        '합곡,행간/곤륜,태계/관절내침술:구허',
        '분구침술',
    ],
    '슬부+경견부' : [
        '합곡,양릉천/삼음교,현종/??',  
        '분구침술',
    ],  
    '슬부+족관절부' : [
        '합곡,양릉천/삼음교,현종/관절내침술:슬안',
        '분구침술',
    ], 
    '족관절부' : [ 
        '외관,구허/곤륜,태계/관절내침술:중봉',
        '외관,부류/곤륜,태계/관절내침술:중봉',
        '합곡,행간/곤륜,태계/관절내침술:구허',
        '독비,합곡/곤륜,태계/관절내침술:구허', 
        '독비,합곡/양릉천,음릉천/관절내침술:중봉', 
        '독비,합곡/양릉천,음릉천/관절내침술:슬안', 
        '합곡,행간/곤륜,태계/관절내침술:구허',
        '신수,환도/곤륜,태계/관절내침술:중봉',
        '태백,태연/곡지,척택/관절내침술:중봉',
        '분구침술',
    ],
    '족외과부' : [ 
        '독비,합곡/곤륜,태계/관절내침술:신맥', 
        '외관,구허/곤륜,태계/관절내침술:곡지', 
        '분구침술',
    ],
    '요부+어혈방' : [
        '독비,합곡/곤륜,태계/관절내침술:신주',
        '분구침술',
    ],
    '안면부' : [
        '합곡,족삼리/지창,협거/관절내침술:곡지',
        '합곡,인중/지창,협거/관절내침술:곡지',
        '백회,합곡/내관,외관/비강내침술:내영향',
        '분구침술',
    ],
    '피부' : [
        '중완,합곡/내관,외관/상복', 
        '중완,합곡/내관,외관/하복', 
        '곡지,삼리/양릉,음릉/중완',
        '분구침술',
    ],
    '식체' : [
        '합곡,족삼리/내관,외관/복강내침술:중완',    
        '분구침술',
    ],
    '중풍' : [
        '곡지,족삼리/후계,합곡/관절내침술:양계',   
        '분구침술',
    ],
    '간열' : ['소부,음곡/합곡,후계/??'], # 
    '간허' : ['경거,음곡/합곡,후계/??'], # 
    '담허' : ['통곡,상양/합곡,후계/??'], # 
    
    '심포실' : ['대릉,태백/내관,외관/??'], # 
    '심포한' : ['대도,소부/합곡,후계/??'], # 
    '심포허' : ['양곡,해계/삼음교,현종/??'], # 
    

    '비허' : ['소부,대도/합곡,후계/??'], # 
    '소장허' : ['후계,족임읍/곤륜,태계/??'], # 
    
    
    '폐허': ['태연,태백/합곡,후계/'],
    '대장허' : ['곡지,족삼리/합곡,후계/??'], # 
    
    '신허' : ['경거,부류/곤륜,태계/기해'],
    '방광허' : ['상양,지음/합곡,후계/신맥'],
    
    '삼초허' : ['중저,통곡/합곡,후계/??'], # 
}

os_data="""간단+후방추돌+운전석|TA(car+car, 후방추돌, 운전석)
간단+전방추돌+운전석|TA(car+car, 정방추돌, 운전석)
3중추돌+1번째+후방|3car Rear end collision MVA in driver\\'s seat (1st car)
3중추돌2번째+후방+고속도로|3car rear end collision MVA in driver\\'s seat on express way (2nd car, 2times collision - Rear/Frontal) 
3중추돌+2번충돌+후방|3car rear end collision MVA in driver\\'s seat (2 times collision)
3중추돌+양쪽에서중간충돌|AM9 3 car both side collsion MVA (middle side)  
4중추돌1번째|4-way collision MVA in driver\\'s seat(4중추돌 첫번째 차량) 
4중추돌1번째+조수석|4 car rear end collision MVA in passenger\\'s seat (1st car)
전방추돌+운전석|Frontal impact collision MVA in driver\\'s seat 
후방추돌+운전석|Rear impact collision MVA in driver\\'s seat 
후방추돌+뒷좌석(Lt.)|Rear imapct collision MVA in back seat (Lt.) 
후방추돌+뒷자석(Rt.)|Rear impact collision MVA in back seat (Rt.)
후방추돌+뒷자석|Rear impact collision MVA in back seat 
후방추돌+택시+뒷자석|Rear impact collision MVA in back seat (TAXI) 
우측추돌+운전석|Rt. side impact collition MVA in driver\\'s seat
좌측추돌+운전석|Lt. side impact collision MVA in driver\\'s seat
좌측추돌+뒷자석(Rt.)|Lt side impact collision MVA in  Back seat (Rt.)
좌측추돌+조수석|Lt. side impact collision MVA in Passenger\\'s seat 
좌측추돌+운전석+교차로|MVA (Lt side impact collision MVA in driver\\'s seat / cross way) 
자전거+차|Bike collision Car MVA 
자전거+차+상세|Bike - Car Frontal impact collision MVA in driver\\'s seat (Bike driver)
자전거+차+운전석|Bike collision Car MVA in driver\\'s seat (Bike rider) 
자전거+차+자전거뒷자리|Bike collision other car MVA on Bike\\'s driver seat. Bike overturned.
나무+차|Car collsion tree MVA ** 
보행차+차|Impact collision MVA in pedestrian
보행자+차|car collision pedestrian MVA **
가드레인+차|collision to guardrail (self) 
전봇대+차|MVA (self collision to power pole)  
버스+차|MVA in bus
---|----
국건|알수없음, Old, Unknown 
국건|오래된 증상/별무
국건|C/C occur after slip down at 2020.02.23. (on cycle) 
국건|2020/03/04(slip down in kitchen) 
국건|2020/02/16 / slip down on climb a mountain (무등산에 눈구경하러 갔다가 넘어져서 손을 짚었다.) 
국건|Old, unknown, 5-6months ago aggravation  / C.C occur without provocation 
국건|5,6 years ago 
국건|1month ago, marked aggravation 2wks ago 
국건|C/C occur / 2020.02. sx.aggravation 
국건|김장김치를 담그던 중 허리와 무릎 염좌 발생
국건|런지 운동 하시던 중 다쳐서 상기의 C/C 발생. 
국건|C.C occur after long time sitting
국건|간헐적으로 지속 / 2020.09.07 컴퓨터 장시간 사용 후 악화
국건|1month ago, Occipitalgia appearance  / 2-3days ago, Cervicalgia aggravated 
국건|2020년 04월경부터 / exactly unknown 
국건|2019년 말 - tennis elbow 
국건|Old, 2020년 4월 6일 C/C marked aggravation after slip down 
국건|sudden aggravation at 3~4wks ago / Lt side pelvic pain 
국건|Old, unknown / Cervicalgia ass. sx. 
국건|2004 C/C occur / 2018 sx. relapse 
국건|2020.08.10. approx.
국건|2020.09.01. sudden C/C aggravation without trauma Hx. 
국건|2020.10.20 sx. sudden aggravation 
국건|Old / 2020.05 aggravation tendency 
국건|Rt shoudler : 1year ago / Arthroscopic reconstruction at 2020.11.13. 
국건|Lt side flank - 2020.08. (폼롤러 중 sx.appearance / 문형래 OS 진단) 
국건|2020.08.15 C/C occur after heavy object transporting"""
pi_data="""
|2019.12.14 타 정형외과 진료 -> 인대 손상 가능성 설명 들음   2020.01.02~01.03 우측 발목통증으로 본원 adm tx.  2020.01.07~01.21 수완센트럴병원 adm tx. (01.08 인대파열 op)   
|상기 환자는 상기일에 상기와 같은 MVA로 C/C 발생. 이후 당일 해피퓨병원 OPD XR 상 non specific fx. 확인. 잔여 소견에 대한 적극적 진료 위하여 본원 외래 내원. 
|상기 환자는 상기와 같은 소견에 대한 적극적 진료 위하여 본원 외래 내원. 
|상기 환자는 상기일에 차량 뒷좌석 착석 신호대기 중 후방차량 추돌 MVA로 C/C 발생. 이후 이에 대한 보다 적극적 진료 위하여 본원 외래 내원. 
|상기 환자는 상기일에 운전석 착석 신호대기 중 후방차량 추돌 MVA로 C/C 발생. 이후 이에 대한 보다 적극적 진료 위하여 본원 외래 내원. 
|01.11~01.13 ks 병원 입원치료 x-ray 검사상 별무소견.
|상기 환자는 상기일에 차량 후방좌석 착석 주행중 후방차량 추돌 MVA로 C/C 발생. 이후 2020.01.11 ~ 2020.01.13 KS병원 Adm Tx. 후 본원 잔여소견 진료 위하여 외래 내원. 
|From 10years ago HT medication, QD P.O   From 2years ago Hyperlipidemia QD P.O   From 2years ago BPH QD P.O 
|상기 환자는 상기일에 운전석 착석 주행중 다중 후면 추돌 MVA로 C/C 발생. 1일간 경과관찰한 후 증상 강도로 인한 업무기능 저하 및 통증 악화 소견 있어 이에 대한 보다 적극적 진료 및 평가 위하여 본원 외래 내원. 
|2020.11.19 am 9:00 함평 ic 빠져나가서 터미널 부근 운전석 착석 주행 중 정면추돌당함  수상일 11:40 경 1차례 구토 1pm 경 상무병원 ER OPD Tx(혈액검사, 링거맞으심)
|상기 환자는 약 3년간 상기의 소견 지속적으로 호소하시는 상태로 L-spine MR상 mild Disc herniation 소견 받으셨으며, 2019.09. 아산병원 OPD Tx. 시에도 뚜렷한 통증 원인 규명이 안되어 현재까지 Local 의원등 진료 수행해오시는 상태로 증상에 대한 적극적 진료 위하여 본원 외래 내원. 
|상기 환자는 상기일에 운전석 착석 신호정차 중 후방추돌 MVA로 C/C 발생. 이후 이에 대한 적극적 진료 및 진찰 위하여 본원 외래 내원. 
|상기 환자는 상기일에 상기와 같은 MVA로 C/C 발생한 후 2020.02.02. 자생한방병원 Adm Tx. 시행 후 이에 대한 적극적 진료 위하여 본원 외래 내원. 
|*상기 환자는 상기일에 차량 운전 중 도로 주변 나무 및 돌 등 구조물과 충돌 MVA로 C/C 발생. 사고 당일 부안성모병원 XR, BrainCT 상 non specific fx. 확인 후 2020.01.29 ~ 2020.02.01. 시티병원 Adm Tx. 중 L-spine CT, MR 상 Coccyx region non fx. 확인. 잔여 소견 지속되므로 지속적인 진료 위하여 본원 외래 내원.  **
|상기 환자는 상기일에 차량 운전석 착석 주행중 3중추돌 MVA로 C/C 발생. 이후 지속적인 Sx. aggravation tendency 있어 2020.02.08. 로컬 한의원 OPD Tx. 1회 시행 후 본원 외래 내원. -> 조제한약 약 7일분 처방받았다고 함. 
|상기 환자는 상기일에 차량 후면 조수석 착석 주행 중 후방차량 추돌 MVA로 C/C 발생. 이후 업무상 사정으로 self management 해오시다 sx. aggravaiton tendency 있어서 이에 대한 보다 적극적 진료 위하여 본원 외래 내원. 
|01/20 타병원 진료-약처방
|상기 환자는 상기일에 오토바이 탑승 운행 중 타차량과 충돌 MVA로 C/C 발생. 이후 2020.01.05. ~ 2020.01.14. 미래로21H Adm Tx. 중 MR 등 Imagingt test상 Fx. of metatarsal bone/Dislocation of metatarsophalageal joint Dx. 이후  Trauma region Op.(2020.01.08. Pin inserting) 시행하였으며 2020.01.14 ~ 2020.02.03. 시원병원 Postoperative conservative Tx. 시행 후 잔여 소견에 대한 적극적 진료 위하여 본원 외래 내원. 
|상기 환자는 상기일에 보행자 추돌 MVA로 C/C 발생. 12월04일에서 23일까지 전대 병원 입원 치료 후 적극적 진료 위하여 2019년 12월 23일부터 27일까지 본원 입원치료 받음. 입원검사상 Rt AC joint의 탈구 소견 보여, 시원병원에서 시행한 추가영상검사상 양측성 AC joint 탈구로 확인되어 수술적 처치(관혈적 정복술 및 금속판 내고정술) 시행받고 2019년 12월 31일 재입원함.
|상기 환자는 농구선수로 활동하시던 중 장기간 상기의 소견으로 고생해오셨으며, 최근 자전거를 탄 후 상기의 SX. aggrvation tendency 있으므로 이에 대한 적극적 진료 위하여 본원 외래 내원.  
|2020.02.28 본원 OPD Tx. / XR imaging test : C spine : no specific HNP/ L spine : L4-5 HNP 의심/ shoulder : no fracture
|상기 환자는 상기의 소견으로 2020.03.05-2020.03.09 한사랑병원 Adm Tx.(XR, CT 상 non specific pathological finding) 후 잔여 소견 지속되므로 이에 대한 적극적 진료 및 further evaluation 위하여 본원 내원. 
|상기 환자는 상기와 같은 병력으로 증상에 대한 further evaluation및 Tx. 위하여 본원 OPD 내원.
|상기 환자는 상기일에 교차로 직진 주행중 우측면 차량 의하여 추돌 MVA로 C/C 발생. 이후 로컬 한의원 Acu Tx. 시행하였으나 증상 지속 악화경향 있어 이에 대한 적극적 평가 및 진료 위하여 본원 OPD 내원함.
|상기 환자는 상기일에 차량유턴 중 후방차량 추돌 MVA로 C/C 발생후 2020.03.16 ~ 2020.03.19. 천수당 한방병원 XR n-s detected. Adm-Tx. 시행하였으며 이후 잔여 소견에 대한 further evaluation 및 Tx. 위하여 본원 OPD visit. 
|상기 환자는 상기일에 차량 후방좌석 착석 유턴 중 후방차량 추돌 MVA로 C/C 발생. 이후 2020.03.16 한국병원 Brain CT n-s detected. 2020.03.16 ~ 2020.03.19. 천수당 한방병원 XR n-s detected. Adm-Tx. 시행하였으며 잔여증상에 대한 further evaluation 및 Tx. 위하여 본원 OPD visit. 
|상기 환자는 상기일에 차량 뒷좌석 착석 신호정차 중 후방 차량 추돌 MVA로 C/C 발생. 이후 이에 대한 보다 적극적 진료 위하여 본원 외래 내원. 
|상기 환자는 상기일에 차량 운전석 착석, 신호정차 중 후방차량 추돌 MVA로 C/C 발생. 이후 이에 대한 적극적 진료 위하여 본원 외래 내원.
|2020.03.03-04 본원 OPD Tx. 및 2020.03.03 L-spine XR, 2020.03.04 L-spine MRI : compression fx. of L1 Dx.하여 적극적인 한방치료 위해 본원 Adm.
|상기 환자는 상기일에 운전석 착석 주행 중 후방차량(미감속) 추돌 MVA로 C/C 발생. 이후 소견에 대한 evaluation 및 Tx. 위하여 본원 외래 내원. 
|상기 환자는 상기의 병력으로 본원 내원하신 분이며 2019.01.고도일병원 L-spine MR상 L4-5 HIVD 소견 들으심. 상기 증상의 계속적인 호전을 위하여 본원 외래 재내원하시어 on foot으로 509호 입원하심.
|상기 환자는 상기일에 조수석 착석, 신호정차 중 후진하던 전방차량과 충돌 MVA로 C/C 발생. 이후 당일 일곡병원 XR및 CT 상 non specific fx. 확인 후 2020.03.27-2020.03.30. 약손한방병원 Adm-Tx. 이후 이에 잔여소견에 대한 적극적 진료 위하여 본원 외래 내원. 
|상기 환자는 상기 일에 상기 C/C 발생하여 일상업무 및 생활 기능 장애 발생하여 이에 대한 적극적인 한의과적 치료위해 본원 외래 경유하여 on foot으로 1006호 입원하심.
|상기 환자는 상기일에 운전석 착석 우회전 중 타차량과 좌측면 충돌 MVA로 C/C 발생. 이후 이에 대한 보다 적극적인 진료 위하여 본원 외래 내원. 
|상기 환자는 상기의 소견으로 약 2개월간 지속적으로 고생해오시다 업무 효율 및 삶의 질이 저하되어 이에 대한 further evaluation 및 Tx. 위하여 본원 외래 내원함.
|상기 환자는 상기일에 오토바이 운전석 착석 정정차 중 중앙선 침범 타 차량 의하여 우측면 충돌 MVA로 오토바이 전복되어 상기 C/C 발생. 이후 이에 대한 적극적 evaluation 및 Tx 위하여 본원 외래 내원.
|상기 환자는 상기일에 차량 조수석 착석 신호정차 중 후방차량 추돌 MVA로 C/C 발생. 이후 이에 대한 evaluation 및 Tx. 위하여 본원 외래 내원.
|상기 환자는 상기일에 오토바이 운전석 착석 주행중 후방 차량의 좌측 끼어들기 중 측면 충돌로 오토바이가 전복되면서 상기의 C/C 발생. 이후 이에 대한 evaluation 및 Tx. 위하여 본원 외래 내원. 
|상기 환자는 상기일에 운전석 착석 신호정차 중 후방차량 추돌 MVA로 C/C 발생. 이후 이에 대한 보다 적극적인 evaluation 및 Tx. 위하여 본원 외래 내원.
|상기 환자는 상기일에 차량 조수석 착석 신호정차 중 후방차량 추돌 MVA로 C/C 발생. 이후 이에 대한 evaluation 및 Tx. 위하여 본원 외래 내원.
|상기 환자는 상기일에 운전석 착석 주행 신호감속 중 후방 차량 추돌 MVA로 C/C 발생. 2020.04.18 현대병원에서 C,L-spine, Rt knee joint XR imaging test 상 non specific fx. 확인. 이후 잔여 소견에 대한 적극적 진료 위하여 본원 외래 내원.
|상기 환자는 상기일에 상기와 같은 외상력에 의하여 통증 발생하여 이에 대한 적극적인 evaluation 및 Tx.위하여 본원 내원하여 1105호 on foot admission. 
|상기 환자는 상기일에 운전석 착석 신호정차 중 후방차량 추돌 MVA로 C/C 발생. 이후 이에 대한 보다 적극적 evaluation 및 Tx. 위하여 본원 외래 내원하여 on foot으로 502호 adm.
|상기 환자는 상기일에 조수석 착석 후방추돌 MVA로 C/C 발생. 이후 당일 한국병원 MSK XR imaging test 및 Brain CT상 non specific 확인. 잔여 소견에 대한 적극적 진료 위하여 본원 외래 내원.
|상기 환자는 상기일에 운전석 착석 후방추돌 MVA로 C/C 발생. 이후 당일 한국병원 MSK XR imaging test 및 Brain CT상 non specific 확인. 잔여 소견에 대한 적극적 진료 위하여 본원 외래 내원. 
|상기 환자는 상기일에 운전석 착석 고속도로 IC 감속 중 후방차량 추돌 MVA로 C/C 발생. 5월 9일 첨단병원, 5월 10일 선한병원 OPD XR imaging test 상 non specific fx. 확인하였으나 해당 기간 중 sx. aggravation tendency 뚜렷하므로 이에 대한 보다 적극적 진료 위하여 본원 외래 내원. 
|상기 환자는 상기일에 운동 중 외상으로 상기의 소견 발생하여 2020.04.29 ~ 2020.05.02. 상무병원 Adm Tx. 및 MR 상 내측 측부인대손상, 외측반월상 연골판 손상, 전방십자인대 손상 진단 후 보존적 치료 여부에 대한 상담 위하여 본원 외래 내원. 
|상기 환자는 평소 학교 선생님으로 근무하시던 중 장시간의 온라인 강의 제작 등으로 인한 업무 후 상기의 소견 발생하여 이에 대하여 Local 한의원 OPD Tx. 시행하였으나 상기 소견 지속되므로 이에 대한 적극적 Tx. 위하여 본원 외래 내원.
|상기 환자는 상기일 차량 조수석 착석 신호정차 중 후방차량 추돌 MVA로 C/C 발생. 이후 당일 상무병원 ER C,L-spine XR상 non specific fx. 확인. 이후 지속되는 잔여 소견에 대하여 적극적 진료 위하여 본원 외래 내원.   
|상기 환자는 약 1개월 전부터 상기의 소견으로 고생해오셨으며, 약 2주전 기독병원 Brain CT 및 CT angiography 상 non specific Dx. 받았으며  2020.05.08. 기독병원 Lab test 상으로도 특이소견 없으나 상단의 소견 지속되는 가운데 Cervical sx. 소견의 악화가 뚜렷하므로 이에 대한 보다 적극적 진료 위하여 본원 외래 내원.  
|상기 환자는 상기 일에 상기 C/C 발생하여 2020.05.25 본원 OPD-Tx 받았으나 지속되는 증상으로 적극적인 한방치료위해 본원 외래 경유하여 on foot으로 507호 입원하심.  
|상기 환자는 상기일에 운전석 착석 주행 중 좌측면 차량 충돌 MVA로 C/C 발생. 이후 이에 대한 보다 적극적 진료 위하여 본원 외래 내원.   
|상기 환자는 상기일에 운전석 착석 주행 중 좌측면 차량 충돌 MVA로 C/C 발생. 이후 이에 대한 보다 적극적 진료 위하여 본원 외래 내원.   
|2020.08월 중순경 타 한의원 약침 2회 치료, 증상 여전.  상기 환자는 상기일에 차량 우측 후방좌석 착석 신호정차 중 후방차량 추돌 MVA로 C/C 발생. 이후 self management 중 sx.aggravation tendency 있으므로 이에 대한 보다 적극적 진료 위하여 본원 외래 내원.   
|상기 환자는 상기일에 운전석 착석 주행 중 전방 차량 급감속에 의한 감속 중 후방차량 추돌 MVA로 C/C 발생. 2days self management 중 sx.aggravation tendency 있으므로 이에 대한 보다 적극적 진료 위하여 본원 외래 내원.   
|상기 환자는 상기일에 차량 조수석 착석 골목 사거리 주행 중 좌측방 차량 충돌 MVA로 C/C 발생하여 이에 대한 적극적 진료 위하여 본원 외래 내원.   
|상기 환자는 상기일에 차량 운전석 착석 3차선 주행 중 2차선 주행중이던 후방 덤프트럭 의하여 좌측면 타이어 충돌 MVA로 C/C 발생. 이후 이에 대한 보다 적극적 진료 위하여 본원 외래 내원.   
|상기 환자는 장기간 상기의 소견으로 고생해오시던 중 상기일 낙상으로 증상이 뚜렷하게 악화되었으며 이후 Local 의원 OPD Tx. 시행해오시다 호전 미흡하므로 2020.05.07. ~ 2020.05.21. 우리들 병원 Adm Tx. (MR상 spinal stenosis Dx. 후 2020.05.08. microscopic laser discectomy, L-spien Laminectomy) 시행. 이후 잔여 소견에 대한 보다 적극적 진료 위하여 본원 외래 내원.   
|상기 환자는 상기와 같은 소견으로 장기간 통증으로 고생하시다 이에 대한 보다 적극적 진료 위하여 본원 외래 내원.   
|상기 환자는 상기일에 운전석 착석 신호정차중 후방 차량 추돌 MVA로 C/C 발생. 이후 1day self management 중 sx.aggravation 소견 있으므로 이에 대한 보다 적극적인 evaluation 및 Tx. 위하여 본원 외래 내원.   
|상기 환자는 보행자로 골목길 보행 중 후진하는 차량 의하여 보행자-차량 충돌 MVA로 C/C 발생. 이후 1day self management 중 sx.aggravation tendency 있으므로 이에 대한 보다 적극적인 evaluation 및 Tx. 위하여 본원 외래 내원. **  
|상기 환자는 상기일경부터 발생한 상기의 소견으로 지속적으로 고생해오시다 이에 대한 further evaluation 및 Tx. 위하여 본원 외래 내원하심.   
|상기 환자는 상기 일에 차량 운전석 착석 주행 중 우측면 차량 충돌 MVA로 상기 C/C 발생하여 2020.07.22 본원 OPD-Tx 후 지속되는 증상에 대한 적극적인 한의과적 치료위해 본원 외래 경유하여 on foot으로 507호 입원하심.  
|상기 환자는 상기 일에 운전석 착석주행 중 후방 좌측면 차량충돌 MVA 후 충격에 의하여 전방차량 후방 2차충돌하여 상기 C/C 발생함. 이후 2020.07.21 전남대학교 ER Brain, Cervical, Chest, Abdomen CT 상 non specific structural injury finding. 이후 잔여 소견에 대한 적극적인 한의과적 치료위해 본원 외래 경유하여 on foot으로 1108호 입원하심.  
|상기 환자는 상기 일에 운전석 착석 주행 중 우천으로 인하여 도로변 가드레일에 충돌 MVA 발생하여 이후 4days self mangement 중 sx.aggravation tendency 있으므로 이에 대한 보다 적극적 진료 위하여 본원 외래 경유하여 on foot으로 504호 입원하심.   
|상기 환자는 상기일에 조수석 착석 주행 중 타차량 의하여 좌측면 충돌 MVA로 상기 C/C 발생하여 2020.07.31-2020.08.01 본원 OPD-Tx. 지속되는 증상에 대한 적극적 진료 위하여 본원 외래 경유하여 on foot으로 505호 입원하심.   
|상기 환자는 상기일에 운전석 착석 주행 중 차량 이상으로 인하여 전신주 차량 충돌(자손) MVA 후 C/C 발생. 이후 당일 소방차 활용하여 무안병원 ER visit XR imaging test (Pelvic, Rt wrist / Rt hand / C-spine / L-spine / Lt clavicle and rib) non specific finding. 잔여 소견 강도높게 지속되므로 이에 대한 적극적 진료 위하여 본원 외래 경유하여 504호 입원함.   
|상기 환자는 상기일에 조수석 착석 주행 중 차량 우측면 타 정차차량 충돌 MVA로 C/C 발생. 이후 소견 지속되므로 이에 대한 보다 적극적 진료 위하여 본원외래 경유하여 502호 입원하심.   
|상기 환자는 상기일에 운전석 착석 주행 중 차량 우측면 타 정차차량 충돌 MVA로 C/C 발생. 이후 소견 지속되므로 이에 대한 보다 적극적 진료 위하여 본원  상기 환자는 2004년 상기 C/C 발생하여 동아병원 Pelvic CT 상 ONFH detected 후 전남대학교 병원 femoral osteotomy(대퇴골두 회전술) 통하여 증상 호전.       이후 2018년경 증상 재발 경향 있어, 2019 전남대학교 병원 소견 상 secondary arthritis d/t ONFH(Rt.) 확인 후      2020.07.26.-2020.08.07. 조선대학교 병원 Adm TX. 및 2020.07.27. artificial joint replacement 후       잔여 소견에 대한 적극적 재활 치료 위하여 본원 외래 경유하여 1102호 입원하심.  
|상기 환자는 2020.08.24 버스 내에 서있는 상태에서, 버스 좌측면 타차량 충돌 MVA 의한 차내 충격으로 상기 C/C 발생하여 이후 당일 일곡병원 Adm Tx. (2020.08.24.-2020.08.25.) 및 XR imaging test(C,T-spine) 상 non specific finding. 확인 후 잔여 소견에 대한 적극적 진료 위하여 본원 외래 경유하여 501호 입원하심.  
|상기 환자는 평소 장시간 걸어야 하는 업무를 수행해오시던 중 상기일 경부터 돌연 외상력 없이 상기의 C/C 발생하여 일상생활 및 업무기능 저하 발생하므로 광주광역시 서울상무정형외과 OPD.에서 2020.09.09 XR 및 Diagnostic US 시행 후 MR rec. (medial/lateral meniscus tear suspected) 받아 이에 대한 보다 적극적 진료 위하여 본원 외래 경유하여 입원.  
|상기 환자는 상기일에 운전석 착석 우회전 위하여 감속 중 후방차량 추돌 의하여 C/C 발생. 이후 이에 대한 보다 적극적 진료 위하여 본원 외래 내원.   
|상기 환자는 상기일에 운전석 착석 이동 중 타 차량 의하여 차량 우측면 충돌 MVA 후 C/C 발생. 이후 이에 대한 보다 적극적 평가 및 진료 위하여 본원 외래        거쳐 adm.tx. 함.  
|상기 환자는 상기일에 운전석 착석 주행중 좌후측면 덤프트럭 차선 변경 중 좌후측방 충돌 MVA로 C/C 발생. 이후 2days self management 중 sx.aggravation tendency 있으므로 이에 대한 보다 적극적인 진찰 및 진료 위하여 본원 외래 내원.   
|상기 환자는 상기일경 가내 slip down으로 상기의 C/C 발생. 당일 상무병원 ER XR imaging test 상 Lt side femur shaft and subtrochanteric fracturefx. Dx. 당 병원 2day Adm ABR Tx. 이후 2020.08.24 ~ 2020.09.15 수완센트럴병원 Adm Tx. (with internal fixation at 2020.08.25.) 후 잔여 소견에 대한 progress monitoring 및 Rehab. Tx. 위하여 본원 내원.   
|상기 환자는 상기일에 운전석 착석 차량 주행 중 우측면 차량 충돌 MVA로 C/C 발생. 이후 1day self management 중 sx. aggravation tendency 있어 이에 대한 보다 적극적 진료 위하여 본원 외래 거쳐 adm.tx.함.  
|상기 환자는 평소 지속 재발되는 허리 통증으로 고생해오시던 중 상기일에 돌연 상기의 C/C 악화되어 수면 장애 및 일상생활 기능 저하 소견 뚜렷하여 2020.10.26. 선한병원 L-spine HIVD 소견 들으신 후 L-spine IDET 시술 (2020.10.27.) 받으신 후 ~2020.11.02. Adm Tx. 시행하였으나 소견 잔여된 상태로 이에 대한 보다 적극적 진료 위하여 본원 외래 내원.   
|상기 환자는 상기일에 운전석 착석 신호 정차 중 전방 차량 의하여 충돌 MVA로 C/C 발생. 이후 3days self manamgent 중 sx.aggravation tendency 있어 이에 대한 보다 적극적인 진료 위하여 본원 외래 내원.   
|상기 환자는 상기일에 운전석 착석 주행 중 양측면 차량 충돌 MVA로 C/C 발생. 이후 소견에 대한 assessment 및 Tx. 위하여 본원 외래 경유하여 adm.  
|상기 환자는 장기간 상기와 같은 소견으로 여러 의료기관 등 진료 수행하였으나 호전 미흡한 상태에서 보다 적극적 진료 위하여 본원 외래 거쳐 adm.tx.함  
|상기 환자는 장기간 상기의 소견으로 고생하시던 중 Local NS C-spine MR 상 Cervical spine myelopathy 진단 후 연세대학교 H 20.10.14. ~ 20.10.20. Adm Tx. 및 Lt side laminaplasty C3-6 level(2020.10.15.) 시행. 이후 20.10.21 ~ 20.11.07. 더나은병원 Adm Tx. (including manual therapy) 후 잔여 소견에 대한 OBS 및 management 위하여 본원 외래 거쳐 본원 adm.tx. 함.  
|상기 환자는 상기일에 운전석 착석 신호정차 중 음주운전 후방차량 의한 추돌 MVA로 C/C 발생. 이후 해당 소견에 대한 assessment 위하여 당일 21세기 병원 OPD XR imaging test상 non specific fx. 확인. 이후 2020.09.17. 잔여 소견에 대한 적극적인 진료 위하여 본원 외래 내원.   
|상기 환자는 상기일에 운전석 착석 차량 정차 중 돌연 우측면 차량 충돌 MVA로 C/C 발생. 이후 1day self management 중 sx.aggravation tendency 있어 이에 대한 보다 적극적 진료 위하여 본원 외래 경유하여 입원.  
|상기 환자는 상기의 소견으로 고생해오시다 2020.11.02. 문형래 OS서 MR상 Rotator cuff rupture 확인 후 arthroscopic rotator cuff repair 시행. 당 병원 2020.10.31 ~ 2020.11.13 Adm Tx. 이후 postoperative Rehab. 위하여 본원 외래 거쳐 adm.tx. 함.   
|상기 환자는 상기일경 업무 중 무거운 물건을 옮기시다가 C/C 발생. 이후 사내 한의원 OPD Tx. 시행하셨으며 2020.08.25. 우리들 병원 L-spine MR 상 L4-5, L5-S1 HIVD / spinal stenosis 소견 확인하시고 이에 대한 적극적 conservative Tx. 위하여 본원 외래 내원.   
|상기 환자는 약 30년간 무용 관련 교육 및 실무에 종사하시다 은퇴하신 후 현재 가사 하시는 중으로 상기의 소견 장기간 지속적으로 호소해오신 바 이에 대한 further evaluation 및 Tx. 위하여 본원 외래 내원하심.   
|상기 환자는 상기일에 운전석 착석 주행 중 우측면 차량 의하여 조수석 뒷면 충돌 MVA로 C/C 발생. 이후 이에 대한 보다 적극적인 진료 위하여 본원 외래 거쳐 adm.tx. 함.  
|상기 환자는 상기일에 운전석 착석 주행중 차량 우측면과 타 차량 도어 충돌 MVA로 C/C 발생. 2020.09.15~21. 인성한방병원 Adm Tx. (XR imaging test상 non specific / Discharge H-med 7days Px.) 이후 잔여 소견에 대한 적극적 진료 위하여 본원 외래 내원.   
|상기 환자는 상기일에 택시 조수석 착석 상태에서 좌측면 신호위반 차량 의하여 충돌 MVA로 C/C 발생(MVA 당시 운전석 기사와 두부 충돌로 syncope). 당일 119로 한국병원 ER visit 및 Adm Tx. start. Brain CT 및 Brain MR / Other site XR상 non specific finding. 이후 상기의 C/C 지속되므로 f/e Diangnostic US 시행 결과 Lt side rib fx. Dx. 한국병원 2020.09.29. ~ 2020.10.20. Adm Tx. 후 잔여소견에 대하여 적극적 진료 위하여 본원 외래 내원.   
|상기 환자는 상기일에 운전석 착석 이동 중 타차량과 전방충돌 MVA로 C/C 발생. 이후 self management 중 sx. 지속되므로 이에 대한 보다 적극적인 진료 위하여 본원 외래 내원. 
    
"""
ph_data="""
|- or 별무
|non specific medication at present. / No other past Op. Hx. 
|15years ago MVA d/t ankle, clavicle, L-spine fx. long term Hops. Adm Tx. 
|2019.03월경 꼬리뼈 골절
|	# HT(-) / DM(-) / Hepatitis (-) / Hyperlipidemia (-) 
|	# Op. History: non specific 
|	# Medication History: non specific 
|2years ago 첨단우리병원 Lt side ankle ligament rupture reconstruction op. 
|	non specific medicaiton at present. 
|3~4years ago, local ENT, sinusitis op.
|4year ago, Rt side upper arm fx d/t bone tumor. 이대분당병원 Op. (pin inserting state.)
|2000년경 정형외과 진료-mri상 척추전방전위증 소견
|	2017년경 좌측 눈 대상포진op
|	고지혈증약 복용중
|2019.09 DM Dx. Local IM dept. medicaiton QD PO
|	Hepatitis (-)., HT (-) 
|	#오리 알러지
|# 20년전 좌측 백내장 op
|	# 15년전 치질 op
|	# 10년전 좌측 아킬레스건 단열 op
|# HT(-) / DM(-) / Hepatitis (-) / Hyperlipidemia (-) 
|	# Op. History: none
|	# Medication History: none
|	# non specific medication at present. 
|HTN(-) / DM(-) / Hepatitis (-)
|  2019년, Local OS, Rt side shoulder joint ligament rupture, Lt side shoulder joint bursitis(suspected.) detected. PRP inj.
|  2019년, Local IM dept. Insomina (chronic), hypnotic medication intermittent. 
|  2018년, 전남대학교H. Brain MR상 Cerebral aneurysm (dia 0.3cm) detected. 
|  2017년(approx.), Local IM dept. Hyperlipedmia with fatty liver medication, respectively QD
|  2015년(approx.), Local IM dept. Hypothyroidism medication QD 
|4years ago Local IM HTN Dx. p.o.med. QD 
|3 years ago 전대병원 depression, insomnia dx. Remeron Tab. 15mg px.(현재복용안함) 
|   1.5 years ago local H insomnia dx. Lunapam Tab. 1mg 2T prn px. 
|   HTN(-) DM(-) Hyperlipidemia(-) Hepatitis(-) Tb(-) 
|2019.08 우리들병원 L-spine MR 상 L-spine HNP detected. Neuroplasty.
|   Op. History: From 10years ago, 하남성심병원 urolithiasis, Extracorporal Shock-Wave Therapy2 2times. 
|   HTN(-) DM(-) Hyperlipidemia(-) Hepatitis(-) Tb(-) Medication(-)
|2014.02.12 전대H Both TKRA op.
| 2014.02.12 전대H HTN dx. 
| DM(-) Hyperlipidemia(-) Hepatitis(-) Tb(-)
|7years ago 기독병원 L-spine MR 상 HIVD detected. 
|   4years ago 기독병원 neuroplasty 
|   HTN(-) DM(-) Hyperlipidemia(-) Hepatitis(-) Tb(-) Medication(-)
|<2020.07.02 임플란트 시술 후 med p.o> 로도질정 3T #TID 휴로펜정 3T #TID 휴모리드정5mg 3T #TID 리나치올캡슐 3T #TID 슈다페드정 1.5T #TID 헥사메딘액0.12% /  2days
|2014. 서울대학교 병원, thyroid carcinoma, Total thyroidectomy, medication QD P.O (Levothyroxine Sodium)
|   2013. 서울대학교 병원, Ovarian cystectomy.
|   HTN(-) DM(-) Hyperlipidemia(-) Hepatitis(-) Tb(-) 
|# HTN(-) DM(-) Dyslipidemia(-) Hepatitis(-) TBc(-)
|    # Op. History: 2019.05 cholesteatoma op. 
|    # Medication History: non specific medication at present
|# HTN(-) DM(-) Hyperlipidemia(-) Hepatitis(-) Tb(-)
|   # Op. History: 2019.01. 화순전대병원 acute cholecystitis. op. 
|   # Medication History: non specific at present
|25years ago, 기독병원, Rt ankle fx. Op. d/t motor vehicle collision
|   23years ago, local 병원 App. Op.
|   HTN(-) DM(-) Hyperlipidemia(-) Hepatitis(-) Tb(-) Medication (-)   
|HTN(+) / DM(-) / Hyperlipidemia(-) / Hepatitis(-) / Tb(-)
| # From 1years ago, L-spine상 L-spine HIVD detected.
| # Op. History: non specific 
| # Medication History: from 5years ago HTN medication QD 
|HTN(-) / DM(-) / Hepatitis (-) / Hyperlipidemia (-) / Tb(-) 
| # Op. History: 7years ago, 동아병원 Both side knee meniscus injury, reconstruction op. 
| # Medication History: 2019년 6월 Local IM dept. Xerostomia d/t Sjogren syndrome detected. medication BID P.O 
|HTN(-) DM(-) Hepatitis(-) Tb(-)
|From 3 years ago, local IM Hyperlipidemia dx. p.o.med  
| # Op.History : From 20years ago (exacly unknown), Rt side knee meniscus injury(suspected.) reconstruction op. 
| # Medication : 20.04.13 본원 FM 입원검사상 hyperlipidemia dx. 리피토정10mg 1T#1 SPC px.
|# HTN(-) / DM(-) / Hepatitis (-) / Hyperlipidemia (-) / Tbc(-)
|   # Op. History: non specific 
|   # Medication History: non specific medication at present
|# HT(-) / DM(-) / Hepatitis (-) / Hyperlipidemia (-) 
| # Op. History: non specific 
| # Medication History: non specific medication 
|# HT(-) / DM(-) / Hepatitis (-) / Hyperlipidemia (-) 
|# Op. History: Endometriosis (polyp) 2times op. 
|# Medication History: endometriosis medicaiton(호르몬제) BID P.O  // 프로베라정 10mg 4T # 2 / 에바티스정 1T -짝수날
|                      피부건조 소견 관련 약물 복약 중  
|# HTN(-) DM(-) Hyperlipidemia(-) Hepatitis (-) Tbc(-) 
|# Op. History: 2 years ago, 전남대병원 tonsillectomy op. 
|# Medication History: non specific medication at present
|# HT(-) / DM(-) / Hepatitis (-) / Hyperlipidemia (-) 
|# Op. History: non specific 
|# Medication History: non specific at present
|# HT(+) / DM(-) / Hepatitis (-) / Hyperlipidemia (-) 
|# Op. History: non specific 
|# Medication History
|- From 2wks ago, Local Oph muscae volitantes
|- From 3years ago, Local IM dept. HT medication QD 
|- From 1year ago, hyperthyroidism medication QD with progress monitoring 
| # HT(trace) / DM(-) / Hepatitis (-) / Hyperlipidemia (-) 
|    # Op. History: 2010, 연세대학교 병원, donor nephrectomy
|    # Medication History: From 4years ago, chronic insomnia ataractic agent BID P.O 
|# HT(-) / DM(-) / Hepatitis (-) / Hyperlipidemia (-) 
|    # Op. History: 2019년 화순중앙병원, Lt side ankle fx. op. 
|    # Medication History: - 
|# 2020.05.27 TA 본원 Adm Tx.(2020.05.28~06.01)
|# HT(-) / DM(-) / Hepatitis (-) / Hyperlipidemia (-) 
|    # Op. History: 10years ago, 상무병원, Otitis media, op. 
|    # Medication History:- 
|    # 4years ago, Local H. scoliosis Dx. 
|    # 비타민 주사제 알러지(+) : 전신 부종
|# HT(-) / DM(-) / Hepatitis (-) / Hyperlipidemia (-) 
|    # Op. History: 2019.04. 새나래병원 
|    # Medication History: non specific at present 
|    # 2019/04. 새나래 병원 C-spine MR HIVD detected. Neuroplasty 
|# HT(+) / DM(-) / Hepatitis (-) / Hyperlipidemia (-) 
|    # Op. History: non specific 
|    # Medication History: From 2months ago HT medication QD 
|    # Local H, Rt side elbow lat. epicodylitis Dx. medication/Inj. Tx. 
|# HT(-) / DM(-) / Hepatitis (-) / Hyperlipidemia (-) 
|    # Op. History:  2020.01. 한사랑병원 MR상 Lt side Knee arthritis detected. arthroscopic surgery
|                    2020.04. 밝은안과 21, Both side cataract Op. 
|    # Medication History: non specifc medication at present 
|# HT(-) / DM(-) / Hepatitis (-) / Hyperlipidemia (-) 
|    # Op. History: Prostate Ca. Op. (국립암센터, 5월 14일) / 6월 24일 follow up expectation 
|    # Medication History: non specific at pressent 
|# HT(+) / DM(+) / Hepatitis (-) / Hyperlipidemia (+)
|    # Op. History: 7~8years ago, Rotator cuff tear reconsturction op. (Rt.) 
|    # Medication History: 
|    - From 15years ago HT / DM / Hyperlipidemia medication BID P.O 
|    - Above 10years ago, 
|# HT(-) / DM(-) / Hepatitis (-) / Hyperlipidemia (-) 
|    # Op. History: Old, Lt side 3rd finger fx. 
|    # Medication History: non specific medication at present 
|# HT(-) / DM(-) / Hepatitis (-) / Hyperlipidemia (-) 
|    # Op. History: non specific 
|    # Medication History: 2days ago, Local dent. periodontitis Dx. Medication BID 
|# HTN(+) / DM(-) / Hepatitis (-) / Dyslipidemia (-) 
|    # Op. History: 2019년 현대병원 Lt side breast 0 stage CA op. / 전남대학교 병원 radiation therapy 
|                   2012년 서울 대한병원 rectal carcinoma initial stage op. 
|    # Medication History: From 6years ago, HTN med p.o 동아니세틸정 1T 투베로정30/5mg 1T 프레탈서방캡슐 100mg 1T
|    # From 60 years ago, residual poliomyelitis - Rt side lower limb 
|# HTN(-) DM(-) Dyslipidemia(-) Hepatitis(-) TBc(-) 
|    # Op. History: 2014년 우리들병원 Lt side knee joint meniscus rupture, reconstruction op. 
|                   1993년 5th floor fall down, Local OS Lt side femur fx.  
|    # Medication History: 2018 Local OS, Lt side Gonarthritis Dx. Medication BID. hyaluronate inj. Tx. 등 진행 
|# HTN(-) / DM(-) / Hepatitis (-) / Hyperlipidemia (-) Med(-)
|    # Op. History: 10 years ago approx. L-spine level 4-5 HIVD detected. neuroplasty Tx.    
| # HTN(-) DM(-) Dyslipidemia(-) Hepatitis(-) TBc(-)
|    # Op. History: 2017년 전남대학교 병원 endometriosis op.
|    # Medication History: From 3years ago endometriosis Dx. Post op. medication QD (비잔정, Dienogest 2mg 1T#MPC)     
| # HTN(+) DM(-) Dyslipidemia(-) Hepatitis(-) TBc(-)
|    # Op. History: 2019. 동아병원 CTS op.  
|    # Med : From 10years ago Local IM px.<HTN med> 아스피린프로텍트정100mg 1T#QD 노바스핀정5mg 1T#QD 
|            1 year ago Osteoporosis detected. Med 1 year P.O / discontionue at present
|    <세계로병원 6days prn> 스티렌정 2T#BID 미가드정2.5mg 2T#BID 타이레놀8시간이알서방정 2T#BID 환인그란닥신정 2T#BID 
|    <20.08.20 본원 FM px.> 비모보정500/20mg 1T BID / 네오펜틴캡슐100mg 1C 팜클로정250mg 1T 레바미피드정 1T TID / 바이버크림5g 1개 
|    # Allergy : 어패류     
|# HT(-) / DM(-) / Hepatitis (-) / Hyperlipidemia (-) 
|    # Op. History: non specific 
|    # Medication History: From 5~6years ago Allergic rhinitis, inhalent QD [Nasonex Nasal Spray QD]
|              sensonal asthma, medication QD [플루테롤 250/50 1T#1 QD]
|# Op. History: no op. Hx. not related to P/I
|# Op. History: 2018, 한국병원 Lt side ankle cyst, op. 
|          2019, 한국병원 Lt side ankle joint OLT, micropicking 
|          2019, 한국병원 Rt side shoulder joint, rotator cuff rupture reconstruction op. 
|# Op. History: 2009, 2013 순천새우리병원 L-spine HIVD, 2times op.
|# Medication History: From 8years ago, Local H, Gout Medication BID P.O
|# HT(-) / DM(-) / Hepatitis (-) / Hyperlipidemia (-) 
|    # Op. History: 3wks ago facelift op. 
|    # Medication History: non specific at present     
|# HT(-) / DM(-) / Hepatitis (-) / Hyperlipidemia (-) 
|    # Op. History: 15years ago, 전남대학교 병원 L-spine HIVD Op. 
|    # Medication History: non specific at present    

                                               """
drug_data="""

ex) 기통환QDPC-지속적 통증완화 및 경기 회복(당귀 오공 전갈 산수유 목향 등)
ex) 청풍탕TIDPC-급성기 염증완화(택사,저령,금은화,포공영,감초,육계 등).

청풍탕-급성기 염증완화(택사,저령,금은화,포공영,감초,육계 등).
호근탕-인대근육 손상회복, 통증완화(당귀,천궁,녹각,독활 등).
파어탕-온성활혈,이기지제(백출,단삼,계지,소목,홍화,향부자 등).
강척탕-인대근육 손상회복, 통증완화(숙지황,산수유,전충 등)
당귀수산-瘀血除去(당귀,소목,오약 등)
보중익기탕춘방-筋靭帶 緊張緩和(황기 감초 방풍 백출 등)
곽향정기산-解表化濕 理氣和中(곽향, 소엽 ,길경, 대복피, 대조 등)
오적산-신경통,관절통 완화 (창출,마황,진피,후박 등)
불면방-입면장애,천면증세 개선(산조인,상심자,단삼 등)
을자탕-(당귀,감초,대황,승마,시호 등)
기통환-지속적 통증완화 및 경기 회복(당귀 오공 전갈 산수유 목향 등).
관절고-진정 및 항염증 작용 (지황, 복령 등)
작약감초탕-柔肝解痙 緩急止痛 (백작약 감초)
계지복령환-祛瘀止痛 (계지 목단피 복령 작약 등) 
           
●신경근이완약침요법 - 자생한방병원원외탕전실에서 조제한 척추신처방 약침액을 사용한 약침시술, 약침액을 통증을 일으키는 신경근 주변조직에 안전하게 자입하여, 신경근 주변의 근육과 연조직을 이완시켜 신경에 가해지는 압박을 줄여 통증, 저림, 근력저하를 해소하는 효과가 있다.

●중성어혈약침 - 자생한방병원원외탕전실에서 조제한 중성어혈 약침액을 사용한 약침시술/ 통증을 완화시킬 수 있는 경혈에 대해 약침액을 자입하는 것이며, 진통, 소염의 효과가 있다.
-1vial 당 2ml이상 (hGMP적작약, hGMP단삼, hGMP도인, hGMP몰약, hGMP현호색, hGMP유향, hGMP소목, hGMP치자)

●특수이완약침요법 - 자생한방병원원외탕전실에서 조제한 근이완 약침액을 사용한 약침시술/ 근육을 이완시킬 수 있는 경혈에 대해 약침액을 자입하는 것이며, 진통, 근육이완의 효과가 있다.
-1vial 당 2ml이상 (hGMP백작약, hGMP감초)

●BV1 (봉약침 5%)  (20,000:1) 1vial 당 2ml이상 (봉독 5%) 
"""

#=========================subjective======================
################################## Subjective widgets
ui_title = widgets.HTML("<p/><center><h3>----------------------------------------</h3></center><p/><center><H2>JS's Progress Note in CY</H2><center><p/><center><h3>----------------------------------------</h3></center><p/>")


#=========================subjective======================
################################## Subjective widgets
layout_in = Layout(width='auto')
layout_sub_out = Layout(width='47%')
layout_cc_out = Layout(width='25%')

w_subjective_label = widgets.Label('주관적 호소 : ')
w_cc_label = widgets.Label('C/C : ')

w_subjective_text_list = [widgets.Text('#1 ', layout=layout_in)] # 500
vb_subjective_text_list = widgets.VBox(w_subjective_text_list, layout=layout_sub_out)

w_cc_text_list = [widgets.Text('1. ', layout=layout_in) ]  # 240
vb_cc_text_list = widgets.VBox(w_cc_text_list, layout=layout_cc_out)


w_subjective_plus_btn = widgets.Button(description = '', layout=Layout(width='45px'), button_style='', icon='plus') 
w_subjective_minus_btn = widgets.Button(description = '', layout=Layout(width='45px'), button_style='',icon='minus') 
hb_subjective_btn_list = widgets.HBox([w_subjective_plus_btn, w_subjective_minus_btn])

################################## Subjective func
def f_subjective_plus(b):        
    # 핵심
    vb_subjective_text_list.children=tuple(list(vb_subjective_text_list.children) + [widgets.Text(f'#{len(list(vb_subjective_text_list.children))+1} ', layout=layout_in)]) 
    vb_cc_text_list.children=tuple(list(vb_cc_text_list.children) + [widgets.Text(f'{len(list(vb_cc_text_list.children))+1}. ', layout=layout_in)]) 
def f_subjective_minus(b):       
    ## 뺄때는 1개는 남아있어야한다.
    if len(list(vb_subjective_text_list.children)) > 1:
        # 핵심
        vb_subjective_text_list.children=tuple(list(vb_subjective_text_list.children)[:-1]) 
        vb_cc_text_list.children=tuple(list(vb_cc_text_list.children)[:-1]) 
    ## 뼀을때 1개가 남으면, 그 내용을 짖우기 
    elif len(list(vb_subjective_text_list.children)) == 1:
        vb_subjective_text_list.children[0].value = "#1 "
        vb_cc_text_list.children[0].value = "1. "
    else:
        pass
    
w_subjective_plus_btn.on_click(f_subjective_plus)
w_subjective_minus_btn.on_click(f_subjective_minus)    
    
############################### Subjective ui
ui_s = widgets.HBox([w_subjective_label,vb_subjective_text_list,hb_subjective_btn_list, w_cc_label, vb_cc_text_list])

#=========================disease======================
################################## disease widget
import panel as pn
pn.extension('vega')

w_disease_search = pn.widgets.AutocompleteInput(
#     name='상기 증상에 따른 상병입력 : ', 
    options=v_disease_search_list,
    placeholder='ex> S3350 대문자로 입력시작!', 
    width=400)
w_disease_plus_btn = pn.widgets.Button(name='+', width=30)
w_disease_minus_btn = pn.widgets.Button(name='-', width=30)
w_disease_del_btn = pn.widgets.Button(name='전체삭제', width=50)
w_disease_output = pn.widgets.StaticText(value='입력될 상병표시', height=150) # 전체가 200임

v_disease_dict={}
v_disease_list = []
n = 0


################################## disease functions


def f_disease_plus(event):
            
    global v_disease_dict
    global v_disease_list
    global n
    n+=1
    
    ## 잘못입력된 경우1 : (자동완성x)
    if w_disease_search.value not in v_disease_search_list:
        w_disease_search.value = " " # "" 안됨 한칸 띄우기 " "
        w_disease_search.value = ""
        w_disease_search.placeholder="자동완성을 통해 입력해주세요."
        
        ## 잘못입력 되돌리기####################
        if n>=1:n -= 1
        ## list에 들어있는 것을 string으로 변환해서 표기 
        output_string =f"[{len(v_disease_list)}]"
        for i, s in enumerate(v_disease_list):
            output_string += f" {s}\n"
        w_disease_output.value = f'[error 다시입력 요망] ' + output_string
        pass
        
    else:

        
        ## 잘못입력된 경우2 : (자동완성해서 들어왔지만, 이미 dict or list에 입력된 상병)
        if w_disease_search.value in v_disease_dict.values():
            w_disease_search.value = " " # "" 안됨 한칸 띄우기 " "
            w_disease_search.value = ""
            w_disease_search.placeholder="ex> S3350 대문자로 입력시작!"
            w_disease_output.value = f'[error] 이미 추가된 상병입니다.'
            ## 잘못입력 되돌리기####################
            if n>=1:n -= 1
            ## list에 들어있는 것을 string으로 변환해서 표기 
            output_string =f"[{len(v_disease_list)}]"
            for i, s in enumerate(v_disease_list):
                output_string += f" {s}\n"
            w_disease_output.value = output_string
            w_disease_output.value = f'[error 이미 추가된 상병입니다.] '+output_string_string

            pass
            
        
        ## 드디어 정상 입력 
        ## 횟수가 key / 상병기호가 value
        if n not in v_disease_dict.keys():
            v_disease_dict[n] = ""
            
        v_disease_dict[n]+=f"{w_disease_search.value}"
        v_disease_list.append(f"{w_disease_search.value.split(':')[0].strip()}")

        ## list에 들어있는 것을 string으로 변환해서 표기 
        output_string =f"[{len(v_disease_list)}]"
        for i, s in enumerate(v_disease_list):
            output_string += f" {s}\n"
        w_disease_output.value = output_string
               
                     
        w_disease_search.value = '' # placeceholder 뜨도록 
    
    
def f_disease_minus(event):
    global n
    global v_disease_dict
    global v_disease_list
   
    # 리스트가 존재하면,제일 마지막꺼를 제거
    if len(v_disease_list)>0:
        v_disease_list.pop()
    else:
        pass                       
    
    # dict에서도 제거   
    del v_disease_dict[n]
    # 숫자 하나 줄이기 
    if n>=1:n -= 1
    
                       
    output_string =f"[{len(v_disease_list)}]"
    if len(v_disease_list) >0:
        for i, s in enumerate(v_disease_list):
            output_string += f" {s}\n"
    else:
        pass
    w_disease_output.value = output_string # 버튼.click에는 클릭횟수가 나와있다. 자동으로 증가한다.

    
def f_disease_del(event):
    global n
    n=0
    global v_disease_dict
    global v_disease_list
    
    v_disease_dict = {}
    v_disease_list = []
    w_disease_search.value = ' '
    w_disease_search.value = ''
    w_disease_search.placeholder = 'ex> S3350 대문자로 입력시작!'
    w_disease_output.value = '기존 등록 상병을 다 삭제함.'
    
w_disease_plus_btn.on_click(f_disease_plus)
w_disease_minus_btn.on_click(f_disease_minus)
w_disease_del_btn.on_click(f_disease_del)

row_disease = pn.Row(w_disease_search, w_disease_plus_btn, w_disease_minus_btn, w_disease_output, w_disease_del_btn, height=200)


#=========================o/s======================
################################## o/s widget
layout_fixed_label=Layout(width='40px')
layout_fixed_btn=Layout(width='45px')

w_os_label = widgets.Label('O/S : ', layout=layout_fixed_label)
w_os_picker = widgets.DatePicker(
        value = datetime.datetime.now().date(),
        description='',
        layout=Layout(width='150px'), # 고정!
)
w_os_text_label = widgets.Label('상세 : ', layout=layout_fixed_label)
w_os_text = widgets.Text(
      value='',
      placeholder="<- 년-월-일 정확하지 않다면, 아예 del삭제 후 [ 2020.05 / 상세내용 ] 직접작성",
      description='',
    layout=Layout(width="60%")
        
)

w_os_btn = widgets.Button(description = '', layout=layout_fixed_btn, button_style='', icon='info') 

################################## o/s ui
ui_os = widgets.HBox([w_os_label, w_os_picker,w_os_text_label, w_os_text, w_os_btn])




#=========================p/i======================
################################## p/i widget
layout_pi_text_out = Layout(width="70%")

w_pi_label = widgets.Label('P/I : ', layout=layout_fixed_label,)

w_pi_text_list = [widgets.Text('',
                               placeholder="상기 환자는 상기일에 상기와 같은 MVA로 C/C 발생. 이후 당일 해피퓨병원 OPD XR 상 non specific fx. 확인. 잔여 소견에 대한 적극적 진료 위하여 본원 외래 내원. ",
                               layout=Layout(width='auto')
                              )] 
vb_pi_text_list = widgets.VBox(w_pi_text_list, layout=Layout(width="70%"))

w_pi_plus_btn = widgets.Button(description = '', layout=layout_fixed_btn, button_style='', icon='plus') 
w_pi_minus_btn = widgets.Button(description = '', layout=layout_fixed_btn, button_style='', icon='minus') 
w_pi_info_btn = widgets.Button(description = '', layout=layout_fixed_btn, button_style='', icon='info') 
hb_pi_btn_list = widgets.HBox([w_pi_plus_btn, w_pi_minus_btn, w_pi_info_btn])


################################## p/i functions 
def f_pi_plus(b):        
    # 핵심
    vb_pi_text_list.children=tuple(list(vb_pi_text_list.children) + [widgets.Text(f'', layout=Layout(width='auto'))]) 
    
def f_pi_minus(b):       
    ## 뺄때는 1개는 남아있어야한다.
    if len(list(vb_pi_text_list.children)) > 1:
        # 핵심
        vb_pi_text_list.children=tuple(list(vb_pi_text_list.children)[:-1]) 
    ## 뼀을때 1개가 남으면, 그 내용을 짖우기 
    elif len(list(vb_pi_text_list.children)) == 1:
        vb_pi_text_list.children[0].value = ""
    else:
        pass
    
################################## p/i ui 
ui_pi = widgets.HBox([w_pi_label,vb_pi_text_list,hb_pi_btn_list])

w_pi_plus_btn.on_click(f_pi_plus)
w_pi_minus_btn.on_click(f_pi_minus)


#=========================p/h check & text======================
################################## p/h check widget
layout_fixed_checkbox=Layout(width='auto' )

w_ph_1_label = widgets.Label('P/H : ', layout=layout_fixed_label)


cb_ph_htn = widgets.Checkbox(description="HTN", layout=layout_fixed_checkbox, indent=False,) # checkbox는 indent=False 필수
cb_ph_dm = widgets.Checkbox(description="DM", layout=layout_fixed_checkbox, indent=False,)
cb_ph_lipid = widgets.Checkbox(description="Hyperlipidemia", layout=layout_fixed_checkbox, indent=False,)
cb_ph_hepa = widgets.Checkbox(description="Hepatitis", layout=layout_fixed_checkbox, indent=False,)
cb_ph_tb = widgets.Checkbox(description="Tb", layout=layout_fixed_checkbox, indent=False,)
cb_ph_op= widgets.Checkbox(description="OP history", layout=layout_fixed_checkbox, indent=False,)

hb_ph_check_list = widgets.HBox([cb_ph_htn, cb_ph_dm, cb_ph_lipid, cb_ph_hepa, cb_ph_tb, cb_ph_op],
                               layout=Layout(width='92%'))
################################## p/h check ui
ui_ph_1_check = widgets.HBox([ w_ph_1_label, hb_ph_check_list])

################################## p/h text widget
layout_ph_2_text_out = Layout(width='70%')

w_ph_2_label = widgets.Label('      ', layout=layout_fixed_label)

w_ph_2_text_list = [widgets.Text('',
                               placeholder="non specific medication at present. / No other past Op. Hx.",
                               layout=layout_in
                              )] 
vb_ph_2_text_list = widgets.VBox(w_ph_2_text_list, layout=layout_ph_2_text_out)


w_ph_2_plus_btn = widgets.Button(description = '', layout=layout_fixed_btn, button_style='' , icon='plus') 
w_ph_2_minus_btn = widgets.Button(description = '', layout=layout_fixed_btn, button_style='', icon='minus') 
w_ph_2_info_btn = widgets.Button(description = '', layout=layout_fixed_btn, button_style='', icon='info') 
hb_ph_2_btn_list = widgets.HBox([w_ph_2_plus_btn, w_ph_2_minus_btn, w_ph_2_info_btn])

################################## p/h text func
def f_ph_2_plus(b):        
    # 핵심
    vb_ph_2_text_list.children=tuple(list(vb_ph_2_text_list.children) + [widgets.Text(f'', layout=layout_in)]) 
    
def f_ph_2_minus(b):       
    ## 뺄때는 1개는 남아있어야한다.
    if len(list(vb_ph_2_text_list.children)) > 1:
        # 핵심
        vb_ph_2_text_list.children=tuple(list(vb_ph_2_text_list.children)[:-1]) 
    ## 뼀을때 1개가 남으면, 그 내용을 짖우기 
    elif len(list(vb_ph_2_text_list.children)) == 1:
        vb_ph_2_text_list.children[0].value = ""
    else:
        pass
    

################################## p/h text ui
ui_ph_2_text = widgets.HBox([w_ph_2_label,vb_ph_2_text_list,hb_ph_2_btn_list])

w_ph_2_plus_btn.on_click(f_ph_2_plus)
w_ph_2_minus_btn.on_click(f_ph_2_minus)


#=========================bj======================
################################## bj widget
layout_변증종류 = Layout(width='220px')  #고정
layout_변증소견 = Layout(width='200px')  #고정

w_bj_label = widgets.Label('변증 : ', layout=layout_fixed_label)

w_bj_변증_select = widgets.Select(options=bj_category_dict.keys(),
                                layout=Layout(width='220px'), indent=False,
                                )# 1. 딕셔너리 키값들을 select에 옵션으로 주어 select위젯 객체 만들기
v_bj_변증 = w_bj_변증_select.value# 2. select객체의 선택된 value를 받아, 2번재 select로 데려갈 준비를 한다. /  각종 부위 필요할 때 쓰인다.
w_bj_소견_select = widgets.Select(options=bj_category_dict[v_bj_변증],
                                layout=layout_변증소견, indent=False,) # 3. 선택된key로 받은 list값으로 새로운 select 위젯에 option으로 준다.

################################## bj func
# INTERACTIVE1 : 변증 -dict-> 소견리스트 -> 소견select 옵션으로 
def f_select_변증_to_소견(종류):
    w_bj_소견_select.options = bj_category_dict[종류]

# INTERACTIVE2 : 혈자리 -> str_final_hjr 입력
str_final_bj  = ""
str_final_bj_code = ""
def f_select_소견_to_string(소견):
    # 소견을 통해 나오는 dict의 value는  ['U612', """[변증]   [변증소견]"""] 형태이므로 
    # 앞쪽의 code는 str_final_bj_code 에 저장해놨다가 -> 나중 str_final_disease에 추가되어야한다.
    v_bj_code, v_bj_소견 = bj_code_str_dict[소견]
    
    global str_final_bj_code
    global str_final_bj
    
    # 코드는 괄호에, key인 소견은 앞에 문자열로
    str_final_bj_code = 소견 + f" ({v_bj_code})"
    str_final_bj = v_bj_소견

################################## bj ui
ui_bj_1 = widgets.interactive(f_select_변증_to_소견, 종류=w_bj_변증_select)
ui_bj_2 = widgets.interactive(f_select_소견_to_string, 소견=w_bj_소견_select) # 5. 선택된key값을 기준으로 2번재 위젯에 옵션을 주는 함수 + 인자로 1번째 select위젯을 걸어준다.

# label + 유형select + int select 2개
ui_bj = widgets.HBox([w_bj_label, ui_bj_1,ui_bj_2])



#=========================hjr======================
################################## hjr widget
w_hjr_label = widgets.Label('침 :' , layout=layout_fixed_label)

w_hjr_유형_select = widgets.Select(options=['자보(침술2종)','국건(침술3종)'],
                                layout=Layout(width='auto', ),
                                 indent=False,
                                )#
w_hjr_부위_select = widgets.Select(options=hjr_dict.keys(),
                                layout=Layout(width='auto',),
                                )# 1. 딕셔너리 키값들을 select에 옵션으로 주어 select위젯 객체 만들기
v_hjr_부위 = w_hjr_부위_select.value# 2. select객체의 선택된 value를 받아, 2번재 select로 데려갈 준비를 한다. /  각종 부위 필요할 때 쓰인다.
w_hjr_혈위_select = widgets.Select(options=hjr_dict[v_hjr_부위],
                                 layout=Layout(width='auto'),
                                ) # 3. 선택된key로 받은 list값으로 새로운 select 위젯에 option으로 준다.


w_hjr_plus_btn = widgets.Button(description = '+2차침', layout=Layout(width='50%'), button_style='', icon='') 
w_hjr_minus_btn = widgets.Button(description = '초기화', layout=Layout(width='50%'), button_style='', icon='') 
w_hjr_btn_text = widgets.Textarea("입원용 2차침 지정하려면 [+2차침] -> 침 다시 선택",  
                                  layout=Layout(width='auto', height='172px'))
hb_hjr_btn = widgets.VBox([
                            widgets.HBox([w_hjr_plus_btn, w_hjr_minus_btn]), 
                           w_hjr_btn_text
                        ])


################################## hjr functions
v_hjr_str_list = []
def f_hjr_plus(b):        
    global v_hjr_str_list
    # 현재 선택된 혈자리를 1차로 저장해놓는다.
    # string저장시 잡것들빼고 부위 + 혈자리는 [v_hjr_string]에 들어가 있다.
    global v_hjr_string
    
    if len(v_hjr_str_list) > 0:
        w_hjr_btn_text.value = '이미 1차침이 들어가있어요.'
        pass
    else:
        v_hjr_str_list.append("(1차)" + v_hjr_string)
        w_hjr_btn_text.value = '클릭전 침자리가 1차로 저장됨. 2차는 선택만!'
        
def f_hjr_minus(b):       
    global v_hjr_str_list
    ## 뺄때는 1개는 남아있어야한다.
    if len(v_hjr_str_list) > 0:
        v_hjr_str_list = []
        w_hjr_btn_text.value ='처음부터 혈자리 선택해주세요.'
    else:
        w_hjr_btn_text.value ='아직 삭제할 침set가 없어요.'
    
w_hjr_plus_btn.on_click(f_hjr_plus)
w_hjr_minus_btn.on_click(f_hjr_minus)

v_str_hjr_유형 =""
def f_select_유형(유형):
    global v_str_hjr_유형
    v_str_hjr_유형 = 유형
    
# INTERACTIVE1 : 부위 -dict-> 혈위 -> 혈위select 옵션으로 
def f_select_부위_to_혈위(부위):
    w_hjr_혈위_select.options = hjr_dict[부위]

# INTERACTIVE2 : 혈자리 -> str_final_hjr 입력
str_final_hjr  = ""
v_hjr_string = ""
def f_select_혈위_to_string(혈위):
    혈위 = 혈위.split('/') # 3번째 침술이 있던 없던 /로 끝나게 해서 split되서 2개or3개를 고르게 한다.

    # 자보/국건을 여기서 선택받아서 혈위 2종/3종을 구분한다.
    # 또한 string만들대,select-select 중간에 받아둔 v_hjr_부위를 활용해서 부위를 입력시킨다.
    global w_hjr_부위_select
    global v_hjr_부위
    global w_hjr_부위_select
    v_hjr_부위 = w_hjr_부위_select.value# 2. select객체의 선택된 value를 받아, 2번재 select로 데려갈 준비를 한다. /  각종 부위 필요할 때 쓰인다.
    
    # interactive로 받아놓은 유형 string(str_hjr_유형)을 가지고 자보vs국건을 판단.
    global v_hjr_string # 2차 추가할때 챙기려고 global로 만들었다.
    if '자보' in v_str_hjr_유형:
        # 분구침일때는 분구침술 - 부위 형태로
        if '분구침술' in 혈위:
            v_hjr_string = f"{v_hjr_부위} - 분구침술"
        else:
            v_hjr_string = f"{v_hjr_부위} (이체간:{혈위[0]})(투자법:{혈위[1]})"
    else: # 국건
        if '분구침술' in 혈위:
            v_hjr_string = f"{v_hjr_부위} - 분구침술"
        else:
            v_hjr_string = f"{v_hjr_부위} (이체간:{혈위[0]})(투자법:{혈위[1]})({혈위[2]})"


    global str_final_hjr
    str_final_hjr="P)\n- 침치료(EA) : " # 인터랙티브일때는  (클릭마다 수행되므로) 내부에서 처음시작을 +=이 아니라 =으로 초기화해서 시작하자.
    global v_hjr_str_list
    if len(v_hjr_str_list) ==1:
        # 2차침 추가하여 v_hjr_str_list에 (1차) 부위 (혈자리)로 먼저 저장해놓은 경우
        str_final_hjr+= v_hjr_str_list[0] + "\n" + "               (2차)" + v_hjr_string +"\n"
    else:
        # 2차침 추가가 없는 경우
        str_final_hjr+= v_hjr_string + "\n"

################################## hjr ui 
ui_hjr_0 = widgets.interactive(f_select_유형, 유형=w_hjr_유형_select)
ui_hjr_1 = widgets.interactive(f_select_부위_to_혈위, 부위=w_hjr_부위_select) # 5. 선택된key값을 기준으로 2번재 위젯에 옵션을 주는 함수 + 인자로 1번째 select위젯을 걸어준다.
ui_hjr_2 = widgets.interactive(f_select_혈위_to_string, 혈위=w_hjr_혈위_select)# 4. 목록출력 함수 + 그 인자로 2번재select위젯을 넣어준다.

# label + 유형select + int select 2개
ui_hjr = widgets.HBox([ w_hjr_label,widgets.VBox([widgets.HBox([ui_hjr_0, ui_hjr_1]),
                                                                                   ui_hjr_2,]),           hb_hjr_btn])


#=========================chuna======================
################################## chuna widget
w_chuna_label = widgets.Label('추나 : ')

w_chuna_1_select = widgets.Select(options=chuna_category_dict.keys(),
                                layout=Layout(width='250px'),
                                  description='종류'
                                )# 1. 딕셔너리 키값들을 select에 옵션으로 주어 select위젯 객체 만들기
v_chuna = w_chuna_1_select.value# 2. select객체의 선택된 value를 받아, 2번재 select로 데려갈 준비를 한다. /  각종 부위 필요할 때 쓰인다.
w_chuna_2_select = widgets.Select(options=chuna_category_dict[v_chuna],
                                  description = '상세 종류'
#                                  layout=Layout(width='400px'),
                                ) # 3. 선택된key로 받은 list값으로 새로운 select 위젯에 option으로 준다.


################################## chuna functions
def f_select_chuna(widget_추나):
    w_chuna_2_select.options = chuna_category_dict[widget_추나]
    
str_final_chuna  = ""
def f_select_chuna_to_string(widget_추나부위):
    global str_final_chuna
    str_final_chuna = chuna_str_dict[widget_추나부위]

################################## chuna ui    
ui_chuna_1 = widgets.interactive(f_select_chuna, widget_추나=w_chuna_1_select)
ui_chuna_2 = widgets.interactive(f_select_chuna_to_string, widget_추나부위=w_chuna_2_select) 

ui_chuna = widgets.HBox([w_chuna_label, ui_chuna_1, ui_chuna_2])



#=========================os======================
################################## os widget
layout_fixed_label=Layout(width='40px')
layout_fixed_btn=Layout(width='45px')

w_os_label = widgets.Label('O/S : ', layout=layout_fixed_label)
w_os_picker = widgets.DatePicker(
        value = datetime.datetime.now().date(),
        description='',
        layout=Layout(width='150px'), # 고정!
)
w_os_text_label = widgets.Label('상세 : ', layout=layout_fixed_label)
w_os_text = widgets.Text(
      value='',
      placeholder="<- 년-월-일 정확하지 않다면, 아예 del삭제 후 [ 2020.05 / 상세내용 ] 직접작성",
      description='',
    layout=Layout(width="60%")       
)
w_os_btn = widgets.Button(description = '', layout=layout_fixed_btn, button_style='', icon='info') 

################################## os ui
ui_os = widgets.HBox([w_os_label, w_os_picker,w_os_text_label, w_os_text, w_os_btn])



#=========================drug======================
################################## drug widget
layout_fixed_picker = Layout(width='150px')
layout_drug_out = Layout(width='50%')

# 한약 체크여부
w_drug_check = widgets.Checkbox(
    value=False,
    description='한약',
    disable = False,
    indent=False, layout=layout_fixed_checkbox,
)
w_drug_picker_list = [widgets.DatePicker(
    value = datetime.datetime.now().date(),
    #description='시작일',
    disabled=True,
    layout=layout_fixed_picker, # picker 고정
)]
vb_drug_picker_list = widgets.VBox(w_drug_picker_list)
w_drug_text_list = [widgets.Text(
    #description='처방 정보 :',
    value='',
    placeholder=' XX탕 2ch#2 BIDPC - 적응증: 급성 통증의 억제 및 근긴장, 염증 완화 (독활, 천궁, 우슬 등)',
    disabled=True,
    layout=layout_in
)]

# text + picker 한 묶음..으로 연장
vb_drug_text_list = widgets.VBox(w_drug_text_list, layout=layout_drug_out)


w_drug_plus_btn = widgets.Button(
    description='',
    disabled=True,
    button_style ='', # success
    tooltip='click me',
    icon='plus',
    layout=layout_fixed_btn,
)
w_drug_minus_btn = widgets.Button(
    description='',
    disabled=True,
    button_style ='', # success
    tooltip='click me',
    icon='minus',
    layout=layout_fixed_btn,
)
w_drug_info_btn = widgets.Button(
    description='',
    disabled=True,
    button_style ='', # success
    tooltip=drug_data,
    icon='info',
    layout=layout_fixed_btn,
)

################################## drug ui
ui_drug = widgets.HBox([w_drug_check, vb_drug_picker_list, vb_drug_text_list, w_drug_plus_btn, w_drug_minus_btn, w_drug_info_btn])

################################## drug functions
w_drug_except_check = list(vb_drug_picker_list.children) +list(vb_drug_text_list.children) + [w_drug_plus_btn, w_drug_minus_btn]
def f_drug_observer(change):
    if change['new'] == True:
        # check밑으로 달린 애들 모두 활성화 ( disabled=False)
        for widget in w_drug_except_check:
            widget.disabled=False
    else:
        # check밑으로 달린 애들 모두 disabled
        for widget in w_drug_except_check:
            widget.disabled=True
def f_drug_plus(b):        
    # picker에 자식추가.
    vb_drug_picker_list.children=tuple(list(vb_drug_picker_list.children) + [
        widgets.DatePicker(
            value = datetime.datetime.now().date(),
            #description='시작일',
            disabled=False,
            layout=layout_fixed_picker,
        )
    ]) 
    # text에  자식추가.
    vb_drug_text_list.children=tuple(list(vb_drug_text_list.children) + [
        widgets.Text(
    #description='처방 정보 :',
    value='',
    placeholder=' XX탕 2ch#2 BIDPC - 적응증: 급성 통증의 억제 및 근긴장, 염증 완화 (독활, 천궁, 우슬 등)',
    disabled=False,
    layout=layout_in
    )]) 
def f_drug_minus(b):       
    ## 뺄때는 1개는 남아있어야한다.
    if len(list(vb_drug_picker_list.children)) > 1:
        # 핵심
        vb_drug_picker_list.children=tuple(list(vb_drug_picker_list.children)[:-1]) 
        vb_drug_text_list.children=tuple(list(vb_drug_text_list.children)[:-1]) 
    ## 뼀을때 1개가 남으면, 그 내용을 짖우기 
    elif len(list(vb_drug_text_list.children)) == 1:
        vb_drug_text_list.children[0].value = ""
    else:
        pass

w_drug_check.observe(f_drug_observer, names='value')
w_drug_plus_btn.on_click(f_drug_plus)
w_drug_minus_btn.on_click(f_drug_minus)

#=========================plans======================
################################## plans widget
layout_plans_select = Layout(width='200px', height='80px')

v_plans_부위_list = []

w_plans_check = widgets.Checkbox(
    value=False,
    description='부항,물치-부위 & 뜸-혈위',
    disable = False,
    indent=False, layout=layout_fixed_checkbox,
)
# SELECT 1 from check observe
w_plans_부위_select = widgets.Select(
    options=["경항부", "체크해주세요"],
    description = '부위',
    layout=layout_plans_select,
    )
w_plans_부위_select.disabled=True
v_plans_부위 = w_plans_부위_select.value

# SELECT 2 from select 1 
w_plans_혈자리_select = widgets.Select(
    options=np.unique([ 혈자리.split('/')[:2] for 부위 in v_plans_부위_list for 혈자리 in hjr_dict[v_plans_부위]]).tolist(),
    layout=layout_plans_select,
    description = '혈위',
    disable = True,
) 
w_plans_혈자리_select.disabled=True

################################## plans functions 
# INTERACTIVE1 : 
def f_plans_select_부위_to_혈자리(widget_부위):
    # 만약, 분구침이라면 구체적인 혈자리가 없어서, 혈자리 split해서 [:2]로 혈자리 옵션 주는 것을 할 수 없다.
    # 부위->혈자리 에서, 컴프리핸션에 if로 필터를 걸자
    w_plans_혈자리_select.options = np.unique(
                                        [ 혈자리.split('/')[:2] for 부위 in v_plans_부위_list for 혈자리 in hjr_dict[w_plans_부위_select.value] if '분구침술' not in 혈자리]
                                        ).tolist()
    
w_plans_except_check = [w_plans_부위_select, w_plans_혈자리_select]

def f_plans_observer(change):
    global v_plans_부위_list
    global v_hjr_str_list

    if change['new'] == True:
        # check밑으로 달린 애들 모두 활성화 ( disabled=False)
        for widget in w_plans_except_check:
            widget.disabled=False
            
        # when check 시 침치료에서의 부위, 혈자리 받아오기 ######################### 
        
        v_plans_부위_list = [] # 클릭될때마다,, 비어져있어야한다. 1개 아니면 2개가 한꺼번에 들어올테니 
        
        # 이미 plana부위가 2개 만땅으로 있으면, 체크 풀어도 안들어가도록 하자.
        if len(v_plans_부위_list) >=2:
            pass
        else:
            # 만약 2차침으로 list 1자리에 차있으면
            if len(v_hjr_str_list) > 0: 
                # 먼저 저장한 것에서 1개를 뺀다. 
                # 참고로 (1차)가 적혀있다!! 해당 부분을 제거 하자.
                _부위 = v_hjr_str_list[0].replace("(1차)", "")
                # 추가- 분구침인 경우 (혈자리) 대신 - 분구침술 이 있다. split 기준을 -로 바꿔주자.
                if '분구' in _부위:
                    v_plans_부위_list.append(_부위.split("-")[0].strip())
                else:
                    v_plans_부위_list.append(_부위.split("(")[0].strip())
                # 그리고 나서, 지금 선택된 부위를 추가한다.
            else:
                # 만약 1차침이면, 현재 선택된 부위가 담긴 v_hjr_부위만 담는다.
                
                pass
            # 이미 있으면 안담는다.
            if v_hjr_부위 in v_plans_부위_list:
                pass
            else:
                v_plans_부위_list.append(v_hjr_부위)
        w_plans_부위_select.options = v_plans_부위_list

    else:
        # 체크를 풀때, 다시 한번 부위 리스트를 초기화하고, default options를 넣어준다.
        v_plans_부위_list = []
        w_plans_부위_select.options = ["경항부", "체크해주세요."]
        
        # check밑으로 달린 애들 모두 disabled
        for widget in w_plans_except_check:
            widget.disabled=True    
        
w_plans_check.observe(f_plans_observer, names='value')    
    
################################## plans ui
ui_plans_1 = widgets.interactive(f_plans_select_부위_to_혈자리, widget_부위=w_plans_부위_select)
ui_plans_2 = w_plans_혈자리_select

ui_plans = widgets.HBox([w_plans_check, ui_plans_1, ui_plans_2])




#=========================yc======================
################################## yc widget
layout_2select = Layout(width='45%')
layout_yc_selcet = Layout(width='200px', height='120px')
#### check -  45% ( 200x120, 200x120 ) + 45% ( 200x120, 200x120 )
w_yc_check = widgets.Checkbox(
    value=False,
    description='약침',
    disable = True,
    indent=False, layout=layout_fixed_checkbox,
)
# SELECT 1-1 약침종류만. 
w_yc_종류_select = widgets.Select(
    options=yc_category_dict.keys(),    description='종류',
    layout=layout_yc_selcet,
    )
w_yc_종류_select.disabled=True
v_yc_종류 = w_yc_종류_select.value
# SELECT 1-2 약침에 따른 세부설정. 
w_yc_세부_select = widgets.Select(options=yc_category_dict[v_yc_종류],
#                                 description='세부',
                                layout=layout_yc_selcet,
                                )
w_yc_세부_select.disabled=True

# SELECT 2-1  from check observe
w_yc_부위_select = widgets.Select(
    options=["경항부", "체크해주세요"],
    description="부위",
    layout=layout_yc_selcet,
    )
w_yc_부위_select.disabled=True
v_yc_부위 = w_yc_부위_select.value
# SELECT 2-2 from select 
#         v_yc_부위_list는 observe에서 값을 전달받는 놈으로.. 옵져버 위에 선언되어있다. 오류나면 약간 더 위로 빼기
v_yc_부위_list = []
w_yc_혈자리_select = widgets.Select(
    options=["체크해주세요."],
    layout=layout_yc_selcet,
    disable = True,
    ) 
w_yc_혈자리_select.disabled=True

################################## yc functions
# INTERACTIVE1 : 
def f_select_종류_to_세부_yc(widget_종류):
    w_yc_세부_select.options = yc_category_dict[widget_종류]
    
# INTERACTIVE2 : 
def f_select_부위_to_혈자리_yc(widget_부위):
    # 분구침술을 제외하는 if 필터 걸었음.
    w_yc_혈자리_select.options = np.unique(
                                        [ 혈자리.split('/')[:2] for 부위 in v_yc_부위_list for 혈자리 in hjr_dict[widget_부위] if '분구침술' not in 혈자리]
                                        ).tolist()
    
w_yc_except_check = [
    w_yc_종류_select, w_yc_세부_select,
    w_yc_부위_select, w_yc_혈자리_select,
]
def f_yc_observer(change):
    global v_yc_부위_list
    global v_hjr_str_list

    if change['new'] == True:
        # check밑으로 달린 애들 모두 활성화 ( disabled=False)
        for widget in w_yc_except_check:
            widget.disabled=False
            
        # when check 시 침치료에서의 부위, 혈자리 받아오기 ######################### 
        
        v_yc_부위_list = [] # 클릭될때마다,, 비어져있어야한다. 1개 아니면 2개가 한꺼번에 들어올테니 
        
        # 이미 plana부위가 2개 만땅으로 있으면, 체크 풀어도 안들어가도록 하자.
        if len(v_yc_부위_list) >=2:
            pass
        else:
            # 만약 2차침으로 list 1자리에 차있으면
            if len(v_hjr_str_list) > 0: 
                # 먼저 저장한 것에서 1개를 뺀다. 
                # 참고로 (1차)가 적혀있다!! 해당 부분을 제거 하자.
                _부위 = v_hjr_str_list[0].replace("(1차)", "")
                # 추가- 분구침인 경우 (혈자리) 대신 - 분구침술 이 있다. split 기준을 -로 바꿔주자.
                if '분구' in _부위:
                    v_yc_부위_list.append(_부위.split("-")[0].strip())
                else:
                    v_yc_부위_list.append(_부위.split("(")[0].strip())

                # 그리고 나서, 지금 선택된 부위를 추가한다.
            else:
                # 만약 1차침이면, 현재 선택된 부위가 담긴 v_hjr_부위만 담는다.
                
                pass
            # 이미 있으면 안담는다.
            if v_hjr_부위 in v_yc_부위_list:
                pass
            else:
                v_yc_부위_list.append(v_hjr_부위)
        w_yc_부위_select.options = v_yc_부위_list

    else:
        # 체크를 풀때, 다시 한번 부위 리스트를 초기화하고, default options를 넣어준다.
        v_yc_부위_list = []
        w_yc_부위_select.options = ["경항부", "체크해주세요."]
        
        # check밑으로 달린 애들 모두 disabled
        for widget in w_yc_except_check:
            widget.disabled=True    
        
w_yc_check.observe(f_yc_observer, names='value')    

################################## yc ui    
ui_yc_1 = widgets.interactive(f_select_종류_to_세부_yc, widget_종류=w_yc_종류_select)
ui_yc_1.layout=layout_2select
ui_yc_2 = widgets.interactive(f_select_부위_to_혈자리_yc, widget_부위=w_yc_부위_select)
ui_yc_2.layout=layout_2select 

ui_yc = widgets.HBox([w_yc_check, ui_yc_1, w_yc_세부_select, ui_yc_2, w_yc_혈자리_select])



#=========================p/e======================
################################## p/e widget
### select 자체는 width auto -> 바깥의 Interactive에 %주기
### select1-INTER(auto-23%) select2-INTER(auto-35%) text(32%)  3_btn(15%) 
layout_pe_select_in = Layout(width='auto', height='120px')
layout_pe_select_1 = Layout(width='27%')
layout_pe_select_2 = Layout(width='35%')
layout_pe_text = Layout(width='28%')
layout_3_btn = Layout(width='15%')

w_pe_check = widgets.Checkbox(
    value=False,
    description='P/E',
    disable = True,
    indent=False, layout=layout_fixed_checkbox,    
)

# SELECT 1 
w_pe_종류_select = widgets.Select(
    options=pe_category_dict.keys(),
    description="종류",
    layout=layout_pe_select_in,
    )
w_pe_종류_select.disabled=True
v_pe_종류 = w_pe_종류_select.value

# SELECT 2
#         세부는 (검사명, 자동으로 올라갈 텍스트)로 구성 -> [0]으로 검사명만 options으로
w_pe_세부_select = widgets.Select(
    options=pe_category_dict[v_pe_종류][0],
    description = '세부',
    layout=layout_pe_select_in,
    )
w_pe_세부_select.disabled=True

################################## p/e functions
# INTERACTIVE1 : 
def f_select_종류_to_세부_pe(widget_종류):
    w_pe_세부_select.options = pe_category_dict[widget_종류]
    
w_pe_text_list = [widgets.Text('',
                               placeholder="여기는 선택만(X) 반드시 [+]로 추가해야함!!",
                               disabled=True,
                               layout=layout_in,
                               )] 
vb_pe_text_list = widgets.VBox(w_pe_text_list, layout=layout_pe_text)

# INTERAVTIVE2 : 세부 (검사명,)[0] 클릭시 --> text0번재놈 ( , 자동텍스트)[1]
def f_select_세부_to_text_pe(widget_세부):
    vb_pe_text_list.children[0].value =  pe_detail_dict[widget_세부]
    
w_pe_plus_btn = widgets.Button(description = '', layout=layout_fixed_btn, icon ="plus", button_style='') 
w_pe_minus_btn = widgets.Button(description = '', layout=layout_fixed_btn, icon ="minus", button_style='') 
w_pe_info_btn = widgets.Button(description = '', layout=layout_fixed_btn, icon ="info", button_style='') 
hb_pe_btn_list = widgets.HBox([w_pe_plus_btn, w_pe_minus_btn, w_pe_info_btn],
                             layout=layout_3_btn)

def f_pe_plus(b):        
    # 핵심
    vb_pe_text_list.children=tuple(list(vb_pe_text_list.children) + [widgets.Text('',
                               placeholder="(+/+) on Lt. shoulder acromion, anterior knee, Rt. dorsal wrist area",
                               layout=layout_in,
                              )]) 
    list(vb_pe_text_list.children)[-1].value = f"""# {w_pe_세부_select.value} {vb_pe_text_list.children[0].value}"""
    vb_pe_text_list.children[0].value = "" # 다시 첫번째 내용 초기화
    
def f_pe_minus(b):       
    ## 뺄때는 1개는 남아있어야한다.
    if len(list(vb_pe_text_list.children)) > 1:
        # 핵심
        vb_pe_text_list.children=tuple(list(vb_pe_text_list.children)[:-1]) 
    ## 뼀을때 1개가 남으면, 그 내용을 짖우기 
    elif len(list(vb_pe_text_list.children)) == 1:
        vb_pe_text_list.children[0].value = ""
    else:
        pass
w_pe_plus_btn.on_click(f_pe_plus)
w_pe_minus_btn.on_click(f_pe_minus)

    
w_pe_except_check = [
    w_pe_종류_select, w_pe_세부_select,
    w_pe_plus_btn,w_pe_minus_btn,w_pe_info_btn] + list(vb_pe_text_list.children) + list(hb_pe_btn_list.children)
def f_pe_observer(change):
    if change['new'] == True:
        # check밑으로 달린 애들 모두 활성화 ( disabled=False)
        for widget in w_pe_except_check:
            widget.disabled=False
    else:
        # check밑으로 달린 애들 모두 disabled
        for widget in w_pe_except_check:
            widget.disabled=True    
        
w_pe_check.observe(f_pe_observer, names='value')    

################################## p/e ui    
ui_pe_1 = widgets.interactive(f_select_종류_to_세부_pe, widget_종류=w_pe_종류_select)
ui_pe_1.layout = layout_pe_select_1
ui_pe_2 = widgets.interactive(f_select_세부_to_text_pe, widget_세부=w_pe_세부_select)
ui_pe_2.layout = layout_pe_select_2
ui_pe = widgets.HBox([w_pe_check, ui_pe_1, ui_pe_2, vb_pe_text_list, hb_pe_btn_list])




#=========================etc======================
################################## etc widget
layout_etc_out = Layout(width='60%')

w_etc_check = widgets.Checkbox(
    value=False,
    description='기타 치료',
    disable = False,
    indent=False, layout=layout_fixed_checkbox,
)

w_etc_text_list = [widgets.Text(
    #description='처방 정보 :',
    value='',
    placeholder='자보한방파스 PRN 1매 or 파스 PRN 1매',
    disabled=True,
    layout=layout_in
)]

vb_etc_text_list = widgets.VBox(w_etc_text_list, layout=layout_etc_out)

w_etc_plus_btn = widgets.Button(
    description='',
    disabled=True,
    button_style ='', # success
    tooltip='click me',
    icon='plus',
    layout=layout_fixed_btn,
)
w_etc_minus_btn = widgets.Button(
    description='',
    disabled=True,
    button_style ='', # success
    tooltip='click me',
    icon='minus',
    layout=layout_fixed_btn,
)
w_etc_info_btn = widgets.Button(
    description='',
    disabled=True,
    button_style ='', # success
    tooltip=drug_data,
    icon='info',
    layout=layout_fixed_btn,
)

#=========================etc======================
################################## etc ui 
ui_etc = widgets.HBox([w_etc_check, vb_etc_text_list, w_etc_plus_btn, w_etc_minus_btn, w_etc_info_btn])

# check시 활성화 주기/안주기를 위해서 편하게 리스트로 
w_etc_except_check = list(vb_etc_text_list.children) + [w_etc_plus_btn, w_etc_minus_btn, w_etc_info_btn]

################################## etc functions
def f_etc_observer(change):
    if change['new'] == True:
        # check밑으로 달린 애들 모두 활성화 ( disabled=False)
        for widget in w_etc_except_check:
            widget.disabled=False
    else:
        # check밑으로 달린 애들 모두 disabled
        for widget in w_etc_except_check:
            widget.disabled=True

def f_etc_plus(b):        
    # text에  자식추가.
    vb_etc_text_list.children=tuple(list(vb_etc_text_list.children) + [
        widgets.Text(
    value='',
    placeholder=' 자보한방파스 PRN 1매 or 파스 PRN 1매',
    disabled=False,
    layout=layout_in
    )]) 
    
def f_etc_minus(b):       
    ## 뺄때는 1개는 남아있어야한다.
    if len(list(vb_etc_text_list.children)) > 1:
        # 핵심
        vb_etc_text_list.children=tuple(list(vb_etc_text_list.children)[:-1]) 
    ## 뼀을때 1개가 남으면, 그 내용을 짖우기 
    elif len(list(vb_etc_text_list.children)) == 1:
        vb_etc_text_list.children[0].value = ""
    else:
        pass
    
    
w_etc_check.observe(f_etc_observer, names='value')


w_etc_plus_btn.on_click(f_etc_plus)
w_etc_minus_btn.on_click(f_etc_minus)



#=========================consult======================
################################## consult widgets
layout_consult_text = Layout(width='70%')

w_consult_label = widgets.Label('상담 및 처치 : ')

w_consult_text_list = [widgets.Text('',
                               placeholder="약 2주 입원치료 예정. 00병원 F/U는 3월 6일. crutch 보행 상태.",
                               layout=layout_in,
                              )] 
vb_consult_text_list = widgets.VBox(w_consult_text_list,
                                   layout=layout_consult_text)

w_consult_plus_btn = widgets.Button(description = '', layout=layout_fixed_btn, button_style='', icon='plus') 
w_consult_minus_btn = widgets.Button(description = '', layout=layout_fixed_btn, button_style='', icon='minus') 
w_consult_info_btn = widgets.Button(description = '', layout=layout_fixed_btn, button_style='', icon='info') 
hb_consult_btn_list = widgets.HBox([w_consult_plus_btn, w_consult_minus_btn, w_consult_info_btn],
                                  layout=layout_3_btn)

################################## consult functions 
def f_consult_plus(b):        
    # 핵심
    vb_consult_text_list.children=tuple(list(vb_consult_text_list.children) + [widgets.Text('', 
                                                                                             placeholder="# 비급여 내역 안내: 00이완약침 시술 설명, 환자 동의 취득 [2020.00.00.] "   ,
                                                                                            layout=layout_in)]) 
    
def f_consult_minus(b):       
    ## 뺄때는 1개는 남아있어야한다.
    if len(list(vb_consult_text_list.children)) > 1:
        # 핵심
        vb_consult_text_list.children=tuple(list(vb_consult_text_list.children)[:-1]) 
    ## 뼀을때 1개가 남으면, 그 내용을 짖우기 
    elif len(list(vb_consult_text_list.children)) == 1:
        vb_consult_text_list.children[0].value = ""
    else:
        pass
    
################################## consult ui
ui_consult = widgets.HBox([w_consult_label,vb_consult_text_list,hb_consult_btn_list])

w_consult_plus_btn.on_click(f_consult_plus)
w_consult_minus_btn.on_click(f_consult_minus)



#=========================output======================
################################## output widget
layout_last_2_btn = [Layout(width='70%', height='40px'), Layout(width='30%', height='40px')]

w_write_btn = widgets.Button(
    description = '경과지 작성',
    button_style='danger',
    icon='check',
    layout=layout_last_2_btn[0],
)
w_init_btn = widgets.Button(
    description = '초기화',
    button_style='', # 'success', 'info', 'warning', 'danger' or ''
    icon='bell',
    layout=layout_last_2_btn[1],
)
hb_last_2_btn = widgets.HBox([w_write_btn, w_init_btn])

w_output = widgets.Output()

################################## output ui
ui_last_btn_ouput = widgets.VBox([
    hb_last_2_btn,
    w_output,
])

################################## output functions


def f_output(b):
    #### str_주관적 호소=============================================================
    subjective_text_list = list(vb_subjective_text_list.children)
    subjective_text_values_list = [subjective_text.value for subjective_text in subjective_text_list if len(subjective_text.value[3:])>0]


    str_final_subjective=""  # 2번째부터는 스페이스 2칸과 동일 
    if len(subjective_text_values_list) > 0:
        str_final_subjective +="S) "#+1칸
        for text in subjective_text_values_list:
            str_final_subjective += f"{text}\n   " # 2칸+1 뛰워주기-> 나중에는 strip
        str_final_subjective = str_final_subjective.strip() + "\n\n" # 마지막 한줄은 띄워줘야한다.


    #### str_주소증=============================================================
    cc_text_list = list(vb_cc_text_list.children)
    cc_text_values_list = [cc_text.value for cc_text in cc_text_list if len(cc_text.value[3:])>0]
    # cc_text_values_list

    str_final_cc=""  
    if len(cc_text_values_list) > 0:
        str_final_cc += f"""O)
- C/C : {cc_text_values_list[0]}
{'ass.sx: '+', '.join(cc_text_values_list[1:]) if len(cc_text_values_list[1:]) >0 else ''}"""

    str_final_cc = str_final_cc.strip() + "\n"  # 마지막 한줄은 띄워줘야한다.


    #### str_상병모음=============================================================
    v_language_type = 'kor' # 0이면 한국어, 1이면 영어

    str_final_disease = ''
    if len(v_disease_list)>0:
        str_final_disease+="A)\n"
        for n, disease_full in v_disease_dict.items():
            # 상병만 골라내기
            v_sb = disease_full.split(':')[0].strip()
            v_kor_eng_sbm = disease_full.split(':')[1].strip()
            if v_language_type == 'kor':
                # 한글만 골라내기
                v_sbm = v_kor_eng_sbm.split('(')[0]
            else :
                v_sbm = v_kor_eng_sbm.split('(')[1][:-1]

            str_final_disease += f"   {n}. {v_sbm} ({v_sb}) \n"

    ## str_final_bj_code  혈어증 (U612)  부분을 dict.items()의 맨 마지막 숫자로 더해야한다.
    if len(v_disease_dict) == 0:
        str_final_disease+="A)\n"
    str_final_disease = str_final_disease.strip() +     f"\n   {len(v_disease_list)+1}. {str_final_bj_code}" + "\n\n"# 마지막의 한줄띔은 삭제시켜주기  



    #### str_O/S=============================================================
    str_final_os = '- O/S : '

    # 피커에 날짜 찍혔을 때
    if w_os_picker.value:
        date_str = str(w_os_picker.value).replace('-','.')
        str_final_os += date_str+' / '
    else:
        pass

    str_final_os += w_os_text.value
    str_final_os = str_final_os.strip() + "\n"  # 마지막 한줄은 띄워줘야한다.

    #### str_P/I=============================================================

    pi_text_list = list(vb_pi_text_list.children)
    pi_text_values_list = [pi_text.value for pi_text in pi_text_list if len(pi_text.value)>0]
    # pi_text_values_list


    str_final_pi=""  # 2번째부터는 스페이스 2칸과 동일 
    if len(pi_text_values_list) > 0:
        str_final_pi+="- P/I : "#+1칸
        for text in pi_text_values_list:
            str_final_pi += f"{text}\n        " # 2칸+1 뛰워주기-> 나중에는 strip
        str_final_pi = str_final_pi.strip() + "\n" # 마지막 한줄은 띄워줘야한다.



    #### str_P/H_1 체크박스===
    ph_check_list = list(ui_ph_1_check.children)
    check_name_and_value = [(check.description,  check.value) for check in hb_ph_check_list.children ] # 라벨(0)빼고 1번재부터 

    str_final_ph_1_check = "- P/H : "
    for name, value in check_name_and_value:
        str_final_ph_1_check+=f"{name}({'+' if value else '-'}) "
    str_final_ph_1_check +='\n'    

    #### str_ph2_text===
    ph_text_list = list(vb_ph_2_text_list.children)
    ph_text_values_list = [ph_text.value for ph_text in ph_text_list if len(ph_text.value)>0]
    str_final_ph_2_text = ""  # 2번째부터는 스페이스 2칸과 동일 
    if len(ph_text_values_list) > 0:
        str_final_ph_2_text+="        "#+1칸
        for text in ph_text_values_list:
            str_final_ph_2_text += f"# {text}\n        " # 2칸+1 뛰워주기-> 나중에는 strip
        # 마지막에 #+1칸  하나 부텅있는 것 제거해야함
        # 첫줄에 띄워놓은것도 삭제해서, strip() -> rstip()으로 변경
        str_final_ph_2_text = str_final_ph_2_text.rstrip() + "\n" # 마지막 한줄은 띄워줘야한다.
    
    


    #### str_final_bj   INTERACTIVE===
    # interactive하게 dict에서 꺼내므로, 따로 코드가 없다. 
    # f_bj_ui_and_string_from_toggle()에서 받아서 들어간다. 
    # 맨 구간 맨 마지막이므로 dict값마다 +\n\n해주기
    
    #### str_final_hjr select1 + INTERACTIVE select 2개 ===
    # interactive하게 dict에서 꺼내므로, 따로 코드가 없다. 
    # f_select_혈위_to_string()에서 받아서 들어간다. 
    
    #### str_final_chuna  INTERACTIVE===
    # interactive하게 dict에서 꺼내므로, 따로 코드가 없다. 
    
    
    
    #### str_drug_text===
    v_drug_text_list = list(vb_drug_text_list.children)
    v_drug_picker_list = list(vb_drug_picker_list.children)

    str_drug_list = [str(drug_picker.value).replace('-','.') + '~ / ' + drug_text.value for drug_text,drug_picker in zip(v_drug_text_list, v_drug_picker_list)  if len(drug_text.value)>0]


    str_final_drug = "- 한약치료 : "
    # check 확인부터
    if w_drug_check.value==False:
        str_final_drug += "- \n"
    else :
        # check는 풀렸는데 빈칸으로 비어있다면.. 그냥 - 주기
        if len(str_drug_list)<1:
            str_final_drug+="-"        

        drug_str_ = "\n               ".join(str_drug_list) # join으로 str마다 <\n + 공백> 넣어주기
        str_final_drug += drug_str_ + "\n" # 마지막 한칸 띄워주기
        
    #### str_plans ===
    str_final_plans = "- 부항치료 : "
    if w_plans_check.value == False:
        str_final_plans += "- \n"
    else:
        str_final_plans += f"""{','.join(w_plans_부위_select.options)}(PRN습식) / 간접구(기기구) : {w_plans_혈자리_select.value}(PRN황토쑥탄)
- 물리치료 : 경피적외선조사요법 : {','.join(w_plans_부위_select.options)}(3∼25㎛, 250w)
             경근저주파요법 : {','.join(w_plans_부위_select.options)}(SI&TM-25%, GP-level 10) {'(2부위 ~'+str(w_os_picker.value+timedelta(days=16)).replace('-','.')[-5:] + ')' if w_hjr_유형_select.value=='자보(침술2종)' and w_os_picker and (datetime.datetime.now().date() - w_os_picker.value).days <=16  else  ''}
""" 
    #             경근초음파요법 : {','.join(w_plans_부위_select.options)}(1.0~2.0㎒) <- 일단 생략


    #### str_약침 ===
    str_final_yc = "- 약침치료 : "
    if w_yc_check.value == False:
        str_final_yc += "- \n"
    else:
        # 약침 : 중성어혈 0.5cc → 견관절(견우,견료)
        # (완관절부-양지,양계,양곡혈/견부-견우,노수,견정혈/상기 혈위 및 주위 tenderness point)
        #  {yc_str_dict[w_yc_종류_select.value]}
        str_final_yc += f"""{w_yc_종류_select.value}({w_yc_세부_select.value}) → {w_yc_부위_select.value}-{w_yc_혈자리_select.value} 및 주위 tenderness point에 시행함.
"""
    #### str_pe_text===
    # 여기서는 0번을 제외하고 텍스트를 가져온다.
    # cc밑에 달릴 거라서 그에 맞게 띄워스기해서 join한다.
    str_final_pe = ""
    # check 확인부터
    if w_pe_check.value==False:
        str_final_pe = "" # 아예 출력해도 없는 것으로 비워져있어야함. c/c와 밑에 것 사이에..
    else :
        # check는 풀렸는데 +로 추가생성된 텍스트란이 없다면, 없는 걸로 치자.
        if len(list(vb_pe_text_list.children)) <= 1:
            str_final_pe=""        
        else: # +로 텍스트 추가생성된 상태
            # pe에서만 2번재 텍스트부터 데이터를 긁어모은다. 1번째 텍스트는 입력용이다.
            for w_text in vb_pe_text_list.children[1:]:
                str_final_pe += "        " + w_text.value + "\n" # join으로 str마다 <\n + 공백> 넣어주기

    #### str_final_etc ===
    etc_text_list = list(vb_etc_text_list.children)
    etc_text_values_list = [etc_text.value for etc_text in etc_text_list if len(etc_text.value)>0]
    # print(etc_text_values_list)

    str_final_etc = "- 기타치료 : "  # 2번째부터는 스페이스 2칸과 동일 
    if len(etc_text_values_list) > 0 and w_etc_check.value==True:
        #str_final_etc+=""#+1칸
        for text in etc_text_values_list:
            str_final_etc += f"{text}\n             " # 2칸+1 뛰워주기-> 나중에는 strip
        # 첫줄에 띄워놓은것도 삭제해서, strip() -> rstip()으로 변경
        str_final_etc = str_final_etc.rstrip() + "\n" # 마지막 한줄은 띄워줘야한다.
    else:
        str_final_etc +="-\n"
                
    #### str_final_consult ===
    consult_text_list = list(vb_consult_text_list.children)
    consult_text_values_list = [consult_text.value for consult_text in consult_text_list if len(consult_text.value)>0]
    # ph_text_values_list

    str_final_consult = "- 상담 및 처치 : "  # 2번째부터는 스페이스 2칸과 동일 
    if len(consult_text_values_list) > 0:
        #str_final_consult+="                 "#+1칸
        for text in consult_text_values_list:
            str_final_consult += f"{text}\n                 " # 2칸+1 뛰워주기-> 나중에는 strip
        # 첫줄에 띄워놓은것도 삭제해서, strip() -> rstip()으로 변경
        str_final_consult = str_final_consult.rstrip() + "\n\n" # 마지막 한줄은 띄워줘야한다.
    else:
        str_final_consult +="-\n"
        
        

    
    ##### output widget을 with한 상태에서 clear_output()이후에 print
    with w_output:
        clear_output()
        print(
        str_final_subjective + \
        
        str_final_cc + \
        
        str_final_pe + \
        
        str_final_os +\
        str_final_pi +\
        str_final_ph_1_check+\
        str_final_ph_2_text+\
        str_final_bj +\
        
        str_final_disease +\
        
        str_final_hjr +\
        str_final_chuna +\
        str_final_drug +\
        str_final_plans +\
        str_final_yc +\
        str_final_etc +\
        str_final_consult

        )

def initial(b):
    #### 아래 내용물도 초기화
    with w_output:
        clear_output()
    w_output.value=""
    
    ### 주소증 초기화 -> 빼기 버튼으로 일단 초기화 시켰지만..각 칸의 처음것만 남기고,, 처음 것은 value =""
    vb_subjective_text_list.children = [list(vb_subjective_text_list.children)[0]] # 처음 것만 남기기
    vb_cc_text_list.children = [list(vb_cc_text_list.children)[0]]
    vb_subjective_text_list.children[0].value = "#1 " # 남겨진 처음것에 defaul값 주기 
    vb_cc_text_list.children[0].value = "1. "


    # 상병모음 초기화 
    row_disease[0].value ="" # 검색란 비우기
    row_disease[0].placeholder = "ex> S3350 대문자로 입력시작!"
    w_disease_output.value = "자동입력을 이용해주세요" # 정보표시란 지우기 
    n = 0 # n도 비워야함!!
    v_disease_dict = {} # 자료구조 비우기
    v_disease_list = [] 

    # o/s 초기화
    w_os_picker.value = datetime.datetime.now().date()
    w_os_text.value = ""
    w_os_text.placeceholder = "<- 년-월-일 정확하지 않다면, 아예 del삭제 후 [ 2020.05 / 상세내용 ] 직접작성"

    #p/i 초기화
    vb_pi_text_list.children = [list(vb_pi_text_list.children)[0]] # 처음 것만 남기기
    vb_pi_text_list.children[0].value = "" # 남겨진 처음것에 defaul값 주기 

    #p/h_1 check 초기화
    for check in list(hb_ph_check_list.children):
        check.value = False

    #p/h_2 text 초기화
    vb_ph_2_text_list.children = [list(vb_ph_2_text_list.children)[0]] # 처음 것만 남기기
    vb_ph_2_text_list.children[0].value = "" # 남겨진 처음것에 defaul값 주기 

    # bj 초기화
    w_bj_변증_select.value= '기혈음양진액변증'


    # hjr초기화
    w_hjr_유형_select.value= '자보(침술2종)'
    w_hjr_부위_select.value= '경항부' # -> w_hjr_혈위는 알아서 bj_dict['경항부']로 interacive 선택될 것임.
    v_hjr_string =""
    v_hjr_str_list = []
    w_hjr_btn_text.value="버튼클릭 안할시 침 1번으로 자동인식!"

    # chuna 초기화
    w_chuna_1_select.value= '추나'
    w_chuna_2_select.value="시행하지 않음."

    # 한약 drug 초기화 ###################################################################
    # check풀기
    w_drug_check.value = False
    # picker 자식 1개로
    vb_drug_picker_list.children = [list(vb_drug_picker_list.children)[0]] # 처음 것만 남기기
    vb_drug_picker_list.children[0].value = datetime.datetime.now().date() # 남겨진 처음것에 defaul값 주기 
    # text 자식 1개로
    vb_drug_text_list.children = [list(vb_drug_text_list.children)[0]] # 처음 것만 남기기
    vb_drug_text_list.children[0].value = ""

    # plans check 초기화 ###################################################################
    # check 풀기
    w_plans_check.value = False
    # 부위 부분에 들어갈 list 초기화하고, 경항부만..
    v_plans_부위_list = []

    # 약침 check 초기화 ###################################################################
    # check 풀기
    w_yc_check.value = False
    # 부위 부분에 들어갈 list 초기화하고, 경항부만..
    v_yc_부위_list = []
    w_yc_종류_select.value= '중성어혈'


    # pe check 초기화 ###################################################################
    # check 풀기
    w_pe_check.value = False
    # 부위 부분에 들어갈 list 초기화하고, 경항부만..
    w_pe_종류_select.value= '국소통증'
    # text 자식 1개로
    vb_pe_text_list.children = [list(vb_pe_text_list.children)[0]] # 처음 것만 남기기
    vb_pe_text_list.children[0].value = "" # 남겨진 처음것에 defaul값 주기 
    
    # etc check 초기화 ###################################################################
    # check 풀기
    w_etc_check.value = False
    # text 자식 1개로
    vb_etc_text_list.children = [list(vb_etc_text_list.children)[0]] # 처음 것만 남기기
    vb_etc_text_list.children[0].value = ""
    
    #### consult 초기화
    vb_consult_text_list.children = [list(vb_consult_text_list.children)[0]] # 처음 것만 남기기
    vb_consult_text_list.children[0].value = "" # 남겨진 처음것에 defaul값 주기 
    
def progress():
    initial('b') # 한번 widget 초기화 해줘야. 다시 불렀을 때 빈 상태
    display(
        ui_title,
        ui_s,
        row_disease,
        ui_pe,
        ui_os,
        ui_pi,
        ui_ph_1_check,
        ui_ph_2_text,
        ui_bj,
        ui_hjr,
        ui_chuna,
        ui_drug,
        ui_plans,
        ui_yc,
        ui_etc,
        ui_consult,
        ui_last_btn_ouput,
       )

# output widget에 with를 띄운 상태로 print한다.
# print할 대상은 global 변수여야한다.
# f_output자체를 with w_output : 상태에서clear_output() +  print하게 했다.
# f_output() 에 onclick을 걸 수 있게 b라는 인자를 받아준다.-> f_ouput(b)
w_write_btn.on_click(f_output)
w_init_btn.on_click(initial) # 역시 b인자를 받아주게 수정 def init(b)



#=========================import======================
from IPython.core.display import display, HTML
display(HTML("<style>.container { width:100% !important; }</style>"))

