---
title: Skipping along contigs gives the k-mer intersection exactly when all read k-mers are indexed, and a superset of it otherwise
proves: [correctness]
status: full
---

We use the pseudocode of the page. $K$ is the set of k-mers of the transcripts and of their reverse complements, and $\mathrm{col}(x)$ is the set of transcripts that hold $x$ on either strand. There is an edge from $x$ to $y$ in $K$ when the last $k - 1$ letters of $x$ are the first $k - 1$ letters of $y$. A read $R$ has length $L \ge k$ and the k-mers $R_i = R[i..i + k - 1]$ for $i = 1, \ldots, L - k + 1$. The *naive set* is

$$\mathrm{Naive}(R) = \bigcap_{i : R_i \in K} \mathrm{col}(R_i),$$

and the empty set when no $R_i$ is in $K$. Positions are 1-based, as on the page; the code uses 0-based positions.

## 1. Contigs

The index cuts $K$ into contigs $c = (c_1, \ldots, c_{|c|})$. For $j < |c|$ the code puts $c_{j+1}$ after $c_j$ only if $c_j$ has exactly one successor in $K$, that successor is $c_{j+1}$, $c_{j+1}$ has exactly one predecessor in $K$, and $\mathrm{col}(c_{j+1}) = \mathrm{col}(c_j)$.

**Lemma 1.** Every k-mer of $K$ lies in exactly one contig, at one position. All k-mers of a contig have the same color, the color of the contig.

*Proof.* Call $y$ the *next* node of $x$ if the four conditions above hold for $x$ and $y$. Each node has at most one next node, and is the next node of at most one node, because a next node has exactly one predecessor. So the relation splits $K$ into disjoint simple paths and simple cycles. The first loop of the code starts a contig at every node that is not the next node of another node and follows next nodes to the end of its path; this covers every path. The second loop takes each node that is still not placed, which lies on a cycle, and follows the cycle once, so it covers every cycle. No node is placed twice, because a walk enters a node only from its unique predecessor in the relation. The colors are equal along each step, so they are equal on the whole contig. $\square$

## 2. Skipping is safe on indexed k-mers

**Lemma 2.** Suppose $R_i = c_p$ and $d \le |c| - p$, and suppose $R_{i+1}, \ldots, R_{i+d}$ are all in $K$. Then $R_{i+j} = c_{p+j}$ for $0 \le j \le d$.

*Proof.* By induction on $j$. The case $j = 0$ is given. Let $j < d$ with $R_{i+j} = c_{p+j}$. The k-mers $R_{i+j}$ and $R_{i+j+1}$ overlap in $k - 1$ letters, and $R_{i+j+1} \in K$, so $R_{i+j+1}$ is a successor of $c_{p+j}$ in $K$. As $p + j < |c|$, the node $c_{p+j}$ is not the last of its contig, so it has exactly one successor in $K$, namely $c_{p+j+1}$. Hence $R_{i+j+1} = c_{p+j+1}$. $\square$

## 3. The result

Let $H$ be the set of positions that the algorithm looks up in line L4 and finds in $K$ in line L5, and let $\mathrm{Fast}(R)$ be the returned set. Line L6 intersects one color per position in $H$, and line L10 returns the empty set when $H$ is empty.

**Lemma 3.** The loop stops, and $\mathrm{Fast}(R) = \bigcap_{i \in H} \mathrm{col}(R_i)$, or the empty set if $H$ is empty.

*Proof.* Each round raises $i$ by at least 1, so there are at most $L - k + 1$ rounds. By Lemma 1, $\mathrm{col}(R_i)$ is the color of the contig of $R_i$, which is what line L6 intersects. $\square$

**Theorem 1 (superset).** $\mathrm{Fast}(R) \supseteq \mathrm{Naive}(R)$ for every read.

*Proof.* Every position in $H$ holds a k-mer in $K$, so $\mathrm{Fast}(R)$ is an intersection over a subset of the positions of the naive set, which can only be larger. It remains to check the case $H = \emptyset$. A skip happens only in line L8, after a hit. If there is no hit, the loop visits every position one by one, so no $R_i$ is in $K$ and $\mathrm{Naive}(R)$ is empty too. $\square$

**Theorem 2 (exact).** If every k-mer of $R$ is in $K$, then $\mathrm{Fast}(R) = \mathrm{Naive}(R)$. In particular this holds for every error-free read that is a substring of a transcript or of its reverse complement, and then the source transcript is in $\mathrm{Fast}(R)$.

*Proof.* Take a hit at position $i$ with $R_i = c_p$, and the value $d = \min(|c| - p, L - k + 1 - i)$ of line L7. All of $R_{i+1}, \ldots, R_{i+d}$ are in $K$, so by Lemma 2 they are $c_{p+1}, \ldots, c_{p+d}$. Their colors equal the color of $c$ by Lemma 1, which line L6 has already intersected. So skipping them in line L8 does not change the intersection. (The test of line L8 also passes, by the same lemma.) Every position is thus either in $H$ or skipped with a color already in the intersection, and the two sets are equal. An error-free read from a transcript $t$ has all its k-mers in $t$ or in its reverse complement, so they are all in $K$, and $t$ is in every color that is intersected. $\square$

**Theorem 3 (what the set means).** If every k-mer of $R$ is in $K$, then $\mathrm{Fast}(R)$ is the set of transcripts $t$ such that every k-mer of $R$ occurs in $t$ or in its reverse complement.

*Proof.* By Theorem 2 and the definition of the colors. $\square$

This set contains every transcript that holds $R$ itself, but it can be larger: a transcript can hold all k-mers of $R$ in another order, or some on one strand and some on the other. Pseudoalignment does not check the order of the k-mers.

## 4. The number of lookups

**Theorem 4.** If every k-mer of $R$ is in $K$, the number of lookups is the number of *contig visits* of $R$: the maximal runs of consecutive read k-mers that lie at consecutive positions of one contig.

*Proof.* At a hit $R_i = c_p$, Lemma 2 shows that the read follows $c$ to position $p + d$, and the test of line L8 passes when $d > 0$, so the next lookup is at $i + d + 1$. Either $i + d + 1 > L - k + 1$ and the loop ends, or $p + d = |c|$ and the next k-mer starts a new visit. If $d = 0$, the visit has one k-mer. So each visit costs exactly one lookup. $\blacksquare$
