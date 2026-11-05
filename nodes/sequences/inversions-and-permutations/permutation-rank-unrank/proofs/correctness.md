---
title: RANK and UNRANK are inverse bijections that respect lexicographic order
proves: [correctness, termination]
status: full
---

We use the pseudocode of the page. Let $S_n$ be the permutations of $[n]$, and for $a \in S_n$ let $c_i(a) = |\{j > i : a_j < a_i\}|$ be its Lehmer code. Let $U_i(a) = [n] \setminus \{a_1, \ldots, a_{i-1}\}$ be the set of values not used before position $i$; it has $n - i + 1$ elements and contains $a_i, \ldots, a_n$.

**Lemma 1 (digits).** $c_i(a) = |\{v \in U_i(a) : v < a_i\}|$, and $0 \le c_i(a) \le n - i$.

*Proof.* The values of $U_i(a)$ other than $a_i$ are exactly $a_{i+1}, \ldots, a_n$, the values at the positions after $i$. So the values of $U_i(a)$ below $a_i$ are the values after position $i$ below $a_i$. There are $n - i$ positions after $i$. $\square$

**Lemma 2 (rank formula).** $\operatorname{rank}(a) := |\{b \in S_n : b < a\}| = \sum_{i=1}^{n} c_i(a)\,(n-i)!$, where $<$ is lexicographic order.

*Proof.* For $b < a$, let $i$ be the first position with $b_i \ne a_i$; then $b_i < a_i$. So the set of $b < a$ is the disjoint union over $i$ of the sets $B_i = \{b : b_1 \cdots b_{i-1} = a_1 \cdots a_{i-1},\ b_i < a_i\}$. For $b \in B_i$, the value $b_i$ lies in $U_i(a)$ and is below $a_i$, which leaves $c_i(a)$ choices by Lemma 1, and then $b_{i+1}, \ldots, b_n$ is any order of the other $n - i$ values of $U_i(a)$, which leaves $(n-i)!$ choices. Every such choice is a permutation in $B_i$. So $|B_i| = c_i(a)(n-i)!$. $\square$

**Lemma 3 (the Fenwick tree).** If the tree $T$ represents a 0-1 array $f[1 \ldots n]$, then PREFIX$(T, i)$ returns $f[1] + \cdots + f[i]$ and ADD$(T, i, \delta)$ makes $T$ represent $f$ with $\delta$ added to $f[i]$. This is the lemma proved on the [Fenwick tree](/fenwick-tree/) page: cell $T[j]$ holds $\sum_{j - \operatorname{lowbit}(j) < v \le j} f[v]$. When every $f[v] = 1$, cell $j$ holds $\operatorname{lowbit}(j)$, so lines L1 and L8 build the tree of the all-ones array.

**Lemma 4 (SELECT).** Let $T$ represent a 0-1 array $f$ with $F(p) = f[1] + \cdots + f[p]$, and let $1 \le k_0 \le F(n)$. Then SELECT$(T, k_0)$ returns the least $q$ with $F(q) \ge k_0$, which is the $k_0$-th smallest $v$ with $f[v] = 1$.

*Proof.* Let $2^m$ be the initial value of $s$, the largest power of two with $2^m \le n$. We claim that before each test of line L14 with $s = 2^t$, three facts hold: $p$ is a multiple of $2^{t+1}$ (for $t = m$, $p = 0$), $F(p) < k_0$ and $k = k_0 - F(p)$, and the least $q$ with $F(q) \ge k_0$ satisfies $p < q \le p + 2^{t+1}$, or $p < q \le n$ when $t = m$. Initially $p = 0$, $F(0) = 0 < k_0$, $k = k_0$, and $q \le n < 2^{m+1}$. In a round with $s = 2^t$, since $p$ is a multiple of $2^{t+1}$, $\operatorname{lowbit}(p + s) = s$, so by Lemma 3 the cell $T[p + s]$ holds $F(p + s) - F(p)$ when $p + s \le n$. The test $T[p + s] < k$ is then $F(p + s) < k_0$. If it holds, $q > p + s$, and the new $p' = p + s$ has $F(p') < k_0$ and $k' = k - T[p + s] = k_0 - F(p')$. If it fails, or if $p + s > n$, then $q \le p + s$. In both cases the new $p$ is a multiple of $2^t$ and $p < q \le p + 2^t$ (when $p + s > n$, $q \le n < p + s$). This is the claim for $s = 2^{t-1}$. When the loop ends after the round with $s = 1$, $p < q \le p + 1$, so $q = p + 1$. Since $f$ is 0-1 and $F$ grows by 1 exactly at the values with $f[v] = 1$, the least $q$ with $F(q) \ge k_0$ is the $k_0$-th such value. $\square$

**Theorem 1 (RANK).** For $a \in S_n$, RANK$(a)$ returns $\operatorname{rank}(a)$.

*Proof.* Invariant: before the iteration of line L2 with index $i$, $T$ represents the indicator array of $U_i(a)$, and $r = R_i := \sum_{k < i} c_k(a) \prod_{t=k+1}^{i-1} (n - t + 1)$. Before $i = 1$, line L1 makes $T$ the all-ones tree (Lemma 3), $U_1(a) = [n]$, and $r = 0 = R_1$. In iteration $i$, line L3 sets $c = |\{v \in U_i(a) : v \le a_i - 1\}| = c_i(a)$ by Lemmas 3 and 1. Line L4 removes $a_i$, so $T$ represents $U_{i+1}(a)$. Line L5 sets
$$r = R_i\,(n - i + 1) + c_i(a) = \sum_{k < i} c_k(a) \prod_{t=k+1}^{i} (n - t + 1) + c_i(a) = R_{i+1}.$$
After the last iteration, $r = R_{n+1} = \sum_{k=1}^{n} c_k(a) \prod_{t=k+1}^{n}(n-t+1) = \sum_{k=1}^{n} c_k(a)(n-k)!$, which is $\operatorname{rank}(a)$ by Lemma 2. $\square$

**Theorem 2 (UNRANK).** For $0 \le r < n!$, UNRANK$(r, n)$ returns the $a \in S_n$ with $\operatorname{rank}(a) = r$.

*Proof.* *Digits.* Write $r_0 = r$, and let line L7 process $i = n, n-1, \ldots, 1$, with $\rho$ the value of $r$ before step $i$. At step $i$ it sets $d_i = \rho \bmod (n - i + 1)$ and replaces $\rho$ by $\lfloor \rho/(n-i+1) \rfloor$. By induction on the steps, before step $i$ we have $\rho = \lfloor r / \prod_{t=i+1}^{n} (n-t+1) \rfloor = \lfloor r/(n-i)! \rfloor$, and $r = \rho\,(n-i)! + \sum_{k > i} d_k (n-k)!$ with $0 \le d_k \le n - k$. After step 1, $\rho = \lfloor r / n! \rfloor = 0$, so $r = \sum_{k=1}^{n} d_k (n-k)!$ with $0 \le d_k \le n - k$.

*Items.* Invariant: before the iteration of line L9 with index $i$, $T$ represents the indicator array of $V_i = [n] \setminus \{a_1, \ldots, a_{i-1}\}$, which has $n - i + 1$ elements, and $a_1, \ldots, a_{i-1}$ are distinct. Initially $V_1 = [n]$ by line L8 and Lemma 3. In iteration $i$, $1 \le d_i + 1 \le n - i + 1 = |V_i|$, so by Lemma 4 line L10 sets $a_i$ to the $(d_i + 1)$-th smallest element of $V_i$, which is new. Line L11 removes it, which gives $V_{i+1}$. At the end $a_1, \ldots, a_n$ are $n$ distinct values of $[n]$, so $a \in S_n$, and $U_i(a) = V_i$ for every $i$. By Lemma 1, $c_i(a)$ is the number of elements of $V_i$ below $a_i$, which is $d_i$. By Lemma 2, $\operatorname{rank}(a) = \sum_i d_i (n-i)! = r$. The permutation is unique because $\operatorname{rank}$ is injective: by Lemma 2 it maps $S_n$ into $\{0, \ldots, n! - 1\}$, and $a < b$ implies $\operatorname{rank}(a) < \operatorname{rank}(b)$, since every permutation below $a$ is also below $b$ and $a$ itself is below $b$ but not below $a$. $\square$

**Termination.** The loops of lines L2, L7 and L9 run $n$ times. The loop of PREFIX clears one set bit of $i$ per round, the loop of ADD at least doubles $\operatorname{lowbit}(i)$ per round until $i > n$, and the loop of SELECT halves $s$ until it is 0. So every loop ends, after at most $\lfloor \lg n \rfloor + 1$ rounds for the three tree operations. $\blacksquare$
