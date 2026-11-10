---
tag: 9PZKQY
kind: definition
slug: k-independent-hashing
name: k-independent hashing
aliases:
- k-wise independent hash family
- k-universal hashing
- k-wise independent hashing
- strongly k-universal hashing
area: randomized/random-hashing
level: advanced
summary: Any k distinct keys receive independent uniform hash values; built from random polynomials over a prime field.
prereqs: [pairwise-independence, polynomial-interpolation, markov-inequality]
see_also: [k-wise-independence, limited-independence, universal-hash-family, linear-probing, tabulation-hashing, cuckoo-hashing-load-threshold, min-wise-independent-hashing, ams-sketch]
sources:
  - paper: doi:10.1016/0022-0000(81)90033-7
    title: Mark N. Wegman and J. Lawrence Carter, New hash functions and their use in authentication and set equality, Journal of Computer and System Sciences 22(3), 265 to 279, 1981
    locator: strongly universal_k classes and the construction by random polynomials over a finite field
  - book: isbn:9781107154889
    title: Michael Mitzenmacher and Eli Upfal, Probability and Computing, second edition, Cambridge University Press, 2017
    locator: Chapter 15, Pairwise Independence and Universal Hash Functions (k-wise independence and constructions over a prime field)
  - paper: doi:10.1137/070702278
    title: Anna Pagh, Rasmus Pagh and Milan Ružić, Linear probing with constant independence, SIAM Journal on Computing 39(3), 1107 to 1120, 2009
    locator: the main theorem (5-wise independence gives constant expected time for linear probing) and the 2-wise lower example with logarithmic cost
  - paper: doi:10.1145/2716317
    title: Mihai Pătrașcu and Mikkel Thorup, On the k-independence required by linear probing and minwise independence, ACM Transactions on Algorithms 12(1), article 8, 2016
    locator: the 4-independent families that make linear probing take logarithmic expected time, and the lower bound for approximate min-wise independence
---

A family of hash functions is $k$-independent when, for a function drawn at random from it, every $k$ distinct keys get hash values that are independent and uniform on the $m$ slots. For $k = 1$ each single value is uniform; $k = 2$ is [pairwise independence](/pairwise-independence/); and as $k$ grows the family looks more and more like a fully random function, while one function still takes only $k$ numbers to store. Wegman and Carter (1981) gave the standard construction: a random polynomial of degree $k - 1$ over a prime field. The parameter $k$ is how the randomized analysis of hashing states its needs: chaining needs $k = 2$, [linear probing](/linear-probing/) needs $k = 5$ (Pagh, Pagh and Ružić 2009, with Pătrașcu and Thorup showing that $k = 4$ is not enough), and moment bounds on the load of a slot need larger $k$. The same notion for general random variables, used to build small sample spaces, is on the page [k-wise independence](/k-wise-independence/).

## Definition

Let $U$ be a universe of keys, $m \ge 1$, $[m] = \{0, \ldots, m-1\}$, and $k \ge 1$. Let $\mathcal{H}$ be a finite nonempty multiset of functions $h : U \to [m]$, and draw $h$ uniformly from $\mathcal{H}$.

**k-independent.** $\mathcal{H}$ is *$k$-independent* (or *$k$-wise independent*, or *strongly $k$-universal*) when for all distinct keys $x_1, \ldots, x_k \in U$ and all values $v_1, \ldots, v_k \in [m]$,
$$\Pr_h\big[h(x_1) = v_1 \wedge \cdots \wedge h(x_k) = v_k\big] = \frac{1}{m^k}.$$
So the vector $(h(x_1), \ldots, h(x_k))$ is uniform on $[m]^k$. A $k$-independent family is $j$-independent for each $j \le k$: sum the condition over the values of the extra keys. (This needs $|U| \ge k$; on smaller universes the condition is about all $|U|$ keys.)

**Approximately k-independent.** $\mathcal{H}$ is *$(c, k)$-independent* when each probability above lies between $1/m^k$ and $c/m^k$, or, in other forms, within a factor $1 \pm \varepsilon$ of $1/m^k$. Reductions modulo $m$ give families of this kind.

**The polynomial construction.** Let $p$ be a prime, $U = \mathbb{Z}_p$, and $1 \le k \le p$. Draw $a_0, \ldots, a_{k-1}$ uniformly and independently from $\mathbb{Z}_p$, and let
$$h_a(x) = \big(a_0 + a_1 x + \cdots + a_{k-1} x^{k-1}\big) \bmod p.$$

**Theorem (Wegman and Carter 1981).** The $p^k$ functions $h_a$ form a $k$-independent family from $\mathbb{Z}_p$ to $\mathbb{Z}_p$.

*Proof.* Fix distinct $x_1, \ldots, x_k \in \mathbb{Z}_p$ and values $v_1, \ldots, v_k \in \mathbb{Z}_p$. The conditions $h_a(x_j) = v_j$ for $j = 1, \ldots, k$ are $k$ linear equations in the unknowns $a_0, \ldots, a_{k-1}$, with the Vandermonde matrix $V = (x_j^{\,i})_{j, i}$. Its determinant is $\prod_{j < j'} (x_{j'} - x_j)$, which is a product of nonzero elements of the field $\mathbb{Z}_p$, so it is not zero. Hence $V$ is invertible, and exactly one vector $a$ satisfies the equations. (This is [Lagrange interpolation](/lagrange-interpolation/): there is exactly one polynomial of degree less than $k$ through $k$ points with distinct abscissae.) So exactly one of the $p^k$ equally likely vectors gives the values $v_1, \ldots, v_k$, and the probability is $1/p^k$. $\blacksquare$

The evaluation takes $k - 1$ multiplications by Horner's rule, and one function is stored in $k$ numbers below $p$, which is $k \lceil \log_2 p \rceil$ bits.

**Fewer slots.** For a table of $m < p$ slots, use $h_a(x) \bmod m$. Each slot receives $\lfloor p/m \rfloor$ or $\lceil p/m \rceil$ residues, so each probability in the definition lies between $(\lfloor p/m \rfloor / p)^k$ and $(\lceil p/m \rceil / p)^k$. With $p \gg km$ the family is close to $k$-independent. For a field of size $2^\ell$, the same polynomials over $\mathrm{GF}(2^\ell)$ give exact $k$-independence with $m = 2^\ell$.

## Examples and non-examples

**Exact check for small primes.** Enumerating all $p^k$ polynomials and all sets of distinct keys confirms the theorem for $(p, k) = (3, 2), (5, 2), (5, 3), (7, 3)$ and $(5, 4)$. In each case the family is also $j$-independent for $j < k$, and it is not $(k + 1)$-independent, as the next example shows.

**Degree k − 1 is not (k + 1)-independent.** The values at $k$ keys determine the polynomial, so they determine the value at every other key. For $k = 3$ and $p = 7$, $a = (2, 5, 3)$ gives $h(x) = 2 + 5x + 3x^2 \bmod 7$, with values $2, 3, 3, 2, 0, 4, 0$ at $x = 0, \ldots, 6$. Any other polynomial of degree at most 2 that agrees with it at $x = 0, 1, 2$ is the same polynomial, so the value at $x = 3$ is fixed by the first three: only $7^3$ of the $7^4$ value vectors at four keys can occur.

**The reduction mod m.** For $p = 7$, $k = 3$ and $m = 3$, slot 0 gets the residues $0, 3, 6$. So $\Pr[h(1) \bmod 3 = 0] = 147/343 = 3/7$, while slots 1 and 2 have $2/7$ each. The family is approximately, not exactly, independent.

**Simple tabulation.** Split a key into $c$ characters and XOR $c$ random tables, one lookup per character. This family is 3-independent but not 4-independent: for keys $(0, 0)$, $(0, 1)$, $(1, 0)$ and $(1, 1)$, the XOR of the four hash values is 0 for every choice of the tables. See [tabulation hashing](/tabulation-hashing/). It still behaves much better than its independence suggests for linear probing and cuckoo hashing.

**Plain multiply-shift.** $h_a(x) = (ax \bmod 2^w) \gg (w - \ell)$ with odd $a$ is not even 1-independent: the key 0 always goes to slot 0. It is only 2-approximately universal. See [multiply-shift hashing](/multiply-shift-hashing/).

**The affine family.** $(ax + b) \bmod p$ with $a, b \in \mathbb{Z}_p$ is the case $k = 2$ of the polynomial construction. If $a = 0$ is excluded, it is universal but no longer 2-independent, since two distinct keys never get the same value.

**What each k buys.** These bounds hold for every fixed set of $n$ keys, with $m \ge n$ slots unless stated:

| independence | guarantee | source |
|---|---|---|
| 2 | expected chain length at most $1 + n/m$ | [chain length bound](/universal-hashing-expected-chain-length/) |
| 2 | expected longest chain $O(\sqrt{n})$ for $m = n$ | second moment of the loads |
| 4 | variance of the AMS estimate of $F_2$ | [AMS sketch](/ams-sketch/) |
| 5 | linear probing in $O(1)$ expected time per operation | Pagh, Pagh and Ružić 2009 |
| 4 is not enough | some 4-independent families give linear probing $\Theta(\log n)$ expected time | Pătrașcu and Thorup 2016 |
| $k$ | longest chain at most $(n/\delta)^{1/k}$, roughly, with probability $1 - \delta$ for $m = n$ | the $k$-th moment, below |
| $O(\log n)$ | the analysis of [cuckoo hashing](/cuckoo-hashing-load-threshold/) by Pagh and Rodler | Pagh and Rodler 2004 |

**A k-th moment bound on the longest chain.** Let $m = n$ and let $h$ be $k$-independent. A set of $k$ keys is *monochromatic* when all its keys share a slot, which happens with probability $m \cdot m^{-k} = m^{1-k}$. So the expected number of monochromatic $k$-sets is $\binom{n}{k} n^{1-k} \le n/k!$. A slot with $t \ge k$ keys holds $\binom{t}{k}$ such sets, so by [Markov's inequality](/markov-inequality/)
$$\Pr[\text{some slot has at least } t \text{ keys}] \le \frac{n / k!}{\binom{t}{k}}.$$
For constant $k$ and large $t$ the right side is about $n/t^k$, so the longest chain is $O(n^{1/k})$ with constant probability. With $k = \Theta(\log n / \log\log n)$, this gives the $O(\log n/\log\log n)$ bound of a fully random function.

## Related definitions

- [Pairwise independence](/pairwise-independence/). The case $k = 2$, with the variance facts that it gives.
- [Universal hash family](/universal-hash-family/). Only the collision probability of pairs is bounded; it is implied by 2-independence.
- [k-wise independence](/k-wise-independence/) and [limited independence](/limited-independence/). The same property for random variables in general, and the small sample spaces of size about $n^{k/2}$ used in derandomization.
- [Min-wise independent hashing](/min-wise-independent-hashing/). Exact min-wise independence needs large families, but $O(\log(1/\varepsilon))$-independence gives $\varepsilon$-approximate min-wise independence (Indyk 2001), and this is tight up to a constant (Pătrașcu and Thorup).
- [Tabulation hashing](/tabulation-hashing/). Fast hashing with only 3-independence but strong guarantees for specific structures.
- [Dot-product hashing](/dot-product-hashing/). Linear in a vector key, 2-independent with an offset, never 3-independent.

## References
