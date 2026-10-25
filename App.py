import random
import streamlit as st
import matplotlib.pyplot as plt

SIZE = 8

EMPTY = 0
PLAYER = 1
CPU = 2

LETTERS = "ABCDEFGH"

DIRECTIONS = [
    (-1, -1), (-1, 0), (-1, 1),
    (0, -1),           (0, 1),
    (1, -1),  (1, 0),  (1, 1)
]


# ------------------------
# 初期化
# ------------------------
def init_board():
    board = [[EMPTY for _ in range(SIZE)] for _ in range(SIZE)]

    board[3][3] = CPU
    board[3][4] = PLAYER
    board[4][3] = PLAYER
    board[4][4] = CPU

    return board


if "board" not in st.session_state:
    st.session_state.board = init_board()

if "message" not in st.session_state:
    st.session_state.message = ""

if "game_over" not in st.session_state:
    st.session_state.game_over = False


board = st.session_state.board


# ------------------------
# オセロ処理
# ------------------------
def is_valid_move(row, col, stone):

    if board[row][col] != EMPTY:
        return False

    opponent = PLAYER if stone == CPU else CPU

    for dr, dc in DIRECTIONS:

        r = row + dr
        c = col + dc

        found = False

        while 0 <= r < SIZE and 0 <= c < SIZE:

            if board[r][c] == opponent:
                found = True

            elif board[r][c] == stone:

                if found:
                    return True

                break

            else:
                break

            r += dr
            c += dc

    return False


def get_valid_moves(stone):

    moves = []

    for r in range(SIZE):
        for c in range(SIZE):

            if is_valid_move(r, c, stone):
                moves.append((r, c))

    return moves


def make_move(row, col, stone):

    opponent = PLAYER if stone == CPU else CPU

    board[row][col] = stone

    for dr, dc in DIRECTIONS:

        r = row + dr
        c = col + dc

        flips = []

        while 0 <= r < SIZE and 0 <= c < SIZE:

            if board[r][c] == opponent:
                flips.append((r, c))

            elif board[r][c] == stone:

                for fr, fc in flips:
                    board[fr][fc] = stone

                break

            else:
                break

            r += dr
            c += dc


def cpu_choice(moves):

    corners = [
        (0, 0),
        (0, 7),
        (7, 0),
        (7, 7)
    ]

    for corner in corners:
        if corner in moves:
            return corner

    return random.choice(moves)


def count_stones():

    black = sum(row.count(PLAYER) for row in board)
    white = sum(row.count(CPU) for row in board)

    return black, white


# ------------------------
# 描画
# ------------------------
def draw_board():

    fig, ax = plt.subplots(figsize=(6, 6))

    ax.set_facecolor("forestgreen")

    for i in range(SIZE + 1):
        ax.plot([0, SIZE], [i, i], color="black")
        ax.plot([i, i], [0, SIZE], color="black")

    for r in range(SIZE):
        for c in range(SIZE):

            if board[r][c] == PLAYER:

                stone = plt.Circle(
                    (c + 0.5, SIZE - r - 0.5),
                    0.4,
                    color="black"
                )

                ax.add_patch(stone)

            elif board[r][c] == CPU:

                stone = plt.Circle(
                    (c + 0.5, SIZE - r - 0.5),
                    0.4,
                    color="white",
                    ec="black"
                )

                ax.add_patch(stone)

    ax.set_xlim(0, SIZE)
    ax.set_ylim(0, SIZE)

    ax.set_xticks([i + 0.5 for i in range(SIZE)])
    ax.set_xticklabels(list(LETTERS))

    ax.xaxis.tick_top()

    ax.set_yticks([SIZE - i - 0.5 for i in range(SIZE)])
    ax.set_yticklabels(range(1, SIZE + 1))

    ax.tick_params(length=0)

    st.pyplot(fig)


# ------------------------
# 画面
# ------------------------
st.title("オセロ")

draw_board()

black, white = count_stones()

st.write(f"⚫ あなた: {black}")
st.write(f"⚪ CPU: {white}")

player_moves = get_valid_moves(PLAYER)
cpu_moves = get_valid_moves(CPU)

if not player_moves and not cpu_moves:
    st.session_state.game_over = True

if st.session_state.game_over:

    st.subheader("ゲーム終了")

    if black > white:
        st.success("あなたの勝ち！")
    elif white > black:
        st.error("CPUの勝ち！")
    else:
        st.info("引き分け")

else:

    options = [
        f"{LETTERS[c]}{r+1}"
        for r, c in player_moves
    ]

    if options:

        move_text = st.selectbox(
            "手を選んでください",
            options
        )

        if st.button("石を置く"):

            col = LETTERS.index(move_text[0])
            row = int(move_text[1:]) - 1

            make_move(row, col, PLAYER)

            cpu_moves = get_valid_moves(CPU)

            if cpu_moves:

                cpu_move = cpu_choice(cpu_moves)

                make_move(
                    cpu_move[0],
                    cpu_move[1],
                    CPU
                )

            st.rerun()

    else:

        st.warning("置ける場所がありません（パス）")


if st.button("新しいゲーム"):

    st.session_state.board = init_board()
    st.session_state.game_over = False
    st.rerun()
