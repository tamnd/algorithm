---
tag: BJR06Z
kind: problem
slug: median-string-problem
name: Median string problem
aliases:
- motif median string
area: biology/gene-finding-and-motifs
level: intro
summary: Find a string of length l with the smallest total Hamming distance to its closest window in each sequence. It is equivalent to motif finding with the total Hamming distance score only.
prereqs: [hamming-distance, motif-finding-problem]
see_also: [branch-and-bound-motif-search, planted-motif-problem, greedy-motif-search, consensus-sequence, kmer, edit-distance, brute-force-search, np-hard]
sources:
  - book: isbn:9780262101066
    title: Neil C. Jones and Pavel A. Pevzner, An Introduction to Bioinformatics Algorithms, MIT Press, 2004
    locator: Chapter 4, Section 4.9 (finding a median string), with the problem statements of Section 4.6 and the search trees of Sections 4.7 and 4.8
  - book: isbn:9780990374619
    title: Phillip Compeau and Pavel Pevzner, Bioinformatics Algorithms, An Active Learning Approach, Volume I, 2nd edition, Active Learning Publishers, 2015
    locator: Chapter 2, Section 2.4, from motif finding to finding a median string
  - paper: doi:10.1006/jcss.2002.1823
    title: Ming Li, Bin Ma and Lusheng Wang, Finding similar regions in many sequences, Journal of Computer and System Sciences 65(1), 2002
    locator: NP-hardness of Consensus Patterns, the same problem under the total Hamming distance
---

The median string problem asks for a string $v$ of length $L$ that is close to all of a set of sequences at once: for each sequence, take the [Hamming distance](/hamming-distance/) from $v$ to its closest window, and add these distances. A string with the smallest sum is a median string. The problem has the same optimum as [motif finding](/motif-finding-problem/) with the total Hamming distance score, and it turns a search over $W^n$ choices of sites into a search over $4^L$ strings. With other scores, such as [information content](/motif-information-content/), the two problems differ.

## In plain words

Think of a candidate word of length $L$. Slide it along each sequence and find the place where it fits best, the place with the fewest different letters. Write down that number of different letters for each sequence and add them up. That sum says how well the word fits all the sequences.

The median string is the word with the smallest sum. You can find it by trying all the words of length $L$. That is a lot of words when $L$ is large, but it is far fewer than all the ways to pick one window in each sequence, because the number of words does not grow with the number of sequences.

## Definition

**Input.** Sequences $s_1, \ldots, s_n$ over $\{A, C, G, T\}$, each of length $G$, and a length $L \le G$. Each $s_i$ has $W = G - L + 1$ windows $s_i[q .. q + L - 1]$, $1 \le q \le W$. Positions are 1-based on this page.

**Distance to a sequence.** For a string $v$ of length $L$, let $d(v, s_i) = \min_{1 \le q \le W} d_H(v, s_i[q .. q + L - 1])$.

**Total distance.** $D(v) = \sum_{i=1}^{n} d(v, s_i)$.

**The question.** Find a string $v \in \{A, C, G, T\}^L$ with the smallest $D(v)$. Such a $v$ is a *median string*. The decision form asks whether some $v$ has $D(v) \le k$.

The median $v$ is any string of length $L$; it does not have to occur in any sequence.

## Variants

- **Over the windows only.** Restrict $v$ to the windows of the input. This takes $O((nW)^2 L)$ time, but the result can be worse than the true median.
- **The largest distance.** Replace the sum by $\max_i d(v, s_i)$. This is the closest substring problem, the core of the [planted motif problem](/planted-motif-problem/).
- **A median under edit distance.** In string algorithms, a median string of whole strings often means a string with the smallest sum of [edit distances](/edit-distance/) to them. That is a different problem with no windows, and it is not the subject of this page.

## Examples

Take the five sequences of Rosalind problem BA2D with $L = 3$: GGCGTTCAGGCA, AAGAATCAGTCA, CAAGGAGTTCGC, CACGTCAATCAC and CAATAATATTCG. A computation of $D(v)$ for all 64 strings gives this distribution:

| $D(v)$ | 2 | 3 | 4 | 5 | 6 | 7 | 8 |
|---|---|---|---|---|---|---|---|
| strings | 3 | 8 | 7 | 17 | 17 | 6 | 6 |

The three median strings, with $D = 2$, are:

| $v$ | $d(v, s_1), \ldots, d(v, s_5)$ | first closest windows (start) |
|---|---|---|
| CAA | 1, 1, 0, 0, 0 | CAG (7), GAA (3), CAA (1), CAA (6), CAA (1) |
| TCA | 0, 0, 1, 0, 1 | TCA (6), TCA (6), TCG (9), TCA (5), TAA (4) |
| TTC | 0, 1, 0, 1, 0 | TTC (5), ATC (5), TTC (8), GTC (4), TTC (9) |

TCA has no exact copy in $s_3$ or $s_5$, and CAA has none in $s_1$ or $s_2$. CAG occurs exactly in $s_1$ and $s_2$ but has $D = 3$. The windows CAG, CAG, CAA, CAA, CAA of the [greedy motif search](/greedy-motif-search/) have the consensus CAA and the score 2, so they are optimal sites, and their consensus is a median string.

## Known algorithms

| method | type | time | source |
|---|---|---|---|
| all $4^L$ strings, each scored against all windows | exact | $O(4^L n W L)$ | Jones and Pevzner, Section 4.9; Compeau and Pevzner, Section 2.4 |
| the same on the tree of prefixes, one column per tree node | exact | $O(4^L n W)$ | Jones and Pevzner, Sections 4.7 to 4.9 |
| [branch and bound](/branch-and-bound-motif-search/) on the tree of prefixes | exact | $O(4^L n W)$ worst case, often less | Jones and Pevzner, Section 4.9 |
| the windows of the input as candidates | heuristic | $O((nW)^2 L)$ | folklore |

On the tree of prefixes, a node of depth $k$ keeps for each window the number of mismatches of its first $k$ letters with the prefix. A child adds one column, which takes $O(nW)$ time, and the tree has fewer than $\frac{4}{3} 4^L$ nodes. This gives the $O(4^L n W)$ bound.

## Bounds

**Theorem (equivalence).** Let $\mathrm{Score}(p) = \sum_j (n - \max_a c_j(a))$ be the motif score of a choice of sites $p$, as on the [motif finding](/motif-finding-problem/) page. Then $\min_p \mathrm{Score}(p) = \min_v D(v)$. A consensus of an optimal choice is a median string, and the closest windows of a median string are an optimal choice.

*Proof.* For a choice $p$ with windows $t_1, \ldots, t_n$ and any string $v$, column $j$ adds $n - c_j(v_j)$ mismatches to $\sum_i d_H(v, t_i)$. So $\sum_i d_H(v, t_i) \ge \mathrm{Score}(p)$, with equality when $v$ is a consensus of $p$.

First, let $v$ be any string and let $p(v)$ pick a closest window of $v$ in each sequence. Then $\mathrm{Score}(p(v)) \le \sum_i d_H(v, t_i) = D(v)$. So $\min_p \mathrm{Score}(p) \le \min_v D(v)$.

Second, let $p$ be any choice and $v$ a consensus of $p$. Each $d(v, s_i) \le d_H(v, t_i)$, so $D(v) \le \sum_i d_H(v, t_i) = \mathrm{Score}(p)$. So $\min_v D(v) \le \min_p \mathrm{Score}(p)$, and the two minima are equal.

If $p$ is optimal, its consensus $v$ has $D(v) \le \mathrm{Score}(p) = \min D$, so $v$ is a median string. If $v$ is a median string, $\mathrm{Score}(p(v)) \le D(v) = \min \mathrm{Score}$, so $p(v)$ is optimal. $\square$

- **NP-hard.** The proof maps each instance to itself and keeps the optimal value, so the decision forms "is $\min D \le k$" and "is $\min \mathrm{Score} \le k$" are the same question. The second is Consensus Patterns, which Li, Ma and Wang (2002) proved NP-hard, so the median string problem with $L$ in the input is NP-hard. See [NP-hard](/np-hard/).
- **Fixed $L$.** The enumeration takes $O(4^L n W)$ time, which is linear in the input size $nG$ for a fixed $L$.
- **A lower bound for each prefix.** For a prefix $u$ of length $k$, every extension $v$ has $D(v) \ge \sum_i \min_q d_H(u, s_i[q .. q + k - 1])$, because the mismatches of the first $k$ letters never go away. This is the bound of the [branch and bound search](/branch-and-bound-motif-search/).

## Reductions

- **From motif finding.** By the theorem, any motif finding method for the total score gives median strings, and back, with $O(nWL)$ extra time to find the closest windows or the consensus.
- **To the planted motif problem.** A planted motif $M$ has $D(M) \le nd$. If the total distance of the planted motif is the smallest, the median string recovers it. On random data with subtle signals this can fail, because other strings can have a smaller sum while some sequence has no window within $d$ of them.
- **To exact pattern counting.** The question whether some $v$ has $D(v) = 0$ asks for a [k-mer](/kmer/) that occurs exactly in all sequences. A hash set of the windows of each sequence answers it in $O(nWL)$ time.

## Applications

- **Exact motif finding for short motifs.** For short motifs the $4^L$ strings can be enumerated ($4^{10} = 1{,}048{,}576$), and the median string gives the optimal sites under the total score.
- **Seeds for other methods.** A median string or the best strings of the enumeration can start a [Gibbs sampler](/gibbs-motif-sampler/) or an EM method such as [MEME](/meme-algorithm/).
- **Teaching.** The problem is the standard example of how a change of the search space, from sites to strings, makes an exponential search practical.

## References
