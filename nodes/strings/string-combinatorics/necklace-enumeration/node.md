---
tag: S98SFW
kind: problem
slug: necklace-enumeration
name: Necklace enumeration
aliases:
- generating necklaces
- necklace generation
area: strings/string-combinatorics
level: core
summary: Generate one representative of every necklace of a given length.
model: word-ram
complexity:
  vars: {n: the length of the necklaces, k: the alphabet size}
  time: {amortized: Θ(1)}
  space: {aux: Θ(n)}
prereqs: [necklace, lyndon-word]
see_also: [fkm-algorithm, cattell-necklace-generation, necklace-counting, de-bruijn-sequence, bracelet, minimal-rotation, lyndon-factorization, burnside-lemma]
sources:
  - paper: doi:10.1016/0196-6774(92)90047-G
    title: Frank Ruskey, Carla Savage and Terry Min Yih Wang, Generating necklaces, Journal of Algorithms 13(3), 1992, 414-430
    locator: the proof that the algorithm of Fredricksen, Kessler and Maiorana runs in constant amortized time per necklace
  - book: isbn:9780201038040
    title: Donald E. Knuth, The Art of Computer Programming, Volume 4A, Combinatorial Algorithms, Part 1, Addison-Wesley, 2011
    locator: Section 7.2.1.1, Generating all n-tuples (Algorithm F, prime and preprime strings in lexicographic order, and the theorem behind it)
  - paper: "Harold Fredricksen and James Maiorana, Necklaces of beads in k colors and k-ary de Bruijn sequences, Discrete Mathematics 23(3), 1978, 207-210"
    locator: the generation of necklaces in lexicographic order and the concatenation of Lyndon words into a de Bruijn sequence
  - paper: doi:10.1006/jagm.2000.1108
    title: Kevin Cattell, Frank Ruskey, Joe Sawada, Micaela Serra and C. Robert Miers, Fast algorithms to generate necklaces, unlabeled necklaces, and irreducible polynomials over GF(2), Journal of Algorithms 37(2), 2000, 267-282
    locator: the recursive constant amortized time generation of necklaces and Lyndon words
---

Necklace enumeration asks for a list of all [necklaces](/necklace/) of length $n$ over a $k$-letter alphabet, each given by one representative, usually its least rotation. Testing all $k^n$ words costs $\Theta(n k^n)$, while the [algorithm of Fredricksen, Kessler and Maiorana](/fkm-algorithm/) visits the prenecklaces in [lexicographic order](/lexicographic-order/) and spends constant amortized time per necklace. Restricting the same procedure to the aperiodic ones lists the [Lyndon words](/lyndon-word/).

## In plain words

Think of all the ways to string $n$ beads of $k$ colours on a ring, where two rings that differ only by a turn count as the same. The task is to list each ring once. The slow way writes down every possible row of beads, turns each row to its smallest-looking start, and keeps the row only if it already was the smallest. The fast way walks through the candidate rows in dictionary order and jumps straight from one good row to the next, using a rule that tells, from the current row, where the next one is. The work per ring listed is a fixed amount on average.

## Definition

**Input.** Integers $n \ge 1$ and $k \ge 1$. The alphabet is $\{0, 1, \ldots, k-1\}$ with its natural order, so words are compared in lexicographic order. Indices are 0-based.

**Output.** Every word $w \in \{0, \ldots, k-1\}^n$ that is a *necklace*, that is, $w \le \mathrm{rot}_i(w)$ for all $i$, each exactly once. These are the least representatives of the rotation classes, and there are
$$ N_k(n) = \frac{1}{n} \sum_{d \mid n} \varphi(d)\, k^{n/d} $$
of them (see [necklace](/necklace/) for the proof).

**Prenecklaces and the Lyndon prefix.** A word is a *prenecklace* if it is a prefix of some necklace. For a nonempty word $a$, let $\mathrm{lyn}(a)$ be the length of its longest prefix that is a Lyndon word. The theorem behind the fast method (Fredricksen, Kessler and Maiorana; see Knuth, Section 7.2.1.1) states: if $a$ is a prenecklace of length $n$ with $p = \mathrm{lyn}(a)$, then $a$ is a necklace if and only if $p$ divides $n$, and $a$ is a Lyndon word if and only if $p = n$. Moreover, if $i$ is the largest index with $a[i] < k - 1$, then the word $b$ with $b[0..i-1] = a[0..i-1]$, $b[i] = a[i] + 1$ and $b[t] = b[t - (i + 1)]$ for $t > i$ is the next prenecklace in lexicographic order, and $\mathrm{lyn}(b) = i + 1$.

## Variants

- **Lyndon words.** Output only the aperiodic necklaces, $p = n$; there are $\frac{1}{n} \sum_{d \mid n} \mu(d) k^{n/d}$ of them by the [Witt formula](/witt-formula/).
- **Fixed content or density.** Only necklaces with a given number of each letter, or of nonzero letters; constant amortized time algorithms exist for these.
- **Bracelets.** One representative per class under rotation and reversal; see [bracelet](/bracelet/).
- **Unlabeled necklaces.** Classes under rotation and a permutation of the colours, as in the work of [Cattell and coauthors](/cattell-necklace-generation/).
- **Ranking and unranking.** Compute the position of a given necklace in the lexicographic list, or the necklace at a given position, without listing all of them.
- **Gray codes.** List the necklaces so that consecutive ones differ in one letter.

## Examples

The run of the successor rule for $n = 4$, $k = 2$ visits the eight prenecklaces of length 4. The six with $p \mid 4$ are the necklaces, and the three with $p = 4$ are the Lyndon words.

| step | prenecklace $a$ | $p = \mathrm{lyn}(a)$ | $p \mid n$ | output |
| --- | --- | --- | --- | --- |
| 1 | `0000` | 1 | yes | necklace |
| 2 | `0001` | 4 | yes | necklace, Lyndon |
| 3 | `0010` | 3 | no | none |
| 4 | `0011` | 4 | yes | necklace, Lyndon |
| 5 | `0101` | 2 | yes | necklace |
| 6 | `0110` | 3 | no | none |
| 7 | `0111` | 4 | yes | necklace, Lyndon |
| 8 | `1111` | 1 | yes | necklace |

From `0011` the largest index with a letter below 1 is $i = 1$, so the next word starts with `01` and copies its period $p = 2$: `0101`. From `0111`, $i = 0$ gives `1` followed by copies of `1`.

| $n$ | 4 | 8 | 12 | 16 |
| --- | --- | --- | --- | --- |
| binary necklaces $N_2(n)$ | 6 | 36 | 352 | 4116 |
| prenecklaces visited | 8 | 71 | 747 | 8800 |

The number of prenecklaces stays within a constant factor of the number of necklaces, which is the reason for the constant amortized time bound.

## Known algorithms

**Filter all words, $\Theta(n k^n)$.** For each of the $k^n$ words, compute its [least rotation](/minimal-rotation/) in $O(n)$ time and keep the word if it is its own least rotation. Simple and useful as a test oracle, but the work per necklace is about $n^2$, since $k^n \approx n N_k(n)$.

**FKM successor rule, constant amortized time.** Apply the successor rule from $0^n$ and output the words with $p \mid n$:

```pseudo id=fkm
NECKLACES(n, k)
L1  a ← array of n zeros, p ← 1
L2  loop
L3      if n mod p = 0 then output a
L4      i ← n − 1
L5      while i ≥ 0 and a[i] = k − 1 do i ← i − 1
L6      if i < 0 then return
L7      a[i] ← a[i] + 1, p ← i + 1
L8      for t ← i + 1 to n − 1 do a[t] ← a[t − p]
```

Ruskey, Savage and Wang (1992) proved that the total number of steps of lines L5 and L8 is $O(N_k(n))$, so the time per necklace is constant on average, not counting the time to write each output. See the [FKM algorithm](/fkm-algorithm/) page for the proof of the successor rule.

**Recursive generation.** Cattell, Ruskey, Sawada, Serra and Miers (2000) gave a recursive form that extends a prenecklace one letter at a time, keeping $p$, and only branches on letters $a[t] \ge a[t - p]$. It is constant amortized time and adapts to restrictions such as fixed density.

**History.** Fredricksen and Maiorana (1978) and Fredricksen and Kessler (1986) introduced the lexicographic method, and Fredricksen and Maiorana showed that concatenating the Lyndon words of lengths dividing $n$ in this order gives a [de Bruijn sequence](/de-bruijn-sequence/). Ruskey, Savage and Wang (1992) proved the constant amortized time bound. Knuth presents it as Algorithm F in Volume 4A.

## Bounds

**Output size.** $N_k(n) = \frac{k^n}{n}(1 + o(1))$ for fixed $k \ge 2$, because the term $d = 1$ of the sum dominates. Any algorithm writes $N_k(n)$ words of length $n$, so writing them out costs $\Theta(n N_k(n)) = \Theta(k^n)$.

**Amortized time.** $O(1)$ per necklace beyond the output, by the FKM rule, when only the changed letters are reported. This is optimal up to the constant.

**Space.** $\Theta(n)$ for the current word.

## Reductions

- **To least rotation.** The filter method reduces enumeration to the [minimal rotation](/minimal-rotation/) problem on every word.
- **To prenecklace generation.** Necklaces and Lyndon words are the prenecklaces with $p \mid n$ or $p = n$.
- **De Bruijn sequences from Lyndon words.** Concatenating the Lyndon words whose lengths divide $n$, in lexicographic order, gives a [de Bruijn sequence](/de-bruijn-sequence/) of order $n$.
- **Irreducible polynomials.** Lyndon words of length $n$ over $k$ letters are in bijection with monic irreducible polynomials of degree $n$ over a field of $k$ elements when $k$ is a prime power, by the same Witt count; enumeration of one gives the other with extra arithmetic.

## Applications

- **De Bruijn sequences** for testing, robotics and combinatorial design, via the Lyndon concatenation.
- **Chemistry and combinatorics.** Listing cyclic molecules or circular arrangements up to rotation.
- **Exhaustive search.** Searching over circular objects only once per class, for example in the search for words avoiding a pattern up to rotation.
- **Counting checks.** The list confirms counts from the [Burnside lemma](/burnside-lemma/) and [necklace counting](/necklace-counting/).

## References
