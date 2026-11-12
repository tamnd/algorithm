---
title: Leapfrog triejoin computes the join, and its number of seeks is within the AGM bound
proves: [correctness, complexity]
status: full
---

Notation. The query has hypergraph $H = (V, E)$ and the global order $v_1, \ldots, v_k$. Each relation $R_e$ is stored as a list of tuples sorted in the lexicographic order of its attributes, taken in the global order. Write $V_{<i} = \{v_1, \ldots, v_{i-1}\}$. For a tuple $t$ over $V_{<i}$ and an edge $e \ni v_i$, let $R_e[t]$ be the set of values $r[v_i]$ over the rows $r \in R_e$ with $r[e \cap V_{<i}] = t[e \cap V_{<i}]$.

**Lemma 1 (iterator).** After the iterator of $R_e$ has been opened along the values $t[e \cap V_{<i}]$ and once more for $v_i$, its range is the block of rows that agree with $t$ on $e \cap V_{<i}$. In this block, the column of $v_i$ is sorted, its distinct values are $R_e[t]$, `next` moves to the first row with a larger key, and `seek(x)` moves to the first row at or after the position with key at least $x$. The `up` operation restores the range and the position from before the matching `open`.

*Proof.* In a lexicographically sorted list, the rows that share a prefix form one contiguous block, and inside the block the next column is sorted. `open` replaces the range by the block of rows that share the current key, which by induction on the depth is the block for the longer prefix. `next` and `seek` are binary searches in the sorted column of the range, starting at the current position. `up` pops the saved state. $\square$

**Lemma 2 (leapfrog intersection).** Let $m \ge 1$ iterators be at one level with key sets $A_1, \ldots, A_m$. The leapfrog join (lines L8 to L16) reports the values of $A_1 \cap \cdots \cap A_m$ in increasing order, each once, and then stops.

*Proof.* Assume no iterator is at the end at the start, otherwise the join stops at line L8 and the intersection is empty because some $A_j$ is empty. Consider the following two invariants, which hold each time line L11 is reached.

- (a) Read cyclically from position $p$, the keys are non-decreasing: $\mathrm{key}(J_p) \le \mathrm{key}(J_{p+1}) \le \cdots \le \mathrm{key}(J_{p-1})$, and $x' = \mathrm{key}(J_{p-1})$ is the largest key.
- (b) Each value of the intersection that has not been reported is at least the key of each iterator.

After line L9 sorts the iterators and sets $p = 0$, (a) holds, and (b) holds because no iterator has moved. Suppose line L12 finds $x \ne x'$. By (a), $x < x'$. Every value that the seek at line L13 skips is in $[x, x')$, and is less than $\mathrm{key}(J_{p-1}) = x'$, so by (b) it is not an unreported value of the intersection. Hence (b) still holds. The new key of $J_p$ is at least $x'$, so it is now the largest key, and with $p$ moved by one, (a) holds again. Suppose line L12 finds $x = x'$. By (a), all keys equal $x$, so $x$ is in every $A_j$, and the join reports $x$. Then line L15 moves $J_p$ past $x$; it skips only $x$, which is reported, so (b) holds, and the new key is larger than all others, so (a) holds after line L16.

Reported values strictly increase, because each report is followed by a move past it and keys never decrease, so each value is reported at most once. Each reported value is in the intersection. When an iterator reaches its end, its key is in effect $+\infty$, and (b) says that no unreported value of the intersection remains. So the join reports exactly the intersection. Each move strictly advances one iterator, so the join stops. $\square$

**Lemma 3 (moves).** Let $n_{\min} = \min_j |A_j|$. The leapfrog join makes at most $m(n_{\min} + 1)$ moves (calls of `seek` and `next`).

*Proof.* Each move is made on $J_p$, and after it $p$ advances by one modulo $m$ (lines L14 and L16). So the moves visit the iterators in cyclic order, and of any $m$ consecutive moves exactly one is on a fixed iterator $J_s$ with $|A_s| = n_{\min}$. Each move on $J_s$ strictly increases its key: a seek is made only when its key is below $x'$ by (a), and `next` moves past the current key. So $J_s$ is moved at most $n_{\min}$ times before it reaches its end, after which the join stops. The number of moves is then at most $m(n_{\min} + 1)$. $\square$

**Theorem 1 (correctness).** Leapfrog triejoin outputs each tuple of the join exactly once, in lexicographic order of $v_1, \ldots, v_k$.

*Proof.* Let $P_i$ be the set of tuples over $v_1, \ldots, v_i$ whose projection on $e \cap \{v_1, \ldots, v_i\}$ is in the matching projection of $R_e$, for each $e$. We show by induction on $i$ that the level-$i$ calls run exactly once for each $t \in P_{i-1}$, in lexicographic order. For a call with prefix $t$, by Lemma 1 the opened iterators of the edges $e \ni v_i$ have key sets $R_e[t]$, so by Lemma 2 the values bound at line L6 are $\bigcap_{e \ni v_i} R_e[t]$ in increasing order. A tuple $(t, a)$ is in $P_i$ if and only if $t \in P_{i-1}$ and $a \in R_e[t]$ for each $e \ni v_i$; for an edge without $v_i$ the condition does not change. So the calls at level $i + 1$ are for the tuples of $P_i$, each once, in lexicographic order. Before each call returns, it calls `up` on each iterator it opened, so by Lemma 1 the caller's iterators are as before. At level $k + 1$, line L2 outputs the tuples of $P_k$, which is the join. $\blacksquare$

**Theorem 2 (work).** Let $W_i = \sum_{t \in P_{i-1}} \min_{e \ni v_i} |R_e[t]|$. For each fractional edge cover $x$ of $H$, $W_i \le \prod_e |R_e|^{x_e}$. So the number of moves at level $i$ is at most $m_i (W_i + |P_{i-1}|)$, where $m_i$ is the number of edges that hold $v_i$, and $|P_{i-1}| \le W_{i-1}$ for $i \ge 2$.

*Proof.* The move bound follows from Lemma 3, summed over the calls at level $i$. For the bound on $W_i$, assume $W_i > 0$. For each $t \in P_{i-1}$, choose an edge $e^*(t) \ni v_i$ with the smallest $R_e[t]$, and let $(T, A)$ be uniform over the $W_i$ pairs $(t, a)$ with $a \in R_{e^*(t)}[t]$. Then $\log W_i = H(T) + H(A \mid T)$, with entropies to base 2.

Given $T = t$, $A$ takes at most $\min_{e \ni v_i} |R_e[t]|$ values. Since the weights of the edges that hold $v_i$ sum to at least 1, $\log \min_e b_e \le \sum_{e \ni v_i} x_e \log b_e$ for $b_e \ge 1$, so $H(A \mid T) \le \sum_{e \ni v_i} x_e \mathbb{E}[\log |R_e[T]|]$.

Let $T_e$ be the restriction of $T$ to $e \cap V_{<i}$. By the chain rule, conditioning, and the cover condition (each attribute has total weight at least 1), $H(T) \le \sum_e x_e H(T_e)$; this is Shearer's lemma.

For $e \not\ni v_i$, $T_e$ takes values in a projection of $R_e$, so $H(T_e) \le \log |R_e|$. For $e \ni v_i$, $|R_e[T]|$ is a function $f(T_e)$, and by Gibbs' inequality $H(T_e) + \mathbb{E}[\log f(T_e)] \le \log \sum_y f(y) \le \log |R_e|$, because the pairs $(y, a)$ with $a \in R_e[y]$ are distinct rows of a projection of $R_e$. Adding up, $\log W_i \le \sum_e x_e \log |R_e|$. $\blacksquare$

**Corollary (running time).** Sorting the relations takes $O(k n \log n)$ time for $n$ input tuples. Each move is a binary search, $O(\log n)$, and each call does $O(m_i \log m_i)$ extra work to sort its iterators and $O(m_i \log n)$ to open them. Summing Theorem 2 over the levels with the best cover gives $O\bigl(k n \log n + k r \cdot \mathrm{AGM}(Q, D) \log n\bigr)$ time, where $r = |E|$ and $\mathrm{AGM}(Q, D) = \min_x \prod_e |R_e|^{x_e}$. With galloping seeks in place of binary search, as in Veldhuizen's paper, the cost of a move is amortized $O(1 + \log(n / n_{\min}))$.
