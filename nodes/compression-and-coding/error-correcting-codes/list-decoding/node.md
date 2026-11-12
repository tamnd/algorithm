---
tag: 4JPZFM
kind: problem
slug: list-decoding
name: List decoding
aliases:
- list decoding problem
- list-of-L decoding
area: compression-and-coding/error-correcting-codes
level: advanced
summary: Output all codewords within a given radius of a received word. This allows decoding beyond half the minimum distance, with a short list in place of a single answer.
prereqs: [minimum-distance, hamming-distance]
see_also: [guruswami-sudan, reed-solomon-decoding, berlekamp-welch, elias-bound, channel-capacity, binary-entropy-function, hadamard-code, reed-muller-code]
sources:
  - paper: "P. Elias, List decoding for noisy channels, Technical Report 335, Research Laboratory of Electronics, MIT, 1957"
    title: P. Elias, List decoding for noisy channels, 1957
    locator: The definition of a decoder that outputs a list, and its error exponent for random codes
  - paper: "J. M. Wozencraft, List decoding, Quarterly Progress Report 48, Research Laboratory of Electronics, MIT, 1958"
    title: J. M. Wozencraft, List decoding, 1958
    locator: The note that introduces the term list decoding
  - paper: doi:10.1109/TIT.1962.1057714
    title: S. M. Johnson, A new upper bound for error-correcting codes, IRE Transactions on Information Theory 8(3), 1962
    locator: The bound on the number of codewords in a ball, which gives the Johnson radius
  - paper: doi:10.1006/jcom.1997.0439
    title: M. Sudan, Decoding of Reed Solomon codes beyond the error-correction bound, Journal of Complexity 13(1), 1997
    locator: The first polynomial time list decoder for Reed-Solomon codes beyond half the distance
  - paper: doi:10.1109/18.782097
    title: V. Guruswami and M. Sudan, Improved decoding of Reed-Solomon and algebraic-geometry codes, IEEE Transactions on Information Theory 45(6), 1999
    locator: The list decoder with multiplicities up to the Johnson radius n - sqrt(n(k - 1))
  - paper: doi:10.1109/TIT.2007.911222
    title: V. Guruswami and A. Rudra, Explicit codes achieving list decoding capacity, error-correction with optimal redundancy, IEEE Transactions on Information Theory 54(1), 2008
    locator: Folded Reed-Solomon codes list decodable up to a fraction 1 - R - epsilon of errors
  - url: https://cse.buffalo.edu/faculty/atri/courses/coding-theory/book/
    title: V. Guruswami, A. Rudra and M. Sudan, Essential Coding Theory (book draft)
    locator: The chapters on list decoding (the Johnson bound and list decoding capacity) and on the decoding of Reed-Solomon and folded Reed-Solomon codes
  - paper: "O. Goldreich and L. A. Levin, A hard-core predicate for all one-way functions, Proceedings of the 21st ACM Symposium on Theory of Computing, 1989"
    title: O. Goldreich and L. A. Levin, A hard-core predicate for all one-way functions, 1989
    locator: The local list decoder for the Hadamard code
---

List decoding is the problem of finding every codeword within a given distance $e$ of a received word. A unique decoder must stop at $e < d/2$, where $d$ is the [minimum distance](/minimum-distance/), because two codewords at distance $d$ have a word halfway between them. A list decoder goes further and returns a short list. Peter Elias (1957) and John Wozencraft (1958) introduced the idea for the analysis of noisy channels. The Johnson bound says that every code has lists of polynomial size up to a radius of about $n - \sqrt{n(n-d)}$. List decoding capacity says that codes of rate $R = 1 - h_q(p) - \varepsilon$ exist that are list decodable up to a fraction $p$ of errors. For large alphabets this radius $p$ is close to $1 - R$, twice the unique decoding radius $(1 - R)/2$. The [Guruswami-Sudan algorithm](/guruswami-sudan/) reaches the Johnson radius for Reed-Solomon codes, and folded Reed-Solomon codes reach capacity.

## In plain words

A decoder that must give one answer can only fix errors up to half the distance between codewords. With more errors, the received word can be just as close to two codewords, and the decoder cannot choose. A list decoder does not choose. It returns every codeword that is close enough. The list is almost always short, often just one codeword, and the receiver can pick the right one with a little extra information, such as a checksum. This doubles the number of errors that a good code can handle.

## Definition

Let $C \subseteq \Sigma^n$ be a code over an alphabet of size $q$, with minimum distance $d$, and let $\Delta$ be the [Hamming distance](/hamming-distance/).

**Problem.** Given $y \in \Sigma^n$ and a radius $e$, output the list

$$\mathcal{L}(y, e) = \{ c \in C : \Delta(c, y) \le e \}.$$

**Combinatorial version.** $C$ is $(p, L)$-list decodable if $|\mathcal{L}(y, pn)| \le L$ for every $y \in \Sigma^n$. The algorithmic problem is useful only when $L$ is small, constant or polynomial in $n$, because the decoder must at least write the list.

With $e < d/2$, the list has at most one element, and the problem is unique (bounded distance) decoding. With $e \ge d/2$, the list can have more than one element. For a received word, the ball of radius $e$ can also be empty, and then the list is empty.

The rate is $R = \log_q |C| / n$, and the relative distance is $\delta = d/n$.

## Variants

- **Algorithmic list decoding.** Output $\mathcal{L}(y, e)$ in time polynomial in $n$. This is the usual meaning.
- **List decoding with a list size bound.** Output a list of at most $L$ codewords that contains every codeword within the radius.
- **List recovery.** Each position has a set of up to $\ell$ allowed symbols, and the output is every codeword that agrees with the sets at enough positions. Concatenated codes and expander based codes use it.
- **Soft decision list decoding.** Each position has a weight for each symbol, and the output is every codeword with enough total weight. The Koetter-Vardy algorithm does this for Reed-Solomon codes.
- **Local list decoding.** Each codeword in the list is given by a small program that computes any of its symbols with few queries to $y$. The Goldreich-Levin algorithm does this for the [Hadamard code](/hadamard-code/).
- **List decoding with erasures** and **average radius list decoding**, where the average distance of the list to $y$, not each distance, is bounded.

## Examples

**Reed-Solomon over GF(7).** Take the code $\{(f(1), \ldots, f(6)) : f \in \mathrm{GF}(7)[x],\ \deg f < 2\}$, the lines over $\mathrm{GF}(7)$. It has $n = 6$, $k = 2$ and $d = 5$, so the unique decoding radius is 2. Let $y = (0, 0, 0, 4, 5, 6)$.

| radius $e$ | list | size |
|---|---|---|
| 2 | none | 0 |
| 3 | $f = 0$, which agrees at the points 1, 2, 3, and $f = x$, which agrees at 4, 5, 6 | 2 |
| 4 | 11 lines | 11 |

A unique decoder fails here. A list decoder with radius 3 returns two candidates. At radius 3 the Johnson bound below gives at most 4 codewords; at radius 4 it does not apply, and the list has 11 of the 49 codewords.

**Reed-Muller RM(1, 4).** This binary $[16, 5, 8]$ code has unique decoding radius 3. At radius 4, among all $2^{16}$ received words, 15232 have an empty list, 22304 have one codeword, 26880 have two, and 1120 have four. The Johnson bound for $n = 16$, $d = 8$, $e = 4$ is also 4, so it is tight for this code.

**Reed-Solomon codes of rate 1/2.** Unique decoding corrects a fraction $0.25$ of errors. The Guruswami-Sudan algorithm corrects a fraction close to $1 - \sqrt{1/2} \approx 0.293$, and folded Reed-Solomon codes of rate $1/2$ can be list decoded up to a fraction close to $0.5$.

**Binary codes of rate 1/2.** The list decoding capacity is the $p$ with $h_2(p) = 1/2$, which is $p \approx 0.110$. See the [binary entropy function](/binary-entropy-function/).

## Known algorithms

| algorithm | code | radius (fraction of $n$) | time |
|---|---|---|---|
| brute force | any | any | $O(\lvert C \rvert\, n)$ |
| unique decoders ([Berlekamp-Welch](/berlekamp-welch/), [Reed-Solomon decoding](/reed-solomon-decoding/)) | Reed-Solomon | $(1 - R)/2$ | polynomial |
| Goldreich and Levin (1989) | Hadamard | $1/2 - \varepsilon$, local | $\mathrm{poly}(\log n, 1/\varepsilon)$ queries |
| Sudan (1997) | Reed-Solomon | about $1 - \sqrt{2R}$ | polynomial |
| [Guruswami-Sudan](/guruswami-sudan/) (1999) | Reed-Solomon, algebraic geometry codes | $1 - \sqrt{R}$, the Johnson radius | polynomial |
| Koetter and Vardy (2003) | Reed-Solomon, soft decision | depends on the reliabilities | polynomial |
| Parvaresh and Vardy (2005) | Parvaresh-Vardy codes | above $1 - \sqrt{R}$ for low rates | polynomial |
| Guruswami and Rudra (2008) | folded Reed-Solomon | $1 - R - \varepsilon$, capacity | $n^{O(1/\varepsilon)}$ |

## Bounds

**Johnson bound.** Let $C$ have length $n$ and distance $d$, and let $y$ be any word. Suppose $L$ codewords agree with $y$ in at least $a$ positions each, and put $s = n - d$, the most positions in which two codewords can agree. If $a^2 > n s$, then

$$L \le \frac{n (a - s)}{a^2 - n s}.$$

*Proof sketch.* Let $x_j$ be the number of the $L$ codewords that agree with $y$ at position $j$. Then $\sum_j x_j \ge L a$, and $\sum_j x_j (x_j - 1)$ counts ordered pairs of codewords that agree with $y$, and so with each other, at a position, which is at most $L(L-1) s$. By the Cauchy-Schwarz inequality, $\sum_j x_j^2 \ge (L a)^2 / n$. Combining, $L a^2 / n - a \le (L - 1) s$, which gives the bound.

So every code has lists of size at most $n^2$ up to the radius $e < n - \sqrt{n(n-d)}$, a fraction $1 - \sqrt{1 - \delta}$ of the length. With the alphabet size $q$, a sharper form gives the radius $J_q(\delta) = (1 - 1/q)\bigl(1 - \sqrt{1 - q\delta/(q-1)}\bigr)$. For Reed-Solomon codes, $\delta \approx 1 - R$, and the Johnson radius is $1 - \sqrt{R}$, larger than $(1 - R)/2$ for every $0 < R < 1$.

**List decoding capacity.** For $0 \le p < 1 - 1/q$ and $\varepsilon > 0$:

- there are codes of rate $R \ge 1 - h_q(p) - \varepsilon$ that are $(p, O(1/\varepsilon))$-list decodable; random codes have this property with high probability;
- every code of rate $R \ge 1 - h_q(p) + \varepsilon$ has a ball of radius $p n$ with $q^{\Omega(\varepsilon n)}$ codewords.

Here $h_q$ is the $q$-ary entropy, which for $q = 2$ is the [binary entropy function](/binary-entropy-function/). As $q$ grows, $h_q(p) \to p$, so the capacity radius approaches $1 - R$: with $k$ symbols of message, one can hope to recover from any $n - k(1 + \varepsilon)$ errors. The capacity mirrors the [channel capacity](/channel-capacity/) $1 - h_q(p)$ of the $q$-ary symmetric channel, but holds for worst case errors.

**Unique decoding.** No code can be uniquely decoded beyond $d/2$, and with $d \le n - k + 1$ (the [Singleton bound](/singleton-bound/)), unique decoding is limited to a fraction $(1 - R)/2$.

## Reductions

- **Unique decoding from list decoding.** Run the list decoder with radius $\lfloor (d-1)/2 \rfloor$ or more and return the nearest codeword in the list.
- **Reed-Solomon list decoding is polynomial reconstruction.** Given $n$ points $(a_i, y_i)$ and a number $a$, find every polynomial of degree less than $k$ that passes through at least $a$ of them. The Guruswami-Sudan algorithm reduces it to bivariate interpolation and the root finding of a polynomial in $y$ over $\mathrm{GF}(q)[x]$.
- **Hard-core predicates.** Goldreich and Levin showed that the inner product bit $\langle x, r \rangle$ is a hard-core predicate of any one-way function by local list decoding of the Hadamard code.
- **Hardness amplification and extractors.** Local list decoding of Reed-Muller codes and of concatenated codes turns a function that is hard in the worst case into one that is hard on average, and list decodable codes give randomness extractors.

## Applications

- Decoding Reed-Solomon codes in storage and communication beyond half the distance, with the soft decision variants of Koetter and Vardy.
- Complexity theory: hard-core predicates, hardness amplification, pseudorandom generators, randomness extractors and probabilistically checkable proofs.
- Cryptography: traitor tracing schemes and the analysis of learning problems with noise.
- Information theory: list decoding was first used for error exponents of random codes, and list decoding capacity matches the capacity of the $q$-ary symmetric channel.

## References
