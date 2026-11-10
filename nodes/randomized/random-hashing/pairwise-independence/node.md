---
tag: RX9P50
kind: definition
slug: pairwise-independence
name: Pairwise independence
aliases:
- 2-wise independence
- strong universality
- pairwise independent hash family
- strongly universal hash family
area: randomized/random-hashing
level: core
summary: Hash values of any two distinct keys are independent and uniform over the table.
prereqs: [independent-events, random-variable, hash-function]
see_also: [universal-hash-family, k-independent-hashing, k-wise-independence, limited-independence, chebyshev-inequality, dot-product-hashing, multiply-shift-hashing, universal-hashing-expected-chain-length]
sources:
  - paper: doi:10.1016/0022-0000(81)90033-7
    title: Mark N. Wegman and J. Lawrence Carter, New hash functions and their use in authentication and set equality, Journal of Computer and System Sciences 22(3), 265 to 279, 1981
    locator: the definition of strongly universal classes and the affine construction over a finite field
  - paper: doi:10.1561/0400000009
    title: Michael Luby and Avi Wigderson, Pairwise independence and derandomization, Foundations and Trends in Theoretical Computer Science 1(4), 237 to 301, 2005
    locator: Chapter 1, Pairwise Independence (definitions, the constructions over a field and from linear maps over GF(2), and the use of Chebyshev's inequality)
  - book: isbn:9781107154889
    title: Michael Mitzenmacher and Eli Upfal, Probability and Computing, second edition, Cambridge University Press, 2017
    locator: Chapter 15, Pairwise Independence and Universal Hash Functions (pairwise independent variables, Chebyshev for pairwise independent sums, Section 15.3 on strongly 2-universal families)
---

Pairwise independence is the property that makes a random hash function behave, on each two keys, exactly like a fully random function. A family $\mathcal{H}$ of functions from a universe $U$ to $[m] = \{0, \ldots, m-1\}$ is pairwise independent, or strongly universal, when for each two distinct keys the pair of hash values is uniform on $[m]^2$ over a uniform choice of $h \in \mathcal{H}$. Wegman and Carter defined it in 1981. It is stronger than [universality](/universal-hash-family/), which only bounds the collision probability, and it is the case $k = 2$ of [k-independent hashing](/k-independent-hashing/). In the randomized analysis of an algorithm, it is exactly what is needed to compute variances of sums of indicator variables, so it turns [Chebyshev's inequality](/chebyshev-inequality/) into a tool that needs only $O(\log |U|)$ random bits. The view of the same notion as a small sample space for derandomization is on the page [k-wise independence](/k-wise-independence/).

## Definition

**Pairwise independent random variables.** Random variables $X_1, \ldots, X_n$ on one probability space are *pairwise independent* when, for each $i \ne j$ and all values $s, t$,
$$\Pr[X_i = s \wedge X_j = t] = \Pr[X_i = s] \cdot \Pr[X_j = t].$$
This asks nothing about three or more variables at once. *Mutual independence* asks the product rule for every subset.

**Pairwise independent hash family.** Let $\mathcal{H}$ be a finite nonempty multiset of functions $h : U \to [m]$, and draw $h$ uniformly from $\mathcal{H}$. The family is *pairwise independent* (also *strongly universal*, *strongly 2-universal* or *2-wise independent*) when
$$\forall x \ne y \in U,\ \forall s, t \in [m]: \qquad \Pr_h[h(x) = s \wedge h(y) = t] = \frac{1}{m^2}.$$
Equivalently, each value $h(x)$ is uniform on $[m]$, and the variables $\{h(x)\}_{x \in U}$ are pairwise independent. In terms of counts, exactly $|\mathcal{H}|/m^2$ functions send $x$ to $s$ and $y$ to $t$, so $m^2$ divides $|\mathcal{H}|$.

**Three facts used everywhere.**

1. *It implies universality.* Summing over the $m$ pairs with $s = t$ gives $\Pr[h(x) = h(y)] = m \cdot \frac{1}{m^2} = \frac{1}{m}$, so the [expected chain length bound](/universal-hashing-expected-chain-length/) holds.
2. *Variances add.* If $X_1, \ldots, X_n$ are pairwise independent with finite variances, then $\operatorname{Var}\big[\sum_i X_i\big] = \sum_i \operatorname{Var}[X_i]$, because every covariance $E[X_i X_j] - E[X_i]E[X_j]$ with $i \ne j$ is zero, and the variance of a sum is the sum of the variances plus the sum of the covariances.
3. *Chebyshev applies.* So for a sum $X$ of pairwise independent indicators with mean $\mu$, $\operatorname{Var}[X] \le \mu$ and $\Pr[|X - \mu| \ge \lambda] \le \mu/\lambda^2$. Chernoff bounds, which need mutual independence, do not apply.

**Approximate forms.** A family is *$c$-approximately strongly universal* when each pair of values has probability at most $c/m^2$. Universal families that are not strongly universal, such as plain [multiply-shift](/multiply-shift-hashing/), give the collision bound but not uniform single values.

## Examples and non-examples

**The affine family over a prime field.** For a prime $p$, the $p^2$ functions $h_{a,b}(x) = (ax + b) \bmod p$ with $a, b \in \{0, \ldots, p-1\}$ form a pairwise independent family from $\mathbb{Z}_p$ to $\mathbb{Z}_p$. For $x \ne y$ and targets $s, t$, the system $ax + b = s$, $ay + b = t$ has exactly one solution $a = (s - t)(x - y)^{-1}$, $b = s - ax$, so each pair of values comes from exactly one of the $p^2$ functions. The same proof works over any finite field, for example $\mathrm{GF}(2^\ell)$ with $m = 2^\ell$.

*Exact numbers for $p = 5$.* Let $X$ be the number of keys of $\mathbb{Z}_5$ that land in slot 0. Over the 25 functions, $X = 1$ for the 20 functions with $a \ne 0$, $X = 5$ for $a = 0, b = 0$, and $X = 0$ for the 4 functions with $a = 0, b \ne 0$. So $E[X] = 1$ and $\operatorname{Var}[X] = 9/5 - 1 = 4/5$, which is $5 \cdot \frac{1}{5} \cdot \frac{4}{5}$, the sum of the five variances, as fact 2 says.

**The affine dot product.** For keys in $\mathbb{Z}_p^r$, $h_{a,b}(x) = (a \cdot x + b) \bmod p$ with $a \in \mathbb{Z}_p^r$ and $b \in \mathbb{Z}_p$ is pairwise independent. See [dot-product hashing](/dot-product-hashing/).

**Strong multiply-shift.** For $w$-bit keys and $m = 2^\ell$, pick $\bar w \ge w + \ell - 1$ and $a, b$ uniform in $\{0, \ldots, 2^{\bar w} - 1\}$, and return the bits $\bar w - \ell$ to $\bar w - 1$ of $ax + b$. Dietzfelbinger (1996) proved this family pairwise independent. It needs no prime and no division. See [multiply-shift hashing](/multiply-shift-hashing/).

**Bits from parities.** Draw $k$ independent fair bits $t = (t_1, \ldots, t_k)$. For each nonempty subset $S \subseteq \{1, \ldots, k\}$, let $X_S = \bigoplus_{i \in S} t_i$. The $2^k - 1$ bits $X_S$ are uniform and pairwise independent: for $S \ne T$, the vectors of $S$ and $T$ are linearly independent over GF(2), so $(X_S, X_T)$ is uniform on $\{0, 1\}^2$. So $k$ random bits give $2^k - 1$ pairwise independent bits.

*Exact numbers for $k = 3$.* The 7 bits each have mean $1/2$, and their sum $X$ has $\operatorname{Var}[X] = 7 \cdot \frac{1}{4} = \frac{7}{4}$, as for 7 independent bits. But the sum is $0$ with probability $1/8$ (when $t = 000$) and $4$ with probability $7/8$. It is never $1, 2, 3, 5, 6$ or $7$. Pairwise independence controls the variance and nothing more.

**Non-example: pairwise but not 3-wise.** In the parity example, $X_{\{1\}}$, $X_{\{2\}}$ and $X_{\{1,2\}}$ are pairwise independent, but the third is the XOR of the first two. In the affine family modulo $p$, the values at $0$, $1$ and $2$ are $b$, $a + b$ and $2a + b$, and the third equals $2h(1) - h(0)$. Only $25$ of the $125$ triples occur for $p = 5$.

**Non-example: universal but not pairwise independent.** The Carter-Wegman family $((ax + b) \bmod p) \bmod m$ with $a \ne 0$ never maps two distinct keys of $\mathbb{Z}_p$ to the same value before the reduction mod $m$, so for $m = p$ the pair $(s, s)$ has probability 0. With $m < p$ and $m$ not dividing $p$, the single values are not even uniform: for $p = 7$ and $m = 3$, slot 0 gets the residues $0, 3, 6$ and has probability $3/7$, not $1/3$. Thorup notes that the reduction mod $m$ keeps the family 2-approximately strongly universal.

**Non-example: linear maps without an offset.** $h_a(x) = a \cdot x \bmod p$ is universal, but $h_a(0) = 0$ for every $a$. Plain multiply-shift has the same flaw.

**The family of all functions.** The $m^{|U|}$ functions from $U$ to $[m]$ are fully independent, so pairwise independent. One function needs $|U| \log_2 m$ bits, against $2 \log_2 p$ bits for the affine family.

## Related definitions

- [Universal hash family](/universal-hash-family/). The weaker property $\Pr[h(x) = h(y)] \le 1/m$. Pairwise independence implies it.
- [k-independent hashing](/k-independent-hashing/). Every $k$ distinct keys get independent uniform values. Pairwise independence is $k = 2$, and random polynomials of degree $k - 1$ over a prime field give it for each $k$.
- [k-wise independence](/k-wise-independence/) and [limited independence](/limited-independence/). The same property for random variables in general, and its use to replace full randomness by small sample spaces in [derandomization](/method-of-conditional-expectations/).
- [Min-wise independent hashing](/min-wise-independent-hashing/). A different property, about which key of a set gets the least value. Pairwise independence does not give it.
- [Leftover hash lemma](/leftover-hash-lemma/). Universal and pairwise independent families extract nearly uniform bits from weak sources.
- [Count-Sketch](/count-sketch/) and the [AMS sketch](/ams-sketch/). Streaming sketches whose variance analysis needs pairwise or 4-wise independent hash and sign functions.

## References
