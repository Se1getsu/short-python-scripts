"""
以下のルールに則って行われるブラックジャックの確率計算・期待値計算を行う。

- Duplicates allowed (draw with replacement)
- Max 5 cards per hand (player & dealer)
- J,Q,K = 10, A = 1 or 11 (best value ≤ 21)
- Dealer must HIT on 16 or less, STAND on 17 or more
- Blackjack on initial 2 cards (total 21) -> payout 3x bet (this world: immediate win)
- Normal win -> payout 2x bet, push -> 1x bet, surrender -> 0.5x bet returned
- DOUBLE: doubling draws exactly one card and then player cannot HIT anymore.
- SURRENDER: allowed any time, even after HIT/DOUBLE in this world; returns half the bet.
"""

from argparse import ArgumentParser
from dataclasses import dataclass
from fractions import Fraction
import sys
from typing import List, Tuple, Dict

# MARK: - Constants

RANKS = list('A23456789') + ['10'] + list('JQK')
MAX_CARDS = 5  # 手札の最大枚数
BUST = 999     # >21 を表す値

LOSE_MULTIPLIER = Fraction(-1)          # 敗北の配当倍率
SURRENDER_MULTIPLIER = Fraction(-1, 2)  # サレンダーの配当倍率
DRAW_MULTIPLIER = Fraction(0)           # 引き分けの配当倍率
WIN_MULTIPLIER = Fraction(1)            # 通常勝利の配当倍率
BLACKJACK_MULTIPLIER = Fraction(2)      # ブラックジャックの配当倍率

# MARK: - Structures

@dataclass
class HandState:
    ncard: int       # 手札の枚数
    current_sum: int # A=1 とした時の手札の合計値
    nace: int        # 手札の A の枚数

    @classmethod
    def from_cards(cls, cards: List[str]) -> 'HandState':
        return cls(
            ncard=len(cards),
            current_sum=sum(card_value(c) for c in cards),
            nace=cards.count('A')
        )

    def copy(self) -> 'HandState':
        return HandState(self.ncard, self.current_sum, self.nace)

# MARK: - Game Specifications

def card_value(rank: str) -> int:
    """
    カードのランクから値を返す (A=1)
    """
    if rank in 'JQK' or rank == '10':
        return 10
    elif rank == 'A':
        return 1
    else:
        return int(rank)

def hand_value(hand: HandState) -> Tuple[int]:
    """
    A を 1 または 11 として数え、手札の最良の値を計算する
    """
    elevens = max(min((21 - hand.current_sum) // 10, hand.nace), 0)
    best_value = hand.current_sum + elevens * 10
    return best_value

def is_blackjack(hand: HandState) -> bool:
    """
    手札がブラックジャックかどうかを判定する
    """
    return hand.ncard == 2 and hand_value(hand) == 21

# MARK: - ディーラーの確率計算

def _dealer_probabilities(
    dealer: HandState
) -> Dict[int, Fraction]:
    """
    ディーラーの手札が ncard 枚、合計 current_sum、A を nace 枚持っている時、
    key=(10|11|...|21|bust) になる確率を計算する
    """
    # 結果を 0 で初期化
    outcomes = {k: Fraction(0) for k in range(10, 22)} | {BUST: Fraction(0)}

    # 終了条件
    if dealer.current_sum > 21:
        outcomes[BUST] = Fraction(1)
        return outcomes
    if dealer.ncard == MAX_CARDS or hand_value(dealer) >= 17:
        outcomes[hand_value(dealer)] = Fraction(1)
        return outcomes

    # 手札を増やす
    for drawn_card in RANKS[:-3]:  # 10, J, Q, K は同じ扱い
        new_dealer = dealer.copy()
        new_dealer.ncard += 1
        new_dealer.current_sum += card_value(drawn_card)
        new_dealer.nace += int(drawn_card == 'A')
        for k, v in _dealer_probabilities(new_dealer).items():
            outcomes[k] += v * Fraction(4 if drawn_card == '10' else 1, len(RANKS))
    return outcomes

dealer_probabilities_cache: Dict[str, Dict[int, Fraction]] = {}

def dealer_probabilities(
    dealer_card: str
) -> Dict[int, Fraction]:
    """
    ディーラーの見えているカードが dealer_card の時、
    key=(10|11|...|21|bust) になる確率を計算する
    """
    if dealer_card in dealer_probabilities_cache:
        return dealer_probabilities_cache[dealer_card]

    initial_dealer = HandState.from_cards([dealer_card])
    dealer_probabilities_cache[dealer_card] = _dealer_probabilities(initial_dealer)
    return _dealer_probabilities(initial_dealer)

# MARK: - プレイヤーの期待値計算

def expected_value_if_hit(my_hand: HandState, dealer_card: str) -> Fraction:
    """
    プレイヤーがヒットした場合の、賭け金の倍率の期待値を計算する
    """
    ev = Fraction(0)
    for drawn_card in RANKS[:-3]:  # 10, J, Q, K は同じ扱い
        new_hand = my_hand.copy()
        new_hand.ncard += 1
        new_hand.current_sum += card_value(drawn_card)
        new_hand.nace += int(drawn_card == 'A')
        if new_hand.current_sum > 21:
            ev += LOSE_MULTIPLIER * Fraction(4 if drawn_card == '10' else 1, len(RANKS))
        else:
            es, a = expected_value(new_hand, dealer_card)
            ev += es[a] * Fraction(4 if drawn_card == '10' else 1, len(RANKS))
    return ev

def expected_value_if_stand(my_hand: HandState, dealer_card: str) -> Fraction:
    """
    プレイヤーがスタンドした場合の、賭け金の倍率の期待値を計算する
    """
    ev = Fraction(0)
    ps = dealer_probabilities(dealer_card)
    my_value = hand_value(my_hand)
    for dealer_value, p in ps.items():
        if dealer_value == BUST or my_value > dealer_value:
            ev += WIN_MULTIPLIER * p
        elif my_value == dealer_value:
            ev += DRAW_MULTIPLIER * p
        else:
            ev += LOSE_MULTIPLIER * p
    return ev

def expected_value_if_double(my_hand: HandState, dealer_card: str) -> Fraction:
    """
    プレイヤーがダブルした場合の、賭け金の倍率の期待値を計算する
    """
    ev = Fraction(0)
    for drawn_card in RANKS[:-3]:  # 10, J, Q, K は同じ扱い
        new_hand = my_hand.copy()
        new_hand.ncard += 1
        new_hand.current_sum += card_value(drawn_card)
        new_hand.nace += int(drawn_card == 'A')
        if new_hand.current_sum > 21:
            ev += LOSE_MULTIPLIER * 2 * Fraction(4 if drawn_card == '10' else 1, len(RANKS))
        else:
            es, a = expected_value(new_hand, dealer_card, doubled=True)
            ev += es[a] * Fraction(4 if drawn_card == '10' else 1, len(RANKS))
    return ev

def expected_value(
    my_hand: HandState,
    dealer_card: str,
    doubled: bool = False,
) -> Tuple[Dict[str, Fraction], str]:
    """
    プレイヤーが最適な行動を取った場合の、賭け金の倍率の期待値を計算する
    """
    actions = {}
    if doubled:
        actions['STAND'] = expected_value_if_stand(my_hand, dealer_card) * 2
        actions['SURRENDER'] = SURRENDER_MULTIPLIER * 2
    elif my_hand.ncard == 2:
        actions['HIT'] = expected_value_if_hit(my_hand, dealer_card)
        actions['STAND'] = expected_value_if_stand(my_hand, dealer_card)
        actions['DOUBLE'] = expected_value_if_double(my_hand, dealer_card)
        actions['SURRENDER'] = SURRENDER_MULTIPLIER
    elif my_hand.ncard < MAX_CARDS:
        actions['HIT'] = expected_value_if_hit(my_hand, dealer_card)
        actions['STAND'] = expected_value_if_stand(my_hand, dealer_card)
        actions['SURRENDER'] = SURRENDER_MULTIPLIER
    else:
        actions['STAND'] = expected_value_if_stand(my_hand, dealer_card)

    best_action = max(actions, key=actions.get)
    return actions, best_action

# MARK: - ゲーム全体の期待値の計算

def overall_expected_value() -> Fraction:
    """
    全ての初期手札とディーラーの見えているカードの組み合わせに対する、
    プレイヤーが最適な行動を取った場合の、賭け金の倍率の期待値を計算する
    """
    ev = Fraction(0)
    total_combinations = Fraction(len(RANKS) ** 3)

    for my_card1 in RANKS:
        for my_card2 in RANKS:
            if is_blackjack(HandState.from_cards([my_card1, my_card2])):
                ev += BLACKJACK_MULTIPLIER * Fraction(len(RANKS), total_combinations)
                continue
            for dealer_card in RANKS:
                my_hand = HandState.from_cards([my_card1, my_card2])
                es, a = expected_value(my_hand, dealer_card)
                ev += es[a] * Fraction(1, total_combinations)
    return ev

# MARK: - メイン処理

def main():
    def parse_card_input(card_char: str) -> str:
        assert len(card_char) == 1
        if card_char == '0':
            return '10'
        elif card_char in RANKS:
            return card_char
        else:
            raise ValueError(f"未定義のカード: {card_char}")

    print("入力例: 30aq (ディーラーの見えているカードが Q、手札が 3, 10, A の場合)")
    inp = input("状況: ").upper().strip()
    *my_hand, dealer_card = [parse_card_input(c) for c in inp]

    while len(my_hand) < 5:
        print()
        es, a = expected_value(HandState.from_cards(my_hand), dealer_card)
        for action, ev in es.items():
            out = "* " if action == a else "  "
            out += f"{action:9s}: {float(ev):6.3f}x"
            print(out)
        print()

        if len(my_hand) >= 4: break
        inp = input("次のカード(終了する場合は Enter): ").upper().strip()
        if not inp:
            break
        if len(inp) == 1:
            my_hand.append(parse_card_input(inp))
        else:
            *my_hand, dealer_card = [parse_card_input(c) for c in inp]

if __name__ == "__main__":
    parser = ArgumentParser(description="ブラックジャックの確率・期待値計算ツール")
    parser.add_argument("-d", "--dealer-prob", action="store_true", help="ディーラーの確率分布を表示する")
    parser.add_argument("-e", "--entire", action="store_true", help="ゲーム全体の期待値を計算する")
    args = parser.parse_args()

    if args.dealer_prob:
        print("    " + " ".join(f"{i:8d}" for i in range(10, 22)) + f" {'BUST':>8s}")
        for rank in RANKS:
            p = dealer_probabilities(rank)
            out = f"{rank:>2s}: "
            for v in p.values():
                out += f"{float(v*100):7.3f}% "
            print(out)
        sys.exit(0)

    if args.entire:
        ev = overall_expected_value()
        print(f"{ev} = {float(ev):.4f}x")
        sys.exit(0)

    main()
