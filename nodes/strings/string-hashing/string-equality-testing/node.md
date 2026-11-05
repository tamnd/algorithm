---
tag: XA2QCG
kind: problem
slug: string-equality-testing
name: String equality testing
aliases:
- checking whether two strings are equal
area: strings/string-hashing
level: intro
summary: Decide whether two strings are equal when reading both in full is too costly, using fingerprints with small error.
model: word-ram
complexity:
  vars: {n: the length of the strings}
  time: {worst: Θ(n)}
  space: {extra: O(1)}
prereqs: [polynomial-rolling-hash, polynomial-hash-collision-bound]
see_also: [fingerprinting, communication-complexity, randomized-communication-complexity, substring-equality-queries, rabin-fingerprint, checksum, cryptographic-hash-function, polynomial-identity-testing]
sources:
  - book: isbn:9780521474658
    title: Rajeev Motwani and Prabhakar Raghavan, Randomized Algorithms, Cambridge University Press, 1995
    locator: Chapter 7, Algebraic techniques (the sections on fingerprinting and on verifying the equality of two strings held by two parties)
  - book: isbn:9780521560672
    title: Eyal Kushilevitz and Noam Nisan, Communication Complexity, Cambridge University Press, 1997
    locator: Chapter 1 (the equality function and the fooling set bound) and Chapter 3 (randomized protocols for equality with private and public coins)
  - book: isbn:9780262046305
    title: Cormen, Leiserson, Rivest and Stein, Introduction to Algorithms, fourth edition
    locator: Section 32.2, The Rabin-Karp algorithm (the exercise on comparing two long files by a random polynomial evaluation)
  - paper: doi:10.1147/rd.312.0249
    title: Richard M. Karp and Michael O. Rabin, Efficient randomized pattern-matching algorithms, IBM Journal of Research and Development 31(2) (1987), 249-260
    locator: the use of fingerprints to compare strings and the bound on the error probability
---

String equality testing asks whether two strings $x$ and $y$ are equal. On one machine the answer takes $\Theta(n)$ time and is easy; the problem becomes interesting when the strings are far apart, so that sending them is the cost, or when the same strings are compared many times. Then each string is replaced by a short [fingerprint](/fingerprinting/), such as a [polynomial hash](/polynomial-rolling-hash/) with a random base modulo a prime $p$, and the fingerprints are compared instead. Equal strings always give equal fingerprints, and two fixed different strings of length at most $n$ give equal ones with probability at most $(n-1)/p$. In [communication complexity](/communication-complexity/), this turns the $n + 1$ bits that a deterministic protocol needs into $O(\log n)$ bits.

## In plain words

Two people each have a copy of a very long file, in two different cities. They want to know if the copies are the same, without sending a whole file over the line.

One of them picks a random number and computes a short summary of the file that depends on it. She sends the random number and the summary. The other computes the summary of his own file with the same random number and compares. If the files are equal, the summaries are equal. If the files differ, the summaries differ except with a tiny chance, which depends on the random number and not on the files. The message is a few dozen digits long, even for a file of many gigabytes.

## Definition

**Input.** Two strings $x, y$ over an alphabet $\Sigma$ with integer codes $c(a) \in \{0, \ldots, \sigma - 1\}$. Indices are 0-based. Write $n = \max(|x|, |y|)$.

**Output.** Yes if $x = y$, that is $|x| = |y|$ and $x_i = y_i$ for all $i$; no otherwise.

**Settings.**

- *Local.* Both strings are in one memory. Cost: time.
- *Two parties.* Alice holds $x$ and Bob holds $y$, both of length $n$ bits; they exchange messages, and one of them outputs the answer. Cost: the number of bits sent. This is the equality function $\mathrm{EQ}_n$ of communication complexity.
- *Stored fingerprints.* Many strings are stored with a fingerprint each, and pairs are compared later. Cost: time per comparison after the fingerprints exist.

**Error.** A randomized method may answer yes when $x \ne y$, with probability at most $\varepsilon$ over its own random choices, for every fixed input pair. It never answers no when $x = y$. This is one-sided error.

## Variants

- **Equal lengths.** If the lengths differ, the answer is no at once. So the hard case is $|x| = |y| = n$, and the polynomial hash may use the code 0 there; for strings of different lengths the codes must be nonzero, or the lengths must be compared first.
- **Many strings.** Decide whether all of $x^{(1)}, \ldots, x^{(N)}$ are distinct, or group them into classes of equal strings. Sort or hash the fingerprints; by the union bound over $\binom{N}{2}$ pairs, the error is at most $\binom{N}{2}(n-1)/p$.
- **Substrings.** Compare substrings of one string, many times: [substring equality queries](/substring-equality-queries/).
- **Streaming.** The strings arrive one character at a time, and only $O(1)$ words of memory are allowed. Horner's rule computes the polynomial hash on the fly, so the fingerprint method works in the [streaming model](/streaming-model/).
- **Adversarial setting.** If an adversary chooses $y$ after seeing the fingerprint function, a random-base hash gives no guarantee; a [cryptographic hash function](/cryptographic-hash-function/) or a [message authentication code](/message-authentication-code/) is then the right tool.

## Examples

Alice holds $x = 10110010$ and Bob holds $y = 10100011$, so $n = 8$, with the bits as codes. They use the prime $p = 67 \ge n^2$, and Alice draws $r = 13$.

- Alice computes $h_{13}(x) = 13$ by Horner's rule and sends $(13, 13)$, the base and the hash.
- Bob computes $h_{13}(y) = 62 \ne 13$ and answers no, which is right.

The difference polynomial is $D(t) = t^4 - 1$: the strings differ in the bit of weight $t^4$ (1 against 0) and in the last bit (0 against 1). Modulo 67, $t^4 = 1$ has exactly the roots $1$ and $66$, because $\gcd(4, 66) = 2$. So 2 of the 67 bases give a wrong yes, a probability of $2/67 \approx 0.03$, below the bound $(n-1)/p = 7/67 \approx 0.10$.

For such short strings the message is longer than the strings. The gain appears for long ones: with $n = 10^9$ bits and the fixed public prime $p = 2^{61} - 1$, Alice sends $r$ and $h_r(x)$, 122 bits in all, and a wrong yes has probability at most $(10^9 - 1)/(2^{61} - 1) < 4.4 \times 10^{-10}$.

## Known algorithms

- **Direct comparison.** Compare the lengths, then the characters from left to right, and stop at the first difference: $\Theta(n)$ time in the worst case, no error. In the two-party setting, Alice sends all of $x$: $n$ bits, plus one bit for the answer.
- **Random-base polynomial fingerprint.** Fix a prime $p$, draw $r$ uniformly from $\{0, \ldots, p-1\}$, and compare $h_r(x)$ with $h_r(y)$, where $h_r(x) = \sum_i c(x_i)\, r^{|x|-1-i} \bmod p$. Error at most $(n-1)/p$ by the [collision bound](/polynomial-hash-collision-bound/). With $p$ between $n^2$ and $2n^2$, the message $(p, r, h_r(x))$ has $O(\log n)$ bits and the error is below $1/n$.
- **Random-prime fingerprint.** Read $x$ and $y$ as $n$-bit integers, draw a random prime $q$ from the primes up to $M$, and compare $x \bmod q$ with $y \bmod q$. The nonzero integer $|x - y| < 2^n$ has fewer than $n$ distinct prime factors, so the error is below $n/\pi(M)$, where $\pi(M) \approx M / \ln M$ by the [prime number theorem](/prime-number-theorem/). This is the fingerprint of Karp and Rabin.
- **Public coin.** If Alice and Bob share random bits, they can compare $k$ random parities of $x$ and $y$ (inner products with random vectors modulo 2). Each parity of $x \oplus y \ne 0$ is 1 with probability $1/2$, so $k$ bits give error $2^{-k}$, independent of $n$.
- **Fingerprints over GF(2).** The [Rabin fingerprint](/rabin-fingerprint/) takes $x$ modulo a random irreducible polynomial of degree $k$ over GF(2), with error about $n/2^k$.

## Bounds

- **Local, deterministic.** Any algorithm that answers correctly for all inputs of length $n$ reads all $2n$ characters in the worst case, when $x = y$: if it does not read position $i$ of $x$, changing $x_i$ gives a pair with the same reads and the opposite answer.
- **Two parties, deterministic: $n + 1$ bits.** The $2^n$ pairs $(x, x)$ form a fooling set: no two of them can end in the same transcript, because a transcript shared by $(x, x)$ and $(x', x')$ would also be followed by $(x, x')$, whose answer is no. So there are at least $2^n$ transcripts with answer yes and at least one with answer no, and at least $\lceil \log_2(2^n + 1) \rceil = n + 1$ bits in the worst case. Sending $x$ and one answer bit meets this.
- **Two parties, randomized.** With private coins and constant error, $\Theta(\log n)$ bits are necessary and sufficient; the polynomial fingerprint gives the upper bound. With public coins, $O(1)$ bits suffice for constant error. These results are in the cited book of Kushilevitz and Nisan.
- **The cost of a small error.** For error $\varepsilon$, the polynomial fingerprint needs $p \ge (n-1)/\varepsilon$, so $O(\log n + \log(1/\varepsilon))$ bits.

## Reductions

- **To polynomial identity testing.** The strings are equal if and only if the polynomials $\sum_i c(x_i)\, t^{n-1-i}$ and $\sum_i c(y_i)\, t^{n-1-i}$ are equal, so string equality is the one-variable case of [polynomial identity testing](/polynomial-identity-testing/), and the fingerprint is the [Schwartz-Zippel](/schwartz-zippel-lemma/) test.
- **From string matching.** A pattern $P$ occurs at $s$ in $T$ if and only if $P = T[s \ldots s + m - 1]$. [Rabin-Karp](/rabin-karp/) runs $n - m + 1$ such tests with rolling fingerprints.
- **To set equality and verification.** Comparing two multisets, or checking that a matrix product is right, uses the same idea of evaluating at a random point; see [Freivalds' algorithm](/freivalds-algorithm/).

## Applications

- **Remote file comparison.** Compare files or blocks on two machines by their fingerprints, and send only the blocks whose fingerprints differ.
- **Deduplication.** Store one copy of each distinct block by keying blocks on fingerprints: [dedup](/dedup/).
- **Hash tables of strings.** Compare stored hash values before the strings, so most unequal keys are rejected in $O(1)$ time.
- **Substring and pattern problems.** [Rabin-Karp](/rabin-karp/) and [substring equality queries](/substring-equality-queries/) reduce many string comparisons to comparisons of numbers.
- **Integrity checks.** A [checksum](/checksum/) detects accidental changes; against deliberate changes, a [cryptographic hash function](/cryptographic-hash-function/) is needed.

## References
