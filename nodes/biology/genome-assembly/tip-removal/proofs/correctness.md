---
title: Tip removal stops with no removable tip, and an error near a read end makes a removable tip
proves: [correctness]
status: full
---

We use the pseudocode of the page. The graph $G$ is the edge-centric de Bruijn graph of order $k$: the vertices are $(k-1)$-mers, each kept $k$-mer $x$ is an edge from $x[1 \ldots k-1]$ to $x[2 \ldots k]$, and $\mathrm{count}(x)$ is the number of times $x$ occurs in the reads. A *unitig* is a maximal path whose inner vertices have in-degree 1 and out-degree 1. A unitig $P = e_1 \cdots e_m$ is a **removable tip** for the bound $\ell$ if $m < \ell$ and one of these holds:

- (source tip) the tail of $e_1$ has in-degree 0, the head $w$ of $e_m$ has in-degree at least 2, and $\mathrm{count}(e_m) < \mathrm{count}(f)$ for some other edge $f$ into $w$;
- (sink tip) the head of $e_m$ has out-degree 0, the tail $u$ of $e_1$ has out-degree at least 2, and $\mathrm{count}(e_1) < \mathrm{count}(f)$ for some other edge $f$ out of $u$.

Lines L3 to L7 test exactly these conditions, so in each round the set $T$ is the set of removable tips of the current graph.

## 1. The loop stops, and the result has no removable tip

**Theorem 1.** TIP-REMOVAL stops after at most $m_0 + 1$ rounds, where $m_0$ is the number of edges of the input. The output is a subgraph of the input with the same counts on the edges that remain, it has no removable tip, and each deleted edge was on a removable tip of the graph at the time it was deleted.

*Proof.* A round that does not return reaches line L9 with $T \ne \emptyset$ and deletes the edges of one tip, which has at least one edge. So each such round lowers the number of edges by at least 1, and after at most $m_0$ such rounds the next round returns. Line L9 only deletes edges and never changes a count, so each graph in the loop is a subgraph of the input with the input counts. The loop returns at line L8 only when $T = \emptyset$, that is, when the current graph has no removable tip. Line L9 deletes only the edges of a member of $T$, which is a removable tip of the current graph. $\square$

The output can depend on the order of the deletions, because a deletion changes the degrees at a junction and so changes the unitigs around it. Line L9 fixes the order: the tip with the smallest junction count goes first, as in Velvet, and ties go to the smaller string.

## 2. An error near the end of a read makes a removable sink tip

Let the genome be $S$ and let a read $r$ of length $L \ge k$ be the copy of $S[p \ldots p+L-1]$ (indices from 0) with one wrong letter at index $i$ of $r$. Let $d = L - 1 - i$ be the number of letters after the error.

**Lemma 2.** Assume that $k - 1 \le i$ and $d \le k - 2$. Assume also:

1. no $(k-1)$-mer that contains index $i$ of $r$ occurs in $S$ or in another read, and none occurs twice in $r$;
2. the $k$-mer $x = S[p+i-k+1 \ldots p+i]$ of the genome is kept and has $\mathrm{count}(x) \ge 2$.

Then the $k$-mers of $r$ that contain index $i$ form a removable sink tip of $d + 1$ edges for each bound $\ell > d + 1$, in particular for $\ell = 2k$.

*Proof.* The $k$-mers of $r$ that contain index $i$ start at the positions $i - k + 1, \ldots, L - k$ of $r$. These are $L - k - (i - k + 1) + 1 = L - i = d + 1$ edges $y_0, \ldots, y_d$. Each one contains index $i$, so by assumption 1 it is in no other read and not in $S$, and its count is 1.

The tail of $y_0$ is $u = r[i-k+1 \ldots i-1]$. It ends just before index $i$, so it is the correct $(k-1)$-mer $S[p+i-k+1 \ldots p+i-1]$. The edge $x$ also leaves $u$, and $x \ne y_0$ because they differ at the last letter. So $u$ has out-degree at least 2.

For $1 \le j \le d$, the tail of $y_j$ is $r[i-k+1+j \ldots i-1+j]$. It contains index $i$, because $i - k + 1 + j \le i$ and $i - 1 + j \ge i$. By assumption 1, the only kept $k$-mers that touch this vertex are $y_{j-1}$, which enters it, and $y_j$, which leaves it. So it has in-degree 1 and out-degree 1. The head of $y_d$ is $r[L-k+1 \ldots L-1]$, and it contains index $i$ because $L - k + 1 \le i$ holds exactly when $d \le k - 2$. It is a suffix of $r$, so by assumption 1 no kept $k$-mer leaves it: its out-degree is 0.

So $y_0 \cdots y_d$ starts at a non-simple vertex $u$, passes only simple vertices, and stops at a vertex of out-degree 0. It is a unitig. It has $d + 1 < \ell$ edges, its tail has out-degree at least 2, and $\mathrm{count}(y_0) = 1 < 2 \le \mathrm{count}(x)$ with $x$ another edge out of $u$. So it is a removable sink tip. $\square$

In the same way, an error at index $i \le k - 2$ near the start of a read, with $i + k - 1 \le L - 1$, makes a removable source tip of $i + 1$ edges, under the mirror assumptions. An error with $k - 1 \le i \le L - k$ is at least $k - 1$ letters from each end of the read. Then all $k$ of its $k$-mers lie inside the read, the path of false $k$-mers returns to the genome path, and it makes a bubble, not a tip.

## 3. Removal of the error tip does not touch the genome path

**Corollary 3.** Under the assumptions of Lemma 2, deleting the tip $y_0 \cdots y_d$ deletes no $k$-mer of $S$.

*Proof.* Each $y_j$ contains index $i$ of $r$, so by assumption 1 it is not a $k$-mer of $S$. $\square$

So the error tips go away and the genome $k$-mers stay, if no genome path is itself a removable tip. The second example of the page shows that this last condition can fail at the end of a genome.
