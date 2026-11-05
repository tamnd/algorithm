---
tag: DEK3N2
kind: algorithm
slug: minimal-absent-words-algorithm
name: Minimal absent words algorithm
aliases:
- minimal absent words computation algorithm
area: strings/string-combinatorics
level: advanced
summary: Computes all minimal absent words of a string using suffix structures.
solves: [minimal-absent-words]
model: word-ram
complexity:
  vars: {n: the length of the string, σ: the alphabet size, z: the number of minimal absent words}
  time: {expected: O(n + σ + z)}
  space: {extra: O(n)}
properties: {deterministic: true, recursive: false, online: false}
prereqs: [minimal-absent-words, suffix-automaton, suffix-link]
see_also: [minimal-absent-word, suffix-array, lcp-array, suffix-tree, maximal-repeats, shortest-unique-substring, subword-complexity, aho-corasick]
sources:
  - paper: "Maxime Crochemore, Filippo Mignosi and Antonio Restivo, Automata and forbidden words, Information Processing Letters 67(3), 1998, 111-117"
    locator: the algorithm that lists the minimal forbidden words of a word by comparing the transitions of each state of the factor automaton with those of its suffix-link target
  - paper: "Anselm Blumer, Janet Blumer, David Haussler, Andrzej Ehrenfeucht, M. T. Chen and Joel Seiferas, The smallest automaton recognizing the subwords of a text, Theoretical Computer Science 40, 1985, 31-55"
    locator: the online construction of the directed acyclic word graph (suffix automaton), its suffix links, and the bounds on its numbers of states and edges
  - paper: "Carl Barton, Alice Heliou, Laurent Mouchard and Solon P. Pissis, Linear-time computation of minimal absent words using suffix array, BMC Bioinformatics 15, 2014, article 388"
    locator: the alternative computation from the suffix array and the LCP array
---

The minimal absent words algorithm lists every [minimal absent word](/minimal-absent-word/) of a string $y$: every word that does not occur in $y$ although all its proper factors do. It builds the [suffix automaton](/suffix-automaton/) of $y$ and compares, for each state $p$, the letters that leave $p$ with the letters that leave the target of its [suffix link](/suffix-link/). Each letter $b$ that leaves the link target but not $p$ gives exactly one minimal absent word, the shortest word of $p$ followed by $b$. The method is due to Crochemore, Mignosi and Restivo (1998) and runs in time linear in the length of $y$ plus the number of words reported.

## In plain words

Think of a machine that reads a word and tells you whether it occurs in the text. The machine has one stop for each group of words that occur in exactly the same places, and a jump from each stop to the stop for a shorter tail of its words. A word occurs in the text if you can follow it through the machine.

Now look at any stop and the stop its jump leads to. The shorter tail can always be continued by every letter that the longer words can, and maybe by more. Each extra letter is a word that is missing from the text even though the word without its first letter and the word without its last letter are both present. Collecting these extra letters at every stop, plus the letters that never occur at all, gives the full list.

## The problem

The input is a string $y = y[0..n-1]$ over a finite alphabet $\Sigma$ of $\sigma$ letters that contains all letters of $y$; letters are only tested for equality, through hash maps. Strings are indexed from 0. The output is the set $\mathrm{MAW}(y)$ of words $w \ne \varepsilon$ with $w$ not a factor of $y$ and every proper factor of $w$ a factor of $y$. Each word is reported as a triple $(i, \ell, b)$, meaning $y[i..i+\ell-1]\,b$, so that the output takes $O(1)$ space per word; a letter $b$ missing from $y$ is $(0, 0, b)$. This is the [minimal absent words](/minimal-absent-words/) problem.

## The algorithm

The suffix automaton of $y$ has one state for each class of nonempty factors with the same set of end positions in $y$, plus the initial state $0$ for the empty word. For a state $p$, $\mathrm{len}[p]$ is the length of its longest word, $\mathrm{link}[p]$ is the state of the longest suffix of that word that lies in another class, $\mathrm{end}[p]$ is one end position of its words, and $\mathrm{next}[p]$ maps a letter $b$ to the state of $xb$ for the words $x$ of $p$, when $xb$ is a factor. The words of $p$ are the suffixes of its longest word with lengths $\mathrm{len}[\mathrm{link}[p]] + 1, \ldots, \mathrm{len}[p]$.

```pseudo id=main
MINIMAL-ABSENT-WORDS(y[0 .. n − 1], Σ)
L1  build the suffix automaton of y: states 0 .. N − 1, with len, link, end, next
L2  M ← empty list
L3  for each letter b in Σ do
L4      if next[0][b] is undefined then append (0, 0, b) to M
L5  for p ← 1 to N − 1 do
L6      ℓ ← len[link[p]] + 1                      ▷ length of the shortest word of p
L7      for each letter b with next[link[p]][b] defined do
L8          if next[p][b] is undefined then
L9              append (end[p] − ℓ + 1, ℓ, b) to M   ▷ the word y[end[p] − ℓ + 1 .. end[p]] · b
L10 return M
```

Line L1 is the standard online construction, which also records $\mathrm{end}$: a new state created while reading $y[i]$ gets $\mathrm{end} = i$, and a cloned state copies $\mathrm{end}$ from the state it was cloned from. Line L7 scans only the transitions of the link target, never the whole alphabet.

## Example

Let $y = $ `abaab` over $\Sigma = \{a, b\}$. The suffix automaton has six states.

| state $p$ | $\mathrm{len}$ | $\mathrm{link}$ | $\mathrm{end}$ | words of $p$ | letters out of $p$ | letters out of $\mathrm{link}[p]$ | reported |
| --- | --- | --- | --- | --- | --- | --- | --- |
| 0 | 0 | none | none | $\varepsilon$ | $a$, $b$ | | none |
| 1 | 1 | 0 | 0 | `a` | $a$, $b$ | $a$, $b$ | none |
| 2 | 2 | 0 | 1 | `ab`, `b` | $a$ | $a$, $b$ | $(1, 1, b)$ = `bb` |
| 3 | 3 | 1 | 2 | `aba`, `ba` | $a$ | $a$, $b$ | $(1, 2, b)$ = `bab` |
| 4 | 4 | 1 | 3 | `abaa`, `baa`, `aa` | $b$ | $a$, $b$ | $(2, 2, a)$ = `aaa` |
| 5 | 5 | 2 | 4 | `abaab`, `baab`, `aab` | none | $a$ | $(2, 3, a)$ = `aaba` |

Lines L3 and L4 report nothing, since both letters occur. For state 4, the shortest word is `aa` ($\ell = 2$, ending at position 3), and the link target, the state of `a`, has a transition by $a$ that state 4 lacks: so `aaa` is absent while its two maximal proper factors, both `aa`, occur. For state 5, the shortest word is `aab` ($\ell = 3$), and `ab` can be followed by $a$ but `aab` cannot, so `aaba` is reported. The output is $\{$`bb`, `bab`, `aaa`, `aaba`$\}$, the four minimal absent words of `abaab`.

## Correctness

The key fact is a bijection. A word $a\,u\,b$ with letters $a, b$ is a minimal absent word if and only if $au$ is the shortest word of some state $p \ne 0$, $u$ is the longest word of $\mathrm{link}[p]$, $\mathrm{next}[\mathrm{link}[p]][b]$ is defined and $\mathrm{next}[p][b]$ is not. In one direction, $au$ occurs and $aub$ does not, while $ub$ occurs, so $au$ and $u$ have different sets of end positions; since the words of a state are suffixes of each other with consecutive lengths, $u$ must be the longest word of the link target and $au$ the shortest word of $p$. In the other direction, the conditions say that $au$ and $ub$ occur but $aub$ does not. Distinct states have distinct shortest words, so each word is reported once, and the one-letter minimal absent words are exactly the letters with no transition from state 0. The full proof is in the correctness proof below.

## Complexity

- **Building.** The suffix automaton has at most $2n - 1$ states and at most $3n - 4$ transitions for $n \ge 3$, and the online construction takes $O(n)$ time with hash maps for the transitions (expected), or $O(n \log \sigma)$ with balanced search trees.
- **Scanning.** Every letter that leaves $p$ also leaves $\mathrm{link}[p]$, because a suffix of an extendable word is extendable. So the loop of line L7 for state $p$ takes $|\mathrm{next}[p]|$ steps that report nothing plus one step per reported word. Summed over all states this is at most $3n + z$ steps, and lines L3 and L4 add $\sigma$.
- **Total.** $O(n + \sigma + z)$ expected time and $O(n)$ extra space besides the output. Since $z \le 2\sigma n$ for $n \ge 1$, this is $O(\sigma n)$ in the worst case.

## Properties

- **Output-sensitive.** The time is linear in the input plus the output, not in $\sigma n$ when the output is small.
- **Compact output.** The words can be long (for $y = a^n$ the word $a^{n+1}$ is reported), so each is reported by a position, a length and a letter.
- **Online construction.** The automaton is built letter by letter, but the minimal absent words of a prefix are not maintained; the scan runs once at the end.
- **Deterministic output.** With hash maps only the running time depends on the hashing; the set of reported words does not, though their order may.

## Variants and improvements

- **Suffix array version.** Barton, Heliou, Mouchard and Pissis (2014) find the same pairs from the [suffix array](/suffix-array/) and [LCP array](/lcp-array/), in $O(n)$ time for a fixed alphabet and with less memory, which matters for genomes.
- **Suffix tree version.** The suffix links of the suffix automaton of $y$ form the [suffix tree](/suffix-tree/) of the reversed string, so the same comparison of extensions can be done on that suffix tree.
- **Bounded length.** Skip the states with $\mathrm{len}[\mathrm{link}[p]] + 2 > k$ to report only the words of length at most $k$.
- **Back to factors.** Inserting the reported words into a trie and adding failure links, as in [Aho-Corasick](/aho-corasick/), gives an automaton that accepts exactly the words with no minimal absent factor, which are the factors of $y$.

## When to use it

Use it when all minimal absent words of a text are needed, for example to build an antidictionary for compression or to compare the absent words of genomes, and the text fits in memory with an automaton of about $2n$ states. For very long texts over a small alphabet, the suffix array version uses less memory. To test whether one given word is a minimal absent word, it is simpler to check that it is absent and that its two maximal proper factors occur, with any factor index.

## Pitfalls

- **Forgetting the absent letters.** The scan of lines L5 to L9 finds only words of length at least 2; letters of $\Sigma$ that do not occur in $y$ are minimal absent words too, and they depend on $\Sigma$, not on $y$ alone.
- **Wrong end position for clones.** A clone must copy $\mathrm{end}$ from the state it was split from. Setting it to the current position gives a position where the words of the clone may not end, and the reported triples spell the wrong words.
- **Using the longest word.** The reported word starts with the shortest word of $p$, of length $\mathrm{len}[\mathrm{link}[p]] + 1$. Longer words of $p$ followed by $b$ are absent but not minimal, because they contain the shorter absent word.
- **Scanning the whole alphabet.** Looping over all of $\Sigma$ at every state is correct but costs $\Theta(\sigma n)$ even when the output is small.

## Implementations

## History

The suffix automaton, also called the directed acyclic word graph, was introduced by Blumer and coauthors (1985) together with its linear-time online construction. Crochemore, Mignosi and Restivo (1998) studied minimal forbidden words of a word, showed that they can be read off its factor automaton and that the factor automaton can be rebuilt from them, and so obtained linear-time conversions in both directions. Crochemore, Mignosi, Restivo and Salemi (2000) used these antidictionaries for data compression. Barton, Heliou, Mouchard and Pissis (2014) gave the suffix-array version aimed at whole genomes.

## References
