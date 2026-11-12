---
tag: J54TPG
kind: concept
slug: minimizer
name: Minimizer
aliases:
- minimizer sketch
- window minimizer
- (w,k)-minimizer
area: biology/sequence-alignment
level: advanced
summary: The smallest k-mer in each window of w consecutive k-mers. Strings that share w + k - 1 letters share a minimizer, and a random order keeps about 2/(w + 1) of all k-mers.
prereqs: [kmer-index]
see_also: [minimap2, kmer, kmer-counting, seed-and-extend, read-mapping, minhash, shingling]
sources:
  - paper: doi:10.1093/bioinformatics/bth408
    title: Michael Roberts, Wayne Hayes, Brian R. Hunt, Stephen M. Mount and James A. Yorke, Reducing storage requirements for biological sequence comparison, Bioinformatics 20(18), 2004
    locator: pages 3363 to 3369, the definition of (w,k)-minimizers and the property that two strings with a common substring of length w + k - 1 have a common minimizer
  - paper: doi:10.1145/872757.872770
    title: Saul Schleimer, Daniel S. Wilkerson and Alex Aiken, Winnowing, local algorithms for document fingerprinting, Proceedings of ACM SIGMOD 2003
    locator: pages 76 to 85, the winnowing algorithm (the minimum hash in each window), its guarantee threshold, its expected density 2/(w + 1) and the lower bound for local algorithms
  - paper: doi:10.1093/bioinformatics/btw152
    title: Heng Li, Minimap and miniasm, fast mapping and de novo assembly for noisy long sequences, Bioinformatics 32(14), 2016
    locator: pages 2103 to 2110, the minimizer sketch with an invertible integer hash and both strands of each k-mer
  - paper: doi:10.1093/bioinformatics/bty191
    title: Heng Li, Minimap2, pairwise alignment for nucleotide sequences, Bioinformatics 34(18), 2018
    locator: pages 3094 to 3100, Section 2 (the minimizer index in a hash table)
---

A $(w,k)$-minimizer of a string is the smallest [k-mer](/kmer/), under a fixed order, among $w$ consecutive k-mers of the string. The minimizers of all such windows form a *sketch*: a sample of the k-mers with two useful properties. Any two strings that share a substring of length $w + k - 1$ share a minimizer, and with a random order the sample keeps only about $2/(w+1)$ of the k-mers. Roberts, Hayes, Hunt, Mount and Yorke introduced minimizers for DNA in 2004; Schleimer, Wilkerson and Aiken had described the same idea in 2003 as *winnowing*, for document fingerprints. Minimizers are the seeds of [minimap2](/minimap2/) and of many other mappers and assemblers.

## In plain words

A DNA read and a genome have many short words in common. Storing every short word of the genome with its position takes a lot of memory. A minimizer scheme stores only some of the words, and it picks them in a way that two sequences agree on.

Slide a window over the sequence. The window holds a fixed number of short words that overlap. In each window, keep only the smallest word, where "smallest" is a fixed rule such as a hash value. Neighboring windows mostly keep the same word, so only a small part of all words is kept.

Two sequences that share a long enough piece also share a full window. In that window both of them keep the same word. So the kept words are enough to find the shared piece.

## The idea

**The model.** The alphabet is $\Sigma = \{A, C, G, T\}$. Let $s$ be a string of length $n$, and let $k \ge 1$ and $w \ge 1$ be integers with $n \ge w + k - 1$. Let $L = n - k + 1$ be the number of k-mers of $s$, and write $x_p = s[p \ldots p+k-1]$ for the k-mer at position $p$, for $0 \le p < L$. Fix a function $h : \Sigma^k \to \mathbb{Z}$, the *order*. Lexicographic order and an integer hash of the 2-bit code are the usual choices.

**Definition.** Window $i$, for $0 \le i \le L - w$, is the list of k-mers $x_i, x_{i+1}, \ldots, x_{i+w-1}$. It covers the substring $s[i \ldots i+w+k-2]$ of length $w + k - 1$. The minimizer position of window $i$ is

$$m(i) = \arg\min_{i \le p \le i+w-1} \bigl(h(x_p),\ p\bigr),$$

where pairs are compared lexicographically, so a tie goes to the leftmost k-mer. The *minimizer sketch* of $s$ is the set $M(s) = \{(x_p, p) : p = m(i) \text{ for some window } i\}$. The *density* of the scheme on $s$ is $|M(s)| / L$, the fraction of k-mer positions that it keeps.

The offset $m(i) - i$ depends only on the substring that window $i$ covers, not on the rest of $s$. This is the source of the first property.

**Property 1 (shared windows give shared minimizers).** Let $s$ and $t$ be strings with $s[i \ldots i+w+k-2] = t[j \ldots j+w+k-2]$. Then window $i$ of $s$ and window $j$ of $t$ have the same minimizer k-mer, at the same offset: $m_s(i) - i = m_t(j) - j$.

*Proof.* For $0 \le q < w$, the k-mer at offset $q$ of window $i$ of $s$ is $s[i+q \ldots i+q+k-1]$. It lies inside the common substring, so it equals the k-mer at offset $q$ of window $j$ of $t$. The two windows are the same list of k-mers, so they have the same values of $h$ in the same order, and the rule $\arg\min (h, \text{position})$ picks the same offset in both. $\square$

The length $w + k - 1$ is the least that works for every pair of strings: a common substring of length $w + k - 2$ does not contain a full window, and the example below has two strings with such a common substring and no common minimizer. This is the guarantee that Roberts et al. state for $(w,k)$-minimizers, and that Schleimer et al. call the guarantee threshold of winnowing.

**Property 2 (density about $2/(w+1)$).** Assume that the $L$ k-mers of $s$ are pairwise distinct and that the values $h(x_0), \ldots, h(x_{L-1})$ are independent and identically distributed with a continuous distribution. (Then each order of the values is equally likely, as for a uniformly random permutation.) Then

$$\mathbb{E}\,|M(s)| = 1 + \frac{2\,(L - w)}{w + 1},$$

so the expected density tends to $2/(w+1)$ as $L$ grows.

*Proof.* With distinct values there are no ties. First, $m(i) \le m(i+1)$ for each $i$. Let $p = m(i)$. If $p = i$, then $m(i+1) \ge i+1 > p$. If $p > i$, then $p$ lies in window $i+1$ too, and each position $q$ of window $i+1$ with $q < p$ also lies in window $i$, where $h(x_q) > h(x_p)$. So the minimum of window $i+1$ is not to the left of $p$. Since the sequence $m(0), m(1), \ldots$ never decreases, $|M(s)|$ is 1 plus the number of indices $i$, for $0 \le i < L - w$, with $m(i+1) \ne m(i)$.

Fix such an $i$, and let $r$ be the position of the smallest value among the $w + 1$ k-mers $x_i, \ldots, x_{i+w}$, which form the union of windows $i$ and $i+1$. If $i < r < i + w$, then $r$ is in both windows and is the minimum of both, so $m(i) = m(i+1) = r$. If $r = i$, then $m(i) = i$, and $m(i+1) \ne i$ because $i$ is not in window $i+1$. If $r = i + w$, then $m(i+1) = i + w$, which is not in window $i$. So the minimizer changes exactly when $r \in \{i, i+w\}$. Under the assumption each of the $w+1$ positions is the minimum with probability $1/(w+1)$, so a change happens with probability $2/(w+1)$. Linearity of expectation over the $L - w$ indices gives the formula. $\square$

Any scheme that keeps at least one k-mer of each window keeps at least $\lfloor L/w \rfloor$ positions, because the windows $0, w, 2w, \ldots$ that fit in $s$ have no k-mer position in common. So the density of any such scheme is at least about $1/w$, and a random order is within a factor of 2 of this bound. Schleimer et al. prove a sharper lower bound for their class of local algorithms and show that winnowing comes within 33% of it.

**The order matters.** The proof needs an order that behaves like a random one. Lexicographic order does not: overlapping k-mers have correlated ranks, and a run such as AAAA…A is the smallest k-mer of every window that contains it. The table gives the density on one random DNA string of 200,000 bases (Python `random.Random(1)`, each base uniform), for lexicographic order and for an invertible 64-bit integer hash of the 2-bit code, with leftmost tie-breaking:

| $(w, k)$ | lexicographic | integer hash | $2/(w+1)$ |
|---|---|---|---|
| (5, 11) | 0.3617 | 0.3334 | 0.3333 |
| (10, 15) | 0.1987 | 0.1823 | 0.1818 |
| (19, 19) | 0.1098 | 0.1006 | 0.1000 |

This is why minimap and minimap2 hash each k-mer with an invertible integer function before they compare. These programs also hash both strands of each k-mer and keep the smaller value, so a read and its reverse complement select the same positions.

**Ties and repeats.** When a window holds the same k-mer twice, as in a tandem repeat, the values are not distinct and Property 2 does not apply. The density on low-complexity sequence can then differ from $2/(w+1)$. The tie rule must depend only on the window, as the leftmost rule does, or Property 1 fails.

**Minimizers and MinHash.** [MinHash](/minhash/) keeps the smallest hash of a whole set, to estimate the Jaccard similarity of two sets. A minimizer keeps the smallest hash of each local window, so it keeps positions and finds local matches. The two ideas use the same "keep the minimum of a random order" trick for different questions.

## Examples

**A sketch.** Take $s = \texttt{GATTACACATTAG}$, $n = 13$, with $k = 3$, $w = 3$ and lexicographic order. The $L = 11$ k-mers are GAT, ATT, TTA, TAC, ACA, CAC, ACA, CAT, ATT, TTA, TAG at positions 0 to 10. There are $L - w + 1 = 9$ windows:

| window $i$ | k-mers | $m(i)$ | minimizer |
|---|---|---|---|
| 0 | GAT ATT TTA | 1 | ATT |
| 1 | ATT TTA TAC | 1 | ATT |
| 2 | TTA TAC ACA | 4 | ACA |
| 3 | TAC ACA CAC | 4 | ACA |
| 4 | ACA CAC ACA | 4 | ACA |
| 5 | CAC ACA CAT | 6 | ACA |
| 6 | ACA CAT ATT | 6 | ACA |
| 7 | CAT ATT TTA | 8 | ATT |
| 8 | ATT TTA TAG | 8 | ATT |

The sketch is $\{(\texttt{ATT}, 1), (\texttt{ACA}, 4), (\texttt{ACA}, 6), (\texttt{ATT}, 8)\}$: 4 of the 11 positions, a density of $4/11 \approx 0.36$. Window 4 holds ACA twice and the leftmost copy wins.

**A shared minimizer.** The string $t = \texttt{GGACATTCC}$ shares ACATT, of length $w + k - 1 = 5$, with $s[6 \ldots 10]$. Its window 2 is ACA, CAT, ATT, the same as window 6 of $s$, and both pick ACA at offset 0. A mapper that stores the sketch of $s$ finds $t$ through this one k-mer.

**A non-example.** With $w = k = 3$ and lexicographic order, $a = \texttt{AACCGT}$ and $b = \texttt{CCGTTG}$ share CCGT, of length $w + k - 2 = 4$. The sketch of $a$ holds AAC and ACC, and the sketch of $b$ holds CCG and CGT. The two sketches have no k-mer in common, so a common substring one letter shorter than the threshold can be missed.

## Where it is used

- **Read mapping.** [Minimap2](/minimap2/) stores the minimizers of the reference in a hash table, looks up the minimizers of each read, and chains the hits with [seed chaining](/seed-chaining/). A [k-mer index](/kmer-index/) of minimizers is about $(w+1)/2$ times smaller than an index of all k-mers. A match is found when the read and the reference share an exact piece of $w + k - 1$ bases, so the scheme can miss hits in regions with many errors.
- **Overlap detection in assembly.** Minimap finds the [overlaps](/overlap-detection/) between long reads by their shared minimizers, and the miniasm assembler builds its graph from these overlaps.
- **Counting k-mers.** [K-mer counting](/kmer-counting/) programs group consecutive k-mers that have the same minimizer, so that each group goes to one bucket on disk.
- **Document fingerprints.** Winnowing selects the minimum hash of each window of $w$ consecutive $k$-gram hashes to detect copied text and code, the setting of [shingling](/shingling/).

## References
