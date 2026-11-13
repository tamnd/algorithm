---
title: Correctness of the discrete wavelet transform
proves: [correctness]
status: full
---

We prove that IDWT inverts DWT when the four filters satisfy the biorthogonality conditions. The proof works with the periodic extension and with every even block length, including blocks that are shorter than the filters.

## Setup

Let $m$ be even and $n = m/2$. For a finite filter $f$ and an integer $i$, let $f^{(i)}$ be the vector of length $m$ with entries

$$f^{(i)}[t] = \sum_{l \equiv t - 2i \ (\mathrm{mod}\ m)} f[l], \qquad 0 \le t < m.$$

This is $f$ shifted by $2i$ and wrapped modulo $m$. Taps that land on the same position are added. On lines L7 and L8, ANALYSIS computes $s[i] = \langle \tilde h^{(i)}, a \rangle$ and $d[i] = \langle \tilde g^{(i)}, a \rangle$, because $\sum_l \tilde h[l]\, a[(2i + l) \bmod m] = \sum_t a[t] \sum_{l \equiv t - 2i} \tilde h[l]$. On line L15, SYNTHESIS computes $b = \sum_i s[i]\, h^{(i)} + d[i]\, g^{(i)}$, by the same regrouping.

So ANALYSIS is the $m \times m$ matrix $\tilde A$ whose rows are $\tilde h^{(0)}, \ldots, \tilde h^{(n-1)}, \tilde g^{(0)}, \ldots, \tilde g^{(n-1)}$, and SYNTHESIS is the $m \times m$ matrix $S$ whose columns are $h^{(0)}, \ldots, h^{(n-1)}, g^{(0)}, \ldots, g^{(n-1)}$.

## Lemma 1 (periodized inner products)

For finite filters $u$ and $v$ and integers $i, i'$,

$$\langle u^{(i)}, v^{(i')} \rangle = \sum_{k \equiv i' - i \ (\mathrm{mod}\ n)} c_{u,v}(k), \qquad c_{u,v}(k) = \sum_l u[l]\, v[l - 2k].$$

*Proof.* Expand both vectors:

$$\langle u^{(i)}, v^{(i')} \rangle = \sum_{t=0}^{m-1} \sum_{l \equiv t - 2i} u[l] \sum_{l' \equiv t - 2i'} v[l'].$$

For a fixed pair $(l, l')$, a position $t$ with both congruences exists exactly when $l + 2i \equiv l' + 2i' \pmod m$, and then $t$ is unique in $[0, m)$. Since $m$ is even, this forces $l - l'$ to be even. Put $l' = l - 2k$. Then the condition is $2k \equiv 2(i' - i) \pmod{2n}$, that is, $k \equiv i' - i \pmod n$. Each pair $(l, l')$ that meets the condition adds $u[l]\, v[l']$ once, so the sum is $\sum_{k \equiv i' - i} \sum_l u[l]\, v[l - 2k]$. $\square$

## Lemma 2 (biorthogonality of the periodized vectors)

Assume, for every integer $k$,

$$c_{\tilde h, h}(k) = c_{\tilde g, g}(k) = \delta_{k,0}, \qquad c_{\tilde h, g}(k) = c_{\tilde g, h}(k) = 0.$$

Then for $0 \le i, i' < n$: $\langle \tilde h^{(i)}, h^{(i')} \rangle = \langle \tilde g^{(i)}, g^{(i')} \rangle = [i = i']$, and $\langle \tilde h^{(i)}, g^{(i')} \rangle = \langle \tilde g^{(i)}, h^{(i')} \rangle = 0$.

*Proof.* By Lemma 1, $\langle \tilde h^{(i)}, h^{(i')} \rangle$ is the sum of $c_{\tilde h, h}(k)$ over all $k$ in one residue class modulo $n$. Only $k = 0$ gives a nonzero term, and $0$ is in the class of $i' - i$ if and only if $i \equiv i' \pmod n$. For $0 \le i, i' < n$ this means $i = i'$. The sum is then $1$, and otherwise $0$. The same argument gives the $\tilde g, g$ case. For the mixed pairs, every term is $0$. $\square$

Only finitely many $k$ give a nonzero $c(k)$, because the filters are finite, so all sums are finite.

## Theorem (one level)

$\tilde A S = I$ and $S \tilde A = I$. So for every vector $a$ of even length $m$, SYNTHESIS applied to the output of ANALYSIS returns $a$, and ANALYSIS applied to the output of SYNTHESIS returns $(s, d)$.

*Proof.* The entry of $\tilde A S$ in row $r$ and column $r'$ is the inner product of the row vector $r$ of $\tilde A$ with the column vector $r'$ of $S$. Lemma 2 says this is $1$ if $r = r'$ and $0$ otherwise. So $\tilde A S = I$. Both matrices are square of size $m$, so $S$ is the inverse of $\tilde A$, and $S \tilde A = I$. $\square$

## Theorem (all levels)

For $N$ divisible by $2^J$, IDWT(DWT($x$)) $= x$.

*Proof.* Let $a^{(0)} = x$ and let $a^{(j)}, d^{(j)}$ be the outputs of ANALYSIS at level $j$, on a block of the even length $N/2^{j-1}$. We show by induction on $j$, going down from $J$ to $1$, that after the loop body of line L11 runs for level $j$, the variable $a$ holds $a^{(j-1)}$. Before the loop, $a = a^{(J)}$. If $a = a^{(j)}$ before the body for level $j$, the body computes SYNTHESIS$(a^{(j)}, d^{(j)})$, and the one-level theorem with $m = N/2^{j-1}$ makes this $a^{(j-1)}$. After the body for $j = 1$, $a = a^{(0)} = x$, which line L12 returns. $\square$

## Remarks

- The conditions are on the infinite filters, not on the length $m$. So the same filters give perfect reconstruction at every level, even on the last level, where the block is shorter than the filter and many taps wrap onto the same position.
- In the orthonormal case $h = \tilde h$ and $g = \tilde g$, the matrix $S$ is $\tilde A^{\mathsf T}$, so $\tilde A$ is orthogonal and the transform keeps the energy.
- For the 5/3 filters on the page, the conditions hold: for example $c_{\tilde h, h}(0) = \tfrac14 \cdot \tfrac12 + \tfrac34 \cdot 1 + \tfrac14 \cdot \tfrac12 = 1$ and $c_{\tilde h, h}(1) = \tilde h[1] h[-1] + \tilde h[2] h[0] = \tfrac14 \cdot \tfrac12 - \tfrac18 \cdot 1 = 0$.
