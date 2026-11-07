---
title: The Wallace tree computes the product in few levels
proves: [correctness, termination]
status: full
---

Let $a = \sum_{i<n} a_i 2^i$ and $b = \sum_{j<m} b_j 2^j$ with bits $a_i, b_j$. A *configuration* is a finite multiset of bits placed in columns $0, 1, 2, \ldots$; its value is $V = \sum_k 2^k \sigma_k$, where $\sigma_k$ is the number of ones in column $k$, and its height in column $k$ is the number $h_k$ of bits in column $k$.

**Lemma 1 (the adders keep the value).** For bits $x, y, z$,

$$x + y + z = (x \oplus y \oplus z) + 2\,\mathrm{maj}(x, y, z), \qquad x + y = (x \oplus y) + 2(x \wedge y).$$

*Proof.* Both sides of the first identity are symmetric in $x, y, z$ and depend only on the number $t$ of ones among them: for $t = 0, 1, 2, 3$ the right side is $0, 1, 0 + 2, 1 + 2$. The second identity is the first with $z = 0$. $\square$

The full adder of the implementation computes $s = (x \oplus y) \oplus z$ and $c = (x \wedge y) \vee ((x \oplus y) \wedge z)$, and the second expression is $\mathrm{maj}(x, y, z)$: if $x = y$ it is $x$, and if $x \ne y$ it is $z$. So replacing three bits of column $k$ by a full adder's sum bit in column $k$ and carry bit in column $k + 1$ changes $V$ by $2^k(s - x - y - z) + 2^{k+1} c = 0$, and the same holds for a half adder.

**Lemma 2 (invariant).** After line L1 and after every level of lines L2 to L6, $V = ab$.

*Proof.* After line L1, column $k$ holds the bits $a_i \wedge b_j = a_i b_j$ with $i + j = k$, so $V = \sum_{i,j} a_i b_j 2^{i+j} = ab$. A level replaces disjoint groups of bits by adder outputs, each replacement keeps $V$ by Lemma 1, and bits outside the groups stay where they are; so $V$ is unchanged. $\square$

**Lemma 3 (termination).** The loop of line L2 ends after finitely many levels.

*Proof.* A full adder replaces three bits by two, and a half adder two bits by two, so the total number of bits never grows. If the loop runs, some column holds $h \ge 3$ bits, and line L5 applies $\lfloor h/3 \rfloor \ge 1$ full adders there, so the total number of bits falls by at least one. It starts at $nm$, so there are at most $nm$ levels. Lemma 4 gives a much better bound. $\square$

**Theorem (correctness).** The algorithm returns $ab$.

*Proof.* When the loop ends every column holds at most two bits, so line L7 can place them in two rows $X$ and $Y$ with $X + Y = \sum_k 2^k \sigma_k = V = ab$ by Lemma 2. Line L8 adds them exactly, for example by the [Kogge-Stone adder](/kogge-stone-adder/). No bit is lost by the width $n + m$: a bit in a column $k \ge n + m$ would have weight at least $2^{n+m}$, and since all weights are nonnegative and $V = ab < 2^{n+m}$, every such bit is 0. $\square$

**Lemma 4 (levels).** Let $d_0 = 2$ and $d_{j+1} = \lfloor 3 d_j / 2 \rfloor$. If every column has height at most $d_{j+1}$, then after one level every column has height at most $d_j$. Hence, if $L$ is the least index with $d_L \ge \min(n, m)$, the loop runs at most $L$ times.

*Proof.* Consider column $k$ of height $h$ and column $k - 1$ of height $h'$. Write $h = 3q + r$ with $0 \le r < 3$. In column $k$ the level leaves $q$ sum bits of full adders and, if $r > 0$, one more bit (a half adder's sum or a single bit); that is $\lceil h/3 \rceil$ bits. From column $k - 1$ it receives one carry for each full adder and one for a half adder, which is $\lfloor h'/3 \rfloor + [h' \bmod 3 = 2] = \lfloor (h' + 1)/3 \rfloor$ carries. Both counts are nondecreasing in $h$ and $h'$, so for $h, h' \le D = d_{j+1}$ the new height is at most

$$\lceil D/3 \rceil + \lfloor (D + 1)/3 \rfloor = \lceil 2D/3 \rceil ,$$

as the three cases $D = 3q, 3q + 1, 3q + 2$ give $2q, 2q + 1, 2q + 2$. Since $D = \lfloor 3 d_j/2 \rfloor \le 3 d_j / 2$, we have $2D/3 \le d_j$, and $d_j$ is an integer, so $\lceil 2D/3 \rceil \le d_j$.

After line L1 column $k$ has $\min(k, n - 1, m - 1, n + m - 2 - k) + 1 \le \min(n, m) \le d_L$ bits. By induction, after $t$ levels every height is at most $d_{L - t}$, so after $L$ levels every height is at most $d_0 = 2$, and the loop has stopped. $\square$

Since $d_{j+1} \ge \frac{3}{2} d_j - \frac12$, we have $d_j \ge (3/2)^j + 1$, so $L \le \log_{3/2}(\min(n, m)) + 1$.

**Corollary (depth).** The AND gates of line L1 have depth 1. A full adder's outputs have depth at most 3 more than its inputs, and a half adder's at most 1 more, so after $L$ levels every bit has depth at most $1 + 3L$. A Kogge-Stone adder of width $W = n + m$ adds at most $2\lceil \log_2 W \rceil + 2$: one level for the generate and propagate signals, two gates for each of the $\lceil \log_2 W \rceil$ prefix levels, and one XOR for the sum bits. So the depth is at most $3L + 2 \lceil \log_2 (n + m) \rceil + 3$, which is $O(\log n)$ for $m = n$. $\blacksquare$
