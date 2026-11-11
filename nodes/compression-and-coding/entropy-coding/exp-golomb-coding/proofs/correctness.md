---
title: The exp-Golomb decoder returns the coded integers and the code is prefix-free
proves: [correctness]
status: full
---

Fix $k \ge 0$. For $x \ge 0$ let $y = x + 2^k$ and $n = \lfloor \log y \rfloor$. Since $y \ge 2^k$, $n \ge k$. The binary form of $y$ has exactly $n + 1$ digits and its top digit is a one; write it $1\,b_{n-1} \cdots b_0$. Lines L3 and L4 write

$$c(x) = 0^{\,n-k}\; 1\, b_{n-1} \cdots b_0, \qquad |c(x)| = 2n - k + 1.$$

**Lemma 1 (one codeword).** Let the reader stand at the start of $c(x)$, followed by any bits. Then EXPGOLOMB-DECODE$(k, R)$ returns $x$ and leaves the reader just after $c(x)$.

*Proof.* The first $n - k$ bits of $c(x)$ are zeros and bit $n - k + 1$ is a one. Line L5 counts zeros until it reads a one, so it sets $z = n - k$ and has read the top digit of $y$. Line L6 sets $y$ to 1, the value of that digit.

Line L7 keeps the invariant: after $j$ rounds, $y = (1\, b_{n-1} \cdots b_{n-j})_2$, the value of the top $j + 1$ digits. This holds for $j = 0$ by line L6. If it holds after round $j$, round $j + 1$ reads the next bit, which is $b_{n-j-1}$, and $2y + b_{n-j-1}$ is the value of the top $j + 2$ digits. The loop runs $z + k = n$ rounds, so at its end $y$ is the value of all $n + 1$ digits, which is $x + 2^k$. Line L8 returns $x$. The reader has read $(n - k) + 1 + n = |c(x)|$ bits. $\square$

**Lemma 2 (prefix-free).** If $x \ne x'$, then $c(x)$ is not a prefix of $c(x')$.

*Proof.* Suppose $c(x)$ is a prefix of $c(x')$, with parameters $n$ and $n'$. The first one bit of $c(x)$ is at position $n - k + 1$. Because $c(x)$ is a prefix of $c(x')$, the first one bit of $c(x')$ is at the same position, so $n' = n$. Then $|c(x)| = |c(x')| = 2n - k + 1$, so $c(x) = c(x')$, and the last $n + 1$ bits give $x + 2^k = x' + 2^k$, so $x = x'$, a contradiction. $\square$

**Theorem.** Let $s = c(x_1) \cdots c(x_m)$ be the output of EXPGOLOMB-ENCODE with order $k$ on $x_1, \ldots, x_m \ge 0$. A decoder that calls EXPGOLOMB-DECODE with the same $k$ until the reader reaches the end of $s$ returns $x_1, \ldots, x_m$, and no other sequence has the code $s$.

*Proof.* By induction with Lemma 1, call $i$ starts at the first bit of $c(x_i)$ and returns $x_i$, and after call $m$ the reader is at the end of $s$, so the decoder stops. If $x'_1, \ldots, x'_p$ also has the code $s$ and both lists are nonempty, then one of $c(x_1)$ and $c(x'_1)$ is a prefix of the other, and Lemma 2 gives $x_1 = x'_1$. Remove this codeword from both and repeat. Each codeword has at least one bit, so both lists end together, $p = m$ and $x'_i = x_i$ for all $i$.

The signed map of `se(v)` is a bijection from the integers onto $\{0, 1, 2, \ldots\}$: $v > 0$ goes to the odd number $2v - 1$ and $v \le 0$ goes to the even number $-2v$, and the inverse $(-1)^{c+1} \lceil c/2 \rceil$ undoes both cases. So the signed code also decodes uniquely. $\blacksquare$
