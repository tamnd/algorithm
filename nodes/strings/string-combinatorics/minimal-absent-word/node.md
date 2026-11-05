---
tag: NJR64B
kind: definition
slug: minimal-absent-word
name: Minimal absent word
aliases:
- minimal forbidden word
area: strings/string-combinatorics
level: advanced
summary: A word that does not occur in s while all its proper factors do.
prereqs: [alphabet, suffix-automaton]
see_also: [minimal-absent-words, minimal-absent-words-algorithm, shortest-unique-substring, subword-complexity, de-bruijn-sequence, maximal-repeats, square-free-word, avoidability]
sources:
  - paper: doi:10.1016/s0020-0190(98)00104-5
    title: Maxime Crochemore, Filippo Mignosi and Antonio Restivo, Automata and forbidden words, Information Processing Letters 67(3), 1998, 111-117
    locator: the definition of minimal forbidden words of a word, the factor automaton built back from them, their computation in linear time, and the O(σn) bound on their number
  - paper: doi:10.1016/s0304-3975(00)00436-9
    title: Filippo Mignosi, Antonio Restivo and Marinella Sciortino, Words and forbidden factors, Theoretical Computer Science 273(1-2), 2002, 99-117
    locator: the correspondence between factorial languages and their sets of minimal forbidden words, and the reconstruction of a word from its minimal forbidden words
  - paper: doi:10.1006/aama.2000.0682
    title: Marie-Pierre Béal, Filippo Mignosi, Antonio Restivo and Marinella Sciortino, Forbidden words in symbolic dynamics, Advances in Applied Mathematics 25(2), 2000, 163-193
    locator: minimal forbidden words of factorial languages and of shifts of finite type
  - paper: doi:10.1109/5.892711
    title: Maxime Crochemore, Filippo Mignosi, Antonio Restivo and Sergio Salemi, Data compression using antidictionaries, Proceedings of the IEEE 88(11), 2000, 1756-1768
    locator: the antidictionary of a text, made of minimal forbidden words, and its use for compression
  - paper: doi:10.1016/j.tcs.2012.04.031
    title: Supaporn Chairungsee and Maxime Crochemore, Using minimal absent words to build phylogeny, Theoretical Computer Science 450, 2012, 109-116
    locator: a distance between sequences defined from their minimal absent words
---

A minimal absent word of a string $s$ is a word that does not occur in $s$, while every proper factor of it does. For example, `aaba` is a minimal absent word of `abaab`: it does not occur, but `aab` and `aba` both do. The minimal absent words of $s$ describe $s$ completely: a word is a factor of $s$ exactly when it contains none of them. There are $O(\sigma n)$ of them for a string of length $n$ over $\sigma$ letters, and they can be listed in linear time, see [minimal absent words](/minimal-absent-words/).

## Definition

Let $\Sigma$ be a finite [alphabet](/alphabet/) of size $\sigma$, fixed in advance; only equality of letters is used. The definition depends on $\Sigma$, not only on the letters that occur in $s$. Indices are 0-based. Let $s \in \Sigma^n$, and let $\mathrm{Fact}(s)$ be the set of factors of $s$, including $\varepsilon$ and $s$.

**Minimal absent word.** A word $w \in \Sigma^+$ is a minimal absent word (MAW) of $s$ if $w \notin \mathrm{Fact}(s)$ and every proper factor of $w$ is in $\mathrm{Fact}(s)$. The set of them is $\mathrm{MAW}(s)$, also called the antidictionary of $s$, or its set of minimal forbidden words.

**Equivalent form.** A letter $a$ is a MAW of $s$ if and only if $a$ does not occur in $s$. A word of length at least 2, written $w = a x b$ with letters $a, b$ and $x \in \Sigma^*$, is a MAW of $s$ if and only if
$$ a x \in \mathrm{Fact}(s), \quad x b \in \mathrm{Fact}(s), \quad a x b \notin \mathrm{Fact}(s). $$
*Proof.* The only proper factor of a letter is $\varepsilon$, which is always a factor. For $w = axb$, every proper factor of $w$ is a factor of $ax$ or of $xb$, which are themselves proper factors, and $\mathrm{Fact}(s)$ is closed under taking factors. $\square$

### Basic facts

1. **Factors are characterized.** A word $y$ is a factor of $s$ if and only if no MAW of $s$ is a factor of $y$. *Proof.* If $y \in \mathrm{Fact}(s)$, all its factors are in $\mathrm{Fact}(s)$, so none is absent. If $y \notin \mathrm{Fact}(s)$, take a shortest factor $w$ of $y$ that is not in $\mathrm{Fact}(s)$; it is nonempty, and all its proper factors are shorter, hence in $\mathrm{Fact}(s)$, so $w$ is a MAW. $\square$
2. **The word is determined.** $s$ is the longest word over $\Sigma$ that contains no MAW of $s$, by fact 1, since $s$ is the longest element of $\mathrm{Fact}(s)$. So $\mathrm{MAW}(s)$ and $\Sigma$ determine $s$. Crochemore, Mignosi and Restivo rebuild the factor automaton of $s$ from $\mathrm{MAW}(s)$ in time linear in their total length.
3. **Length.** Each MAW has length at most $n + 1$, since for $w = axb$ the factor $ax$ has length at most $n$. The bound is reached by $a^{n+1}$ for $s = a^n$.
4. **Number.** The number of letters that are MAWs is $\sigma$ minus the number of distinct letters of $s$. The total number of MAWs is $O(\sigma n)$ (Crochemore, Mignosi and Restivo, 1998). For each $n$ from 3 to 16, the largest number of MAWs of a binary word of length $n$ is $n$. For ternary words of the lengths 1 to 10 the largest numbers are 3, 4, 7, 8, 9, 11, 12, 15, 16, 19.
5. **Reversal.** $w$ is a MAW of $s$ if and only if its reversal is a MAW of the reversal of $s$, since reversal maps factors to factors.
6. **Shortest absent words.** If $k$ is the length of a shortest MAW, then all $\sigma^{k-1}$ words of length $k - 1$ occur in $s$, since a missing one would contain a shorter MAW. There are at most $n - k + 2$ distinct factors of length $k - 1$, so $\sigma^{k-1} \le n - k + 2$, and $k \le \log_\sigma (n + 1) + 1$.

## Examples and non-examples

Over $\Sigma = \{a, b\}$ unless stated:

| $s$ | $\Sigma$ | $\mathrm{MAW}(s)$ |
|---|---|---|
| `abaab` | $\{a, b\}$ | `bb`, `aaa`, `bab`, `aaba` |
| `abaab` | $\{a, b, c\}$ | `c`, `bb`, `aaa`, `bab`, `aaba` |
| `aaaa` | $\{a, b\}$ | `b`, `aaaaa` |
| `abbab` | $\{a, b\}$ | `aa`, `aba`, `bbb`, `babb` |
| `abcab` | $\{a, b, c\}$ | `aa`, `ac`, `ba`, `bb`, `cb`, `cc`, `cabc` |
| `0001011100` | $\{0, 1\}$ | the 9 words of length 4 that do not occur |
| $\varepsilon$ | $\{a, b\}$ | `a`, `b` |

- In `abaab`, the word `aaba` is a MAW: `aab` occurs at index 2 and `aba` at index 0, but `aaba` does not occur. The word `abb` is absent but not minimal, since its factor `bb` is absent.
- In `mississippi` over $\{i, m, p, s\}$ there are 18 MAWs, such as `ii`, `ipi`, `sss` and the longest ones `missip` and `sissis`.
- `0001011100` contains all 8 binary words of length 3, so each absent word of length 4 has both proper factors of length 3 present and is a MAW; 7 of the 16 words of length 4 occur, so 9 are MAWs.
- **Non-examples.** A factor of $s$ is never a MAW. An absent word with an absent proper factor, such as `bbb` for `abaab`, is not minimal.

## Related definitions

- **[Minimal absent words](/minimal-absent-words/).** The problem of listing $\mathrm{MAW}(s)$, solved in $O(n + \sigma + |\mathrm{MAW}(s)|)$ time from the [suffix automaton](/suffix-automaton/) or the suffix array; see the [algorithm](/minimal-absent-words-algorithm/).
- **Absent and forbidden words of a language.** For any factorial language $L$, closed under factors, the minimal words not in $L$ define $L$ in the same way as in fact 1. For the language of an infinite word or a shift space, they are the minimal forbidden words of symbolic dynamics; a shift is of finite type exactly when this set is finite.
- **[Shortest unique substring](/shortest-unique-substring/).** A dual notion: a shortest factor that occurs exactly once, instead of zero times.
- **[Subword complexity](/subword-complexity/).** The number of distinct factors of each length; a length $k$ with fewer than $\sigma^k$ factors has absent words of length at most $k$.
- **Antidictionary.** In compression with antidictionaries, the encoder and decoder share $\mathrm{MAW}(s)$; whenever the context determines the next letter, because every other letter would complete a MAW, that letter is not transmitted.
- **[De Bruijn sequence](/de-bruijn-sequence/).** A string that contains every word of length $k$; its MAWs all have length at least $k + 1$.

## References
