---
tag: 1R2HY1
kind: definition
slug: k-wise-independent-hashing
name: k-wise independent hashing
aliases:
- k-independent hash family
area: data-structures/hashing
level: advanced
summary: Hash family where any k keys are mapped independently and uniformly.
prereqs: [hash-function, universal-hash-family]
see_also: [k-independent-hashing, independent-random-variables, universal-hashing, tabulation-hashing, linear-probing, count-sketch, min-wise-independent-hashing, polynomial-interpolation]
sources:
  - paper: doi:10.1016/0022-0000(81)90033-7
    title: Mark N. Wegman and J. Lawrence Carter, New hash functions and their use in authentication and set equality, Journal of Computer and System Sciences 22(3), 1981
    locator: pages 265 to 279 (strongly universal_k classes, and the polynomial construction)
  - paper: doi:10.1016/0022-0000(79)90044-8
    title: J. Lawrence Carter and Mark N. Wegman, Universal classes of hash functions, Journal of Computer and System Sciences 18(2), 1979
    locator: pages 143 to 154 (universal classes, the case k = 2)
  - book: isbn:9781107154889
    title: Michael Mitzenmacher and Eli Upfal, Probability and Computing, second edition
    locator: Chapter 15 (Pairwise independence and universal hash functions)
  - paper: doi:10.1137/070702278
    title: Anna Pagh, Rasmus Pagh and Milan Ružić, Linear probing with constant independence, SIAM Journal on Computing 39(3), 2009
    locator: pages 1107 to 1120 (5-wise independence gives expected O(1) time for linear probing)
  - paper: doi:10.1007/978-3-642-14165-2_60
    title: Mihai Pătraşcu and Mikkel Thorup, On the k-independence required by linear probing and minwise independence, ICALP 2010, LNCS 6198
    locator: pages 715 to 726 (a 4-wise independent family that makes linear probing slow)
  - paper: doi:10.1006/jcss.1997.1545
    title: Noga Alon, Yossi Matias and Mario Szegedy, The space complexity of approximating the frequency moments, Journal of Computer and System Sciences 58(1), 1999
    locator: pages 137 to 147 (the second moment sketch with 4-wise independent signs)
---

A family $\mathcal{H}$ of [hash functions](/hash-function/) is $k$-wise independent when, for a function $h$ drawn at random from $\mathcal{H}$, the hash values of any $k$ distinct keys are independent and uniform over the range. The notion lets an analysis that needs only $k$ keys at a time use the same facts as a fully random function, with a function that takes only $O(k)$ words to store. Wegman and Carter defined it in 1981 as a "strongly universal$_k$" class. For $k = 2$ it is stronger than a [universal family](/universal-hash-family/), and it is the same notion as the [$k$-independent hashing](/k-independent-hashing/) of the randomized algorithms area.

## Definition

Let $U$ be a set of keys, let $m \ge 1$, and write $[m] = \{0, 1, \ldots, m - 1\}$. Let $\mathcal{H}$ be a finite multiset of functions $h : U \to [m]$, and let $h$ be drawn uniformly from $\mathcal{H}$. Let $k \ge 1$ with $k \le |U|$.

**Definition.** $\mathcal{H}$ is **$k$-wise independent** when, for all distinct keys $x_1, \ldots, x_k \in U$ and all values $y_1, \ldots, y_k \in [m]$,

$$\Pr_{h \in \mathcal{H}}\big[h(x_1) = y_1 \wedge h(x_2) = y_2 \wedge \cdots \wedge h(x_k) = y_k\big] = \frac{1}{m^k}.$$

In words, for each fixed $x$ the random variable $h(x)$ is uniform on $[m]$, and the random variables $h(x_1), \ldots, h(x_k)$ for distinct keys are mutually [independent](/independent-random-variables/). The case $k = 2$ is called **pairwise independent** or **strongly universal**.

Three facts follow at once.

- **Smaller $k$.** A $k$-wise independent family is $j$-wise independent for each $1 \le j \le k$. To see it, fix distinct $x_1, \ldots, x_j$, add distinct keys $x_{j+1}, \ldots, x_k$, and sum the equation over the $m^{k-j}$ choices of $y_{j+1}, \ldots, y_k$. This gives $m^{k-j}/m^k = 1/m^j$.
- **Universal.** A pairwise independent family is universal: for $x \ne y$, $\Pr[h(x) = h(y)] = \sum_{z \in [m]} \Pr[h(x) = z \wedge h(y) = z] = m \cdot m^{-2} = 1/m$. The converse is false, as the non-examples show.
- **Size.** If $|U| \ge k$, the family has at least $m^k$ members. Fix distinct $x_1, \ldots, x_k$: each of the $m^k$ tuples $(y_1, \ldots, y_k)$ has positive probability, so some member of $\mathcal{H}$ gives it, and different tuples need different members. So a function of the family needs at least $k \lg m$ bits to name.

**Approximate independence.** Many uses need only an upper bound. A family is **$(c, k)$-independent** when the probability in the definition is at most $c/m^k$ for a constant $c \ge 1$, for all distinct keys and all values. With $c = 1$ and the bound required for all values, the probabilities must sum to 1, so each is exactly $1/m^k$ and the two notions agree.

## Examples and non-examples

**Polynomials over a prime field.** Let $p$ be a prime, $U = [m] = \{0, \ldots, p - 1\}$, and let $\mathcal{H}$ be the $p^k$ polynomials

$$h_{a}(x) = (a_0 + a_1 x + \cdots + a_{k-1} x^{k-1}) \bmod p, \qquad a = (a_0, \ldots, a_{k-1}) \in \{0, \ldots, p - 1\}^k.$$

This family is $k$-wise independent. For distinct $x_1, \ldots, x_k$ and any $y_1, \ldots, y_k$, there is exactly one polynomial of degree less than $k$ over the field $\mathbb{Z}_p$ with $h(x_i) = y_i$ for each $i$, by [polynomial interpolation](/polynomial-interpolation/): the Vandermonde matrix of distinct points is invertible. So exactly one of the $p^k$ choices of $a$ gives the values, and the probability is $1/p^k$. For example, with $p = 5$ and $k = 2$, the only pair $(a_0, a_1)$ with $h(1) = 2$ and $h(3) = 4$ is $(1, 1)$, so the probability is $1/25$. With $p = 5$ and $k = 3$, the 125 polynomials of degree at most 2 give 125 different triples $(h(0), h(1), h(4))$, one for each possible triple.

**Linear functions with $a_1$ allowed to be 0.** The case $k = 2$ above, $h(x) = (a_0 + a_1 x) \bmod p$ with both coefficients uniform in $\{0, \ldots, p - 1\}$, is pairwise independent. It is not 3-wise independent: three values of a line are not free. With $p = 3$, no line has $h(0) = 0$, $h(1) = 0$ and $h(2) = 1$, so this event has probability $0 \ne 1/27$.

**Non-example: the universal family with $a \ne 0$.** The family $h_{a,b}(x) = (a x + b) \bmod p$ with $a \in \{1, \ldots, p - 1\}$ is universal but not pairwise independent. Two distinct keys never collide, because $a(x - y) \not\equiv 0 \pmod p$, so $\Pr[h(1) = h(3)] = 0$ for $p = 5$. A pairwise independent family into $[5]$ has collision probability exactly $1/5$.

**Non-example: reduction mod $m$.** The family $((a x + b) \bmod p) \bmod m$, with $a$ and $b$ uniform in $\{0, \ldots, p - 1\}$ and $1 < m < p$, is not exactly 2-wise independent, because $h(x)$ is not uniform. For $p = 5$ and $m = 2$, the values 0, 2 and 4 of $(ax + b) \bmod 5$ give 0, so $\Pr[h(x) = 0] = 3/5$. It is $(c, 2)$-independent with $c = (\lceil p/m \rceil \, m/p)^2$, which is close to 1 when $p \gg m$; here $c = (6/5)^2 = 1.44$.

**Non-example: multiplicative and simple tabulation hashing.** The [multiply-shift](/multiply-shift-hashing/) family of Dietzfelbinger and others has collision probability at most $2/m$, but it is not pairwise independent: it maps the key 0 to 0 for each choice of the multiplier. [Simple tabulation hashing](/tabulation-hashing/) is 3-wise independent but not 4-wise independent, although Pătraşcu and Thorup showed that it behaves well in many of the uses that need more independence.

**A fully random function** is $k$-wise independent for each $k$. It needs $|U| \lg m$ bits, which is the reason for the families above.

**Why $k$ matters: a variance bound.** Let $X_1, \ldots, X_n$ be indicators of events on distinct keys, each a function of one hash value. If the family is pairwise independent, then $\operatorname{Var}[\sum_i X_i] = \sum_i \operatorname{Var}[X_i]$, because each covariance $E[X_i X_j] - E[X_i] E[X_j]$ with $i \ne j$ is 0 by the independence of $h(x_i)$ and $h(x_j)$. So [Chebyshev's inequality](/chebyshev-inequality/) applies as for fully random hashing. Known thresholds for other uses:

- [Linear probing](/linear-probing/) runs in $O(1)$ expected time for each operation with 5-wise independence (Pagh, Pagh and Ružić). Pătraşcu and Thorup gave a 4-wise independent family for which the expected time is $\Theta(\log n)$.
- The second moment sketch of Alon, Matias and Szegedy, the base of the [count sketch](/count-sketch/), needs 4-wise independent random signs, so that the variance of the estimate is bounded.
- [Universal hashing](/universal-hashing/) for chaining, and the first level of [FKS perfect hashing](/fks-perfect-hashing/), need only a universal family, which is weaker than 2-wise independence.

## Related definitions

- [Universal hash family](/universal-hash-family/): only the collision probability of two keys is bounded by $1/m$. Each pairwise independent family is universal.
- [$k$-independent hashing](/k-independent-hashing/): the same notion, on the page of the randomized algorithms area.
- [Min-wise independent hashing](/min-wise-independent-hashing/): each key of a set is equally likely to have the least hash value. It is used for [MinHash](/minhash/), and $k$-wise independence gives it only approximately.
- [Tabulation hashing](/tabulation-hashing/): a fast family with 3-wise independence and strong extra properties.
- [Uniform hashing assumption](/uniform-hashing-assumption/) and [simple uniform hashing](/simple-uniform-hashing/): idealized models in which the hash function is fully random.
- [Independent random variables](/independent-random-variables/): the probability notion behind the definition.

## References
