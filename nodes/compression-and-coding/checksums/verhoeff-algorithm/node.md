---
tag: ZV0WXF
kind: algorithm
slug: verhoeff-algorithm
name: Verhoeff algorithm
aliases:
- Verhoeff check digit
area: compression-and-coding/checksums
level: advanced
summary: Decimal check digit from the dihedral group of order 10 and a permutation of order 8. It catches every single error and every adjacent transposition, which no weighted mod 10 sum can do.
model: word-ram
complexity:
  vars: {n: the number of digits}
  time: {worst: Θ(n), average: Θ(n), best: Θ(n)}
  space: {extra: Θ(1)}
properties: {deterministic: true, recursive: false, online: false, comparison: false}
history:
  year: 1969
  people: [Jacobus Verhoeff]
  note: Verhoeff published the scheme in Error Detecting Decimal Codes, Mathematical Centre Tracts 29, Amsterdam, 1969, with a study of the errors that people make when they copy numbers.
prereqs: [check-digit-computation, finite-group]
see_also: [luhn-algorithm, damm-algorithm, permutation, cyclic-group, error-detection, hamming-distance]
sources:
  - paper: "J. Verhoeff, Error Detecting Decimal Codes, Mathematical Centre Tracts 29, Mathematisch Centrum, Amsterdam, 1969"
    title: J. Verhoeff, Error Detecting Decimal Codes, Mathematical Centre Tracts 29, 1969
    locator: The classification of human copying errors and their frequencies, and the check based on the dihedral group of order 10 with a permutation of the digits
  - paper: doi:10.1145/243439.243457
    title: Joseph A. Gallian, Error detection methods, ACM Computing Surveys 28(3), 1996, pages 504 to 517
    locator: The section on the dihedral group method (Verhoeff's scheme, its tables, and the condition a σ(b) ≠ b σ(a))
---

The Verhoeff algorithm computes a decimal check digit that catches every single wrong digit and every swap of two adjacent digits. Jacobus Verhoeff published it in 1969. It replaces the addition mod 10 of other schemes by the multiplication of the dihedral group $D_5$, the ten symmetries of a regular pentagon, and it moves each digit by the $i$-th power of a fixed permutation $\sigma$ before it enters the product. Because $D_5$ is not commutative, the swap problem that defeats every weighted sum mod 10 goes away. Its pair, the [Damm algorithm](/damm-algorithm/), gets the same guarantee with one table and no permutation; the older [Luhn algorithm](/luhn-algorithm/) misses the swaps 09 and 90. The method is one [finite group](/finite-group/) and three small tables.

## In plain words

Think of the ten digits as the ten ways to turn or flip a pentagon so that it lands on itself. Digits 0 to 4 are the five turns, and 5 to 9 are the five flips. "Multiplying" two digits means doing one move after the other. Unlike addition, the order matters: a flip then a turn is not the same as the turn then the flip.

To check a number, read it from the right. Before each digit joins the running result, scramble it with a fixed shuffle of the digits, applied once for the second digit, twice for the third, and so on. The number is valid when the result is the "do nothing" move, 0. Swapping two neighbors changes the result, because the moves come in a different order and with different scrambles, and the tables are built so that this always shows.

## The problem

The input is a payload of $n$ decimal digits; the output is one check digit $c$. Write the code word from the right as $x_0 x_1 \ldots x_n$ with $x_0 = c$. Let $\ast$ be the operation of $D_5$ on $\{0, \ldots, 9\}$ given by the table $D$ below, with identity 0, and let $\sigma$ be the permutation $(0\,1\,5\,8\,9\,4\,2\,7)(3\,6)$ of the digits. The code word is valid when

$$\sigma^0(x_0) \ast \sigma^1(x_1) \ast \cdots \ast \sigma^n(x_n) = 0.$$

Since $\sigma$ has order 8, $\sigma^i = \sigma^{i \bmod 8}$, so a table $P$ of 8 rows holds all the powers. We count table lookups in the [word RAM](/word-ram/).

## The algorithm

The three tables, copied from Verhoeff's construction as Gallian gives it:

| $D$ | 0 | 1 | 2 | 3 | 4 | 5 | 6 | 7 | 8 | 9 |
|---|---|---|---|---|---|---|---|---|---|---|
| **0** | 0 | 1 | 2 | 3 | 4 | 5 | 6 | 7 | 8 | 9 |
| **1** | 1 | 2 | 3 | 4 | 0 | 6 | 7 | 8 | 9 | 5 |
| **2** | 2 | 3 | 4 | 0 | 1 | 7 | 8 | 9 | 5 | 6 |
| **3** | 3 | 4 | 0 | 1 | 2 | 8 | 9 | 5 | 6 | 7 |
| **4** | 4 | 0 | 1 | 2 | 3 | 9 | 5 | 6 | 7 | 8 |
| **5** | 5 | 9 | 8 | 7 | 6 | 0 | 4 | 3 | 2 | 1 |
| **6** | 6 | 5 | 9 | 8 | 7 | 1 | 0 | 4 | 3 | 2 |
| **7** | 7 | 6 | 5 | 9 | 8 | 2 | 1 | 0 | 4 | 3 |
| **8** | 8 | 7 | 6 | 5 | 9 | 3 | 2 | 1 | 0 | 4 |
| **9** | 9 | 8 | 7 | 6 | 5 | 4 | 3 | 2 | 1 | 0 |

| $P$ | 0 | 1 | 2 | 3 | 4 | 5 | 6 | 7 | 8 | 9 |
|---|---|---|---|---|---|---|---|---|---|---|
| $\sigma^0$ | 0 | 1 | 2 | 3 | 4 | 5 | 6 | 7 | 8 | 9 |
| $\sigma^1$ | 1 | 5 | 7 | 6 | 2 | 8 | 3 | 0 | 9 | 4 |
| $\sigma^2$ | 5 | 8 | 0 | 3 | 7 | 9 | 6 | 1 | 4 | 2 |
| $\sigma^3$ | 8 | 9 | 1 | 6 | 0 | 4 | 3 | 5 | 2 | 7 |
| $\sigma^4$ | 9 | 4 | 5 | 3 | 1 | 2 | 6 | 8 | 7 | 0 |
| $\sigma^5$ | 4 | 2 | 8 | 6 | 5 | 7 | 3 | 9 | 0 | 1 |
| $\sigma^6$ | 2 | 7 | 9 | 3 | 8 | 0 | 6 | 4 | 1 | 5 |
| $\sigma^7$ | 7 | 0 | 4 | 6 | 9 | 1 | 3 | 2 | 5 | 8 |

The inverse table is $\mathrm{INV} = 0, 4, 3, 2, 1, 5, 6, 7, 8, 9$: a rotation $k$ has the inverse $5 - k$ (and 0 its own), and each reflection is its own inverse.

```pseudo id=main
STATE(x, s)                                  ▷ x read from the right, positions from s
L1  c ← 0
L2  for each digit v of x, from right to left, with position i = s, s+1, ... do
L3      c ← D[c][P[i mod 8][v]]
L4  return c

CHECK-DIGIT(p)
L5  return INV[STATE(p, 1)]                 ▷ the payload starts at position 1

IS-VALID(w)
L6  return STATE(w, 0) = 0                  ▷ the check digit is at position 0
```

The check digit sits at position 0, where $\sigma^0$ is the identity, and it is the first factor of the product. So if $q$ is the product of the payload factors, the code word gives $c \ast q$, and $c = q^{-1}$ makes it 0.

## Example

The payload 236. Its digits from the right are 6, 3, 2 at positions 1, 2, 3:

| position $i$ | digit | $\sigma^i(\text{digit})$ | $c$ |
|---|---|---|---|
| 1 | 6 | 3 | $D[0][3] = 3$ |
| 2 | 3 | 3 | $D[3][3] = 1$ |
| 3 | 2 | 1 | $D[1][1] = 2$ |

So $q = 2$ and the check digit is $\mathrm{INV}[2] = 3$. Validating 2363 from position 0 gives $c = 3, 1, 4, 0$, so it is valid, and 2364 is not. The tests check these values.

## Correctness

Two facts carry the proof. First, $D$ is the table of a group, so a product changes when any one factor changes; and every $\sigma^i$ is a permutation, so a changed digit is a changed factor. Second, $\sigma$ satisfies $a \ast \sigma(b) \ne b \ast \sigma(a)$ for all $a \ne b$. A swap of neighbors in positions $i$ and $i + 1$ replaces $\sigma^i(a) \ast \sigma^{i+1}(b)$ by $\sigma^i(b) \ast \sigma^{i+1}(a)$; with $u = \sigma^i(a)$ and $v = \sigma^i(b)$ these are $u \ast \sigma(v)$ and $v \ast \sigma(u)$, which differ, and by cancellation the whole product differs. The tests check the group axioms on all $10^3$ triples, the dihedral relations, that the rows of $P$ are the powers of $\sigma$ with $\sigma^8 = \mathrm{id}$, and the condition for all 90 pairs. The full proof is in the correctness file below.

## Complexity

Each digit costs two table lookups, so both procedures take $\Theta(n)$ time and $\Theta(1)$ extra space. The tables hold $100 + 80 + 10$ small entries.

## Properties

Over all 10,000 payloads of 4 digits, the tests count the missed errors exactly:

| error | example | missed | of |
|---|---|---|---|
| single error | $a \to b$ | 0 | 450,000 |
| adjacent transposition | $ab \to ba$ | 0 | 36,000 |
| twin error | $aa \to bb$ | 1,600 | 36,000 |
| jump transposition | $abc \to cba$ | 1,560 | 27,000 |
| jump twin error | $aca \to bcb$ | 1,560 | 27,000 |

The [Damm algorithm](/damm-algorithm/) page puts these numbers next to those of Luhn and Damm. Verhoeff catches all of the two most common classes and about 95 percent of the next three.

- **Leading zeros matter.** $\sigma$ moves 0 to 1, so a leading zero changes the product: the check digit of 0236 differs from that of 236, and the check digit of 0 is 4. A system that uses Verhoeff must fix the length of its numbers or never drop zeros.
- **One valid digit.** For each payload exactly one of the ten digits is a valid check, because $c \mapsto c \ast q$ is a bijection. The tests check this on random payloads.

## Variants and improvements

- **[Damm algorithm](/damm-algorithm/).** A single table of a quasigroup of order 10, with no permutation and no inverse table. It catches the same two classes, and leading zeros do not change its check digit.
- **[Luhn algorithm](/luhn-algorithm/).** Simpler to do by hand, but misses 09 and 90.
- **Other groups and permutations.** Any group $G$ and permutation $\sigma$ with $a \ast \sigma(b) \ne b \ast \sigma(a)$ for $a \ne b$ give the same guarantee, by the proof below. For alphabets of other sizes, the same method works with other groups.
- **Why a non-abelian group.** The only abelian group of order 10 is the cyclic group $\mathbb{Z}_{10}$. There, weighted sums cannot catch both single errors and adjacent swaps, as the [check digit computation](/check-digit-computation/) page shows, and the correctness file below shows that no permutation $\sigma$ can either. $D_5$ is the only other group of order 10.

## When to use it

Use Verhoeff for a new decimal code that people will type or read aloud, when you want all single errors and adjacent swaps caught with one digit and no extra symbol such as X. The Aadhaar number of India uses it. Prefer [Damm](/damm-algorithm/) when you want one table and an implementation that ignores leading zeros. Use [Luhn](/luhn-algorithm/) when a standard requires it.

## Pitfalls

- **Positions from the right.** Positions count from the right, starting at 0 for the check digit when validating and at 1 for the payload when generating. Mixing the two gives a wrong digit for every payload.
- **The order of the product.** $D$ is not commutative. The code computes $D[c][\cdot]$, with the running value on the left. Swapping the indices gives a different and wrong result.
- **Copying the tables.** One wrong entry breaks the guarantees without any visible error. Test the group axioms and the condition $a \ast \sigma(b) \ne b \ast \sigma(a)$, as the tests here do.
- **Leading zeros.** See above: 04 is valid but 00 is not, while 0 alone is valid.

## Implementations

## History

Jacobus Verhoeff, a Dutch mathematician, studied the errors that people make when they copy decimal numbers and classified them into single errors, transpositions, twin errors, jump transpositions, jump twin errors and phonetic errors. In Error Detecting Decimal Codes (Mathematical Centre Tracts 29, 1969) he showed that single errors and adjacent transpositions are by far the most frequent, and he built this scheme on the dihedral group of order 10 to catch both. Gallian's 1996 survey made it widely known among programmers. Later work, such as the thesis of H. Michael Damm (2004), found a scheme with the same guarantees from a single quasigroup table.

## References
