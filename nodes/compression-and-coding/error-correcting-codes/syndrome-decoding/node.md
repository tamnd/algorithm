---
tag: 4Q2QZ4
kind: algorithm
slug: syndrome-decoding
name: Syndrome decoding
aliases:
- coset leader decoding
area: compression-and-coding/error-correcting-codes
level: core
summary: Decode a linear code with a table from each syndrome H r^T to a least weight coset leader e, and output r - e. A nearest codeword decoder for hard decisions.
solves: [nearest-codeword-problem]
model: word-ram
complexity:
  vars: {n: the code length, k: the code dimension, q: the field size}
  time: {worst: Θ((n - k) n), total: O(q^n n^2)}
  space: {extra: Θ(q^(n-k) n)}
properties: {deterministic: true, recursive: false, online: false}
history:
  year: 1956
  people: [Richard W. Hamming, David Slepian]
  note: Hamming read the position of a single error from the checking number in 1950. Slepian decoded any binary group code by its cosets and their leaders in 1956.
prereqs: [syndrome, standard-array]
see_also: [hamming-code, maximum-likelihood-decoding, binary-symmetric-channel, nearest-codeword-problem, bch-code, information-set-decoding, syndrome-decoding-problem, majority-logic-decoding]
sources:
  - book: isbn:9780130426727
    title: Shu Lin and Daniel J. Costello, Jr., Error Control Coding, second edition, Pearson Prentice Hall, 2004
    locator: Chapter 3, Section 3.5 (standard array and syndrome decoding, the table of syndromes and coset leaders, and the probability of a decoding error)
  - book: isbn:9780444851932
    title: F. J. MacWilliams and N. J. A. Sloane, The Theory of Error-Correcting Codes, North-Holland, 1977
    locator: Chapter 1 (decoding by syndromes and coset leaders)
  - paper: doi:10.1002/j.1538-7305.1956.tb02379.x
    title: David Slepian, A class of binary signaling alphabets, Bell System Technical Journal 35(1), 1956, pages 203 to 234
    locator: The decomposition of a group alphabet into cosets and the maximum likelihood detector that it gives
  - paper: doi:10.1002/j.1538-7305.1950.tb00463.x
    title: R. W. Hamming, Error detecting and error correcting codes, Bell System Technical Journal 29(2), 1950, pages 147 to 160
    locator: The single error correcting codes, where the checking number written in binary gives the position of the error
  - book: isbn:9780521642989
    title: David J. C. MacKay, Information Theory, Inference, and Learning Algorithms, Cambridge University Press, 2003
    locator: Chapter 1 (syndrome decoding of the (7,4) Hamming code and its error probability)
---

Syndrome decoding decodes a [linear code](/linear-code/) by a table that maps each [syndrome](/syndrome/) $s = H r^T$ to a coset leader, an error pattern of least weight with that syndrome. The decoder computes the syndrome of the received word $r$, looks up the leader $\hat e$, and outputs $r - \hat e$. It is a nearest codeword decoder, so on a binary symmetric channel with crossover probability below $1/2$ it is a maximum likelihood decoder for hard decisions. The table has $q^{n-k}$ entries, so it is practical only when the number of check symbols is small.

## In plain words

Each parity check of a code either passes or fails. The pattern of failed checks does not depend on the message, only on the error. So before any data arrives, the receiver lists, for each possible pattern of failed checks, the smallest error that causes it.

To decode a word, the receiver runs the checks, looks up the smallest error for that pattern in the list, and undoes it. If the real error was that smallest error, the result is right. If the real error was larger, the decoder makes a mistake, but it still returns a valid codeword that is as close as possible to the word that arrived.

The list has one line for each possible pattern of failed checks. Each extra check doubles the length of the list for a binary code, so the method suits codes with few checks.

## The problem

**Notation.** $C$ is an $[n, k, d]_q$ linear code over $\mathrm{GF}(q)$ with generator matrix $G$ ($c = m G$) and an $(n - k) \times n$ parity-check matrix $H$ of rank $n - k$ ($H c^T = 0$). Vectors are rows. The rate is $R = k/n$, $t = \lfloor (d - 1)/2 \rfloor$, and $\mathrm{wt}$ is the [Hamming weight](/hamming-weight/).

**Channel and decisions.** A codeword $c$ is sent over a [binary symmetric channel](/binary-symmetric-channel/) BSC($p$) with $p < 1/2$, or its $q$-ary symmetric form, which changes each symbol with probability $p$ to one of the $q - 1$ other symbols with equal chances. The receiver makes hard decisions and gets $r = c + e$.

**Task.** Given $r$, output a codeword $\hat c$ that minimizes $d(r, \hat c)$, the [nearest codeword](/nearest-codeword-problem/). Since $r - \hat c$ runs over the coset $r + C$ as $\hat c$ runs over $C$, this is the same as finding a word $\hat e$ of least weight with $H \hat e^T = H r^T$.

## The algorithm

BUILD-TABLE runs once per code. SYNDROME-DECODE runs once per received word.

```pseudo id=main
BUILD-TABLE(H)                          ▷ H is (n − k) × n over GF(q), of rank n − k
L1  T ← an empty map from syndromes to error patterns
L2  for w ← 0 to n do
L3      for each e in GF(q)^n of weight w, in a fixed order do
L4          s ← H e^T
L5          if T has no entry for s then T[s] ← e
L6      if T has q^(n − k) entries then return T
L7  return T

SYNDROME-DECODE(T, H, r)
L8  s ← H r^T
L9  ê ← T[s]                            ▷ the coset leader of r
L10 return r − ê
```

Line L2 goes through the weights in increasing order, so the first pattern stored for a syndrome has the least weight in its coset. Line L5 never replaces an entry. Line L6 stops after the weight $\rho$ at which the last syndrome appears; $\rho$ is the covering radius of the code, so the loop never visits patterns heavier than $\rho$. The implementation lists the patterns of one weight by their positions in lexicographic order, then by their values.

The table is the first column of the [standard array](/standard-array/), indexed by syndrome instead of by row. Both give the same decoder when they choose the same leaders.

## Example

**A [6, 3, 3] code.** Take $G = [I_3 \mid P]$ with $P$ rows $011, 101, 110$, so

$$H = [P^T \mid I_3] = \begin{pmatrix} 0&1&1&1&0&0 \\ 1&0&1&0&1&0 \\ 1&1&0&0&0&1 \end{pmatrix}.$$

The codewords are $000000, 001110, 010101, 011011, 100011, 101101, 110110, 111000$: four of weight 3 and three of weight 4, so $d = 3$ and $t = 1$. BUILD-TABLE stores:

| syndrome | leader | how it is found |
|---|---|---|
| 000 | 000000 | weight 0 |
| 011 | 100000 | weight 1, column 1 |
| 101 | 010000 | weight 1, column 2 |
| 110 | 001000 | weight 1, column 3 |
| 100 | 000100 | weight 1, column 4 |
| 010 | 000010 | weight 1, column 5 |
| 001 | 000001 | weight 1, column 6 |
| 111 | 100100 | weight 2, the first of 100100, 010010, 001001 |

After weight 1 the table has 7 entries. At weight 2 the pairs of positions $\{1, 2\}$ and $\{1, 3\}$ give $011 + 101 = 110$ and $011 + 110 = 101$, which are already stored; the pair $\{1, 4\}$ gives $011 + 100 = 111$, a new entry. Now the table has $2^3 = 8$ entries and line L6 returns it. The covering radius is 2.

Decode $r = 111100$. Line L8 gives $s = H r^T = 100$ (rows: $0 + 1 + 1 + 1 = 1$, $1 + 0 + 1 + 0 = 0$, $1 + 1 + 0 + 0 = 0$). Line L9 gives $\hat e = 000100$, and line L10 returns $111000$, a codeword at distance 1 from $r$.

On BSC($p$) the decoder is correct exactly when the error is one of the 8 leaders, so the block error rate is $1 - (1 - p)^6 - 6 p (1 - p)^5 - p^2 (1 - p)^4$. At $p = 0.1$ it is $0.107704$.

**The Hamming code.** For the $[7, 4, 3]$ [Hamming code](/hamming-code/) the 8 syndromes are 0 and the 7 columns of $H$, so the leaders are $0$ and the 7 words of weight 1. Every single error is corrected and every double error is decoded to a wrong codeword. The block error rate on BSC($p$) is $1 - (1 - p)^7 - 7 p (1 - p)^6$: $0.0020310$ at $p = 0.01$, $0.0443805$ at $p = 0.05$ and $0.1496944$ at $p = 0.1$. A simulation of 20000 random codewords over BSC($0.05$) with the seed 2026 in the tests gives $0.04615$, within two standard deviations ($0.00146$) of the exact value.

**Over GF(3).** The tetracode has $H = \begin{pmatrix} 2&2&1&0 \\ 2&1&0&1 \end{pmatrix}$. Its $3^2 = 9$ syndromes are $0$ and the $4 \cdot 2 = 8$ single errors $a\, h_j$ with $a \in \{1, 2\}$. The codeword $1011$ with the error $0200$ arrives as $r = 1211$. Then $s = (2 + 4 + 1,\ 2 + 2 + 1) = (1, 2)$ modulo 3, the table gives $\hat e = 0200$, and $r - \hat e = 1011$.

## Correctness

The full proof is in the proofs file. The key facts:

- **Syndromes are cosets.** $H x^T = H y^T$ if and only if $x - y \in C$. Since $H$ has rank $n - k$, the map $e \mapsto H e^T$ is onto $\mathrm{GF}(q)^{n-k}$, so each of the $q^{n-k}$ syndromes is the syndrome of one coset.
- **The table holds least weight leaders.** Line L2 visits weights in increasing order and line L5 keeps the first pattern, so $T[s]$ has the least weight among all $e$ with $H e^T = s$. All syndromes are reached, because the loop would visit all of $\mathrm{GF}(q)^n$.
- **The output is a nearest codeword.** $H (r - \hat e)^T = s - s = 0$, so $r - \hat e \in C$. For any codeword $c$, $r - c$ has the syndrome $s$, so $d(r, c) = \mathrm{wt}(r - c) \ge \mathrm{wt}(\hat e) = d(r, r - \hat e)$.

If $c$ is sent and the error is $e$, the output is $c + e - \hat e$, which is $c$ exactly when $e = \hat e$. Every $e$ of weight at most $t$ is the unique least weight word of its coset, so it is corrected. On BSC($p$) with $p < 1/2$ a lighter error is more likely, so the decoder is a [maximum likelihood decoder](/maximum-likelihood-decoding/).

## Complexity

**Decoding.** Line L8 costs $(n - k) n$ multiplications and additions in $\mathrm{GF}(q)$, which is $\Theta(n^2)$ for a fixed rate, and fewer for a sparse $H$. Lines L9 and L10 cost one table lookup and $n$ subtractions. With the syndrome read as a number from $0$ to $q^{n-k} - 1$, the table is a plain array.

**Building.** The loop visits $\sum_{w \le \rho} \binom{n}{w} (q - 1)^w$ patterns, where $\rho$ is the covering radius, and at least $q^{n-k}$ of them. Each costs one syndrome, $O(n^2)$, or $O(n - k)$ if the syndrome is updated from that of a pattern with one fewer nonzero entry. In the worst case this is $O(q^n n^2)$.

**Memory.** $q^{n-k}$ patterns of $n$ symbols, against $q^n$ for the full [standard array](/standard-array/). For the binary $[23, 12, 7]$ Golay code this is $2^{11} = 2048$ entries. For a $[255, 223]$ Reed-Solomon code over $\mathrm{GF}(256)$ it would be $256^{32} = 2^{256}$ entries, which is why such codes use algebraic decoders.

## Properties

- **Complete.** Every received word is decoded to some codeword. The decoder never reports a failure.
- **Hard decisions.** The input is a word over $\mathrm{GF}(q)$. It cannot use the reliability of each symbol.
- **Deterministic ties.** When a coset has several patterns of least weight, the fixed order of line L3 picks one. The block error rate on BSC($p$) depends only on how many leaders of each weight there are, not on which tied pattern is chosen.
- **Linear time per word.** After the table is built, decoding costs one syndrome and one lookup.

## Variants and improvements

- **Bounded distance decoding.** Store only the leaders of weight at most $t$. If the syndrome is not in the table, report a detected error. This trades corrections beyond $t$ for detection.
- **Hamming codes without a table.** If the columns of $H$ are the binary numbers $1, 2, \ldots, 2^r - 1$ in order, the syndrome read as a number is the position of a single error. See [Hamming code](/hamming-code/).
- **Algebraic syndrome decoding.** For [BCH](/bch-code/) and Reed-Solomon codes, the syndromes $S_j = r(\alpha^j)$ feed the Berlekamp-Massey algorithm, which finds the error locations in polynomial time, up to $t$ errors.
- **Majority logic decoding.** For codes with many orthogonal checks, such as Reed-Muller codes, [majority logic decoding](/majority-logic-decoding/) decides each symbol by a vote of checks.
- **Information set decoding.** For codes with large $n - k$ and no structure, [information set decoding](/information-set-decoding/) searches for a low weight $e$ with $H e^T = s$ by guessing error free information sets. It is exponential but much faster than a table.

## When to use it

Use syndrome decoding for short linear codes with few check symbols: a binary code with $n - k$ up to about 20 has a table of about a million entries. Memory ECC with Hamming and SECDED codes, small codes in sensors and in control channels, and inner codes of concatenated schemes fit. Use it also as the exact nearest codeword reference in tests of faster decoders. Do not use it for long codes with many checks, where algebraic, iterative or information set decoders are the only option, and do not use it when soft information is available, where a soft decision [maximum likelihood decoder](/maximum-likelihood-decoding/) does better.

## Pitfalls

- **Patterns not in order of weight.** If line L2 and line L3 visit all of $\mathrm{GF}(q)^n$ in numerical order, a heavy pattern can be stored first. For the Hamming code with the columns $110, 011, 111, 101, 100, 010, 001$, the pattern $0000011$ comes before $0100000$ in numerical order and has the same syndrome $011$, so a single error at position 2 becomes a decoder error.
- **Overwriting entries.** If line L5 stores $e$ without the test, the table keeps the last pattern of each syndrome, the heaviest in the order, and the decoder is no longer nearest.
- **Adding instead of subtracting.** Line L10 must return $r - \hat e$. Over $\mathrm{GF}(2)$ this is $r + \hat e$, but over $\mathrm{GF}(3)$ the tetracode word $1211$ with $\hat e = 0200$ gives $r + \hat e = 1111$, which is not a codeword.
- **Two different parity-check matrices.** The table of lines L1 to L7 is valid only for the same $H$ used at line L8. With $H' = A H$ the syndromes change to $A s$, and the lookup returns wrong leaders.
- **Expecting detection.** The decoder is complete, so a pattern of $t + 1$ errors is decoded to a wrong codeword without a warning, as every double error in the Hamming code. Use the bounded distance variant, or an extended code, when detection matters.

## Implementations

## History

Richard Hamming's 1950 paper built single error correcting codes whose parity checks, read as a binary number, give the position of the error; this is a syndrome table in which the syndrome is the address. David Slepian's 1956 paper on group alphabets treated any binary linear code as a group, split the space into its cosets, and decoded each received word to the codeword that its coset leader points to, which is maximum likelihood on the binary symmetric channel. Textbooks since then present the standard array and the table of syndromes together, as Lin and Costello do in their chapter on linear block codes.

## References
