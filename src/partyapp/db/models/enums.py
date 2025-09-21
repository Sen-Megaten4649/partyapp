"""
ENUM 定義モジュール
各 ENUM は「英語キー」と「日本語の説明」をセットで管理する。
"""

# 法令種別 law_type
LAW_TYPE_VALUES = [
    ("constitution", "憲法: 日本における最高位の法令"),
    ("statute", "法律: 国会の可決により成立"),
    ("cabinet_order", "政令: 内閣が制定"),
    ("imperial_order", "勅令: 明治憲法下の命令（現行有効なものあり）"),
    ("ministerial_order", "府省令: 各省庁が制定"),
    ("national_rule", "規則: 行政機関や裁判所などが制定"),
    ("ordinance", "条例: 地方公共団体の議会が制定"),
    ("local_rule", "規則（地方）: 地方自治体の長が制定"),
]

# 管轄レベル jurisdiction
JURISDICTION_VALUES = [
    ("national", "国レベル（国会・内閣など）"),
    ("local", "地方レベル（自治体）"),
]

# 提出系 submission_role
SUBMISSION_ROLE_VALUES = [
    ("submitter", "提出（議員立法など）"),
    ("co_submitter", "共同提出（複数党で提出）"),
    ("cabinet", "内閣提出（政府提出法案）"),
    ("amendment", "修正動議提出"),
    ("none", "関与なし"),
]

# 推進系 promotion_role
PROMOTION_ROLE_VALUES = [
    ("coalition", "与党として推進（与党内合意）"),
    ("support", "野党などが支持を表明（提出なし）"),
    ("none", "関与なし"),
]

# 投票系 vote_role
VOTE_ROLE_VALUES = [
    ("voted_for", "賛成票を投じた"),
    ("voted_against", "反対票を投じた"),
    ("abstained", "棄権した"),
    ("boycott", "欠席または審議拒否"),
    ("none", "関与なし"),
]