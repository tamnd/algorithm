---
tag: 2YWNJQ
kind: concept
slug: gapped-palindrome
name: Gapped palindrome
aliases:
- gapped inverted repeat
area: strings/palindromes
level: research
summary: A palindrome with a fixed-length gap between its two halves, studied for repeat detection.
prereqs: [palindrome, reverse-complement-palindrome]
see_also: [manacher, palindrome-substring-queries, palindrome-edit-distance, rna-secondary-structure, runs-theorem, suffix-tree, lowest-common-ancestor]
sources:
  - paper: doi:10.1016/j.tcs.2009.09.013
    title: Roman Kolpakov and Gregory Kucherov, Searching for gapped palindromes, Theoretical Computer Science 410(51) (2009), 5365-5373
    locator: the definitions of maximal gapped palindromes, long-armed palindromes and length-constrained palindromes, and the O(n + S) algorithms for a constant-size alphabet, S the output size
  - paper: doi:10.1007/s00224-017-9794-5
    title: Paweł Gawrychowski, Tomohiro I, Shunsuke Inenaga, Dominik Köppl and Florin Manea, Tighter bounds and optimal algorithms for all maximal α-gapped repeats and palindromes, Theory of Computing Systems 62(1) (2018), 162-191
    locator: the definition of α-gapped palindromes, the O(αn) bound on the number of maximal ones, and the O(αn) algorithm that lists them
  - paper: doi:10.1016/j.tcs.2018.06.033
    title: Tomohiro I and Dominik Köppl, Improved upper bounds on all maximal α-gapped repeats and palindromes, Theoretical Computer Science 753 (2019), 1-15
    locator: the improved constants in the bound on the number of maximal α-gapped palindromes
  - book: isbn:9780521585194
    title: Dan Gusfield, Algorithms on Strings, Trees, and Sequences, Cambridge University Press, 1997
    locator: Chapter 9, Section 9.2, Finding all maximal palindromes in linear time (longest common extension queries between a string and its reverse, the tool for arms of gapped palindromes)
---

A gapped palindrome is a string $u\,v\,u^R$: an *arm* $u$, a *gap* $v$ of any content, and the reversal of the arm. The gap length $g = |v|$ is part of the description, and the problem asks for all gapped palindromes whose gap satisfies a constraint, such as a fixed length, a length in a range, or a length that is small compared with the arm. Ordinary [palindromes](/palindrome/) are the cases with gap 0 or 1. In DNA, the same shape with the reverse complement in place of the reversal is a hairpin: a stem of paired bases around a loop.

## In plain words

Write a word, then any short piece of filler, then the first word backwards. The whole thing is a gapped palindrome. The filler is the gap, and the two copies of the word are the arms. A normal palindrome is the case where the filler is empty or one letter long. To find gapped palindromes in a long text, you choose where the gap is and how long it is, and then match letters outward from the two ends of the gap for as long as they agree. The number of matches is the length of the arm. Most interest is in long arms around short gaps, because those are the shapes that stand out from chance.

## The idea

**Conventions.** Indices are 0-based and $s[i..j]$ includes both ends. Symbols are only tested for equality; for DNA, the test "is the complement of" replaces equality, as on the [reverse-complement palindrome](/reverse-complement-palindrome/) page.

**Definition.** A *gapped palindrome* in $s$ with gap $s[p..p+g-1]$ and arm length $a \ge 1$ is the substring $s[p-a..p+g+a-1]$ with
$$ s[p-1-t] = s[p+g+t] \quad \text{for } 0 \le t < a. $$
It is *maximal* if the arm cannot grow: $p - a = 0$, or $p + g + a = n$, or $s[p-1-a] \ne s[p+g+a]$. For each gap position $(p, g)$ there is one maximal arm length $A(p, g)$, possibly 0.

- **Gap 0.** $A(p, 0) \ge 1$ means an even palindrome with center between $p - 1$ and $p$.
- **Gap 1.** $A(p, 1)$ is the radius of the odd palindrome with center $p$, beyond the center symbol.
- **Other gaps.** The gap content is free. A gap that is itself a palindrome gives an ordinary palindrome, so the interesting cases have a gap that is not one.

**Constraints on the gap.** Without a constraint every pair of equal symbols is a gapped palindrome, so the problem fixes one:

- **Length-constrained.** The gap length lies in a given range $[g_1, g_2]$ (Kolpakov and Kucherov).
- **Long-armed.** The arm is long compared with the gap (Kolpakov and Kucherov).
- **$\alpha$-gapped.** $|u\,v| \le \alpha |u|$ for a fixed $\alpha \ge 1$, that is, the gap is at most $(\alpha - 1)$ times the arm (Gawrychowski, I, Inenaga, Köppl and Manea).

**Computing arms.** $A(p, g)$ is a longest common extension: the longest common prefix of the reversed prefix $s[0..p-1]^R$ and the suffix $s[p+g..n-1]$. With a [suffix tree](/suffix-tree/) of $s\,\#\,s^R$ and constant-time [lowest common ancestor](/lowest-common-ancestor/) queries, each $A(p, g)$ takes $O(1)$ time after $O(n)$ preprocessing for a constant alphabet. Gusfield uses these queries for the maximal palindromes. So all maximal gapped palindromes with one gap length $g$ come in $O(n)$ time, and with all gap lengths up to $G$ in $O(nG)$ time.

**Output-sensitive algorithms.** Kolpakov and Kucherov list all maximal long-armed and all maximal length-constrained gapped palindromes in $O(n + S)$ time for a constant alphabet, where $S$ is the number of output palindromes. For $\alpha$-gapped palindromes, Gawrychowski et al. show that a string of length $n$ has $O(\alpha n)$ maximal ones and list them in $O(\alpha n)$ time, which is optimal; I and Köppl improve the constant in the bound.

## Examples

Let $s = $ `aabcdbaa`, of length 8. The table gives $A(p, g)$ for each gap start $p$ and each gap length $g \le 3$.

| $g$ \ $p$ | 0 | 1 | 2 | 3 | 4 | 5 | 6 | 7 | 8 |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 0 | 0 | 1 | 0 | 0 | 0 | 0 | 0 | 1 | 0 |
| 1 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | |
| 2 | 0 | 0 | 0 | 3 | 0 | 0 | 0 | | |
| 3 | 0 | 0 | 0 | 0 | 0 | 0 | | | |

The entry $A(3, 2) = 3$ is the gapped palindrome `aab` $\cdot$ `cd` $\cdot$ `baa`, the whole string, with arm `aab` and gap `cd`; it is maximal because it touches both ends of $s$. The row for gap 0 shows the two even palindromes `aa`, and the row for gap 1 shows that $s$ has no odd palindrome longer than 1. The string `aabcdbaa` is not a palindrome at all, but it is a gapped palindrome with a gap of length 2.

In DNA, the hairpin `GCGC` `TTTT` `GCGC` has the stem `GCGC`, whose reverse complement is `GCGC`, and the loop `TTTT`. With complement in place of equality, it is a gapped reverse-complement palindrome with arm 4 and gap 4.

## Where it is used

- **Biology.** Hairpins and stem-loop structures in DNA and RNA are gapped reverse-complement palindromes: the stem pairs with itself and the loop is the gap. They are a basic element of [RNA secondary structure](/rna-secondary-structure/) and of some regulatory signals.
- **Repeat detection.** Gapped palindromes are the inverted counterpart of gapped repeats $u\,v\,u$, and both are listed with the same techniques, often together, as in the work of Gawrychowski et al. and of Kolpakov and Kucherov.
- **Combinatorics on words.** The bound $O(\alpha n)$ on maximal $\alpha$-gapped palindromes is in the same family as the bound on runs, see the [runs theorem](/runs-theorem/).
- **Approximate palindromes.** Allowing mismatches or edits in the arms gives approximate gapped palindromes, as in [palindrome edit distance](/palindrome-edit-distance/).

## References
