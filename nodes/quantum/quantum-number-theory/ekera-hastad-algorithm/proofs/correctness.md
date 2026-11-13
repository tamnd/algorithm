---
title: The Ekerå-Håstad algorithm returns the short logarithm d
proves: [correctness]
status: full
---

We use the pseudocode of the page. $g$ is an element of a finite abelian group $G$ of order $r$, which is not given to the algorithm, and $x = g^d$ with $0 \le d < 2^m$. Let $\ell = \lceil m/s \rceil$, $A = 2^{\ell + m}$, $B = 2^\ell$ and $\omega = e^{2\pi i/A}$, so $e^{2\pi i/B} = \omega^{2^m}$. For an integer $z$, $\{z\}$ is the residue of $z$ modulo $A$ in $[-A/2, A/2)$. The quantum Fourier transform of size $M$ maps $|a\rangle$ to $M^{-1/2} \sum_{c=0}^{M-1} e^{2\pi i ac/M} |c\rangle$. We assume, as Ekerå and Håstad do, that

$$r \ge A + (B - 1)d. \qquad (*)$$

For a pair $(j, k)$ let $T = dj + 2^m k$. The pair is *good* if $|\{T\}| \le 2^{m-2}$.

**Lemma 1 (the output distribution).** Under $(*)$, one run of lines L4 to L7 gives $(j, k)$ with probability

$$P(j, k) = \frac{1}{(AB)^2} \sum_{e} \Big| \sum_{b \in B_e} \omega^{bT} \Big|^2, \qquad B_e = \{\, b : 0 \le b < B,\ 0 \le e + bd < A \,\}.$$

So $P(j, k)$ depends on $(j, k)$ only through $T \bmod A$.

*Proof.* Line L4 gives $(AB)^{-1/2} \sum_{a < A, b < B} |a\rangle|b\rangle|0\rangle$, and line L5 gives $(AB)^{-1/2} \sum_{a, b} |a\rangle|b\rangle|g^{a - bd}\rangle$, because $x^{-b} = g^{-bd}$. Group the terms by $e = a - bd$. For fixed $e$ the pairs are $(e + bd, b)$ with $b \in B_e$. The values of $e$ lie in an interval of $A + (B - 1)d$ consecutive integers, so by $(*)$ distinct values of $e$ give distinct group elements $g^e$. After line L6 the amplitude of $|j\rangle|k\rangle|g^e\rangle$ is

$$\frac{1}{AB} \sum_{b \in B_e} \omega^{(e + bd)j} \omega^{2^m bk} = \frac{\omega^{ej}}{AB} \sum_{b \in B_e} \omega^{bT}.$$

The states $|g^e\rangle$ are orthogonal, so line L7 sees the sum over $e$ of the squared moduli. $\square$

**Lemma 2 (good pairs are likely).** Under $(*)$ and for $m \ge 2$, one run gives a good pair with probability at least $1/8$.

*Proof.* Fix a good pair, so the step angle $\varphi = 2\pi \{T\}/A$ satisfies $|\varphi| \le 2\pi 2^{m-2}/2^{\ell + m} = \pi/(2B)$. Each $B_e$ is a set of $n_e$ consecutive integers with $n_e \le B$, so the terms $\omega^{bT} = e^{i b \varphi}$ for $b \in B_e$ lie on an arc of width at most $(B - 1)\pi/(2B) < \pi/2$. Each term is within $\pi/4$ of the middle of the arc, so its component in that direction is at least $\cos(\pi/4)$, and $|\sum_{b \in B_e} \omega^{bT}|^2 \ge n_e^2/2$. The $n_e$ add up to $AB$, and at most $A + (B - 1)d < 2A$ of them are nonzero, because $d < 2^m$. By the Cauchy-Schwarz inequality, $\sum_e n_e^2 > (AB)^2/(2A)$. Lemma 1 then gives $P(j, k) > 1/(4A)$ for every good pair.

Now count the good pairs. For a fixed $j$, the values $2^m k \bmod A$ for $k < B$ are the $B$ multiples of $2^m$ below $A$, so the values of $\{T\}$ are the integers in $[-A/2, A/2)$ that are congruent to $dj$ modulo $2^m$, one in each block of $2^m$ consecutive integers. The window $[-2^{m-2}, 2^{m-2}]$ is shorter than $2^m$, so it holds one such value if the residue $u$ of $dj$ modulo $2^m$ in $[-2^{m-1}, 2^{m-1})$ satisfies $|u| \le 2^{m-2}$, and none otherwise. Write $d = 2^t d'$ with $d'$ odd (if $d = 0$, every $j$ counts). As $j$ runs over $[0, A)$, $dj \bmod 2^m$ takes each multiple of $2^{\min(t, m)}$ below $2^m$ equally often, $2^{\ell + \min(t, m)}$ times. If $t \le m - 2$, the window holds $2^{m-1-t} + 1$ of these multiples. If $t \ge m - 1$, it holds the multiple 0, which is hit at least $2^{\ell + m - 1}$ times. In all cases there are at least $A/2$ good pairs, so their total probability is more than $(A/2) \cdot 1/(4A) = 1/8$. $\square$

**Lemma 3 (the lattice).** Let $L$ be the lattice spanned by the rows $(j_1, \dots, j_s, 1)$ and $A e_i$ for $i = 1, \dots, s$, and let $v = (\{-2^m k_1\}, \dots, \{-2^m k_s\}, 0)$. For every integer $d'$, the vectors of $L$ with last coordinate $d'$ are the vectors $(d' j_i + t_i A)_i$ followed by $d'$, with $t_i \in \mathbb{Z}$, and the closest of them to $v$ has squared distance

$$D(d') = \sum_{i=1}^{s} \{d' j_i + 2^m k_i\}^2 + d'^2.$$

If $|\{d j_i + 2^m k_i\}| \le 2^{m-1}$ for every $i$, in particular if all $s$ pairs are good, then $D(d) < (s/4 + 1) 4^m$.

*Proof.* A vector of $L$ is $y_0 (j_1, \dots, j_s, 1) + \sum_i y_i A e_i$, and its last coordinate is $y_0$. With $y_0 = d'$, coordinate $i$ minus $v_i$ is congruent to $d' j_i + 2^m k_i$ modulo $A$, and $y_i$ moves it by any multiple of $A$, so the smallest modulus is $|\{d' j_i + 2^m k_i\}|$. For $d' = d$ each term is at most $4^{m-1}$, and $d^2 < 4^m$. $\square$

**Lemma 4 (the enumeration).** Line L10 returns every $u \in L$ with $|u - v|^2 \le R^2 = (s/4 + 1) 4^m$, so line L11 tries every $d' \in [0, 2^m)$ with $D(d') \le R^2$.

*Proof.* LLL only changes the basis by unimodular integer operations, so the reduced basis spans $L$. Let $b_1^*, \dots, b_{s+1}^*$ be its Gram-Schmidt vectors. Write $u = \sum_i y_i b_i$ and $v = \sum_i \nu_i b_i^*$. Then $|u - v|^2 = \sum_i (y_i + \sum_{t > i} \mu_{t,i} y_t - \nu_i)^2 |b_i^*|^2$, and each term is nonnegative. The enumeration fixes $y_{s+1}, y_s, \dots$ in turn and keeps every integer $y_i$ whose term, added to the terms already fixed, stays at most $R^2$. A vector with $|u - v|^2 \le R^2$ passes every one of these tests, so the enumeration finds it. The vectors found with last coordinate $d'$ include the closest one, and by Lemma 3 that one has squared distance $D(d')$. $\square$

**Theorem.** If the algorithm returns $d'$, then $g^{d'} = x$ and $0 \le d' < 2^m$. Under $(*)$, each batch of $s$ runs makes line L12 return with probability at least $8^{-s}$, so the number of batches is at most geometric with this success rate. If $d$ is the only exponent in $[0, 2^m)$ with $g^d = x$, for example if $r \ge 2^m$, the output is $d$.

*Proof.* Line L11 keeps only $d' \in [0, 2^m)$, and line L12 returns $d'$ only after it checks $g^{d'} = x$. The $s$ runs of a batch are independent, so by Lemma 2 all of them are good with probability at least $8^{-s}$. Then $D(d) < R^2$ by Lemma 3, so line L11 tries $d$ by Lemma 4, and line L12 accepts it, or an earlier candidate $d'$ with $g^{d'} = x$. The last claim holds because $g^{d'} = g^d$ with $|d' - d| < 2^m \le r$ forces $d' = d$. $\square$

The bound $8^{-s}$ is crude. A batch can succeed when some pairs are not good, because Lemma 3 needs only $|\{d j_i + 2^m k_i\}| \le 2^{m-1}$ and the radius has slack. Ekerå and Håstad give a heuristic analysis of the success rate, and Ekerå proved a much stronger lower bound for one run with a limited classical search.

**Corollary (factoring RSA integers).** Let $N = pq$ with distinct odd primes $2^{n-1} < p, q < 2^n$, and let $g \in \mathbb{Z}_N^*$. Then $x = g^{(N-1)/2}$ equals $g^d$ with $d = (p + q - 2)/2$ and $2^{n-1} \le d < 2^n$. If lines L13 to L17 obtain this $d$, then $c = d + 1$ satisfies $\{p, q\} = \{c - \sqrt{c^2 - N},\ c + \sqrt{c^2 - N}\}$.

*Proof.* $\varphi(N) = (p-1)(q-1) = N - (p + q) + 1$, so $(N - 1)/2 - d = \varphi(N)/2$. The exponent $\varphi(N)/2$ is a multiple of $\operatorname{lcm}(p - 1, q - 1)$, because $p - 1$ and $q - 1$ are both even, so $g^{\varphi(N)/2} = 1$ and $x = g^d$. From $2^{n-1} + 1 \le p, q \le 2^n - 1$ we get $2^{n-1} \le d \le 2^n - 2$, so $m = n$ bits suffice. Finally $c = (p + q)/2$ and $c^2 - N = ((p - q)/2)^2$, so $c \pm \sqrt{c^2 - N}$ are $p$ and $q$. If the order of $g$ is less than $2^m$, the returned $d'$ may differ from $d$; then $c^2 - N$ is in general not a square, and line L15 retries with a new $g$. $\square$
