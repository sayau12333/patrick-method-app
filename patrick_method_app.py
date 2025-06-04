import streamlit as st

def decimal_to_binary(n, width):
    return format(n, f'0{width}b')

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

def simplify(minterms, num_vars):
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

def term_to_expression(term, var_names):
    expression = ""
    for i, val in enumerate(term):
        if val == "1":
            expression += var_names[i]
        elif val == "0":
            expression += var_names[i] + "'"
    return expression

st.title("Patrick Method - Minimum SOP 簡化器")

st.markdown("### 輸入參數")
num_vars = st.number_input("請輸入變數數量（例如3代表 A, B, C）", min_value=2, max_value=8, value=3)
var_names = [chr(ord('A') + i) for i in range(num_vars)]

minterm_input = st.text_input("請輸入 minterms（用逗號分隔，例如：1,3,5,7）")

if st.button("進行化簡"):
    try:
        minterms = [int(x.strip()) for x in minterm_input.split(",") if x.strip().isdigit()]
        max_val = 2 ** num_vars - 1
        minterms = [m for m in minterms if 0 <= m <= max_val]
        if not minterms:
            st.error("請至少輸入一個合法的 minterm")
        else:
            prime_implicants = simplify(minterms, num_vars)
            simplified = [term_to_expression(t, var_names) for t in prime_implicants]

            st.markdown("### 最小化 SOP 結果")
            st.write(" + ".join(simplified))

            st.markdown("### Prime Implicants（中間步驟）")
            st.write(prime_implicants)
    except Exception as e:
        st.error(f"發生錯誤：{e}")
