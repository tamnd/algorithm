---
title: The omega decoder returns the coded integers and the code is prefix-free
proves: [correctness]
status: full
---

For an integer $v \ge 1$ write $\beta(v)$ for the binary digits of $v$ (with its leading one) and $\lambda(v) = \lfloor \log_2 v \rfloor$, so $|\beta(v)| = \lambda(v) + 1$.

**The codeword.** For $x \ge 1$ define the chain $x_0 = x$ and $x_{i+1} = \lambda(x_i)$, and let $k \ge 0$ be the first index with $x_k = 1$. It exists because $\lambda(v) < v$ for $v \ge 2$. The loop of lines L2 to L4 runs for $i = 0, \ldots, k-1$, puts $\beta(x_i)$ in front of $S$, and stops when $x = x_k = 1$. So line L5 writes

$$\omega(x) = \beta(x_{k-1})\, \beta(x_{k-2}) \cdots \beta(x_0)\, 0,$$

and $\omega(1) = 0$. Each group $\beta(x_i)$ starts with a one, and $|\beta(x_i)| = x_{i+1} + 1$.

**Lemma 1 (one codeword).** Let the reader $R$ stand at the start of $\omega(x)$, followed by any bits. Then OMEGA-DECODE$(R)$ returns $x$ and leaves $R$ just after the last bit of $\omega(x)$.

*Proof.* We show this invariant for the test of line L7:

> **(I)** Before the $j$-th test of line L7, for $0 \le j \le k$, the reader has read $\beta(x_{k-1}) \cdots \beta(x_{k-j})$ and $x = x_{k-j}$.

For $j = 0$ nothing is read and line L6 sets $x = 1 = x_k$. Suppose (I) holds for some $j < k$. The next bit of $\omega(x)$ is the first bit of $\beta(x_{k-j-1})$, which is a one, so the test reads it and line L8 runs. The group $\beta(x_{k-j-1})$ has $x_{k-j} + 1 = x + 1$ bits, so line L8 reads exactly its other $x$ bits, and $2^x$ plus their value is the value of the whole group, $x_{k-j-1}$. So (I) holds for $j + 1$.

At $j = k$, the reader has read all groups and $x = x_0$. The next bit is the final zero of $\omega(x)$, so the test reads it, the loop stops, and line L9 returns $x_0 = x$ with the reader just after $\omega(x)$. $\square$

**Lemma 2 (prefix-free).** If $x \ne y$, then $\omega(x)$ is not a prefix of $\omega(y)$.

*Proof.* Suppose $\omega(x)$ is a prefix of $\omega(y)$. Run the decoder on a reader that holds $\omega(y)$. The decoder reads one bit at a time and its choices depend only on the bits read so far. By Lemma 1 on $\omega(x)$ followed by the rest of $\omega(y)$, it stops after exactly the bits of $\omega(x)$ and returns $x$. By Lemma 1 on $\omega(y)$, it stops after exactly the bits of $\omega(y)$ and returns $y$. Both runs are the same run, so $x = y$, a contradiction. $\square$

**Theorem.** Let $s = \omega(x_1) \cdots \omega(x_n)$ be the output of OMEGA-ENCODE on $x_1, \ldots, x_n \ge 1$. A decoder that calls OMEGA-DECODE until the reader reaches the end of $s$ returns $x_1, \ldots, x_n$, and no other sequence of positive integers has the code $s$.

*Proof.* By induction with Lemma 1, before call $i$ the reader stands at the start of $\omega(x_i)$, and call $i$ returns $x_i$. After call $n$ the reader is at the end of $s$. If another sequence $y_1, \ldots, y_p$ has the code $s$ and both lists are nonempty, then $\omega(x_1)$ and $\omega(y_1)$ are both prefixes of $s$, so one is a prefix of the other, and Lemma 2 gives $x_1 = y_1$. Removing this codeword and repeating ends with both lists empty at the same time, since every codeword has at least one bit. So $p = n$ and $y_i = x_i$. $\blacksquare$
