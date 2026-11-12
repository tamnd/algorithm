---
tag: 0S9GAW
kind: algorithm
slug: von-neumann-debiasing
name: Von Neumann debiasing
aliases:
- von Neumann extractor
- von Neumann's trick
- Peres extractor
area: randomized/derandomization
level: intro
summary: Reads coin flips in pairs, outputs 0 for 01, 1 for 10, and discards 00 and 11, yielding unbiased bits from independent biased flips.
solves: [unbiased-bits-from-biased-coin]
model: word-ram
complexity:
  vars: {n: the number of input flips}
  time: {worst: Θ(n), average: Θ(n), best: Θ(n)}
  space: {extra: Θ(1)}
properties: {deterministic: true, exact: true, online: true, recursive: false}
history:
  year: 1951
  people: [John von Neumann]
  note: "Von Neumann described the pair trick in 1951. Elias (1972) and Peres (1992) gave procedures whose rate tends to the entropy of the coin."
prereqs: [unbiased-bits-from-biased-coin, bernoulli-trials, binary-entropy-function]
see_also: [randomness-extractor, entropy-source, min-entropy, santha-vazirani-source, shannon-entropy, markov-chain]
sources:
  - paper: "John von Neumann, Various techniques used in connection with random digits, in Monte Carlo Method, National Bureau of Standards Applied Mathematics Series 12, 1951, pages 36 to 38"
    locator: the procedure that maps the pairs 01 and 10 to an output bit and drops 00 and 11
  - paper: doi:10.1214/aos/1176348543
    title: Yuval Peres, Iterating von Neumann's procedure for extracting random bits, Annals of Statistics 20(1), 1992
    locator: pages 590 to 597 (the iterated procedure, the proof that its output is unbiased, and the theorem that its rate tends to h(p))
  - paper: doi:10.1214/aoms/1177692552
    title: Peter Elias, The efficient construction of an unbiased random sequence, Annals of Mathematical Statistics 43(3), 1972
    locator: pages 865 to 870 (the upper bound h(p) on the rate and block procedures that approach it)
  - paper: "Manuel Blum, Independent unbiased coin flips from a correlated biased source, a finite state Markov chain, Combinatorica 6(2), 1986, pages 97 to 108"
    locator: the extension of von Neumann's method to a source that is a finite Markov chain with unknown transition probabilities
---

Von Neumann debiasing turns independent flips of a coin with an unknown bias into exactly fair, independent bits. It reads the flips in pairs, outputs 0 for $01$ and 1 for $10$, and discards $00$ and $11$. Since $01$ and $10$ have the same probability $p(1-p)$, each output bit is fair whatever $p$ is. Peres (1992) showed that applying the same idea again to the discarded information gives a rate that tends to the [binary entropy](/binary-entropy-function/) $H(p)$, the best possible.

## In plain words

You have a coin that may be unfair, and you do not know by how much. Flip it twice. If you see heads then tails, write 1. If you see tails then heads, write 0. If both flips are the same, write nothing and try again with two new flips.

Heads then tails and tails then heads are equally likely for any coin, because they contain the same flips in a different order. So each bit you write is a fair coin, and the bits do not depend on each other.

The price is waste. A fair coin gives one bit for every four flips on average, and a very unfair coin gives much less. Peres's version reuses the pairs that were thrown away and comes close to the best rate allowed by the entropy of the coin.

## The problem

Notation. $x = x_1 x_2 \ldots x_n$ is a string of [Bernoulli trials](/bernoulli-trials/): independent bits with $\Pr[x_i = 1] = p$ for all $i$, where $p \in (0, 1)$ is unknown, and $q = 1 - p$. For a string $y$, $|y|$ is its length and $\oplus$ is XOR. $H(p) = -p\log_2 p - q\log_2 q$.

Compute a deterministic function $\Psi$ of $x$ such that, for every $p$ and every $\ell$, the output $\Psi(x)$ conditioned on $|\Psi(x)| = \ell$ is uniform on $\{0,1\}^\ell$. The function must not depend on $p$. Among such functions, the goal is a large expected output length $\mathrm{E}|\Psi(x)|$. This is the problem [unbiased bits from a biased coin](/unbiased-bits-from-biased-coin/), and $\Psi$ is a deterministic [randomness extractor](/randomness-extractor/) for the class of i.i.d. sources.

## The algorithm

```pseudo id=main
VON-NEUMANN(x)                          ▷ x = x_1 … x_n, i.i.d. bits with Pr[1] = p
L1  out ← empty list
L2  for i ← 1 to ⌊n/2⌋ do
L3      if x_{2i−1} ≠ x_{2i} then append x_{2i−1} to out    ▷ 10 gives 1, 01 gives 0
L4  return out
PERES(x)
L5  if |x| < 2 then return empty list
L6  u ← (x_1 ⊕ x_2, x_3 ⊕ x_4, …, x_{2m−1} ⊕ x_{2m})       ▷ m = ⌊|x|/2⌋
L7  v ← (x_{2i−1} for each i ≤ m with x_{2i−1} = x_{2i})
L8  return VON-NEUMANN(x) ++ PERES(u) ++ PERES(v)
```

An odd last flip is ignored. In PERES, $u$ records which pairs were unequal, and $v$ records the value of each equal pair. Both are discarded by VON-NEUMANN, and both still carry randomness: $u$ is i.i.d. with $\Pr[1] = 2pq$, and given $u$, $v$ is i.i.d. with $\Pr[1] = p^2/(p^2 + q^2)$. A cutoff on the depth of the recursion keeps the output exact; depth 1 is VON-NEUMANN.

## Example

Take $x = 110100101101$, with the pairs $11, 01, 00, 10, 11, 01$.

- VON-NEUMANN keeps the unequal pairs $01, 10, 01$ and outputs $0, 1, 0$.
- PERES sets $u = 010101$ and $v = 101$ (the values of the equal pairs $11, 00, 11$).
- PERES($u$): the pairs $01, 01, 01$ give $0, 0, 0$; then $u' = 111$ and $v'$ is empty. PERES($111$) has one pair $11$, which gives nothing, and its recursive calls get $0$ and $1$, which are too short.
- PERES($v$): the pair $10$ gives $1$; then $u'' = 1$ and $v''$ is empty, both too short.

So VON-NEUMANN outputs $010$ (3 bits from 12 flips) and PERES outputs $0100001$ (7 bits).

Expected rates in output bits per input flip, as $n \to \infty$, for depth $\nu$ of PERES (depth 1 is VON-NEUMANN):

| $p$ | $\nu = 1$ | $\nu = 2$ | $\nu = 3$ | $\nu = 4$ | $\nu = 10$ | $H(p)$ |
|---|---|---|---|---|---|---|
| 0.5 | 0.25 | 0.4375 | 0.5781 | 0.6836 | 0.9437 | 1 |
| 0.3 | 0.21 | 0.3698 | 0.4926 | 0.5861 | 0.8261 | 0.8813 |
| 0.1 | 0.09 | 0.1687 | 0.2333 | 0.2849 | 0.4309 | 0.4690 |

## Correctness

For VON-NEUMANN: a pair is $01$ with probability $qp$ and $10$ with probability $pq$. Condition on the set of indices $i$ whose pair is unequal. The pairs are independent, so each of these pairs is $10$ or $01$ with probability $pq/(2pq) = 1/2$, independently of the others. The output is the list of first bits of these pairs, so given its length it is uniform.

For PERES, the proof is an induction on the length with a stronger hypothesis: if $x$ is uniform among the strings of length $N$ with exactly $k$ ones, then $\Psi(x)$ is uniform given its length. An i.i.d. string, conditioned on its number of ones, is of this kind, and a mixture of distributions that are uniform given the length is uniform given the length. The key step is that, given the number $a$ of unequal pairs, the three parts $w = \text{VON-NEUMANN}(x)$, $u$ and $v$ are independent, $w$ is uniform on $\{0,1\}^a$, and $u$ and $v$ are again uniform among strings of fixed length and weight. The full proof is in the proof file.

## Complexity

- **VON-NEUMANN.** One pass, $\lfloor n/2 \rfloor$ comparisons, $\Theta(n)$ time and $\Theta(1)$ extra space besides the output. It works on a stream: each pair gives its bit at once.
- **PERES.** The recursive inputs $u$ and $v$ have lengths $\lfloor |x|/2 \rfloor$ and at most $\lfloor |x|/2 \rfloor$, so each level of the recursion tree has total input length at most $n$, and the depth is at most $\lfloor \log_2 n \rfloor + 1$. The time is $O(n \log n)$ in the worst case, and $O(n\nu)$ with a depth cutoff $\nu$. The extra space is $O(n)$ for the lists $u$ and $v$ on the stack.
- **Random input.** The expected number of flips per output bit of VON-NEUMANN is $1/(pq)$, so a coin with $p = 0.01$ needs about 101 flips per bit.

## Properties

- **Exact.** The output is exactly uniform given its length, for every $p \in (0, 1)$, with no knowledge of $p$. It is not merely close to uniform.
- **Expected yield.** By [linearity of expectation](/linearity-of-expectation/), $\mathrm{E}|\text{VON-NEUMANN}(x)| = \lfloor n/2 \rfloor \cdot 2pq$, a rate of $pq \le 1/4$ per flip.
- **Peres rates.** With $r_0 = 0$, the rate of depth $\nu$ satisfies
  $$r_\nu(p) = pq + \tfrac{1}{2} r_{\nu-1}(2pq) + \tfrac{p^2 + q^2}{2}\, r_{\nu-1}\!\Big(\frac{p^2}{p^2 + q^2}\Big),$$
  because $u$ has $n/2$ bits with $\Pr[1] = 2pq$, and $v$ has about $(p^2 + q^2)n/2$ bits with $\Pr[1] = p^2/(p^2 + q^2)$. Peres proved that $r_\nu(p) \to H(p)$ as $\nu \to \infty$.
- **Entropy bound.** No exact procedure does better than $H(p)$ per flip. Let $L = |\Psi(x)|$. Since $\Psi(x)$ is uniform on $\{0,1\}^\ell$ given $L = \ell$, its [Shannon entropy](/shannon-entropy/) is $H(\Psi(x)) = H(L) + \sum_\ell \Pr[L = \ell]\,\ell \ge \mathrm{E}[L]$. Since $\Psi(x)$ is a function of $x$, $H(\Psi(x)) \le H(x) = nH(p)$. So $\mathrm{E}[L] \le nH(p)$ (Elias 1972).
- **Random output length.** The length depends on $x$. With $n$ flips there is a probability $(p^2 + q^2)^{\lfloor n/2 \rfloor}$ that VON-NEUMANN gives no bit at all.

## Variants and improvements

- **Peres iteration.** The procedure of this page. It keeps the simple pair structure and reaches the entropy rate as the depth grows.
- **Elias (1972).** Read the flips in blocks of length $k$. Inside each class of strings with the same number of ones, all strings have the same probability, so the position of the block inside its class can be turned into fair bits. The rate tends to $H(p)$ as $k \to \infty$.
- **Markov sources.** Blum (1986) extended the method to sources that are finite Markov chains with unknown transition probabilities. The extension needs care, because simple ways to apply the pair trick to such a chain can give dependent output bits.
- **Weaker sources.** For sources with dependent bits, no deterministic function works in general. For a [Santha-Vazirani source](/santha-vazirani-source/) no deterministic function gives even one bit that is almost fair. Sources described only by their [min-entropy](/min-entropy/) need a [seeded extractor](/seeded-extractor/) or several independent sources.

## When to use it

Use it when the bits are independent and have a fixed but unknown bias, such as a physical [entropy source](/entropy-source/) whose samples are known to be independent, or a coin whose bias may change slowly from pair to pair. It is a few lines of code and the output is exact. Use the PERES form when the rate matters. When the samples may be correlated, use a conditioning function based on a hash or a seeded extractor, and check the source with health tests.

## Pitfalls

- **Correlated flips break it.** Let $x$ be a [Markov chain](/markov-chain/) on $\{0, 1\}$ with a uniform first bit, where each bit repeats the one before with probability $3/4$. On 4 flips, the outputs of length 2 come from $0101, 0110, 1001, 1010$ with probabilities $1/128, 3/128, 3/128, 1/128$. So given two output bits, $00$ has probability $1/8$ and $01$ has $3/8$: each bit is fair, but the two bits are dependent.
- **The two flips of a pair need the same bias.** If $\Pr[x_{2i-1} = 1] = p_1$ and $\Pr[x_{2i} = 1] = p_2$, then $\Pr[10] = p_1(1 - p_2) \ne (1 - p_1)p_2$ unless $p_1 = p_2$. The bias may change between pairs, but not inside a pair.
- **Do not use overlapping pairs.** If the pairs are $x_1x_2, x_2x_3, \ldots$, the unequal pairs are the changes of the sequence, and changes alternate between up and down. So the outputs alternate $0, 1, 0, 1, \ldots$ after the first one.
- **Keep the order of PERES.** The output is exact for the concatenation in the order of line L8, and also for any other order fixed in advance. An order that depends on the values of the bits is not covered by the proof.
- **No bound on the time to the first bit.** If $p$ is near 0 or 1, a long run of equal pairs is likely. A program that needs a fixed number of bits must accept a random running time, or fail with small probability.

## Implementations

## History

Von Neumann (1951) described the pair trick in a short note on techniques for random digits in Monte Carlo computation. Elias (1972) proved that no exact procedure has a rate above $H(p)$ and gave block procedures that approach it. Blum (1986) treated sources that are Markov chains. Peres (1992) showed that iterating von Neumann's procedure on the discarded information reaches the rate $H(p)$, with a short recursive algorithm.

## References
