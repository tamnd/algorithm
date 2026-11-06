---
title: The nearest plane method returns a lattice vector whose error has Gram-Schmidt coordinates at most one half, decodes within half the shortest Gram-Schmidt vector, and approximates CVP within 2^(n/2) on LLL-reduced bases
proves: [correctness, termination, time.worst]
status: full
---

**Setting.** The input is $n \ge 1$ linearly independent rows $b_1, \ldots, b_n \in \mathbb{Q}^m$ and a target $t \in \mathbb{Q}^m$. We write $L$ for the lattice they generate, $b_1^*, \ldots, b_n^*$ for the Gram-Schmidt vectors, $N_i = \|b_i^*\|^2 > 0$, and $\mu_{ij} = \langle b_i, b_j^* \rangle / N_j$. Then $b_i = b_i^* + \sum_{j < i} \mu_{ij} b_j^*$, so $\langle b_i, b_j^* \rangle = 0$ for $i < j$ and $\langle b_i, b_i^* \rangle = N_i$. The nearest integer is $\lceil z \rfloor = \lfloor z + 1/2 \rfloor$, so $-1/2 \le z - \lceil z \rfloor < 1/2$. Indices in the loop at line L3 run $i = n, n - 1, \ldots, 1$; $w^{(i)}$ denotes the value of $w$ after the iteration for $i$, and $w^{(n+1)} = t$.

**Lemma 1 (invariant).** For every $i$, $w^{(i)} = t - \sum_{j \ge i} x_j b_j$ with integers $x_j$. Hence the output $v = t - w^{(1)} = \sum_j x_j b_j$ lies in $L$, with coefficients $x$.

*Proof.* Line L2 sets $w = t$, and each pass of line L5 subtracts $x_i b_i$ with the integer $x_i$ of line L4. $\square$

**Lemma 2 (the error).** Write $t - v = o + \sum_{i=1}^n c_i b_i^*$ with $o$ orthogonal to $\operatorname{span}(L)$. Then $-1/2 \le c_i < 1/2$ for every $i$. In particular $\|t - v\|^2 \le \|o\|^2 + \tfrac14 \sum_i N_i$.

*Proof.* Fix $i$. Line L4 sets $x_i = \lceil \langle w^{(i+1)}, b_i^* \rangle / N_i \rfloor$, and line L5 gives $\langle w^{(i)}, b_i^* \rangle / N_i = \langle w^{(i+1)}, b_i^* \rangle / N_i - x_i$, which lies in $[-1/2, 1/2)$. The later iterations subtract multiples of $b_j$ with $j < i$, and $\langle b_j, b_i^* \rangle = 0$, so $\langle w^{(1)}, b_i^* \rangle = \langle w^{(i)}, b_i^* \rangle$. Since $w^{(1)} = t - v$ and the $b_k^*$ are orthogonal, $c_i = \langle t - v, b_i^* \rangle / N_i \in [-1/2, 1/2)$. The bound follows from Pythagoras. $\square$

**Lemma 3 (the first wrong coefficient).** Let $u = \sum_i z_i b_i$ be any lattice vector and $e = t - u$. If $x \ne z$, let $k$ be the largest index with $x_k \ne z_k$. Then $\|e\| \ge \tfrac12 \|b_k^*\|$.

*Proof.* For $j > k$, $x_j = z_j$, so $w^{(k+1)} = t - \sum_{j > k} z_j b_j = e + \sum_{j \le k} z_j b_j$. Taking the inner product with $b_k^*$ and dividing by $N_k$ gives $z_k + \varepsilon$ with $\varepsilon = \langle e, b_k^* \rangle / N_k$, because $\langle b_j, b_k^* \rangle = 0$ for $j < k$. Line L4 rounds $z_k + \varepsilon$ to $z_k + \lceil \varepsilon \rfloor$, and this differs from $z_k$, so $\lceil \varepsilon \rfloor \ne 0$ and $|\varepsilon| \ge 1/2$. By Cauchy-Schwarz $\|e\| \ge |\langle e, b_k^* \rangle| / \|b_k^*\| = |\varepsilon| \|b_k^*\| \ge \tfrac12 \|b_k^*\|$. $\square$

**Lemma 4 (decoding).** If some $u \in L$ satisfies $\|t - u\| < \tfrac12 \min_i \|b_i^*\|$, then $v = u$.

*Proof.* Otherwise Lemma 3 gives an index $k$ with $\|t - u\| \ge \tfrac12 \|b_k^*\| \ge \tfrac12 \min_i \|b_i^*\|$. $\square$

**Lemma 5 (approximation).** Let $u$ be a closest lattice vector to $t$. Then

$$\|t - v\|^2 \le \Big(1 + \max_{1 \le k \le n} \sum_{i \le k} \frac{N_i}{N_k}\Big) \|t - u\|^2.$$

*Proof.* If $v = u$ there is nothing to prove. Otherwise let $k$ be as in Lemma 3, $e = t - u$. The difference $v - u = \sum_{j \le k} (x_j - z_j) b_j$ lies in $\operatorname{span}(b_1, \ldots, b_k) = \operatorname{span}(b_1^*, \ldots, b_k^*)$. So $t - v$ and $e$ have the same component $o$ orthogonal to $\operatorname{span}(L)$ and the same coordinates along $b_i^*$ for $i > k$. With Lemma 2 for the coordinates $i \le k$,

$$\|t - v\|^2 = \|o\|^2 + \sum_{i > k} \frac{\langle e, b_i^* \rangle^2}{N_i} + \sum_{i \le k} c_i^2 N_i \le \|e\|^2 + \frac14 \sum_{i \le k} N_i.$$

Lemma 3 gives $\tfrac14 N_k \le \|e\|^2$, so $\tfrac14 \sum_{i \le k} N_i \le \|e\|^2 \sum_{i \le k} N_i / N_k$, and the claim follows. $\square$

**Corollary (LLL-reduced bases).** If the basis is LLL-reduced with parameter $\delta \in (1/4, 1]$ and $\alpha = 1/(\delta - 1/4)$, then $\|t - v\|^2 \le \big(1 + \frac{\alpha^n - 1}{\alpha - 1}\big) \operatorname{dist}(t, L)^2$. For $\delta = 3/4$, $\alpha = 2$ and $\|t - v\| \le 2^{n/2} \operatorname{dist}(t, L)$.

*Proof.* The Lovász condition and $|\mu_{i+1,i}| \le 1/2$ give $N_{i+1} \ge (\delta - \mu_{i+1,i}^2) N_i \ge N_i / \alpha$, so $N_i \le \alpha^{k - i} N_k$ for $i \le k$. Then $\sum_{i \le k} N_i / N_k \le \sum_{j=0}^{k-1} \alpha^j = (\alpha^k - 1)/(\alpha - 1)$, which is largest at $k = n$. Insert this into Lemma 5. For $\alpha = 2$ the factor is $1 + 2^n - 1 = 2^n$. $\square$

**Termination and cost.** Line L1 computes Gram-Schmidt in $O(n^2 m)$ arithmetic operations. The loop at line L3 runs $n$ times; line L4 is one inner product, $O(m)$, and line L5 is $O(m)$, so the loop costs $O(n m)$. The total is $O(n^2 m)$ arithmetic operations, and the algorithm terminates.

**Theorem.** On every valid input the algorithm returns $x \in \mathbb{Z}^n$ and $v = x B \in L$ (Lemma 1) such that the Gram-Schmidt coordinates of $t - v$ lie in $[-1/2, 1/2)$ (Lemma 2). It returns a closest vector whenever $\operatorname{dist}(t, L) < \tfrac12 \min_i \|b_i^*\|$ (Lemma 4), it is within the factor of Lemma 5 of the optimum on every basis and within $2^{n/2}$ on bases that are LLL-reduced with $\delta = 3/4$, and it uses $O(n^2 m)$ arithmetic operations. $\blacksquare$
