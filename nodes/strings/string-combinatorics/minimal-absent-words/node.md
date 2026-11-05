---
tag: Z3P95N
kind: problem
slug: minimal-absent-words
name: Minimal absent words
aliases:
- minimal forbidden words computation
area: strings/string-combinatorics
level: advanced
summary: Compute all minimal absent words of a string.
model: word-ram
complexity:
  vars: {n: the length of the string, σ: the alphabet size, z: the number of minimal absent words}
  time: {worst: O(n + σ + z)}
  space: {extra: O(n)}
prereqs: [minimal-absent-word, suffix-automaton]
see_also: [minimal-absent-words-algorithm, suffix-link, suffix-array, lcp-array, shortest-unique-substring, subword-complexity, de-bruijn-sequence, maximal-repeats]
sources:
  - paper: "Maxime Crochemore, Filippo Mignosi and Antonio Restivo, Automata and forbidden words, Information Processing Letters 67(3), 1998, 111-117"
    locator: the computation of the minimal forbidden words of a word from its factor automaton in time linear in the size of the input and output, and the bound on their number
  - paper: "Filippo Mignosi, Antonio Restivo and Marinella Sciortino, Words and forbidden factors, Theoretical Computer Science 273(1-2), 2002, 99-117"
    locator: the correspondence between factorial languages and their sets of minimal forbidden words
  - paper: "Maxime Crochemore, Filippo Mignosi, Antonio Restivo and Sergio Salemi, Data compression using antidictionaries, Proceedings of the IEEE 88(11), 2000, 1756-1768"
    locator: the antidictionary of a text and its use for compression
  - paper: "Carl Barton, Alice Heliou, Laurent Mouchard and Solon P. Pissis, Linear-time computation of minimal absent words using suffix array, BMC Bioinformatics 15, 2014, article 388"
    locator: the computation of all minimal absent words from the suffix array and LCP array in linear time for a fixed alphabet
---

The minimal absent words problem asks for all [minimal absent words](/minimal-absent-word/) of a string $y$ over an alphabet $\Sigma$: the words that do not occur in $y$ while every proper factor of them does. Such a word is a letter missing from $y$ or has the form $a\,u\,b$ with letters $a, b$, where $au$ and $ub$ occur in $y$ but $aub$ does not. There are $O(\sigma n)$ of them for $|y| = n$ and $|\Sigma| = \sigma$, they determine the set of factors of $y$ exactly, and they can be listed in time linear in the input plus the output with a [suffix automaton](/suffix-automaton/) or a [suffix array](/suffix-array/). They are used for compression with antidictionaries and for comparing genomes.

## In plain words

Take a text and ask which short words never appear in it. Most absent words are absent for a boring reason: they contain a shorter absent word. If `bb` never occurs, then neither does `abba` or `bbbb`. The interesting absent words are the ones that are absent only as a whole: every piece obtained by dropping a letter at the start or the end does occur. These minimal absent words are few, at most a small multiple of the text length, and together they say exactly which words occur in the text: a word occurs if and only if it contains none of them.

## Definition

Let $\Sigma$ be a finite ordered alphabet with $\sigma$ letters; only equality of letters matters for the definition, and the order fixes the output order. Strings are indexed from 0. Let $\mathrm{Fact}(y)$ be the set of factors of $y$, including the empty word.

**Input.** A string $y = y[0..n-1]$ over $\Sigma$, and the alphabet $\Sigma$.

**Output.** The set $\mathrm{MAW}(y)$ of words $w \in \Sigma^+$ with $w \notin \mathrm{Fact}(y)$ and every proper factor of $w$ in $\mathrm{Fact}(y)$. Each word is reported in constant space, as a letter $a$ alone or as a triple $(i, \ell, b)$ standing for $y[i..i+\ell-1]\,b$.

**Two maximal proper factors suffice.** Since $\mathrm{Fact}(y)$ is closed under taking factors, $w = a\,u\,b$ with letters $a, b$ is in $\mathrm{MAW}(y)$ if and only if $aub \notin \mathrm{Fact}(y)$, $au \in \mathrm{Fact}(y)$ and $ub \in \mathrm{Fact}(y)$; every other proper factor lies inside $au$ or $ub$. A one-letter word is in $\mathrm{MAW}(y)$ if and only if it does not occur in $y$. So every minimal absent word has length at most $n + 1$.

**The factors are the words avoiding the minimal absent words.** For every word $w$, $w \in \mathrm{Fact}(y)$ if and only if no factor of $w$ is in $\mathrm{MAW}(y)$. *Proof.* If $w$ occurs in $y$, so do all its factors, and none of them is absent. If $w$ does not occur, let $v$ be a shortest factor of $w$ that does not occur in $y$. Its proper factors are shorter factors of $w$, so they occur, and $v \in \mathrm{MAW}(y)$. $\square$ The same argument works for every language closed under factors (Mignosi, Restivo and Sciortino). In particular $y$ is the longest word with no factor in $\mathrm{MAW}(y)$, so $y$ can be rebuilt from its minimal absent words.

**Number.** For $n \ge 1$, $|\mathrm{MAW}(y)| \le 2\sigma n$. *Proof.* By the correspondence proved on the [algorithm page](/minimal-absent-words-algorithm/), the minimal absent words of length at least 2 correspond one to one to some pairs $(p, b)$ of a non-initial state $p$ of the suffix automaton of $y$ and a letter $b$. The automaton has at most $2n$ states, so at most $2n - 1$ non-initial ones, and there are at most $\sigma$ minimal absent words of length 1. $\square$

## Variants

- **Bounded length.** Report only the minimal absent words of length at most $\ell$, as used in genomics where long ones are numerous and uninformative.
- **Several strings.** Minimal absent words of a set of strings, or of a factorial language given by an automaton.
- **Circular strings.** Minimal absent words of the circular word, where factors may wrap around.
- **Relative absent words.** Words absent from a string $y$ whose proper factors occur in a reference string $x$, used to compare two sequences.
- **Sliding window.** Maintain the minimal absent words of every window of fixed width of a long text.
- **Shortest absent word.** Only the shortest word that does not occur, which is the shortest minimal absent word; compare the [shortest unique substring](/shortest-unique-substring/), which is about words that occur exactly once.

## Examples

| $y$ | $\Sigma$ | minimal absent words |
| --- | --- | --- |
| `abaab` | $\{a, b\}$ | `aaa`, `aaba`, `bab`, `bb` |
| `abbab` | $\{a, b\}$ | `aa`, `aba`, `babb`, `bbb` |
| `banana` | $\{a, b, n\}$ | `aa`, `ab`, `bb`, `bn`, `nanan`, `nb`, `nn` |
| `aaaa` | $\{a, b\}$ | `aaaaa`, `b` |
| empty | $\{a, b\}$ | `a`, `b` |

- For `abaab`, the word `aaba` is minimal absent: `aab` occurs at position 2 and `aba` at position 0, but `aaba` does not occur. The word `abb` is absent but not minimal, since its factor `bb` is absent.
- For `banana`, `nanan` is minimal absent because both `nana` and `anan` occur.
- **Rebuilding the factors.** A word over $\{a, b\}$ occurs in `abaab` if and only if it contains none of `aaa`, `aaba`, `bab`, `bb`; the longest such word is `abaab` itself.
- **How many.** By exhaustive search, the largest number of minimal absent words of a binary string of length $n$ is $n$ for $3 \le n \le 12$, and over three letters it is $3, 4, 7, 8, 9, 11, 12$ for $n = 1, \ldots, 7$.

## Known algorithms

- **Brute force.** Test every word of length up to $n + 1$, or every triple $(a, u, b)$ with $u \in \mathrm{Fact}(y)$; this takes polynomial time with a factor index, but much more than linear.
- **Suffix automaton.** Crochemore, Mignosi and Restivo (1998) read the minimal absent words off the suffix automaton (factor automaton) of $y$: a word $a\,u\,b$ is minimal absent exactly when $au$ is the shortest word of some state $p$, $u$ is the longest word of the state reached by the [suffix link](/suffix-link/) of $p$, that state has a transition by $b$ and $p$ has none. The total time is $O(n \sigma)$ with transition tables, or $O(n + \sigma + z)$ with the output-sensitive scan of the [minimal absent words algorithm](/minimal-absent-words-algorithm/).
- **Suffix array.** Barton, Heliou, Mouchard and Pissis (2014) compute the same set from the suffix array and the [LCP array](/lcp-array/) in $O(n)$ time for a fixed alphabet, which uses less memory on genomes; parallel and external-memory versions exist.
- **Integer alphabets.** Linear-time constructions of the suffix automaton for integer alphabets give $O(n + z)$ time for $\Sigma = \{0, \ldots, n^{O(1)}\}$.

## Bounds

- **Output size.** $z = |\mathrm{MAW}(y)| \le 2\sigma n$ for $n \ge 1$, as shown above, so the linear-time algorithms are also $O(\sigma n)$ in the worst case.
- **Lower bound.** Every algorithm reads the whole input, and each minimal absent word must be output, so $\Omega(n + z)$ time is necessary; the algorithms above meet it.
- **Lengths.** Every minimal absent word has length at most $n + 1$, and $a^{n+1}$ is one for $y = a^n$, so the total length of the words, as opposed to their number, can be large; this is why the output uses triples.

## Reductions

- **To the suffix automaton.** The bijection with pairs of a state and a missing transition, proved on the [algorithm page](/minimal-absent-words-algorithm/), reduces the problem to building a [suffix automaton](/suffix-automaton/) and scanning its suffix links.
- **Factor membership from absent words.** By the property above, an automaton that recognizes the words avoiding $\mathrm{MAW}(y)$, recognizes exactly $\mathrm{Fact}(y)$; such an automaton can be built from the trie of the minimal absent words, so the absent words are a complete description of the factors.

## Applications

- **Compression with antidictionaries.** In DCA compression (Crochemore, Mignosi, Restivo and Salemi, 2000) the encoder and decoder share a set of minimal absent words of the text. Whenever the next bit is forced, because the other choice would create an absent word, it is not transmitted.
- **Genomics.** Minimal absent words of genomes are short signatures of what a sequence avoids; distances between the sets of minimal absent words of two sequences give alignment-free comparisons.
- **Symbolic dynamics and languages.** A factorial language, such as the set of factors of an infinite word or a subshift, is described by its minimal forbidden words; a finite set of them defines a subshift of finite type.

## References
