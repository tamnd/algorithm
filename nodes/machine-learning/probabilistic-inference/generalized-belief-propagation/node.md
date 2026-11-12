---
tag: 7XZC5Z
kind: algorithm
slug: generalized-belief-propagation
name: Generalized belief propagation
aliases:
- region-based belief propagation
- Kikuchi approximation
- GBP
- parent-to-child algorithm
area: machine-learning/probabilistic-inference
level: research
summary: "Message passing between regions (clusters of variables) of a region graph. Its fixed points are the stationary points of the Kikuchi free energy, which generalizes the Bethe one."
solves: [marginal-inference]
model: real-ram
complexity:
  vars: {t: the number of sweeps, g: the number of edges of the region graph, k: the largest number of states of a variable, w: the largest number of variables in a region, s: the largest number of messages and factors in one update}
  time: {worst: "O(t g s k^w)"}
  space: {extra: "O(g k^w)"}
properties: {deterministic: true, exact: false, online: false, recursive: false}
history:
  year: 2001
  people: [Jonathan S. Yedidia, William T. Freeman, Yair Weiss, Ryoichi Kikuchi]
  note: Yedidia, Freeman and Weiss (NIPS 2000, published 2001) linked BP fixed points to the Bethe free energy and built generalized BP from the cluster variation method of Kikuchi (1951). Their 2005 paper gave region graphs and the parent-to-child algorithm.
prereqs: [loopy-belief-propagation, bethe-free-energy]
see_also: [junction-tree-algorithm, tree-decomposition, residual-belief-propagation, tree-reweighted-belief-propagation, expectation-propagation, mean-field-approximation, ising-model, markov-random-field]
sources:
  - paper: "Jonathan S. Yedidia, William T. Freeman and Yair Weiss, Generalized belief propagation, Advances in Neural Information Processing Systems 13 (NIPS 2000), MIT Press, 2001"
    title: Yedidia, Freeman and Weiss 2001
    locator: "the Kikuchi free energy, generalized BP on clusters, and the experiments on square lattices where it is much more accurate than BP"
  - paper: doi:10.1109/TIT.2005.850085
    title: "Jonathan S. Yedidia, William T. Freeman and Yair Weiss, Constructing free-energy approximations and generalized belief propagation algorithms, IEEE Transactions on Information Theory 51(7), 2005, pages 2282 to 2312"
    locator: "region graphs, counting numbers, the cluster variation method, the parent-to-child algorithm with its sets N(P, R) and D(P, R), and the equivalence of its fixed points with the stationary points of the region-based free energy"
  - paper: doi:10.1103/PhysRev.81.988
    title: "Ryoichi Kikuchi, A theory of cooperative phenomena, Physical Review 81(6), 1951"
    locator: the cluster variation method for lattice models
  - paper: doi:10.1561/2200000001
    title: "Martin J. Wainwright and Michael I. Jordan, Graphical models, exponential families, and variational inference, Foundations and Trends in Machine Learning 1(1-2), 2008"
    locator: "Chapter 4 (Kikuchi and hypertree-based approximations, and generalized belief propagation)"
  - paper: doi:10.1162/08997660260028674
    title: "Alan L. Yuille, CCCP algorithms to minimize the Bethe and Kikuchi free energies: convergent alternatives to belief propagation, Neural Computation 14(7), 2002"
    locator: double-loop algorithms that are guaranteed to converge to a stationary point of the Kikuchi free energy
---

Generalized belief propagation (GBP) passes messages between *regions*, sets of variables, instead of between single variables and factors. The regions and their overlaps form a region graph, and each region has a counting number that says how much its entropy and energy count in an approximate free energy. With the regions of the cluster variation method, this is the Kikuchi free energy, and the fixed points of GBP are its stationary points, as the fixed points of [loopy belief propagation](/loopy-belief-propagation/) are those of the [Bethe free energy](/bethe-free-energy/). With larger regions, GBP holds many of the short loops that make loopy BP wrong, so on grids it is often far more accurate. It is exact when the regions form a junction tree. It was introduced by Yedidia, Freeman and Weiss.

## In plain words

Loopy belief propagation lets single variables talk to each other. When the graph has many short loops, as a grid does, the messages go around the loops and the answer is off.

Generalized belief propagation lets groups of variables talk instead. Each group handles all the short loops inside it exactly. The groups overlap, and to avoid counting the overlaps twice, each overlap gets a correction weight, which can be negative. Messages go from a big group to each smaller overlap below it. The rule for each message is chosen so that, when the messages stop changing, any two groups agree about the variables they share. With well-chosen groups the answer is much closer to the truth, and with groups that form a tree of clusters it is exact. The cost grows quickly with the size of the groups.

## The problem

**The model.** A positive distribution on a [factor graph](/factor-graph/): $p(x) = \frac{1}{Z} \prod_a f_a(x_a)$. The query is approximate marginals, as for loopy BP.

**Regions and counting numbers.** A region $R$ is a set of variables. Its factors $A_R$ are the factors whose variables all lie in $R$, and $f_R(x_R) = \prod_{a \in A_R} f_a(x_a)$. A region graph is a set of regions with directed edges from a parent $P$ to a child $R \subset P$, and a counting number $c_R$ for each region. It is *valid* if, for each variable and for each factor, the counting numbers of the regions that contain it add up to 1.

**The cluster variation method (CVM).** Choose a set of outer regions such that each factor lies in at least one of them. Add all intersections of regions, again and again, until the set is closed under intersection. Set $c_R = 1$ for the outer regions and

$$c_R = 1 - \sum_{S \supsetneq R} c_S$$

for the others. Draw an edge from each region to each region just below it (a subset with no region in between). This region graph is valid.

**The Kikuchi free energy.** For beliefs $b_R$ over the regions,

$$F_K(b) = \sum_R c_R \sum_{x_R} b_R(x_R) \log \frac{b_R(x_R)}{f_R(x_R)},$$

to be minimized subject to normalization and to the consistency $\sum_{x_{P \setminus R}} b_P = b_R$ on the edges. If the outer regions are the factors and the smaller regions are the single variables, then $c_i = 1 - d_i$ and $F_K$ is the Bethe free energy. If the region graph is a junction tree, so that $p = \prod_R p_R^{c_R}$, then $F_K$ at the exact marginals is $-\log Z$.

**The 3 by 3 grid.** With the four $2 \times 2$ squares (plaquettes) as outer regions, the intersections are the four inner edges $\{1, 4\}$, $\{3, 4\}$, $\{4, 5\}$, $\{4, 7\}$ (with the variables numbered row by row from 0), and their intersection is the center $\{4\}$. The counting numbers are $1$ for the squares, $1 - 2 = -1$ for the edges and $1 - (4 - 4) = 1$ for the center. Every 4-cycle of the grid is inside a region.

## The algorithm

Write $E(R)$ for $R$ and all its descendants in the region graph. The parent-to-child algorithm has one message $m_{P \to R}(x_R)$ for each edge. The belief of a region uses the messages that enter $R$ or one of its descendants from outside $E(R)$:

$$b_R(x_R) \propto f_R(x_R) \prod_{(I, J) \in M(R)} m_{I \to J}(x_J), \qquad M(R) = \{(I, J) : J \in E(R),\ I \notin E(R)\}.$$

The message update comes from asking that $\sum_{x_{P \setminus R}} b_P = b_R$. Messages that appear on both sides cancel, and what remains is

$$m_{P \to R}(x_R) \propto \frac{\sum_{x_{P \setminus R}} \prod_{a \in A_P \setminus A_R} f_a(x_a) \prod_{(I, J) \in N(P, R)} m_{I \to J}(x_J)}{\prod_{(I, J) \in D(P, R)} m_{I \to J}(x_J)},$$

where $N(P, R)$ holds the edges $(I, J)$ with $J \in E(P) \setminus E(R)$ and $I \notin E(P)$, and $D(P, R)$ holds the edges $(I, J)$ with $J \in E(R)$ and $I \in E(P) \setminus E(R)$, other than $(P, R)$ itself. The numerator collects the messages into the part of the graph below $P$ that $R$ does not see; the denominator removes the messages that $R$ gets from inside the part below $P$, which would otherwise be counted twice.

```pseudo id=main
GBP(factor graph, outer regions, λ, ε, T)
L1  build the CVM region graph: regions closed under intersection, counting numbers c_R, edges, and the sets M(R), N(P, R), D(P, R)
L2  m_{P→R} ← uniform, for every edge
L3  for sweep t ← 1 to T do (δ ← 0)
L4      for each edge (P, R), those into larger children first: m' ← the parent-to-child update of m_{P→R}, with the newest messages
L5          δ ← max(δ, max |m' − m_{P→R}|)
L6          m_{P→R} ← normalize((1 − λ) m' + λ m_{P→R})
L7      if δ < ε then return the beliefs b_R, "converged"
L8  return the beliefs b_R, "not converged"
```

The schedule is sequential: each update uses the newest values of the other messages. The single-variable marginals come from the smallest region that holds each variable. At a fixed point, all regions that hold it agree.

## Example

Take an Ising model on the $3 \times 3$ grid, spins $s_i \in \{-1, +1\}$, $p(s) \propto \exp(\sum_i h_i s_i + \sum_{(i,j)} J_{ij} s_i s_j)$, with the fields drawn uniformly from $[-0.5, 0.5]$ and the 12 couplings uniformly from $[-1, 1]$ (seed 5). The fields are $h = (0.123, 0.242, 0.295, 0.442, 0.240, 0.422, -0.471, -0.034, 0.443)$. The exact $\log Z$ is $8.50493$, from the sum over all 512 states.

GBP on the plaquette region graph with $\lambda = 0.5$ reaches $\delta < 10^{-10}$ after 70 sweeps of the 12 messages. GBP on the region graph of edges and single variables is exactly loopy BP.

| spin | 0 | 1 | 2 | 3 | 4 | 5 | 6 | 7 | 8 |
|---|---|---|---|---|---|---|---|---|---|
| exact $p(s_i = +1)$ | 0.6260 | 0.6408 | 0.5928 | 0.7516 | 0.3951 | 0.6949 | 0.2420 | 0.5118 | 0.7460 |
| GBP, plaquettes | 0.6260 | 0.6408 | 0.5928 | 0.7516 | 0.3951 | 0.6949 | 0.2420 | 0.5118 | 0.7460 |
| loopy BP | 0.6225 | 0.6336 | 0.5883 | 0.7301 | 0.4057 | 0.6926 | 0.2680 | 0.5110 | 0.7459 |

The largest error of GBP is $4.9 \times 10^{-6}$; that of loopy BP is $0.026$. The free energy estimates are $-F_K = 8.50494$ for the plaquettes and $-F_{\mathrm{Bethe}} = 8.55673$ for loopy BP. On five seeded grids of this kind, the largest error of plaquette GBP was between $5 \times 10^{-6}$ and $1.6 \times 10^{-4}$, and that of loopy BP between $0.0075$ and $0.072$. This is an observed result on these grids, not a theorem: GBP has no general guarantee of being more accurate.

With the two outer regions $\{0, \ldots, 5\}$ (the top two rows) and $\{3, \ldots, 8\}$ (the bottom two), the only intersection is the middle row, with $c = -1$. These regions form a junction tree, and GBP gives the exact marginals and $-F_K = \log Z$, up to the tolerance.

## Correctness

GBP has no general guarantee of convergence or accuracy. What is proved:

- **Consistency at fixed points.** At a fixed point, $\sum_{x_{P \setminus R}} b_P = b_R$ on every edge; the message rule is this equation solved for $m_{P \to R}$.
- **Validity of the CVM.** With the regions closed under intersection and $c_R = 1 - \sum_{S \supsetneq R} c_S$, every variable and every factor is counted once in total.
- **Exactness on junction trees.** If $p = \prod_R p_R^{c_R}$ for the region graph, then $F_K$ at the exact marginals is $-\log Z$. For two outer regions that hold all factors, GBP converges to the exact marginals.
- **The variational meaning.** The fixed points of the parent-to-child algorithm are the stationary points of the region-based free energy $F_K$ under the consistency constraints (Yedidia, Freeman and Weiss 2005). This extends the Bethe result, with one Lagrange multiplier per consistency constraint.

The proofs of the first three points are in the correctness proof.

## Complexity

The costs are in the [real RAM](/real-ram/) model, with regions of at most $w$ variables of at most $k$ states.

- **One message.** The update sums over the $k^{|P|}$ states of the parent and multiplies at most $s$ factors and messages at each, then divides by the messages of $D(P, R)$ at each child state: $O(s k^w)$.
- **One sweep.** $O(g s k^w)$ for $g$ edges of the region graph. For plaquettes on an $n \times n$ grid with binary spins, $g = O(n^2)$ and $k^w = 16$.
- **Sweeps.** Not bounded in general. In the example, 70 sweeps.
- **Memory.** One message per edge, $O(g k^w)$.

The cost is exponential in the size of the regions, as for the [junction tree algorithm](/junction-tree-algorithm/) in the treewidth. The point of GBP is to use regions much smaller than the cliques of a junction tree.

## Properties

- **Generalizes loopy BP.** With the factors and single variables as regions it is loopy BP, and the Kikuchi free energy is the Bethe one.
- **Exact on junction trees.** With the cliques and separators of a [tree decomposition](/tree-decomposition/) as regions, the fixed point is the exact answer.
- **Not convex.** Like the Bethe free energy, $F_K$ can have several local minima, and GBP can have several fixed points.
- **No bound.** $-F_K$ is not in general a lower or an upper bound on $\log Z$.
- **The regions matter.** Small regions that hold the short loops help most. Large regions cost exponentially more.

## Variants and improvements

- **Other region graphs.** Yedidia, Freeman and Weiss also give junction graph and Bethe region graphs, and any valid region graph defines a region-based free energy. The counting numbers need not come from the CVM.
- **Other message rules.** The child-to-parent and two-way algorithms of Yedidia, Freeman and Weiss have the same fixed points as the parent-to-child algorithm on the same region graph.
- **Convergent algorithms.** Double-loop algorithms minimize $F_K$ directly and always converge to a stationary point, at a higher cost per step (Yuille 2002).
- **Convex counting numbers.** Counting numbers that make the free energy convex give a unique fixed point; [tree-reweighted belief propagation](/tree-reweighted-belief-propagation/) does this for the Bethe case and gives an upper bound on $\log Z$.
- **Schedules.** [Residual belief propagation](/residual-belief-propagation/) applies to the messages of GBP as well.

## When to use it

Use GBP when loopy BP is too inaccurate because of many short loops, as on grids and lattices, and the short loops fit in small regions. For an image grid, plaquettes are the usual choice. If a junction tree with small cliques exists, use the exact [junction tree algorithm](/junction-tree-algorithm/) instead. If GBP does not converge, use damping, change the schedule, or use a double-loop method.

## Pitfalls

- **The synchronous schedule.** On the seeded grids above, updating all messages at once from the old ones made the plaquette beliefs swing without end, even with damping 0.5. The sequential schedule converged on all of them.
- **No damping.** With the sequential schedule and no damping, the messages into the center region of the grid swung between near 0 and near 1, each swing larger, until they underflowed to 0 and the run broke down. Damping 0.5 fixed this.
- **Double counting in a home-made region graph.** If the counting numbers do not add up to 1 for each variable and each factor, the free energy is not a valid approximation. Build them with the CVM or check them.
- **Factors outside every region.** Each factor must lie inside some outer region; otherwise it is lost.
- **Reading a non-converged run.** As for loopy BP, report whether the run converged.
- **Region size.** The cost per message is exponential in the size of the parent region.

## Implementations

## History

Kikuchi's cluster variation method of 1951 approximated the free energy of lattice models in statistical physics by sums over clusters of sites, with correction terms for their overlaps. In 2001, Yedidia, Freeman and Weiss showed that the fixed points of belief propagation are the stationary points of the Bethe free energy, and that message passing based on Kikuchi's free energy, which they called generalized belief propagation, is much more accurate on grids. Their 2005 paper introduced region graphs as a general language for such approximations, proved that the parent-to-child, child-to-parent and two-way algorithms all have the stationary points of the region-based free energy as their fixed points, and showed how to construct valid region graphs.

## References
