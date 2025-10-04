import streamlit as st

st.title("🎈 My new app")

st.header("에라토스테네스의 체 체험하기")


# 세션 상태 초기화

if "numbers" not in st.session_state:
    st.session_state.numbers = []
if "max_num" not in st.session_state:
    st.session_state.max_num = 0
if "message" not in st.session_state:
    st.session_state.message = ""
if "clicked_primes" not in st.session_state:
    st.session_state.clicked_primes = []

def reset_state():
    st.session_state.numbers = list(range(2, st.session_state.max_num + 1))
    st.session_state.message = ""
    st.session_state.clicked_primes = []
    st.session_state.stop_prime_check = False


max_num = st.number_input("숫자를 입력하세요 (2 이상의 자연수)", min_value=2, value=30, step=1, key="max_num_input")
if st.button("초기화 및 시작"):
    st.session_state.max_num = max_num
    reset_state()


import math

# 입력한 수가 이미 지워졌으면 합성수 메시지 및 소인수분해 결과 표시 후 동작 중단
def factorize(n):
    factors = []
    d = 2
    while d * d <= n:
        while n % d == 0:
            factors.append(d)
            n //= d
        d += 1
    if n > 1:
        factors.append(n)
    return factors

if st.session_state.numbers:
    input_num = st.session_state.max_num
    sqrt_input = math.isqrt(input_num)
    # 입력한 수가 이미 지워졌으면 합성수 메시지 및 소인수분해 결과 표시 후 동작 중단
    if input_num not in st.session_state.numbers:
        fac = factorize(input_num)
        st.error(f"{input_num}은 합성수입니다! 소인수분해 결과: {' × '.join(map(str, fac))}")
    else:
        # 제곱근 이하의 가장 큰 소수 구하기 (내부적으로만)
        def get_largest_prime(n):
            primes = []
            for i in range(2, n+1):
                is_prime = True
                for p in primes:
                    if i % p == 0:
                        is_prime = False
                        break
                if is_prime:
                    primes.append(i)
            return primes[-1] if primes else None

        largest_prime = get_largest_prime(sqrt_input)

        # 작업 종료 플래그 확인
        if st.session_state.get("stop_prime_check", False):
            st.success(f"{input_num}은 소수입니다! 더 이상 클릭할 필요가 없습니다.")
        else:
            st.subheader("남아있는 수들 (클릭해서 소수/합성수 판별)")
            cols = st.columns(10)
            for idx, num in enumerate(st.session_state.numbers):
                col = cols[idx % 10]
                if col.button(str(num), key=f"num_{num}"):
                    # 클릭한 숫자의 배수들을 즉시 numbers에서 제거
                    st.session_state.numbers = [n for n in st.session_state.numbers if n == num or n % num != 0]
                    if num == largest_prime:
                        st.session_state.stop_prime_check = True
                    st.session_state.message = ""
                    st.rerun()
