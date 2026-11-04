---
title: An xor filter accepts every key of its set
proves: [correctness, invariant, termination]
status: full
---

Let $S$ be a set of $n$ distinct keys. For fixed hash functions write $E(x) = \{h_0(x), h_1(x), h_2(x)\}$, a set of three distinct cells, one in each block.

**Lemma 1 (peeling order).** If PEEL$(S)$ succeeds, its order $(x_1, c_1), \ldots, (x_n, c_n)$ lists each key of $S$ once, and for each $t$, $c_t \in E(x_t)$ and $c_t \notin E(x_{t'})$ for each $t' > t$.

*Proof.* Call a key *remaining* while it is not yet in the order. Lines L6 and L9 keep, for each cell $c$, the count and the xor of the indices of the remaining keys $y$ with $c \in E(y)$: line L6 sets them for all keys, and line L9 removes a key from its three cells when it leaves. When line L8 takes a cell $c$ with count 1, exactly one remaining key uses $c$, and the xor is its index. That key $x_t$ is appended and stops being remaining. So $c_t \in E(x_t)$, each key is appended at most once, and the keys $x_{t'}$ with $t' > t$ were remaining at that time and are not $x_t$, so they do not use $c_t$. Success at line L10 means all $n$ keys are listed. $\square$

**Lemma 2.** In the loop of lines L4 and L5, the cell $c_t$ is written only at step $t$, and after step $t$ no cell of $E(x_t)$ is written.

*Proof.* Step $t'$ writes only $c_{t'}$. For $t' > t$, $c_t \notin E(x_{t'})$ by Lemma 1, while $c_{t'} \in E(x_{t'})$, so $c_{t'} \ne c_t$. The steps after step $t$ are the steps $t' < t$, and they write $c_{t'}$, which is not in $E(x_t)$ by Lemma 1 applied to $t'$ and the later index $t$. $\square$

**Theorem 1 (invariant (X) and no false negatives).** After BUILD, $B[h_0(x)] \oplus B[h_1(x)] \oplus B[h_2(x)] = \mathrm{fp}(x)$ for each $x \in S$, so QUERY$(x)$ returns true.

*Proof.* Take $x = x_t$, and let $u, v$ be the two cells of $E(x_t)$ other than $c_t$. Line L5 sets $B[c_t] = \mathrm{fp}(x_t) \oplus B[u] \oplus B[v]$, so right after step $t$, $B[c_t] \oplus B[u] \oplus B[v] = \mathrm{fp}(x_t)$, since $a \oplus a = 0$. By Lemma 2 none of the three cells changes after step $t$. Line L11 then computes the same xor. $\square$

**Theorem 2 (termination).** Under ideal hashing, with a fresh independent choice of hash functions in each try, BUILD ends with probability 1, and the number of tries has a geometric distribution.

*Proof.* Each try succeeds with the same probability $p$, independently. It remains to show $p > 0$, by one choice of the cells that peels. Since $3\ell \ge 1.23 n + 32$, we have $3(\ell - 1) \ge n$, so we can give each key $x$ a *private* cell $\pi(x)$, all distinct, using at most $\ell - 1$ cells of each block, and keep one *spare* cell $z_j$ in each block $j$. Let the other two cells of $x$ be the spare cells of the two other blocks. Then each $\pi(x)$ has count 1 and is in the first queue, and peeling removes the keys one after another, so it succeeds. This choice of cells has positive probability under ideal hashing. Each try is $O(n)$ steps, since each key leaves the queue at most once. $\blacksquare$
