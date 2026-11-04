---
tag: V7MR79
kind: definition
slug: universal-hash-family
name: Universal hash family
aliases:
- 2-universal family
- Carter-Wegman family
- universal family
- universal hashing family
area: data-structures/hashing
level: core
summary: Family of hash functions where any two distinct keys collide with probability at most 1/m.
prereqs: [hash-function, probability-space]
see_also: [universal-hashing, pairwise-independence, k-wise-independent-hashing, multiplicative-hashing, tabulation-hashing, universal-string-hashing, uniform-hashing-assumption, perfect-hash-function]
sources:
  - paper: doi:10.1016/0022-0000(79)90044-8
    title: J. Lawrence Carter and Mark N. Wegman, Universal classes of hash functions, Journal of Computer and System Sciences 18(2), 1979
    locator: pages 143 to 154 (the definition of a universal class and the first constructions)
  - paper: doi:10.1016/0022-0000(81)90033-7
    title: Mark N. Wegman and J. Lawrence Carter, New hash functions and their use in authentication and set equality, Journal of Computer and System Sciences 22(3), 1981
    locator: pages 265 to 279 (strongly universal classes)
  - book: isbn:9780262046305
    title: Cormen, Leiserson, Rivest and Stein, Introduction to Algorithms, fourth edition
    locator: Section 11.3 (Hash functions), the parts on universal families and on designing a universal family
  - book: isbn:9781107154889
    title: Michael Mitzenmacher and Eli Upfal, Probability and Computing, second edition
    locator: Section 15.3 (Universal Families of Hash Functions), with 15.3.1 (a 2-universal family) and 15.3.2 (a strongly 2-universal family)
---

A universal hash family is a set $\mathcal{H}$ of [hash functions](/hash-function/) from a universe $U$ to $m$ slots such that, for each two distinct keys, at most a $1/m$ share of the functions in $\mathcal{H}$ maps both keys to the same slot. So a function drawn uniformly from $\mathcal{H}$ makes two fixed keys collide with probability at most $1/m$, the same as a fully random function. Carter and Wegman defined these families in 1977, and they are the base of [universal hashing](/universal-hashing/). The best known example is $h_{a,b}(x) = ((ax + b) \bmod p) \bmod m$ for a prime $p$.

## Definition

Let $U$ be a finite set, the universe of keys, let $m \ge 1$ be an integer, and write $[m] = \{0, 1, \dots, m-1\}$. Let $\mathcal{H}$ be a finite nonempty multiset of functions $h : U \to [m]$, and let $h$ be drawn uniformly at random from $\mathcal{H}$.

**Universal.** $\mathcal{H}$ is *universal* when

$$\forall x, y \in U,\ x \ne y: \quad \Pr_{h \in \mathcal{H}}[h(x) = h(y)] \le \frac{1}{m},$$

that is, $|\{h \in \mathcal{H} : h(x) = h(y)\}| \le |\mathcal{H}|/m$ for each pair. Carter and Wegman call this property universal$_2$, and some books call it 2-universal.

**Almost universal.** For a real $\varepsilon > 0$, $\mathcal{H}$ is *$\varepsilon$-almost universal* when $\Pr[h(x) = h(y)] \le \varepsilon$ for all $x \ne y$. For a constant $c \ge 1$, $\mathcal{H}$ is *$c$-approximately universal* when it is $c/m$-almost universal. A universal family is the case $\varepsilon = 1/m$.

**Strongly universal.** $\mathcal{H}$ is *strongly universal* (or *pairwise independent*, or *2-wise independent*) when

$$\forall x, y \in U,\ x \ne y,\ \forall u, v \in [m]: \quad \Pr_{h \in \mathcal{H}}[h(x) = u \wedge h(y) = v] = \frac{1}{m^2}.$$

Wegman and Carter defined this property in 1981. It says that the pair $(h(x), h(y))$ is uniform on $[m]^2$, so each single value $h(x)$ is uniform on $[m]$ and the two values are [independent](/pairwise-independence/). A strongly universal family is universal: sum the condition over the $m$ pairs with $u = v$ to get $\Pr[h(x) = h(y)] = m \cdot 1/m^2 = 1/m$. The converse is false (see the non-examples).

**The bound $1/m$ is almost the best.** Let $N = |U| > m$. For each fixed $h$, let $n_j = |h^{-1}(j)|$, so $\sum_j n_j = N$. The number of colliding pairs of $h$ is $\sum_j \binom{n_j}{2}$. The function $t \mapsto t(t-1)/2$ is convex, so by Jensen's inequality this sum is at least $m \binom{N/m}{2} = N(N - m)/(2m)$. Average this over $h \in \mathcal{H}$ and divide by the $\binom{N}{2}$ pairs: the mean collision probability of a pair is at least $(N - m)/(m(N-1))$. So some pair collides with probability at least $(N-m)/(m(N-1)) \ge 1/m - 1/N$, and no family is $\varepsilon$-almost universal for $\varepsilon < 1/m - 1/N$.

## Examples and non-examples

### The Carter-Wegman family

Let $p$ be a prime with $U \subseteq \{0, \dots, p-1\}$, let $2 \le m \le p$, and let

$$\mathcal{H}_{p,m} = \{\, h_{a,b} : a \in \{1, \dots, p-1\},\ b \in \{0, \dots, p-1\} \,\}, \qquad h_{a,b}(x) = ((ax + b) \bmod p) \bmod m.$$

**Claim.** $\mathcal{H}_{p,m}$ is universal. It has $p(p-1)$ functions, and each one is stored as the two numbers $a$ and $b$.

*Proof.* Fix keys $x \ne y$ in $\{0, \dots, p-1\}$. For a pair $(a, b)$, let $r = (ax + b) \bmod p$ and $s = (ay + b) \bmod p$. All the arithmetic below is in the field $\mathbb{Z}_p$.

1. $r \ne s$. Indeed $r - s \equiv a(x - y) \pmod p$, and $a \not\equiv 0$ and $x - y \not\equiv 0$, so the product is not 0 because $p$ is prime.
2. The map $(a, b) \mapsto (r, s)$ is a bijection from $\{1, \dots, p-1\} \times \mathbb{Z}_p$ onto the set of pairs $(r, s) \in \mathbb{Z}_p^2$ with $r \ne s$. Given such $(r, s)$, the only solution is $a = (r - s)(x - y)^{-1}$ and $b = r - ax$, and $a \ne 0$ because $r \ne s$. Both sets have $p(p-1)$ elements.
3. So when $(a, b)$ is uniform, $(r, s)$ is uniform over the $p(p-1)$ pairs with $r \ne s$. The keys collide exactly when $r \equiv s \pmod m$.
4. Fix $r$. The values $s \in \{0, \dots, p-1\}$ with $s \equiv r \pmod m$ number at most $\lceil p/m \rceil$, and one of them is $r$ itself. So at most $\lceil p/m \rceil - 1 \le (p + m - 1)/m - 1 = (p-1)/m$ values $s \ne r$ give a collision.
5. Summing over the $p$ values of $r$, at most $p(p-1)/m$ of the $p(p-1)$ pairs give a collision. So $\Pr[h_{a,b}(x) = h_{a,b}(y)] \le 1/m$. $\square$

For $p = 17$ and $m = 6$, the function $h_{3,4}$ maps the key 8 to $((3 \cdot 8 + 4) \bmod 17) \bmod 6 = 11 \bmod 6 = 5$. Over all $16 \cdot 17 = 272$ functions, the pair of keys that collides most often collides with probability $2/17 \approx 0.118$, which is below $1/6 \approx 0.167$.

### Other universal families

- **All functions.** The family of all $m^{|U|}$ functions $U \to [m]$ is strongly universal, so it is universal. It is useless in practice: one function takes $|U| \lg m$ bits to store.
- **Linear modulo a prime, strongly universal.** For a prime $p$, the family $\{x \mapsto (ax + b) \bmod p : a, b \in \mathbb{Z}_p\}$ from $\mathbb{Z}_p$ to $\mathbb{Z}_p$ is strongly universal. For $x \ne y$ and targets $u, v$, the system $ax + b = u$, $ay + b = v$ has exactly one solution $(a, b)$, because its determinant $x - y$ is not 0 in $\mathbb{Z}_p$. So each pair $(u, v)$ has probability $1/p^2$. Here $a = 0$ is allowed and $m = p$.
- **Dot product modulo a prime.** Let $m$ be a prime, let the keys be vectors $x = (x_0, \dots, x_{r-1})$ with $0 \le x_i < m$, and let $h_a(x) = \big(\sum_i a_i x_i\big) \bmod m$ for $a$ uniform in $\mathbb{Z}_m^r$. For $x \ne y$, pick $i$ with $x_i \ne y_i$. For each fixed choice of the other coordinates of $a$, the collision is the equation $a_i (x_i - y_i) \equiv c \pmod m$ for a fixed $c$, and it has exactly one solution $a_i$. So the collision probability is exactly $1/m$. For $m = 3$ and $r = 2$, each pair of the 9 keys collides under exactly 3 of the 9 functions.
- **Multiply-shift.** The family $h_a(x) = (ax \bmod 2^w) \gg (w - \ell)$ with $a$ odd is 2-approximately universal, with collision probability at most $2/m$ for $m = 2^\ell$. It is not universal: for $w = 8$ and $\ell = 3$, the keys 1 and 9 collide for 32 of the 128 odd values of $a$, with probability $1/4 = 2/m$. The proof is on the page of [multiplicative hashing](/multiplicative-hashing/).
- **Simple tabulation.** [Tabulation hashing](/tabulation-hashing/) is 3-wise independent, so it is strongly universal.

### Non-examples

- **One fixed function.** If $|U| > m$, a fixed function $h$ maps two keys to the same slot by the pigeonhole principle, and that pair collides with probability 1. Each family with a single member is a non-example. This is why a fixed function has bad inputs.
- **The Carter-Wegman family with $a = 0$.** If $a$ ranges over all of $\{0, \dots, p-1\}$ and $m < p$, the $p$ functions with $a = 0$ are constant and make each pair collide. For $p = 17$ and $m = 6$, the worst pair then collides with probability $49/289 \approx 0.170 > 1/6$. The family is not universal.
- **Keys outside $\mathbb{Z}_p$.** On the universe $\{0, \dots, 2p-1\}$, the keys $x$ and $x + p$ have the same value under each $h_{a,b}$, so they collide with probability 1.
- **Low bits of a product.** The family $x \mapsto ax \bmod 2^\ell$ with $a$ random sends both 0 and $2^\ell$ to slot 0 for each $a$. Multiplication moves the information of a key only to the higher bits, so a product must be cut from the top, as multiply-shift does.
- **Universal but not strongly universal.** For $p = 17$ and $m = 6$, the value $(ax + b) \bmod 17$ is uniform on the 17 residues, and five slots get three residues each, while slot 5 gets only the two residues 5 and 11. So $\Pr[h_{a,b}(x) = 5] = 2/17 \ne 1/6$, and $\mathcal{H}_{17,6}$ is not strongly universal.
- **Strongly universal but not 3-wise independent.** In the family $(ax + b) \bmod p$, the values at two keys determine $a$ and $b$, and so the value at each third key. The triple of values is not uniform on $\mathbb{Z}_p^3$.

## Related definitions

- [Universal hashing](/universal-hashing/) is the technique that draws a function from a universal family, with the analysis of chaining and of collision counts.
- [Pairwise independence](/pairwise-independence/) is the property of random variables that strong universality asks of the values $h(x)$. [$k$-wise independent hashing](/k-wise-independent-hashing/) asks it of each $k$ keys.
- The [universal hashing lemma](/universal-hashing-lemma/) states the bound on the expected chain length that a universal family gives.
- The [uniform hashing assumption](/uniform-hashing-assumption/) is the stronger modelling assumption that $h$ is a fully random function.
- A [perfect hash function](/perfect-hash-function/) has no collision at all on one fixed set. A universal family into $n^2$ slots contains many such functions for each set of $n$ keys.
- A [locality-sensitive hash family](/locality-sensitive-hash-family/) asks the reverse: close keys should collide with high probability.
- [Universal string hashing](/universal-string-hashing/) gives almost universal families for strings of any length.

## References
