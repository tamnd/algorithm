---
title: Top-k sampling keeps a set of maximum mass and draws from the renormalized distribution
proves: [correctness]
status: full
---

We use the notation of the page. The input is a distribution $p$ over the vocabulary $V = \{0, 1, \ldots, |V| - 1\}$, an integer $k \ge 1$, and a number $u$ drawn uniformly from $[0, 1)$. Let $m = \min(k, |V|)$. We assume exact arithmetic, as with the Fractions of the tests; the last remark treats rounding.

**Lemma 1 (the kept set).** Line L1 sorts the indices by the key $(-p_i, i)$, and line L2 keeps the first $m$ of them. The kept set $K$ has $m$ elements, every kept token has a probability at least as large as every dropped token, and among the tokens with the same probability as the least probable kept token, the kept ones have the smaller indices.

*Proof.* The key $(-p_i, i)$ is distinct for distinct $i$, so the sorted order is unique, whatever sort algorithm runs. A token $i$ comes before a token $j$ exactly when $p_i > p_j$, or $p_i = p_j$ and $i < j$. The first $m$ positions therefore hold tokens whose probabilities are at least the probability of every later token, and on a tie at the boundary the smaller indices come first. $\square$

**Theorem 2 (maximum mass).** Among all sets $S \subseteq V$ with $|S| = m$, the kept set has the largest mass $\sum_{i \in S} p_i$.

*Proof.* Let $S$ be any set of size $m$ with $S \ne K$. Then there are $i \in K \setminus S$ and $j \in S \setminus K$, and $p_i \ge p_j$ by Lemma 1. The set $S' = S \setminus \{j\} \cup \{i\}$ has size $m$, its mass is at least the mass of $S$, and it has one more element in common with $K$. Repeat until the set is $K$. The mass never goes down, so the mass of $K$ is at least the mass of $S$. $\square$

So top-k keeps the $m$ tokens of largest mass. Theorem 2 only says that the set is best for its size; whether $k$ tokens is a good size is a separate question, which [nucleus sampling](/nucleus-sampling/) answers with a mass threshold.

**Theorem 3 (the draw).** Let $Z = \sum_{i \in K} p_i > 0$. TOP-K-SAMPLE returns each $i \in K$ with probability $p_i / Z$, and returns no token outside $K$ and no token with $p_i = 0$.

*Proof.* Write the kept tokens in sorted order as $i_1, \ldots, i_m$, and let $c_0 = 0$ and $c_t = p_{i_1} + \cdots + p_{i_t}$, so $c_m = Z$. Line L4 sets $r = u Z$, which is uniform on $[0, Z)$. The loop of lines L6 to L8 returns $i_t$ for the first $t$ with $r < c_t$. Since the $c_t$ do not decrease and $r < Z = c_m$, such a $t$ exists, and it is the unique $t$ with $c_{t-1} \le r < c_t$. The interval $[c_{t-1}, c_t)$ has length $p_{i_t}$, so the probability of returning $i_t$ is $p_{i_t} / Z$. If $p_{i_t} = 0$, the interval is empty and $i_t$ is never returned. Line L9 is not reached. $\square$

This is inverse transform sampling on the renormalized distribution $q_i = p_i / Z$ for $i \in K$ and $q_i = 0$ otherwise, but with the bound $Z$ moved to the random number: comparing $r = uZ$ with $c_t$ is the same as comparing $u$ with $c_t / Z$, and no division is needed. The tests check Theorem 3 exactly: with $u$ on the grid $j / n$ and Fraction probabilities, the share of grid points that return each token equals $q_i$.

**Corollary 4 (special cases).** With $k = 1$ the kept set is the first index of a largest probability, and the draw returns it with probability 1, which is [greedy decoding](/greedy-decoding/) of one step. With $k \ge |V|$, the kept set is all of $V$, $Z = 1$, and the draw is a sample from $p$ itself.

*Proof.* Both follow from Lemma 1 and Theorem 3. $\square$

**Remark (rounding).** With floats, the sum $Z$ of line L3 and the running sum $c_m$ of line L7 can differ in the last bits, because two ways of adding the same numbers can round differently, and the product $uZ$ of line L4 can round up to $Z$ when $u$ is very close to 1. Then $r$ can be at least $c_m$, and no $t$ has $r < c_t$. Line L9 returns the last kept token of positive probability in that case. The event has probability of the order of the rounding error, and it does not change which tokens can be drawn.
