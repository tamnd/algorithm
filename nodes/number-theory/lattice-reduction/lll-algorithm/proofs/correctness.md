---
title: The LLL algorithm returns a delta-LLL-reduced basis of the same lattice after O(n^2 log X) swaps
proves: [correctness, termination, time.worst]
status: full
---

**Setting.** The input is a list of linearly independent rows $b_1, \ldots, b_n \in \mathbb{Q}^m$ and a rational $\delta$ with $1/4 < \delta < 1$. We write $b_i^*$ for the Gram-Schmidt vectors of the current rows, $B_i = \|b_i^*\|^2$, $\mu_{ij} = \langle b_i, b_j^* \rangle / B_j$ for $j < i$, so that $b_i = b_i^* + \sum_{j < i} \mu_{ij} b_j^*$, and $\pi_i$ for the orthogonal projection onto $\operatorname{span}(b_1, \ldots, b_{i-1})^\perp$. The nearest integer $\lceil x \rfloor = \lfloor x + 1/2 \rfloor$ satisfies $|x - \lceil x \rfloor| \le 1/2$. The line numbers refer to the `main` block of the page.

**Lemma 1 (the rows stay a basis of $L$).** At every moment the current rows are a basis of the input lattice $L$.

*Proof.* REDUCE replaces $b_k$ by $b_k - q b_j$ with $q \in \mathbb{Z}$ and $j \ne k$, and line L6 exchanges two rows. Both are multiplications on the left by an integer matrix of determinant $\pm 1$, whose inverse is again an integer matrix. So the new rows generate the same lattice, and they are still independent. $\square$

**Lemma 2 (REDUCE keeps the data correct).** After REDUCE$(k, j)$, $j < k$, the $b_i^*$ and $B_i$ are unchanged, the stored $\mu$ equal the Gram-Schmidt coefficients of the new rows, and $|\mu_{kj}| \le 1/2$.

*Proof.* The change $-q b_j$ lies in $\operatorname{span}(b_1, \ldots, b_{k-1})$, so $\pi_k(b_k)$, which is $b_k^*$, does not change; no other row changes. Using $b_j = b_j^* + \sum_{i < j} \mu_{ji} b_i^*$, the new $b_k$ is $b_k^* + \sum_{i < k} \mu_{ki}' b_i^*$ with $\mu_{ki}' = \mu_{ki} - q \mu_{ji}$ for $i < j$, $\mu_{kj}' = \mu_{kj} - q$, and $\mu_{ki}' = \mu_{ki}$ for $j < i < k$. These are the updates of REDUCE, and $|\mu_{kj} - \lceil \mu_{kj} \rfloor| \le 1/2$. Rows $i \ne k$ of $\mu$ are coefficients of other rows on the unchanged $b_i^*$, so they do not change. $\square$

**Lemma 3 (the swap formulas).** Let $c$ be the rows after line L6, so $c_{k-1} = b_k$, $c_k = b_{k-1}$ and $c_i = b_i$ otherwise. Let $\mu = \mu_{k,k-1}$ and $B = B_k + \mu^2 B_{k-1}$. Then $c_i^* = b_i^*$ for $i \ne k - 1, k$, and

$$\|c_{k-1}^*\|^2 = B, \quad \nu := \mu^c_{k,k-1} = \frac{\mu B_{k-1}}{B}, \quad \|c_k^*\|^2 = \frac{B_{k-1} B_k}{B},$$

$\mu^c_{k-1,j} = \mu_{k,j}$ and $\mu^c_{k,j} = \mu_{k-1,j}$ for $j < k - 1$, and for $i > k$, $\mu^c_{i,k} = \mu_{i,k-1} - \mu \mu_{i,k}$ and $\mu^c_{i,k-1} = \mu_{i,k} + \nu \mu^c_{i,k}$.

*Proof.* For $i < k - 1$ nothing changes. For $i > k$, the span of the first $i - 1$ rows is the same set, so $c_i^* = b_i^*$; the same holds for the span $V$ of the first $k$ rows, so $\{c_{k-1}^*, c_k^*\}$ and $\{b_{k-1}^*, b_k^*\}$ are orthogonal bases of the same plane $V \cap \operatorname{span}(b_1, \ldots, b_{k-2})^\perp$.

Since $c_{k-1} = b_k = b_k^* + \mu b_{k-1}^* + (\text{a vector of } \operatorname{span}(b_1, \ldots, b_{k-2}))$, its projection is $c_{k-1}^* = b_k^* + \mu b_{k-1}^*$, of squared length $B_k + \mu^2 B_{k-1} = B$, as $b_k^* \perp b_{k-1}^*$. Next, $c_k = b_{k-1}$ projects to $b_{k-1}^*$ orthogonally to $\operatorname{span}(b_1, \ldots, b_{k-2})$, and then $c_k^* = b_{k-1}^* - \nu c_{k-1}^*$ with $\nu = \langle b_{k-1}^*, c_{k-1}^* \rangle / B = \mu B_{k-1} / B$. The first $k$ rows generate a lattice whose Gram determinant $\prod_{i \le k} B_i$ does not depend on the order of the rows, so $B \cdot \|c_k^*\|^2 = B_{k-1} B_k$. For $j < k - 1$, $\mu^c_{k-1,j} = \langle b_k, b_j^* \rangle / B_j = \mu_{k,j}$, and likewise $\mu^c_{k,j} = \mu_{k-1,j}$.

For $i > k$, $b_i$ has the component $\mu_{i,k-1} b_{k-1}^* + \mu_{i,k} b_k^*$ in the plane. From $c_{k-1}^* = b_k^* + \mu b_{k-1}^*$ and $c_k^* = b_{k-1}^* - \nu c_{k-1}^*$ we get $b_{k-1}^* = c_k^* + \nu c_{k-1}^*$ and $b_k^* = (1 - \mu \nu) c_{k-1}^* - \mu c_k^*$. Substituting,

$$\mu_{i,k-1} b_{k-1}^* + \mu_{i,k} b_k^* = \big(\mu_{i,k} + \nu (\mu_{i,k-1} - \mu \mu_{i,k})\big) c_{k-1}^* + (\mu_{i,k-1} - \mu \mu_{i,k}) c_k^*,$$

which gives the two formulas. $\square$

By Lemmas 2 and 3 and the correctness of the Gram-Schmidt step of line L1, the stored $B$ and $\mu$ are always the Gram-Schmidt data of the current rows.

**Lemma 4 (loop invariant).** Each time line L3 is reached, $2 \le k \le n + 1$, and $b_1, \ldots, b_{k-1}$ satisfy the two conditions of a $\delta$-LLL-reduced basis among themselves: $|\mu_{ij}| \le 1/2$ for $j < i \le k - 1$, and $\delta B_{i-1} \le B_i + \mu_{i,i-1}^2 B_{i-1}$ for $2 \le i \le k - 1$.

*Proof.* At the first visit $k = 2$ and the conditions are empty. Assume the invariant at some visit with $k \le n$.

*Case of a swap.* Line L4 changes only $b_k$ and row $k$ of $\mu$. The swap changes rows $k - 1$ and $k$ and the coefficients in rows $\ge k - 1$, and leaves $b_1, \ldots, b_{k-2}$, their $\mu_{ij}$ and their $B_i$ unchanged (Lemma 3). The new value $k' = \max(2, k - 1)$ needs the conditions for the first $k' - 1 \le k - 2$ rows, which held before.

*Case of a pass.* By Lemma 2, after line L4 and the loop of line L9 (which runs $j = k - 2, \ldots, 1$ in that order), $|\mu_{kj}| \le 1/2$ for all $j < k$: each REDUCE$(k, j)$ fixes $\mu_{kj}$ and later calls, with smaller $j$, change only $\mu_{ki}$ with $i < j$. REDUCE does not change any $B_i$, nor $\mu_{k,k-1}$ when $j < k - 1$, so the Lovász condition at $k$, checked at line L5, still holds. Rows $1, \ldots, k - 1$ are unchanged. So the invariant holds for $k + 1$. $\square$

**Theorem 1 (correctness).** If the algorithm stops, it returns a $\delta$-LLL-reduced basis of $L$.

*Proof.* It stops when line L3 sees $k = n + 1$. By Lemma 4 all $n$ rows are then reduced, and by Lemma 1 they are a basis of $L$. $\square$

**Lemma 5 (the potential).** Let $d_i = \prod_{j \le i} B_j$ for $0 \le i \le n$ and $D = \prod_{i=1}^{n-1} d_i$. Then REDUCE does not change $D$, and a swap multiplies $D$ by a factor less than $\delta$. If the input rows are integer vectors, every $d_i$ is a positive integer at all times.

*Proof.* REDUCE does not change any $B_j$ (Lemma 2). A swap at $k$ replaces $B_{k-1}, B_k$ by $B, B_{k-1} B_k / B$, so $d_i$ is unchanged for $i \ne k - 1$, and $d_{k-1}$ is multiplied by $B / B_{k-1}$. The swap is done only when $B = B_k + \mu^2 B_{k-1} < \delta B_{k-1}$. Finally, $d_i$ is the Gram determinant $\det(G_i)$, $G_i = (\langle b_s, b_t \rangle)_{s,t \le i}$, of the first $i$ rows; it is positive since they are independent, and an integer when the rows are integer vectors. $\square$

**Theorem 2 (termination and number of swaps).** Let the input be an integer basis with $\|b_i\|^2 \le X$ for all $i$, $X \ge 2$. The number $s$ of swaps satisfies $s \le \log_{1/\delta} D_0 \le \frac{n (n - 1)}{2} \log_{1/\delta} X$, where $D_0$ is the value of $D$ for the input, and the loop runs at most $n - 1 + 2s$ times. For a rational input the algorithm also stops.

*Proof.* By Lemma 5, after $s$ swaps $1 \le D \le \delta^s D_0$, so $s \le \log_{1/\delta} D_0$. At the input, $B_j = \|b_j^*\|^2 \le \|b_j\|^2 \le X$, so $d_i \le X^i$ and $D_0 \le X^{1 + 2 + \cdots + (n - 1)} = X^{n(n-1)/2}$. Each loop iteration is a pass, which adds 1 to $k$, or a swap, which subtracts at most 1. $k$ goes from 2 to $n + 1$, so the number $p$ of passes satisfies $p - s \le n - 1$, that is $p \le n - 1 + s$, and the number of iterations is $p + s \le n - 1 + 2s$.

For a rational input, let $c$ be a positive integer such that $c b_i \in \mathbb{Z}^m$ for all $i$. On the rows $c b_i$, the $\mu_{ij}$ are the same and the $B_i$ are multiplied by $c^2$, so every rounding of REDUCE and every test of line L5, which is homogeneous in the $B_i$, gives the same result. So the run on $b$ is the run on $c b$ divided by $c$, and it stops. $\square$

**Theorem 3 (arithmetic cost).** For an integer basis with $\|b_i\|^2 \le X$, $m \ge n$ and fixed $\delta$, the algorithm uses $O(n^2 m + n^3 m \log X)$ arithmetic operations, and $O(n^2 m)$ if the input is already $\delta$-LLL-reduced.

*Proof.* Line L1 is Gram-Schmidt with $O(n^2 m)$ operations. One REDUCE costs $O(m + n)$: $m$ for the row and at most $n$ for the coefficients. Lines L4 to L7 cost $O(m + n)$, since the swap formulas touch $O(n)$ coefficients. Line L9 does at most $n$ REDUCE calls, $O(n (m + n)) = O(n m)$. By Theorem 2 there are $O(n + s)$ iterations with $s = O(n^2 \log X)$, so the total is $O(n^2 m + (n + n^2 \log X) n m) = O(n^3 m \log X)$ for $X \ge 2$. If the input is reduced, no test of line L5 fails: a REDUCE$(k, k - 1)$ on $|\mu_{k,k-1}| \le 1/2$ finds $q = 0$, or $q = 1$ when $\mu_{k,k-1} = 1/2$ exactly, and then the new value is $-1/2$; in both cases $\mu_{k,k-1}^2$ and all $B_i$ are unchanged, so the Lovász condition at $k$ still holds. So $s = 0$ and the cost is $O(n^2 m)$. $\blacksquare$

The bound on the sizes of the numbers, $O(n \log X)$ binary digits for the integers $d_i$, $d_j \mu_{ij}$ and the entries of the rows, is proved in Section 1 of Lenstra, Lenstra and Lovász (1982); it turns Theorem 3 into the bit bound on the page.
