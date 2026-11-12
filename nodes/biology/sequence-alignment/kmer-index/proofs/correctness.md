---
title: The k-mer index returns exactly the indexed occurrences, in increasing order
proves: [correctness]
status: full
---

Let $T$ have length $n$ over $\Sigma = \{A, C, G, T\}$ plus other letters, let $k \ge 1$ and $s \ge 1$. A position $p$ is *indexed* when $0 \le p \le n - k$, $p \bmod s = 0$ and $T[p \ldots p+k-1]$ holds only letters of $\Sigma$. Write $I$ for the set of indexed positions, $P = |I|$, and $c_p$ for the code of $T[p \ldots p+k-1]$ when $p \in I$.

**Lemma 1 (codes).** The map $c(x) = \sum_{i=1}^{k} v(x_i)\, 4^{k-i}$ is a bijection from $\Sigma^k$ to $\{0, 1, \ldots, 4^k - 1\}$, and the rolling update gives $c_p$ for each $p \in I$.

*Proof.* The map writes $x$ as a number with $k$ digits in base 4, with digit values $v(x_i) \in \{0, 1, 2, 3\}$. Each integer in $[0, 4^k)$ has exactly one such representation, so the map is a bijection. For the rolling update, let $u$ be the code after the letter $T[i]$, taken over the last $\min(k, r)$ letters, where $r$ is the number of letters of $\Sigma$ since the last letter outside $\Sigma$. The step $u \leftarrow (4u \bmod 4^k) + v(T[i])$ shifts the digits by one place, drops the digit that leaves the window, and appends the new digit. By induction on $i$, $u$ is the code of the last $\min(k, r)$ letters. When $r \ge k$, the window $T[i-k+1 \ldots i]$ holds only letters of $\Sigma$ and $u = c_{i-k+1}$. When $r < k$, the window holds a letter outside $\Sigma$ and the position is not indexed. $\square$

**Lemma 2 (bucket bounds).** After line L5, for each code $c$, `off[c]` is the number of positions $p \in I$ with $c_p < c$, and `off[c+1] - off[c]` is the number of positions $p \in I$ with $c_p = c$.

*Proof.* After lines L1 to L3, `cnt[c]` is the number of $p \in I$ with $c_p = c$, since the loop visits each indexed position once. Line L5 sets `off[c+1] = off[c] + cnt[c]` with `off[0] = 0`, so by induction on $c$, `off[c]` is $\sum_{d < c}$ `cnt[d]`. $\square$

**Lemma 3 (fill).** Let $p_1 < p_2 < \cdots < p_P$ be the indexed positions. Before the step of lines L8 and L9 for $p_t$, the following invariant holds for every code $c$:

> **(F)** `next[c]` $=$ `off[c]` $+ a_c$, where $a_c$ is the number of $j < t$ with $c_{p_j} = c$, and `pos[off[c] .. next[c] - 1]` holds these $a_c$ positions in increasing order.

*Proof.* Before the first step, line L6 sets `next[c] = off[c]` and $a_c = 0$ for all $c$, so (F) holds with empty slices. In the step for $p_t$, let $c = c_{p_t}$. Line L8 writes $p_t$ into slot `next[c]`, and line L9 adds one to `next[c]`. Now $a_c$ grows by one, so the first part of (F) holds for $c$. The slice of $c$ gets $p_t$ at its right end, and $p_t$ is larger than every earlier position, so the slice stays increasing. For the other codes nothing changes. The slot `next[c]` is less than `off[c+1]`, because $a_c$ before the step is less than the total number of positions of code $c$, which by Lemma 2 is `off[c+1] - off[c]`. So the write stays inside the bucket of $c$ and does not touch another bucket. $\square$

**Theorem.** After BUILD-KMER-INDEX, for each $x \in \Sigma^k$, LOOKUP$(x)$ returns the increasing list of all $p \in I$ with $T[p \ldots p+k-1] = x$. LOOKUP returns the empty list for a string with a letter outside $\Sigma$, and SEED-HITS$(Q)$ returns exactly the pairs $(q, p)$ with $Q[q \ldots q+k-1] = T[p \ldots p+k-1]$, $Q[q \ldots q+k-1] \in \Sigma^k$ and $p \in I$.

*Proof.* After the last step of the fill, (F) holds with $t = P + 1$, so $a_c$ is the number of all indexed positions with code $c$, which by Lemma 2 is `off[c+1] - off[c]`. So the slice `pos[off[c] .. off[c+1] - 1]` holds all indexed positions of code $c$, in increasing order. By Lemma 1, $c_p = c(x)$ holds exactly when $T[p \ldots p+k-1] = x$. Line L13 returns this slice for $c = c(x)$, which proves the first claim. A string with a letter outside $\Sigma$ is never an indexed k-mer, so line L11 is correct. SEED-HITS calls LOOKUP for each k-mer of $Q$ over $\Sigma$ (its codes come from the rolling update, correct by Lemma 1), and appends one pair for each returned position, which gives the third claim. $\square$

**Theorem (sampled index).** Let $s = k$. If $Q[a \ldots a+\ell-1] = T[b \ldots b+\ell-1]$ with $\ell \ge 2k - 1$ and both strings over $\Sigma$, then SEED-HITS$(Q)$ returns a pair $(a + p - b, p)$ with $b \le p$ and $p + k \le b + \ell$.

*Proof.* Let $p$ be the smallest multiple of $k$ with $p \ge b$. Then $p \le b + k - 1$, so $p + k \le b + 2k - 1 \le b + \ell$. The k-mer $T[p \ldots p+k-1]$ lies inside the match, so it holds only letters of $\Sigma$, and $p \le n - k$; so $p \in I$. With $q = a + (p - b)$, the match gives $Q[q \ldots q+k-1] = T[p \ldots p+k-1]$. By the theorem above, SEED-HITS returns $(q, p)$. $\square$

The bound $2k - 1$ is tight: for $\ell = 2k - 2$ and $b = 1$, the window $T[1 \ldots 2k-2]$ holds no full k-mer that starts at a multiple of $k$, because the only candidate $p = k$ ends at $2k - 1$.
