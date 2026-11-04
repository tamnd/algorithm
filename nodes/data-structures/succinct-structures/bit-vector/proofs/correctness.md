---
title: The packed bit vector answers access, rank and select correctly
proves: [correctness]
status: full
---

We use the pseudocode of the page, with words of $w$ bits, and write $\beta_t(x) = \lfloor x / 2^t \rfloor \bmod 2$ for bit $t$ of a word $x$. Let $b[0 \ldots n-1]$ be the input and $m$ the number of its 1s.

**Lemma 1 (BUILD).** After BUILD, (P1) $\beta_{i \bmod w}(W[\lfloor i/w \rfloor]) = b[i]$ for $0 \le i < n$, and (P2) $\beta_t(W[\lceil n/w \rceil - 1]) = 0$ for each $t$ with $w(\lceil n/w \rceil - 1) + t \ge n$.

*Proof.* The map $i \mapsto (\lfloor i/w \rfloor, i \bmod w)$ is one to one, so each bit of each word belongs to at most one position $i$. Line L1 sets each word to 0. Line L3, at step $i$, sets the bit $(\lfloor i/w \rfloor, i \bmod w)$ to 1 when $b[i] = 1$, and the OR leaves all other bits as they are. So after the loop of line L2, the bit of position $i$ is 1 exactly when $b[i] = 1$, which is (P1). The bits that belong to no position $i < n$ were set to 0 by line L1 and never written, which is (P2). $\square$

The structure is static, so (P1) and (P2) hold for each later query.

**Lemma 2 (ACCESS).** ACCESS$(i)$ returns $b[i]$ for $0 \le i < n$.

*Proof.* For a word $x$ and $0 \le t < w$, $(x \gg t) \wedge 1 = \lfloor x / 2^t \rfloor \bmod 2 = \beta_t(x)$. With $x = W[\lfloor i/w \rfloor]$ and $t = i \bmod w$, line L4 returns $b[i]$ by (P1). $\square$

**Lemma 3 (RANK1).** RANK1$(i)$ returns $\text{rank}_1(i) = |\{p < i : b[p] = 1\}|$ for $0 \le i \le n$.

*Proof.* Let $q = \lfloor i/w \rfloor$ and $r = i \bmod w$, so $i = qw + r$. The set $\{0, \ldots, i-1\}$ is the disjoint union of the blocks $\{kw, \ldots, kw + w - 1\}$ for $0 \le k < q$ and of $\{qw, \ldots, qw + r - 1\}$. Each block $k < q$ lies inside $\{0, \ldots, n-1\}$ because $kw + w - 1 \le qw - 1 < i \le n$. By (P1), the number of 1s of $b$ in block $k$ is the number of 1 bits of $W[k]$, which line L6 adds. If $r > 0$, then $qw < i \le n$, so $W[q]$ exists. The word $W[q] \wedge (2^r - 1)$ keeps the bits $0$ to $r - 1$ of $W[q]$, which by (P1) are $b[qw], \ldots, b[i-1]$, and line L7 adds their number of 1s. If $r = 0$, the last part is empty and line L7 adds nothing. So line L8 returns the number of 1s in $b[0 \ldots i-1]$. $\square$

**Lemma 4 (SELECT1).** For $1 \le j \le m$, SELECT1$(j)$ returns the position $p$ with $b[p] = 1$ and $\text{rank}_1(p) = j - 1$.

*Proof.* Let $j_0$ be the argument and $c_k$ the number of 1 bits of $W[k]$. By (P1) and (P2), $c_k$ is the number of 1s of $b$ in block $k$, and $\sum_k c_k = m$. We use this invariant of the loop of line L10:

> **(S)** $1 \le j$ and $j_0 = j + \sum_{k' < k} c_{k'}$.

It holds at the start with $k = 0$ and $j = j_0 \ge 1$. An iteration runs only if $c_k < j$, and it sets $j \leftarrow j - c_k \ge 1$ and $k \leftarrow k + 1$, so (S) holds again. The loop stops: if it reached $k = \lceil n/w \rceil$, then (S) would give $j_0 = j + m > m$, against $j_0 \le m$. So the loop stops at a word $W[k]$ with $c_k \ge j$, and $k$ grows by one in each iteration, so at most $\lceil n/w \rceil$ iterations run. By (S), exactly $j_0 - j$ ones of $b$ lie before block $k$, so the wanted 1 is the $j$-th 1 of $W[k]$, counted from the least significant bit.

For $x \ne 0$, the word $x \wedge (x - 1)$ is $x$ with its lowest 1 bit cleared: if the lowest 1 is at bit $t$, then $x - 1$ has bits $0$ to $t - 1$ set, bit $t$ cleared and the higher bits of $x$, so the AND keeps the higher bits and clears bits $0$ to $t$. Line L12 does this $j - 1$ times on $x = W[k]$, which has $c_k \ge j$ ones, so it removes the $j - 1$ lowest ones and $x \ne 0$ after it. The lowest 1 of the new $x$ is the $j$-th 1 of $W[k]$, at bit $t = $ LOWEST$(x)$. Line L13 returns $p = kw + t$. By (P1) $b[p] = 1$, and the 1s before $p$ are the $j_0 - j$ ones before block $k$ and the $j - 1$ ones of $W[k]$ below bit $t$, so $\text{rank}_1(p) = j_0 - 1$. $\square$

**Lemma 5 (rank and select of 0s).** $\text{rank}_0(i) = i - \text{rank}_1(i)$, and SELECT0 is correct when it runs SELECT1 on the words $\neg W[k]$, with the last word masked to its first $n - w(\lceil n/w \rceil - 1)$ bits.

*Proof.* Each position $p < i$ holds a 0 or a 1, so the two counts add to $i$. For select, the masked complemented words satisfy (P1) and (P2) for the bit sequence $1 - b[0], \ldots, 1 - b[n-1]$: the complement flips each bit, and the mask clears exactly the padding bits, which the complement had set. Lemma 4 applied to that sequence gives the position of the $j$-th 0 of $b$. $\blacksquare$
