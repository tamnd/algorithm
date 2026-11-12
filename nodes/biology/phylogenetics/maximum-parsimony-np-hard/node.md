---
tag: 1JE9GH
kind: theorem
slug: maximum-parsimony-np-hard
name: Maximum parsimony is NP-hard
aliases:
- Foulds-Graham theorem
area: biology/phylogenetics
level: advanced
summary: Deciding if some tree explains binary characters with at most k changes is NP-complete (Foulds and Graham 1982), so exact parsimony search does not scale to many taxa.
prereqs: [maximum-parsimony, np-complete, vertex-cover, steiner-tree-problem]
see_also: [fitch-algorithm, camin-sokal-parsimony, dollo-parsimony, wagner-parsimony, parsimony-informative-site, ml-tree-np-hard, msa-np-hardness, apx]
sources:
  - paper: doi:10.1016/S0196-8858(82)80004-3
    title: L. R. Foulds and R. L. Graham, The Steiner problem in phylogeny is NP-complete, Advances in Applied Mathematics 3(1), 1982, 43-49
    locator: the NP-completeness of the Steiner tree problem for binary characters, which is the decision version of maximum parsimony
  - paper: "R. L. Graham and L. R. Foulds, Unlikelihood that minimal phylogenies for a realistic biological study can be constructed in reasonable computational time, Mathematical Biosciences 60, 1982, 133-142"
    locator: the consequences of the NP-completeness result for real phylogenetic studies
  - paper: "William H. E. Day, Computationally difficult parsimony problems in phylogenetic systematics, Journal of Theoretical Biology 103, 1983, 429-438"
    locator: the NP-completeness of further parsimony and compatibility problems
  - paper: doi:10.1016/0025-5564(86)90161-6
    title: William H. E. Day, David S. Johnson and David Sankoff, The computational complexity of inferring rooted phylogenies by parsimony, Mathematical Biosciences 81(1), 1986, 33-42
    locator: the NP-completeness of the Camin-Sokal and Dollo versions of parsimony
  - book: isbn:9780878931774
    title: Joseph Felsenstein, Inferring Phylogenies, Sinauer Associates, 2004
    locator: the discussion of the computational complexity of the search for most parsimonious trees
---

The large [maximum parsimony](/maximum-parsimony/) problem is NP-hard. Its decision version asks if some tree explains a set of characters with at most $k$ changes, and it is [NP-complete](/np-complete/) already for binary characters. Foulds and Graham proved this in 1982 through the link between parsimony and the [Steiner tree problem](/steiner-tree-problem/) in the hypercube. Day, Johnson and Sankoff (1986) proved the same for the rooted versions, [Camin-Sokal](/camin-sokal-parsimony/) and [Dollo](/dollo-parsimony/) parsimony. The score of one fixed tree is easy to compute with [Fitch's algorithm](/fitch-algorithm/), so all of the hardness is in the choice of the tree. This page gives a short proof by a reduction from [vertex cover](/vertex-cover/) that can be checked by hand on small graphs.

## Statement

**Maximum parsimony, decision version.** The input is a matrix of binary characters, with one row per taxon, and an integer $k$. The question is: is there an unrooted binary tree with the taxa at its leaves whose parsimony score, the least total number of changes over all labelings of the internal nodes, is at most $k$?

**Theorem (Foulds and Graham 1982).** This problem is NP-complete. So the large parsimony problem is NP-hard for binary characters, and then also for unordered characters with more states (such as DNA) and for ordered ([Wagner](/wagner-parsimony/)) characters.

**Theorem (Day, Johnson and Sankoff 1986).** The decision versions of Camin-Sokal parsimony and of Dollo parsimony on rooted trees are NP-complete.

The proof below shows the first theorem, and the Camin-Sokal case of the second, from this lemma.

**Lemma.** Let $G$ be a graph with the vertices $1, \ldots, n$ and $m \ge 2$ edges, and let $\tau(G)$ be the size of its smallest vertex cover. Build $m + 1$ taxa with $n$ binary characters: the zero row $0 = 00\cdots0$, and for each edge $\{a, b\}$ the row with 1 in the columns $a$ and $b$ and 0 elsewhere. The parsimony score of the best tree for these taxa is $m + \tau(G)$.

## In plain words

Parsimony asks for the tree that explains the data with the fewest changes. To score one tree is fast. The hard part is the choice of the tree. The theorem says that no method makes this choice fast in all cases, even with two states per character, unless every problem in NP has a fast method.

The proof turns a graph into species. One species has no traits. Each edge of the graph gives a species with two traits, one for each end of the edge. A good tree puts some ancestors with one trait next to the species with no traits, and hangs each edge species below one of them. The traits of those ancestors touch every edge, so they form a vertex cover. A best tree gives a smallest cover, and to find one is a known hard problem.

## Proof

**Membership in NP.** A certificate is a tree. Fitch's algorithm computes its score in time linear in the size of the matrix, and the tree has a size linear in the number of taxa.

**Parsimony is a Steiner problem.** The labels of the nodes are vertices of the hypercube $Q_n$, the graph on $\{0, 1\}^n$ in which two strings are joined when they differ in one place. The number of changes on a tree edge is the [Hamming distance](/hamming-distance/) between its ends. So a labeled tree with the taxa at its leaves is a tree in the Hamming metric that spans the taxa, and its score is its length. In the other direction, take any tree $S$ whose nodes are labeled by strings, that contains the taxa as nodes, and whose length is the sum of the Hamming distances on its edges. It becomes a phylogenetic tree with a score of at most that length: give each taxon that is an internal node a new leaf joined by an edge of length 0, delete the leaves that are not taxa, join the two edges at a node of degree 2 into one edge (by the triangle inequality, this does not add length), and split each node of degree more than 3 with new edges of length 0.

**Upper bound.** Let $C$ be a vertex cover with $|C| = \tau(G)$, and let $e_c$ be the string with a single 1 in column $c$. Take the tree in $Q_n$ with the node $0$, a node $e_c$ for each $c \in C$, an edge from $0$ to each $e_c$, and for each edge $\{a, b\}$ of $G$ an edge from its taxon to $e_c$ for one end $c \in C \cap \{a, b\}$. Each of these edges has length 1, so the length is $|C| + m$. By the previous step, some phylogenetic tree has a score of at most $m + \tau(G)$.

**Lower bound.** Take a phylogenetic tree with a labeling of score $L$. Replace each tree edge by a shortest path in $Q_n$ between its ends. The union of these paths is a connected subgraph of $Q_n$ with at most $L$ edges that contains all the taxa. Let $T'$ be a spanning tree of it. Root $T'$ at $0$, and let $p(y)$ be the parent of a node $y$. The weight of a string is its number of ones, and the weights of a node and its parent differ by exactly 1. The nodes of $T'$ are $0$, the $m$ edge taxa (weight 2), the set $W_1$ of nodes of weight 1, and the set $X$ of the other nodes, which have weight at least 2 and are not taxa. So

$$|E(T')| = |V(T')| - 1 = m + |W_1| + |X|.$$

Let $C_1 = \{c : e_c \in W_1\}$. If the parent of the taxon of an edge has weight 1, it is $e_a$ or $e_b$, so $C_1$ covers that edge. Every other taxon has a parent of weight 3, which is in $X$. Let $Y$ be the set of nodes of weight 3 that are parents of these other taxa. The edge taxa below $y \in Y$ correspond to pairs inside the 3-set $\operatorname{supp}(y)$ of the ones of $y$. Cover them in three cases.

- **The parent of $y$ has weight 2.** Then $p(y)$ is one pair of $\operatorname{supp}(y)$, and it is not a child of $y$. The other two pairs share one element $c$, and $\{c\}$ covers all the edges whose taxa are children of $y$. Charge this one vertex to $y$.
- **$z$ has weight 4 and is the parent of exactly one $y \in Y$.** Two elements of the 3-set $\operatorname{supp}(y)$ cover all three of its pairs. Charge these two vertices to $y$ and $z$.
- **$z$ has weight 4 and is the parent of two or more nodes of $Y$.** All their child taxa are pairs inside the 4-set $\operatorname{supp}(z)$, and any three elements of a 4-set cover all of its six pairs. Charge these three vertices to $z$ and to at least two nodes of $Y$.

Each node of $Y$ is charged once, through its own parent, and each node $z$ of weight 4 is charged at most once, so the charged nodes are distinct elements of $X$. The vertices of the three cases cover every edge not covered by $C_1$, and there are at most $|X|$ of them. So $G$ has a vertex cover of size at most $|W_1| + |X|$, and

$$L \ge |E(T')| = m + |W_1| + |X| \ge m + \tau(G).$$

This proves the lemma. $\square$

**The reduction.** Vertex cover is NP-complete. Map a graph $G$ and a number $t$ to the matrix of the lemma and $k = m + t$. This takes polynomial time, and by the lemma, $G$ has a vertex cover of size at most $t$ if and only if some tree has a score of at most $k$. With membership in NP, the decision version of maximum parsimony is NP-complete for binary characters.

**Other kinds of characters.** A binary character is an ordered character with two states, so Wagner parsimony is NP-hard. For unordered characters with more states, use any two states, for example A and C. A labeling that uses a state that is at no leaf can be changed to one that does not, with no more changes (the [Hartigan](/hartigan-algorithm/) proof shows this), so the score is the same.

**Camin-Sokal parsimony.** Root the trees at the taxon $0$, with all characters ancestral in state 0. In the upper bound, every edge goes from a string to a string with one more 1, so each change is a gain, and the Camin-Sokal score is also $m + \tau(G)$. A Camin-Sokal labeling is also a labeling for unordered parsimony, so no rooted tree has a smaller Camin-Sokal score than $m + \tau(G)$. Dollo parsimony needs another construction, which is in the paper of Day, Johnson and Sankoff. $\blacksquare$

**A small example.** Take the 4-cycle with the edges $\{1, 2\}$, $\{2, 3\}$, $\{3, 4\}$ and $\{4, 1\}$. Here $m = 4$ and $\tau = 2$. The taxa are $t_0 = 0000$, $t_1 = 1100$, $t_2 = 0110$, $t_3 = 0011$ and $t_4 = 1001$. Of the 15 unrooted trees on five taxa, 2 have the score 6, 8 have the score 7 and 5 have the score 8. The two best trees are $(t_0, (t_1, t_4), (t_2, t_3))$, which hangs $t_1$ and $t_4$ below $e_1$ and $t_2$ and $t_3$ below $e_3$, and $(t_0, (t_1, t_2), (t_3, t_4))$, which uses $e_2$ and $e_4$. They match the two smallest vertex covers $\{1, 3\}$ and $\{2, 4\}$. For the triangle, $m = 3$ and $\tau = 2$, and all three trees on the four taxa have the score 5.

## Consequences

- **No exact polynomial method.** Unless P = NP, no algorithm finds a most parsimonious tree in polynomial time. Exact search uses branch and bound, as in [depth-first branch and bound](/depth-first-branch-and-bound/), and practical search uses heuristics: [stepwise addition](/stepwise-addition/), [nearest-neighbor interchange](/nearest-neighbor-interchange/), [subtree pruning and regrafting](/subtree-prune-and-regraft/), [tree bisection and reconnection](/tree-bisection-and-reconnection/) and the [parsimony ratchet](/parsimony-ratchet/).
- **No approximation scheme.** The lower bound of the proof is constructive: from a tree of score $L$ it builds, in polynomial time, a vertex cover of size at most $L - m$. On graphs whose degree is at most $\Delta$, $m \le \Delta \tau(G)$, so the best score is at most $(\Delta + 1)\tau(G)$. This is an L-reduction from vertex cover on graphs of bounded degree, which is [APX](/apx/)-hard, so maximum parsimony on binary characters is APX-hard: unless P = NP, no polynomial algorithm comes within a factor $1 + \varepsilon$ of the best score for every $\varepsilon > 0$.
- **A factor of 2 is easy.** A [minimum spanning tree](/minimum-spanning-tree/) of the taxa under the Hamming distance has at most twice the length of the best Steiner tree, and the conversion of the proof turns it into a phylogenetic tree with a score of at most that length.
- **The hard part is the tree.** The [small parsimony](/small-parsimony/) problem on a fixed tree takes linear time for each character. Likelihood has the same split: the score of one tree is easy with [Felsenstein's pruning](/felsenstein-pruning/), and the search over trees is [NP-hard](/ml-tree-np-hard/).

## Tightness

- **Very simple characters stay hard.** In the reduction, each taxon has at most two ones, and column $c$ has its ones in as many taxa as the degree of vertex $c$. Vertex cover stays NP-complete on graphs of degree at most 3, so the problem stays NP-complete when every character has state 1 in at most 3 taxa. With state 1 in at most one taxon, a character is not [informative](/parsimony-informative-site/) and the problem is trivial.
- **Few taxa.** With a fixed number of taxa, there is a fixed number of trees, and each is scored in linear time.
- **Few characters.** With a fixed number of characters with a fixed number of states, there is a fixed number of different rows. Equal rows can be joined by edges of length 0, so the problem has a fixed size after a linear pass.
- **Perfect data.** Each binary character that is not constant needs at least one change. The question whether a tree reaches this bound, one change per character, is the [perfect phylogeny](/perfect-phylogeny/) problem, which [Gusfield's algorithm](/gusfield-perfect-phylogeny/) solves in $O(nm)$ time for $n$ taxa and $m$ binary characters.

## History

Camin and Sokal (1965) and the Wagner methods of Kluge and Farris (1969) and Farris (1970) already searched for good trees with heuristics, because the number of trees grows too fast for complete search. Foulds and Graham (1982) proved that the problem is NP-complete, under the title "The Steiner problem in phylogeny is NP-complete", and in a second paper of the same year Graham and Foulds discussed what this means for real studies. Day (1983) extended the list of hard parsimony problems, and Day, Johnson and Sankoff (1986) proved the hardness of the rooted Camin-Sokal and Dollo versions. The reduction on this page, from vertex cover with a zero row and one taxon per edge, is a short proof for binary characters. It is not the original construction of Foulds and Graham.

## References
