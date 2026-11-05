---
tag: 30WCBH
kind: technique
slug: fingerprinting
name: Fingerprinting
aliases:
- Karp-Rabin fingerprinting
- Randomized fingerprinting
- fingerprint
- random fingerprint
- short hash of an object
area: strings/string-hashing
level: intro
summary: Map a large object to a short fingerprint so that equality of fingerprints tests equality of objects with small error.
prereqs: [hash-function, randomized-algorithm, prime-number]
see_also: [polynomial-rolling-hash, polynomial-hash-collision-bound, string-equality-testing, rabin-fingerprint, freivalds-algorithm, schwartz-zippel-lemma, universal-string-hashing, minhash]
sources:
  - book: isbn:9780521474658
    title: Rajeev Motwani and Prabhakar Raghavan, Randomized Algorithms, Cambridge University Press, 1995
    locator: Chapter 7, Algebraic techniques (fingerprinting and Freivalds' technique, verifying polynomial identities, verifying the equality of strings, and the comparison of fingerprinting techniques)
  - book: isbn:9781107154889
    title: Michael Mitzenmacher and Eli Upfal, Probability and Computing, second edition, Cambridge University Press, 2017
    locator: Chapter 1 (Section 1.1, verifying polynomial identities, and the application to verifying matrix multiplication)
  - paper: doi:10.1147/rd.312.0249
    title: Richard M. Karp and Michael O. Rabin, Efficient randomized pattern-matching algorithms, IBM Journal of Research and Development 31(2) (1987), 249-260
    locator: the definition of fingerprint functions and their use in pattern matching
  - paper: doi:10.1007/978-1-4613-9323-8_11
    title: Andrei Z. Broder, Some applications of Rabin's fingerprinting method, in Sequences II, Methods in Communication, Security, and Computer Science, Springer (1993), 143-152
    locator: the fingerprint modulo an irreducible polynomial, its error bound, and its applications to file systems and web pages
---

Fingerprinting is the technique of replacing a large object $x$ by a short value $f_k(x)$, its fingerprint, chosen from a family of functions by a random key $k$, so that two objects are compared by comparing their fingerprints. A fingerprint family has two properties: equal objects always have equal fingerprints, and two fixed different objects have equal fingerprints with a small probability $\varepsilon$ over the key. The standard families evaluate a polynomial built from the object at a random point, as in the [polynomial rolling hash](/polynomial-rolling-hash/), or reduce the object modulo a random prime or a random irreducible polynomial. The technique is behind [Rabin-Karp](/rabin-karp/), [string equality testing](/string-equality-testing/), [Freivalds' algorithm](/freivalds-algorithm/) and file deduplication.

## In plain words

A fingerprint is a short summary of something big, like a long file. Two copies of the same file always get the same summary. Two different files get the same summary only by bad luck.

To make the bad luck rare and not under anyone's control, the summary depends on a secret random choice, made after the files exist. With a good method, the chance of bad luck can be computed and made as small as you want, by making the summary a little longer or by repeating the test with new random choices.

A fingerprint never proves that two things are equal. It proves that they differ when the summaries differ, and it makes equality very likely when they agree.

## When it applies

- **Equality is the question.** The task needs to know whether two objects are equal: strings, files, multisets, matrices, polynomials. Fingerprints do not answer order questions or similarity questions directly.
- **The objects are large or far apart.** Reading or sending the objects in full is the cost to avoid, or the same object takes part in many comparisons.
- **A small one-sided error is acceptable, or a check is cheap.** A "different" answer is always right; an "equal" answer is wrong with probability at most $\varepsilon$. If the answer must be exact, verify each "equal" in full, which pays only for the matches.
- **The objects are fixed before the key is drawn.** The bound $\varepsilon$ holds for every fixed pair. An adversary who sees the key, or chooses objects after seeing fingerprints, can find collisions for the algebraic families on this page.

## The template

```pseudo id=main
FINGERPRINT-EQUAL(x, y)
L1  k ← a uniform random key from the key set K        ▷ hole: the family {f_k}
L2  a ← f_k(x); b ← f_k(y)                             ▷ hole: how to compute f_k
L3  if a ≠ b then return DIFFERENT                     ▷ always correct
L4  return PROBABLY-EQUAL                              ▷ hole: accept, repeat, or verify
```

**The holes.**

- *The family.* A set of functions $f_k$ from objects to a small range, with $f_k(x) = f_k(y)$ whenever $x = y$, and $\Pr_k[f_k(x) = f_k(y)] \le \varepsilon$ for each fixed pair $x \ne y$. The fingerprint should take $O(\log n + \log(1/\varepsilon))$ bits for objects of size $n$.
- *The computation.* A good family can be computed in one pass, and it is *composable*: the fingerprint of a concatenation follows from the fingerprints of the parts. For the polynomial hash, $h(uv) = h(u)\, r^{|v|} + h(v) \bmod p$. This gives rolling windows, prefix sums of fingerprints, and trees of fingerprints.
- *The decision.* Accept PROBABLY-EQUAL with error $\varepsilon$ (Monte Carlo), repeat with $t$ independent keys for error $\varepsilon^t$, or verify the objects in full and keep an exact answer (Las Vegas).

**Why it is correct.** If $x = y$, then $f_k(x) = f_k(y)$ for every key, so the method never answers DIFFERENT for equal objects. If $x \ne y$, it answers PROBABLY-EQUAL only when the key lands in the set $\{k : f_k(x) = f_k(y)\}$, whose probability is at most $\varepsilon$ by the property of the family. With $t$ independent keys, all $t$ tests are fooled with probability at most $\varepsilon^t$.

**The standard families.**

| object | fingerprint | key | collision bound for $x \ne y$ |
|---|---|---|---|
| string of length $\le n$ | $\sum_i c(x_i)\, r^{n-1-i} \bmod p$ | base $r \in \{0, \ldots, p-1\}$ | $(n-1)/p$ |
| $n$-bit integer | $x \bmod q$ | prime $q \le M$ | below $n / \pi(M)$ |
| bit string of length $n$ | $x(t) \bmod P(t)$ over GF(2) | irreducible $P$ of degree $k$ | about $n / 2^k$ |
| multiset of $N$ elements of $\mathbb{F}_p$ | $\prod_i (r - a_i) \bmod p$ | point $r \in \mathbb{F}_p$ | $N/p$ |
| $n \times n$ matrix | $A v$ | random vector $v \in \{0, 1\}^n$ | $1/2$ |

The first row is the [polynomial hash collision bound](/polynomial-hash-collision-bound/), for codes from 1 or strings of equal length. The second counts prime factors: a nonzero integer below $2^n$ has fewer than $n$ of them, and $\pi(M)$ is the number of primes up to $M$. The third is the [Rabin fingerprint](/rabin-fingerprint/). The fourth and the first are cases of the [Schwartz-Zippel lemma](/schwartz-zippel-lemma/) in one variable: a nonzero polynomial of degree $d$ over a field has at most $d$ roots. The last is the test of [Freivalds' algorithm](/freivalds-algorithm/): if $A \ne B$, then $Av \ne Bv$ for at least half of the vectors $v \in \{0,1\}^n$.

**Example.** Compare the multisets $A = \{1, 1, 4\}$ and $B = \{1, 2, 3\}$ modulo $p = 13$. A deterministic summary such as the sum fails: both sums are 6. The product fingerprint with the key $r = 5$ gives $F_A = (5-1)(5-1)(5-4) = 16 \equiv 3$ and $F_B = (5-1)(5-2)(5-3) = 24 \equiv 11$, so the multisets differ. The difference of the two polynomials is

$$(t-1)^2(t-4) - (t-1)(t-2)(t-3) = (t-1)\big((t^2 - 5t + 4) - (t^2 - 5t + 6)\big) = -2(t-1),$$

which has the single root $t = 1$. So exactly 1 of the 13 keys fools the test, below the bound $N/p = 3/13$. For the multiset $\{3, 1, 2\}$, which equals $B$, the fingerprint at $r = 5$ is $11$, the same as $F_B$, as it must be for every key.

## Classic examples

- [Rabin-Karp](/rabin-karp/): fingerprints of all text windows, updated in $O(1)$ time each, compared with the fingerprint of the pattern.
- [String equality testing](/string-equality-testing/): two parties compare $n$-bit strings with $O(\log n)$ bits of communication, while a deterministic protocol needs $n + 1$ bits.
- [Freivalds' algorithm](/freivalds-algorithm/): check a matrix product $AB = C$ in $O(n^2)$ time by comparing $A(Bv)$ with $Cv$.
- [Polynomial identity testing](/polynomial-identity-testing/): decide whether a polynomial given as a formula or circuit is zero by evaluating it at a random point.
- [Substring equality queries](/substring-equality-queries/): composable fingerprints of prefixes give the fingerprint of any substring in $O(1)$ time.
- [Rabin fingerprints](/rabin-fingerprint/) in storage systems: content-defined chunking and [deduplication](/dedup/) of file blocks.

## Variations

- **Exact answers by verification.** Use the fingerprint as a filter and compare the objects in full on each match. The time then depends on the number of real matches and of false matches, but the answer is always right.
- **Repetition.** $t$ independent keys give error $\varepsilon^t$ at $t$ times the cost. For a polynomial hash, a single larger prime is usually cheaper than several small ones.
- **Universal hashing.** A fingerprint family with $\varepsilon = O(1/M)$ for a range of size $M$ is an almost [universal hash family](/universal-hash-family/); [universal string hashing](/universal-string-hashing/) combines a polynomial fingerprint with a universal hash of the result to index tables.
- **Similarity sketches.** [MinHash](/minhash/) and other locality-sensitive sketches give equal values with a probability that grows with the similarity of the objects, not only for equal objects. They estimate similarity instead of testing equality.
- **Keyed cryptographic functions.** When an adversary sees the fingerprints, use a [message authentication code](/message-authentication-code/) or a keyed hash such as [SipHash](/siphash/), which are designed to resist chosen inputs.

## Pitfalls

- **No random key.** A fixed function, such as a hash with a constant base, is not a fingerprint family in this sense: the bound $\varepsilon$ is over the key, and with no key there is no probability. Inputs chosen against the fixed function collide; see [anti-hash tests](/anti-hash-tests/).
- **Inputs chosen after the key.** The bound requires the objects to be fixed before the key is drawn. A system that shows its fingerprints to users who then choose inputs loses the bound.
- **One comparison versus many.** The error $\varepsilon$ is for one pair. For $q$ comparisons, the union bound gives $q\varepsilon$; for checking that $N$ objects are all distinct, it gives $\binom{N}{2}\varepsilon$. Choose the size of the fingerprint for the total.
- **Non-prime moduli.** The root-counting argument needs a field. Polynomial hashes modulo $2^{64}$ have no such bound, and Thue-Morse strings collide for every odd base.
- **Deterministic summaries.** Sums, XORs and lengths are not fingerprints: they collide on many natural pairs, such as all anagrams or all permutations of a multiset, whatever the key.
- **Error in the wrong direction.** A fingerprint method errs only by saying "equal". If an application needs no false "equal" (for example, deduplication that could lose data), it must verify or use a fingerprint large enough that the total error is negligible.

## Exercises

1. Show that the fingerprint $f(x) = \sum_i c(x_i) \bmod p$ makes every pair of anagrams collide, for every prime $p$, so it has no useful bound $\varepsilon$.
2. Prove the bound $N/p$ in the multiset row of the table: two different multisets $A, B$ of $N$ elements of $\mathbb{F}_p$ give two different monic polynomials of degree $N$, and their difference has degree less than $N$.
3. Prove the concatenation formula $h(uv) = h(u)\, r^{|v|} + h(v) \bmod p$ for the polynomial hash, and use it to compute the fingerprint of a string of length $2^k$ from the fingerprints of its two halves.
4. A program compares $10^6$ pairs of strings of length at most $10^6$. Which primes $p$ make the union bound on the total error at most $10^{-6}$? *Answer:* $p \ge 10^6 (10^6 - 1) \cdot 10^6$, about $10^{18}$; the Mersenne prime $2^{61} - 1 \approx 2.3 \times 10^{18}$ is enough.
5. Alice and Bob each hold a set of $N$ numbers from $\{0, \ldots, p-1\}$. Give a protocol with $O(\log p)$ bits that decides whether the sets are equal with error at most $N/p$.

## References
