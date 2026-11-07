---
title: The subproduct tree holds the range products, and its two traversals evaluate and combine correctly
proves: [correctness]
status: full
---

Let $R$ be a commutative ring, $n \ge 1$ and $u_0, \ldots, u_{n-1} \in R$. For integers $0 \le l \le r \le n$ write

$$P(l, r) = \prod_{l \le j < r} (x - u_j),$$

a monic polynomial of degree $r - l$, with $P(l, l) = 1$. For a level $h \ge 0$ and an index $i \ge 0$, let $l_{h,i} = i\,2^h$ and $r_{h,i} = \min((i + 1)\,2^h, n)$.

## The build

**Claim.** After line L1, and after each pass of the loop L3 to L8, the list $T[h]$ has $\lceil n / 2^h \rceil$ nodes and its node $i$ is $P(l_{h,i}, r_{h,i})$.

*Level 0.* Line L1 sets node $i$ to $x - u_i = P(i, i + 1)$, and $r_{0,i} = i + 1$ because $i < n$. There are $n$ nodes.

*From $h$ to $h + 1$.* Let $L = \lceil n / 2^h \rceil$ be the number of nodes at level $h$. For a pair $2i, 2i + 1 < L$, line L6 forms

$$P(l_{h,2i}, r_{h,2i}) \cdot P(l_{h,2i+1}, r_{h,2i+1}) = P(2i\,2^h, (2i + 1)\,2^h) \cdot P((2i + 1)\,2^h, r_{h,2i+1}) = P(l_{h+1,i}, r_{h+1,i}),$$

because $r_{h,2i} = (2i + 1) 2^h$ when node $2i + 1$ exists, and $r_{h,2i+1} = \min((2i + 2) 2^h, n) = r_{h+1,i}$. If $L$ is odd, line L7 copies the last node, of index $L - 1 = 2i$, as node $i$ of level $h + 1$. It is $P(2i\,2^h, n)$, and $l_{h+1,i} = 2i\,2^h$ and $r_{h+1,i} = n$ because $(2i + 1) 2^h \ge n$. So level $h + 1$ has $\lceil L / 2 \rceil = \lceil n / 2^{h+1} \rceil$ nodes of the claimed form.

*End.* The number of nodes is at least $1$ and decreases strictly while it is larger than $1$, so the loop stops, at the first $k$ with $\lceil n / 2^k \rceil = 1$, that is $k = \lceil \log_2 n \rceil$. Then $T[k] = [P(0, n)] = [m]$ with $m = \prod_j (x - u_j)$.

## Remainder descent

Let $f \in R[x]$. Every node is monic, so division with remainder by a node is defined over $R$. EVALUATE sets $r_{k,0} = f \operatorname{rem} m$ and then, for each level $h$ from $k - 1$ down to $0$, $r_{h,i} = r_{h+1, \lfloor i/2 \rfloor} \operatorname{rem} T[h][i]$.

**Claim.** $r_{h,i} = f \operatorname{rem} T[h][i]$ for all $h$ and $i$.

The node $T[h][i]$ divides its parent $T[h+1][\lfloor i/2 \rfloor]$, because by the build claim the range of the child is contained in the range of the parent. If $g \mid G$ and $G$ is monic, then $(f \operatorname{rem} G) \operatorname{rem} g = f \operatorname{rem} g$: write $f = q G + (f \operatorname{rem} G)$; then $f - (f \operatorname{rem} G) = q G$ is a multiple of $g$, so $f$ and $f \operatorname{rem} G$ have the same remainder modulo the monic $g$, by the uniqueness of the remainder. The claim follows by induction from the root down. When the degree of $r_{h+1, \lfloor i/2 \rfloor}$ is already less than the degree of the node, the remainder is this polynomial itself, which is the shortcut in the implementation.

At level $0$ the node is $x - u_j$ and $f \operatorname{rem} (x - u_j) = f(u_j)$ by the [polynomial remainder theorem](/polynomial-remainder-theorem/). So EVALUATE returns $f(u_0), \ldots, f(u_{n-1})$.

## Linear combination

Let $c_0, \ldots, c_{n-1} \in R$. COMBINE sets $s_{0,i} = c_i$ and, for each level, $s_{h+1,i} = s_{h,2i} \cdot T[h][2i + 1] + s_{h,2i+1} \cdot T[h][2i]$ for each pair, and copies $s_{h, L-1}$ when $L$ is odd.

**Claim.** $s_{h,i} = \sum_{l \le j < r} c_j\, P(l, r) / (x - u_j)$, where $l = l_{h,i}$, $r = r_{h,i}$, and $P(l, r) / (x - u_j) = P(l, j)\, P(j + 1, r)$ is the product of the other factors.

At level $0$ the sum has the single term $c_i P(i, i+1) / (x - u_i) = c_i$. For a pair, let the left range be $[l, t)$ and the right range $[t, r)$. For $j$ in the left range, $P(l, r) / (x - u_j) = (P(l, t) / (x - u_j)) \cdot P(t, r)$, and $P(t, r)$ is the right node $T[h][2i + 1]$. For $j$ in the right range, $P(l, r) / (x - u_j) = P(l, t) \cdot (P(t, r) / (x - u_j))$, and $P(l, t)$ is the left node. Adding the two parts gives the formula of line C4. A copied node keeps its range, so its sum does not change. At the root, COMBINE returns $\sum_j c_j\, m / (x - u_j)$.

## Interpolation

Let $R$ be a field and the $u_j$ distinct. Then $m'(u_j) = \prod_{i \ne j} (u_j - u_i) \ne 0$, by the product rule applied to $m = (x - u_j) \cdot m / (x - u_j)$ at $x = u_j$. With $c_j = v_j / m'(u_j)$, the polynomial $f = \sum_j c_j\, m / (x - u_j)$ has degree less than $n$, and at $x = u_i$ every term with $j \ne i$ vanishes, so $f(u_i) = c_i \prod_{j \ne i} (u_i - u_j) = v_i$. This is the Lagrange form of the interpolating polynomial, which is the unique polynomial of degree less than $n$ with these values. $\blacksquare$
