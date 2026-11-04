---
tag: G6X9X7
kind: model
slug: red-blue-pebble-game
name: Red-blue pebble game
aliases:
- Hong-Kung pebble game
- pebble game
area: foundations/models-of-computation
level: advanced
summary: Pebble game on a computation DAG in which red pebbles model fast memory and blue pebbles model slow memory; the cost is the number of moves between the two.
prereqs: [external-memory-model, memory-hierarchy, asymptotic-notation]
see_also: [external-memory-model, cache-oblivious-model, blocked-matrix-multiplication, fast-fourier-transform, naive-matrix-multiplication, external-sorting-io-lower-bound]
sources:
  - paper: "Jia-Wei Hong and H. T. Kung, I/O complexity: the red-blue pebble game, Proceedings of the 13th Annual ACM Symposium on Theory of Computing (STOC 1981)"
    locator: the definition of the game, the S-partition lemma, and the bounds for matrix multiplication and the FFT
  - paper: "Dror Irony, Sivan Toledo and Alexander Tiskin, Communication lower bounds for distributed-memory matrix multiplication, Journal of Parallel and Distributed Computing 64(9) (2004)"
    locator: the proof of the lower bound for the conventional algorithm with the Loomis and Whitney inequality
  - paper: "Lynn H. Loomis and Hassler Whitney, An inequality related to the isoperimetric inequality, Bulletin of the American Mathematical Society 55 (1949)"
    locator: the inequality on the volume of a set and the areas of its three projections
  - paper: "Grey Ballard, James Demmel, Olga Holtz and Oded Schwartz, Graph expansion and communication costs of fast matrix multiplication, Journal of the ACM 59(6) (2012)"
    locator: abstract (the bound for Strassen-like algorithms)
  - paper: "Alok Aggarwal and Jeffrey Scott Vitter, The input/output complexity of sorting and related problems, Communications of the ACM 31(9) (1988), 1116 to 1127"
    locator: the model with blocks, and the sorting bound
  - paper: "Michael S. Paterson and Carl E. Hewitt, Comparative schematology, Record of the Project MAC Conference on Concurrent Systems and Parallel Computation (1970)"
    locator: the pebble game on the graph of a program schema
  - paper: "John Hopcroft, Wolfgang Paul and Leslie Valiant, On time versus space, Journal of the ACM 24(2) (1977), 332 to 337"
    locator: the pebble game with one colour and the space bound for graphs of bounded in-degree
  - paper: "Erik D. Demaine and Quanquan C. Liu, Red-blue pebble game: complexity of computing the trade-off between cache size and memory transfers, Proceedings of the 30th ACM Symposium on Parallelism in Algorithms and Architectures (SPAA 2018), 195 to 204"
    locator: Section 2 (PSPACE-completeness) and the result for the game without deletions (NP-completeness)
  - paper: "Pal Andras Papp and Roger Wattenhofer, On the hardness of red-blue pebble games, Proceedings of the 32nd ACM Symposium on Parallelism in Algorithms and Architectures (SPAA 2020)"
    locator: abstract (NP-hardness in the one-shot variant)
---

The red-blue pebble game is a model of the data movement of a computation. The computation is a directed acyclic graph. A player puts red pebbles (fast memory, a limited number) and blue pebbles (slow memory, an unlimited number) on its vertices by fixed rules. The cost of a play is the number of moves between red and blue. Hong and Kung introduced it in 1981 and used it to prove tight lower bounds on the I/O of matrix multiplication and of the fast Fourier transform.

## The machine

**The graph.** The input is a directed acyclic graph $G = (V, E)$. A vertex with no incoming edge is an *input*. A vertex with no outgoing edge is an *output*. An edge $u \to v$ means that the value of $v$ is computed from the value of $u$ (and from the other predecessors of $v$). The graph is the data-flow of one algorithm on one input size, so the model analyses an algorithm, not a problem. Assume that each vertex is an ancestor of an output. Otherwise delete the vertex.

**The pebbles.** There are $S \ge 1$ red pebbles and as many blue pebbles as the player wants. A vertex holds at most one pebble of each colour. Red models the fast memory with $S$ words. Blue models the slow memory. At the start, each input has a blue pebble and no vertex has a red pebble.

**The moves.** There are four moves.

1. *Read (R1).* Put a red pebble on a vertex that has a blue pebble.
2. *Write (R2).* Put a blue pebble on a vertex that has a red pebble.
3. *Compute (R3).* Put a red pebble on a vertex that is not an input, if every immediate predecessor of the vertex has a red pebble.
4. *Delete (R4).* Remove a red pebble or a blue pebble from a vertex.

R1 and R3 need a free red pebble: at most $S$ red pebbles are on the graph at any time. A *play* is a sequence of moves that ends with a blue pebble on each output. Hong and Kung allow R3 to be used more than once on the same vertex (recomputation). The *one-shot* variant allows R3 at most once for each vertex. A game on a graph with a vertex of in-degree $d$ needs $S \ge d + 1$.

## What it counts

The cost of a play is the number of moves R1 and R2, called I/O moves. The moves R3 and R4 are free. The *I/O complexity* $Q(G, S)$ of $G$ with $S$ red pebbles is the minimum cost over all plays. It is a property of the graph and of $S$. It is a lower bound for every program that computes the graph with a fast memory of $S$ words, because a program is a play: a word in the fast memory is a red pebble, and a move between the memories is an I/O move.

**Example.** Let $G$ have four inputs $x_1, \dots, x_4$, two sums $s_{12} = x_1 + x_2$ and $s_{34} = x_3 + x_4$, and the output $s = s_{12} + s_{34}$. With $S = 2$ no play exists, because a sum needs a red pebble on both predecessors and on itself, which is 3 pebbles. With $S = 4$, the player reads $x_1$ and $x_2$, computes $s_{12}$, deletes $x_1$ and $x_2$, reads $x_3$ and $x_4$, computes $s_{34}$, deletes $x_3$ and $x_4$, computes $s$ and writes it. This costs $5$. With $S = 3$ the player cannot keep $s_{12}$, $x_3$ and $x_4$ and also compute $s_{34}$. So the player writes $s_{12}$ and reads it again later. This play costs $7$: 4 reads of the inputs, 1 write and 1 read of $s_{12}$, and 1 write of $s$. No play costs less. Every play reads each input at least once, because R3 does not apply to an input, and writes $s$ once. When R3 computes $s$, both $s_{12}$ and $s_{34}$ hold red pebbles. Look at the times when these two red pebbles were placed, and let $u$ be the sum whose pebble was placed later. If R3 placed it, then $u$ and its two inputs held 3 red pebbles at that time, so the other sum had no red pebble, and this contradicts the choice of $u$. So R1 placed it, and R1 needs a blue pebble on $u$, which only an earlier R2 on $u$ gives. These are 2 more I/O moves, so the cost is at least $5 + 2 = 7$.

## Relation to other models

- **External memory model.** The [external memory model](/external-memory-model/) has a block size $B$ and a cache of $M$ items. The pebble game is the case $B = 1$ with $S = M$, and with a fixed graph in place of a program. Aggarwal and Vitter (1988) added the block size. The FFT bound below, $\Theta(n \log n / \log S)$, has the same shape as the sorting bound with $B = 1$.
- **Cache-oblivious model.** The [cache-oblivious model](/cache-oblivious-model/) also has an optimal offline cache. A lower bound on $Q(G, S)$ holds for each schedule, so it holds for an algorithm that does not know $S$.
- **Time.** The game ignores the number of computation steps. An algorithm that recomputes values may reduce I/O and increase time. The one-shot variant forbids this.
- **Other pebble games.** The game extends the black pebble game of Paterson and Hewitt (1970), which Hopcroft, Paul and Valiant (1977) used for time versus space. The black pebble game has one colour. It measures the number of pebbles, which is the space, and sometimes the number of moves, which is the time, but it has no notion of I/O. The second colour is the new element: it makes the slow memory part of the model.

## Known results in the model

Here $S$ is the number of red pebbles and $Q$ is the I/O complexity.

**The S-partition lemma.** A *2S-partition* of $G$ is a partition of $V$ into sets $V_1, \dots, V_h$ with three properties.

1. If $u \to v$ is an edge, $u \in V_i$ and $v \in V_j$, then $i \le j$.
2. Each $V_i$ has a *dominator set* $D_i$ with $|D_i| \le 2S$. This is a set of vertices of $G$ such that every path from an input to a vertex of $V_i$ contains a vertex of $D_i$.
3. The *minimum set* of $V_i$ is the set of vertices of $V_i$ that have no successor in $V_i$. It has at most $2S$ vertices.

Let $H(2S)$ be the smallest $h$ for which a $2S$-partition exists.

**Lemma (Hong and Kung).** Every play with $S$ red pebbles makes at least $S\,(H(2S) - 1)$ I/O moves.

Proof for the one-shot variant. Hong and Kung prove the lemma when recomputation is allowed; that proof is in their paper. Take a play with $q$ I/O moves. Cut the sequence of moves after each $S$-th I/O move. This gives $\lfloor q/S \rfloor + 1$ segments, each with at most $S$ I/O moves. Let $V_i$ be the set of vertices whose first red pebble appears in segment $i$. Every vertex gets a red pebble at some time, because it is an ancestor of an output. We check the three properties for segment $i$.

*Property 1.* Let $u \to v$ be an edge. The vertex $v$ is not an input, and it gets its first red pebble by R3, since R1 needs a blue pebble and a blue pebble needs an earlier red pebble. At that time $u$ has a red pebble, so the first red pebble of $u$ is in the same segment or an earlier one.

*Property 2.* Let $D_i$ be the set of vertices that have a red pebble at the start of segment $i$, together with the vertices that get a red pebble by R1 in segment $i$. At most $S$ vertices have a red pebble at the start, and R1 occurs at most $S$ times in the segment. So $|D_i| \le 2S$. We show: every vertex $x$ that has a red pebble at some time in segment $i$ is such that every path from an input to $x$ contains a vertex of $D_i$. We use induction on the time of the pebble. If $x$ has the pebble at the start or gets it by R1, then $x \in D_i$. Otherwise R3 puts the pebble on $x$. Then $x$ is not an input, and every predecessor of $x$ has a red pebble at that time. Each such predecessor satisfies the claim, by the induction hypothesis (it has its pebble from the start, or it got it earlier in the segment). A path from an input to $x$ ends with an edge $y \to x$, and its part up to $y$ is a path to $y$. So it contains a vertex of $D_i$. Each vertex of $V_i$ has a red pebble in segment $i$, so $D_i$ is a dominator set of $V_i$.

*Property 3.* Let $v$ be in the minimum set of $V_i$. We show that one of three cases holds: $v$ has a red pebble at the end of segment $i$; or R2 puts a blue pebble on $v$ in segment $i$; or $v$ is an input and R1 puts a red pebble on $v$ in segment $i$. At most $S$ vertices fall in the first case. The second and third cases together use distinct I/O moves of the segment, so at most $S$ vertices fall in them. So the minimum set has at most $2S$ vertices. Suppose that the three cases fail. Then $v$ is not an input, because an input of $V_i$ gets its first red pebble by R1 in segment $i$. So R3 puts the first red pebble on $v$ in segment $i$, and no blue pebble is on $v$ before that. The red pebble is removed before the end of the segment, and R2 does not act on $v$ in the segment. So $v$ has no blue pebble after the segment. In the one-shot variant, R3 has been used on $v$, and R1 needs a blue pebble, which only R2 creates. So $v$ never gets a red pebble again. Suppose that $v$ has a successor $w$. A play computes $w$ at some time, because $w$ is an ancestor of an output, and $v$ has a red pebble then. If this happens in segment $i$, then $w$ is in $V_i$, and this contradicts that $v$ is in the minimum set. If it happens later, $v$ has a red pebble after segment $i$, which is impossible. Suppose that $v$ has no successor. Then $v$ is an output, and it needs a blue pebble, which needs a red pebble on $v$ after segment $i$. This is impossible too. So one of the three cases holds.

The segments give a $2S$-partition with $\lfloor q/S \rfloor + 1$ parts, so $H(2S) \le \lfloor q/S \rfloor + 1$ and $q \ge S\lfloor q/S \rfloor \ge S(H(2S) - 1)$. $\square$

**Matrix multiplication.** Let $G$ be the graph of the conventional algorithm for $C = AB$ with $n \times n$ matrices. It has $2n^2$ inputs $a_{ik}$ and $b_{kj}$, $n^3$ product vertices $p_{ijk}$ with predecessors $a_{ik}$ and $b_{kj}$, and for each pair $(i,j)$ a binary tree of $n - 1$ additions that sums the products $p_{ijk}$, $k = 1, \dots, n$. The shape of each tree is arbitrary. The root of the tree is the output $c_{ij}$. Then in the one-shot variant
$$Q(G, S) \ge \frac{n^3}{4\sqrt{2S}} - S = \Omega\!\left(\frac{n^3}{\sqrt{S}}\right).$$
Hong and Kung proved the bound $\Omega(n^3/\sqrt S)$ with recomputation allowed. Here is a proof of the displayed bound by the lemma, in the style of Irony, Toledo and Tiskin. Take a $2S$-partition with $h = H(2S)$ parts. Let $P$ be the set of product vertices of one part $V_i$, with the dominator set $D$ and the minimum set $M_0$. The set $P \cap D$ has at most $2S$ vertices. Take a product $p_{ijk}$ in $P \setminus D$. The path that consists of the edge $a_{ik} \to p_{ijk}$ starts at an input and ends in $V_i$, so it contains a vertex of $D$. This vertex is not $p_{ijk}$, so it is $a_{ik}$. In the same way, $b_{kj} \in D$. So the pairs $(i,k)$ and the pairs $(k,j)$ of the products in $P \setminus D$ are at most $2S$ each. Next, count the pairs $(i,j)$. If $V_i$ contains a vertex of the tree of $c_{ij}$, follow the successors from this vertex up the tree. Every vertex has one successor in the tree. By property 1 the indices of the parts do not decrease along an edge, so once the path leaves $V_i$ it does not come back. The last vertex of the path in $V_i$ has no successor in $V_i$, so it is in $M_0$. Different trees are disjoint, so $P$ meets at most $|M_0| \le 2S$ trees. By the Loomis and Whitney inequality, a set of triples $(i,j,k)$ has at most $\sqrt{\alpha\beta\gamma}$ elements, where $\alpha$, $\beta$, $\gamma$ are the numbers of different pairs $(i,k)$, $(k,j)$, $(i,j)$ among them. So $|P \setminus D| \le \sqrt{(2S)^3}$ and $|P| \le (2S)^{3/2} + 2S \le 2(2S)^{3/2}$. Every one of the $n^3$ products is in some part, so $h \ge n^3 / (2(2S)^{3/2})$. The lemma gives $Q \ge S(h - 1) \ge n^3/(4\sqrt{2S}) - S$. $\square$

For the usual summation order, where $c_{ij}$ accumulates $p_{ij1}, p_{ij2}, \dots$ as a chain (or along any tree that respects the $k$-blocks), the bound is tight. For an arbitrary tree shape, one entry of $C$ may need many partial sums at once, and the schedule below does not apply. The blocked algorithm ([blocked matrix multiplication](/blocked-matrix-multiplication/)) with blocks of $b \times b$, where $3b^2 + O(1) \le S$, makes $O(n^3/\sqrt S + n^2)$ moves. Example: $n = 1024$, $b = 32$, so $S = 3 \cdot 32^2 = 3072$ plus a few pebbles. The algorithm reads $2n^3/b = 67\,108\,864$ values of $A$ and $B$ and writes $n^2 = 1\,048\,576$ values of $C$, so $68\,157\,440$ I/O moves in all. The lower bound above is about $3.42 \times 10^6$. The two differ by a factor of about 20, which is a constant factor.

Ballard, Demmel, Holtz and Schwartz (2012) proved the analogue for Strassen-like algorithms with exponent $\omega_0$: the I/O complexity is $\Omega(n^{\omega_0} / S^{\omega_0/2 - 1})$. For $\omega_0 = 3$ this is the bound above.

**The fast Fourier transform.** Let $n = 2^m$. The graph of the [FFT](/fast-fourier-transform/) has $m + 1$ levels of $n$ vertices. The vertex $(\ell, i)$ at level $\ell < m$ has two outgoing edges, to $(\ell + 1, i)$ and to $(\ell+1, i \oplus 2^{\ell})$, where $\oplus$ is the exclusive or of the binary numbers. Hong and Kung proved
$$Q(G, S) = \Theta\!\left(\frac{n \log n}{\log S}\right).$$
The lower bound has the following outline. A set of vertices of this graph that satisfies properties 2 and 3 of a $2S$-partition has $O(S \log S)$ vertices. The graph has $\Theta(n \log n)$ vertices, so $H(2S) = \Omega(n \log n / (S \log S))$, and the lemma gives the bound. The proof of the set size is in their paper and is not given here. The upper bound has a short proof. Let $g = \lfloor \lg(S - 2) \rfloor$. The $g$ levels from level $\ell$ to level $\ell + g$ split into $n/2^g$ separate butterflies of $2^g$ inputs each. Compute a butterfly with $2^g + 2$ red pebbles, one level at a time: read its $2^g$ inputs, compute, and write its $2^g$ outputs. Each group of $g$ levels moves $2n$ values, and there are $\lceil m/g \rceil$ groups, so the cost is $2n\lceil m/g \rceil$. Example: $n = 2^{20}$ and $S = 2^{10} + 2$. Then $g = 10$ and there are 2 groups, so the cost is $4n = 4\,194\,304$. A plain level-by-level algorithm reads and writes every level, so it costs about $2n\log n = 2 \cdot 20 \cdot 2^{20} = 41\,943\,040$ moves. The quantity $n \log n / \log S$ is $2^{21}$.

**The complexity of computing $Q$.** Computing $Q(G, S)$ exactly is hard. Demaine and Liu (2018) proved that the minimum cost of a red-blue pebbling is PSPACE-complete to compute, and that the problem stays NP-complete when deletions are forbidden. Papp and Wattenhofer (2020) proved that it is NP-hard in the one-shot variant. So the bounds above come from structural arguments such as the $S$-partition lemma, not from a search over plays.

## References
