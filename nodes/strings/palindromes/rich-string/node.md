---
tag: 2VB2RT
kind: concept
slug: rich-string
name: Rich string (palindromic richness)
aliases:
- palindromic rich word
- palindromically rich string
area: strings/palindromes
level: research
summary: A string of length n containing exactly n+1 distinct palindromic substrings, including the empty one.
prereqs: [palindrome, palindrome-count-bound]
see_also: [palindromic-tree, count-palindromic-substrings, palindromic-closure, sturmian-word, fibonacci-word, series-links]
sources:
  - paper: doi:10.1016/S0304-3975(99)00320-5
    title: Xavier Droubay, Jacques Justin and Giuseppe Pirillo, Episturmian words and some constructions of de Luca and Rauzy, Theoretical Computer Science 255 (2001), 539-553
    locator: Proposition 2 (at most |w| + 1 distinct palindromic factors), Proposition 3 (equality if and only if each prefix has a unioccurrent palindromic suffix), and the result that episturmian words reach the bound
  - paper: doi:10.1016/j.ejc.2008.04.006
    title: Amy Glen, Jacques Justin, Steve Widmer and Luca Q. Zamboni, Palindromic richness, European Journal of Combinatorics 30 (2009), 510-531
    locator: Definition 2.2, Proposition 2.4, Corollary 2.5 (factors and reversal of rich words), Proposition 2.6 (closure preserves richness), Theorem 2.14 (complete returns), Theorem 3.1 (periodic rich words), Section 4.1 (the defect)
  - paper: doi:10.1142/S012905410400242X
    title: Srecko Brlek, Sylvie Hamel, Maurice Nivat and Christophe Reutenauer, On the palindromic complexity of infinite words, International Journal of Foundations of Computer Science 15(2) (2004), 293-306
    locator: the definition of the palindromic defect and of full words (defect 0)
  - paper: doi:10.1016/j.ipl.2010.07.018
    title: Richard Groult, Élise Prieur and Gwénaël Richomme, Counting distinct palindromes in a word in linear time, Information Processing Letters 110(20) (2010), 908-912
    locator: the linear-time count of distinct palindromes and its use as a linear-time test of richness
---

A string $w$ of length $n$ is *rich*, or *full*, if it has $n + 1$ distinct palindromic substrings, counting the empty string. This is the most possible, by the [palindrome count bound](/palindrome-count-bound/) of Droubay, Justin and Pirillo: each new symbol adds at most one new palindrome, and in a rich string every symbol adds one. Glen, Justin, Widmer and Zamboni studied these words as a class in 2009, and Brlek, Hamel, Nivat and Reutenauer measure the distance from richness by the *defect* $D(w) = n + 1 - |\mathrm{Pal}(w)|$. Sturmian and episturmian words, such as the [Fibonacci word](/fibonacci-word/), are rich.

## In plain words

Read a word one letter at a time and look at the longest piece that ends at the new letter and reads the same from both ends. Each time, at most one palindrome can appear that you have not seen before, and if one appears, it is that longest piece. A word is rich when this happens at every letter: every letter brings a palindrome that is new. So a rich word has as many different palindromes as it has letters. All short words over two letters are rich, but from length 8 on some are not, such as `aababbaa`, where the last letter brings nothing new.

## The idea

**Conventions.** Indices are 0-based and $w[i..j]$ includes both ends. Symbols are only compared for equality. Both odd and even palindromes count. $\mathrm{Pal}(w)$ is the set of distinct palindromic substrings of $w$, including the empty string $\varepsilon$; [counting palindromic substrings](/count-palindromic-substrings/) excludes $\varepsilon$, so there the condition reads $N_{\mathrm{dist}}(w) = n$.

**Definition.** $w$ is rich if $|\mathrm{Pal}(w)| = |w| + 1$ (Glen et al., Definition 2.2). The *defect* is $D(w) = |w| + 1 - |\mathrm{Pal}(w)| \ge 0$, so the rich words are the words with defect 0. An infinite word is rich if all its finite factors are rich.

**Characterizations.** The following are equivalent for a finite word $w$:

1. $w$ is rich.
2. Each prefix $w[0..i]$ has a *unioccurrent* longest palindromic suffix, one that occurs only one time in $w[0..i]$ (Droubay, Justin and Pirillo, Proposition 3; Glen et al., Proposition 2.4). The same holds with suffixes and prefixes exchanged.
3. Each *complete return* to a palindrome is a palindrome: if a factor $u$ of $w$ begins and ends with a palindrome $p$ and has no other occurrence of $p$, then $u$ is a palindrome (Glen et al., Theorem 2.14).

Condition 2 is the step-by-step view: the longest palindromic suffix of $w[0..i]$ is the only candidate for a new palindrome at step $i$, and it is new exactly when it is unioccurrent.

**Closure properties.** If $w$ is rich, then every factor of $w$ is rich and its reversal is rich (Glen et al., Corollary 2.5), and its [palindromic closure](/palindromic-closure/) is rich (Proposition 2.6). The defect never decreases from a factor to the whole word, so $D(w)$ is the maximum over its prefixes.

**Periodic words.** For a finite word $w$, the infinite word $w^\omega = w\,w\,w \cdots$ is rich if and only if $w^2$ is rich, and also if and only if $w$ is a product of two palindromes and all its conjugates are rich (Glen et al., Theorem 3.1).

**Testing.** Richness is tested in $O(n)$ time for a constant alphabet: build the [palindromic tree](/palindromic-tree/) and check that every step adds a node, or count the distinct palindromes with the method of Groult, Prieur and Richomme and compare with $n$.

## Examples

| $w$ | $n$ | distinct nonempty palindromes | rich |
| --- | --- | --- | --- |
| `abaab` | 5 | a, b, aa, aba, baab | yes |
| `banana` | 6 | a, b, n, ana, nan, anana | yes |
| `abacaba` | 7 | a, b, c, aba, aca, bacab, abacaba | yes |
| `eertree` | 7 | e, r, t, ee, rtr, ertre, eertree | yes |
| `abaababaaba` | 11 | a, b, aa, aba, bab, baab, ababa, abaaba, aababaa, baababaab, abaababaaba | yes |
| `aababbaa` | 8 | a, b, aa, bb, aba, bab, abba | no, defect 1 |
| `abca` | 4 | a, b, c | no, defect 1 |
| `abcab` | 5 | a, b, c | no, defect 2 |

- **Binary words.** All $2^n$ binary words of length $n \le 7$ are rich. Of length 8 there are $252$ rich words, and the four that are not are `aababbaa`, `aabbabaa`, `bbaababb` and `bbabaabb`. For lengths 9 to 12 the numbers of rich binary words are 488, 932, 1756 and 3246, by exhaustive count.
- **A failure of condition 2.** In `aababbaa`, the longest palindromic suffix of the whole word is `aa`, which already occurs at the start, so the last symbol adds nothing new.
- **A failure of condition 3.** In the same word, the factor from the first `aa` to the last one is the whole word, with no other `aa` inside, and it is not a palindrome.
- **Periodic words.** `aabbaabab` $\cdot$ `aabbaabab` and `abcba` $\cdot$ `abcba` are rich, so $(\texttt{aabbaabab})^\omega$ and $(\texttt{abcba})^\omega$ are rich, as in Example 3.2 of Glen et al.
- **Sturmian words.** The prefix `abaababaaba` of the Fibonacci word is rich; Droubay, Justin and Pirillo show that every factor of an episturmian word is rich.

## Where it is used

- **Combinatorics on words.** Rich words are a meeting point of the studies of palindromes, Sturmian and episturmian words, and complete returns. The defect classifies infinite words by how far they are from rich, and the words with bounded defect are the *almost rich* words of Glen et al.
- **Testing structures for palindromes.** Rich words are the inputs where the palindromic tree has the most nodes, $n + 2$, so they are worst cases for its size and good test inputs.
- **Sturmian words.** Richness gives a common frame for the palindromic properties of [Sturmian words](/sturmian-word/) and of episturmian words, which are all rich.
- **Algorithms.** A linear-time count of distinct palindromes gives a linear-time test of richness, as Groult, Prieur and Richomme note.

## References
