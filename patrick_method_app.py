import streamlit as st
from itertools import combinations

# Patrick Method 簡化函數
def get_minimum_sop(minterms, pi_chart):
    pi_list = list(pi_chart.items())
    min_cover_solutions = []

    for r in range(1, len(pi_list)+1):
        found = False
        for combo in combinations(pi_list, r):
            covered = set()
            combo_names = []
            for name, covered_minterms in combo:
                covered.update(covered_minterms)
                combo_names.append(name)
            if set(minterms) == covered:
                min_cover_solutions.append(combo_names)
                found = True
        if found:
            break

    return min_cover_solutions

# Streamlit 介面
st.title("Patrick Method 最小 SOP 化簡工具")

# 輸入 minterms
minterm_str = st.text_input("請輸入 minterms（用逗號分隔，例如 1,3,7,11）")
minterms = [int(x.strip()) for x in minterm_str.split(",") if x.strip().isdigit()]

# 輸入 PI 表
st.markdown("請輸入 PI 表（每行格式：term: m1,m2,...）")
pi_text = st.text_area("例如：\nA'B'C: 1\nA'BC: 3\nAB'C: 7,15\nABC: 11")

# 解析 PI 表輸入
pi_chart = {}
for line in pi_text.strip().splitlines():
    if ":" in line:
        term, covered = line.split(":")
        pi_chart[term.strip()] = [int(x.strip()) for x in covered.split(",")]

# 按鈕：執行 Patrick Method
if st.button("化簡"):
    if minterms and pi_chart:
        results = get_minimum_sop(minterms, pi_chart)
        st.subheader("最小 SOP 結果：")
        for r in results:
            st.write(" + ".join(r))
    else:
        st.warning("請完整輸入 minterms 和 PI 表。")
