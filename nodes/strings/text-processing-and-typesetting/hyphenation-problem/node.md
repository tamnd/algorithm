---
tag: ZMG689
kind: problem
slug: hyphenation-problem
name: Hyphenation
aliases:
- word hyphenation
area: strings/text-processing-and-typesetting
level: intro
summary: Find the positions inside a word where it may be split across two lines with a hyphen, by the rules of a language.
prereqs: [alphabet]
see_also: [liang-hyphenation, hyphenation-pattern-generation, packed-trie, dictionary-matching, box-glue-penalty-model, greedy-line-breaking, knuth-plass-line-breaking]
sources:
  - url: http://bitsavers.trailing-edge.com/pdf/stanford/Stanford_CS_TR_Collection_2025-12-12/PDF/1983/CS-TR-83-977.pdf
    title: "Franklin Mark Liang, Word Hy-phen-a-tion by Com-put-er, PhD thesis, Stanford University, August 1983, report STAN-CS-83-977"
    locator: "Chapter 1 (the problem, the dictionary and the rule-based methods, and the old TeX algorithm) and Chapter 3 (hyphenation by patterns)"
  - book: isbn:0201134470
    title: "Donald E. Knuth, The TeXbook, Computers and Typesetting volume A, Addison-Wesley"
    locator: "Appendix H, Hyphenation"
  - paper: doi:10.1002/spe.4380111102
    title: "Donald E. Knuth and Michael F. Plass, Breaking paragraphs into lines, Software: Practice and Experience 11(11), 1119-1184, 1981"
    locator: "the use of hyphens as flagged penalties in the box, glue and penalty model"
---

Hyphenation is the problem of finding the places inside a word where a line may end with a hyphen. A typesetter needs these places when a paragraph has narrow lines: without them, long words leave large gaps between the other words. The correct places are set by the conventions of a language and by its dictionaries, not by a formula, so a program can only approximate them. The usual methods are a dictionary of hyphenated words, rules on letter classes, and the patterns of [Liang's method](/liang-hyphenation/), which TeX uses.

## In plain words

A long word at the end of a line may not fit. If you can cut it into two parts, with a hyphen after the first part, the line can be full and the spaces stay even. You cannot cut anywhere. In English "hy-phen-ation" may be cut after "hy" or after "hyphen", but not after "hyp". The rules depend on the language, on how the word is said, and sometimes on its meaning.

A program gets a word and must give the allowed cut points. It can look the word up in a list, but no list holds every word. So most programs learn short letter patterns from a list and apply them to any word. They try to find as many correct cut points as they can and to make no wrong one.

## Definition

Fix an alphabet $\Sigma$ and a language. A word is a string $u = u_0 u_1 \cdots u_{n-1}$ over $\Sigma$. A *position* $k$, with $1 \le k \le n - 1$, is the gap between $u_{k-1}$ and $u_k$; a hyphen at $k$ splits $u$ into $u_0 \cdots u_{k-1}$- and $u_k \cdots u_{n-1}$.

The reference of the language is a function $H$ that maps each word to its set of correct positions $H(u) \subseteq \{1, \ldots, n-1\}$. In practice $H$ is known only on a finite word list $D$, for example a dictionary with the hyphens marked.

A *hyphenation method* is a procedure $h$ that maps every word to a set $h(u) \subseteq \{1, \ldots, n-1\}$. On a word, its result splits the positions into three groups:

- found: $h(u) \cap H(u)$;
- errors (bad hyphens): $h(u) \setminus H(u)$;
- missed: $H(u) \setminus h(u)$.

The problem is to build an $h$ that is small and fast, finds a large share of $\sum_{u \in D} |H(u)|$, and makes almost no errors. A typesetter also applies two limits after the method: it keeps only the positions $k$ with $k \ge \lambda$ and $n - k \ge \rho$, where $\lambda$ and $\rho$ are the least numbers of letters before and after the hyphen (\lefthyphenmin and \righthyphenmin in TeX; plain TeX sets $\lambda = 2$ and $\rho = 3$).

Errors cost more than misses. A missed position only makes the spacing of one paragraph a little worse; a wrong hyphen is visible to every reader. So methods are tuned for few errors first.

## Variants

- **Exact lookup.** Store $D$ and answer $H(u)$ for $u \in D$. This is a static dictionary problem on strings, solved with a [trie](/trie/) or a [hash table](/hash-table/). It cannot hyphenate words that are not in $D$, such as new words, names and many derived forms.
- **Rules on letter classes.** Split between two consonants in a vowel-consonant-consonant-vowel group, split before known suffixes, and keep a short exception list. The hyphenation of the first TeX worked this way.
- **Patterns.** Store short strings with a digit in each gap, and decide each gap by the largest digit of all patterns that cover it, as in [Liang's method](/liang-hyphenation/). The patterns are learned from $D$ by [pattern generation](/hyphenation-pattern-generation/), and an exception list fixes the rest.
- **Weighted positions.** Some languages and some publishers rank the positions: a break between the parts of a compound word is better than a break inside a part. A method then returns a value per position, not a yes or a no.
- **Breaks that change the spelling.** In some languages the letters change at a hyphen. In German spelling before 1996, "Zucker" became "Zuk-ker". TeX models this with a discretionary break that has a text before the break, a text after it, and a text with no break.

## Examples

| word | correct positions | written |
|---|---|---|
| hyphenation | 2, 6, 7 | hy-phen-a-tion |
| table | 2 | ta-ble |
| record (noun) | 3 | rec-ord |
| record (verb) | 2 | re-cord |

The two rows for "record" show that $H$ is not a function of the letters alone in American English: the noun and the verb are spelled the same and hyphenated differently. Every method that looks only at the letters makes an error or a miss on one of them.

With the patterns of TeXbook Appendix H (hy3ph, he2n, hena4, hen5at, 1na, n2at, 1tio, 2io and o2n), Liang's rule gives hy-phen-ation: it finds the positions 2 and 6 and misses 7. A miss is the safe kind of mistake.

With the limits of plain TeX ($\lambda = 2$, $\rho = 3$), "table" can break at 2 ("ta-ble"), because $2 \ge 2$ and $5 - 2 \ge 3$. A word of four letters would need $k \ge 2$ and $4 - k \ge 3$, which no $k$ meets, so plain TeX never hyphenates a word of four letters.

## Known algorithms

- [Liang's hyphenation algorithm](/liang-hyphenation/): pattern matching with a trie of patterns; $O(k^2)$ trie steps for a word of $k$ letters in the worst case. TeX uses it.
- [Hyphenation pattern generation](/hyphenation-pattern-generation/) (patgen): builds the patterns from a hyphenated word list, level by level.
- [Packed trie](/packed-trie/): the compact table that holds the patterns in TeX82, with one table index per letter.
- [Dictionary matching](/dictionary-matching/) with [Aho-Corasick](/aho-corasick/) finds all occurrences of a set of patterns in one pass over the word, which gives the same values as Liang's rule.

## Bounds

For a fixed set of patterns, any method must read the word, so $\Omega(k)$ time is needed in the [word RAM](/word-ram/). Liang's walk takes $O(k^2)$ trie steps, and an automaton of the patterns takes $O(k + z)$, where $z$ is the number of pattern occurrences; for real words $k$ is small and both are fast.

There is no bound on accuracy that holds for all languages. The "record" example shows that a method based on the spelling alone cannot be correct on all of $D$ when $D$ holds two words with the same letters and different positions. The numbers that are known are measurements on one word list. Liang reports that the TeX82 patterns find 89.3 percent of the hyphens of his copy of Webster's Pocket Dictionary with essentially no errors, while the old TeX rules found about 40 percent with an error rate of about 1 percent of the hyphen points.

## Reductions

- Hyphenation by patterns reduces to [dictionary matching](/dictionary-matching/): the value of each gap is the largest digit over all occurrences of the patterns in ".u.", where "." marks the word edges.
- Exact lookup reduces to a static dictionary on strings ([trie](/trie/), [packed trie](/packed-trie/) or [hash table](/hash-table/)).

## Applications

- **Line breaking.** In the [box, glue and penalty model](/box-glue-penalty-model/), each allowed position becomes a flagged penalty with the width of the hyphen. [Greedy line breaking](/greedy-line-breaking/) and the [Knuth-Plass algorithm](/knuth-plass-line-breaking/) then choose which of them to use.
- **Narrow columns.** Newspapers and mobile screens have short lines, where words without hyphens give very loose lines.
- **Spelling and word lists.** Liang's thesis treats hyphenation and spelling checking together, because both need a compact store of many words.

## References
