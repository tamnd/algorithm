---
title: CCDM is a one-to-one map onto words of the composition c, and its rate is close to the entropy of the type
proves: [correctness]
status: full
---

Fix the symbols $a_1 < \cdots < a_M$ and the counts $c = (c_1, \ldots, c_M)$ with $c_s \ge 0$ and $\sum_s c_s = n \ge 1$. Let $\mathcal{T}_c$ be the set of words of length $n$ with exactly $c_s$ copies of $a_s$, ordered by dictionary order of the symbol indices, and let $T(c) = |\mathcal{T}_c| = n!/\prod_s c_s!$. The rank of a word is its position in this order, starting at $0$.

**Lemma 1 (first symbol).** If $c_s \ge 1$, the number of words of $\mathcal{T}_c$ that start with $a_s$ is $T(c - e_s) = T(c)\, c_s/n$, where $e_s$ is the unit vector of $s$. In particular $T(c)\,c_s/n$ is an integer.

*Proof.* Removing the first symbol is a bijection from the words that start with $a_s$ onto $\mathcal{T}_{c - e_s}$. And $T(c - e_s) = (n - 1)!/\big((c_s - 1)!\prod_{s' \ne s} c_{s'}!\big) = T(c)\cdot c_s/n$. $\square$

**Lemma 2 (unranking).** For $0 \le r < T(c)$, lines L4 to L10 return the word of $\mathcal{T}_c$ with rank $r$.

*Proof.* We show the invariant: at the start of each pass of line L5 with $\ell$ symbols left and the current counts $c'$ (with $\sum c' = \ell$), $N = T(c')$, $0 \le r < N$, and the wanted word is $x_1 \ldots x_{n-\ell}$ followed by the word of rank $r$ in $\mathcal{T}_{c'}$.

It holds at the start, with $\ell = n$, $c' = c$ and $N = T(c)$ (line L4). In one pass, the words of $\mathcal{T}_{c'}$ fall into consecutive groups by their first symbol, in the order $a_1, \ldots, a_M$, because the order is the dictionary order. The groups of the symbols with $c'_s = 0$ are empty. By Lemma 1 the group of $a_s$ has $N_s = N c'_s/\ell$ words (line L7). Line L9 subtracts the sizes of the groups that come before the one that holds rank $r$, and line L8 stops at the group $s$ where the remaining $r$ is less than $N_s$; such a group exists because the sizes add up to $N > r$. Inside that group the remaining $r$ is the rank, and removing the first symbol $a_s$ keeps the order. So after line L8, with $c'_s$ decreased and $N = N_s = T(c' - e_s)$, the invariant holds for $\ell - 1$. When $\ell = 0$, $\mathcal{T}_{c'}$ has only the empty word, and $x_1 \ldots x_n$ is the wanted word. $\square$

**Lemma 3 (ranking).** For $x \in \mathcal{T}_c$, lines L11 to L14 compute the rank of $x$.

*Proof.* By the same grouping, the rank of $x$ in $\mathcal{T}_{c'}$ is the sum of the sizes of the groups of the symbols before $x_t$ (line L13), plus the rank of the rest of the word in $\mathcal{T}_{c' - e_q}$ (line L14 updates $N$ and the counts for it). Induction on the length gives the claim. $\square$

**Lemma 4 (encoder and decoder).** Let $k = \lfloor\log_2 T\rfloor$, so that $2^k \le T$. For $0 \le v < 2^k$, put $r(v) = \lceil vT/2^k\rceil$. Then $0 \le r(v) < T$, $r$ is strictly increasing, and $\lfloor r(v)\, 2^k/T\rfloor = v$.

*Proof.* $r(v) \ge 0$ is clear. Since $v \le 2^k - 1$, $vT/2^k \le T - T/2^k \le T - 1$, so $r(v) \le T - 1$. By the definition of the ceiling, $r(v) - 1 < vT/2^k \le r(v)$. Multiplying by $2^k/T > 0$ gives $v \le r(v)\,2^k/T < v + 2^k/T \le v + 1$, so the floor is $v$. If $v < v'$, then $r(v) \le r(v')$, and $r(v) = r(v')$ would give $v = v'$ by the last claim; so $r$ is strictly increasing. $\square$

**Theorem.** CCDM-ENCODE maps the $2^k$ input blocks one-to-one to words of $\mathcal{T}_c$, and CCDM-DECODE inverts it on its image.

*Proof.* Line L2 maps the $k$ bits one-to-one onto $0 \le v < 2^k$. Line L3 computes $r(v)$, which by Lemma 4 is a valid rank, and Lemma 2 gives the word $x$ of that rank, which lies in $\mathcal{T}_c$. Different $v$ give different ranks (Lemma 4) and so different words, because unranking is a bijection between $\{0, \ldots, T - 1\}$ and $\mathcal{T}_c$. The decoder computes the rank $r(v)$ of $x$ by Lemma 3 and returns $\lfloor r(v)\,2^k/T\rfloor = v$ by Lemma 4, whose $k$ bits are the input. $\blacksquare$

**Lemma 5 (the most likely type class).** Let $Q = c/n$ and let $Q^n$ be the i.i.d. distribution with marginal $Q$. For every composition $c'$ of $n$ with support in the support of $Q$, $Q^n(\mathcal{T}_c) \ge Q^n(\mathcal{T}_{c'})$.

*Proof.* Every word of $\mathcal{T}_{c'}$ has probability $\prod_s Q(a_s)^{c'_s}$, so with $m_s = c_s$ and $l_s = c'_s$, both sums equal to $n$,

$$\frac{Q^n(\mathcal{T}_c)}{Q^n(\mathcal{T}_{c'})} = \prod_s \frac{l_s!}{m_s!}\, Q(a_s)^{m_s - l_s}.$$

For integers $l, m \ge 0$, $l!/m! \ge m^{l - m}$: if $l \ge m$ the left side is a product of $l - m$ factors, each at least $m$; if $l < m$ it is the inverse of a product of $m - l$ factors, each at most $m$. The symbols with $m_s = 0$ have $l_s = 0$ by the support condition, and their factor is 1. For the others, $Q(a_s) = m_s/n$, so

$$\prod_s \frac{l_s!}{m_s!} Q(a_s)^{m_s - l_s} \ge \prod_s m_s^{l_s - m_s} \Big(\frac{m_s}{n}\Big)^{m_s - l_s} = \prod_s n^{l_s - m_s} = n^{\sum_s l_s - \sum_s m_s} = 1. \qquad \square$$

**Proposition (rate).** Let $H(Q) = -\sum_s Q(a_s)\log_2 Q(a_s)$ with $Q = c/n$. Then

$$T \ge \binom{n + M - 1}{M - 1}^{-1} 2^{nH(Q)} \ge \frac{2^{nH(Q)}}{(n + 1)^{M - 1}}, \qquad \frac{k}{n} > H(Q) - \frac{(M - 1)\log_2(n + 1) + 1}{n}.$$

*Proof.* Every word of $\mathcal{T}_c$ has probability $\prod_s Q(a_s)^{c_s} = 2^{-nH(Q)}$ under $Q^n$, so $Q^n(\mathcal{T}_c) = T\,2^{-nH(Q)}$. The words of length $n$ with letters in the support of $Q$ carry all the probability and fall into type classes, one for each composition $c'$ of $n$ with that support. There are at most $\binom{n + M - 1}{M - 1}$ compositions of $n$ into $M$ nonnegative parts. By Lemma 5 each class has probability at most $Q^n(\mathcal{T}_c)$, so

$$1 \le \binom{n + M - 1}{M - 1} T\, 2^{-nH(Q)}.$$

For the second inequality, $\binom{n + M - 1}{M - 1} = \prod_{i=1}^{M-1}\frac{n + i}{i}$ and $(n + i)/i \le n + 1$ for $i \ge 1$. Finally $k = \lfloor\log_2 T\rfloor > \log_2 T - 1 \ge nH(Q) - (M - 1)\log_2(n + 1) - 1$. Divide by $n$. $\square$

So for a fixed alphabet the rate loss $H(Q) - k/n$ is $O(\log n/n)$. If the type is chosen close to the target $P$, as below, $H(c/n)$ tends to $H(P)$, and so does the rate.

**Proposition (the type).** Let $P(a_s) > 0$ for the symbols in its support. The greedy rule of `composition` (start from all counts zero, and $n$ times add one copy to the symbol with the smallest increase of $F(c) = \sum_s c_s\ln\big(c_s/(nP(a_s))\big)$, never to a symbol with $P(a_s) = 0$) returns counts with the smallest $D(c/n\,\|\,P) = F(c)/n$ among all compositions of $n$.

*Proof.* $F$ is a sum of terms $f_s(c_s) = c_s\ln\big(c_s/(nP(a_s))\big)$, with $f_s(0) = 0$. Since $x\ln x$ is convex on $[0, \infty)$, the increments $\delta_s(j) = f_s(j + 1) - f_s(j)$ are nondecreasing in $j$. Any composition $c$ has $F(c) = \sum_s\sum_{j < c_s}\delta_s(j)$, the sum of $n$ elements of the multiset $\{\delta_s(j)\}$ in which each symbol contributes a prefix of its sequence. Such a sum is at least the sum of the $n$ smallest elements of the multiset. The greedy rule takes, at each step, the smallest increment that is still available; since each sequence is nondecreasing, the available increments are always the next ones of their sequences, and the $n$ choices are $n$ smallest elements of the multiset. So the greedy counts reach the lower bound. Symbols with $P(a_s) = 0$ would make $D$ infinite, so an optimal $c$ gives them $0$. $\square$

**Cost.** Each pass of line L7 and line L13 multiplies a number of at most $\log_2 T \le n\log_2 M$ bits by $c_s \le n$ and divides exactly by $\ell \le n$; with $w \ge \log_2 n$ this is $O(n\log M/w)$ word operations. There are at most $M$ passes per symbol and $n$ symbols, which gives $O(Mn^2\log M/w)$ for unranking and ranking. Computing $T$ as a running product takes $n$ such steps. Line L3 and line L15 each do one product of numbers of $O(n\log M)$ bits and one shift or exact division, $O((n\log M/w)^2)$ by schoolbook methods, which is at most $O(Mn^2\log M/w)$ since $\log M/w \le 1 \le M$.
