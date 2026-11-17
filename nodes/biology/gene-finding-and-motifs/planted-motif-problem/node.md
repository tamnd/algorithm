---
tag: R51XFJ
kind: problem
slug: planted-motif-problem
name: Planted motif problem
aliases:
- "planted (l; d)-motif problem"
area: biology/gene-finding-and-motifs
level: core
summary: Recover a hidden string of length l from random background sequences, when a copy of it with at most d mismatches was planted in each sequence.
prereqs: [hamming-distance, motif-finding-problem]
see_also: [winnower-algorithm, random-projection-motif-finding, median-string-problem, branch-and-bound-motif-search, np-complete, w-hierarchy, clique-problem, kmer]
sources:
  - paper: "Pavel A. Pevzner and Sing-Hoi Sze, Combinatorial approaches to finding subtle signals in DNA sequences, Proceedings of the Eighth International Conference on Intelligent Systems for Molecular Biology (ISMB 2000), AAAI Press, 2000"
    title: Pavel A. Pevzner and Sing-Hoi Sze, Combinatorial approaches to finding subtle signals in DNA sequences, 2000
    locator: pp. 269 to 278, the planted (l, d) motif problem, the (15, 4) challenge, the expected distance of two instances and the comparison of CONSENSUS, GibbsDNA, MEME, WINNOWER and SP-STAR
  - paper: doi:10.1089/10665270252935430
    title: Jeremy Buhler and Martin Tompa, Finding motifs using random projections, Journal of Computational Biology 9(2), 2002
    locator: pp. 225 to 242, the planted motif model and the harder (14, 4), (16, 5) and (18, 6) cases
  - paper: doi:10.1007/s002240000044
    title: Moti Frances and Ami Litman, On covering problems of codes, Theory of Computing Systems 30(2), 1997
    locator: pp. 113 to 119, NP-completeness of the radius of a binary code (the closest string problem)
  - paper: doi:10.1007/s00493-006-0011-4
    title: Michael R. Fellows, Jens Gramm and Rolf Niedermeier, On the parameterized intractability of motif search problems, Combinatorica 26(2), 2006
    locator: pp. 141 to 167, W[1]-hardness of closest substring in the number of strings, also for a binary alphabet
  - paper: doi:10.1145/506147.506150
    title: Ming Li, Bin Ma and Lusheng Wang, On the closest string and substring problems, Journal of the ACM 49(2), 2002
    locator: pp. 157 to 171, polynomial-time approximation schemes for closest string and closest substring
---

The planted motif problem is a test form of [motif finding](/motif-finding-problem/) in which the answer is known. A hidden string $M$ of length $L$ is chosen, and a copy of $M$ with at most $d$ changed letters is put into each of $n$ random sequences. The task is to find $M$ from the sequences alone. Pevzner and Sze posed the case $L = 15$, $d = 4$ as a challenge in 2000, because the methods of that time failed on it. The decision form of the problem is NP-complete.

## In plain words

Someone writes a secret word of 15 letters. They make 20 random DNA strings of 600 letters each. Into each string they copy the word, but before each copy they change 4 of its letters, at random places. So no two copies are the same, and none is equal to the secret word.

You get the 20 strings and the numbers 15 and 4, and you must find the secret word. The hard part is that two copies can differ in up to 8 letters, while many pairs of random pieces of the strings are just as close as that by chance. A method that compares the pieces two at a time sees millions of false matches for each true one.

## Definition

The literature writes $l$ for the motif length; this page writes $L$, as the other motif pages do. Positions are 1-based on this page.

**The model.** Fix $n$, $G$, $L$ and $d < L$. Each background sequence $s_1, \ldots, s_n$ has $G$ letters drawn independently and uniformly from $\{A, C, G, T\}$. A motif $M$ of length $L$ is drawn uniformly. For each $i$, an *instance* $M_i$ with $d_H(M, M_i) \le d$ replaces the window of $s_i$ that starts at a position $p_i$, $1 \le p_i \le W = G - L + 1$. Here $d_H$ is the [Hamming distance](/hamming-distance/). In the model of Pevzner and Sze each instance has exactly $d$ changes: $d$ positions are picked at random, and each picked letter becomes one of the other three letters at random.

**An $(L, d)$ motif** of the sequences is a string $v$ of length $L$ such that every $s_i$ has a window $t_i$ with $d_H(v, t_i) \le d$. The planted motif $M$ is one of them.

**The search problem.** Given $s_1, \ldots, s_n$, $L$ and $d$, find the planted motif $M$ and the positions $p_i$.

**The decision problem.** Given strings $s_1, \ldots, s_n$ and integers $L$ and $d$, does an $(L, d)$ motif exist? This is the decision form of the closest substring problem, with no assumption on how the strings were made.

## Variants

- **At most $d$ or exactly $d$ changes.** The search for $(L, d)$ motifs is the same in both; only the statistics of the instances differ.
- **Sites in only some sequences.** In real data a factor may not bind every sequence. A quorum version asks for a string with a $d$ match in at least $q$ of the $n$ sequences.
- **Edit distance.** Insertions and deletions in the instances give the edited motif problem; the methods on this page do not handle it.
- **All motifs.** Exact methods list every $(L, d)$ motif. The output can then hold the planted one and spurious ones, as below.

## Examples

**A small case.** With a fixed seed, the test generator of these pages plants $M$ = AATTA ($L = 5$, $d = 1$) in $n = 4$ sequences of length $G = 12$:

| $i$ | $s_i$ | $p_i$ | instance | $d_H(M, M_i)$ |
|---|---|---|---|---|
| 1 | TCGAATCACAAC | 4 | AATCA | 1 |
| 2 | CTAGTTACTCTT | 3 | AGTTA | 1 |
| 3 | GCTAGATTACGT | 5 | GATTA | 1 |
| 4 | AACTAGTGGGAC | 1 | AACTA | 1 |

A check of all $4^5 = 1024$ strings finds that AATTA is the only $(5, 1)$ motif of these four sequences. No instance equals $M$, and two instances can differ in 2 letters: AATCA and AGTTA differ at positions 2 and 4.

**The challenge.** Pevzner and Sze used $n = 20$, $G = 600$, $L = 15$ and $d = 4$. Their Table 1 (a measurement, on 8 random samples) gives the average performance coefficient $|K \cap P| / |K \cup P|$, where $K$ is the set of planted letter positions and $P$ is the set of predicted ones: CONSENSUS 0.07, GibbsDNA 0.12, MEME 0.10, [WINNOWER](/winnower-algorithm/) 0.92 and SP-STAR 0.84.

## Known algorithms

| method | type | time | source |
|---|---|---|---|
| pattern enumeration: test each of the $4^L$ strings | exact | $O(4^L n W L)$ | folklore; see [median string](/median-string-problem/) |
| neighborhood enumeration: test each string within $d$ of a window of $s_1$ | exact | $O(W V(L, d) \cdot n W L)$ | folklore |
| [branch and bound](/branch-and-bound-motif-search/) on the string tree | exact | $O(4^L n W L)$ worst case | Jones and Pevzner 2004 |
| [WINNOWER](/winnower-algorithm/): filter a graph of windows to its $n$-cliques | exact on the graph, heuristic filter | polynomial per round | Pevzner and Sze 2000 |
| SP-STAR: local improvement of star-shaped sets of windows | heuristic | polynomial per round | Pevzner and Sze 2000 |
| [PROJECTION](/random-projection-motif-finding/): hash on random positions, then EM | randomized heuristic | depends on the trials | Buhler and Tompa 2002 |

Here $V(L, d) = \sum_{i=0}^{d} \binom{L}{i} 3^i$ is the number of strings within distance $d$ of a fixed string. The second method is right because $M$ is within $d$ of the instance in $s_1$, so $M$ is in the neighborhood of some window of $s_1$. For $(15, 4)$, $V = 123{,}841$, so it tests $586 \times 123{,}841 \approx 7.3 \times 10^7$ strings, against $4^{15} \approx 1.07 \times 10^9$ for the first method.

## Bounds

**Theorem.** The decision problem is NP-complete.

*Proof.* It is in NP: a string $v$ and one window in each sequence are a certificate, and the check takes $O(nL)$ time. For hardness, reduce from the closest string problem over the binary alphabet: given binary strings $x_1, \ldots, x_n$ of length $L$ and an integer $d$, is there a binary $v$ with $d_H(v, x_i) \le d$ for all $i$? Frances and Litman (1997) proved it NP-complete. Write each $x_i$ over $\{A, C\}$ with $0 \mapsto A$ and $1 \mapsto C$, and take $G = L$, so each sequence has one window, itself. A binary center gives an $(L, d)$ motif at once. Conversely, let $v$ be an $(L, d)$ motif over $\{A, C, G, T\}$. Change every G or T of $v$ into A. At such a position every $x_i$ had a mismatch, since $x_i$ holds A or C there, and after the change only the strings with C mismatch. So no distance grows, and the new $v$ is a center over $\{A, C\}$. The reduction takes linear time. $\square$

- **Parameterized.** Closest substring is W[1]-hard with the number $n$ of strings as the parameter, also over a binary alphabet (Fellows, Gramm and Niedermeier 2006). So an algorithm with time $f(n) \cdot \mathrm{poly}(G)$ is not expected; see the [W hierarchy](/w-hierarchy/). For a fixed $L$ the enumeration above is polynomial.
- **Approximation.** Li, Ma and Wang (2002) give polynomial-time approximation schemes for closest string and closest substring: a center within $(1 + \epsilon) d$ of a window of every sequence.

**Theorem (the distance of two instances).** In the model with exactly $d$ changes, two instances $M_1$ and $M_2$ of the same motif have $E[d_H(M_1, M_2)] = 2d - 4d^2/(3L)$.

*Proof.* Each instance changes a uniform random set of $d$ positions, so a fixed position is in both sets with probability $(d/L)^2$, and the expected number of shared positions is $d^2/L$. A position changed in one instance only is a mismatch. There are $2(d - d^2/L)$ of them on average. A position changed in both is a mismatch unless both picked the same of the three other letters, which has probability $1/3$. So the expected distance is $2(d - d^2/L) + \frac{2}{3} \cdot d^2/L = 2d - 4d^2/(3L)$. $\square$

For $(15, 4)$ this is $8 - 64/45 \approx 6.58$. Two random 15-mers are within distance 8 with probability about 0.0566. With 20 sequences of 600 letters there are $\binom{20}{2} \cdot 586^2 = 65{,}245{,}240$ pairs of windows from different sequences, so about $3.69 \times 10^6$ random pairs are as close as the worst pair of instances, against $\binom{20}{2} = 190$ pairs of instances. This is the ratio of about 20,000 to 1 that Pevzner and Sze give.

**How many spurious motifs (a heuristic).** A fixed string is within $d$ of a random window with probability $P_d = V(L, d)/4^L$. If the windows were independent, a sequence would hold a $d$ match with probability $1 - (1 - P_d)^W$, and the expected number of $(L, d)$ motifs made by chance would be $4^L (1 - (1 - P_d)^W)^n$. For $n = 20$ and $G = 600$:

| $(L, d)$ | $V(L, d)$ | $P_d$ | match in one sequence | expected spurious motifs |
|---|---|---|---|---|
| (15, 4) | 123,841 | $1.15 \times 10^{-4}$ | 0.065 | $2.2 \times 10^{-15}$ |
| (14, 4) | 91,771 | $3.42 \times 10^{-4}$ | 0.182 | $4.2 \times 10^{-7}$ |
| (16, 5) | 1,225,093 | $2.85 \times 10^{-4}$ | 0.154 | $2.3 \times 10^{-7}$ |
| (18, 6) | 15,886,504 | $2.31 \times 10^{-4}$ | 0.126 | $7.1 \times 10^{-8}$ |
| (9, 2) | 352 | $1.34 \times 10^{-3}$ | 0.549 | 1.6 |

So the $(15, 4)$ motif is the only one with high probability, and the problem is well posed. In the harder cases of Buhler and Tompa, $(14, 4)$, $(16, 5)$ and $(18, 6)$, background windows are close to the motif more often, but a unique answer is still expected. For $(9, 2)$ with these sizes, chance alone gives an $(L, d)$ motif, and no method can tell the planted one from the others.

## Reductions

- **To motif finding.** An $(L, d)$ motif with its windows is a choice of sites whose largest distance to a center is at most $d$, so its total distance score is at most $nd$. The motif finding methods with the total score can find it, but a choice with a small total score need not have a small largest distance.
- **To cliques.** Make a graph with one vertex for each window and an edge between windows of different sequences at distance at most $2d$. The instances of a planted motif are pairwise within $2d$ by the triangle inequality, so they form an $n$-clique in an $n$-partite graph. [WINNOWER](/winnower-algorithm/) uses this view; finding a largest clique is the [clique problem](/clique-problem/).
- **From closest string.** The NP-completeness proof above.

## Applications

- **Benchmarks.** The model gives inputs with a known answer, so the success rate of a method can be measured. Many motif finding papers after 2000 report results on $(15, 4)$ and harder cases.
- **Design of methods.** The analysis of two instances showed why methods that start from pairs of similar windows fail on subtle signals, and led to WINNOWER, PROJECTION and the exact enumeration methods.
- **Real binding sites.** Real sites are not planted uniformly and the background is not uniform, so success on planted data is a necessary test, not proof of success on promoters.

## References
