---
tag: RAWF2P
kind: theorem
slug: cooper-theorem
name: Cooper's theorem
aliases:
- NP-hardness of exact Bayesian network inference
- Cooper's NP-hardness theorem
area: machine-learning/probabilistic-inference
level: advanced
summary: "Deciding whether P(X = x) > 0 in a Bayesian network is NP-complete, by a reduction from 3SAT. So exact inference is NP-hard, and the same network makes it #P-hard."
prereqs: [bayesian-network, np-hard, 3-sat]
see_also: [dagum-luby-theorem, marginal-inference, model-counting, parsimonious-reduction, treewidth, variable-elimination, partition-function-computation, np-complete]
sources:
  - paper: doi:10.1016/0004-3702(90)90060-D
    title: "Gregory F. Cooper, The computational complexity of probabilistic inference using Bayesian belief networks, Artificial Intelligence 42(2-3), 1990, pages 393 to 405"
    locator: the reduction from 3SAT that shows probabilistic inference in belief networks is NP-hard
  - paper: doi:10.1016/0004-3702(94)00092-1
    title: "Dan Roth, On the hardness of approximate reasoning, Artificial Intelligence 82(1-2), 1996, pages 273 to 302"
    locator: exact probabilistic inference is #P-complete, by a reduction from counting satisfying assignments
  - book: isbn:9780262013192
    title: Daphne Koller and Nir Friedman, Probabilistic Graphical Models, Principles and Techniques, MIT Press, 2009
    locator: "Section 9.1, the complexity of exact inference: the 3-SAT network with one node per variable, one per clause, and a chain of AND nodes"
---

Cooper's theorem says that exact inference in [Bayesian networks](/bayesian-network/) is NP-hard. Cooper (1990) built, for each 3-CNF formula, a small network in which one node has positive probability exactly when the formula is satisfiable. The same network gives the number of satisfying assignments, so exact inference is #P-hard too, and it is the base of the [Dagum-Luby theorem](/dagum-luby-theorem/) on approximate inference.

## Statement

**Theorem (Cooper 1990).** Consider the problem: given a Bayesian network over binary variables, with rational conditional tables, a node $Y$ and a value $y$, decide whether $P(Y = y) > 0$. This problem is [NP-complete](/np-complete/). It stays NP-complete when every node has at most three parents and every table entry is $0$, $\tfrac12$ or $1$.

So computing $P(Y = y)$ exactly, or a posterior $P(Y = y \mid e)$, is [NP-hard](/np-hard/): no algorithm does it in polynomial time on all networks unless P = NP. The network of the proof also has $2^n P(Y = 1)$ equal to the number of satisfying assignments of the formula, so exact inference is #P-hard as well (Roth 1996).

## In plain words

A Bayesian network can describe any yes or no puzzle in which some switches must be set so that a list of rules all hold. Put one fair coin for each switch, one node for each rule that says whether the rule holds, and one final node that says whether all the rules hold.

Now ask the network a simple question: can the final node be yes at all? The answer is yes exactly when some setting of the switches satisfies every rule. That puzzle is one of the standard hard problems, so no fast method can answer every question of this kind, unless a large group of hard problems all have fast methods.

The network is small and each node looks at three others at most. The hardness comes from the way the nodes share their parents, not from big tables.

## Proof

Let $\varphi = c_1 \wedge \cdots \wedge c_m$ be a [3-CNF](/3-sat/) formula over variables $q_1, \ldots, q_n$, where each clause $c_j$ is an OR of at most three literals on distinct variables. Build a network $B_\varphi$ with binary nodes:

1. **Roots.** $Q_1, \ldots, Q_n$ with no parents and $P(Q_i = 1) = \tfrac12$.
2. **Clause nodes.** $C_j$ for $j = 1, \ldots, m$, with the variables of $c_j$ as parents, and $P(C_j = 1 \mid q) = 1$ if the clause is true under the parent values and $0$ if not.
3. **A chain of ANDs.** $A_1$ with parent $C_1$ and $A_1 = C_1$; for $j \ge 2$, $A_j$ with parents $A_{j-1}$ and $C_j$, and $A_j = A_{j-1} \wedge C_j$. Each is a 0 and 1 table.

The query node is $Y = A_m$ and the value is $y = 1$.

**Size.** $B_\varphi$ has $n + 2m$ nodes. Each node has at most three parents, so each table has at most 8 rows, and every entry is $0$, $\tfrac12$ or $1$. The network is written in $O(n + m)$ space and built in that time. The chain is what keeps the in-degree small: one AND node over all the clauses would need a table with $2^m$ rows.

**Lemma.** Let $q \in \{0,1\}^n$. Write $c_j(q)$ for the truth value of clause $j$ and $a_j(q) = c_1(q) \wedge \cdots \wedge c_j(q)$. A full assignment $(q, c, a)$ of $B_\varphi$ has probability $2^{-n}$ if $c_j = c_j(q)$ and $a_j = a_j(q)$ for all $j$, and probability $0$ otherwise.

*Proof of the lemma.* By the chain rule of a Bayesian network, $P(q, c, a)$ is the product of one table entry per node. The $n$ root entries are each $\tfrac12$. Each clause and chain entry is $1$ when the node has the value that its function gives on the parent values, and $0$ otherwise. If every such node agrees with its function, then by induction on $j$ we get $c_j = c_j(q)$ and $a_j = a_j(q)$, and the product is $2^{-n}$. If some node disagrees, one factor is $0$. $\square$

**The reduction.** Sum the lemma over all full assignments with $a_m = 1$. Only the $q$ with $a_m(q) = 1$ count, that is, the $q$ that satisfy $\varphi$, and each one gives exactly one assignment of probability $2^{-n}$. So
$$P(A_m = 1) = \frac{\#\varphi}{2^n},$$
where $\#\varphi$ is the number of satisfying assignments. Hence $P(A_m = 1) > 0$ if and only if $\varphi$ is satisfiable. The map $\varphi \mapsto (B_\varphi, A_m, 1)$ is a [polynomial-time reduction](/polynomial-time-reduction/) from 3SAT, which is NP-complete, so the decision problem is NP-hard, even with in-degree at most 3 and entries in $\{0, \tfrac12, 1\}$.

**Membership in NP.** $P(Y = y) = \sum_x P(x)$ over the full assignments $x$ with $x_Y = y$, and every term is nonnegative. So $P(Y = y) > 0$ exactly when some such $x$ has $P(x) > 0$. Such an $x$ is a certificate: it has one bit per node, and $P(x) > 0$ holds exactly when each of its table entries is nonzero, which the verifier checks with one table lookup per node. So the problem is in NP, and it is NP-complete.

**Exact values.** An algorithm that computes $P(Y = y)$ exactly answers the decision question with one call, so it is NP-hard. A posterior is no easier: add a node $E$ with parent $A_m$ and $E = A_m$; then $P(A_m = 1 \mid E = 1)$ is defined, and equal to $1$, exactly when $\varphi$ is satisfiable. Finally, $\#\varphi = 2^n P(A_m = 1)$, so one call to an exact algorithm counts the satisfying assignments of a 3-CNF formula. Counting them is #P-complete, so exact inference is #P-hard; the reduction is [parsimonious](/parsimonious-reduction/) in the sense that each model of $\varphi$ gives exactly one positive-probability assignment of the network. $\blacksquare$

**An example.** Take $\varphi = (q_1 \vee q_2 \vee \neg q_3) \wedge (\neg q_1 \vee q_3 \vee q_4) \wedge (\neg q_2 \vee \neg q_3 \vee \neg q_4)$, with $n = 4$ and $m = 3$. The network has $4 + 2 \cdot 3 = 10$ nodes. Each clause is false on exactly two of the 16 assignments, and these six assignments are all different, so 10 assignments satisfy $\varphi$ and $P(A_3 = 1) = 10/16 = 5/8$. If the eight clauses on three variables with all sign patterns are used instead, no assignment satisfies them, and $P(A_8 = 1) = 0$.

## Consequences

- **No general fast algorithm.** Unless P = NP, every exact algorithm for [marginal inference](/marginal-inference/) takes more than polynomial time on some networks. Cooper (1990) concluded that research should look at special classes of networks, at average-case behaviour, and at approximation.
- **Which structure matters.** [Variable elimination](/variable-elimination/) and the [junction tree algorithm](/junction-tree-algorithm/) run in time $O(n\, d^{w+1})$ for an elimination order of induced width $w$. So the hard networks must have large [treewidth](/treewidth/).
- **Other queries.** The same network shows that [MAP inference](/map-inference/) is hard: with evidence $A_m = 1$, a most probable assignment has positive probability exactly when $\varphi$ is satisfiable, and its $q$ part satisfies $\varphi$.
- **Partition functions.** With the tables as factors, $Z(A_m = 1) = P(A_m = 1)$, so [partition function computation](/partition-function-computation/) is #P-hard by the same argument, and so is weighted [model counting](/model-counting/).
- **Approximation.** The theorem leaves open whether approximate answers are easy. The Dagum-Luby theorem answers this for answers with evidence, with the same network.

## Tightness

- **Bounded treewidth.** For networks whose moral graph has treewidth at most a constant $w$, exact inference takes polynomial time, by elimination along a good order. So the hardness needs unbounded treewidth.
- **Polytrees.** If the network has no undirected cycle, [belief propagation](/belief-propagation/) computes all marginals in time linear in the total size of the tables. In $B_\varphi$, two clauses that share two variables already make an undirected cycle.
- **In-degree.** Three parents is not the limit. Split each clause node into two OR nodes, $D_j = \ell_1 \vee \ell_2$ and $C_j = D_j \vee \ell_3$, with the signs of the literals put into the tables. The proof goes through with $n + 3m$ nodes, and every node has at most two parents.
- **Thresholds.** The question "is $P(Y = y) > p$" for a given $p$ is harder than the question "is it $> 0$": it is complete for the class [PP](/pp/), as listed by Park and Darwiche (2004). Deciding "$> 0$" sits in NP, as shown above.
- **Absolute error without evidence.** Forward sampling gives $P(Y = y)$ within any fixed additive error $\varepsilon$ with high probability, in time polynomial in the network size and $1/\varepsilon$, by the [Hoeffding inequality](/hoeffding-inequality/). The hardness is for exact values, for relative error, and for conditioning on evidence.

## History

Pearl (1982, 1986) gave a message passing algorithm that is fast on singly connected networks, and Lauritzen and Spiegelhalter (1988) gave a general exact algorithm whose cost grows with the size of the cliques. Cooper (1990) explained why no general algorithm can be fast in the worst case: he reduced 3SAT to the question whether a node has positive probability. Dagum and Luby (1993) then showed that approximate inference with evidence is also NP-hard. Roth (1996) used the same kind of construction with a count of models to show that exact inference is #P-complete, and studied which approximate tasks stay hard. Koller and Friedman (2009, Section 9.1) give the version of the proof with the chain of AND nodes.

## References
