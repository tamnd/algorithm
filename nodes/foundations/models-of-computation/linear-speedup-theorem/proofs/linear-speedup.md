---
title: Compressing m symbols into one cell speeds up a multitape machine by the factor m
id: linear-speedup
proves: [linear-speedup]
method: induction
form: full
sources:
  - {title: "Hartmanis and Stearns, On the computational complexity of algorithms, Transactions of the American Mathematical Society 117, 1965", locator: "pp. 285 to 306"}
  - {book: "isbn:9780201530827", locator: "Papadimitriou 1994, Chapter 2"}
---

**Statement.** Let $k \ge 2$ and let $M$ be a deterministic $k$-tape machine (as on the [multitape Turing machine](/multitape-turing-machine/) page) that halts on every input and decides $L$. Let $n_0 \ge 0$ and $m \ge 1$ be integers, and let $t$ be a function with $t(n) \ge n$ such that on every input of length $n \ge n_0$ the machine $M$ halts within $t(n)$ steps. Then there is a deterministic $k$-tape machine $M'$ with $L(M') = L$ such that on every input of length $n$ the machine $M'$ halts within

$$
T'(n) \le n + 1 \quad \text{if } n < n_0, \qquad T'(n) \le n + \lceil n/m \rceil + 6\lceil t(n)/m \rceil - 1 \quad \text{if } n \ge n_0 .
$$

For every $\varepsilon > 0$, the choice $m = \lceil 14/\varepsilon \rceil$ and $n_0 = \lceil 8/\varepsilon \rceil$ (and $n_0 \ge$ the bound from which $t$ holds) gives $T'(n) \le \varepsilon\, t(n) + n + 2$ for all $n$.

**Setup.** The tapes of $M$ and $M'$ are infinite to the right, with cells numbered $0, 1, \ldots$. A head on cell $0$ that moves $L$ stays. The input $w = w_1 \cdots w_n$ is in cells $0$ to $n-1$ of tape 1. Let $\Gamma$ be the tape alphabet of $M$, with blank $\sqcup$. Write $q_0$ for its start state. Let $t' \ge 1$ be the running time of $M$ on $w$. The value $t' \ge 1$ holds because the start state is not a halting state. For $n \ge n_0$ we have $t' \le t(n)$.

The tape alphabet of $M'$ is $\Gamma \cup (\Gamma^m \times \{0, 1\})$. A *block* is an element $(a_0, \ldots, a_{m-1}; e)$ of $\Gamma^m \times \{0,1\}$. The bit $e$ is the *end flag*. A cell of $M'$ that holds $\sqcup$ is read as the block $(\sqcup, \ldots, \sqcup; 0)$.

*The roles of the tapes.* Tape $1$ of $M$ is kept on tape $2$ of $M'$. Tape $2$ of $M$ is kept on tape $1$ of $M'$. Tape $i$ of $M$ is kept on tape $i$ of $M'$ for $i \ge 3$. This swap is the place where $k \ge 2$ is used: tape $1$ of $M'$ holds the input at the start, and it is free for use after the input is copied. Let $\tau(i)$ be the tape of $M'$ that keeps tape $i$ of $M$. Let $o_2 = n$ and $o_i = 0$ for $i \ne 2$. For $b \ge 0$, block $b$ of tape $i$ of $M$ is the cell $o_i + b$ of tape $\tau(i)$ of $M'$. It holds the cells $bm, bm+1, \ldots, bm+m-1$ of tape $i$ of $M$, in this order. Only block $0$ has the end flag $e = 1$.

*The finite control.* The state of $M'$ holds a state $q$ of $M$, an offset $p_i \in \{0, \ldots, m-1\}$ for each tape $i$, and a bounded buffer: at most $m$ symbols during the copy, at most $n_0 - 1$ symbols of the input, and three blocks for each tape during a simulation round. All of these come from finite sets, so $M'$ has finitely many states.

**Proof.**

*Step 1: copy the input.* Let $c = \lceil n/m \rceil$.

- Transition $i$, for $1 \le i \le n$: head $1$ reads $w_i$ in cell $i - 1$, writes $\sqcup$ and moves right. The control keeps $w_i$ in its buffer. If $m$ divides $i$, head $2$ writes the block $(w_{i-m+1}, \ldots, w_i;\ e)$ in its cell and moves right, with $e = 1$ if $i = m$ and $e = 0$ otherwise. Otherwise head $2$ stays. In transition $1$, heads $3, \ldots, k$ write the block $(\sqcup, \ldots, \sqcup; 1)$ and stay.
- Transition $n + 1$: head $1$ reads the blank in cell $n$. If $n < n_0$, the control holds the whole input, because it keeps the first $n_0 - 1$ symbols. Then $M'$ halts at once with the verdict of $M$ on $w$. This verdict exists because $M$ halts on every input. So $T'(n) = n + 1$ and the first claim holds. If $n \ge n_0$, head $1$ writes the block $(\sqcup, \ldots, \sqcup; 1)$ on its cell $n$ and stays. This is block $0$ of tape $2$ of $M$. If $n = 0$, transition $1$ is this transition, and head $2$ writes $(\sqcup, \ldots, \sqcup; 1)$ on cell $0$ and stays, and heads $3, \ldots, k$ do what transition 1 says. If $n \ge 1$ and $m \nmid n$, head $2$ writes the last block, padded with $\sqcup$, with $e = 1$ if $n < m$, and stays on cell $c - 1$. If $n \ge 1$ and $m \mid n$, head $2$ moves left to cell $c - 1$.
- Transitions $n + 2, \ldots, n + c$: head $2$ moves left. It moves left in each cell where it reads $e = 0$. It reads $e = 1$ in cell $0$ after $c - 1$ moves. At that reading, the machine does not spend a separate transition. The reading is transition 1 of the read phase of round 1: it moves head 2 as that transition says (move $S$), and the other heads, which are already on block $0$, read their blocks in the same transition.

Now every head of $M'$ is on block $0$ of the tape that it keeps. The tapes hold the blocks of the initial configuration of $M$: the blocks of tape $1$ hold $w$ followed by blanks, and all other blocks are blank. The copy takes $n + c$ transitions if $n \ge 1$, and $1$ transition if $n = 0$.

*Step 2: the invariant.* A *round* simulates $m$ steps of $M$. Let $r \ge 0$. We call the following statement $I_r$, for a round number $r$ with $rm < t'$. After the copy and $r$ rounds, the control holds the state $q$ of $M$ after $rm$ steps and the offsets $p_i = x_i \bmod m$, where $x_i$ is the position of head $i$ of $M$ after $rm$ steps. Head $\tau(i)$ of $M'$ is on block $\lfloor x_i / m \rfloor$ of its tape. Block $b$ of each tape holds the cells $bm, \ldots, bm + m - 1$ of the corresponding tape of $M$ after $rm$ steps. Statement $I_0$ holds at the end of step 1, since the head positions of $M$ are $0$ at the start.

*Step 3: a round, assuming $I_r$ and $rm < t'$.* Let $b_i = \lfloor x_i / m \rfloor$ be the block of head $i$.

- *Read (4 transitions).* In parallel for each tape $i$: the head of $\tau(i)$ makes the moves $L, R, R, L$ if the block $b_i$ has $e = 0$, and the moves $S, S, R, L$ if it has $e = 1$. After the four transitions the head is on block $b_i$ again, and the control has read the blocks $b_i - 1$ (if $e = 0$), $b_i$ and $b_i + 1$ of each tape.
- *Decide (no transition).* The control runs $M$ for up to $m$ steps from its state, in its memory, on the three blocks of each tape. This is possible because, in at most $m$ steps, head $i$ stays inside these three blocks. It starts at offset $p_i$ in block $b_i$, and in $j \le m$ steps it moves at most $j$ cells, so it stays in the cells $b_i m - m$ to $b_i m + 2m - 1$. If $b_i = 0$, the left block does not exist, and the head cannot move there, because the left-end rule keeps it on cell $0$. The control knows when the head of $M$ is on cell $0$: this holds exactly when $e = 1$ and the offset is $0$. Also, head $i$ cannot visit both the left block and the right block. To visit a cell of the left block (a cell with number below $b_i m$) and a cell of the right block (number at least $b_i m + m$), the head moves at least $m + 1$ cells between the two visits, and it has only $m$ steps. So for each $i$ there is at most one neighbor block $Y_i$ that the head visits.
- *Halting.* If $M$ halts within these $m$ steps, then $M'$ halts at once, in transition $4$ of the round, with the same verdict.
- *Write (2 transitions).* Otherwise $M$ makes exactly $m$ steps and is not halted. Let $q'$ be its new state and $x_i'$ the new position of head $i$. The final block $F_i = \lfloor x_i' / m \rfloor$ is $b_i$ or the block $Y_i$. In transition $5$ the head of $\tau(i)$ writes the new content of block $b_i$ (with its old end flag) and moves toward $Y_i$, or stays if $Y_i$ does not exist. In transition $6$ it writes the new content of $Y_i$, with its old end flag, and moves to $F_i$: it stays if $F_i = Y_i$, and it moves back to block $b_i$ if $F_i = b_i$. If $Y_i$ does not exist, it does nothing in transition $6$. The control now holds $q'$ and the offsets $x_i' \bmod m$.

The blocks other than $b_i$ and $Y_i$ do not change, because no head of $M$ visits them. So $I_{r+1}$ holds. Notice that the round uses $6$ transitions if $M$ does not halt, and $4$ transitions if it halts.

*Step 4: correctness.* By induction on $r$ using step 3, $I_r$ holds for every round $r$ with $rm < t'$, and $M'$ does not halt before round $h = \lceil t'/m \rceil$. In round $h$ the machine $M$ halts within the $m$ simulated steps, because $(h-1)m < t' \le hm$. Then $M'$ halts with the verdict of $M$. So $M'$ accepts $w$ exactly when $M$ accepts $w$, for $n \ge n_0$ by this argument and for $n < n_0$ by step 1.

*Step 5: time.* Let $n \ge n_0$. Step 1 takes at most $n + \lceil n/m \rceil$ transitions if $n \ge 1$ and $1$ transition if $n = 0$. Rounds $1, \ldots, h - 1$ take $6$ transitions each, and round $h$ takes $4$. So the total is at most

$$
(n + \lceil n/m \rceil) + 6(h - 1) + 4 = n + \lceil n/m \rceil + 6h - 2 \quad (n \ge 1), \qquad 1 + 6(h-1) + 4 = 6h - 1 \quad (n = 0).
$$

In both cases it is at most $n + \lceil n/m \rceil + 6\lceil t(n)/m \rceil - 1$, because $h = \lceil t'/m \rceil \le \lceil t(n)/m \rceil$. For $n < n_0$ the time is $n + 1$ by step 1.

*Step 6: the choice of $m$ and $n_0$.* Let $\varepsilon > 0$, $m = \lceil 14/\varepsilon \rceil$ and $n_0 = \lceil 8/\varepsilon \rceil$ (or larger, to meet the hypothesis on $t$). If $n < n_0$, then $T'(n) \le n + 1 \le \varepsilon\, t(n) + n + 2$. Let $n \ge n_0$. Use $\lceil x \rceil \le x + 1$ and $n \le t(n)$:

$$
T'(n) \le n + \frac{n}{m} + 1 + \frac{6\,t(n)}{m} + 6 - 1 \le n + 6 + \frac{7\,t(n)}{m} \le n + 6 + \frac{\varepsilon\, t(n)}{2},
$$

because $m \ge 14/\varepsilon$. Since $t(n) \ge n \ge n_0 \ge 8/\varepsilon$, we have $\varepsilon\,t(n)/2 \ge 4$, so $6 \le 2 + \varepsilon\, t(n)/2$. Hence $T'(n) \le n + 2 + \varepsilon\, t(n)$. $\blacksquare$
