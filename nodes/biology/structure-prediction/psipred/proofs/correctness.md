---
title: The block-wise forward pass equals the network on the full window vector
proves: [correctness]
status: full
---

We use the names and line numbers of the pseudocode on the page. Correctness here is about the computation, not about the predictions: the weights are given, and we show that WINDOW-NET computes the outputs of the stated network. Nothing is claimed about the accuracy of any set of weights.

**Setting.** The input is $n$ rows $R[0], \ldots, R[n-1]$, each a vector of $f$ real features, and an odd window width $w$ with $c = \lfloor w/2 \rfloor$. For a centre $j$, the full input vector $X_j$ has $w(f + 1)$ entries in $w$ blocks of $f + 1$. Block $o$, for $0 \le o < w$, belongs to the position $p = j + o - c$. If $0 \le p < n$, block $o$ is $R[p]$ followed by a 0. Otherwise it is $f$ zeros followed by a 1, the end flag. The network computes

$$g_j = \sigma(W X_j + b), \qquad \mathrm{out}_j = \sigma(V g_j + c_0),$$

with $\sigma(u) = 1 / (1 + e^{-u})$ applied to each entry, $W$ of size $u \times w(f+1)$, $b$ of length $u$, $V$ of size $3 \times u$ and $c_0$ of length 3.

**Lemma (block sum).** For each $j$, the vector $z$ at the end of the loop of lines L3 to L6 equals $W X_j + b$.

*Proof.* Split the columns of $W$ into the same $w$ blocks as $X_j$, and write $W_o$ for the $u \times (f + 1)$ block $o$, with columns $0, \ldots, f - 1$ for the features and column $f$ for the flag. Then

$$W X_j = \sum_{o=0}^{w-1} W_o \, X_j^{(o)},$$

where $X_j^{(o)}$ is block $o$ of $X_j$, because a matrix times a vector is the sum of its column blocks times the matching parts of the vector. If the position $p$ of block $o$ is on the chain, $X_j^{(o)} = (R[p], 0)$, so $W_o X_j^{(o)}$ is the first $f$ columns of $W_o$ times $R[p]$, which is the term that line L5 adds. If $p$ is off the chain, $X_j^{(o)} = (0, \ldots, 0, 1)$, so $W_o X_j^{(o)}$ is column $f$ of $W_o$, which is the term that line L6 adds. Line L2 starts $z$ at $b$, and the loop visits each $o$ from 0 to $w - 1$ once, so at the end $z = b + \sum_o W_o X_j^{(o)} = W X_j + b$. $\square$

**Theorem.** For each centre $j$, WINDOW-NET returns $\mathrm{out}_j$. PSIPRED returns the stage 2 outputs of the two networks applied in turn to $\sigma$ of the profile, and the state of the largest stage 2 output at each position.

*Proof.* By the lemma, line L7 sets $g = \sigma(W X_j + b) = g_j$, and line L8 sets $\mathrm{out}[j] = \sigma(V g_j + c_0) = \mathrm{out}_j$. The loop of line L1 does this for each $j$. Line L10 forms the rows $\sigma(Q[p][a])$ of stage 1, line L11 applies the first network, and line L12 applies the second network to the $n$ rows of 3 outputs from stage 1, so $f = 3$ there. Line L13 takes the largest of the three outputs at each position. $\blacksquare$

The two computations are equal in real arithmetic. In floating point they add the same terms in a different order, so they agree up to rounding; the tests compare them with an absolute tolerance of $10^{-12}$.

**Cost.** For one network, line L5 costs $O(uf)$ and line L6 costs $O(u)$ for each of the $w$ offsets, and line L8 costs $O(3u)$. So one network costs $O(n w f u)$ time and $O(n)$ space for the outputs plus $O(u)$ working space, the same as the full vector product, without building the vector of length $w(f + 1)$.
