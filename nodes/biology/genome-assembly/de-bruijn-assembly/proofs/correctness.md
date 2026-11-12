---
title: The de Bruijn assembler outputs the unitigs, and they spell the genome when no (k-1)-mer repeats
proves: [correctness]
status: full
---

We use the pseudocode of the page. The graph $G$ has one vertex for each $(k-1)$-mer and one edge $x$ from $x[1 \ldots k-1]$ to $x[2 \ldots k]$ for each kept $k$-mer $x$. Write $\mathrm{tail}(x)$ and $\mathrm{head}(x)$ for the two ends of $x$. A vertex $v$ is *simple* if it has in-degree 1 and out-degree 1. The string spelled by a walk $x_1 x_2 \cdots x_m$ is $x_1$ followed by the last letter of each of $x_2, \ldots, x_m$. It has length $m + k - 1$.

## 1. The paths are the unitigs

Define a relation on the edges: $e \to f$ if $\mathrm{head}(e) = \mathrm{tail}(f)$ and this vertex is simple. A *unitig* is a maximal sequence of edges $e_1, \ldots, e_m$ with $e_i \to e_{i+1}$ for each $i < m$. It is a maximal walk of $G$ whose inner vertices are all simple.

**Lemma 1.** Each edge has at most one successor and at most one predecessor under $\to$.

*Proof.* If $e \to f$, then $\mathrm{head}(e)$ is simple, so $f$ is its only out-edge. If $e \to f$, then $\mathrm{tail}(f)$ is simple, so $e$ is its only in-edge. $\square$

So the relation $\to$ splits the edges into disjoint chains and disjoint cycles, and the unitigs are exactly these chains and cycles. A chain starts at an edge $f$ with no predecessor, that is, an edge whose tail is not simple. A cycle has only simple vertices, so it is a whole connected component of $G$: no other edge can enter or leave a simple vertex on it.

**Theorem 1.** Lines L7 to L10 output each unitig exactly once, and each kept $k$-mer is on exactly one output path.

*Proof.* Lines L7 and L8 take each edge $e$ whose tail is not simple. These are exactly the first edges of the chains. Line L9 follows $\to$ from $e$: while the head is simple, it takes the only out-edge of the head. This is the successor of the last edge. It stops when the head is not simple, that is, at the last edge of the chain. The walk does not run forever: by Lemma 1, a repeated edge on it would have two predecessors, or would be $e$ with a predecessor, and neither is possible. So each chain is output once and in full. The edges not on a chain lie on cycles of $\to$. Line L10 takes the first such edge, follows the only out-edge until it returns to that edge, and marks each edge as used. So it outputs each cycle once. $\square$

## 2. Reconstruction when no (k-1)-mer repeats

Let $S$ be the genome, read on one strand, with $|S| \ge k$. The *genome walk* is $W = S[1 \ldots k], S[2 \ldots k+1], \ldots, S[|S|-k+1 \ldots |S|]$. Consecutive $k$-mers overlap in $k-1$ letters, so $W$ is a walk of $G$, and it spells $S$.

**Theorem 2.** Assume that the reads are substrings of $S$, that each $k$-mer of $S$ occurs in at least $t$ reads, and that no $(k-1)$-mer occurs twice in $S$. Then the output is the single contig $S$.

*Proof.* Each $k$-mer of a read is a $k$-mer of $S$, and each $k$-mer of $S$ has count at least $t$. So line L4 keeps exactly the $k$-mers of $S$. The vertices of $G$ are the $(k-1)$-mers $v_1, \ldots, v_{|S|-k+2}$ of $S$ in order, and by assumption they are distinct. The edges are the $k$-mers of $S$, and the $i$-th one goes from $v_i$ to $v_{i+1}$. So $G$ is one simple path. Its first vertex has in-degree 0, its last vertex has out-degree 0, and each other vertex is simple. By Theorem 1 the output is this one path, and it spells $S$. $\square$

## 3. Contigs are substrings when the ends are unique

**Theorem 3.** Assume that the reads are substrings of $S$, that each $k$-mer of $S$ is kept, and that the first and the last $(k-1)$-mer of $S$ each occur exactly once in $S$. Then each output contig is a substring of $S$.

*Proof.* As in Theorem 2, the edges of $G$ are the $k$-mers of $S$, so the genome walk $W$ uses every edge. Let $s$ be the first $(k-1)$-mer of $S$ and $z$ the last one. An edge enters $s$ only if some $k$-mer of $S$ ends with $s$. That would be an occurrence of $s$ at a position after the first, so the in-degree of $s$ is 0. In the same way the out-degree of $z$ is 0, and $W$ ends at $z$.

First, $G$ has no cycle of simple vertices. Such a cycle is a whole component, so if $W$ uses one of its edges, $W$ stays on it. Then $W$ ends at a simple vertex, but $W$ ends at $z$ with out-degree 0.

Now let $e_1, \ldots, e_m$ be an output chain. The walk $W$ uses $e_1$ at some step. We show by induction on $i$ that the next steps of $W$ are $e_2, \ldots, e_m$. After $W$ uses $e_i$ with $i < m$, it is at $\mathrm{head}(e_i)$, which is simple. This vertex has out-degree 1, so it is not $z$, and $W$ continues. The only out-edge is $e_{i+1}$. So $e_1 \cdots e_m$ is a consecutive part of $W$, and its spelled string is a substring of the string spelled by $W$, which is $S$. $\square$

**The condition on the ends is necessary.** Let $S = \mathtt{AABABAA}$ and $k = 3$. The first 2-mer $\mathtt{AA}$ occurs twice. The kept 3-mers are $\mathtt{AAB}$, $\mathtt{ABA}$, $\mathtt{BAB}$, $\mathtt{BAA}$. The vertex $\mathtt{AA}$ is simple, so the chain from $\mathtt{BA}$ is $\mathtt{BAA}, \mathtt{AAB}$. It spells $\mathtt{BAAB}$, which is not a substring of $S$. For a circular genome the condition is not needed, and the same induction shows that each unitig is a substring of the circular genome.
