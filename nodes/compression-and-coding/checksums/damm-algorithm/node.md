---
tag: B1H68B
kind: algorithm
slug: damm-algorithm
name: Damm algorithm
aliases:
- Damm check digit
area: compression-and-coding/checksums
level: advanced
summary: Decimal check digit from one 10 by 10 table, a quasigroup with a zero diagonal that is weakly totally anti-symmetric. It catches every single error and every adjacent transposition.
model: word-ram
complexity:
  vars: {n: the number of digits}
  time: {worst: Θ(n), average: Θ(n), best: Θ(n)}
  space: {extra: Θ(1)}
properties: {deterministic: true, recursive: false, online: true, comparison: false}
history:
  year: 2004
  people: [H. Michael Damm]
  note: Damm presented totally anti-symmetric quasigroups and their use for check digits in his doctoral thesis at the Philipps-Universitat Marburg in 2004.
prereqs: [check-digit-computation]
see_also: [verhoeff-algorithm, luhn-algorithm, latin-square-completion, finite-group, permutation, error-detection]
sources:
  - paper: "H. Michael Damm, Total anti-symmetrische Quasigruppen, Dissertation, Philipps-Universitat Marburg, 2004"
    title: H. Michael Damm, Total anti-symmetrische Quasigruppen, doctoral thesis, Marburg, 2004
    locator: The definition of totally anti-symmetric quasigroups, the check digit method with one quasigroup, and the table of order 10 (page 111 in the copy cited by Wikipedia)
  - paper: "H. Michael Damm, Totally anti-symmetric quasigroups for all orders n ≠ 2, 6, Discrete Mathematics 307(6), 2007, pages 715 to 729"
    title: H. Michael Damm, Totally anti-symmetric quasigroups for all orders n ≠ 2, 6, Discrete Mathematics, 2007
    locator: The construction of totally anti-symmetric quasigroups of every order other than 2 and 6, and their use for check digit systems
  - paper: "J. Verhoeff, Error Detecting Decimal Codes, Mathematical Centre Tracts 29, Mathematisch Centrum, Amsterdam, 1969"
    title: J. Verhoeff, Error Detecting Decimal Codes, Mathematical Centre Tracts 29, 1969
    locator: The error classes (single, adjacent transposition, twin, jump transposition, jump twin) used in the comparison
---

The Damm algorithm computes a decimal check digit with a single table $Q$ of 10 rows and 10 columns. Start with the interim digit 0, and for each digit $d$ of the number, from the left, replace the interim digit $c$ by $Q[c][d]$. The check digit of a payload is the final interim digit, and a full number is valid when the final interim digit is 0. H. Michael Damm built such tables in his 2004 thesis. Every row and every column of $Q$ is a permutation of the digits, so $Q$ is a quasigroup and a Latin square; its diagonal is zero; and it is weakly totally anti-symmetric: $(c \ast x) \ast y = (c \ast y) \ast x$ only if $x = y$. These three facts give the same guarantee as the [Verhoeff algorithm](/verhoeff-algorithm/), all single errors and all adjacent transpositions, but with one table, no permutation and no inverse table, and leading zeros do not change the result. The [Luhn algorithm](/luhn-algorithm/) is simpler and misses 09 and 90.

## In plain words

You have a 10 by 10 table of digits. Start at row 0. Take the first digit of the number, go to that column, and read the entry: that is your new row. Take the next digit, go to that column in the new row, read the entry, and so on. The row you end on is the check digit.

To check a full number, do the same walk over all its digits, including the check digit. Every entry on the diagonal of the table is 0, so if you are in row $c$ and the next digit is $c$, you land on 0. So a correct number ends on 0. The table is built so that one wrong digit, or two neighbors swapped, always sends the walk to a different row at the end.

## The problem

The input is a payload of $n$ decimal digits $x_1 \ldots x_n$, read from the left; the output is one check digit. Write $a \ast b = Q[a][b]$. The table must satisfy:

- **Quasigroup (Latin square).** Each row and each column holds every digit once. So for all $a, b$ the equations $a \ast x = b$ and $y \ast a = b$ have unique solutions. A Latin square is the object of [Latin square completion](/latin-square-completion/).
- **Zero diagonal.** $x \ast x = 0$ for every digit $x$.
- **Weak total anti-symmetry.** For all $c, x, y$: if $(c \ast x) \ast y = (c \ast y) \ast x$ then $x = y$.

Unlike a group, $\ast$ need not be associative and has no identity, so the order of the walk is part of the definition. We count table lookups in the [word RAM](/word-ram/).

## The algorithm

The table used here is the one printed in the Wikipedia article on the algorithm, which takes it from Damm's thesis and orders the rows so that the diagonal is zero:

| $Q$ | 0 | 1 | 2 | 3 | 4 | 5 | 6 | 7 | 8 | 9 |
|---|---|---|---|---|---|---|---|---|---|---|
| **0** | 0 | 3 | 1 | 7 | 5 | 9 | 8 | 6 | 4 | 2 |
| **1** | 7 | 0 | 9 | 2 | 1 | 5 | 4 | 8 | 6 | 3 |
| **2** | 4 | 2 | 0 | 6 | 8 | 7 | 1 | 3 | 5 | 9 |
| **3** | 1 | 7 | 5 | 0 | 9 | 8 | 3 | 4 | 2 | 6 |
| **4** | 6 | 1 | 2 | 3 | 0 | 4 | 5 | 9 | 7 | 8 |
| **5** | 3 | 6 | 7 | 4 | 2 | 0 | 9 | 5 | 8 | 1 |
| **6** | 5 | 8 | 6 | 9 | 7 | 2 | 0 | 1 | 3 | 4 |
| **7** | 8 | 9 | 4 | 5 | 3 | 6 | 2 | 0 | 1 | 7 |
| **8** | 9 | 4 | 3 | 8 | 6 | 1 | 7 | 2 | 0 | 5 |
| **9** | 2 | 5 | 8 | 1 | 4 | 3 | 6 | 7 | 9 | 0 |

```pseudo id=main
INTERIM(x)                                   ▷ x read from the left
L1  c ← 0
L2  for each digit d of x, from left to right do
L3      c ← Q[c][d]
L4  return c

CHECK-DIGIT(p)
L5  return INTERIM(p)

IS-VALID(w)
L6  return INTERIM(w) = 0
```

Line L5 works because after the payload the interim digit is $c$, and the check digit $c$ then gives $Q[c][c] = 0$.

## Example

The payload 572. The walk is $0 \to Q[0][5] = 9 \to Q[9][7] = 7 \to Q[7][2] = 4$, so the check digit is 4. Validating 5724 continues with $Q[4][4] = 0$, so it is valid. The swap 5742 gives $9, 7, Q[7][4] = 3, Q[3][2] = 5$, not 0, so it is caught. The tests check these values, the walk, and that 00572 has the same check digit as 572.

## Correctness

A single error at position $i$ changes the interim digit right after position $i$, because each row of $Q$ is a permutation. An adjacent transposition $xy \to yx$ changes it after position $i + 1$, by weak total anti-symmetry. After that, each further step maps the interim digit by a column of $Q$, which is a permutation, so two different interim digits stay different to the end. The correct walk ends at 0, so the wrong one does not. The tests check that $Q$ is a Latin square, that its diagonal is zero, and the anti-symmetry condition for all 1,000 triples. The full proof is in the correctness file below.

## Complexity

Each digit costs one table lookup, so validation and generation take $\Theta(n)$ time and $\Theta(1)$ extra space. The table has 100 entries. The walk reads from the left, so digits can be checked as they arrive.

## Properties

Over all 10,000 payloads of 4 digits (5-digit code words), the tests count the missed errors of each class exactly. The numbers for Luhn and Verhoeff come from the same count in their own tests:

| error | example | of | Luhn | Verhoeff | Damm |
|---|---|---|---|---|---|
| single error | $a \to b$ | 450,000 | 0 | 0 | 0 |
| adjacent transposition | $ab \to ba$ | 36,000 | 800 | 0 | 0 |
| twin error | $aa \to bb$ | 36,000 | 2,400 | 1,600 | 3,520 |
| jump transposition | $abc \to cba$ | 27,000 | 27,000 | 1,560 | 2,498 |
| jump twin error | $aca \to bcb$ | 27,000 | 3,000 | 1,560 | 3,122 |

| | Luhn | Verhoeff | Damm |
|---|---|---|---|
| structure | doubling map, sum mod 10 | dihedral group $D_5$ and a permutation of order 8 | one quasigroup |
| tables | 10 entries | 100 + 80 + 10 entries | 100 entries |
| reading order | from the right | from the right | from the left |
| leading zeros | no effect | change the check digit | no effect |
| all adjacent swaps caught | no (misses 09, 90) | yes | yes |

So Damm and Verhoeff are equal on the two main classes. Verhoeff misses fewer twin and jump errors with this table; Damm is simpler and reads left to right.

- **Leading zeros.** $Q[0][0] = 0$, so zeros at the start keep the interim digit at 0. The check digit of 0 is 0, and 0 and 00 are valid.
- **One valid digit.** For each payload exactly one check digit is valid, because row $c$ has its single 0 at column $c$. The tests check this on random payloads.

## Variants and improvements

- **Totally anti-symmetric quasigroups.** Damm's thesis studies quasigroups that also satisfy $x \ast y = y \ast x \Rightarrow x = y$. The form on this page, which starts at 0 and has a zero diagonal, needs only the weak condition. The proof shows that the weak condition alone catches every adjacent swap, including a swap of the check digit with the last payload digit.
- **Other orders.** Damm (2007) showed that totally anti-symmetric quasigroups exist for every order $n \ne 2, 6$. So the method works for alphabets of letters and digits, for example $n = 36$ or 37, with one table each.
- **[Verhoeff algorithm](/verhoeff-algorithm/).** A group with a permutation in place of a quasigroup. It needs non-commutativity, since no permutation works in $\mathbb{Z}_{10}$.
- **[Luhn algorithm](/luhn-algorithm/).** The common choice for payment cards, with the 09/90 gap.

## When to use it

Use Damm for a new decimal identifier that people type or read aloud, when you want all single errors and adjacent swaps caught with one digit and the simplest correct code: one table, one loop, left to right, and no trouble with leading zeros. Use [Luhn](/luhn-algorithm/) when a standard requires it, and [Verhoeff](/verhoeff-algorithm/) where an existing system uses it. None of them protects against deliberate changes.

## Pitfalls

- **The table.** Not every Latin square works. The table must have the anti-symmetry property, and the zero diagonal is needed for the check digit to be the final interim digit. A mistyped entry breaks the guarantee without any visible error, so test the three properties, as the tests here do.
- **Index order.** The interim digit is the row and the new digit is the column. $Q$ is not symmetric, so $Q[d][c]$ is wrong.
- **The direction.** Damm reads from the left. Reading from the right gives a different and unrelated check digit.
- **Table versions.** Damm's thesis and later sources print different tables of the same kind. Two systems agree only if they use the same table.

## Implementations

## History

H. Michael Damm wrote his doctoral thesis on totally anti-symmetric quasigroups at the Philipps-Universitat Marburg in 2004. Such quasigroups had been studied for check digit systems before, but Damm gave constructions and showed how to use one with a zero diagonal so that the check digit is simply the last interim digit. In 2007 he published in Discrete Mathematics the result that totally anti-symmetric quasigroups exist for all orders except 2 and 6. His method gives the guarantee of [Verhoeff](/verhoeff-algorithm/) (1969) with a single table.

## References
