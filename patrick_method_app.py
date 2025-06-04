import streamlit as st
from collections import defaultdict

# 十進位轉固定長度二進位
def decimal_to_binary(n, width):
    return format(n, f'0{width}b')

# 合併只差一位的 term
def combine_terms(term1, term2):
    diff = 0
    combined = ""
    for a, b in zip(term1, term2):
        if a != b:
            diff += 1
            combined += "-"
        else:
            combined += a
    return combined if diff == 1 else None

# 產生所有 Prime Implicants（含重複）
def generate_prime_implicants(minterms, num_vars):
    minterms = list(set(minterms))
    terms = [decimal_to_binary(m, num_vars) for m in minterms]
    unchecked = terms[:]
    prime_implicants = []

    while unchecked:
        next_terms = []
        used = set()
        for i in range(len(unchecked)):
            for j in range(i + 1, len(unchecked)):
                combined = combine_terms(unchecked[i], unchecked[j])
                if combined:
                    next_terms.append(combined)
                    used.add(unchecked[i])
                    used.add(unchecked[j])
        for term in unchecked:
            if term not in used and term not in prime_implicants:
                prime_implicants.append(term)
        unchecked = list(set(next_terms))
    
    return prime_implicants

# 轉成 A'B 型式
def term_to_expression(term, var_names):
    expression = ""
    for i, val in enumerate(term):
        if val == "1":
            expression += var_names[i]
        elif val == "0":
            expression += var_names[i] + "'"
    return expression

# 某 term 是否能覆蓋一個 minterm
def term_covers_minterm(term, minterm):
    for t_bit, m_bit in zip(term, minterm):
        if t_bit != '-' and t_bit != m_bit:
            return False
    return True

# 為某函數選出覆蓋其 minterms 的最小 SOP
def select_covering_terms(minterms, prime_implicants, num_vars):
    minterms_bin = [decimal_to_binary(m, num_vars) for m in minterms]
    selected = []
    uncovered = set(minterms_bin)

    for pi in prime_implicants:
        for m in minterms_bin:
            if m in uncovered and term_covers_minterm(pi, m):
                selected.append(pi)
                uncovered -= {m for m in minterms_bin if term_covers_minterm(pi, m)}
                break
        if not uncovered:
            break

    return selected

# --- Streamlit 介面 ---
st.title("Patrick Method - 多輸出最小 SOP 化簡器")

st.markdown("### 輸入變數數量與函數")
num_vars = st.number_input("請輸入變數數量", min_value=2, max_value=8, value=3)
var_names = [chr(ord('A') + i) for i in range(num_vars)]

st.markdown("### 輸入格式：一行一個輸出函數，例如：")
st.code("F = 1,3,5\nG = 2,3,7")

multi_input = st.text_area("請輸入多個輸出函數", height=150)

if st.button("開始化簡"):
    try:
        func_minterms = {}
        all_minterms = set()

        lines = multi_input.strip().split("\n")
        for line in lines:
            if '=' not in line: continue
            fname, mints = line.split('=')
            fname = fname.strip()
            minterms = [int(x.strip()) for x in mints.split(",") if x.strip().isdigit()]
            func_minterms[fname] = minterms
            all_minterms.update(minterms)

        if not func_minterms:
            st.error("請正確輸入至少一個輸出函數")
        else:
            # 先生成所有的 Prime Implicants（包含 shared）
            all_prime_implicants = generate_prime_implicants(list(all_minterms), num_vars)

            st.markdown("### 各輸出函數的最小 SOP")
            for fname, minterms in func_minterms.items():
                selected_terms = select_covering_terms(minterms, all_prime_implicants, num_vars)
                expression = " + ".join([term_to_expression(t, var_names) for t in selected_terms])
                st.write(f"**{fname}(最小 SOP):** {expression}")

            st.markdown("### 所有 Prime Implicants（含 shared）")
            st.write(all_prime_implicants)

    except Exception as e:
        st.error(f"發生錯誤：{e}")
