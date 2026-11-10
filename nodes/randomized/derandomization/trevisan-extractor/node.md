---
tag: ENJAWZ
kind: algorithm
slug: trevisan-extractor
name: Trevisan's extractor
aliases:
- Trevisan extractor construction
area: randomized/derandomization
level: advanced
summary: A seeded extractor that encodes the source with a list-decodable code and outputs the codeword bits at m overlapping slices of the seed, as in the Nisan-Wigderson generator.
solves: [randomness-extraction]
model: word-ram
complexity:
  vars: {m: "the number of output bits", n: "the length of the source, with field elements of t bits held in one word"}
  time: {worst: Θ(m·n), average: Θ(m·n), best: Θ(m·n)}
  space: {extra: Θ(m)}
properties: {in_place: false, online: true, deterministic: true, recursive: false}
history:
  year: 2001
  people: [Luca Trevisan]
  note: Trevisan presented the construction at STOC 1999, and the journal version appeared in 2001.
prereqs: [nisan-wigderson-generator, randomness-extractor, list-decoding, hadamard-code]
see_also: [seeded-extractor, randomness-extractor, nisan-wigderson-generator, leftover-hash-lemma, list-decoding, reed-solomon-code, hadamard-code, concatenated-codes]
sources:
  - paper: doi:10.1145/502090.502099
    title: Luca Trevisan, Extractors and pseudorandom generators, Journal of the ACM 48(4), 2001
    locator: the construction, the reconstruction argument and the parameters of the extractor
  - paper: doi:10.1006/jcss.2002.1824
    title: Ran Raz, Omer Reingold and Salil Vadhan, Extracting all the randomness and reducing the error in Trevisan's extractors, Journal of Computer and System Sciences 65(1), 2002
    locator: weak designs, the strong form of the extractor, and the improved output length
  - paper: doi:10.1561/0400000010
    title: Salil P. Vadhan, Pseudorandomness, Foundations and Trends in Theoretical Computer Science 7(1 to 3), 2012
    locator: Chapter 5 (list decoding and the Johnson bound) and Chapter 7 (Trevisan's extractor as a black-box generator construction)
  - paper: doi:10.1016/S0022-0000(05)80043-1
    title: Noam Nisan and Avi Wigderson, Hardness vs randomness, Journal of Computer and System Sciences 49(2), 1994
    locator: designs and the generator that the extractor reuses
---

Trevisan's extractor is a [seeded extractor](/seeded-extractor/) built from the [Nisan-Wigderson generator](/nisan-wigderson-generator/). It encodes the source $x$ with an error-correcting code $C$ that has good [list decoding](/list-decoding/), and outputs the bits of $C(x)$ at the positions $y|_{S_1}, \ldots, y|_{S_m}$, where $y$ is the seed and $S_1, \ldots, S_m$ are sets with small overlaps. The source plays the role of the hard function. Trevisan's insight was that the proof of the NW generator never uses the hardness of $f$ except to say that $f$ has no short description; a source of high min-entropy has the same property for most of its values. The extractor has a seed of $O(\log^2(n/\varepsilon)/\log k)$ bits, which is $O(\log n)$ when $k = n^{\Omega(1)}$ and $\varepsilon = 1/\mathrm{poly}(n)$. The analysis is unconditional.

## In plain words

Take the weak random string and stretch it with an error-correcting code, so that every part of the long string depends on all of the short one. Then read single bits of the long string at places chosen by a short truly random seed. Each output bit uses a different slice of the seed, and the slices overlap only a little.

Why is the output random? Suppose some test could tell it from fair coins for many source strings. Then the test, plus a few hundred hints, would let one rebuild each of those source strings. A short list of hints can rebuild only a few strings. A source with enough randomness puts little weight on any few strings, so the test cannot work for most of the source.

## The problem

Given $n$, a min-entropy $k$, an error $\varepsilon$ and an output length $m$, find an explicit function $\mathrm{Ext} : \{0,1\}^n \times \{0,1\}^d \to \{0,1\}^m$ such that for every random variable $X$ with $\Pr[X = x] \le 2^{-k}$ for all $x$, $\mathrm{Ext}(X, U_d)$ is $\varepsilon$-close to $U_m$ in statistical distance. The seed length $d$ should be short, ideally $O(\log n)$. This is [randomness extraction](/randomness-extraction/) with a seed.

**Ingredients.**

- A code $C : \{0,1\}^n \to \{0,1\}^{2^\ell}$, with positions indexed by $\ell$-bit strings, such that every word has at most $L$ codewords with agreement at least $\frac12 + \varepsilon/m$. This implementation uses the [Reed-Solomon code](/reed-solomon-code/) over $\mathrm{GF}(2^t)$ [concatenated](/concatenated-codes/) with the [Hadamard code](/hadamard-code/), so $\ell = 2t$.
- An $(\ell, a)$ design: sets $S_1, \ldots, S_m \subseteq [d]$ of size $\ell$ with $|S_i \cap S_j| \le a$ for $i \ne j$. This implementation uses the polynomial design over a prime field $\mathrm{GF}(q)$ with $\ell \le q$: for each polynomial $p$ of degree less than $r$, the set $\{(\alpha, p(\alpha)) : \alpha < \ell\}$, with the point $(\alpha, \beta)$ numbered $\alpha q + \beta$. So $d = \ell q$, $m \le q^r$ and $a = r - 1$.

## The algorithm

For a seed $y \in \{0,1\}^d$, $y|_S$ is the string of the bits of $y$ at the positions in $S$, in increasing order. The source $x$ is read as $n/t$ elements $x_0, x_1, \ldots$ of $\mathrm{GF}(2^t)$, with $n/t \le 2^t$, and $p_x(\alpha) = \sum_j x_j \alpha^j$.

```pseudo id=main
TREVISAN(x, y)                          ▷ x ∈ {0,1}^n, y ∈ {0,1}^d, design S_1 … S_m
L1  for i ← 1 to m do
L2      z ← y|S_i                       ▷ ℓ = 2t seed bits
L3      out_i ← RSH-BIT(x, z)           ▷ bit z of C(x); the codeword is never built
L4  return out_1 … out_m

RSH-BIT(x, z)
L5  α ← the first t bits of z; β ← the last t bits of z
L6  v ← p_x(α) in GF(2^t), by Horner's rule
L7  return ⟨v, β⟩ mod 2                 ▷ inner product of t-bit vectors
```

## Example

**A toy with the Hadamard code.** Take $n = 3$ and the Hadamard code $C(x)_z = \langle x, z \rangle \bmod 2$, so $\ell = 3$. The design is the nine lines over $\mathrm{GF}(3)$, the same as in the [NW example](/nisan-wigderson-generator/), with $d = 9$ and $a = 1$. For $x = 101$ and $y = 101100110$:

| line $(c_0, c_1)$ | (0,0) | (0,1) | (0,2) | (1,0) | (1,1) | (1,2) | (2,0) | (2,1) | (2,2) |
|---|---|---|---|---|---|---|---|---|---|
| $S_i$ | 0,3,6 | 0,4,8 | 0,5,7 | 1,4,7 | 1,5,6 | 1,3,8 | 2,5,8 | 2,3,7 | 2,4,6 |
| $z = y\vert_{S_i}$ | 111 | 100 | 101 | 001 | 001 | 010 | 100 | 111 | 101 |
| $\langle 101, z \rangle$ | 0 | 1 | 0 | 1 | 1 | 0 | 1 | 0 | 0 |

The output is $010110100$. Here $m = 9 = d$, so nothing is gained; the toy shows only the shape. With $m = 1$ the extractor is the inner product with a slice of the seed, which is a strong extractor by the [leftover hash lemma](/leftover-hash-lemma/).

**The inner code.** Take $t = 2$, $\mathrm{GF}(4)$ with the modulus $u^2 + u + 1$, and the source $x = 1001$, read as $x_0 = 1$ and $x_1 = 2$ (the element $u$). Then $p_x(\alpha) = 1 + 2\alpha$ takes the values $1, 3, 2, 0$ at $\alpha = 0, 1, 2, 3$. Bit $(\alpha, \beta)$ of $C(x)$ is the inner product of $p_x(\alpha)$ with $\beta$, so $C(x)$ has 16 bits. For $t = 2$ and $n = 4$, two different codewords differ in at least $(4 - 2 + 1) \cdot 2 = 6$ positions, and this bound is reached.

**A full-size instance.** With $t = 61$ and $n = 61 \cdot 17189 = 1048529$, take $\ell = 122$, $q = 127$, $r = 2$ and $\varepsilon = 2^{-10}$. Then $d = 122 \cdot 127 = 15494$, $m = 127^2 = 16129$ and $a = 1$. The list bound gives $L \le 2^{47}$, and the theorem below gives a $(k, 2^{-9})$-extractor for $k \ge 48457$. The extractor outputs more bits than its seed from any source with about one bit of min-entropy per 22 bits of length.

## Correctness

The full proof is in [proofs/correctness.md](proofs/correctness.md).

**Theorem.** Let $C$ be injective, with at most $L$ codewords of agreement at least $\frac12 + \varepsilon/m$ with any word, and let $S_1, \ldots, S_m$ be an $(\ell, a)$ design. If

$$k \ge (m - 1)2^a + m + \lceil \log_2 m \rceil + 1 + \log_2 L + \log_2(1/\varepsilon),$$

then $\mathrm{Ext}(x, y) = (C(x)_{y|_{S_1}}, \ldots, C(x)_{y|_{S_m}})$ is a $(k, 2\varepsilon)$-extractor.

The proof is the NW reconstruction with the source in place of the hard function. Fix a test $T$ and call $x$ bad if $T$ tells $\mathrm{Ext}(x, U_d)$ from $U_m$ with advantage more than $\varepsilon$. For a bad $x$, the hybrid argument gives a position $i$ and a predictor for bit $i$ from bits $1, \ldots, i - 1$ with success more than $\frac12 + \varepsilon/m$. Fix the seed bits outside $S_i$ and the random bits of the predictor. The earlier output bits then depend on at most $a$ bits of $z = y|_{S_i}$ each, so they are tables of $2^a$ bits. The predictor becomes a word $R$ that agrees with $C(x)$ on more than $\frac12 + \varepsilon/m$ of the positions, and $R$ is determined by about $m 2^a$ bits of advice that do not include $x$. So there are at most $2^{m 2^a + O(m)} L$ bad strings, and a source of min-entropy $k$ gives them total weight at most $\varepsilon$.

The proof also shows that the code of RSH-BIT has small lists. Two different codewords agree on at most $\frac12 + \gamma$ of the positions with $\gamma = (n/t - 1)/2^{t+1}$, and then at most $1/(4\delta^2 - 2\gamma)$ codewords have agreement $\frac12 + \delta$ with any word, by the Cauchy-Schwarz inequality.

**Parameters (cited).** Trevisan (2001) shows that for every constant $\alpha > 0$, with suitable designs, the construction gives a $(k, \varepsilon)$-extractor with output $m = k^{1-\alpha}$ and seed $d = O(\log^2(n/\varepsilon)/\log k)$. For $k = n^{\Omega(1)}$ and $\varepsilon = 1/\mathrm{poly}(n)$ the seed is $O(\log n)$. Raz, Reingold and Vadhan (2002) show that the extractor is strong and, with weak designs and a repetition step, extract almost all of the min-entropy at the cost of a longer seed.

## Complexity

- **Time.** Each output bit needs $2t$ seed bits for line L2 and one evaluation of $p_x$ for line L6: $n/t$ multiplications in $\mathrm{GF}(2^t)$. With a $t$-bit element in one word, a multiplication by shift and add takes $O(t)$ word operations, so one bit costs $O(n)$ and the output costs $\Theta(m \cdot n)$. With table lookups for field multiplication, one bit costs $O(n/t)$.
- **Design.** The polynomial design is computed on the fly: set $i$ is the graph of the polynomial with coefficient list number $i$, so $y|_{S_i}$ costs $O(\ell r)$ field operations over $\mathrm{GF}(q)$.
- **Space.** $\Theta(m)$ for the output, plus $O(n)$ for the source. The codeword of length $2^{2t}$ is never stored.

## Properties

- **Unconditional.** No hardness assumption is used. The reconstruction counts descriptions instead of bounding circuit size.
- **Strong.** The output is close to uniform even given the seed (Raz, Reingold and Vadhan 2002). The simple proof above shows only the ordinary form.
- **Local.** Each output bit depends on one bit of $C(x)$, and that bit depends on all of $x$ through $p_x(\alpha)$.
- **Black-box.** The proof works for any test, of any complexity. It is the information-theoretic form of the NW proof.
- **Parallel.** The output bits can be computed in any order.

## Variants and improvements

- **Weak designs.** Raz, Reingold and Vadhan (2002) replace the bound $|S_i \cap S_j| \le a$ by a bound on $\sum_{j < i} 2^{|S_i \cap S_j|}$. This is exactly the size of the advice in the proof, and it allows shorter seeds.
- **Extracting more.** Repeating the extractor with independent seeds on the same source, as on the [seeded extractor](/seeded-extractor/) page, raises the output from $k^{1-\alpha}$ to almost $k$.
- **Codes.** Any code with a good list-size bound works. The Hadamard code alone needs $\ell = n$ and a long seed. Reed-Solomon concatenated with Hadamard gives $\ell = O(\log(n/\varepsilon))$. Other constructions use Reed-Muller codes, which also give the multilinear and low-degree extractors of Ta-Shma, Zuckerman and Safra and of Shaltiel and Umans.
- **Seeds of optimal length.** Guruswami, Umans and Vadhan (2009) reach a seed of $O(\log n + \log(1/\varepsilon))$ with output $(1 - \alpha)k$ by a different method, condensers from Parvaresh-Vardy codes.

## When to use it

- When a short seed matters more than the output length, for example to simulate randomized algorithms with a weak source by trying all seeds.
- When the extractor must be easy to analyze and to compute bit by bit.
- When a strong extractor with a seed much shorter than the [leftover hash lemma](/leftover-hash-lemma/) needs is required. If the seed may be long and the output should keep almost all of the entropy, the leftover hash lemma is simpler.

## Pitfalls

- The design must keep the overlaps small. The advice grows like $m 2^a$, so $a$ must be about $\log(k/m)$ or less.
- The code must be list-decodable at radius $\frac12 - \varepsilon/m$, not $\frac12 - \varepsilon$. The hybrid argument loses a factor $m$.
- Unique decoding is not enough: no binary code can be uniquely decoded close to radius $\frac12$. The argument needs only that the list is short, not that it can be found fast.
- The polynomial design needs $r \le \ell$; otherwise two coefficient lists can give the same set.
- The seed must be uniform and independent of the source. Reusing a seed that depends on the source breaks the analysis.
- The error $2\varepsilon$ is for the ordinary extractor. Using it as a strong extractor needs the strong analysis.

## Implementations

The Python implementation in `impl/python/trevisan_extractor.py` uses the standard library only. It implements $\mathrm{GF}(2^t)$ for $t \le 8$, the Hadamard code, the Reed-Solomon code concatenated with the Hadamard code, the polynomial design, and the word $R$ of the reconstruction step. The tests check the field and the design, the worked examples, the list bound for the Hadamard code with Parseval's identity, the exact minimum distance of the concatenated code for small $t$, the list bound on random and noisy words, the leftover hash bound for one output bit on every flat source with $n = 3$, and the reconstruction exactly: for every source, test, position and fixing, the average agreement of $R$ with $C(x)$ equals $\frac12 + p_i - p_{i-1}$, and list decoding of $R$ returns $x$.

## History

Trevisan presented the construction at STOC 1999 and published it in the Journal of the ACM in 2001. It joined two lines of work that had been separate: pseudorandom generators from hard functions and extractors for weak sources. Raz, Reingold and Vadhan (2002) introduced weak designs, proved that the extractor is strong and extracted almost all of the min-entropy. The view of extractors as reconstruction proofs led to the construction of Shaltiel and Umans and influenced later work on list-decodable codes in pseudorandomness.

## References
