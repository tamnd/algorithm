---
title: The BLEU procedure computes the clipped precisions, the brevity penalty and a score in [0, 1]
proves: [correctness]
status: full
---

Fix the maximum order $N \ge 1$ and a corpus of candidates $y^{(1)}, \ldots, y^{(S)}$, each a list of tokens, where candidate $s$ has a non-empty list $R_s$ of references. For a list $x$ of tokens and an $n$-gram $g$ (a tuple of $n$ tokens), $\mathrm{count}_x(g)$ is the number of positions $i$ with $x_i \ldots x_{i+n-1} = g$. The definition of Papineni et al. (2002) is

$$m_n = \sum_s \sum_{g} \min\Bigl(\mathrm{count}_{y^{(s)}}(g),\ \max_{x \in R_s} \mathrm{count}_x(g)\Bigr), \qquad t_n = \sum_s \sum_g \mathrm{count}_{y^{(s)}}(g),$$

with $g$ over all $n$-grams, $p_n = m_n / t_n$, $c = \sum_s |y^{(s)}|$, $r = \sum_s r_s$ where $r_s$ is the length in $R_s$ closest to $|y^{(s)}|$ (the shorter one on a tie), $\mathrm{BP} = 1$ if $c > r$ and $e^{1 - r/c}$ otherwise, and

$$\mathrm{BLEU} = \mathrm{BP} \cdot \exp\Bigl(\frac{1}{N} \sum_{n=1}^{N} \ln p_n\Bigr),$$

taken as 0 when some $m_n = 0$ (the logarithm is $-\infty$ there, and the exponential of $-\infty$ is 0).

**Lemma 1 (the counts).** After the loop of lines L3 to L9, the variables $m_n$, $t_n$, $c$ and $r$ hold the values of the definition.

*Proof.* Lines L1 and L2 set all of them to 0. The loop body for candidate $s$ adds $|y^{(s)}|$ to $c$ (line L4) and $r_s$ to $r$ (line L5). For each $n$, line L8 runs over the distinct $n$-grams $g$ of $y^{(s)}$, so it adds the inner sum of $m_n$ over those $g$. An $n$-gram that does not occur in $y^{(s)}$ has $\mathrm{count}_{y^{(s)}}(g) = 0$ and adds 0 to the definition, so the sum over the distinct $n$-grams of $y^{(s)}$ equals the sum over all $g$. A list of length $\ell$ has exactly $\max(\ell - n + 1, 0)$ positions where an $n$-gram starts, so $\sum_g \mathrm{count}_{y^{(s)}}(g) = \max(|y^{(s)}| - n + 1, 0)$, which line L9 adds to $t_n$. Addition is commutative, so after all candidates every variable holds its sum over $s$. $\square$

**Lemma 2 (the range of a precision).** For each $n$, $0 \le m_n \le t_n$.

*Proof.* Each term of $m_n$ is a minimum of two non-negative integers, so it is at least 0 and at most $\mathrm{count}_{y^{(s)}}(g)$. Summing the upper bound over $g$ and $s$ gives $t_n$. $\square$

**Theorem.** The procedure returns the value $\mathrm{BLEU}$ of the definition, and $0 \le \mathrm{BLEU} \le 1$. The score is 1 exactly when $m_n = t_n > 0$ for every $n$ and $c \ge r$.

*Proof.* By Lemma 1 the variables hold the values of the definition when line L10 runs. If some $m_n = 0$, line L10 returns 0, which is the value of the definition. Otherwise every $m_n \ge 1$, so by Lemma 2 every $t_n \ge 1$, every $p_n$ is in $(0, 1]$, and $c \ge t_1 \ge 1$, so $r / c$ is defined. Line L11 computes BP as defined, and line L12 returns the formula of the definition.

For the range: if line L10 returns, the score is 0. Otherwise each $\ln p_n \le 0$, so the exponential is in $(0, 1]$. If $c > r$ then $\mathrm{BP} = 1$, and if $c \le r$ then $1 - r/c \le 0$ and $\mathrm{BP} = e^{1 - r/c} \in (0, 1]$. The product of two numbers in $(0, 1]$ is in $(0, 1]$.

For the case of equality: the product of two numbers in $(0, 1]$ is 1 only if both are 1. The exponential is 1 only if every $\ln p_n = 0$, that is $m_n = t_n$, and these are positive because line L10 did not return. BP is 1 if $c > r$, and for $c \le r$ it is 1 only if $r / c = 1$, that is $c = r$. Conversely, if $m_n = t_n > 0$ for all $n$ and $c \ge r$, both factors are 1. $\square$

**Remark (sentence order).** The statistics are sums over the candidates, so the score does not depend on the order of the sentences, and the statistics of two parts of a corpus add up to the statistics of the whole. The score itself does not add up: corpus BLEU is in general not the mean of the sentence scores, because the logarithm and the brevity penalty are applied once, to the sums. The tests check both facts.

**Remark (smoothing).** With smoothing method 3 of Chen and Cherry (2014), line L10 does not return. The $k$-th order with $m_n = 0$, counted from $n = 1$, gets $p_n = 1 / (2^k t_n)$. If $t_n \ge 1$ this is in $(0, 1)$, so the range proof above still gives a score in $(0, 1]$. If some $t_n = 0$ (a candidate shorter than $n$ tokens), the implementation returns 0 in both modes.

**Remark (complexity).** For one candidate with $\ell$ tokens and references with $\ell'$ tokens in total, line L8 needs the counts of the $n$-grams of the candidate and of each reference. With a hash table keyed by the $n$-gram, building them takes $O(n (\ell + \ell'))$ expected time, and the clipped sum takes $O(n \ell)$. Summed over $n \le N$ and over the corpus with $L$ tokens in all, this is $O(N^2 L)$ expected time and $O(N L)$ space for one sentence at a time.
