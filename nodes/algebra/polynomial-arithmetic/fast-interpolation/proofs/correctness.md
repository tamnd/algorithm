---
title: FAST-INTERPOLATE returns the interpolating polynomial in O(M(n) log n) operations
proves: [correctness]
status: full
---

Let $R$ be a commutative ring with $1$, $n \ge 1$, $u_0, \ldots, u_{n-1} \in R$ with $u_i - u_j$ a unit for all $i \ne j$, and $v_0, \ldots, v_{n-1} \in R$. Let $m = \prod_i (x - u_i)$ and, for a node $(j, k)$ of the subproduct tree, let $S_{j,k}$ be the set of leaves below it, so that $m_{j,k} = \prod_{i \in S_{j,k}} (x - u_i)$. The structure of the tree is Lemma 1 of the proof for [fast multipoint evaluation](/fast-multipoint-evaluation/): the sets of one level partition the leaves, and a node is the product of its children or a copy of its only child.

**Lemma 1 (the derivative at a root).** For each $i$, $m'(u_i) = \prod_{j \ne i} (u_i - u_j)$, which is a unit.

*Proof.* Write $m = (x - u_i) q_i$ with $q_i = \prod_{j \ne i} (x - u_j)$. The product rule for formal derivatives gives $m' = q_i + (x - u_i) q_i'$, so $m'(u_i) = q_i(u_i)$. A product of units is a unit. $\square$

**Lemma 2 (Lagrange's formula).** The polynomial $f = \sum_i c_i\, q_i$ with $c_i = v_i\, m'(u_i)^{-1}$ has degree less than $n$ and satisfies $f(u_i) = v_i$ for all $i$, and it is the only polynomial with these two properties.

*Proof.* Each $q_i$ has degree $n - 1$, so $\deg f < n$. For $j \ne i$, $q_i(u_j) = 0$, because $x - u_j$ is a factor of $q_i$. So $f(u_i) = c_i q_i(u_i) = v_i m'(u_i)^{-1} m'(u_i) = v_i$ by Lemma 1. For uniqueness, let $g$ have the same properties and $d = f - g$. Then $d(u_0) = 0$, so $d = (x - u_0) d_1$ by the factor theorem. Since $d(u_1) = (u_1 - u_0) d_1(u_1) = 0$ and $u_1 - u_0$ is a unit, $d_1(u_1) = 0$. Repeating, $m$ divides $d$. As $m$ is monic of degree $n > \deg d$, $d = 0$. $\square$

**Lemma 3 (the upward pass).** LINEAR-COMBINATION$(c, \text{tree})$ computes, for every node, $r_{j,k} = \sum_{i \in S_{j,k}} c_i\, m_{j,k}/(x - u_i)$, where each quotient $m_{j,k}/(x - u_i)$ is the exact product $\prod_{l \in S_{j,k}, l \ne i} (x - u_l)$.

*Proof.* By induction on $j$. At level $0$, $S_{0,i} = \{i\}$ and $m_{0,i}/(x - u_i) = 1$, so $r_{0,i} = c_i$, which is line C1. Let $j \ge 1$. If node $k$ of level $j$ is a copy of node $2k$ of level $j - 1$, then $S_{j,k} = S_{j-1,2k}$, $m_{j,k} = m_{j-1,2k}$, and line C6 keeps the value, which is correct. Otherwise let $L = S_{j-1,2k}$, $Q = S_{j-1,2k+1}$, $m_L = m_{j-1,2k}$ and $m_Q = m_{j-1,2k+1}$. Then $S_{j,k} = L \cup Q$, disjoint, and $m_{j,k} = m_L m_Q$. For $i \in L$, $m_{j,k}/(x - u_i) = m_Q \cdot m_L/(x - u_i)$, and for $i \in Q$, $m_{j,k}/(x - u_i) = m_L \cdot m_Q/(x - u_i)$. Hence

$$\sum_{i \in L \cup Q} c_i \frac{m_{j,k}}{x - u_i} = m_Q \sum_{i \in L} c_i \frac{m_L}{x - u_i} + m_L \sum_{i \in Q} c_i \frac{m_Q}{x - u_i} = m_Q\, r_{j-1,2k} + m_L\, r_{j-1,2k+1},$$

by the induction hypothesis, which is line C5. $\square$

**Theorem (correctness).** FAST-INTERPOLATE returns the unique $f$ with $\deg f < n$ and $f(u_i) = v_i$ for all $i$.

*Proof.* For $n = 0$ the zero polynomial is the unique polynomial of degree less than $0$, and line L1 returns it. Let $n \ge 1$. Line L3 computes $s_i = m'(u_i)$ for all $i$, by the correctness theorem of fast multipoint evaluation, which applies to any polynomial and any points on the same tree. By Lemma 1 each $s_i$ is a unit, so line L4 computes $c_i = v_i m'(u_i)^{-1}$. By Lemma 3 at the root, line L5 returns $\sum_i c_i\, m/(x - u_i) = \sum_i c_i q_i$, which is the unique interpolant by Lemma 2. $\square$

**Theorem (cost).** Assume that multiplying a polynomial with $a$ coefficients by one with at most $a$ coefficients costs at most $M(a)$ ring operations, that $M(a)/a$ is nondecreasing, and that $M(2a) \le 4M(a)$. Then FAST-INTERPOLATE uses at most $19 M(n) \lceil \log_2 n \rceil + O(n \log n)$ ring operations and $n$ inversions in $R$.

*Proof.* As in the proof for fast multipoint evaluation, $M$ is nondecreasing and superadditive. The tree costs at most $4M(n)$ per level. The derivative $m'$ costs $O(n)$, and since $\deg m' < n$, its evaluation on the tree costs at most $7M(n) + O(n)$ per level, by the cost theorem for fast multipoint evaluation. Line L4 costs $n$ inversions and $n$ multiplications. In the upward pass, a node of level $j$ that is a product of children of degrees $d_1$ and $d_2$, with $D = d_1 + d_2$, does two products in line C5. By Lemma 3, $r_{j-1,2k}$ has degree less than $d_1$ and $m_Q$ has $d_2 + 1$ coefficients, so this product costs at most $M(D + 1)$, and the same holds for the other product. The addition costs $O(D)$. A level has at most $n$ nodes and the degrees sum to $n$, so $\sum (D + 1) \le 2n$ and the level costs at most $2M(2n) + O(n) \le 8M(n) + O(n)$. Adding $4M(n) + 7M(n) + 8M(n) + O(n)$ over $\lceil \log_2 n \rceil$ levels gives the bound. $\blacksquare$
