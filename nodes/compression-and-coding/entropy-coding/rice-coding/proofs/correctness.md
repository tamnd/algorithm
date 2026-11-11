---
title: The Rice decoder returns the coded integers and the code is prefix-free
proves: [correctness]
status: full
---

Fix $k \ge 0$. For $x \ge 0$ let $q = \lfloor x / 2^k \rfloor$ and $r = x - q 2^k$, so $0 \le r < 2^k$, and write $\langle r \rangle_k$ for the $k$-bit binary form of $r$. Line L1 computes $q$, because a right shift by $k$ places is a division by $2^k$ rounded down. Line L3 writes the $k$ low bits of $x$, which are $\langle r \rangle_k$. So the codeword is

$$c(x) = 0^q\, 1\, \langle r \rangle_k, \qquad |c(x)| = q + 1 + k.$$

**Lemma 1 (one codeword).** Let the reader stand at the start of $c(x)$, followed by any bits. Then RICE-DECODE$(k, R)$ returns $x$ and leaves the reader just after $c(x)$.

*Proof.* The loop of line L4 keeps the invariant that after $j$ rounds it has read $0^j$ and $q = j$. The bits $1, \ldots, q$ of $c(x)$ are zeros and bit $q + 1$ is a one, so the loop stops after it reads that one, with $q$ equal to the coded quotient. Line L5 reads the next $k$ bits, which are $\langle r \rangle_k$, so $r$ is the coded remainder. Line L6 returns $q 2^k + r = x$; the OR of $q \ll k$ and $r$ is a sum because $r < 2^k$. The reader has read $q + 1 + k$ bits. $\square$

**Lemma 2 (prefix-free).** If $x \ne y$, then $c(x)$ is not a prefix of $c(y)$.

*Proof.* Let $c(y) = 0^{q'} 1 \langle r' \rangle_k$ and suppose $c(x)$ is a prefix of $c(y)$. The first one bit of $c(x)$ is at position $q + 1$, and since $c(x)$ is a prefix of $c(y)$, the first one bit of $c(y)$ is at the same position, so $q = q'$. Then both codewords have length $q + 1 + k$, so $c(x) = c(y)$, which gives $r = r'$ and $x = y$, a contradiction. $\square$

**Theorem.** Let $s = c(x_1) \cdots c(x_n)$ be the output of RICE-ENCODE with parameter $k$ on $x_1, \ldots, x_n \ge 0$. A decoder that calls RICE-DECODE with the same $k$ until the reader reaches the end of $s$ returns $x_1, \ldots, x_n$, and no other sequence has the code $s$.

*Proof.* By induction with Lemma 1, call $i$ starts at the first bit of $c(x_i)$ and returns $x_i$, and after call $n$ the reader is at the end of $s$. If $y_1, \ldots, y_p$ also has the code $s$ and both lists are nonempty, then one of $c(x_1)$ and $c(y_1)$ is a prefix of the other, and Lemma 2 gives $x_1 = y_1$. Remove this codeword and repeat. Each codeword has at least one bit, so both lists end together, and $p = n$ with $y_i = x_i$. $\blacksquare$
