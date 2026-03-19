import streamlit as st
import random
import urllib.parse

# 易經 64 卦對照表 (保持不變)
HEXAGRAMS = {
    "111111": "乾為天", "000000": "坤為地", "100010": "水雷屯", "010001": "山水蒙",
    "111010": "水天需", "010111": "天水訟", "010000": "地水師", "000010": "水地比",
    "111011": "風天小畜", "110111": "天澤履", "111000": "地天泰", "000111": "天地否",
    "101111": "天火同人", "111101": "火天大有", "001000": "地山謙", "000100": "雷地豫",
    "100110": "澤雷隨", "011001": "山風蠱", "110000": "地澤臨", "000011": "風地觀",
    "100101": "火雷噬嗑", "101001": "山火賁", "000001": "山地剝", "100000": "地雷復",
    "100111": "天雷無妄", "111001": "山天大畜", "100001": "山雷頤", "011110": "澤風大過",
    "010010": "坎為水", "101101": "離為火", "001110": "澤山咸", "011100": "雷風恆",
    "001111": "天山遯", "111100": "雷天大壯", "000101": "火地晉", "101000": "地火明夷",
    "101011": "風火家人", "110101": "火澤睽", "001010": "水山蹇", "010100": "雷水解",
    "110001": "山澤損", "100011": "風雷益", "111110": "澤天夬", "011111": "天風姤",
    "000110": "澤地萃", "011000": "地風升", "010110": "澤水困", "011010": "水風井",
    "101110": "澤火革", "011101": "火風鼎", "100100": "震為雷", "001001": "艮為山",
    "001011": "風山漸", "110100": "雷澤歸妹", "101100": "雷火豐", "001101": "火山旅",
    "011011": "巽為風", "110110": "兌為澤", "010011": "風水渙", "110010": "水澤節",
    "110011": "風澤中孚", "001100": "雷山小過", "101010": "水火既濟", "010101": "火水未濟"
}

def toss_coins():
    return sum(random.choice([2, 3]) for _ in range(3))

# Streamlit 網頁標題
st.set_page_config(page_title="易經占卜系統", page_icon="☯️")
st.title("☯️ 易經金錢卦智慧占卜-BY 臣")

# 1. 輸入問題
question = st.text_input("請在心中默念您的問題後輸入：", placeholder="例如：這週的面試運勢？")

if st.button("🔮 開始感應起卦", use_container_width=True)
    with st.spinner('正在與天地感應，模擬擲幣中...'):
        base_binary = ""
        changed_binary = ""
        moving_lines = []
        visual_lines = []
        
        # 2. 演算六爻
        for i in range(1, 7):
            score = toss_coins()
            if score == 6:  # 老陰
                base_binary += "0"; changed_binary += "1"
                moving_lines.append(i)
                visual_lines.append(f"第 {i} 爻: ━  ━  × (老陰動)")
            elif score == 7: # 少陽
                base_binary += "1"; changed_binary += "1"
                visual_lines.append(f"第 {i} 爻: ━━━    (少陽靜)")
            elif score == 8: # 少陰
                base_binary += "0"; changed_binary += "0"
                visual_lines.append(f"第 {i} 爻: ━  ━    (少陰靜)")
            elif score == 9: # 老陽
                base_binary += "1"; changed_binary += "0"
                moving_lines.append(i)
                visual_lines.append(f"第 {i} 爻: ━━━  ○ (老陽動)")

        # 3. 獲取卦名
        base_name = HEXAGRAMS[base_binary]
        changed_name = HEXAGRAMS[changed_binary]
        
        # 4. 顯示卦象圖
        st.subheader("【 卦象結果 】")
        for line in reversed(visual_lines):
            st.code(line)
        
        st.success(f"✨ 本卦：**{base_name}**")
        st.info(f"✨ 變卦：**{changed_name if moving_lines else '無'}**")
        
        # 5. 解卦建議
        q_prefix = f"{question} " if question else ""
        if not moving_lines:
            search_query = f"{q_prefix}易經 {base_name} 卦象解釋"
            advice = "六爻皆靜，請參考「本卦」的整體卦辭。"
        elif len(moving_lines) == 1:
            search_query = f"{q_prefix}易經 {base_name} 動第{moving_lines[0]}爻 變 {changed_name}"
            advice = f"有一動爻，重點參考「本卦」第 {moving_lines[0]} 爻的爻辭。"
        else:
            moving_str = ",".join(map(str, moving_lines))
            search_query = f"{q_prefix}易經 {base_name} 變 {changed_name} 卦象解釋"
            advice = f"多爻發動（第 {moving_str} 爻），請綜合參考本卦與變卦【{changed_name}】。"

        st.write(f"💡 **建議**：{advice}")
        
        # 6. 提供搜尋按鈕 (代替 webbrowser.open)
        google_url = f"https://www.google.com/search?q={urllib.parse.quote(search_query)}"
        st.link_button("👉 查看深度解析 (Google)", google_url)
