---
tag: 4KEFV4
kind: algorithm
slug: small-bias-generator
name: Small-bias generator
aliases:
- AGHP construction
- Alon-Goldreich-Haastad-Peralta generator
- powering construction
- epsilon-biased generator
area: randomized/derandomization
level: advanced
summary: Constructs an epsilon-biased sample space with seed length logarithmic in the output length and 1/epsilon.
model: word-ram
complexity:
  vars: {n: the output length, m: the degree of the field GF(2^m)}
  time: {worst: Θ(n m), average: Θ(n m), best: Θ(n m)}
  space: {extra: Θ(1)}
properties: {deterministic: true, exact: true, online: true, recursive: false}
history:
  year: 1992
  people: [Noga Alon, Oded Goldreich, Johan Håstad, René Peralta]
  note: "Alon, Goldreich, Håstad and Peralta gave the powering, LFSR and quadratic character constructions of small-bias spaces, after the first construction of Naor and Naor in 1990."
prereqs: [small-bias-sample-space, irreducible-polynomial, k-wise-independence]
see_also: [pseudorandom-generator, linear-feedback-shift-register, hadamard-code, reed-solomon-code, linear-code, sample-space-reduction, expander-walk-sampler]
sources:
  - paper: doi:10.1002/rsa.3240030308
    title: Noga Alon, Oded Goldreich, Johan Håstad and René Peralta, Simple constructions of almost k-wise independent random variables, Random Structures and Algorithms 3(3), 1992
    locator: pages 289 to 304 (the powering construction and its bias bound, the LFSR and quadratic character constructions)
  - paper: doi:10.1137/0222053
    title: Joseph Naor and Moni Naor, Small-bias probability spaces, efficient constructions and applications, SIAM Journal on Computing 22(4), 1993 (STOC 1990)
    locator: pages 838 to 856 (the first construction with seed length O(log n + log(1/epsilon)))
  - paper: doi:10.1145/3055399.3055408
    title: Amnon Ta-Shma, Explicit, almost optimal, epsilon-balanced codes, STOC 2017
    locator: pages 238 to 251 (a construction with seed length log n + (2 + o(1)) log(1/epsilon))
---

A small-bias generator stretches a short random seed into $n$ bits whose every nonempty parity has bias at most $\varepsilon$, so its outputs form a [small-bias sample space](/small-bias-sample-space/). The powering construction of Alon, Goldreich, Håstad and Peralta (1992) uses a seed $(x, y)$ of two elements of the field $\mathrm{GF}(2^m)$ and outputs the bits $\langle x^i, y \rangle$ for $i = 0, \ldots, n - 1$. Its bias is at most $(n-1)/2^m$, so the seed length is $2\lceil \log_2((n-1)/\varepsilon) \rceil = O(\log n + \log(1/\varepsilon))$. Each output bit costs one field multiplication and one parity.

## In plain words

You want many coin flips, but you can afford only a few truly random ones. The flips do not need to be independent; they only need to pass one kind of test: the XOR of any group of them must be close to a fair coin.

Pick two random numbers $x$ and $y$ of a fixed size. Write down the powers $1, x, x^2, x^3, \ldots$, computed in a special number system where sums are XOR. Each output bit is a parity of a power of $x$, masked by $y$. A group of output bits combines into one number built from $x$, and this number is zero only for a few choices of $x$. When it is not zero, the mask $y$ makes the XOR of the group a fair coin.

## The problem

Notation. $n$ is the output length and $\varepsilon \in (0, 1)$ the bias. $\mathrm{GF}(2^m)$ is the field with $2^m$ elements, written as polynomials over $\mathrm{GF}(2)$ of degree less than $m$, modulo an [irreducible polynomial](/irreducible-polynomial/) of degree $m$. Each element is also an $m$-bit vector, and $\langle u, v \rangle = \bigoplus_j u_j v_j$ is the inner product over $\mathrm{GF}(2)$ of the vectors. $\mathrm{bias}_S(Z) = |\mathrm{E}[(-1)^{\bigoplus_{i \in S} Z_i}]|$.

Given $n$ and $\varepsilon$, compute a function $G : \{0,1\}^{\ell} \to \{0,1\}^n$, with a seed length $\ell$ as small as possible, such that for a uniform seed every nonempty $S \subseteq \{0, \ldots, n-1\}$ has $\mathrm{bias}_S(G(\text{seed})) \le \varepsilon$. Each output bit must be computable in time polynomial in $\ell$.

## The algorithm

Choose $m = \lceil \log_2((n-1)/\varepsilon) \rceil$, or $m = 1$ when $n = 1$, and an irreducible polynomial of degree $m$. The seed has $2m$ bits.

```pseudo id=main
SMALL-BIAS-GENERATOR(s, n, m)          ▷ s has 2m bits; output n bits
L1  x ← the high m bits of s           ▷ x and y are elements of GF(2^m)
L2  y ← the low m bits of s
L3  z ← 1                              ▷ invariant: z = x^i, with x^0 = 1 also for x = 0
L4  for i ← 0 to n − 1 do
L5      b_i ← ⟨z, y⟩                   ▷ parity of the bitwise AND of z and y
L6      z ← z · x                      ▷ product in GF(2^m)
L7  return b_0 b_1 … b_{n−1}
```

Line L5 is a bitwise AND and a population count. Line L6 is a carry-less product of two $m$-bit words, reduced modulo the irreducible polynomial.

## Example

Take $m = 3$ with the modulus $t^3 + t + 1$, so the field has 8 elements and $t^3 = t + 1$. Write an element as a 3-bit vector $(c_2 c_1 c_0)$ for $c_2 t^2 + c_1 t + c_0$. The seed $x = t = 010$, $y = 011$ gives, for $n = 7$:

| $i$ | $x^i$ | $x^i$ as a vector | $\langle x^i, y \rangle$ |
|---|---|---|---|
| 0 | $1$ | 001 | 1 |
| 1 | $t$ | 010 | 1 |
| 2 | $t^2$ | 100 | 0 |
| 3 | $t + 1$ | 011 | 0 |
| 4 | $t^2 + t$ | 110 | 1 |
| 5 | $t^2 + t + 1$ | 111 | 0 |
| 6 | $t^2 + 1$ | 101 | 1 |

The output is $1100101$. Over all 64 seeds, the largest bias of a nonempty parity of these 7 bits is $3/4 = 6/8$, which equals the bound $(n - 1)/2^m$. For $n = 8$, the bits $b_0$ and $b_7$ have parity $\langle 1 + x^7, y \rangle$. Since $x^7 = 1$ for every $x \ne 0$, this parity is 0 for the 56 seeds with $x \ne 0$ and uniform for $x = 0$, so its bias is $7/8$, again equal to the bound.

## Correctness

Fix a nonempty $S$. Because the inner product with $y$ is linear over $\mathrm{GF}(2)$ and field addition is bitwise XOR,

$$\bigoplus_{i \in S} b_i = \Big\langle \sum_{i \in S} x^i,\; y \Big\rangle = \langle p_S(x), y \rangle, \qquad p_S(t) = \sum_{i \in S} t^i.$$

$p_S$ is a nonzero polynomial of degree at most $n - 1$, so it has at most $n - 1$ roots in the field. For a fixed $x$ with $p_S(x) \ne 0$, the parity $\langle p_S(x), y \rangle$ is unbiased over a uniform $y$. For a root $x$, the parity is 0. So $\mathrm{E}[(-1)^{\text{parity}}] = (\text{number of roots})/2^m \le (n-1)/2^m \le \varepsilon$. The full proof is below.

## Complexity

- **Seed length.** $2m = 2\lceil \log_2((n-1)/\varepsilon) \rceil \le 2\log_2(n/\varepsilon) + 2$ random bits. The space has $2^{2m} < 4(n/\varepsilon)^2$ points.
- **Time.** $n$ field products and $n$ parities. With a shift-and-add product on words of at least $m$ bits, each product takes $\Theta(m)$ word operations, for $\Theta(nm)$ in total. With a carry-less multiply instruction, each product takes $O(1)$ operations, for $\Theta(n)$ in total.
- **One bit alone.** Bit $i$ alone needs $x^i$, which takes $O(\log i)$ field products by repeated squaring.
- **Space.** $\Theta(1)$ words besides the output and the modulus.
- **Setup.** An irreducible polynomial of degree $m$ can be found by a randomized test in expected polynomial time, or deterministically in time polynomial in $2^m$, which is polynomial in $n/\varepsilon$. Tables list them for all practical $m$.

## Properties

- **Exact bias bound.** The bias of every nonempty parity is exactly $r/2^m$, where $r$ is the number of distinct roots of $p_S$ in $\mathrm{GF}(2^m)$. It is never negative: a parity is never more likely to be 1 than 0.
- **Linear in $y$.** For a fixed $x$, the output is a linear function of $y$. So the space is a union of $2^m$ linear subspaces, one for each $x$.
- **Almost $k$-wise independent.** By the XOR lemma, any $k$ output bits are within statistical distance $\frac{1}{2}\sqrt{2^k - 1} \cdot (n-1)/2^m$ of uniform.
- **Near-optimal seed.** The seed length $2\log_2(n/\varepsilon)$ is about $\log_2 n$ more than the optimal $\log_2 n + 2\log_2(1/\varepsilon)$ of [small-bias sample spaces](/small-bias-sample-space/).
- **Tight bound.** For $n = 2^m$ the test $\{0, 2^m - 1\}$ reaches $(n - 1)/2^m$, since $1 + t^{2^m - 1}$ vanishes at every nonzero element. In small fields the largest bias equals the bound also for other $n$: for $m = 3$ with $n = 4$ and $n = 7$, and for $m = 4$ with $n = 8$.

## Variants and improvements

- **LFSR construction (AGHP).** The seed is a random feedback polynomial of degree $m$, taken from a suitable set, and a random start state; the output is the [linear feedback shift register](/linear-feedback-shift-register/) sequence. Its bias is also about $n/2^m$.
- **Quadratic characters (AGHP).** For a prime $p$, bit $i$ is given by the quadratic character of $x + i$ modulo $p$ for a random $x$. Weil's bound on character sums gives bias about $n/\sqrt{p}$.
- **Naor and Naor (1990).** The first construction combined a code of constant rate, a $k$-wise independent space and an expander walk to reach seed length $O(\log n + \log(1/\varepsilon))$.
- **Code concatenation.** An $\varepsilon$-biased space is an $\varepsilon$-balanced code. Concatenating the powering code, which is a form of a [Reed-Solomon code](/reed-solomon-code/) followed by a [Hadamard code](/hadamard-code/), with other codes gives other trade-offs between $n$ and $\varepsilon$.
- **Ta-Shma (2017).** Walks on expanders with a careful choice of the walk give seed length $\log_2 n + (2 + o(1))\log_2(1/\varepsilon)$, which is close to optimal.
- **Almost $k$-wise independence.** Apply a linear map that sends $k$-wise independent bits to $n$ bits to the output of a generator with bias $\varepsilon 2^{-k/2}$ on fewer bits. This gives $\varepsilon$-almost $k$-wise independent bits with $O(k + \log\log n + \log(1/\varepsilon))$ random bits.

## When to use it

Use it when a proof needs only that every parity of the random bits is close to fair, or that every $k$ bits are close to uniform for a $k$ that grows with $n$, such as $k = \log n$. Then $O(\log n + \log(1/\varepsilon))$ seed bits replace $n$ random bits, and a deterministic algorithm can try all $O((n/\varepsilon)^2)$ seeds. For exact $k$-wise independence with a constant $k$, use the polynomial or BCH spaces of [k-wise independence](/k-wise-independence/). Small-bias generators do not fool general tests, such as AND of many bits; for those, use a [pseudorandom generator](/pseudorandom-generator/) for the class of tests.

## Pitfalls

- **The modulus must be irreducible.** If the polynomial factors, the ring has zero divisors, and a polynomial $p_S$ can have more than $n - 1$ roots. Check the modulus.
- **$x = 0$.** The loop starts with $z = 1$, so bit 0 is $\langle 1, y \rangle$ even for $x = 0$. Computing $x^i$ by a library power function with $0^0 = 0$ changes the space.
- **Bias conventions.** This page uses $|\Pr[0] - \Pr[1]|$. With the convention $|\Pr[1] - 1/2|$ the same space has bias $(n-1)/2^{m+1}$.
- **The bound needs $2^m > n - 1$.** For $n - 1 \ge 2^m$ the bound is at least 1 and says nothing; in fact the bits then repeat with period dividing $2^m - 1$ for $x \ne 0$.
- **Not a cryptographic generator.** The output is linear in $y$, so a few output bits reveal $y$ for each guess of $x$. It fools parity tests only.

## Implementations

## History

Naor and Naor (STOC 1990) defined small-bias probability spaces and built the first ones with seed length $O(\log n + \log(1/\varepsilon))$, for use in derandomization and for almost $k$-wise independent variables. Alon, Goldreich, Håstad and Peralta (FOCS 1990, journal version 1992) gave three simpler constructions with explicit constants: the powering construction of this page, the LFSR construction and the quadratic character construction. Later work links small-bias spaces with balanced codes; Ta-Shma (2017) reached a seed length within a lower order term of the optimum.

## References
