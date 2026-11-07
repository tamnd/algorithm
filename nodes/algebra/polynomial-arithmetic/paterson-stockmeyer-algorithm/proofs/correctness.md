---
title: PATERSON-STOCKMEYER returns f(X) with at most 2 ceil(sqrt(n + 1)) - 2 nonscalar multiplications
proves: [correctness]
status: full
---

Let $R$ be a commutative ring, $A$ an associative $R$-algebra with unit $1_A$, $X \in A$, and $a = [a_0, \ldots, a_n]$ with $n \ge 0$ and $f = \sum_{i=0}^{n} a_i x^i$. Fix a block size $k \ge 1$, let $m = \lceil (n+1)/k \rceil$, and set $a_t = 0$ for $t > n$. Let $R[X] \subseteq A$ be the set of elements $g(X)$ for $g \in R[x]$.

**Lemma 1 (polynomials in $X$ commute).** $R[X]$ is a commutative subring of $A$, and evaluation $g \mapsto g(X)$ is a ring homomorphism from $R[x]$ onto $R[X]$.

*Proof.* Since $A$ is an $R$-algebra, $(c P)(c' Q) = (c c')(P Q)$ for $c, c' \in R$ and $P, Q \in A$, and $X^i X^j = X^{i+j} = X^j X^i$ by associativity. Expanding by distributivity, $g(X) h(X) = (gh)(X) = (hg)(X) = h(X) g(X)$, and $g(X) + h(X) = (g + h)(X)$. $\square$

**Lemma 2 (block decomposition).** With $B_j = \sum_{i=0}^{k-1} a_{jk+i} X^i$, we have $f(X) = \sum_{j=0}^{m-1} B_j (X^k)^j$.

*Proof.* Division with remainder by $k$ maps each $t \in \{0, \ldots, mk - 1\}$ to a unique pair $(j, i)$ with $t = jk + i$, $0 \le j < m$ and $0 \le i < k$. Since $n < mk$, the coefficients $a_0, \ldots, a_n$ all occur, and the other terms are zero. By Lemma 1, $X^i (X^k)^j = X^{jk+i}$, so $\sum_j B_j (X^k)^j = \sum_{t < mk} a_t X^t = f(X)$. $\square$

**Theorem (correctness).** PATERSON-STOCKMEYER returns $f(X)$, for every block size $k \ge 1$.

*Proof.* *Lines L2 and L3.* By induction on $i$, $P_i = X^i$ for $0 \le i \le \min(k, n)$, with $P_0 = 1_A = X^0$. If $m \ge 2$, then $k < n + 1$, so $\min(k, n) = k$ and $P_k = X^k$ exists. In line L4 a term with $jk + i \le n$ has $i \le n$ and $i < k$, so $P_i$ is defined. The left-out terms have $a_{jk+i} = 0$. So line L4 computes the $B_j$ of Lemma 2.

*Lines L5 to L7.* We show that after line L7 runs for index $j$, and after line L5 for $j = m - 1$, the value is $S = \sum_{t=j}^{m-1} B_t (X^k)^{t-j}$. For $j = m - 1$, line L5 sets $S = B_{m-1}$. If the claim holds for $j + 1$, then line L7 gives $S \cdot X^k + B_j = \sum_{t=j+1}^{m-1} B_t (X^k)^{t-j-1} X^k + B_j = \sum_{t=j}^{m-1} B_t (X^k)^{t-j}$, using Lemma 1 to move $X^k$ past the powers of $X^k$. For $j = 0$ this is $f(X)$ by Lemma 2, which line L8 returns. For $m = 1$ the loop does not run and $S = B_0 = f(X)$. $\square$

**Theorem (cost).** For $n \ge 1$ the algorithm does $\min(k, n) - 1 + m - 1$ nonscalar multiplications, $n + 1$ scalar multiplications and $n$ additions. With $k = \lceil \sqrt{n+1}\, \rceil$, the number of nonscalar multiplications is at most $2k - 2 \le 2\sqrt{n+1}$.

*Proof.* Line L3 does one nonscalar product for each $i$ from $2$ to $\min(k, n)$, and line L7 does one for each $j$ from $m - 2$ down to $0$. No other line multiplies two elements of $A$: line L4 multiplies the power $P_i$ by the scalar $a_{jk+i}$. Line L4 does one scalar product for each $t = jk + i \le n$, so $n + 1$ in all. The additions of lines L4 and L7 each join two partial sums of the final expression $\sum_t a_t X^t$, which has $n + 1$ terms, so there are $n$ of them. For the bound, $(k - 1)^2 < n + 1 \le k^2$ by the choice of $k$, so $(n+1)/k \le k$ and $m \le k$. Hence $\min(k, n) - 1 + m - 1 \le 2k - 2$. Finally $k < \sqrt{n+1} + 1$, so $2k - 2 < 2\sqrt{n+1}$. $\blacksquare$
