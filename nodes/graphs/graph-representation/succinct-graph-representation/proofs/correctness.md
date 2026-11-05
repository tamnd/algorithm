---
title: The Elias-Fano graph structure answers access, rank, adjacency, degree and neighbour queries correctly
proves: [correctness]
status: full
---

We use the pseudocode of the page. Let $N = n^2$, let $P = \{p_0 < \cdots < p_{m-1}\} \subseteq [0, N)$ be the numbers $un + v$ of the arcs, let $l \ge 0$ be fixed, and write $h_i = \lfloor p_i / 2^l \rfloor$ and $\ell_i = p_i \bmod 2^l$, so $p_i = h_i 2^l + \ell_i$. The structure stores $\texttt{low}[i] = \ell_i$ and a bit vector `high` of length $m + \lfloor N/2^l \rfloor + 1$ with 1s exactly at the positions $c_i = h_i + i$.

**Claim 1 (the layout).** The positions $c_i$ are distinct and $c_0 < c_1 < \cdots < c_{m-1}$, and the number of 0s before $c_i$ is $h_i$.

*Proof.* Since $p_i < p_{i+1}$, $h_i \le h_{i+1}$, so $c_{i+1} = h_{i+1} + i + 1 > c_i$. The positions before $c_i$ hold the 1s $c_0, \ldots, c_{i-1}$, which are $i$ in number, and $c_i - i = h_i$ zeros. Also $c_{m-1} \le \lfloor (N-1)/2^l \rfloor + m - 1$, which is inside the vector. $\square$

**Claim 2 (ACCESS).** By Claim 1, $\texttt{select1}(i) = c_i$, so line L1 returns $(c_i - i) 2^l + \ell_i = h_i 2^l + \ell_i = p_i$. $\square$

**Claim 3 (RANK).** For $0 \le x \le N$, RANK$(x)$ returns $|\{i : p_i < x\}|$.

*Proof.* Let $h = \lfloor x / 2^l \rfloor$ and $r = x \bmod 2^l$. By Claim 1, the 1s with exactly $j$ zeros before them are the elements with $h_i = j$; so the elements with $h_i < h$ are exactly the 1s before the $h$-th zero (counted from 1), that is, before position $q = \texttt{select0}(h - 1) + 1$, or $q = 0$ when $h = 0$. The vector has $\lfloor N / 2^l \rfloor + 1 \ge h + 1$ zeros, so this select exists. Before $q$ there are $q$ positions, $h$ of them zeros, so line L4 sets $k = q - h = |\{i : h_i < h\}|$.

The elements with $h_i = h$ are the 1s in the run that starts at $q$, in increasing order of $i$, hence of $\ell_i$. An element with $h_i < h$ is below $x$, one with $h_i > h$ is not, and one with $h_i = h$ is below $x$ if and only if $\ell_i < r$. Lines L5 and L6 keep the invariant "$k$ is the index of the element at position $q$, and all elements before it are below $x$": each step passes an element of the bucket with $\ell_k < r$. The loop stops at the first 0, the end of the bucket, or at the first element of the bucket with $\ell_k \ge r$; all later elements of the bucket have larger low bits and are not below $x$. So line L7 returns $|\{i : p_i < x\}|$. The loop runs at most the size $s$ of the bucket. $\square$

**Claim 4 (ADJACENT).** Let $p = un + v$ and $k$ = RANK$(p)$. If $p \in P$ then $p = p_k$, since exactly $k$ elements are smaller, and line L10 returns true. If $p \notin P$, then either $k = m$, or $p_k > p$ is the smallest element at least $p$, and line L10 returns false. $\square$

**Claim 5 (DEGREE and NEIGHBOR).** The arcs out of $u$ are the $(u, v)$ with $0 \le v < n$, so their numbers are exactly the elements of $P$ in $[un, un + n)$. Their count is RANK$(un + n)$ − RANK$(un)$, which is line L11. They are $p_k, \ldots, p_{k + d - 1}$ for $k$ = RANK$(un)$, in increasing order of $v$, so line L12 returns the $i$-th smallest out-neighbour $p_{k+i} - un$. $\square$

**Space.** Let $t = \log_2(N/m)$, so $l = \lfloor t \rfloor$, and write $f = t - l \in [0, 1)$. Then $N / 2^l = m 2^f$, and the fields use $ml + m + \lfloor N/2^l \rfloor + 1 \le m(t + 1 + 2^f - f) + 1$ bits. On $[0, 1)$ the function $2^f - f$ is convex and equals 1 at both ends, so it is at most 1, and the total is at most $m(2 + \log_2(N/m)) + 1$ bits. $\blacksquare$
