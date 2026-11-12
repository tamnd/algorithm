---
tag: P7VKS4
kind: theorem
slug: four-gamete-condition
name: Four-gamete condition
aliases:
- four-gamete test
area: biology/phylogenetics
level: core
summary: A binary character matrix has an unrooted perfect phylogeny if and only if no two columns show all four pairs 00, 01, 10 and 11.
prereqs: [perfect-phylogeny, splits-of-a-tree]
see_also: [gusfield-perfect-phylogeny, character-compatibility, ancestral-recombination-graph-inference, ancestral-recombination-graph, phylogenetic-tree, split-system]
sources:
  - paper: "Peter Buneman, The recovery of trees from measures of dissimilarity, in F. R. Hodson, D. G. Kendall and P. Tautu (eds), Mathematics in the Archaeological and Historical Sciences, Edinburgh University Press, 1971"
    title: Peter Buneman, The recovery of trees from measures of dissimilarity, 1971
    locator: pp. 387 to 395, pairwise compatible splits come from one tree
  - paper: doi:10.1016/0025-5564(76)90035-3
    title: George F. Estabrook, C. S. Johnson Jr. and F. R. McMorris, A mathematical foundation for the analysis of cladistic character compatibility, Mathematical Biosciences 29(1-2), 1976
    locator: pp. 181 to 187, pairwise compatibility of binary characters implies joint compatibility
  - paper: doi:10.1002/net.3230210104
    title: Dan Gusfield, Efficient algorithms for inferring evolutionary trees, Networks 21(1), 1991
    locator: pp. 19 to 28, the rooted pair condition and the O(nm) test
  - book: isbn:9780198509424
    title: Charles Semple and Mike Steel, Phylogenetics, Oxford University Press, 2003
    locator: Section 3.1 (the splits-equivalence theorem) and Chapter 4 (compatibility of binary characters)
  - book: isbn:9780521585194
    title: Dan Gusfield, Algorithms on Strings, Trees, and Sequences, Cambridge University Press, 1997
    locator: Chapter 17, the section on the perfect phylogeny problem for binary characters
  - paper: doi:10.1093/genetics/111.1.147
    title: Richard R. Hudson and Norman L. Kaplan, Statistical properties of the number of recombination events in the history of a sample of DNA sequences, Genetics 111(1), 1985
    locator: pp. 147 to 164, the four gametic types as evidence of recombination and the lower bound built on them
---

The four-gamete condition says when a matrix of binary characters fits on a tree in which each character changes only one time. The test is pairwise: the matrix fits if and only if no two columns show all four combinations 00, 01, 10 and 11 in their rows. So a property of the whole matrix follows from properties of its pairs of columns. The theorem is the basis of the [perfect phylogeny](/perfect-phylogeny/) problem for binary characters, of [Gusfield's algorithm](/gusfield-perfect-phylogeny/), of [character compatibility](/character-compatibility/) methods, and of the first lower bounds on the number of recombinations in a sample of DNA sequences.

## Statement

Let $M$ be an $n \times m$ matrix with entries in $\{0, 1\}$. Row $i$ is a taxon, or in population genetics a haplotype, and column $c$ is a binary character, or a site. Two columns $a$ and $b$ *show four gametes* if the set $\{\, (M[i][a], M[i][b]) : 1 \le i \le n \,\}$ has all four elements $(0,0)$, $(0,1)$, $(1,0)$ and $(1,1)$.

An *unrooted perfect phylogeny* for $M$ is a tree $T$ whose nodes carry vectors in $\{0,1\}^m$, such that every row of $M$ is the vector of some node, and every column changes its value on at most one edge of $T$. Equivalently, for each column $c$, the nodes with value 0 at $c$ form a connected subtree, and so do the nodes with value 1. A row may sit at an internal node; attaching a new leaf with the same vector turns any such tree into one with the rows at the leaves.

**Theorem (four-gamete condition).** $M$ has an unrooted perfect phylogeny if and only if no two columns of $M$ show four gametes.

**Theorem (rooted form).** $M$ has a perfect phylogeny in which some node has the all-zero vector (the ancestor) if and only if no two columns show all three of $(0,1)$, $(1,0)$ and $(1,1)$. Equivalently, the sets $O_c = \{\, i : M[i][c] = 1 \,\}$ are pairwise disjoint or nested.

The rooted form is the unrooted form applied to $M$ with an extra all-zero row, because that row adds the pair $(0,0)$ to every pair of columns.

## In plain words

Think of each column as a yes or no trait. If a trait arose one time on a tree and was never lost, it cuts the tree into two parts at one branch: the taxa with the trait on one side and the taxa without it on the other side. Take two such traits. Their two cuts split the tree into at most three pieces, and each piece has one fixed combination of the two traits. So at most three of the four combinations can occur.

The surprise is the converse. If every pair of traits shows at most three combinations, then one tree fits all the traits at the same time. You never need to look at three or more columns together.

## Proof

**Only if.** Let $T$ be an unrooted perfect phylogeny for $M$, and let $a$ and $b$ be two columns. If a column never changes, it is constant on $T$, and the pair shows at most two combinations. Otherwise, let $e_a$ and $e_b$ be the edges where $a$ and $b$ change; they may be the same edge. Deleting $e_a$ and $e_b$ from $T$ leaves at most three connected components. Inside one component, neither column changes its value, so every node of the component has the same pair $(a, b)$. Every row is the vector of a node, so the rows show at most three pairs. $\square$

**If.** Assume that no two columns show four gametes.

*Step 1: make row 1 all zero.* Let $M'$ be $M$ with each column $c$ complemented where $M[1][c] = 1$. Complementing column $a$ swaps the pairs $(0, x)$ and $(1, x)$, so $M'$ also has no pair of columns with four gametes. A tree for $M'$ gives a tree for $M$: complement coordinate $c$ in every node vector, for the same columns. This does not move the edge on which a column changes.

*Step 2: the sets nest.* Row 1 of $M'$ is all zero, so every pair of columns of $M'$ shows $(0,0)$. So no pair shows all three of $(0,1)$, $(1,0)$ and $(1,1)$. Let $O_c$ be the set of rows with a 1 in column $c$ of $M'$. For two columns $a$ and $b$: if no row shows $(1,1)$, then $O_a \cap O_b = \emptyset$. If no row shows $(1,0)$, then $O_a \subseteq O_b$. If no row shows $(0,1)$, then $O_b \subseteq O_a$. So the family $\mathcal{F}$ of distinct nonempty sets $O_c$ is laminar: any two of its sets are disjoint or nested.

*Step 3: build the tree.* The sets of $\mathcal{F}$ that contain a fixed set $S$ all meet in $S$, so they are nested and form a chain. Make a node $r$ and a node for each $S \in \mathcal{F}$. The parent of $S$ is the smallest set of $\mathcal{F}$ that strictly contains $S$, or $r$ if there is none. Each parent step goes to a strictly larger set, so this graph is a tree rooted at $r$. Give node $S$ the vector $x_S$ with $x_S[c] = 1$ if and only if $S \subseteq O_c$, and give $r$ the all-zero vector.

*Step 4: the rows are nodes.* For a row $i$, the sets of $\mathcal{F}$ that contain $i$ form a chain. Let $S_i$ be the smallest of them, or $r$ if there is none. If $M'[i][c] = 1$, then $O_c$ is in the chain, so $S_i \subseteq O_c$ and $x_{S_i}[c] = 1$. If $x_{S_i}[c] = 1$, then $i \in S_i \subseteq O_c$, so $M'[i][c] = 1$. So row $i$ is the vector of node $S_i$. Row 1 is in no set, so it is the vector of $r$.

*Step 5: each column changes on one edge.* Fix a column $c$ with $O_c \neq \emptyset$. The nodes with value 1 at $c$ are the sets $S \in \mathcal{F}$ with $S \subseteq O_c$. Each such $S$ is $O_c$ or lies below $O_c$: the parent steps from $S$ visit the whole chain of sets that contain $S$, in increasing order, and $O_c$ is in that chain. Conversely, every node below $O_c$ is a subset of $O_c$. So the 1-nodes of $c$ are exactly the subtree under node $O_c$, and $c$ changes only on the edge above it. A zero column never changes. So the tree is a perfect phylogeny for $M'$, and by step 1 it gives one for $M$. $\blacksquare$

The rooted form follows from steps 2 to 5 directly: if the sets $O_c$ of $M$ are laminar, the tree of step 3 has the all-zero vector at $r$. Conversely, if a tree with an all-zero node exists, root it there. Then each $O_c$ is the set of rows below the change edge of $c$, and two such sets are disjoint or nested.

## Consequences

- **A polynomial test.** Checking all pairs takes $O(nm^2)$ time. [Gusfield's algorithm](/gusfield-perfect-phylogeny/) decides the same question and builds the tree in $O(nm)$ time, by sorting the columns as binary numbers so that it needs only one parent check per column.
- **Splits.** A binary character is a split of the rows into the 0-rows and the 1-rows. Two characters pass the test if and only if their splits are compatible, which means that one of the four intersections of their parts is empty. So the theorem is the character form of the splits-equivalence theorem of Buneman: a set of splits is the split set of a tree if and only if its splits are pairwise compatible. See [splits of a tree](/splits-of-a-tree/).
- **Character compatibility.** Since compatibility of binary characters is pairwise, the largest set of characters with a perfect phylogeny is a largest clique of the graph whose vertices are the columns and whose edges join compatible pairs. This is the basis of [character compatibility](/character-compatibility/) methods.
- **Evidence of recombination.** Under the infinite sites model, each site mutates at most one time, so the history of a region without recombination is a perfect phylogeny. Two sites that show four gametes prove that at least one recombination (or a repeated mutation) happened between them. Hudson and Kaplan built their lower bound $R_M$ on the number of recombinations from such pairs. See [ancestral recombination graph inference](/ancestral-recombination-graph-inference/).

**A worked example.** Take five rows and four columns.

| row | $a$ | $b$ | $c$ | $d$ |
|---|---|---|---|---|
| 1 | 0 | 1 | 1 | 0 |
| 2 | 0 | 1 | 0 | 0 |
| 3 | 1 | 0 | 1 | 1 |
| 4 | 1 | 0 | 1 | 0 |
| 5 | 0 | 0 | 1 | 0 |

Each of the six pairs shows exactly three gametes. Row 1 has a 1 in columns $b$ and $c$, so step 1 complements them. In $M'$, the rows are $0000$, $0010$, $1101$, $1100$ and $0100$. The sets are $O_a = \{3, 4\}$, $O_b = \{3, 4, 5\}$, $O_c = \{2\}$ and $O_d = \{3\}$. They nest as $\{3\} \subset \{3, 4\} \subset \{3, 4, 5\}$, and $\{2\}$ is disjoint from the others. The tree of step 3 is the path $2 - 1 - 5 - 4 - 3$, where the five nodes carry the five rows, and the four edges are labeled $c$, $b$, $a$ and $d$, in this order. In the original matrix, row 2 is $0100$ and row 1 is $0110$, so only $c$ changes on the first edge. In the same way only $b$ changes from row 1 to row 5 ($0010$), only $a$ from row 5 to row 4 ($1010$), and only $d$ from row 4 to row 3 ($1011$).

Now change row 5 to $0011$. Then columns $a$ and $d$ show $00$ (row 1), $11$ (row 3), $10$ (row 4) and $01$ (row 5). So there is no perfect phylogeny.

## Tightness

- **Four rows are needed.** A matrix with at most three rows shows at most three pairs in any two columns, so it always has a perfect phylogeny. The matrix with rows $00$, $01$, $10$ and $11$ has none. It is the smallest example.
- **The rooted form needs three gametes, not four.** The rows $01$, $10$ and $11$ show three gametes, so they have an unrooted perfect phylogeny: the path $01 - 11 - 10$. They have no rooted one with the all-zero ancestor, because $O_1 = \{2, 3\}$ and $O_2 = \{1, 3\}$ overlap without nesting.
- **Binary characters only.** For characters with three or more states, pairwise compatibility does not imply that all characters fit on one tree. The [character compatibility](/character-compatibility/) page gives a small example. When the number of states is not bounded, the general [perfect phylogeny](/perfect-phylogeny/) problem is NP-complete.
- **Complete data only.** With unknown entries the pairwise test fails too. In the matrix with rows $011$, $?10$, $101$, $1?0$ and $001$, each pair of columns has a way to fill its unknown entries without four gametes. But columns 1 and 2 need the first unknown to be 0, while columns 1 and 3 need it to be 1. So no single filling works for all three columns.

The tests of [Gusfield's algorithm](/gusfield-perfect-phylogeny/) compare the pairwise test with a brute force search over all unrooted binary trees on up to six distinct rows, on 1200 random matrices, and they agree on all of them.

## History

Buneman proved in 1971 that pairwise compatible splits of a set come from one tree, which is the same statement for splits. Estabrook, Johnson and McMorris proved in 1976 that a set of binary characters is jointly compatible when it is pairwise compatible, in the language of cladistic character compatibility. In population genetics, the pairs of sites with all four gametic types became the standard sign of recombination, and Hudson and Kaplan used them in 1985 to bound the number of recombination events in a sample. Gusfield gave the linear-time algorithm in 1991, for matrices with an all-zero ancestor, and reduced the unrooted case to it. The name "four-gamete test" comes from population genetics, where a row is a gamete or haplotype.

## References
