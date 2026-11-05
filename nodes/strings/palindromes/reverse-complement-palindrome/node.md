---
tag: TH5GJQ
kind: concept
slug: reverse-complement-palindrome
name: Reverse-complement palindrome
aliases:
- DNA palindrome
- biological palindrome
area: strings/palindromes
level: intro
summary: A DNA sequence equal to its own reverse complement, as in restriction enzyme sites.
prereqs: [palindrome]
see_also: [manacher, gapped-palindrome, longest-palindromic-substring, palindrome-recognition, genome-repeat, longest-common-extension-query, suffix-tree]
sources:
  - book: isbn:9780521585194
    title: Dan Gusfield, Algorithms on Strings, Trees, and Sequences, Cambridge University Press, 1997
    locator: Chapter 9, Section 9.2, Finding all maximal palindromes in linear time (pages 197 to 199), with complemented palindromes in DNA
  - paper: arxiv:1703.08931
    title: Michał Adamczyk, Mai Alzamel, Panagiotis Charalampopoulos, Costas S. Iliopoulos and Jakub Radoszewski, Palindromic decompositions with gaps and errors, CSR 2017
    locator: Section 1 and the preliminaries (generalized palindromes under an involution, complemented palindromes, and hairpins of the form x followed by its reverse complement)
  - url: https://en.wikipedia.org/wiki/Palindromic_sequence
    title: Wikipedia, Palindromic sequence
    locator: the lead and the section Restriction enzyme sites (EcoRI, BamHI, TaqI and AluI, and hairpins)
---

A reverse-complement palindrome is a DNA string that is equal to its reverse complement: reverse it, then replace each base by its partner (A with T, C with G), and the result is the same string, as for `GAATTC`. In double-stranded DNA this means that both strands read the same sequence in their own 5' to 3' direction. Many restriction enzymes recognize sites of this kind. It is a [palindrome](/palindrome/) in a changed sense, where the mirror symbol must be the complement and not the same symbol, and the algorithms for ordinary palindromes carry over with one change in the symbol test.

## In plain words

DNA has two strands that run in opposite directions, and each letter on one strand pairs with a fixed partner letter on the other strand. Read one strand from its start, then read the other strand from its own start. For most stretches the two readings differ. For some stretches they are the same, and biologists call such a stretch a palindrome. As one string of letters, it is not the same when you read it backward. It is the same when you read it backward and also swap each letter for its partner. Since no letter is its own partner, these stretches always have an even number of letters, and the middle is between two letters.

## The idea

**Complement and reverse complement.** Let $\Sigma = \{A, C, G, T\}$ with the complement map $\overline{A} = T$, $\overline{T} = A$, $\overline{C} = G$, $\overline{G} = C$. For a string $s = s[0..n-1]$, with 0-based indices, the reverse complement is
$$ \mathrm{rc}(s)[i] = \overline{s[n-1-i]} \qquad \text{for } 0 \le i \le n-1. $$
The string $s$ is a reverse-complement palindrome (Gusfield calls it a *complemented palindrome*) if $s = \mathrm{rc}(s)$, that is, if $s[i] = \overline{s[n-1-i]}$ for each $i$.

**Only even lengths.** If $n$ is odd, the middle index $k = (n-1)/2$ would need $s[k] = \overline{s[k]}$, but no base is its own complement. So each nonempty reverse-complement palindrome has even length $2k$ and has the form $u\,\mathrm{rc}(u)$ with $|u| = k$, and each string of that form is one. Its center is the gap between $s[k-1]$ and $s[k]$. So there are exactly $4^{n/2}$ reverse-complement palindromes of each even length $n$, and none of odd length.

**Different from ordinary palindromes.** A string that is both a palindrome and a reverse-complement palindrome satisfies $s[n-1-i] = s[i] = \overline{s[n-1-i]}$, which is impossible for $n \ge 1$. So only the empty string is both. `GAATTC` reversed is `CTTAAG`, so it is not an ordinary palindrome.

**The general model.** Adamczyk, Alzamel, Charalampopoulos, Iliopoulos and Radoszewski define a generalized palindrome for any involution $f$ on the alphabet ($f(f(a)) = a$): $s$ is an $f$-palindrome if $s[i] = f(s[n-1-i])$ for each $i$. The identity gives ordinary palindromes and the DNA complement gives this page. If $f$ has fixed points, odd $f$-palindromes exist, with a fixed point in the middle. The algorithms need only the test "$s[i] = f(s[j])$?".

**Algorithms carry over.** The key facts about palindromes stay true for $f$-palindromes: removing the first and last symbol of an $f$-palindrome leaves an $f$-palindrome with the same center, so the $f$-palindromes with one center are nested. If $x$ is an $f$-palindrome and $y$ occurs in $x$, then the mirror occurrence of $f(y^R)$ also occurs in $x$, and $f(y^R)$ is an $f$-palindrome exactly when $y$ is. That is all that [Manacher's algorithm](/manacher/) uses, so it computes the maximal reverse-complement palindrome at each of the $n + 1$ gaps in $O(n)$ time, with the test $s[i] = \overline{s[j]}$ in place of $s[i] = s[j]$. Gusfield computes them with a [suffix tree](/suffix-tree/) of $s$ and $\mathrm{rc}(s)$ and [longest common extension queries](/longest-common-extension-query/).

**Hairpins.** A string $u\,g\,\mathrm{rc}(u)$ with a loop $g$ between the two arms can fold back on itself: the arm $u$ pairs with $\mathrm{rc}(u)$ to form a stem, and $g$ forms a loop. This is a [gapped palindrome](/gapped-palindrome/) in the reverse-complement sense.

## Examples

**Restriction sites.** The recognition sites below are reverse-complement palindromes and are not ordinary palindromes.

| enzyme | site (5' to 3') | reverse | reverse complement |
| --- | --- | --- | --- |
| EcoRI | `GAATTC` | `CTTAAG` | `GAATTC` |
| BamHI | `GGATCC` | `CCTAGG` | `GGATCC` |
| HindIII | `AAGCTT` | `TTCGAA` | `AAGCTT` |
| EcoRV | `GATATC` | `CTATAG` | `GATATC` |
| TaqI | `TCGA` | `AGCT` | `TCGA` |
| AluI | `AGCT` | `TCGA` | `AGCT` |

**Radii at the gaps.** For $s = $ `TAGTCGACTA` ($n = 10$) let $R[g]$, for $0 \le g \le n$, be the largest $r$ such that $s[g-r..g+r-1]$ is a reverse-complement palindrome, so that the gap $g$ lies between $s[g-1]$ and $s[g]$.

| $g$ | 0 | 1 | 2 | 3 | 4 | 5 | 6 | 7 | 8 | 9 | 10 |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| $R[g]$ | 0 | 1 | 0 | 0 | 0 | 5 | 0 | 0 | 0 | 1 | 0 |

At $g = 5$ the radius 5 covers the whole string, so `TAGTCGACTA` is a reverse-complement palindrome. At $g = 1$ the radius 1 gives `TA`, whose reverse complement is `TA`. For `TTATAA` the radii at the gaps 2, 3 and 4 are 1, 3 and 1: the reverse-complement palindromes `AT`, `TATA`, `TTATAA` share the center 3 and are nested, and only `TTATAA` is maximal.

**Non-examples.** `AGTACTTCATGA` is an ordinary palindrome and not a reverse-complement palindrome, because $s[0] = A$ and $\overline{s[11]} = T$. `GAATTA` is not one: $s[0] = G$ but $\overline{s[5]} = T$. No string of odd length is one.

**A hairpin.** `GCAT` `TTTT` `ATGC` is $u\,g\,\mathrm{rc}(u)$ with $u = $ `GCAT` and loop `TTTT`. The whole string is not a reverse-complement palindrome, because the loop `TTTT` is not one.

## Where it is used

- **Restriction enzymes.** Many restriction enzymes bind a short reverse-complement palindrome and cut both strands there. Finding all sites of an enzyme is a [string matching](/string-matching/) task, and finding all such palindromes in a genome is the reverse-complement version of [Manacher's algorithm](/manacher/).
- **Secondary structure.** Hairpins and stem-loops in DNA and RNA come from approximate reverse-complement gapped palindromes, see [RNA secondary structure](/rna-secondary-structure/).
- **Repeats in genomes.** Inverted repeats, an arm and its reverse complement at some distance, are one of the kinds of [genome repeats](/genome-repeat/). Programs that search for repeats test both the string and its reverse complement.
- **String algorithms with an involution.** Results for palindromes that use only equality tests extend to $f$-palindromes, for example the palindromic decompositions with gaps and errors of Adamczyk et al.

## References
