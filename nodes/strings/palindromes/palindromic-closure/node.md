---
tag: VK5Z43
kind: concept
slug: palindromic-closure
name: Palindromic closure
aliases:
- palindromic closure of a word
area: strings/palindromes
level: research
summary: The shortest palindrome having a given string as a prefix, built by appending its reversed prefix.
prereqs: [palindrome, shortest-palindrome]
see_also: [sturmian-word, fibonacci-word, rich-string, manacher, prefix-function, palindrome-edit-distance, string-morphism]
sources:
  - paper: doi:10.1016/S0304-3975(96)00310-6
    title: Aldo de Luca, Sturmian words, structure, combinatorics, and their arithmetics, Theoretical Computer Science 183 (1997), 45-82
    locator: the right palindromic closure and the iterated palindromic closure, which generates the standard Sturmian words from a directive sequence
  - paper: doi:10.1016/S0304-3975(99)00320-5
    title: Xavier Droubay, Jacques Justin and Giuseppe Pirillo, Episturmian words and some constructions of de Luca and Rauzy, Theoretical Computer Science 255 (2001), 539-553
    locator: the definition of standard episturmian words over any alphabet by iterated palindromic closure
  - paper: doi:10.1016/j.ejc.2008.04.006
    title: Amy Glen, Jacques Justin, Steve Widmer and Luca Q. Zamboni, Palindromic richness, European Journal of Combinatorics 30 (2009), 510-531
    locator: Section 2 (the notation u(+) = u v^(-1) ũ with v the longest palindromic suffix, and Proposition 2.6, palindromic closure preserves richness)
---

The (right) palindromic closure $w^{(+)}$ of a string $w$ is the shortest [palindrome](/palindrome/) that has $w$ as a prefix. If $w = u\,v$ where $v$ is the longest palindromic suffix of $w$, then $w^{(+)} = u\,v\,u^R$: the closure appends the reversal of the part before $v$. It is the [shortest palindrome](/shortest-palindrome/) problem with the new symbols at the end instead of the front. Iterating it, de Luca built the standard Sturmian words, and Droubay, Justin and Pirillo the standard episturmian words, such as the [Fibonacci word](/fibonacci-word/).

## In plain words

Take a word and add letters at its end until it reads the same from both ends, using as few new letters as you can. Find the longest end part of the word that is already a palindrome. The letters in front of it have no partner yet. Copy them in reverse order and write the copy at the end. Now repeat a game: add one letter, then close the word again into a palindrome, add the next letter, close again, and so on. With the letters a, b, a, b, ... this game grows the start of the Fibonacci word, a famous word made of two letters.

## The idea

**Conventions.** Strings are indexed from 0 and $w[i..j]$ includes both ends. Symbols are only compared for equality. The closure may be an odd or an even palindrome; its parity is whatever the shortest one has.

**The closure formula.** Let $v$ be the longest palindromic suffix of $w$ and $w = u\,v$. Then $w^{(+)} = u\,v\,u^R$, of length $2|w| - |v|$, and no shorter palindrome starts with $w$. The proof is the one on the [shortest palindrome](/shortest-palindrome/) page, applied to $w^R$: a palindrome $w\,y$ with $|y| \le |w|$ forces the last $|w| - |y|$ symbols of $w$ to form a palindrome, so $|y| \ge |w| - |v|$. The left closure ${}^{(+)}w$ is the same construction at the front. Glen et al. write $w^{(+)} = w\,v^{-1}\tilde{w}$, with $\tilde{w}$ the reversal of $w$.

**Computing it.** The only work is the length of the longest palindromic suffix of $w$, which [Manacher's algorithm](/manacher/) or the [prefix function](/prefix-function/) of $w^R\,\#\,w$ gives in $O(|w|)$ time with equality tests.

**Iterated palindromic closure.** For a *directive* word $\Delta = x_1 x_2 x_3 \cdots$, define
$$ \psi(\varepsilon) = \varepsilon, \qquad \psi(x_1 \cdots x_k) = \big(\psi(x_1 \cdots x_{k-1})\, x_k\big)^{(+)}. $$
Each $\psi(x_1 \cdots x_k)$ is a prefix of the next one, so an infinite directive word defines an infinite word $\psi(\Delta)$. De Luca (1997) showed that over two letters, when both letters occur infinitely often in $\Delta$, $\psi(\Delta)$ is a standard Sturmian word, and every standard Sturmian word arises in this way. Droubay, Justin and Pirillo (2001) took the same construction over any alphabet as the definition of the standard episturmian words.

**The palindromic prefixes.** The palindromic prefixes of $\psi(x_1 \cdots x_k)$ are exactly $\psi(\varepsilon), \psi(x_1), \ldots, \psi(x_1 \cdots x_k)$. *Proof.* By induction on $k$. Let $q = \psi(x_1 \cdots x_{k-1})$. A palindromic prefix $p$ of $\psi(x_1 \cdots x_k)$ with $|q| < |p|$ starts with $q\,x_k$, so it is a palindrome that has $q\,x_k$ as a prefix, and the closure is the shortest such one, so $p = (q\,x_k)^{(+)}$. The prefixes of length at most $|q|$ are prefixes of $q$, covered by the induction hypothesis. $\square$ So the directive word can be read back from the palindromic prefixes: $x_k$ is the symbol that follows $\psi(x_1 \cdots x_{k-1})$.

**Richness.** The closure of a [rich](/rich-string/) word is rich (Glen et al., Proposition 2.6): if $w = f\,v$ with $v$ unioccurrent, each appended symbol of $f^R$ makes a new, longer palindromic suffix around $v$. Every iterated closure $\psi(\Delta)$ is rich too, because it is a prefix of a standard episturmian word, and Droubay, Justin and Pirillo show that episturmian words are rich.

## Examples

**Single closures.**

| $w$ | longest palindromic suffix $v$ | $u$ | $w^{(+)} = u\,v\,u^R$ |
| --- | --- | --- | --- |
| `ab` | `b` | `a` | `aba` |
| `aab` | `b` | `aa` | `aabaa` |
| `abc` | `c` | `ab` | `abcba` |
| `abca` | `a` | `abc` | `abcacba` |
| `abaab` | `baab` | `a` | `abaaba` |
| `aba` | `aba` | $\varepsilon$ | `aba` |

**Iterated closures.** With $\Delta = abab\cdots$, the words $\psi(a), \psi(ab), \psi(aba), \ldots$ are `a`, `aba`, `abaaba`, `abaababaaba`, `abaababaabaababaaba`, of lengths 1, 3, 6, 11, 19, then 32 and 53. These are the palindromic prefixes of the Fibonacci word `abaababaabaab`$\cdots$, and their lengths are the Fibonacci numbers $3, 5, 8, 13, 21, 34, 55$ minus 2. With $\Delta = abcabc\cdots$ over three letters, the words are `a`, `aba`, `abacaba`, `abacabaabacaba`, the start of the Tribonacci word, an episturmian word. With $\Delta = aab$, the words are `a`, `aa` and `aabaa`; with $\Delta = abb$, they are `a`, `aba` and `ababa`.

## Where it is used

- **Sturmian and episturmian words.** The iterated closure is a standard way to build and study [Sturmian words](/sturmian-word/) and their generalizations over larger alphabets, and the directive word is a code for them.
- **Rich words.** The closure keeps richness, so it gives long [rich words](/rich-string/) from short ones and is a tool in the proofs of Glen et al.
- **Algorithms on palindromes.** Computing $w^{(+)}$ is the shortest palindrome problem at the end of a string, a standard use of the prefix function and of Manacher's algorithm.
- **Generating test strings.** Iterated closures give long strings with many nested palindromic prefixes, which are useful worst cases for palindrome algorithms.

## References
