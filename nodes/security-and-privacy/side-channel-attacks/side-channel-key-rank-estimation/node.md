---
tag: BD5WM2
kind: algorithm
slug: side-channel-key-rank-estimation
name: Key rank estimation
aliases:
- key enumeration rank
area: security-and-privacy/side-channel-attacks
level: research
summary: "Bounds the rank of the true key among all keys from per-byte scores of a side-channel attack, by histogram convolution, without enumerating keys."
model: real-ram
complexity:
  vars: {d: the number of key parts, K: the number of guesses for each part, N: the number of bins in each histogram}
  time: {worst: "O(d K + d^2 N min(N, K))", average: "O(d K + d^2 N min(N, K))", best: "Θ(d K + d^2 N)"}
  space: {extra: "Θ(d N + d K)"}
history:
  year: 2015
  people: [Cezary Glowacz, Vincent Grosso, Romain Poussier, Joachim Schüth, François-Xavier Standaert]
  note: "Glowacz, Grosso, Poussier, Schüth and Standaert gave the histogram method at FSE 2015, after the rank estimation of Veyrat-Charvillon, Gérard and Standaert at EUROCRYPT 2013."
prereqs: [template-attack, convolution]
see_also: [correlation-power-analysis, differential-power-analysis, histogram, brute-force-search, fast-fourier-transform, polynomial-multiplication, subset-sum-problem, advanced-encryption-standard]
sources:
  - paper: doi:10.1007/978-3-662-48116-5_6
    title: "Cezary Glowacz, Vincent Grosso, Romain Poussier, Joachim Schüth and François-Xavier Standaert, Simpler and more efficient rank estimation for side-channel security assessment, FSE 2015, LNCS 9054, pages 117 to 129"
    locator: the histogram construction, the convolution of the histograms and the lower and upper bounds on the rank
  - paper: doi:10.1007/978-3-642-38348-9_8
    title: "Nicolas Veyrat-Charvillon, Benoît Gérard and François-Xavier Standaert, Security evaluations beyond computing power, EUROCRYPT 2013, LNCS 7881, pages 126 to 141"
    locator: the definition of the rank of the key beyond the reach of enumeration and the first rank estimation algorithm with bounds
  - paper: doi:10.1007/978-3-642-01001-9_26
    title: "François-Xavier Standaert, Tal G. Malkin and Moti Yung, A unified framework for the analysis of side-channel key recovery attacks, EUROCRYPT 2009, LNCS 5479, pages 443 to 461"
    locator: the definitions of the success rate and the guessing entropy, which are statistics of the rank
  - paper: doi:10.1007/978-3-540-74735-2_31
    title: "Andrey Bogdanov and others, PRESENT, an ultra-lightweight block cipher, CHES 2007, LNCS 4727"
    locator: the description of the substitution layer (the table of the 4-bit S-box used in the synthetic scores of this page)
---

Key rank estimation tells an evaluator how far a side-channel attack got. A divide-and-conquer attack such as [correlation power analysis](/correlation-power-analysis/) or a [template attack](/template-attack/) gives a list of scores for each small part of the key, for example 16 lists of 256 scores for AES-128. If the right value is first in every list, the attack is done. If not, the attacker must search the full keys in order of their total score, and the question is how many keys come before the right one. For a 128-bit key that number cannot be found by enumeration. The histogram method of Glowacz, Grosso, Poussier, Schüth and Standaert (2015) gives a lower and an upper bound on it with a few convolutions of small histograms, with no enumeration.

## In plain words

An attack on a chip does not find the whole key at once. It looks at one small piece at a time and gives each possible value of the piece a score. To use the result, the attacker tries full keys from the best total score down. The evaluator, who knows the real key, wants to know how many tries that takes. Counting the keys one by one is impossible for a long key. Instead, round each score down to a coarse step and count, for each rounded total, how many keys reach it. This count is a sum over all pieces, and it can be built piece by piece, the same way you count the ways to roll a total with several dice. The rounding blurs each total a little, so you get two numbers that the true count must lie between.

## The problem

The key has $d$ independent parts. For part $i$ there are $K$ possible values with real scores $s_i(0), \ldots, s_i(K - 1)$, where a higher score means a more likely value. The score of a full key $x = (x_1, \ldots, x_d)$ is $S(x) = \sum_i s_i(x_i)$; with log-likelihood scores this is the log-likelihood of the full key, because the parts are independent. The evaluator knows the true key $k^\ast$. Its rank is

$$\mathrm{rank}(k^\ast) = 1 + \#\{x : S(x) > S(k^\ast)\},$$

the number of full keys that an optimal enumeration tries up to and including $k^\ast$ when ties are broken in its favour. The goal is two numbers $\mathrm{lo} \le \mathrm{rank}(k^\ast) \le \mathrm{up}$ that are close, at a cost far below the $K^d$ keys. The cost model is the [real RAM](/real-ram/), with exact integer counts.

## The algorithm

```pseudo id=main
KEY-RANK-BOUNDS(scores s_1 .. s_d, true key k*, bin width w > 0)
L1  for i = 1 .. d do
L2      shift the scores of part i so that the smallest one is 0
L3      H_i[b] ← the number of values x with ⌊s_i(x) / w⌋ = b    ▷ the histogram of part i
L4      b*_i ← ⌊s_i(k*_i) / w⌋                                  ▷ the bin of the true part
L5  H ← H_1
L6  for i = 2 .. d do H ← H ∗ H_i                               ▷ convolution
L7  lo ← 1 + Σ of H[b] for b ≥ b* + d,  with b* = b*_1 + ... + b*_d
L8  up ← Σ of H[b] for b ≥ b* - d + 1
L9  return (lo, up)
```

Line L2 adds a constant to each part. This adds the same constant to every full key, so the order of the keys and the rank do not change. Line L6 is the [convolution](/convolution/) $(H \ast H_i)[b] = \sum_j H[j] \, H_i[b - j]$. After it, $H[b]$ is the number of full keys whose bins add up to $b$. This is the dice count of "In plain words", and it is the same as the product of the polynomials $\sum_b H_i[b] z^b$, as in [polynomial multiplication](/polynomial-multiplication/).

Each bin covers a score interval of width $w$, so the bin sum $B(x)$ of a key fixes its total score to within $d w$: $w B(x) \le S(x) < w (B(x) + d)$. A key with $B(x) \ge b^\ast + d$ has a total score of at least $w(b^\ast + d)$, which is larger than $S(k^\ast)$, so it is better than the true key. A key that is better than the true key has $w(B(x) + d) > S(x) > S(k^\ast) \ge w b^\ast$, so $B(x) \ge b^\ast - d + 1$. Lines L7 and L8 count these two sets.

## Example

Take $d = 2$ parts with $K = 4$ values each, already shifted:

$$s_1 = (0, 3, 5, 9), \qquad s_2 = (0, 2, 7, 8),$$

and the true key $k^\ast = (1, 2)$ with $S(k^\ast) = 3 + 7 = 10$. The keys with a larger total are $(1, 3)$ with 11, $(2, 2)$ with 12, $(2, 3)$ with 13, $(3, 1)$ with 11, $(3, 2)$ with 16 and $(3, 3)$ with 17, so the rank is 7.

With $w = 2$, the bins of part 1 are $0, 1, 2, 4$ and those of part 2 are $0, 1, 3, 4$:

$$H_1 = (1, 1, 1, 0, 1), \qquad H_2 = (1, 1, 0, 1, 1), \qquad H_1 \ast H_2 = (1, 2, 2, 2, 3, 3, 1, 1, 1).$$

The true key is in bins 1 and 3, so $b^\ast = 4$. Line L7 adds the bins from $b^\ast + 2 = 6$ on: $\mathrm{lo} = 1 + (1 + 1 + 1) = 4$. Line L8 adds the bins from $b^\ast - 1 = 3$ on: $\mathrm{up} = 2 + 3 + 3 + 1 + 1 + 1 = 11$. So $4 \le 7 \le 11$. The bounds for other widths are:

| width w | 4 | 2 | 1 | 1/2 |
|---|---|---|---|---|
| (lo, up) | (4, 16) | (4, 11) | (5, 8) | (7, 7) |

At $w = 1/2$ the bounds meet in this example. "Properties" gives a width at which they always meet.

## Correctness

The bounds hold for every input; this is a theorem, with no model of the scores. The two facts are the bin inequality $w B(x) \le S(x) < w(B(x) + d)$, which follows from $w b \le s < w (b + 1)$ for $b = \lfloor s/w \rfloor$ in each part, and the fact that after line L6, $H[b]$ is the exact number of full keys with bin sum $b$, which follows by induction on the number of parts convolved. The true key itself is in the set of line L8, because $b^\ast \ge b^\ast - d + 1$, and it is not strictly better than itself; this is why line L8 has no "1 +". The [proof](proofs/correctness.md) gives the details, and also proves that the bounds are equal to the rank when $(2d - 1) w$ is smaller than every gap between distinct totals.

## Complexity

Lines L1 to L4 cost $\Theta(dK)$. After $i$ parts the histogram $H$ has at most $iN$ bins, and the convolution with $H_{i+1}$ visits each bin of $H$ once for each nonzero bin of $H_{i+1}$, of which there are at most $\min(N, K)$. The sum over $i$ is $O(d^2 N \min(N, K))$. Lines L7 and L8 cost $O(dN)$. The extra space is $O(dN)$ for $H$ and $\Theta(dK)$ for the bins.

The counts can be as large as $K^d$, which is $2^{128}$ for AES-128, so they need exact big integers; Python integers are exact. With a [fast Fourier transform](/fast-fourier-transform/) each convolution costs $O(dN \log(dN))$ arithmetic operations, but floating point values cannot hold such counts exactly.

The tightness depends on $N$. A measurement on synthetic scores: a 64-bit key of $d = 16$ parts of 4 bits, the Gaussian log-likelihood scores of $m$ traces for each part with Hamming weight leakage of the PRESENT S-box and $\sigma = 1$, seed 7. The width is the widest score range of a part divided by the number of bins. The table gives $\log_2 \mathrm{lo}$ and $\log_2 \mathrm{up}$:

| traces for each part | 10 bins | 100 bins | 1000 bins | 5000 bins |
|---|---|---|---|---|
| m = 2 | 0 to 60.25 | 44.14 to 49.60 | 47.02 to 47.56 | 47.22 to 47.33 |
| m = 4 | 0 to 58.11 | 23.98 to 36.21 | 29.80 to 31.02 | 30.29 to 30.53 |
| m = 8 | 0 to 47.02 | 5.49 to 19.25 | 13.35 to 14.63 | 13.85 to 14.11 |

With 10 bins the bounds say almost nothing. With 1000 bins they are within 1.3 bits, and with 5000 bins within 0.3 bits. In this measurement the gap in bits shrinks roughly in proportion to $1/N$; a heuristic reason is that the uncertain band of bin sums is always $2d - 1$ bins wide, and so its width in score units is proportional to $w$.

## Properties

- **Exact counting, approximate scores.** The algorithm counts keys exactly; all the error comes from the rounding of the scores to bins. So the bounds are guaranteed, not statistical.
- **Exact at fine resolution.** If $(2d - 1)w$ is smaller than the smallest gap between distinct totals, then $\mathrm{lo} = \mathrm{rank}$, and $\mathrm{up} = \mathrm{rank}$ when no other key ties with the true key. In practice the totals are too dense for this, and the bounds are used at a few thousand bins.
- **Needs the true key.** The bounds are about the position of a known key. This is an evaluation tool for a designer or a lab, not part of an attack.
- **Independent parts.** The method assumes that the score of a full key is the sum of the scores of its parts. For log-likelihood scores this is true when the parts leak independently.
- **Ties.** The rank counts only strictly better keys. A key with the same total is counted by line L8, so ties make the upper bound larger.

## Variants and improvements

- **Rank of a probability list.** If an attack gives probabilities $p_i(x)$, the scores are $s_i(x) = \log p_i(x)$. A score of $-\infty$ (a probability of 0) must be replaced by a large finite negative value, or the part must be handled apart.
- **Merge before the histograms.** Combine two parts of 8 bits into one of 16 bits with $K = 65536$ exact sums, and bin the merged lists. This halves $d$, and so the band of $2d - 1$ uncertain bins, at the cost of larger lists.
- **The rank of a set of keys.** The same histogram gives, for any threshold, the number of keys above it. This yields the whole curve of enumeration effort against success probability over many runs of an attack.
- **Earlier methods.** Veyrat-Charvillon, Gérard and Standaert (2013) gave the first rank estimation with bounds beyond the reach of enumeration. The histogram method is simpler and faster for the same tightness.
- **Key enumeration.** An enumeration algorithm lists the full keys in order of their total score. It is what an attacker runs when the rank is small enough; rank estimation tells whether it is.

## When to use it

Use it in a security evaluation after a divide-and-conquer attack on a key that is too long to enumerate, to report how much computing power would be left to recover the key. Use [brute-force search](/brute-force-search/) over the full keys only on toy keys, for example to test an implementation, as the tests of this page do with 4096 keys. Report the rank over many runs as a curve, or through statistics such as the success rate and the guessing entropy of Standaert, Malkin and Yung (2009).

## Pitfalls

- **One bin of slack.** The count $1 + \#\{x : B(x) > b^\ast\}$ looks natural but is not a bound in either direction. In the example with $w = 4$ it gives 9, which is more than the rank 7. The band of $d$ bins on each side is necessary.
- **Floating point bins.** With floating point scores, a score that lies exactly on a bin edge can be rounded into the wrong bin, and the bound can fail by the keys in that bin. Use exact rational arithmetic when a guarantee matters; with continuous scores this event has probability 0.
- **Floating point counts.** A histogram of $2^{128}$ keys in double precision loses the low bits of the counts. Keep the counts as integers, or use a logarithmic scale and accept an error.
- **Too few bins.** With 10 bins on 16 parts the upper bound is close to $K^d$ and the lower bound is 1. Increase $N$ until the bounds stop moving by more than the precision you need.
- **Dependent parts.** If the leakage of two parts is correlated, the sum of separate log-likelihoods is not the log-likelihood of the full key, and the rank is for the wrong order of keys.

## Implementations

The code of this page is an abstract model on synthetic data. The function `key_rank_bounds` takes lists of scores; the scores in the tests are either random rational numbers or Gaussian log-likelihoods of a stated Hamming weight leakage model of the PRESENT S-box, drawn with a seeded `random.Random` by `synthetic_scores`. The code never reads a device, a file or a clock. The tests compare the bounds with the brute-force rank on 500 random inputs with exact fractions and up to 4096 keys, check the example, the exact bounds at fine bins, the pitfall of one bin of slack, and the 64-bit measurement above.

## History

The rank of the key as a measure of side-channel security comes from the framework of Standaert, Malkin and Yung (2009), where the success rate and the guessing entropy are statistics of it. Veyrat-Charvillon, Gérard and Standaert (2013) showed how to bound the rank of a key that is far beyond enumeration, so that an evaluator can analyse attacks that cannot be mounted in full. Glowacz, Grosso, Poussier, Schüth and Standaert (2015) replaced that method by the histogram convolution on this page.

## References
