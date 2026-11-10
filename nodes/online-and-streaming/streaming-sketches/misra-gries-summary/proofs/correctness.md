---
title: The Misra-Gries estimates are within m/k below the true counts, also after merges
proves: [correctness]
status: full
---

A summary is a pair $(C, m)$, where $C$ maps at most $k - 1$ items to positive integers and $m$ is the length of the stream it summarizes. Write $\hat f_x = C[x]$ if $x \in C$ and $\hat f_x = 0$ otherwise, and write $|C|_1 = \sum_y C[y]$. Let $f_x$ be the true count of $x$ in the stream. Define the **slack** $s = m - |C|_1$.

**Invariant (I).** For every item $x$:

1. $0 \le \hat f_x \le f_x$, and
2. $k \, (f_x - \hat f_x) \le s$.

**Lemma 1.** The empty summary $(\{\}, 0)$ of the empty stream satisfies (I), and MG-UPDATE keeps (I).

*Proof.* For the empty stream all counts and estimates are 0 and $s = 0$. Now assume (I) before MG-UPDATE$(C, x)$. Line L1 adds 1 to $m$ and the update adds 1 to $f_x$. Write $s'$ and $\hat f'$ for the values after the update.

- *Line L2.* $C[x]$ grows by 1, so $|C|_1$ grows by 1 and $s' = s$. The estimate and the true count of $x$ both grow by 1, and nothing else changes. So both parts of (I) hold.
- *Line L3.* Here $x \notin C$, so $\hat f_x = 0$, and the new counter is 1. Again $|C|_1$ and $m$ both grow by 1, so $s' = s$, and $f_x - \hat f_x$ does not change. The estimate $1$ is at most the new count $f_x + 1$.
- *Lines L4 to L6.* Here $x \notin C$ and $|C| = k - 1$. Each of the $k - 1$ counters is at least 1 and falls by exactly 1, so $|C|_1$ falls by $k - 1$, while $m$ grows by 1. So $s' = s + k$. Each estimate $\hat f_y$ with $y \in C$ falls by 1, and $f_y$ does not change, so $f_y - \hat f_y$ grows by 1. For $x$, the estimate stays 0 and $f_x$ grows by 1, so $f_x - \hat f_x$ grows by 1. For every other item nothing changes. So for each item, $k(f - \hat f)$ grows by at most $k$, which is the growth of the slack. The estimates stay non-negative because a counter that reaches 0 is removed, and they stay at most the true counts because they only fell.

In each case (I) holds after the update. $\square$

**Lemma 2.** If $(C_1, m_1)$ and $(C_2, m_2)$ satisfy (I) for streams $\sigma_1$ and $\sigma_2$ with the same $k$, then MG-MERGE returns a summary $(C, m_1 + m_2)$ that satisfies (I) for the concatenation $\sigma_1 \sigma_2$, with $|C| \le k - 1$.

*Proof.* Let $f = f^{(1)} + f^{(2)}$ be the counts of the concatenation. After line L8, $C[x] = \hat f^{(1)}_x + \hat f^{(2)}_x$, so the slack is $s = s_1 + s_2$, and by (I) for both parts,
$$ k(f_x - C[x]) = k(f^{(1)}_x - \hat f^{(1)}_x) + k(f^{(2)}_x - \hat f^{(2)}_x) \le s_1 + s_2 = s, \qquad 0 \le C[x] \le f_x . $$
If $|C| \le k - 1$, line L9 returns this $C$. Otherwise let $c > 0$ be the $k$-th largest counter, and let $C'$ be the result of line L11, $C'[x] = \max(C[x] - c, 0)$, without the zeros.

- Each estimate falls by at most $c$: $C[x] - C'[x] \le c$.
- The sum falls by at least $kc$: the $k$ largest counters are each at least $c$, and each of them falls by exactly $c$. So the new slack is $s' \ge s + kc$.

Hence $k(f_x - C'[x]) \le k(f_x - C[x]) + kc \le s + kc \le s'$. The new estimates are non-negative and at most the old ones, so they are at most $f_x$. Only counters strictly larger than $c$ stay positive. At most $k - 1$ counters are strictly larger than the $k$-th largest one, so $|C'| \le k - 1$. $\square$

**Theorem.** Each summary built from the empty summary by updates and merges satisfies, for every item $x$,
$$ f_x - \frac{m}{k} \;\le\; f_x - \frac{m - |C|_1}{k} \;\le\; \hat f_x \;\le\; f_x . $$
In particular, each item with $f_x > m/k$ is in $C$.

*Proof.* By induction on the number of operations, Lemmas 1 and 2 give (I). Part 2 of (I) divided by $k$ is the middle inequality, and $|C|_1 \ge 0$ gives the left one. If $f_x > m/k$, then $\hat f_x \ge f_x - m/k > 0$, so $x \in C$. $\blacksquare$

**The number of decrement steps.** For a summary built only by updates, the slack grows by exactly $k$ in each decrement step and by 0 otherwise. So the number $D$ of decrement steps is $s/k = (m - |C|_1)/k$, and each estimate is low by at most $D$.
