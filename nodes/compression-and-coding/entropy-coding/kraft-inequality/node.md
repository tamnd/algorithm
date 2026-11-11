---
tag: AMFER4
kind: theorem
slug: kraft-inequality
name: Kraft inequality
aliases:
- Kraft-McMillan inequality
area: compression-and-coding/entropy-coding
level: core
summary: A prefix code with codeword lengths l_i over D letters exists if and only if sum D^(-l_i) <= 1. By McMillan, every uniquely decodable code obeys the same bound.
prereqs: [prefix-code, uniquely-decodable-code]
see_also: [source-coding-theorem, huffman-coding, canonical-huffman-code, optimal-prefix-code, shannon-fano-coding, elias-gamma-coding, unary-coding, universal-code]
sources:
  - url: https://dspace.mit.edu/handle/1721.1/12390
    title: Leon Gordon Kraft, A device for quantizing, grouping, and coding amplitude-modulated pulses, M.S. thesis, Department of Electrical Engineering, MIT, 1949
    locator: The inequality on the lengths of a code in which no codeword is a prefix of another, and the construction of such a code
  - paper: doi:10.1109/TIT.1956.1056818
    title: Brockway McMillan, Two inequalities implied by unique decipherability, IRE Transactions on Information Theory 2(4), 1956
    locator: The first inequality (the Kraft sum of a uniquely decipherable code is at most 1)
  - book: isbn:9780471241959
    title: Thomas M. Cover and Joy A. Thomas, Elements of Information Theory, second edition, Wiley, 2006
    locator: Section 5.2 (Theorem 5.2.1, the Kraft inequality, and Theorem 5.2.2, the countable case) and Section 5.5 (Theorem 5.5.1, McMillan)
  - book: isbn:9780521642989
    title: David J. C. MacKay, Information Theory, Inference, and Learning Algorithms, Cambridge University Press, 2003
    locator: Chapter 5, Symbol codes (the Kraft inequality for uniquely decodable codes and its proof by powers of the Kraft sum)
---

The Kraft inequality says which lists of codeword lengths a [prefix code](/prefix-code/) can have: lengths $\ell_1, \ldots, \ell_m$ over an alphabet of $D$ letters are possible if and only if $\sum_i D^{-\ell_i} \le 1$. McMillan's theorem extends the "only if" part to every [uniquely decodable code](/uniquely-decodable-code/). So short codewords are a budget: a codeword of length $\ell$ uses $D^{-\ell}$ of a total of 1, and no decodable code can spend more. The inequality turns the design of a code into the choice of numbers, and it is the bridge from codes to [entropy](/shannon-entropy/) in the [source coding theorem](/source-coding-theorem/).

## Statement

Notation. The code alphabet has $D \ge 2$ letters, $\{0, 1, \ldots, D - 1\}$. A code has $m$ codewords (or countably many) with lengths $\ell_1, \ell_2, \ldots \ge 1$. The *Kraft sum* is $K = \sum_i D^{-\ell_i}$. No probability model is needed: the theorem is about lengths only, in the worst case.

**Theorem.**

- **(a) Kraft.** If a prefix code over $D$ letters has codeword lengths $\ell_1, \ldots, \ell_m$, then $\sum_{i=1}^{m} D^{-\ell_i} \le 1$.
- **(b) Converse.** If positive integers $\ell_1, \ldots, \ell_m$ satisfy $\sum_{i=1}^{m} D^{-\ell_i} \le 1$, then there is a prefix code over $D$ letters with exactly these codeword lengths.
- **(c) McMillan.** If a uniquely decodable code over $D$ letters has codeword lengths $\ell_1, \ldots, \ell_m$, then $\sum_{i=1}^{m} D^{-\ell_i} \le 1$.
- **(d) Countable codes.** (a), (b) and (c) also hold for codes with countably many codewords.

## In plain words

Think of all the possible codewords as the branches of a tree. When you pick a short codeword, you also block every longer word that starts with it, so a short codeword uses a large share of the tree. Each codeword uses a share that halves (for two letters) with each extra letter of length. The theorem says that a code can be decoded without delay exactly when the shares add up to at most the whole tree. If the shares fit, we can always build such a code, one codeword after the other, from the shortest to the longest. A surprise is that the weaker demand, that a whole message can be decoded in only one way, gives no extra room. So the best codes can always be the simple ones that decode at once.

## Proof

The full proof of all four parts is in [the proof](proofs/correctness.md). Its main steps:

- **(a)** Give the string $w$ the interval $I(w) = [0.w, 0.w + D^{-|w|})$ of $[0, 1)$, where $0.w$ is $w$ read as a fraction in base $D$. A string $u$ is a prefix of $v$ exactly when $I(v) \subseteq I(u)$, and otherwise the intervals are disjoint. In a prefix code the intervals of the codewords are disjoint, so their lengths $D^{-\ell_i}$ sum to at most 1.
- **(b)** Sort the lengths so that $\ell_1 \le \cdots \le \ell_m$ and let $c_i = \sum_{j < i} D^{-\ell_j}$. Codeword $i$ is $c_i$ written with $\ell_i$ digits in base $D$. The intervals $[c_i, c_i + D^{-\ell_i})$ follow each other without overlap, so no codeword is a prefix of another. This is the canonical code: each codeword is the one before it plus 1, padded with zeros on the right.
- **(c)** Raise $K$ to the power $k$. The terms of $K^k$ correspond to the sequences of $k$ codewords, and a sequence whose concatenation has length $n$ contributes $D^{-n}$. Unique decodability makes the concatenations different, so at most $D^n$ sequences have length $n$, and $K^k \le kL$, with $L$ the longest length. If $K > 1$, $K^k$ grows exponentially in $k$, but $kL$ grows only linearly. So $K \le 1$.
- **(d)** Every finite part of a prefix code or of a uniquely decodable code is again one, so all partial sums are at most 1. For the converse, the construction of (b) works one codeword at a time.

## Consequences

- **The entropy bound.** For a source with law $p$, a uniquely decodable code has mean length $\sum_i p_i \ell_i \ge H_D(p)$, with equality only if $\ell_i = \log_D (1/p_i)$ for all $i$. *Proof.* With $q_i = D^{-\ell_i} / K$, the Gibbs inequality gives $\sum_i p_i \log_D \frac{1}{q_i} \ge H_D(p)$, and $\sum_i p_i \ell_i = \sum_i p_i \log_D \frac{1}{q_i} - \log_D K \ge H_D(p)$, since $K \le 1$. This is the converse half of the variable-length [source coding theorem](/source-coding-theorem/).
- **The Shannon code.** The lengths $\ell_i = \lceil \log_D (1/p_i) \rceil$ have $K \le \sum_i p_i = 1$, so by (b) a prefix code with these lengths exists, and its mean length is less than $H_D(p) + 1$. [Shannon-Fano coding](/shannon-fano-coding/) is one way to build such a code.
- **Prefix codes lose nothing.** By (c) and (b), every uniquely decodable code can be replaced by a prefix code with the same lengths. So the search for an [optimal code](/optimal-prefix-code/), such as [Huffman coding](/huffman-coding/), can be limited to prefix codes.
- **Codes from lengths.** Many codecs store only the codeword lengths and rebuild the codewords with the construction of (b). This is the [canonical Huffman code](/canonical-huffman-code/).
- **Codes for the integers.** A prefix code for all positive integers is a countable code, so (d) applies. The [unary code](/unary-coding/) has $\ell(n) = n$ and $K = \sum_n 2^{-n} = 1$. [Elias gamma](/elias-gamma-coding/) has $\ell(n) = 2 \lfloor \log_2 n \rfloor + 1$, and the $2^k$ integers in $[2^k, 2^{k+1})$ add $2^k \cdot 2^{-(2k+1)} = 2^{-k-1}$, so again $K = 1$. No prefix code has $\ell(n) \le \log_2 n + \log_2 \log_2 n + c$ for all $n \ge 2$, because $\sum_n \frac{1}{n \log_2 n}$ diverges. This is why [universal codes](/universal-code/) need a little more than $\log_2 n + \log_2 \log_2 n$ bits.

## Tightness

**Examples.** The code on this page builds the canonical code of (b) and checks it:

| lengths | $D$ | $K$ | code from (b) |
|---|---|---|---|
| 1, 2, 3, 3 | 2 | 1 | 0, 10, 110, 111 |
| 2, 2, 2, 3, 3 | 2 | 1 | 00, 01, 10, 110, 111 |
| 1, 2, 2 | 3 | 5/9 | 0, 10, 11 |
| 1, 1, 2 | 2 | 5/4 | none exists |

**$K = 1$ is the complete case.** A prefix code with $K = 1$ is *complete*: in its code tree every internal node has all $D$ children, and every infinite string of letters begins with a codeword. If $K < 1$, some branch of the tree is unused. For $D = 2$ this means that some internal node has only one child, and every codeword below that node can be made one letter shorter. So the bound $K \le 1$ cannot be improved, and optimal binary codes such as Huffman codes have $K = 1$. For $D \ge 3$ an optimal code can have $K < 1$: with two symbols and $D = 3$, the best code is $\{0, 1\}$, with $K = 2/3$.

**The converse is about lengths, not about a given code.** The code $\{0, 01\}$ has $K = 3/4$ but is not a prefix code; (b) says only that some prefix code with lengths 1 and 2 exists, for example $\{0, 10\}$. In the same way, $K \le 1$ does not make a code uniquely decodable: $\{0, 01, 10\}$ has $K = 1$, but $010$ is both $0 \cdot 10$ and $01 \cdot 0$. And a uniquely decodable code can have $K = 1$ without being a prefix code: $\{0, 01, 11\}$ is a suffix code.

**McMillan needs unique decodability of all sequences.** The power argument uses the fact that different sequences of $k$ codewords give different strings, for every $k$. A code that is only non-singular, with different codewords but ambiguous concatenations, can have $K > 1$: $\{0, 1, 01\}$ has $K = 5/4$.

## History

Kraft proved the inequality for prefix codes, and the construction of the converse, in his 1949 MIT master's thesis on the coding of amplitude-modulated pulses. McMillan (1956) proved that the same inequality holds for every uniquely decipherable code, so that a prefix code is as good as any uniquely decodable code. The short proof by powers of the Kraft sum, given here, is usually credited to Karush (1961); McMillan's first proof was longer. The countable case and the use of the inequality to prove the entropy bound are standard in textbooks such as Cover and Thomas, Chapter 5.

## References
