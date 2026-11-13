---
tag: R50TV2
kind: problem
slug: split-network-construction
name: Split network construction
area: biology/phylogenetics
level: advanced
summary: Given weighted splits of a taxon set, build a splits graph, in which each split is a class of parallel edges whose removal cuts the graph into its two sides.
prereqs: [split-system, splits-of-a-tree, phylogenetic-network]
see_also: [split-decomposition, neighbor-net, tree-metric, four-point-condition, phylogenetic-tree, planar-graph, robinson-foulds-distance]
sources:
  - paper: "Andreas W. M. Dress and Daniel H. Huson, Constructing splits graphs, IEEE/ACM Transactions on Computational Biology and Bioinformatics 1(3), 2004"
    title: Andreas W. M. Dress and Daniel H. Huson, Constructing splits graphs
    locator: the definition of splits graphs, the convex hull algorithm, and the planar drawing of circular split systems
  - paper: doi:10.1016/1055-7903(92)90021-8
    title: Hans-Jürgen Bandelt and Andreas W. M. Dress, Split decomposition, a new and useful approach to phylogenetic analysis of distance data, Molecular Phylogenetics and Evolution 1(3), 1992, pages 242 to 252
    locator: weakly compatible split systems from distances, and their drawing as networks
  - paper: "Peter Buneman, The recovery of trees from measures of dissimilarity, in Mathematics in the Archaeological and Historical Sciences, Edinburgh University Press, 1971"
    title: Peter Buneman, The recovery of trees from measures of dissimilarity
    locator: the splits of a tree and the graph built from consistent choices of sides, later called the Buneman graph
  - book: isbn:9780521755962
    title: Daniel H. Huson, Regula Rupp and Celine Scornavacca, Phylogenetic Networks, Concepts, Algorithms and Applications, Cambridge University Press, 2010
    locator: the chapters on splits and unrooted networks, with splits graphs, median networks and the algorithms that draw them
---

Split network construction asks for a picture of a set of splits that may conflict with each other. A [phylogenetic tree](/phylogenetic-tree/) shows a set of compatible splits, one edge per split. When the splits are not compatible, as in the output of [split decomposition](/split-decomposition/) or [NeighborNet](/neighbor-net/), no tree can show them all. A *splits graph* shows each split as a class of parallel edges of the same length: removing the edges of the class cuts the graph into two parts, which hold the two sides of the split. Two incompatible splits then form a parallelogram, a box in the drawing. The problem is to build such a graph, small and readable, and for circular split systems, drawn in the plane without crossings.

## In plain words

A tree draws each split as one branch. If you cut that branch, the taxa fall into the two groups of the split. Now suppose you also want to show a split that crosses an existing one, such as $ab \mid cd$ and $ac \mid bd$ at once. A single branch cannot do it. So the picture uses a band of parallel branches for each split. Cutting the whole band separates its two groups.

Two crossing splits give a rectangle: two opposite sides belong to one split and the other two sides to the other split. Many crossing splits give a web of such boxes. The length of the branches in a band is the weight of the split, so the distance along the graph between two taxa is the sum of the weights of the splits that separate them.

## Definition

**Input.** A finite set $X$ of $n$ taxa and a set $\mathcal{S}$ of splits $A \mid B$ of $X$, usually with a positive weight $w(S)$ for each split. It is common to include every trivial split $\{x\} \mid X \setminus \{x\}$, so that each taxon gets a pendant edge.

**Output.** A splits graph for $\mathcal{S}$: a connected graph $G$ with a map from $X$ to its vertices, and a labeling of its edges by splits, such that:

- for each split $S$, removing the edges labeled $S$ leaves exactly two connected components, which contain the taxa of the two sides of $S$;
- every shortest path in $G$ uses each label at most once, so that $G$ embeds in a hypercube with one dimension per split, and the edges of one label are parallel.

With edge lengths $w(S)$, the path distance between taxa $x$ and $y$ is $\sum w(S)$ over the splits that separate them. The goal is a graph with few vertices and edges, and for circular systems a [planar](/planar-graph/) drawing.

**The Buneman graph.** The canonical splits graph is the *median network* or Buneman graph. Its vertices are the choices of one side $\phi(S)$ for each split $S$ such that any two chosen sides intersect, and two vertices are adjacent when they differ for exactly one split. A taxon $x$ sits at the vertex that chooses, for each split, the side that holds $x$. The Buneman graph is a splits graph for $\mathcal{S}$, and for compatible splits it is the tree.

## Variants

- **Compatible splits.** If every two splits are compatible, the splits graph is the tree with these splits, and it has one edge per split.
- **Circular split systems.** The taxa have a circular order such that each side is an interval of the circle. Such systems always have a planar splits graph, which the equal-angle and convex hull methods draw. The output of [NeighborNet](/neighbor-net/) is circular.
- **Weakly compatible systems.** The output of [split decomposition](/split-decomposition/) is weakly compatible, and it has at most $\binom{n}{2}$ splits. Such systems need not be circular, and their splits graphs need not be planar.
- **Median networks from sequences.** For binary characters, each character defines a split, and the median network of these splits is the median network of the sequences, used for mitochondrial haplotypes. The median-joining method keeps only part of it.
- **Outline drawings.** For large circular systems, drawing only the outer boundary of the planar splits graph gives a picture with far fewer vertices.

## Examples

**A rectangle.** Let $X = \{a, b, c, d, e\}$ and let $\mathcal{S}$ consist of the trivial splits of weight 1, the split $ab \mid cde$ of weight 3 and the split $bc \mid ade$ of weight 2. The two nontrivial splits are incompatible, because all four intersections $ab \cap bc = \{b\}$, $ab \cap ade = \{a\}$, $cde \cap bc = \{c\}$ and $cde \cap ade = \{d, e\}$ are nonempty. So the Buneman graph has four inner vertices, one for each choice of sides, and they form a rectangle:

| inner vertex | side of $ab \mid cde$ | side of $bc \mid ade$ | taxa |
|---|---|---|---|
| $v_1$ | $ab$ | $bc$ | $b$ |
| $v_2$ | $ab$ | $ade$ | $a$ |
| $v_3$ | $cde$ | $ade$ | $d$, $e$ |
| $v_4$ | $cde$ | $bc$ | $c$ |

The edges $v_1 v_4$ and $v_2 v_3$ have the label $ab \mid cde$ and length 3, and the edges $v_1 v_2$ and $v_4 v_3$ have the label $bc \mid ade$ and length 2. Each taxon has a pendant edge of length 1. Removing the two edges of $ab \mid cde$ leaves $\{v_1, v_2\}$ with $a, b$ and $\{v_3, v_4\}$ with $c, d, e$, as required. The distance from $a$ to $c$ along the graph is $1 + 3 + 2 + 1 = 7$, which is the sum of the weights of the four splits that separate $a$ from $c$. The order $a, b, c, d, e$ around the circle makes both splits intervals, so the system is circular, and the rectangle is planar.

**A cube.** Let the taxa be the eight binary words of length 3, and let split $i$ separate the words by their $i$-th digit. For every choice of sides of the three splits, some word lies on all three sides, so all $2^3 = 8$ choices are vertices of the Buneman graph, and the graph is the cube. With $k$ such splits on $2^k$ taxa, the Buneman graph is the $k$-dimensional hypercube, which shows that the general problem can need exponentially many vertices. These three splits are not weakly compatible: the words $000$, $011$, $101$ and $110$, with $000$ in the role of $t_0$, break the condition.

## Known algorithms

| method | input | output | cost |
|---|---|---|---|
| tree from compatible splits | compatible splits | the tree | $O(n k)$ for $k$ splits |
| Buneman graph | any splits | the median network | proportional to its size, which can be exponential in $k$ |
| convex hull algorithm (Dress and Huson 2004) | any splits, added one at a time | a splits graph | polynomial in the size of the output |
| equal-angle algorithm (Dress and Huson 2004) | circular splits | a planar splits graph with coordinates | polynomial in $n$ and $k$ |

The convex hull algorithm starts with a single vertex that holds all taxa. To add a split $A \mid B$, it takes the convex hull of the vertices that hold the taxa of $A$, the smallest set closed under shortest paths, copies this hull, moves the taxa of $A$ to the copy, and joins each vertex of the hull to its copy by an edge with the new label. Added in a circular order, the splits of a circular system give a planar graph, and the equal-angle algorithm then places the edges of each split at one fixed angle, so that parallel edges are drawn parallel.

## Bounds

- **Compatible case.** A tree needs exactly one edge per split, so the output size is $O(n)$ for $n$ taxa.
- **Circular and weakly compatible case.** There are at most $\binom{n}{2}$ splits, so the input is polynomial. Planar splits graphs of circular systems have polynomial size.
- **General case.** The Buneman graph of $k$ splits can have $2^k$ vertices, as in the cube example. So a method that always builds the full median network is exponential in the worst case.
- **Lower bound for any splits graph.** Each split needs at least one edge. A split drawn by a single edge $e$ is compatible with every other split: the two parts of $G - e$ are closed under shortest paths, so the side of any other split that does not hold $e$ lies inside one of them. So a split that is incompatible with another one needs at least two edges.

## Reductions

- **Partial cubes.** A graph is a splits graph of some split system exactly when it embeds in a hypercube so that graph distances equal Hamming distances, a partial cube. The splits are its classes of parallel edges.
- **From distances.** [Split decomposition](/split-decomposition/) and [NeighborNet](/neighbor-net/) turn a distance matrix into weighted splits, so a distance matrix can be drawn as a network by composing them with this problem.
- **To trees.** Keeping only a largest compatible subset of the splits gives a tree. Choosing that subset with the largest weight is a maximum weight compatible set problem.
- **Distances.** The path distance in a splits graph with edge lengths is the sum of weighted split metrics, which is a [tree metric](/tree-metric/) exactly when the splits are compatible.

## Applications

- **Exploring conflicting signal.** Splits graphs show where the data support a tree and where they do not, for example through recombination, hybridization or noise.
- **Population data.** Median networks of haplotypes show how mitochondrial or Y chromosome sequences are related within a species.
- **Language and manuscript data.** Distances between languages or copies of a text are often drawn as NeighborNet splits graphs, because borrowing creates conflicting signal.
- **Software.** SplitsTree builds and draws splits graphs from distances, sequences and trees.

## References
