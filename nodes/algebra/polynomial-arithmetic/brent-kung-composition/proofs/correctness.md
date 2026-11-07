---
title: BRENT-KUNG returns f(g) mod h with at most 2 ceil(sqrt(N)) - 2 products modulo h and one matrix product
proves: [correctness]
status: full
---

Let $R$ be a commutative ring, $h \in R[x]$ of degree $n \ge 1$ with a unit leading coefficient, $g \in R[x]$, and $f = \sum_{t=0}^{N-1} f_t y^t$ with $N \ge 1$. Let $Q = R[x]/(h)$ and let $\pi : R[x] \to Q$ be the quotient map. Division with remainder by $h$ is defined over $R$ because the leading coefficient is a unit, and it gives each class of $Q$ a unique representative of degree less than $n$. We write $\operatorname{rep}(\bar a)$ for it, so $a \bmod h = \operatorname{rep}(\pi(a))$. Let $\bar g = \pi(g)$, $k = \lceil \sqrt{N}\, \rceil$, $m = \lceil N/k \rceil$, and $f_t = 0$ for $t \ge N$.

**Lemma 1 (reduction is a homomorphism).** $\pi$ is a ring homomorphism, $\operatorname{rep}$ is $R$-linear, and $f(g) \bmod h = \operatorname{rep}(f(\bar g))$.

*Proof.* $\pi$ is the quotient map by an ideal, so it is a ring homomorphism, and $\pi(f(g)) = f(\bar g)$. If $a$ and $b$ have degree less than $n$ and $c \in R$, then $a + cb$ has degree less than $n$ and lies in the class $\pi(a) + c\pi(b)$, so by uniqueness $\operatorname{rep}$ is $R$-linear. $\square$

**Lemma 2 (baby steps).** For $1 \le i \le \min(k, N - 1)$, line L3 gives $G_i = \operatorname{rep}(\bar g^{\,i})$, and $G_0 = 1 = \operatorname{rep}(1)$.

*Proof.* $G_1 = g \bmod h = \operatorname{rep}(\bar g)$ by line L2. If $G_{i-1} = \operatorname{rep}(\bar g^{\,i-1})$, then $G_{i-1} G_1 \bmod h = \operatorname{rep}(\pi(G_{i-1} G_1)) = \operatorname{rep}(\bar g^{\,i-1} \bar g)$. Also $\operatorname{rep}(1) = 1$ since $n \ge 1$. $\square$

**Lemma 3 (the matrix product).** Row $j$ of $C = A \cdot B$ is the coefficient vector of $\operatorname{rep}(F_j(\bar g))$, where $F_j = \sum_{i=0}^{k-1} f_{jk+i} y^i$.

*Proof.* The entry of $C$ in row $j$ and column $c$ is $\sum_i A[j][i] B[i][c] = \sum_i f_{jk+i} [x^c] G_i$, so row $j$ is the coefficient vector of $\sum_i f_{jk+i} G_i$. A row $i$ of $B$ with $i > N - 1$ is zero, and it meets only $f_{jk+i}$ with $jk + i \ge i \ge N$, which is $0$, so those terms vanish. For the other $i$, $G_i = \operatorname{rep}(\bar g^{\,i})$ by Lemma 2. By the linearity in Lemma 1, $\sum_i f_{jk+i} \operatorname{rep}(\bar g^{\,i}) = \operatorname{rep}(F_j(\bar g))$. $\square$

**Theorem (correctness).** BRENT-KUNG returns $f(g) \bmod h$.

*Proof.* Each $t < mk$ has a unique form $t = jk + i$ with $0 \le i < k$ and $0 \le j < m$, and $N \le mk$. Since $Q$ is commutative, $f(\bar g) = \sum_t f_t \bar g^{\,t} = \sum_j F_j(\bar g)\, (\bar g^{\,k})^j$. If $m \ge 2$, then $N > k$, so $k \le N - 1$ and $G_k = \operatorname{rep}(\bar g^{\,k})$ by Lemma 2. Let $C_j = \operatorname{rep}(F_j(\bar g))$ be row $j$ of $C$ (Lemma 3). We claim that after line L9 for index $j$, and after line L7 for $j = m - 1$, $S = \operatorname{rep}\big(\sum_{t=j}^{m-1} F_t(\bar g)\, (\bar g^{\,k})^{t-j}\big)$. Line L7 gives it for $j = m - 1$. If it holds for $j + 1$, then $S \cdot G_k \bmod h = \operatorname{rep}\big(\sum_{t=j+1}^{m-1} F_t(\bar g) (\bar g^{\,k})^{t-j}\big)$ by Lemma 1, and adding $C_j$ adds $\operatorname{rep}(F_j(\bar g))$, by linearity of $\operatorname{rep}$. At $j = 0$ this is $\operatorname{rep}(f(\bar g)) = f(g) \bmod h$ by Lemma 1. If $m = 1$, the loop does not run and $S = C_0 = \operatorname{rep}(f(\bar g))$. $\square$

**Theorem (cost).** Assume $M(a)/a$ is nondecreasing and $N \le n$, $\deg g < n$. The algorithm does at most $2k - 2$ products modulo $h$, each costing at most $3M(n) + O(n)$ ring operations after a one-time cost of $O(M(n))$ for the inverse of the reversal of $h$. Line L6 costs at most $m k n \le k^2 n$ ring multiplications and as many additions by the schoolbook method, and $O(n^{(\omega + 1)/2})$ with an $O(r^\omega)$ matrix multiplication. So the total is $O(\sqrt{n}\, M(n) + n^{(\omega+1)/2})$.

*Proof.* *Count.* Line L3 runs $\min(k, N - 1) - 1$ times and line L9 runs $m - 1$ times. From $(k - 1)^2 < N \le k^2$ we get $m = \lceil N/k \rceil \le k$, so the total is at most $(k - 1) + (k - 1) = 2k - 2$.

*One product modulo $h$.* Both factors have degree less than $n$, so their product costs at most $M(n)$ and has degree at most $2n - 2$. Fast division of it by $h$ has a quotient with at most $n - 1$ coefficients. With the inverse of the reversal of $h$ to precision $n$ stored, by the cost theorem for fast polynomial division it costs at most $M(n - 1) + M(n) + O(n) \le 2M(n) + O(n)$. The stored inverse costs $O(M(n))$ once, by Newton iteration.

*Matrix product.* Pad $A$ to a $k \times k$ matrix with zero rows and $B$ to a $k \times k\lceil n/k \rceil$ matrix with zero columns. Then $A \cdot B$ is $\lceil n/k \rceil$ products of $k \times k$ matrices. With $k \le \sqrt{n} + 1$, this costs $O((n/k + 1) k^\omega) = O(n^{(\omega+1)/2})$. The schoolbook bound $m k n$ counts one multiplication per triple (row, inner index, column).

*Rest.* Lines L4, L5 and L7 and the additions of line L9 cost $O(mn) = O(n^{3/2})$, which is within $O(\sqrt{n}\, M(n))$ since $M(n) \ge n$. Adding up gives the bound. $\blacksquare$
