---
title: Batch GCD returns gcd(N_i, the product of the other inputs) for each i
proves: [correctness, termination, time.worst, bit_operations.worst, bit_operations.schoolbook]
status: full
---

We use the pseudocode BATCH-GCD of the page, on positive integers $N_1, \ldots, N_n$ with $n \ge 1$. Let $P = \prod_j N_j$ and $Q_i = \prod_{j \ne i} N_j$, so $P = N_i Q_i$. The levels $T[0], \ldots, T[h]$ are lists of positive integers, and each element of $T[\ell + 1]$ is the product of one or two consecutive elements of $T[\ell]$, its children.

**Lemma 1 (product tree).** The loop of lines L3 to L5 stops with $h = \lceil \lg n \rceil$, and $T[h] = [P]$. Each node is the product of the leaves below it, and each leaf lies below exactly one node of each level.

*Proof.* A level of length $L > 1$ produces a level of length $\lceil L/2 \rceil < L$, so the loop stops, after $\lceil \lg n \rceil$ rounds, at length $1$. Each element of $T[\ell + 1]$ is the product of its children, and the children of distinct elements are disjoint and cover $T[\ell]$, in order. By induction on $\ell$, the elements of $T[\ell]$ are the products of disjoint runs of consecutive leaves that cover all leaves. At level $h$ the single run is all leaves, so $T[h] = [P]$. $\square$

**Lemma 2 (nested reduction).** Let $X, Y \ge 1$ with $Y \mid X$, and let $A$ be an integer. Then $(A \bmod X^2) \bmod Y^2 = A \bmod Y^2$.

*Proof.* $A - (A \bmod X^2)$ is a multiple of $X^2$, hence of $Y^2$, since $Y^2 \mid X^2$. Two integers that differ by a multiple of $Y^2$ have the same remainder modulo $Y^2$. $\square$

**Lemma 3 (remainder tree).** After line L8 for level $\ell < h$, each node $Y$ of level $\ell$ has $R[Y] = P \bmod Y^2$.

*Proof.* We show by downward induction on $\ell$, from $\ell = h$, that each node $X$ of level $\ell$ has $R[X] \ge 0$ and $R[X] \equiv P \pmod{X^2}$. At level $h$, line L6 sets $R = [P]$, which satisfies both. Assume it for level $\ell + 1$, and let $Y$ be a child of $X$, so $Y \mid X$ by Lemma 1 and $Y^2 \mid X^2$. Line L8 sets $R[Y] = R[X] \bmod Y^2$. Since $R[X] \equiv P \pmod{X^2}$, also $R[X] \equiv P \pmod{Y^2}$, and by Lemma 2 (or directly), $R[X] \bmod Y^2 = P \bmod Y^2$. So $R[Y] = P \bmod Y^2$, which is non-negative and congruent to $P$ modulo $Y^2$. $\square$

**Theorem 1 (correctness).** BATCH-GCD returns $g_i = \gcd(N_i, Q_i)$ for each $i$.

*Proof.* If $n = 1$, then $h = 0$, the loop of line L7 does not run, $R[1] = N_1$, and line L10 returns $\gcd(N_1, 1) = 1 = \gcd(N_1, Q_1)$, since $Q_1$ is the empty product $1$. Let $n \ge 2$, so $h \ge 1$ and the leaves are at level $0 < h$. By Lemma 3, $R[i] = P \bmod N_i^2$. Divide $Q_i$ by $N_i$: $Q_i = s N_i + t$ with $0 \le t < N_i$. Then $P = N_i Q_i = s N_i^2 + N_i t$ and $0 \le N_i t < N_i^2$, so $P \bmod N_i^2 = N_i t$. So $R[i]$ is divisible by $N_i$ and $R[i]/N_i = t = Q_i \bmod N_i$. Line L10 returns $\gcd(N_i, Q_i \bmod N_i) = \gcd(N_i, Q_i)$, since $Q_i$ and $Q_i \bmod N_i$ differ by a multiple of $N_i$ and so have the same common divisors with $N_i$. $\square$

**Zero and signs.** The wrapper replaces each input by its absolute value, which changes no gcd. With one zero at position $i$, $Q_i = \prod_{j \ne i} N_j$ and $g_i = \gcd(0, Q_i) = |Q_i|$, while for $j \ne i$ the product of the others is $0$, and $\gcd(N_j, 0) = |N_j|$. With two or more zeros, every product of the others is $0$, so $g_j = |N_j|$ for all $j$. These are the values the wrapper returns before calling the trees.

**Theorem 2 (cost).** Let $m = \sum_i \ell_i$ with $\ell_i$ the number of binary digits of $N_i$, and let $M(k)$ be the cost of multiplying two $k$-digit integers, with division with remainder in $O(M(k))$ and $M(k)/k$ non-decreasing. Then lines L1 to L8 cost $O(M(m) \log n)$ bit operations, and with a gcd of cost $O(M(k) \log k)$ the whole algorithm costs $O(M(m) \log m)$. With $M(k) = O(k \log k)$ this is $O(m \log^2 m)$; with schoolbook arithmetic, $M(k) = O(k^2)$ and the total is $O(m^2)$.

*Proof.* A product of numbers with $a$ and $b$ digits has at most $a + b$ digits. So by Lemma 1 the elements of each level have total length at most $m$ digits, and a level of the product tree costs $\sum M(a_j + b_j) \le M(m)$ by the superadditivity that follows from $M(k)/k$ non-decreasing. In the remainder tree, a node $Y$ with parent $X$ reduces a number below $X^2$, of at most $2\,\mathrm{len}(X)$ digits, modulo $Y^2$; this costs $O(M(\mathrm{len}(X)))$, and the parents of one level have total length at most $m$, each counted for at most two children, so each level costs $O(M(m))$. There are $\lceil \lg n \rceil$ levels, so both trees cost $O(M(m) \log n)$. The gcds of line L10 are on numbers of at most $\ell_i$ digits, costing $O(M(\ell_i) \log \ell_i)$ each, in total $O(M(m) \log m)$. Since $n \le m$, the total is $O(M(m) \log m)$.

For schoolbook arithmetic, multiplying an $a$-digit by a $b$-digit number costs $O(ab)$, and dividing an $a$-digit number by a $b$-digit number costs $O(b(a - b + 1))$. In the product tree, a node with children of lengths $a$ and $b$ costs $O(ab)$; expanding $a$ and $b$ as sums of leaf lengths, each pair of leaves $i \ne i'$ contributes $\ell_i \ell_{i'}$ at their lowest common ancestor only, so the whole tree costs $O(\sum_{i < i'} \ell_i \ell_{i'}) = O(m^2)$. In the remainder tree, a node $Y$ with sibling $Z$ and parent $X = YZ$ reduces a number of at most $2(\mathrm{len}(Y) + \mathrm{len}(Z))$ digits modulo $Y^2$, of about $2\,\mathrm{len}(Y)$ digits, at cost $O(\mathrm{len}(Y) (\mathrm{len}(Z) + 1))$; a node without sibling costs $O(\mathrm{len}(Y))$. The products $\mathrm{len}(Y)\mathrm{len}(Z)$ again sum to $O(m^2)$ over the tree, and the other terms are $O(m)$ per level, $O(m \log n) \le O(m^2)$ in total. The Euclidean gcds of line L10 cost $O(\sum \ell_i^2) \le O(m^2)$. So the total is $O(m^2)$. The loops all have fixed bounds, so the algorithm terminates. $\blacksquare$
