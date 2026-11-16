---
tag: J9KNX6
kind: concept
slug: w-hierarchy
name: W-hierarchy
aliases:
- W[1]
- W[2]
- W[t]
area: complexity/parameterized-complexity
level: advanced
summary: "The chain FPT, W[1], W[2], ..., W[P] of parameterized classes. W[t] is defined by weighted satisfiability of constant-depth circuits of weft at most t, not by circuit depth."
prereqs: [parameterized-reduction, boolean-circuit, xp]
see_also: [w-hardness, weighted-satisfiability, clique-w1-completeness, parameterized-clique, parameterized-dominating-set, fpt-w1-conjecture, para-np-hardness, parameterized-counting-complexity]
sources:
  - book: isbn:9783319212746
    title: Marek Cygan, Fedor V. Fomin, Lukasz Kowalik, Daniel Lokshtanov, Daniel Marx, Marcin Pilipczuk, Michal Pilipczuk and Saket Saurabh, Parameterized Algorithms, Springer, 2015
    locator: Chapter 13, Fixed-parameter intractability (Boolean circuits, weft, the classes W[t] and W[P], and the complete problems)
  - book: isbn:9783540299523
    title: Jörg Flum and Martin Grohe, Parameterized Complexity Theory, Springer, 2006
    locator: Chapter 3 (The Class W[P]), Chapter 6 (The First Level of the Hierarchies), Chapter 7 (The W-Hierarchy) and Chapter 8 (The A-Hierarchy)
  - book: isbn:9781447155584
    title: Rodney G. Downey and Michael R. Fellows, Fundamentals of Parameterized Complexity, Springer, 2013
    locator: the chapters on the W hierarchy and its complete problems
  - paper: doi:10.1137/S0097539792228228
    title: "Rodney G. Downey and Michael R. Fellows, Fixed-parameter tractability and completeness I: basic results, SIAM Journal on Computing 24(4), 873-921 (1995)"
    locator: the definition of the W hierarchy by weft, and the W[2]-completeness of dominating set
  - paper: doi:10.1016/0304-3975(94)00097-3
    title: "Rodney G. Downey and Michael R. Fellows, Fixed-parameter tractability and completeness II: on completeness for W[1], Theoretical Computer Science 141(1-2), 109-131 (1995)"
    locator: the main theorem, W[1]-completeness of independent set and clique
---

The W-hierarchy is the chain of classes $\mathsf{FPT} \subseteq \mathsf{W}[1] \subseteq \mathsf{W}[2] \subseteq \cdots \subseteq \mathsf{W}[\mathsf{SAT}] \subseteq \mathsf{W}[\mathsf{P}] \subseteq \mathsf{XP}$ of [parameterized problems](/parameterized-problem/). A problem is in $\mathsf{W}[t]$ when it has a [parameterized reduction](/parameterized-reduction/) to the question "does this circuit of constant depth and weft at most $t$ accept an input with exactly $k$ ones?". The weft counts the gates of large fan-in on a path from an input to the output; the depth alone does not define the classes. Clique is complete for W[1] and dominating set for W[2], and only the last inclusion, FPT in XP, is known to be proper.

## In plain words

Many hard problems ask you to pick a few items from a large set: a few people who all know each other, or a few sites that together reach every town. Trying every group works, but the cost grows very fast. Some problems have a method that stays cheap when the group is small. Others seem to have none.

The hierarchy sorts the second kind into levels by the shape of the test for a proposed group. For people who all know each other, you check each pair, and then one big "all of these hold". For sites that reach every town, you need one big "some chosen site reaches it" inside one big "every town". That is two big steps, so this problem sits one level higher.

Nobody has proved that the levels differ. Most researchers believe that even the first level has no cheap method.

## The idea

**Circuits and weft.** A [Boolean circuit](/boolean-circuit/) has input gates, NOT gates, AND gates and OR gates, and one output gate. Following Cygan et al., a gate is *small* if its fan-in is at most 2 and *large* otherwise. The *depth* of a circuit is the largest number of gates on a path from an input to the output. The *weft* is the largest number of large gates on such a path. The *weight* of an assignment is its number of ones. Downey and Fellows call a gate small when its fan-in is at most a fixed constant $h$; this gives the same classes.

**Weighted circuit satisfiability.** For a class $\mathcal{C}$ of circuits, $\mathrm{WCS}[\mathcal{C}]$ is the problem: given a circuit $C \in \mathcal{C}$ and an integer $k$, does $C$ have a satisfying assignment of weight exactly $k$? The parameter is $k$. See [weighted satisfiability](/weighted-satisfiability/).

**The classes.** Let $\mathcal{C}_{t,d}$ be the circuits of weft at most $t$ and depth at most $d$. Then

- $\mathsf{W}[t]$ is the class of parameterized problems that have a parameterized reduction to $\mathrm{WCS}[\mathcal{C}_{t,d}]$ for some constant $d$;
- $\mathsf{W}[\mathsf{SAT}]$ uses the circuits that are Boolean formulas (every gate has fan-out at most 1), with no bound on depth;
- $\mathsf{W}[\mathsf{P}]$ uses all circuits.

**Why weft and not depth.** Depth alone gives nothing. A circuit of depth $d$ in which every gate is small has an output that depends on at most $2^d$ inputs. For constant $d$, one finds those inputs, tries their at most $2^{2^d}$ values, and checks whether some accepted value can be completed to weight exactly $k$ with the free inputs. This takes polynomial time, so circuits of weft 0 give only FPT problems. A large gate is the expensive step: an AND over many inputs says "all of these hold", an OR says "some of these holds", and each extra large gate on a path adds one more such quantifier over the input set.
**The inclusions.** FPT is in W[1], because a problem in FPT reduces to any problem with at least one yes-instance and one no-instance: solve the instance in FPT time and output a fixed yes-instance or no-instance. Each $\mathcal{C}_{t,d}$ is inside $\mathcal{C}_{t+1,d}$, which gives $\mathsf{W}[t] \subseteq \mathsf{W}[t+1]$. Constant-depth circuits can be turned into formulas of polynomial size, which puts every $\mathsf{W}[t]$ inside W[SAT], and formulas are circuits. W[P] is inside [XP](/xp/): try all $\binom{n}{k} \le n^k$ assignments of weight $k$ and evaluate the circuit on each in polynomial time. FPT is a proper subset of XP without any assumption. Each other inclusion is open. Most researchers believe that all of them are proper. $\mathsf{FPT} = \mathsf{W}[1]$ would refute the [Exponential Time Hypothesis](/strong-exponential-time-hypothesis/); see the [FPT versus W[1] conjecture](/fpt-w1-conjecture/).

**Complete problems.** Hardness is defined by parameterized reductions; see [W[t]-hardness](/w-hardness/).

| Class | Complete problems, with parameter $k$ |
|---|---|
| W[1] | [clique](/parameterized-clique/), [independent set](/parameterized-independent-set/), multicolored clique, weighted q-CNF satisfiability for each fixed $q \ge 2$, acceptance by a single-tape nondeterministic Turing machine within $k$ steps |
| W[2] | [dominating set](/parameterized-dominating-set/), [set cover](/set-cover/) with $k$ sets, [hitting set](/hitting-set/) with $k$ elements, weighted CNF satisfiability |
| W[t], $t \ge 2$ | weighted satisfiability of t-normalized formulas (an AND of ORs of ANDs, and so on, with $t$ alternations) |
| W[SAT] | weighted satisfiability of Boolean formulas |
| W[P] | weighted circuit satisfiability |

The W[1] and W[2] results are by Downey and Fellows (1995). The hard direction for clique is the theorem [clique is W[1]-complete](/clique-w1-completeness/).

## Examples

**Clique has weft 1.** Given a graph $G$ and $k$, use one input $x_v$ for each vertex. For each pair $u, v$ that is not an edge, add a small OR gate $\neg x_u \vee \neg x_v$. Join all these OR gates with one large AND. Each path from an input to the output passes NOT, OR and AND, and only the AND is large, so the weft is 1 and the depth is 3. An assignment of weight $k$ satisfies the circuit exactly when the $k$ chosen vertices have no non-edge between them, that is, when they form a clique. For the house graph (a square 0, 1, 2, 3 and a roof vertex 4 joined to 0 and 1) the non-edges are 02, 13, 24 and 34. The circuit has 4 OR gates. It has 6 satisfying assignments of weight 2 (one per edge), exactly 1 of weight 3, the triangle $\{0, 1, 4\}$, and none of weight 4. This puts p-Clique in W[1].

**Dominating set has weft 2.** For each vertex $v$, add an OR over the inputs $x_u$ with $u$ in the closed neighborhood $N[v]$, then join these ORs with one large AND. When the degrees are at least 2, every path passes two large gates, so the weft is 2. A satisfying assignment of weight $k$ is a dominating set of size $k$. In the Petersen graph every closed neighborhood has 4 vertices. The circuit has no satisfying assignment of weight 2, 10 of weight 3 and 75 of weight 4. No circuit of weft 1 is known for this problem, and none exists unless $\mathsf{W}[1] = \mathsf{W}[2]$, because dominating set is W[2]-complete.

**The same graph, two levels.** The Petersen graph has 15 edges, no triangle, and 5 independent sets of size 4. With parameter $k$, asking for a clique of size $k$ is a W[1] question, asking for an independent set of size $k$ is also a W[1] question (on the complement graph), and asking for a dominating set of size $k$ is a W[2] question. The data is the same; the test of a candidate set has a different shape.

## Where it is used

- *Evidence of hardness.* A W[1]-hardness proof is the standard reason to stop looking for an FPT algorithm, in the same way that an NP-hardness proof is the reason to stop looking for a polynomial-time one. Cygan et al. collect many such proofs, almost all from multicolored clique.
- *Choice of parameter.* The hierarchy separates parameterizations of one problem. Vertex cover with the cover size is FPT; independent set with the set size is W[1]-complete; dominating set with the set size is W[2]-complete, though all three are NP-complete as classical problems.
- *Approximation.* [Parameterized inapproximability](/parameterized-inapproximability/) asks whether hardness stays when an FPT algorithm may return an approximate answer. Many results there assume [Gap-ETH](/gap-eth/).
- *Counting and other hierarchies.* The counting class #W[1] of [parameterized counting complexity](/parameterized-counting-complexity/) mirrors W[1]. Flum and Grohe also define the A-hierarchy by alternation and compare it with the W-hierarchy. The class [para-NP](/para-np-hardness/) contains W[P]; its hard problems are NP-hard for one fixed value of the parameter, and they are not in XP unless P = NP.

## References
