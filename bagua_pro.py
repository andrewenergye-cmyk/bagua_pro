import streamlit as st
import random
import urllib.parse

# 1. 網頁基礎設定
st.set_page_config(page_title="易經占卜系統", page_icon="☯️")

# 2. 易經 64 卦對照表 (整合名稱與標準符號)
HEXAGRAMS = {
    "111111": ("乾為天", "☰\n☰"), "000000": ("坤為地", "☷\n☷"), 
    "100010": ("水雷屯", "☵\n☳"), "010001": ("山水蒙", "☶\n☵"),
    "111010": ("水天需", "☵\n☰"), "010111": ("天水訟", "☰\n☵"),
    "010000": ("地水師", "☷\n☵"), "000010": ("水地比", "☵\n☷"),
    "111011": ("風天小畜", "☴\n☰"), "110111": ("天澤履", "☰\n☱"),
    "111000": ("地天泰", "☷\n☰"), "000111": ("天地否", "☰\n☷"),
    "101111": ("天火同人", "☰\n☲"), "111101": ("火天大有", "☲\n☰"),
    "001000": ("地山謙", "☷\n☶"), "000100": ("雷地豫", "☳\n☷"),
    "100110": ("澤雷隨", "☱\n☳"), "011001": ("山風蠱", "☶\n☴"),
    "110000": ("地澤臨", "☷\n☱"), "000011": ("風地觀", "☴\n☷"),
    "100101": ("火雷噬嗑", "☲\n☳"), "101001": ("山火賁", "☶\n☲"),
    "000001": ("山地剝", "☶\n☷"), "100000": ("地雷復", "☷\n☳"),
    "100111": ("天雷無妄", "☰\n☳"), "111001": ("山天大畜", "☶\n☰"),
    "100001": ("山雷頤", "☶\n☳"), "011110": ("澤風大過", "☱\n☴"),
    "010010": ("坎為水", "☵\n☵"), "101101": ("離為火", "☲\n☲"),
    "001110": ("澤山咸", "☱\n☶"), "011100": ("雷風恆", "☳\n☴"),
    "001111": ("天山遯", "☰\n☶"), "111100": ("雷天大壯", "☳\n☰"),
    "000101": ("火地晉", "☲\n☷"), "101000": ("地火明夷", "☷\n☲"),
    "101011": ("風火家人", "☴\n☲"), "110101": ("火澤睽", "☲\n☱"),
    "001010": ("水山蹇", "☵\n☶"), "010100": ("雷水解", "☳\n☵"),
    "110001": ("山澤損", "☶\n☱"), "100011": ("風雷益", "☴\n☳"),
    "111110": ("澤天夬", "☱\n☰"), "011111": ("天風姤", "☰\n☴"),
    "000110": ("澤地萃", "☱\n☷"), "011000": ("地風升", "☷\n☴"),
    "010110": ("澤水困", "☱\n☵"), "011010": ("水風井", "☵\n☴"),
    "101110": ("澤火革", "☱\n☲"), "011101": ("火風鼎", "☲\n☴"),
    "100100": ("震為雷", "☳\n☳"), "001001": ("艮為山", "☶\n☶"),
    "001011": ("風山漸", "☴\n☶"), "110100": ("雷澤歸妹", "☳\n☱"),
    "101100": ("雷火豐", "☳\n☲"), "001101": ("火山旅", "☲\n☶"),
    "011011": ("巽為風", "☴\n☴"), "110110": ("兌為澤", "☱\n☱"),
    "010011": ("風水渙", "☴\n☵"), "110010": ("水澤節", "☵\n☱"),
    "110011": ("風澤中孚", "☴\n☱"), "001100": ("雷山小過", "☳\n☶"),
    "101010": ("水火既濟", "☵\n☲"), "010101": ("火水未濟", "☲\n☵")
}

def toss_coins():
    return sum(random.choice([2, 3]) for _ in range(3))

# --- 自訂 CSS 加大按鈕 ---
st.markdown("""
    <style>
    div.stButton > button:first-child {
        height: 3.5em;
        font-size: 22px;
        font-weight: bold;
        background-color: #2e7d32;
        color: white;
        border-radius: 12px;
        border: none;
        box-shadow: 0px 4px 10px rgba(0,0,0,0.2);
    }
    div.stButton > button:hover {
        background-color: #1b5e20;
        color: white;
    }
    </style>
""", unsafe_allow_html=True)

st.title("☯️ 易經智慧占卜 - BY 臣")

# 1. 輸入問題
question = st.text_input("🔮 請在心中默念並輸入您的問題：", placeholder="例如：問本週事業運勢？")

# 2. 開始起卦
if st.button("🔮 開始感應起卦", use_container_width=True):
    with st.spinner('正在與天地能量感應...'):
        base_binary, changed_binary = "", ""
        moving_lines, visual_lines = [], []
        
        for i in range(1, 7):
            score = toss_coins()
            if score == 6:  # 老陰
                base_binary += "0"; changed_binary += "1"; moving_lines.append(i)
                visual_lines.append(f"第 {i} 爻: ━  ━  × (老陰動)")
            elif score == 7: # 少陽
                base_binary += "1"; changed_binary += "1"
                visual_lines.append(f"第 {i} 爻: ━━━    (少陽靜)")
            elif score == 8: # 少陰
                base_binary += "0"; changed_binary += "0"
                visual_lines.append(f"第 {i} 爻: ━  ━    (少陰靜)")
            elif score == 9: # 老陽
                base_binary += "1"; changed_binary += "0"; moving_lines.append(i)
                visual_lines.append(f"第 {i} 爻: ━━━  ○ (老陽動)")

        # 3. 取得卦名與符號
        base_name, base_sym = HEXAGRAMS[base_binary]
        changed_name, changed_sym = HEXAGRAMS[changed_binary]
        
        # 4. 顯示結果介面
        st.subheader("【 卦象顯現 】")
        col_img1, col_img2 = st.columns(2)
        with col_img1:
            st.markdown(f"**本卦：{base_name}**")
            st.code(base_sym, language="")
        with col_img2:
            st.markdown(f"**變卦：{changed_name if moving_lines else '無'}**")
            st.code(changed_sym if moving_lines else "無變動", language="")

        # 詳盡爻語顯示
        with st.expander("查看詳細六爻變化"):
            for line in reversed(visual_lines):
                st.write(line)
        
        # 5. 解卦建議與複製框
        q_prefix = f"【問題：{question}】\n" if question else ""
        if not moving_lines:
            search_query = f"易經 {base_name} 卦象解釋"
            advice = "六爻皆靜，請參考「本卦」的整體卦辭。"
        elif len(moving_lines) == 1:
            search_query = f"易經 {base_name} 第{moving_lines[0]}爻 變 {changed_name}"
            advice = f"有一動爻，重點參考「本卦」第 {moving_lines[0]} 爻的爻辭。"
        else:
            moving_str = ",".join(map(str, moving_lines))
            search_query = f"易經 {base_name} 變 {changed_name} 解釋"
            advice = f"多爻發動（第 {moving_str} 爻），請綜合參考本卦與變卦【{changed_name}】。"

        st.info(f"💡 **啟示**：{advice}")
        
        # 組合文字供複製
        res_text = f"{base_name}" + (f" 變 {changed_name}" if moving_lines else "")
        copy_content = f"{q_prefix}☯️ 占卜結果：{res_text}\n啟示：{advice}\n---"
        st.text_area("📋 複製結果摘要：", value=copy_content, height=120)
        
        # 6. 搜尋連結
        google_url = f"https://www.google.com/search?q={urllib.parse.quote(question + ' ' + search_query)}"
        st.link_button("👉 前往 Google 查看深度解析", google_url, use_container_width=True)

st.divider()
st.caption("提示：占卜結果僅供參考，請保持平常心。")
