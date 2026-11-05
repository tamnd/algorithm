---
tag: Q7YN5H
kind: definition
slug: palindrome
name: Palindrome
aliases:
- palindromic string
area: strings/palindromes
level: intro
summary: A string that reads the same forwards and backwards.
prereqs: [alphabet]
see_also: [palindrome-recognition, longest-palindromic-substring, manacher, palindromic-tree, palindrome-count-bound, rich-string, reverse-complement-palindrome, longest-palindromic-subsequence]
sources:
  - book: isbn:9780521585194
    title: Dan Gusfield, Algorithms on Strings, Trees, and Sequences, Cambridge University Press, 1997
    locator: Chapter 9, Section 9.2, Finding all maximal palindromes in linear time (pages 197 to 199)
  - paper: doi:10.1016/S0304-3975(99)00320-5
    title: Xavier Droubay, Jacques Justin and Giuseppe Pirillo, Episturmian words and some constructions of de Luca and Rauzy, Theoretical Computer Science 255 (2001), 539-553
    locator: Proposition 2 (a word w has at most |w| + 1 distinct palindromic factors, the empty word included)
  - paper: doi:10.1016/j.ejc.2008.04.006
    title: Amy Glen, Jacques Justin, Steve Widmer and Luca Q. Zamboni, Palindromic richness, European Journal of Combinatorics 30 (2009), 510-531
    locator: the introduction (reversal and palindromes) and Section 2 (Proposition 2.1 and Definition 2.2)
  - url: https://en.wikipedia.org/wiki/Palindrome
    title: Wikipedia, Palindrome
    locator: the whole article, for the words, the normalization of phrases and the uses in science
---

A palindrome is a string that is equal to its own reversal, so it reads the same from left to right and from right to left, like `racecar` or `abba`. Palindromes are a basic object of string algorithms: [palindrome recognition](/palindrome-recognition/) tests one string, [Manacher's algorithm](/manacher/) finds all palindromes inside a string in linear time, and the [palindromic tree](/palindromic-tree/) stores the distinct ones. A string of length $n$ contains at most $n + 1$ distinct palindromes, a fact with its own page, the [palindrome count bound](/palindrome-count-bound/).

## Definition

Let $\Sigma$ be an [alphabet](/alphabet/). The only operation that this page and the pages of this area need on $\Sigma$ is a test of equality of two symbols. No order on the symbols is needed, and $\Sigma$ may be infinite. A string of length $n$ is $w = w[0]\,w[1] \cdots w[n-1]$ with $w[i] \in \Sigma$. Indices are 0-based on this page and on the other pages of the palindromes area. $w[i..j]$ is the substring $w[i] \cdots w[j]$, both ends included, and it is empty when $j < i$.

**Reversal.** The reversal of $w$ is the string $w^R$ of the same length with
$$ w^R[i] = w[n-1-i] \qquad \text{for } 0 \le i \le n-1. $$

**Palindrome.** The string $w$ is a palindrome if $w = w^R$, that is, if
$$ w[i] = w[n-1-i] \qquad \text{for each } i \text{ with } 0 \le i \le n-1. $$
It is enough to check the indices $0 \le i < \lfloor n/2 \rfloor$, because the condition for $i$ and for $n - 1 - i$ is the same equation, and for $n$ odd the middle index $i = (n-1)/2$ gives $w[i] = w[i]$.

**Even and odd palindromes.** A palindrome of odd length $2k+1$ has a middle symbol $w[k]$, which can be any symbol, and $w = u\,a\,u^R$ with $|u| = k$ and $a \in \Sigma$. A palindrome of even length $2k$ has no middle symbol, and $w = u\,u^R$ with $|u| = k$. So each palindrome has the form $u u^R$ or $u a u^R$, and each string of these forms is a palindrome. The empty string $\varepsilon$ is an even palindrome, and each single symbol is an odd palindrome.

**Center and radius.** An occurrence $s[i..j]$ of a palindrome inside a string $s$ has its center at $(i + j)/2$. The center is an integer (a symbol) for odd length and a half-integer (a gap between two symbols) for even length. A string of length $n$ has $2n + 1$ possible centers: the $n$ symbols and the $n + 1$ gaps, including the two ends. If $s[i..j]$ is a palindrome and $i < j$, then $s[i+1..j-1]$ is a palindrome with the same center. So the palindromes with one center are nested, and the longest one, the **maximal palindrome** at that center, determines all of them. [Manacher's algorithm](/manacher/) computes the maximal palindrome at each of the $2n + 1$ centers.

**Palindromic substrings.** A palindromic substring (or palindromic factor) of $s$ is a substring that is a palindrome. Two counts are common, and the pages of this area say which one they use: occurrences, counted by position $(i, j)$, and distinct palindromes, counted as strings. The string `banana` has 10 palindromic occurrences, but only 6 distinct nonempty palindromes: `a`, `b`, `n`, `ana`, `nan`, `anana`.

### Basic facts

1. **Number of palindromes.** Over an alphabet of size $\sigma$, there are exactly $\sigma^{\lceil n/2 \rceil}$ palindromes of length $n$. *Proof.* A palindrome is fixed by its first $\lceil n/2 \rceil$ symbols, because each later symbol $w[n-1-i]$ equals $w[i]$ with $i < \lceil n/2 \rceil$. Each choice of the first $\lceil n/2 \rceil$ symbols gives a palindrome: set $w[n-1-i] = w[i]$ for the other positions. This map is a bijection. $\square$
2. **Reversal of a product.** $(uv)^R = v^R u^R$. So $u v u^R$ is a palindrome whenever $v$ is a palindrome.
3. **Palindromic suffixes of a palindrome are borders.** Let $w$ be a palindrome and $u$ a suffix of $w$. Then $u$ is a palindrome if and only if $u$ is also a prefix of $w$, that is, a [border](/border/) of $w$. *Proof.* Since $u$ is a suffix of $w$, $u^R$ is a prefix of $w^R = w$. If $u$ is a palindrome, then $u = u^R$ is a prefix. Conversely, if $u$ is a prefix of $w$, then $u$ and $u^R$ are both prefixes of $w$ of the same length, so $u = u^R$. $\square$
4. **Periods.** If $u$ is a palindromic suffix of a palindrome $w$, then $|w| - |u|$ is a [period](/string-period/) of $w$, by fact 3 and the fact that a border of length $b$ gives the period $|w| - b$. So the shortest period of a palindrome $w$ is $|w| - |u|$, where $u$ is its longest proper palindromic suffix. This fact is the base of the [palindromic tree](/palindromic-tree/) and of [series links](/series-links/).

## Examples and non-examples

**Palindromes.**

- $\varepsilon$, `a`, `aa`, `aba`, `abba`, `racecar`, `noon`.
- `eertree`: the symbols at the indices $0$ to $6$ are `e e r t r e e`, and $w[i] = w[6-i]$ for $i = 0, 1, 2$. It is odd, with center `t`.
- $a^n$ for each $n \ge 0$, and $u u^R$ for each string $u$.
- Over $\{a, b\}$ there are $1, 2, 2, 4, 4, 8, 8$ palindromes of length $0, 1, \ldots, 6$, which is $2^{\lceil n/2 \rceil}$.
- The DNA string `GAATTC` is not a palindrome in the sense of this page, but it equals its own reverse complement. That is a different notion, the [reverse-complement palindrome](/reverse-complement-palindrome/).

**Non-examples.**

- `ab`: $w[0] = a \ne b = w[1]$.
- `abca`: the outer symbols match, but $w[1] = b \ne c = w[2]$.
- `Never odd or even` as written: the reversal is `neve ro ddo reveN`. The phrase is a palindrome only after a normalization that removes spaces and ignores case. Programs must say which normalization they apply, if any, before the test.
- `abab`: it has the period 2 and the border `ab`, but $w^R = $ `baba` $\ne w$. A string with a border is not, in general, a palindrome.

**Inside a string.** The string `abaab` has 11 centers. Its nonempty palindromic occurrences are the five single symbols, `aba` $= s[0..2]$ with center 1, and `aa` $= s[2..3]$ and `baab` $= s[1..4]$, which share the center 2.5. So there are 8 occurrences, and the distinct nonempty palindromes are `a`, `b`, `aa`, `aba` and `baab`, five of them for a string of length 5.

## Related definitions

- **[Palindrome recognition](/palindrome-recognition/).** The problem of testing whether a string is a palindrome, in $\lfloor n/2 \rfloor$ comparisons.
- **Maximal palindrome.** The longest palindrome with a given center. The list of the $2n + 1$ maximal palindromes describes all palindromic substrings, and [Manacher's algorithm](/manacher/) computes it in $O(n)$ time.
- **[Longest palindromic substring](/longest-palindromic-substring/)** and **[longest palindromic subsequence](/longest-palindromic-subsequence/).** A substring is contiguous, a subsequence is not. The first is found in linear time, the second by an $O(n^2)$ dynamic program.
- **[Palindromic closure](/palindromic-closure/)** and **[shortest palindrome](/shortest-palindrome/).** The shortest palindrome that has a given string as a prefix or as a suffix.
- **[Rich string](/rich-string/).** A string of length $n$ with the maximum number $n + 1$ of distinct palindromic substrings, counting $\varepsilon$.
- **[Reverse-complement palindrome](/reverse-complement-palindrome/)** and **[gapped palindrome](/gapped-palindrome/).** A string equal to the complement of its reversal, as in DNA; and a string $u v u^R$ with a gap $v$ between the two arms.
- **Language.** The set of all palindromes over an alphabet with at least two symbols is a [context-free language](/context-free-language/), generated by $S \to \varepsilon \mid a \mid a S a$ for each $a \in \Sigma$. It is not regular: the strings $a^i b$ for $i \ge 0$ are pairwise distinguishable, because $a^i b\, a^i$ is a palindrome and $a^j b\, a^i$ is not for $j \ne i$, so by the [Myhill-Nerode theorem](/myhill-nerode-theorem/) no finite automaton accepts the palindromes.

## References
