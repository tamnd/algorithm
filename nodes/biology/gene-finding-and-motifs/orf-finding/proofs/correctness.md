---
title: The six-frame scan reports exactly the ORFs of the sequence
proves: [correctness]
status: full
---

Let $s$ be a sequence of length $G$, let $\ell \ge 0$, and let START and STOP be disjoint sets of codons. Positions are from 0, and $t[i, j)$ is the part of $t$ from position $i$ up to but not including $j$.

Fix a strand $t$ (either $s$ or $\mathrm{rc}(s)$) and an offset $f \in \{0, 1, 2\}$. The codons of the frame are $c_j = t[f + 3j, f + 3j + 3)$ for $j = 0, 1, \ldots, J - 1$, where $J$ is the largest number with $f + 3J \le G$. Line L3 visits them in the order $j = 0, 1, \ldots, J - 1$, with $i = f + 3j$. For a codon index $j$, let $p(j)$ be the largest index $p < j$ with $c_p \in \mathrm{STOP}$, or $-1$ if there is none. So the codons $c_{p(j) + 1}, \ldots, c_{j - 1}$ hold no stop codon.

The ORFs of the frame are as follows (see the definition page). A *stop-stop ORF* is $c_{p(b) + 1}, \ldots, c_b$ for each $b$ with $c_b \in \mathrm{STOP}$. A *start-stop ORF*, in the form with the longest ORF for each stop, is $c_a, \ldots, c_b$ for each $b$ with $c_b \in \mathrm{STOP}$ such that some codon among $c_{p(b) + 1}, \ldots, c_{b - 1}$ is in START, where $a$ is the smallest such index. In both cases the ORF covers the interval $[f + 3a, f + 3b + 3)$ of $t$ and has $b - a$ sense codons, with $a = p(b) + 1$ for a stop-stop ORF.

**Lemma 1 (invariant).** Each time line L4 is reached for the codon $c_j$:

- in start-stop mode, `open` $= f + 3a$, where $a$ is the smallest index in $\{p(j) + 1, \ldots, j - 1\}$ with $c_a \in \mathrm{START}$, and `open` is none if there is no such index;
- in stop-stop mode, `open` $= f + 3(p(j) + 1)$.

*Proof.* By induction on $j$. For $j = 0$, $p(0) = -1$ and the set $\{0, \ldots, -1\}$ is empty. Line L2 sets `open` to none in start-stop mode and to $f = f + 3 \cdot 0$ in stop-stop mode, as claimed.

Assume the claim for $j$, and look at what the loop body does with $c_j$.

*Case $c_j \in \mathrm{STOP}$.* Then $p(j + 1) = j$. Line L7 sets `open` to none in start-stop mode, which is right because the set $\{j + 1, \ldots, j\}$ is empty. In stop-stop mode it sets `open` to $i + 3 = f + 3(j + 1) = f + 3(p(j + 1) + 1)$. Line L8 is not reached, because START and STOP are disjoint.

*Case $c_j \notin \mathrm{STOP}$.* Then $p(j + 1) = p(j)$, and the new set of candidate indices is the old one with $j$ added. In start-stop mode: if `open` was set, the smallest start index of the new set is the old one, and line L8 does not change `open`. If `open` was none and $c_j \in \mathrm{START}$, then $j$ is the only start index of the new set, and line L9 sets `open` to $i = f + 3j$. If `open` was none and $c_j \notin \mathrm{START}$, there is still no start index, and `open` stays none. In stop-stop mode, `open` does not change, and $p(j + 1) = p(j)$. In all cases the claim holds for $j + 1$. $\square$

**Lemma 2.** For one frame, lines L3 to L9 add, for each stop codon $c_b$ of the frame, the ORF that ends at $c_b$ if it exists and has at least $\ell$ sense codons, and they add nothing else.

*Proof.* An ORF is added only at line L6, so only when the codon $c_j$ is a stop, with $i = f + 3j$. By Lemma 1, `open` at that moment is $f + 3a$ for the index $a$ of the definition of the ORF that ends at $c_j$, in either mode, and `open` is none exactly when no start-stop ORF ends at $c_j$ (in stop-stop mode it is never none). The added interval is $[\mathit{open}, i + 3) = [f + 3a, f + 3j + 3)$, the interval of that ORF, and the count $(i - \mathit{open})/3 = j - a$ is its number of sense codons. Line L5 adds it if and only if this count is at least $\ell$. Each codon is visited once, so each stop codon gives at most one ORF. Every ORF ends at a stop codon of the frame, so no ORF is missed. $\square$

A run of codons after the last stop codon of the frame is not followed by a stop, so it is not an ORF, and it is not added: the loop ends without a stop for it.

**Lemma 3 (coordinates of the minus strand).** For $0 \le p < G$, base $p$ of $\mathrm{rc}(s)$ is the complement of base $G - 1 - p$ of $s$. So the interval $[a, b)$ of $\mathrm{rc}(s)$ consists of the complements of the bases of $s$ in $[G - b, G - a)$, in reverse order, and $\mathrm{rc}(s[G - b, G - a)) = \mathrm{rc}(s)[a, b)$.

*Proof.* $\mathrm{rc}(s)$ is $s$ reversed and complemented, so its base $p$ is the complement of base $G - 1 - p$ of $s$. As $p$ runs over $a, \ldots, b - 1$, the index $G - 1 - p$ runs over $G - 1 - a$ down to $G - b$, which is the interval $[G - b, G - a)$ read backward. $\square$

**Theorem.** FIND-ORFS returns every ORF of $s$ in the six frames with at least $\ell$ sense codons, each once, with its correct interval on $s$, and nothing else.

*Proof.* Lines L1 and L2 visit the six frames: offsets 0, 1 and 2 of $s$ and of $\mathrm{rc}(s)$. By Lemma 2, the scan of each frame adds exactly the ORFs of that frame with at least $\ell$ codons, in the coordinates of its strand. Line L10 leaves the plus strand intervals as they are, and by Lemma 3 it maps each minus strand interval $[a, b)$ to the interval of $s$ whose reverse complement is the ORF. ORFs of different frames are different objects, so no ORF is listed twice. Line L11 only sorts. $\square$

**Running time.** Building $\mathrm{rc}(s)$ takes $\Theta(G)$ steps. Frame $(t, f)$ has $J_f = \lfloor (G - f)/3 \rfloor$ codons, and $J_0 + J_1 + J_2 \le G$, so lines L3 to L9 run at most $2G$ times in total, each in $O(1)$ time on a word RAM: a codon is a 6-bit key, and the tests of lines L4 and L8 are look-ups in tables of 64 entries. Line L10 costs $O(1)$ per ORF. Each stop codon gives at most one ORF, so the number $R$ of ORFs is at most $J_0 + J_1 + J_2 \le G$ per strand, and $R \le 2G$. The sort of line L11 costs $O(R \log R)$. The total is $\Theta(G + R \log R)$, and $\Theta(G)$ without the sort.
