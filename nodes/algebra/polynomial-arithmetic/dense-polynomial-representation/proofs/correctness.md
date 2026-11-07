---
title: The operations on dense coefficient lists are exact and keep the lists normalized
proves: [correctness]
status: full
---

Let $R$ be a commutative ring with $1$. For a list $a = [a_0, \ldots, a_{n-1}]$ of elements of $R$ we write $|a| = n$ and $\operatorname{val}(a) = \sum_{i<n} a_i x^i$, and we set $a_i = 0$ for $i \ge n$. A list is *normalized* when it is empty or its last entry is nonzero.

**Lemma 0 (uniqueness).** For each $f \in R[x]$ there is exactly one normalized list $a$ with $\operatorname{val}(a) = f$, and then $|a| - 1 = \deg f$ (with $-1$ for $f = 0$).

*Proof.* Two lists with the same value have the same entries at each position below the shorter length, and the longer one has only zero entries above it, because the coefficients of a polynomial are unique. If both lists are normalized, the longer one would end in a zero entry, unless the lengths are equal. So the lists are equal. The list of the coefficients of $x^0, \ldots, x^{\deg f}$ is normalized and has the value $f$. $\square$

**Lemma 1 (NORMALIZE).** NORMALIZE$(c)$ returns a normalized list with the same value as $c$.

*Proof.* The loop of lines L1 and L2 removes only last entries that are zero, and removing a top zero entry does not change $\sum c_i x^i$. It stops when the list is empty or its last entry is nonzero, which is the definition of normalized. It stops after at most $|c|$ steps, since each step shortens the list. $\square$

**Lemma 2 (ADD).** For normalized $a$ and $b$, ADD$(a, b)$ returns the normalized list of $\operatorname{val}(a) + \operatorname{val}(b)$.

*Proof.* Let $N = \max(|a|, |b|)$. After line L6 has run for $i = 0, \ldots, N - 1$, $c_i = a_i + b_i$ for each $i < N$, with the convention $a_i = 0$ for $i \ge |a|$. Both operands have no terms of degree $N$ or more, so $\operatorname{val}(c) = \sum_{i<N} (a_i + b_i) x^i = \operatorname{val}(a) + \operatorname{val}(b)$. Line L7 and Lemma 1 finish the proof. $\square$

**Lemma 3 (MUL).** For normalized $a$ and $b$, MUL$(a, b)$ returns the normalized list of $\operatorname{val}(a) \operatorname{val}(b)$.

*Proof.* If $|a| = 0$ or $|b| = 0$, one factor is the zero polynomial, the product is zero, and line L8 returns the empty list. Otherwise let $m = |a|$, $n = |b|$. We show the invariant

> **(M)** before row $i$ of the loop of line L10, $c_k = \sum_{i' < i,\ 0 \le k - i' < n} a_{i'} b_{k - i'}$ for each $0 \le k \le m + n - 2$.

*Initialization.* For $i = 0$ the sum is empty, and line L9 sets every $c_k$ to $0$.

*Maintenance.* Row $i$ runs line L12 for $j = 0, \ldots, n - 1$ and adds $a_i b_j$ to $c_{i+j}$. Each index $k$ gets the term with $i' = i$ and $k - i' = j$ exactly when $0 \le k - i < n$, which is the new term of (M) for $i + 1$. The index $i + j \le (m - 1) + (n - 1)$ is in range.

*Termination.* After row $m - 1$, (M) with $i = m$ gives $c_k = \sum_{i + j = k} a_i b_j$, the coefficient of $x^k$ in the product. Every pair $(i, j)$ with $i < m$, $j < n$ has $i + j \le m + n - 2$, so no term of the product is lost. So $\operatorname{val}(c) = \operatorname{val}(a)\operatorname{val}(b)$, and Lemma 1 gives a normalized result. $\square$

**Lemma 4 (EVALUATE).** EVALUATE$(a, u)$ returns $\operatorname{val}(a)(u) = \sum_{j<m} a_j u^j$.

*Proof.* Let $m = |a|$. We show that at the test of line L15 for the index $i$ (counting down from $m - 1$ to $-1$), $s = \sum_{j=i+1}^{m-1} a_j u^{j - i - 1}$. For $i = m - 1$ the sum is empty and line L14 sets $s = 0$. If it holds for $i$, then line L16 sets $s \cdot u + a_i = \sum_{j=i+1}^{m-1} a_j u^{j-i} + a_i = \sum_{j=i}^{m-1} a_j u^{j-i}$, which is the claim for $i - 1$. When the loop ends, $i = -1$, and $s = \sum_{j=0}^{m-1} a_j u^j$. This uses that $R$ is commutative only through the identity $(\sum c_j u^j) u = \sum c_j u^{j+1}$, which holds in every associative ring. $\square$

**Lemma 5 (DIVMOD).** Let $a$ and $b$ be normalized, $n = |b| \ge 1$, and let $b_{n-1}$ be a unit of $R$. Then DIVMOD$(a, b)$ returns normalized lists $q$ and $r$ with $\operatorname{val}(a) = \operatorname{val}(q)\operatorname{val}(b) + \operatorname{val}(r)$ and $|r| \le n - 1$, that is $\deg r < \deg b$. These $q$ and $r$ are the only polynomials with these properties.

*Proof.* Let $m = |a|$. If $m < n$, the loop of line L20 does not run, $q$ is empty, $r = a$ has at most $n - 1$ entries, and $\operatorname{val}(a) = 0 \cdot \operatorname{val}(b) + \operatorname{val}(a)$. Let $m \ge n$. Write $Q_k = \sum_{j > k} q_j x^j$ for the part of the quotient that is set before step $k$ (so $Q_{m-n}$ is $0$). We show the invariant

> **(D)** before step $k$ of the loop of line L20, $\operatorname{val}(a) = Q_k \operatorname{val}(b) + \operatorname{val}(r)$ and $r_j = 0$ for each $j \ge k + n$.

*Initialization.* For $k = m - n$, line L18 sets $r = a$ and $Q_k = 0$, and $r_j = 0$ for $j \ge m$ because $|r| = m$.

*Maintenance.* Step $k$ sets $t = r_{k+n-1} v$ (line L21), stores $q_k = t$ (line L22), and subtracts $t\, x^k \operatorname{val}(b)$ from $\operatorname{val}(r)$ in lines L23 and L24: the entry $r_{k+j}$ loses $t b_j$ for $j = 0, \ldots, n - 1$. Then $Q_{k-1} = Q_k + t x^k$, and

$$Q_{k-1}\operatorname{val}(b) + \operatorname{val}(r_{\text{new}}) = Q_k \operatorname{val}(b) + t x^k \operatorname{val}(b) + \operatorname{val}(r_{\text{old}}) - t x^k \operatorname{val}(b) = \operatorname{val}(a).$$

The entry at $k + n - 1$ becomes $r_{k+n-1} - t\, b_{n-1} = r_{k+n-1} - r_{k+n-1} v\, b_{n-1} = 0$, since $v b_{n-1} = 1$. The entries at $j \ge k + n$ are not touched and stay zero. So $r_j = 0$ for $j \ge (k - 1) + n$, which is (D) for $k - 1$.

*Termination.* After step $k = 0$, (D) holds with $Q_{-1} = \operatorname{val}(q)$ and $r_j = 0$ for $j \ge n - 1$. So $\operatorname{val}(r) = \operatorname{val}(r_0, \ldots, r_{n-2})$, which is what line L25 keeps, and $\operatorname{val}(a) = \operatorname{val}(q)\operatorname{val}(b) + \operatorname{val}(r[0..n-2])$. Lemma 1 normalizes both lists without a change of value, and the remainder list has at most $n - 1$ entries.

*Uniqueness.* Suppose $\operatorname{val}(a) = q b + r = q' b + r'$ with $\deg r, \deg r' < \deg b = n - 1$. Then $(q - q') b = r' - r$. If $q \ne q'$, the top coefficient of $(q - q') b$ is $\operatorname{lc}(q - q') b_{n-1}$, which is nonzero because $b_{n-1}$ is a unit (if $c\, b_{n-1} = 0$ then $c = c\, b_{n-1} v = 0$). So $\deg((q - q') b) \ge n - 1 > \deg(r' - r)$, a contradiction. Hence $q = q'$ and then $r = r'$. By Lemma 0 the normalized lists are also unique. $\square$

**Lemma 6 (derivative and scalar multiple).** The list $[1 \cdot a_1, \ldots, (n-1) \cdot a_{n-1}]$ has the value $\sum_{i \ge 1} i a_i x^{i-1}$, the formal derivative, and $[s a_0, \ldots, s a_{n-1}]$ has the value $s \operatorname{val}(a)$. After NORMALIZE both are normalized by Lemma 1. $\square$

**Theorem.** Each operation of the dense representation takes normalized lists to a normalized list (or pair of lists) whose value is the exact result in $R[x]$, and by Lemma 0 the length of each result is its degree plus one.

*Proof.* Lemmas 2 to 6, with subtraction as ADD of $a$ and the list $[-b_0, \ldots, -b_{n-1}]$, which is normalized because $-b_{n-1} \ne 0$ when $b_{n-1} \ne 0$. $\blacksquare$
