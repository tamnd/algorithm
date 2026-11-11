---
tag: GGJNRV
kind: definition
slug: ruling-set
name: Ruling set
aliases:
- (alpha,beta)-ruling set
area: distributed/distributed-graph-algorithms
level: advanced
summary: 'A relaxation of MIS: nodes pairwise at distance at least alpha, with every node within distance beta of the set. An MIS is a (2, 1)-ruling set.'
prereqs: [local-model, maximal-independent-set, distributed-mis]
see_also: [distributed-mis, network-decomposition, cole-vishkin, ring-coloring, sinkless-orientation, kmw-lower-bound, round-elimination, independent-set]
sources:
  - paper: doi:10.1109/SFCS.1989.63504
    title: Baruch Awerbuch, Andrew V. Goldberg, Michael Luby and Serge A. Plotkin, Network decomposition and locality in distributed computation, FOCS 1989
    locator: pp. 364 to 369 (the definition of (alpha, beta)-ruling sets and the deterministic construction by identifier bits)
  - paper: doi:10.1137/20M1381770
    title: Alkida Balliu, Sebastian Brandt and Dennis Olivetti, Distributed lower bounds for ruling sets, SIAM Journal on Computing 51(1), 2022
    locator: pp. 70 to 115 (Omega(min(log Delta / (beta log log Delta), log_Delta n)) deterministic and the randomized analogue; FOCS 2020 version pp. 365 to 376)
  - paper: doi:10.1109/FOCS61266.2024.00007
    title: Mohsen Ghaffari and Christoph Grunau, Near-optimal deterministic network decomposition and ruling set, and improved MIS, FOCS 2024
    locator: pp. 2148 to 2179 (a deterministic (2, O(log log n))-ruling set in O~(log n) rounds)
  - paper: doi:10.1137/0221015
    title: Nathan Linial, Locality in distributed graph algorithms, SIAM Journal on Computing 21(1), 1992
    locator: pp. 193 to 201 (the Omega(log* n) bound on rings, which applies to ruling sets with constant beta)
---

A ruling set is a set of nodes of a graph that are spread out, so that no two are close, and dense, so that every node is close to one of them. A [maximal independent set](/maximal-independent-set/) is the special case where "not close" means "not adjacent" and "close" means "at distance at most 1". Ruling sets with a larger second parameter are easier to compute in the [LOCAL model](/local-model/), and they serve as cluster centres in [network decomposition](/network-decomposition/) and other algorithms. Awerbuch, Goldberg, Luby and Plotkin (1989) defined them and gave a deterministic $(2, O(\log n))$-ruling set in $O(\log n)$ rounds.

## Definition

Let $G = (V, E)$ be a graph with the shortest path distance $\mathrm{dist}$, and let $\alpha \ge 1$ and $\beta \ge 0$ be integers. A set $R \subseteq V$ is an **$(\alpha, \beta)$-ruling set** of $G$ if

1. (spread) $\mathrm{dist}(u, v) \ge \alpha$ for all distinct $u, v \in R$, and
2. (domination) every $v \in V$ has some $r \in R$ with $\mathrm{dist}(v, r) \le \beta$.

An $(\alpha, \beta)$-ruling set exists for every graph when $\beta \ge \alpha - 1$: a maximal set with condition 1 has condition 2 with $\beta = \alpha - 1$, since a node at distance at least $\alpha$ from all of $R$ could be added. A **$\beta$-ruling set** usually means a $(2, \beta)$-ruling set, an independent set that dominates within distance $\beta$. As a distributed problem, each node outputs one bit, $v \in R$ or not, and the cost is the number of rounds; both conditions can be checked by each node in its ball of radius $\max(\alpha - 1, \beta)$, so it is a [locally checkable labeling](/locally-checkable-labeling/) problem when $\alpha$ and $\beta$ are constants.

**A deterministic construction by identifier bits (AGLP 1989).** Let the identifiers be distinct $B$-bit numbers, $B = \lceil \log_2 N \rceil$ for identifiers in $[0, N)$. For $j = 0, \dots, B$, call two nodes $j$-related if their identifiers agree on all bits from bit $j$ upwards, that is $\lfloor \mathrm{id}(u) / 2^j \rfloor = \lfloor \mathrm{id}(v) / 2^j \rfloor$. Start with $R_0 = V$. At level $j = 1, \dots, B$, a node $v \in R_{j-1}$ whose bit $j - 1$ is 1 leaves if some $u \in R_{j-1}$ with bit $j - 1$ equal to 0 is $j$-related to $v$ and has $\mathrm{dist}(u, v) \le \alpha - 1$. The rest form $R_j$. Output $R = R_B$.

*Claim.* For every level $j$ and every class $S$ of $j$-related nodes, (a) any two distinct nodes of $R_j \cap S$ are at distance at least $\alpha$, and (b) every node of $S$ is within distance $(\alpha - 1) j$ of $R_j \cap S$.

*Proof.* By induction on $j$. For $j = 0$, each class is a single node, which is in $R_0$, so (a) and (b) hold. For $j \ge 1$, the class $S$ splits into $S_0$ and $S_1$, the $(j-1)$-related classes with bit $j - 1$ equal to 0 and to 1. Nodes of $R_{j-1} \cap S_0$ never leave at level $j$, and nodes of $R_{j-1} \cap S_1$ leave exactly when they are within distance $\alpha - 1$ of $R_{j-1} \cap S_0$. (a): two nodes in the same half are at distance at least $\alpha$ by induction, and a node of $S_1$ that stays is at distance at least $\alpha$ from every node of $R_{j-1} \cap S_0$ by the rule. (b): a node $x$ of $S_0$ is within $(\alpha - 1)(j - 1)$ of $R_{j-1} \cap S_0 \subseteq R_j \cap S$. A node $x$ of $S_1$ is within $(\alpha - 1)(j - 1)$ of some $r \in R_{j-1} \cap S_1$; if $r$ stays, we are done, and if $r$ leaves, $r$ is within $\alpha - 1$ of a node of $R_{j-1} \cap S_0 \subseteq R_j \cap S$, so $x$ is within $(\alpha - 1) j$ of $R_j \cap S$. $\blacksquare$

At $j = B$ all nodes are $B$-related, so $R$ is an $(\alpha, (\alpha - 1) B)$-ruling set of $G$. A level needs only the set membership of nodes within distance $\alpha - 1$, so it takes $\alpha - 1$ rounds, and the whole construction takes exactly $(\alpha - 1) B$ rounds. With $N = n^{O(1)}$ and $\alpha = 2$, this is a $(2, O(\log n))$-ruling set in $O(\log n)$ rounds, with one-bit messages.

## Examples and non-examples

- **An MIS is a $(2, 1)$-ruling set**, and every $(2, 1)$-ruling set is an MIS: independence is $\alpha = 2$, and maximality is $\beta = 1$. On the ring of 9 nodes $0, \dots, 8$, the set $\{0, 2, 4, 6\}$ is an MIS, and node 8 is dominated by its neighbour 0.
- **The bit construction on a path.** On the path $0 - 1 - \dots - 15$ with identifiers equal to positions and $\alpha = 2$, level 1 removes every odd node, because its left neighbour has the same bits above bit 0 and bit 0 equal to 0. At levels 2 to 4 the even nodes are not adjacent, and nobody leaves. So $R = \{0, 2, \dots, 14\}$, a $(2, 1)$-ruling set, found in $B = 4$ rounds.
- **From a 3-colouring of a ring.** The nodes whose colour is larger than both neighbours' colours form a $(2, 2)$-ruling set, found in one round; see [Cole-Vishkin](/cole-vishkin/). Neighbours cannot both be local maxima, and from any node, walking towards larger colours reaches a local maximum within 2 steps, since there are only 3 colours.
- **A non-example.** On the path $a - b - c - d - e$, the set $\{a, e\}$ has spread 4 but is not a $(2, 1)$-ruling set, since $c$ is at distance 2 from it. It is a $(4, 2)$-ruling set.
- **Lower bound for constant $\beta$.** On rings, a $(2, \beta)$-ruling set for a constant $\beta$ gives a 3-colouring in $O(\beta)$ rounds, so by [Linial's bound](/linial-coloring-lower-bound/) it needs $\Omega(\log^* n)$ rounds.

## Related definitions

- **[Maximal independent set](/distributed-mis/).** The $(2, 1)$ case. Its distributed complexity is larger: Balliu, Brandt and Olivetti (2020) show that a $(2, \beta)$-ruling set needs $\Omega(\min(\log \Delta / (\beta \log \log \Delta), \log_\Delta n))$ deterministic rounds and $\Omega(\min(\log \Delta / (\beta \log \log \Delta), \log_\Delta \log n))$ randomized rounds, for $\beta$ up to about $\sqrt{\log \Delta / \log \log \Delta}$. So in this regime, relaxing $\beta$ lowers the lower bound only by a factor $\beta$.
- **Power graphs.** In $G^k$, two nodes are adjacent when their distance in $G$ is at most $k$. A $(2, \beta')$-ruling set of $G^{\alpha - 1}$ is an $(\alpha, (\alpha - 1) \beta')$-ruling set of $G$, and so an MIS of $G^k$ is a $(k + 1, k)$-ruling set of $G$. Algorithms often compute ruling sets on $G^k$ to pick well-separated cluster centres, as in [sinkless orientation](/sinkless-orientation/) and [network decomposition](/network-decomposition/).
- **Net.** In metric spaces, an $r$-net is a set of points pairwise more than $r$ apart with every point within $r$ of the set; a ruling set is the graph version with two separate parameters.
- **Dominating set.** A $(1, 1)$-ruling set is a [dominating set](/dominating-set/); ruling sets add the spread condition, which bounds how many centres a node can have nearby.
- **Faster deterministic ruling sets.** Ghaffari and Grunau (2024) compute a $(2, O(\log \log n))$-ruling set deterministically in $\tilde{O}(\log n)$ rounds, where $\tilde{O}$ hides factors polynomial in $\log \log n$.

## References
