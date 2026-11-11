---
title: The Golomb decoder returns the coded integers and the code is prefix-free
proves: [correctness]
status: full
---

Fix $m \ge 1$, and let $k = \lfloor \log_2 m \rfloor$ and $u = 2^{k+1} - m$. Since $2^k \le m < 2^{k+1}$, we have $1 \le u \le 2^k$ and $u \le m$. Write $\langle v \rangle_j$ for the $j$-bit binary form of $0 \le v < 2^j$.

**Truncated binary.** For $0 \le r < m$, lines L4 and L5 write

$$t(r) = \langle r \rangle_k \text{ if } r < u, \qquad t(r) = \langle r + u \rangle_{k+1} \text{ if } r \ge u.$$

The second form is valid: $u \le r < m$ gives $2u \le r + u < m + u = 2^{k+1}$.

**Lemma 1.** Let the reader stand at the start of $t(r)$, followed by any bits. Then lines L8 and L9 set $r$ to the coded remainder and leave the reader just after $t(r)$.

*Proof.* If $r < u$, line L8 reads $\langle r \rangle_k$ and gets $r < u$, so line L9 does nothing. If $r \ge u$, let $v = r + u$. Line L8 reads the top $k$ bits of $\langle v \rangle_{k+1}$, which is $\lfloor v/2 \rfloor \ge u$ because $v \ge 2u$. So line L9 runs, reads the last bit $v \bmod 2$, and sets $r \leftarrow 2\lfloor v/2 \rfloor + (v \bmod 2) - u = v - u$, the coded remainder. In both cases the reader has read exactly $|t(r)|$ bits. $\square$

**Lemma 2.** The words $t(0), \ldots, t(m-1)$ form a prefix code.

*Proof.* Two short words have the same length $k$ and differ as numbers, so neither is a proper prefix of the other. The same holds for two long words. A short word $\langle r \rangle_k$ with $r < u$ cannot be a prefix of a long word $\langle v \rangle_{k+1}$, since the top $k$ bits of the long word are $\lfloor v/2 \rfloor \ge u > r$. $\square$

**The codeword.** For $x \ge 0$, line L1 gives $x = qm + r$ with $q \ge 0$ and $0 \le r < m$, and the codeword is $c(x) = 1^q\, 0\, t(r)$.

**Lemma 3 (one codeword).** Let the reader stand at the start of $c(x)$, followed by any bits. Then GOLOMB-DECODE$(m, R)$ returns $x$ and leaves the reader just after $c(x)$.

*Proof.* The loop of line L6 reads $q$ ones and then the zero, and stops with $q$ equal to the coded quotient: after $j \le q$ reads of a one the counter is $j$, and the next bit after $q$ ones is the zero. Line L7 computes the same $k$ and $u$ as line L3. By Lemma 1, lines L8 and L9 read exactly $t(r)$ and set $r$. Line L10 returns $qm + r = x$. $\square$

**Lemma 4 (prefix-free).** If $x \ne y$, then $c(x)$ is not a prefix of $c(y)$.

*Proof.* Let $x = qm + r$ and $y = q'm + r'$. Suppose $c(x)$ is a prefix of $c(y)$. The first zero of $c(x)$ is at position $q + 1$ and the first zero of $c(y)$ is at position $q' + 1$; since $c(x)$ is a prefix and contains this zero, $q = q'$. Then $t(r)$ is a prefix of $t(r')$, and Lemma 2 gives $r = r'$. So $x = y$, a contradiction. $\square$

**Theorem.** Let $s = c(x_1) \cdots c(x_n)$ be the output of GOLOMB-ENCODE with parameter $m$ on $x_1, \ldots, x_n \ge 0$. A decoder that calls GOLOMB-DECODE with the same $m$ until the reader reaches the end of $s$ returns $x_1, \ldots, x_n$, and no other sequence has the code $s$.

*Proof.* By induction with Lemma 3, call $i$ starts at the first bit of $c(x_i)$ and returns $x_i$, and after call $n$ the reader is at the end of $s$. If $y_1, \ldots, y_p$ also has the code $s$ and both lists are nonempty, then one of $c(x_1)$ and $c(y_1)$ is a prefix of the other, so Lemma 4 gives $x_1 = y_1$. Remove this codeword and repeat. Each codeword has at least one bit, so both lists end together, and $p = n$ with $y_i = x_i$. $\blacksquare$
