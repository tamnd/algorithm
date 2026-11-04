---
title: Elias-Fano access and next-geq are correct, and the space bound
proves: [correctness, space]
status: full
---

Let $0 \le x_0 \le \cdots \le x_{n-1} < u$, let $\ell$ be as in line L1, and write $x_i = h_i 2^\ell + l_i$ with $0 \le l_i < 2^\ell$. Then $h_i = \lfloor x_i / 2^\ell \rfloor \le \lfloor (u-1)/2^\ell \rfloor$, and $h_0 \le h_1 \le \cdots \le h_{n-1}$ because $\lfloor \cdot / 2^\ell \rfloor$ is monotone.

**Lemma 1.** The 1s of $H$ are exactly at the positions $q_i = h_i + i$, these are strictly increasing in $i$, and they lie inside $H$.

*Proof.* Line L4 sets the bits $q_i$ and no others. $q_{i+1} - q_i = h_{i+1} - h_i + 1 \ge 1$. The largest is $q_{n-1} \le \lfloor (u-1)/2^\ell \rfloor + n - 1$, less than the length of $H$. $\square$

**Access.** By Lemma 1 the $(i+1)$-th 1 of $H$, in increasing order, is at $q_i$, so SELECT1$_H(i+1) - i = h_i$. Line L5 returns $h_i 2^\ell + Lo[i] = h_i 2^\ell + l_i = x_i$.

**Lemma 2.** For $h \ge 0$ with $h \le \lfloor (u-1)/2^\ell \rfloor$, let $p_h = 0$ if $h = 0$ and $p_h = \text{SELECT0}_H(h) + 1$ otherwise. Then $p_h - h = |\{i : h_i < h\}|$.

*Proof.* For $h = 0$ both sides are 0. Let $h \ge 1$. $H$ has $\lfloor (u-1)/2^\ell \rfloor + 1 \ge h + 1$ zeros, since it has $n$ ones and length $n + \lfloor (u-1)/2^\ell \rfloor + 1$, so the $h$-th 0 exists. Before position $q_i$ there are exactly $q_i - i = h_i$ zeros, because the other $i$ positions before $q_i$ hold the 1s $q_0, \ldots, q_{i-1}$. So $q_i$ comes before the $h$-th 0 if and only if $h_i < h$: if $h_i < h$, at most $h - 1$ zeros precede $q_i$; if $h_i \ge h$, the $h$-th 0 precedes $q_i$. The positions $0, \ldots, p_h - 1$ contain exactly $h$ zeros, and the ones among them are the $q_i$ with $h_i < h$. Hence $p_h = h + |\{i : h_i < h\}|$. $\square$

**Next-geq.** Let $0 \le x < u$, $h = \lfloor x / 2^\ell \rfloor$, and let $i^* = \min\{i : x_i \ge x\}$, or $n$ if no such $i$ exists. Line L8 sets $i = p_h - h$, which by Lemma 2 is the number of elements with $h_i < h$; by monotonicity these are $x_0, \ldots, x_{i-1}$. Each of them satisfies $x_j < h 2^\ell \le x$, so $i \le i^*$. The loop of line L9 increases $i$ while $x_i < x$; since the sequence is nondecreasing, the elements $x_i, x_{i+1}, \ldots, x_{i^*-1}$ are all less than $x$, and $x_{i^*} \ge x$ or $i^* = n$. So the loop stops exactly at $i = i^*$, which line L10 returns.

**Space.** The low bits take $n \ell$ bits, and $H$ has $n$ ones and $Z = \lfloor (u-1)/2^\ell \rfloor + 1$ zeros. If $u \ge n \ge 1$ and $\ell = \lfloor \lg(u/n) \rfloor$, then $\ell + 1 > \lg(u/n)$, so $2^\ell > u/(2n)$ and $Z \le u / 2^\ell + 1 < 2n + 1$. The total is less than $n \ell + 3n + 1$ bits. If instead $\ell = \lceil \lg(u/n) \rceil$, then $2^\ell \ge u/n$, $Z \le n + 1$, and the total is at most $n \lceil \lg(u/n) \rceil + 2n + 1$. $\blacksquare$
