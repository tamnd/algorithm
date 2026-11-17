---
title: The Hardy-Weinberg exact test computes the null law of the heterozygote count and gives a valid p-value
proves: [correctness]
status: full
---

A sample of $n \ge 1$ diploid individuals at a biallelic locus has genotype counts $n_{AA}$, $n_{Aa}$ and $n_{aa}$. Let $n_A = 2n_{AA} + n_{Aa}$ and $n_a = 2n - n_A$ be the allele counts, and let $m = \min(n_A, n_a)$ be the count of the minor allele. Write $h$ for a possible heterozygote count. Given the allele counts, the counts of the two homozygotes are fixed by $h$: $r(h) = (m - h)/2$ minor homozygotes and $c(h) = n - h - r(h)$ common homozygotes. A value $h$ is *possible* when $0 \le h \le m$ and $h \equiv m \pmod 2$; then $r(h)$ and $c(h)$ are integers, $r(h) \ge 0$, and $c(h) = n - (m + h)/2 \ge n - m \ge 0$ because $m \le n$.

## 1. The null law (Levene 1949)

**Lemma 1.** Suppose the $n$ genotypes are independent draws with probabilities $p^2$, $2pq$ and $q^2$ (Hardy-Weinberg proportions). Then, given $n_A$, the probability of $h$ heterozygotes is

$$P(h) = \frac{n!\; n_A!\; n_a!\; 2^h}{r!\; h!\; c!\; (2n)!} \quad\text{with } r, c \text{ the homozygote counts of } h,$$

taken over the possible values of $h$, and it does not depend on $p$.

*Proof.* Say that $A$ is the minor allele, so $r$ counts $AA$ and $c$ counts $aa$; the other case is the same with the names swapped. The genotype counts are multinomial, so

$$\Pr(r, h, c) = \frac{n!}{r!\, h!\, c!}\, (p^2)^r (2pq)^h (q^2)^c = \frac{n!\, 2^h}{r!\, h!\, c!}\, p^{n_A} q^{n_a},$$

because $2r + h = n_A$ and $2c + h = n_a$. Each of the $2n$ copies is $A$ with probability $p$, independently, so $n_A \sim \text{Binomial}(2n, p)$ and $\Pr(n_A) = \binom{2n}{n_A} p^{n_A} q^{n_a}$. Dividing, the factor $p^{n_A} q^{n_a}$ cancels:

$$\Pr(h \mid n_A) = \frac{n!\, 2^h}{r!\, h!\, c!} \cdot \frac{n_A!\, n_a!}{(2n)!}.$$

So $n_A$ is a sufficient statistic for $p$, and the conditional law is free of the nuisance parameter. $\square$

The same law has a counting form, which the tests use as an independent check. Put the $2n$ copies in slots $0, \ldots, 2n - 1$, where individual $i$ holds slots $2i$ and $2i + 1$. Under the null, given $n_A$, every set of $n_A$ slots for the $A$ copies is equally likely, so each of the $\binom{2n}{n_A}$ placements has probability $1/\binom{2n}{n_A}$. A placement with $h$ heterozygotes is fixed by choosing which individuals are $AA$, $Aa$ and $aa$, in $n!/(r!\,h!\,c!)$ ways, and which slot of each heterozygote holds the $A$, in $2^h$ ways. This gives the same $P(h)$.

## 2. The ratios of neighbouring terms

**Lemma 2.** For possible values $h$ and $h - 2$,

$$\frac{P(h-2)}{P(h)} = \frac{h(h-1)}{4\,(r+1)(c+1)}, \qquad \frac{P(h+2)}{P(h)} = \frac{4\,r\,c}{(h+1)(h+2)},$$

where $r = r(h)$ and $c = c(h)$, and the second form holds when $h + 2$ is possible.

*Proof.* Moving from $h$ to $h - 2$ turns one heterozygote pair into one more homozygote of each kind: $r(h - 2) = r + 1$ and $c(h - 2) = c + 1$. In the ratio of the two closed forms the factors $n!\, n_A!\, n_a! / (2n)!$ cancel, and what is left is

$$\frac{2^{h-2}}{(r+1)!\,(h-2)!\,(c+1)!} \cdot \frac{r!\, h!\, c!}{2^h} = \frac{h(h-1)}{4 (r+1)(c+1)}.$$

The second ratio is the same identity read from $h$ to $h + 2$, where $r(h + 2) = r - 1$ and $c(h + 2) = c - 1$. $\square$

All these ratios are positive on the possible values. For $h \ge 2$, $h(h - 1) > 0$. For $h \le m - 2$, $r = (m - h)/2 \ge 1$ and $c = n - (m + h)/2 \ge n - m + 1 \ge 1$. So no weight is zero and no denominator is zero.

## 3. The algorithm returns $P$

Lines L1 and L2 compute $n$, $m$ and a start value $h_0$ with $h_0 \equiv m \pmod 2$ and $0 \le h_0 \le m$: the floor of $m(2n - m)/(2n)$ lies in $[0, m]$, and it is raised by 1 only when its parity differs from that of $m$, in which case it was below $m$.

**Claim.** After lines L3 to L5, $w[h] = P(h)/P(h_0)$ for every possible $h$, and $w$ has no other keys.

*Proof.* Line L3 sets $w[h_0] = 1 = P(h_0)/P(h_0)$. The loop of line L4 visits $h = h_0, h_0 - 2, \ldots$ while $h \ge 2$ and sets $w[h-2] = w[h] \cdot P(h-2)/P(h)$ by Lemma 2, so by induction on the number of steps $w[h - 2] = P(h - 2)/P(h_0)$. It stops at the least value with the parity of $m$, which is 0 or 1, the least possible value. The loop of line L5 does the same upward with the second ratio of Lemma 2 and stops at $h = m$, the largest possible value. Both loops move in steps of 2 from a value with the parity of $m$, so they visit exactly the possible values. $\square$

Line L6 divides by $\sum_h w[h] = \sum_h P(h)/P(h_0) = 1/P(h_0)$, because $P$ is a probability law on the possible values. So the returned map is $P$.

## 4. The p-value is valid

For an observed count $h$, line L7 returns

$$\pi(h) = \sum_{h' :\, P(h') \le P(h)} P(h').$$

**Theorem.** Under the null hypothesis, for every $\alpha \in [0, 1]$, $\Pr(\pi(H) \le \alpha \mid n_A) \le \alpha$. Hence also $\Pr(\pi(H) \le \alpha) \le \alpha$ without the conditioning.

*Proof.* If $P(h_1) > P(h_2)$, then the set summed for $\pi(h_1)$ contains the set for $\pi(h_2)$ and also $h_1$, so $\pi(h_1) \ge \pi(h_2) + P(h_1) > \pi(h_2)$. Let $S = \{h : \pi(h) \le \alpha\}$. If $S$ is empty there is nothing to prove. Otherwise pick $h^* \in S$ with the largest $P(h^*)$. Every $h \in S$ has $P(h) \le P(h^*)$, so $S \subseteq \{h : P(h) \le P(h^*)\}$ and

$$\Pr(H \in S \mid n_A) \le \sum_{h :\, P(h) \le P(h^*)} P(h) = \pi(h^*) \le \alpha.$$

The bound holds for every value of $n_A$, so it holds after averaging over $n_A$. $\square$

The one-sided p-values $\Pr(H \le h)$ and $\Pr(H \ge h)$ are valid by the same argument with the order of $h$ in place of the order of $P(h)$. They overlap in the term $P(h)$, so their sum is $1 + P(h)$.

## 5. Where the start value comes from

By Lemma 2 the ratio $P(h+2)/P(h) = 4 r c / ((h+1)(h+2))$ decreases strictly in $h$: the numerator decreases because $r$ and $c$ both drop by 1, and the denominator increases. So $P$ rises and then falls on the possible values; it is unimodal. Setting the continuous form of the ratio to 1, $(m - h)(2n - m - h) = h^2$, gives $h = m(2n - m)/(2n)$, the expected heterozygote count $2n \hat p \hat q$ in large samples. Starting there keeps the floating weights near 1 at the mode and below 1 elsewhere, so they do not overflow; far tails may underflow to 0, which changes the p-value by less than the rounding error. The exact form of the start value does not matter for correctness, which Section 3 proves for any possible $h_0$.

## 6. Rounding

With floats, each weight is a product of at most $m/2$ ratios, each computed with a few roundings, so its relative error is $O(m \varepsilon)$ for the unit roundoff $\varepsilon$. Two values of $h$ can have equal true probabilities (for $n = 6$ and $n_A = 4$, both $h = 2$ and $h = 4$ have probability $16/33$), and rounding can then put one of them on the wrong side of the comparison in line L7. The implementation compares with a relative tolerance of $10^{-9}$; with `exact=True` it uses fractions, and the comparison is exact.
