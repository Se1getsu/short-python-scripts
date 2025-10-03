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

from dataclasses import dataclass
from fractions import Fraction
from typing import List, Tuple, Dict

# MARK: - Constants

RANKS = list('A23456789') + ['10'] + list('JQK')
MAX_CARDS = 5  # 手札の最大枚数
BUST = 999     # >21 を表す値

LOSE_MULTIPLIER = Fraction(0)           # 敗北の配当倍率
SURRENDER_MULTIPLIER = Fraction(1, 2)   # サレンダーの配当倍率
DRAW_MULTIPLIER = Fraction(1)           # 引き分けの配当倍率
WIN_MULTIPLIER = Fraction(2)            # 通常勝利の配当倍率
BLACKJACK_MULTIPLIER = Fraction(3)      # ブラックジャックの配当倍率

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
        mult = 4 if drawn_card == '10' else 1
        for k, v in _dealer_probabilities(new_dealer).items():
            outcomes[k] += v / len(RANKS) * mult
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
    pass

def expected_value_if_stand(my_hand: HandState, dealer_card: str) -> Fraction:
    """
    プレイヤーがスタンドした場合の、賭け金の倍率の期待値を計算する
    """
    pass

def expected_value_if_double(my_hand: HandState, dealer_card: str) -> Fraction:
    """
    プレイヤーがダブルした場合の、賭け金の倍率の期待値を計算する
    """
    pass

def expected_value_if_surrender(my_hand: HandState) -> Fraction:
    """
    プレイヤーがサレンダーした場合の、賭け金の倍率の期待値を計算する
    """
    return SURRENDER_MULTIPLIER

# MARK: - メイン処理

def main():
    print("    " + " ".join(f"{i:8d}" for i in range(10, 22)) + f" {'BUST':>8s}")
    for rank in RANKS:
        p = dealer_probabilities(rank)
        out = f"{rank:>2s}: "
        for v in p.values():
            out += f"{float(v*100):7.3f}% "
        print(out)

if __name__ == "__main__":
    main()
