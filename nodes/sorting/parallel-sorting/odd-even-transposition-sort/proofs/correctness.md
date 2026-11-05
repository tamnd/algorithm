---
title: Odd-even transposition sort sorts in n rounds
proves: [correctness]
status: full
---

The comparators of ODD-EVEN-TRANSPOSITION-SORT do not depend on the keys, so the algorithm is a comparator network. Each comparator only exchanges two keys, so the output is a permutation of the input. By the [zero-one principle](/zero-one-principle/) it is enough to show that the output is sorted for each input in $\{0, 1\}^n$. In the rest of the proof the keys are zeros and ones, positions are $0, \ldots, n-1$, and round $t$ applies the comparators $[i : i+1]$ with $i \equiv t - 1 \pmod 2$.

**Moves of the ones.** A comparator $[i : i+1]$ changes the array only if $A[i] = 1$ and $A[i+1] = 0$, and then it moves the one from $i$ to $i + 1$. So a one moves only to the right, by one position, and only when the position to its right holds a zero. Two ones are never exchanged, so the ones keep their left-to-right order. Let $k$ be the number of ones, and number them $1, \ldots, k$ from the right. Let $P_j(t)$ be the position of one $j$ at the start of round $t$. One $j$ has $j - 1$ ones to its right, so $P_j(t) \le n - j$ at all times. We call $n - j$ the *target* of one $j$. The output is sorted exactly when each one $j$ is at its target.

**Alignment.** Say that one $j$ is *aligned* in round $t$ when $P_j(t) \equiv t - 1 \pmod 2$, that is, when the comparator $[P_j(t) : P_j(t) + 1]$ is used in round $t$. One $j$ can move in round $t$ only if it is aligned, because the other comparator that touches its position, $[P_j(t) - 1 : P_j(t)]$, has a one on its right wire and does not move it. Two facts follow from the definition, since $t$ grows by one in each round.

- (A1) If one $j$ is not aligned in round $t$, it does not move, so it is aligned in round $t + 1$.
- (A2) If one $j$ is aligned in round $t$ and moves, then $P_j(t+1) = P_j(t) + 1$, so it is aligned in round $t + 1$.

Say that one $j$ is *blocked* in round $t$ when it is aligned, $P_j(t) < n - j$, and $A[P_j(t) + 1] = 1$. An aligned one that is not blocked and not at its target moves in round $t$.

**Lemma.** For each $j \in \{1, \ldots, k\}$:

1. in each round $t \ge j$, one $j$ is not blocked;
2. in each round $t \ge j + 1$ with $P_j(t) < n - j$, one $j$ is aligned, so it moves.

*Proof.* By induction on $j$.

Part 1. For $j = 1$ no one is to the right of one 1, so it is never blocked. Let $j \ge 2$ and $t \ge j$, and assume that one $j$ is aligned with $P_j(t) < n - j$ and $A[P_j(t) + 1] = 1$. The one at position $P_j(t) + 1$ is the next one to the right, which is one $j - 1$. So $P_{j-1}(t) = P_j(t) + 1 < n - (j - 1)$, and one $j - 1$ is not at its target. Since $t \ge j = (j - 1) + 1$, part 2 for $j - 1$ says that one $j - 1$ is aligned in round $t$. But $P_{j-1}(t) = P_j(t) + 1$ has the other parity, and one $j$ is aligned, so one $j - 1$ is not aligned. This is a contradiction, so one $j$ is not blocked.

Part 2. First take round $j + 1$. In round $j$, one $j$ is aligned or not. If it is not aligned, then by (A1) it is aligned in round $j + 1$. If it is aligned and $P_j(j) < n - j$, then by part 1 it is not blocked, so it moves, and by (A2) it is aligned in round $j + 1$. If it is aligned and $P_j(j) = n - j$, then $P_j(j+1) = n - j$ and the claim for round $j + 1$ says nothing. Now let $t \ge j + 1$ and assume that one $j$ is aligned in round $t$ with $P_j(t) < n - j$. By part 1 it is not blocked, so it moves, and by (A2) it is aligned in round $t + 1$. By induction on $t$, the claim holds for each round $t \ge j + 1$ in which $P_j(t) < n - j$. $\square$

**Theorem.** After round $n$, the array is sorted.

*Proof.* Take a one $j$. Positions never decrease, so $P_j(j+1) \ge 0$, and one $j$ is at most $n - j$ positions from its target at the start of round $j + 1$. By part 2 of the lemma, in each round from $j + 1$ on, one $j$ moves one step to the right until it is at its target, and then it stays there, since $P_j \le n - j$ always. The rounds $j + 1, \ldots, n$ are $n - j$ rounds, so one $j$ is at its target after round $n$. This holds for each $j$, so the ones fill the positions $n - k, \ldots, n - 1$ and the zeros fill the positions $0, \ldots, n - k - 1$. The array is sorted. By the zero-one principle the network sorts every input. $\blacksquare$

**Stability.** Line L5 exchanges $A[i]$ and $A[i+1]$ only when $A[i] > A[i+1]$. An exchange of two neighbours changes the relative order of only these two keys, and these two keys are not equal. So equal keys never change their relative order.
