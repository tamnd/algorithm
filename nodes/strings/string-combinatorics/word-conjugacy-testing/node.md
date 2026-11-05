---
tag: 2RD6JG
kind: problem
slug: word-conjugacy-testing
name: Conjugacy testing
aliases:
- conjugacy problem for words
- rotation equivalence test
area: strings/string-combinatorics
level: core
summary: Decide whether two words are rotations of each other.
model: comparison-model
complexity:
  vars: {n: the common length of the two words}
  time: {worst: Θ(n)}
  space: {aux: Θ(1)}
prereqs: [word-conjugacy, string-matching]
see_also: [minimal-rotation, shiloach-least-rotation, knuth-morris-pratt, z-algorithm, circular-pattern-matching, necklace, polynomial-rolling-hash, word-problem-for-groups]
sources:
  - paper: "Yossi Shiloach, A fast equivalence-checking algorithm for circular lists, Information Processing Letters 8(5), 1979, 236-238"
    locator: the whole paper (deciding whether two circular lists are equal in linear time with constant extra space)
  - paper: doi:10.1137/0206024
    title: Donald E. Knuth, James H. Morris and Vaughan R. Pratt, Fast pattern matching in strings, SIAM Journal on Computing 6(2), 1977, 323-350
    locator: the linear-time matching algorithm, applied to the text uu and the pattern v
  - book: isbn:9780521599245
    title: M. Lothaire, Combinatorics on Words, Cambridge Mathematical Library, Cambridge University Press, 1997
    locator: Chapter 1, Words (D. Perrin), conjugacy and the equation uz = zv
  - paper: doi:10.1016/0196-6774(81)90013-4
    title: Yossi Shiloach, Fast canonization of circular strings, Journal of Algorithms 2(2), 1981, 107-121
    locator: the canonical form of a circular string, which gives a conjugacy test by comparison of canonical forms
---

Conjugacy testing asks whether two words $u$ and $v$ are rotations of each other, that is, whether $u = xy$ and $v = yx$ for some words $x$ and $y$. The standard solution searches for $v$ in the doubled word $uu$ with a linear-time [string matching](/string-matching/) algorithm. Comparing the [least rotations](/minimal-rotation/) of the two words also takes linear time and needs only constant extra space.

## In plain words

Take two necklaces of letters and ask whether they are the same necklace, only cut open at different places. One way is to write the first word twice in a row: every way of cutting the first necklace then shows up as a stretch of that doubled word. So the second word is a cut of the first necklace exactly when it appears somewhere inside the doubled word, and a fast text search answers that. Another way is to turn both necklaces to their standard starting point, the cut that gives the word first in dictionary order, and then compare the two results letter by letter.

## Definition

**Input.** Two words $u = u[0..m-1]$ and $v = v[0..n-1]$ over an [alphabet](/alphabet/) $\Sigma$. The search method needs only equality tests between letters; the least-rotation method needs a total order on $\Sigma$ and three-way comparisons. Indices are 0-based.

**Output.** "Yes" if $u$ and $v$ are [conjugate](/word-conjugacy/), that is, if $m = n$ and $v = \mathrm{rot}_i(u) = u[i..n-1]\,u[0..i-1]$ for some $0 \le i \le n - 1$; "no" otherwise. Two empty words are conjugate.

**The doubling lemma.** For $|u| = |v| = n$, $v$ is a rotation of $u$ if and only if $v$ occurs in $uu$, and then the positions $i \in \{0, \ldots, n-1\}$ of the occurrences are exactly the shifts with $\mathrm{rot}_i(u) = v$. *Proof.* For $0 \le i \le n$, the factor of $uu$ of length $n$ at position $i$ has letters $(uu)[i + t] = u[(i + t) \bmod n]$, so it is $\mathrm{rot}_{i \bmod n}(u)$. $\square$ The occurrence at position $n$, if any, repeats the one at $0$.

## Variants

- **Find the shifts.** Report all $i$ with $\mathrm{rot}_i(u) = v$. They form an arithmetic progression $i_0, i_0 + d, \ldots$, where $d$ is the length of the [primitive root](/primitive-root-of-a-word/) of $u$.
- **Many words.** Group a set of words into conjugacy classes: compute the [least rotation](/minimal-rotation/) of each and sort or hash these canonical forms.
- **With errors.** Decide whether some rotation of $u$ is within Hamming or edit distance $k$ of $v$; this is approximate [circular pattern matching](/circular-pattern-matching/).
- **Up to reversal.** Decide whether $v$ is a rotation of $u$ or of its reversal, the equality of [bracelets](/bracelet/).
- **In free groups.** Two elements of a free group are conjugate if their cyclic reductions are rotations of each other; the conjugacy problem for free groups reduces to this one after cyclic reduction. See the [word problem for groups](/word-problem-for-groups/).

## Examples

| $u$ | $v$ | conjugate | shifts $i$ with $\mathrm{rot}_i(u) = v$ |
| --- | --- | --- | --- |
| `abaab` | `ababa` | yes | 3 |
| `waterbottle` | `erbottlewat` | yes | 3 |
| `abcabc` | `cabcab` | yes | 2, 5 |
| `aaaa` | `aaaa` | yes | 0, 1, 2, 3 |
| `aabb` | `abab` | no | none |
| `abc` | `acb` | no | none |
| `ab` | `abc` | no | lengths differ |

For `abaab` and `ababa`, the doubled word `abaababaab` contains `ababa` at position 3 only. For `abcabc`, the shifts 2 and 5 differ by $d = 3$, the length of the primitive root `abc`. In `aaaa` the doubled word contains `aaaa` at positions 0 to 4, and position 4 repeats position 0. The pair `aabb`, `abab` has equal letter counts, so a test by [Parikh vectors](/parikh-vector/) alone would wrongly accept it.

## Known algorithms

**Try every shift, $O(n^2)$.** Compare $v$ with $\mathrm{rot}_i(u)$ for $i = 0, \ldots, n-1$, letter by letter, stopping at the first mismatch. The worst case is about $n^2/2$ comparisons, for example $u = a^{n-1}b$ and $v = a^n$.

**Search in $uu$, $O(n)$ time and space.** Check $m = n$, then search for the pattern $v$ in the text $uu[0..2n-2]$ with [Knuth-Morris-Pratt](/knuth-morris-pratt/) or the [Z-algorithm](/z-algorithm/). This uses $O(n)$ time and $O(n)$ extra space, and only equality tests, so it works for unordered alphabets. Dropping the last letter of $uu$ removes the duplicate occurrence at position $n$.

```pseudo id=doubling
IS-CONJUGATE(u, v)
L1  if |u| ≠ |v| then return false
L2  t ← u · u[0 .. |u| − 2]
L3  return v occurs in t        ▷ any linear-time matcher
```

**Compare least rotations, $O(n)$ time and $O(1)$ space.** Compute the least rotation index of each word with [Shiloach's algorithm](/shiloach-least-rotation/) or the Lyndon factorization method, then compare the two rotations letter by letter in place. This needs an ordered alphabet.

**Direct scan of two circular lists, $O(n)$ time and $O(1)$ space.** Shiloach (1979) decides the equality of two circular lists directly, without first computing canonical forms, in linear time with constant extra space.

**Fingerprints, $O(n)$ expected.** With a [polynomial rolling hash](/polynomial-rolling-hash/), compute the fingerprints of all $n$ rotations of $u$ in $O(n)$ time and compare each with the fingerprint of $v$; a match is verified letter by letter, or accepted with a small error probability. This is the [Rabin-Karp](/rabin-karp/) search in $uu$.

**History.** The doubling trick is folklore and follows directly from the definition of conjugacy. Knuth, Morris and Pratt (1977) made the search linear. Shiloach (1979) gave the constant-space test for circular lists, and his 1981 paper on canonical forms of circular strings gave the least-rotation route.

## Bounds

**Upper bound.** $O(n)$ time with $O(1)$ extra space for an ordered alphabet; $O(n)$ time with $O(n)$ space using equality tests only.

**Lower bound.** At least $\lceil n/2 \rceil$ comparisons in the worst case, for an alphabet with at least two letters. *Proof.* On $u = v = a^n$ the answer is yes. Suppose some index $j$ of $v$ takes part in no comparison. Change $v[j]$ to $b$: all comparisons give the same results, so the algorithm still says yes, but now $v$ has a different number of letters `a` than $u$, so the words are not conjugate. So every index of $v$ takes part in some comparison, and a comparison involves at most two indices of $v$. $\square$

## Reductions

- **To string matching.** As in the doubling lemma: one search of a pattern of length $n$ in a text of length $2n - 1$.
- **To minimal rotation.** $u \sim v$ if and only if $|u| = |v|$ and the least rotations are equal.
- **Conjugacy in free groups.** After free and cyclic reduction, conjugacy of two elements of a free group is conjugacy of the reduced words, a classic step in combinatorial group theory.

## Applications

- **Circular sequences in biology.** Circular genomes and plasmids have no natural start, so two sequences are compared up to rotation.
- **Shape matching.** A closed contour coded by a chain of directions is the same shape after a change of starting point if and only if the two chains are conjugate.
- **Group theory.** Deciding whether two elements of a free group are conjugate, as above.
- **Interview problems.** The doubling trick, "is `erbottlewat` a rotation of `waterbottle`", is a standard exercise in string handling.

## References
