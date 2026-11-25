"""A = {1, 2, 3, 4, 5}의 동치관계 판별과 폐포."""

A = (1, 2, 3, 4, 5)
N = len(A)


def read_matrix():
    matrix = []
    for a in A:
        while True:
            tokens = input(f"{a}행> ").split()
            if len(tokens) == N and all(v in ("0", "1") for v in tokens):
                matrix.append([int(v) for v in tokens])
                break
            print("입력 오류: 0 또는 1을 공백으로 구분해 5개 입력하세요.")
    return matrix


def is_reflexive(m):
    return all(m[i][i] for i in range(N))


def is_symmetric(m):
    return all(m[i][j] == m[j][i] for i in range(N) for j in range(i + 1, N))


def is_transitive(m):
    for i in range(N):
        for j in range(N):
            for k in range(N):
                if m[i][j] and m[j][k] and not m[i][k]:
                    return False
    return True


def properties(m):
    return is_reflexive(m), is_symmetric(m), is_transitive(m)


def equivalence_class(m, a):
    return [b for b, present in zip(A, m[a - 1]) if present]


def print_classes(m):
    for a in A:
        members = ", ".join(map(str, equivalence_class(m, a)))
        print(f"[{a}] = {{{members}}}")


def reflexive_closure(m):
    result = [row[:] for row in m]
    for i in range(N):
        result[i][i] = 1
    return result


def symmetric_closure(m):
    return [[m[i][j] | m[j][i] for j in range(N)] for i in range(N)]


def transitive_closure(m):
    result = [row[:] for row in m]
    # k는 이번 단계에서 사용할 수 있게 된 중간 원소다.
    for k in range(N):
        for i in range(N):
            for j in range(N):
                result[i][j] |= result[i][k] & result[k][j]
    return result


def first_violation(m, kind):
    if kind == "반사":
        i = next(i for i in range(N) if not m[i][i])
        return f"({A[i]}, {A[i]}) 없음"
    if kind == "대칭":
        i, j = next((i, j) for i in range(N) for j in range(N)
                    if m[i][j] and not m[j][i])
        return f"({A[i]}, {A[j]}) 있음, ({A[j]}, {A[i]}) 없음"
    i, j, k = next((i, j, k) for i in range(N) for j in range(N) for k in range(N)
                   if m[i][j] and m[j][k] and not m[i][k])
    return f"({A[i]}, {A[j]}), ({A[j]}, {A[k]}) 있음, ({A[i]}, {A[k]}) 없음"


def print_matrix(m, title):
    print(title)
    print("    1 2 3 4 5")
    for a, row in zip(A, m):
        print(f"{a} | " + " ".join(map(str, row)))


def print_properties(m, show_witness=False):
    flags = properties(m)
    print(" / ".join(f"{name}: {'O' if ok else 'X'}"
                     for name, ok in zip(("반사", "대칭", "추이"), flags)))
    if show_witness:
        for name, ok in zip(("반사", "대칭", "추이"), flags):
            if not ok:
                print(f"{name} 반례: {first_violation(m, name)}")
    print("동치관계입니다." if all(flags) else "동치관계가 아닙니다.")
    return all(flags)


def print_closure_step(m, name, closure):
    result = closure(m)
    print(f"\n[단계] {name} 폐포")
    print_matrix(m, "변환 전")
    print_matrix(result, "변환 후")
    added = sum(result[i][j] - m[i][j] for i in range(N) for j in range(N))
    print(f"추가한 순서쌍: {added}개" if added else "이미 조건 충족: 변경 없음")
    return result


def main():
    print("A = {1, 2, 3, 4, 5}의 관계행렬 (0/1, 5행)")
    try:
        m = read_matrix()
    except (EOFError, KeyboardInterrupt):
        print("\n입력이 중단되었습니다.")
        return

    print_matrix(m, "\n[입력] 관계행렬")
    print("\n[판별] 입력 관계")
    if print_properties(m, show_witness=True):
        print("\n[결과] 원소별 동치류")
        print_classes(m)
        return

    for name, closure in (("반사", reflexive_closure),
                          ("대칭", symmetric_closure),
                          ("추이", transitive_closure)):
        m = print_closure_step(m, name, closure)

    print("\n[재판별] 폐포 변환 결과")
    if print_properties(m):
        print("\n[결과] 원소별 동치류")
        print_classes(m)


if __name__ == "__main__":
    main()
