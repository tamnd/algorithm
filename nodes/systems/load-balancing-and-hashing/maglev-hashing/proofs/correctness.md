---
title: The Maglev population fills the table, stops, and gives each backend the floor or the ceiling of M/N slots
proves: [correctness]
status: full
---

We use the pseudocode of the page, with a table size $M$ that is prime, $N \ge 1$ backends, $0 \le \text{offset}[i] < M$ and $1 \le \text{skip}[i] \le M - 1$. Write $p_i(j) = (\text{offset}[i] + j \cdot \text{skip}[i]) \bmod M$ for the $j$-th preferred slot of backend $i$.

**Lemma 1 (each list is a permutation).** For each $i$, $p_i(0), \ldots, p_i(M-1)$ are the $M$ slots, each once.

*Proof.* If $p_i(j) = p_i(j')$ with $0 \le j < j' \le M - 1$, then $M$ divides $(j' - j) \cdot \text{skip}[i]$. $M$ is prime and divides neither factor, because $0 < j' - j < M$ and $0 < \text{skip}[i] < M$. This is a contradiction. So the $M$ values are distinct, and there are $M$ slots. $\square$

**Lemma 2 (the pointer invariant).** At each point of the run, for each backend $i$, the slots $p_i(0), \ldots, p_i(\text{next}[i] - 1)$ are all filled, and $\text{filled}$ is the number of filled slots.

*Proof.* At the start, $\text{next}[i] = 0$ and nothing is filled. A filled slot never becomes empty, because only line L9 writes the table, and it writes only an empty slot (the loop of line L7 has just found $\text{entry}[c] < 0$). Line L8 increases $\text{next}[i]$ only after it has seen that slot $p_i(\text{next}[i])$ is filled. Line L10 increases $\text{next}[i]$ right after line L9 has filled slot $p_i(\text{next}[i])$, and adds 1 to $\text{filled}$ for the one new filled slot. $\square$

**Lemma 3 (a turn always succeeds).** Each time line L6 starts a turn of backend $i$ with $\text{filled} < M$, the loop of line L7 stops with $\text{next}[i] \le M - 1$, at an empty slot.

*Proof.* Some slot is empty. By Lemma 1 it is $p_i(j)$ for some $j \le M - 1$, and by Lemma 2 we have $j \ge \text{next}[i]$, since the slots before $\text{next}[i]$ are filled. The loop of line L7 moves $\text{next}[i]$ up by one at a time, so it reaches an empty slot at some position at most $j \le M - 1$. $\square$

**Theorem 1 (termination and a full table).** POPULATE stops after exactly $M$ turns, and then every slot holds a backend.

*Proof.* By Lemma 3 each turn with $\text{filled} < M$ fills exactly one new slot, so $\text{filled}$ goes up by exactly 1 in each turn. Line L11 returns when $\text{filled} = M$, which is after $M$ turns, and then all $M$ slots are filled. Each turn does a finite number of steps of line L8, at most $M$ in total for backend $i$ by Lemma 3, so the run is finite: at most $N M$ steps of line L8 in all. $\square$

**Theorem 2 (exact counts).** Write $M = qN + r$ with $0 \le r < N$. Backends $0, \ldots, r-1$ get $q + 1$ slots and backends $r, \ldots, N-1$ get $q$ slots. So any two counts differ by at most 1.

*Proof.* The turns go through the backends in the order $0, 1, \ldots, N-1, 0, 1, \ldots$, and by Theorem 1 each turn gives one slot to its backend. The run has exactly $M$ turns, which are $q$ full rounds of $N$ turns and then $r$ turns of backends $0$ to $r - 1$. $\blacksquare$

**What does not hold.** There is no statement like the [monotonicity property](/monotonicity-property/). When a backend is removed, the turns of the others change, and a backend can take a slot that it did not own before from another backend that stays. The paper's own example (Table 1, $M = 7$, three backends) has one such slot. The page reports the measured fractions.
