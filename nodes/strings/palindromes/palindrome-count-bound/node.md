---
tag: R2KDEY
kind: theorem
slug: palindrome-count-bound
name: Palindrome count bound
aliases:
- at most n+1 distinct palindromes
area: strings/palindromes
level: intro
summary: A string of length n has at most n+1 distinct palindromic substrings, counting the empty string.
prereqs: [palindrome]
see_also: [rich-string, palindromic-tree, count-palindromic-substrings, manacher, border, count-distinct-substrings, series-links]
sources:
  - paper: doi:10.1016/S0304-3975(99)00320-5
    title: Xavier Droubay, Jacques Justin and Giuseppe Pirillo, Episturmian words and some constructions of de Luca and Rauzy, Theoretical Computer Science 255 (2001), 539-553
    locator: Proposition 2 (at most |w| + 1 distinct palindromic factors) and Proposition 3 (equality if and only if each prefix has a unioccurrent palindromic suffix)
  - paper: doi:10.1016/j.ejc.2008.04.006
    title: Amy Glen, Jacques Justin, Steve Widmer and Luca Q. Zamboni, Palindromic richness, European Journal of Combinatorics 30 (2009), 510-531
    locator: Section 2, Proposition 2.1, Definition 2.2, Proposition 2.4 and Corollary 2.5; Section 4 (the defect and Proposition 4.1)
  - paper: doi:10.1142/S012905410400242X
    title: Srecko Brlek, Sylvie Hamel, Maurice Nivat and Christophe Reutenauer, On the palindromic complexity of infinite words, International Journal of Foundations of Computer Science 15(2) (2004), 293-306
    locator: the definition of the palindromic defect and the words with defect 0 (full words)
  - paper: doi:10.1016/j.ejc.2017.07.021
    title: Mikhail Rubinchik and Arseny M. Shur, EERTREE, an efficient data structure for processing palindromes in strings, European Journal of Combinatorics 68 (2018), 249-265
    locator: Section 2 (the lemma that each new symbol adds at most one new palindrome, and the size of the eertree)
---

The palindrome count bound states that a string of length $n$ has at most $n + 1$ distinct [palindromic](/palindrome/) substrings, the empty string included, so at most $n$ nonempty ones. The reason is that each new symbol adds at most one palindrome that has not occurred before: the longest palindromic suffix of the new prefix. The bound is reached, for example by $a^n$, and the strings that reach it are the [rich strings](/rich-string/). It is why the [palindromic tree](/palindromic-tree/) has a linear number of nodes.

## Statement

Let $\Sigma$ be any [alphabet](/alphabet/) and $s = s[0..n-1] \in \Sigma^n$, with 0-based indices. Let $\mathrm{Pal}(s)$ be the set of distinct strings $u$ such that $u$ is a palindrome and $u = s[i..j]$ for some $i, j$, where $\varepsilon$ counts as a substring. Both even and odd palindromes are counted, and two occurrences of the same string count once.

**Theorem.** For every $n \ge 0$ and every $s \in \Sigma^n$,
$$ |\mathrm{Pal}(s)| \le n + 1. $$

**Key lemma.** For $0 \le i \le n-1$, let $P_i$ be the set of palindromes that occur in $s[0..i]$ as a suffix and do not occur in $s[0..i-1]$. Then $|P_i| \le 1$, and if $P_i$ is not empty, its element is the longest palindromic suffix of $s[0..i]$.

The bound is about distinct strings. The number of palindromic *occurrences* can be as large as $n(n+1)/2$, see [counting palindromic substrings](/count-palindromic-substrings/).

## In plain words

Read a string one letter at a time and keep a list of the palindromes seen so far. When a new letter arrives, the only palindromes that can be new are the ones that end at this letter. Take the longest of them. Each shorter one sits at the end of the longest one, and because the longest one reads the same both ways, the shorter one also sits at its start, so it was already seen earlier. So each letter adds at most one new palindrome to the list. A string with a given number of letters therefore has at most that many different nonempty palindromes, plus the empty one.

## Proof

*Proof of the lemma.* Let $v$ be the longest palindromic suffix of $s[0..i]$; it exists and is nonempty, because $s[i]$ is a palindromic suffix. Let $u$ be a palindromic suffix of $s[0..i]$ with $|u| < |v|$. Then $u$ is a suffix of $v$, since both are suffixes of $s[0..i]$. A palindromic suffix of a palindrome is also its prefix (the [palindrome](/palindrome/) page, fact 3: $u^R$ is a prefix of $v^R = v$, and $u^R = u$). The occurrence of $v$ is $s[i-|v|+1..i]$, so $u$ occurs as $s[i-|v|+1..i-|v|+|u|]$. Its last index is $i - (|v| - |u|) \le i - 1$, so $u$ occurs in $s[0..i-1]$, and $u \notin P_i$. Each element of $P_i$ ends at index $i$, so it is a palindromic suffix of $s[0..i]$. So $P_i \subseteq \{v\}$. $\square$

*Proof of the theorem.* Each nonempty $u \in \mathrm{Pal}(s)$ has a first occurrence, the one with the smallest end index $i$. At that index, $u$ is a palindromic suffix of $s[0..i]$ that does not occur in $s[0..i-1]$, so $u \in P_i$. This gives a map from the nonempty elements of $\mathrm{Pal}(s)$ to the indices $0, \ldots, n-1$. The map is injective, because by the lemma each $P_i$ has at most one element. So there are at most $n$ nonempty palindromes, and with $\varepsilon$ at most $n + 1$. $\blacksquare$

The proof also shows when equality holds: $|\mathrm{Pal}(s)| = n + 1$ if and only if $P_i \ne \emptyset$ for each $i$, that is, if and only if the longest palindromic suffix of each prefix occurs only once in that prefix. This is Proposition 3 of Droubay, Justin and Pirillo, and it is the definition of a [rich string](/rich-string/) used in the algorithms.

### A worked example

For $s = $ `aababbaa` ($n = 8$) the table gives, at each index, the longest palindromic suffix $v$ of $s[0..i]$ and whether it is new.

| $i$ | $s[i]$ | longest palindromic suffix | new? |
| --- | --- | --- | --- |
| 0 | a | a | yes |
| 1 | a | aa | yes |
| 2 | b | b | yes |
| 3 | a | aba | yes |
| 4 | b | bab | yes |
| 5 | b | bb | yes |
| 6 | a | abba | yes |
| 7 | a | aa | no, it occurs at index 0 |

So $\mathrm{Pal}(s)$ has 7 nonempty elements and 8 in all, one less than the bound $n + 1 = 9$. For $s = $ `abaab` the new palindromes are `a`, `b`, `aba`, `aa`, `baab`, one at each index, so `abaab` reaches the bound.

## Consequences

- **The palindromic tree has linear size.** The [palindromic tree (eertree)](/palindromic-tree/) has one node for each distinct nonempty palindrome plus two roots, so at most $n + 2$ nodes. Its online construction adds at most one node for each symbol, which is the lemma in the form of an algorithm.
- **Distinct palindromes can be counted in linear time.** The count is the number of nodes of the eertree minus 2, so it takes $O(n)$ time for a constant-size alphabet. The count of occurrences, a different number, is on the page [counting palindromic substrings](/count-palindromic-substrings/).
- **Defect and rich strings.** The *palindromic defect* $D(s) = |s| + 1 - |\mathrm{Pal}(s)|$ of Brlek, Hamel, Nivat and Reutenauer is a non-negative integer by the theorem. Strings with defect 0 are the [rich strings](/rich-string/). By the lemma, $D(s)$ is the number of indices $i$ with $P_i = \emptyset$ (Glen, Justin, Widmer and Zamboni, Proposition 4.1). For `aababbaa` the defect is 1.
- **Factors of rich strings are rich.** If $s$ reaches the bound, so does each substring and the reversal of $s$ (Glen et al., Corollary 2.5).
- **Series of palindromic suffixes.** The lemma uses only the fact that the shorter palindromic suffixes are borders of the longest one. The same fact leads to the grouping of all palindromic suffixes into $O(\log n)$ arithmetic progressions, see [series links](/series-links/).

## Tightness

**The bound is reached for each $n$ and each alphabet.** The string $a^n$ has the palindromes $\varepsilon, a, a^2, \ldots, a^n$, which is $n + 1$. Over two letters, every string of length at most 7 reaches the bound, and `aababbaa` is a string of length 8 that does not; this follows from an exhaustive check of all $2^8$ strings of length 8 and of all shorter ones. Infinite families of rich strings include the prefixes of the [Fibonacci word](/fibonacci-word/) and of every [Sturmian word](/sturmian-word/), by the result of Droubay, Justin and Pirillo that episturmian words are rich.

**There is no non-trivial lower bound for large alphabets.** The string $(abc)^{k}$ has only 3 distinct nonempty palindromes, `a`, `b` and `c`, for every length. Over two letters, a long string has at least 8 nonempty palindromes: the minimum over all binary strings of length $n$ is $n$ for $n \le 7$, then 7 for $n = 8$, and 8 for each $n$ from 9 to 16. The periodic string `aababb` `aababb` $\cdots$ has exactly the 8 palindromes `a`, `b`, `aa`, `bb`, `aba`, `bab`, `abba`, `baab` at each length from 9 to 120.

## History

Droubay, Justin and Pirillo observed the bound in their 2001 paper on episturmian words, as Proposition 2, together with the characterization of equality by unioccurrent longest palindromic suffixes (Proposition 3), and they proved that episturmian words, which include the Sturmian words, reach it. Brlek, Hamel, Nivat and Reutenauer (2004) introduced the defect and called the words of defect 0 full. Glen, Justin, Widmer and Zamboni (2009) named them rich and studied them as a class. Rubinchik and Shur used the same one-new-palindrome-per-symbol lemma as the base of the eertree, published in 2015 and in journal form in 2018.

## References
