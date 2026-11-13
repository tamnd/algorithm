---
tag: DKGG4M
kind: definition
slug: task-network
name: Task network
aliases:
- partially ordered task network
area: games-and-search/planning
level: core
summary: A finite set of task nodes with a strict partial order on them, and in lifted models variable bindings and state constraints. HTN methods and problems are stated with it.
prereqs: [strips, directed-acyclic-graph]
see_also: [hierarchical-task-network, htn-planning, htn-decomposition, partial-order-plan, topological-sort, kahns-algorithm, counting-linear-extensions, context-free-grammar]
sources:
  - paper: "Kutluhan Erol, James Hendler and Dana Nau, HTN planning: complexity and expressivity, Proceedings of AAAI-94"
    locator: pp. 1123 to 1128 (task networks as labelled task nodes with a formula of ordering, binding and state constraints)
  - paper: doi:10.1007/BF02136175
    title: "Kutluhan Erol, James Hendler and Dana Nau, Complexity results for HTN planning, Annals of Mathematics and Artificial Intelligence 18(1) (1996)"
    locator: pp. 69 to 93 (the definition of task networks and of their reduction by methods; general locator)
  - paper: doi:10.1609/icaps.v25i1.13721
    title: "Ron Alford, Pascal Bercher and David W. Aha, Tight bounds for HTN planning, Proceedings of ICAPS 2015"
    locator: pp. 7 to 15 (task networks as a set of task identifiers, a partial order and a labelling, and decomposition on them)
  - book: isbn:9781558608566
    title: Malik Ghallab, Dana Nau and Paolo Traverso, Automated Planning, Theory and Practice, Morgan Kaufmann, 2004
    locator: Chapter 11 (task networks as acyclic digraphs of task nodes, total-order and partial-order networks)
---

A task network is the object that a [hierarchical task network](/hierarchical-task-network/) planner works on. It is a finite set of nodes, each labelled with a task, and a strict partial order that says which nodes must come before which. The tasks may be primitive, which are [STRIPS](/strips/) operators, or compound, which must be decomposed further. The initial network of an [HTN planning](/htn-planning/) problem says what has to be done, and the network of a method says how one compound task can be done. Nodes, not tasks, carry the order, so the same task can occur twice. A network stands for the set of its linearizations, the orders of all nodes that respect the partial order.

## Definition

Fix a set $T$ of task names, split into primitive tasks $O$ and compound tasks $C$.

**Task network.** A task network over $T$ is a triple $w = (N, \prec, \alpha)$:

- $N$ is a finite set of nodes,
- $\prec$ is a strict partial order on $N$, that is, irreflexive and transitive,
- $\alpha : N \to T$ labels each node with a task.

In practice the order is given by a set $E \subseteq N \times N$ of pairs, and $\prec$ is its transitive closure. Such a pair set defines a task network exactly when the [directed graph](/directed-acyclic-graph/) $(N, E)$ has no cycle; [Kahn's algorithm](/kahns-algorithm/) tests this in $O(|N| + |E|)$ time. Two networks are **isomorphic** if a bijection between their nodes preserves $\prec$ and $\alpha$. Methods hold networks up to isomorphism, and each use takes a fresh copy.

**Linearizations.** A linearization of $w$ is a sequence $n_1, \ldots, n_k$ of all nodes of $N$ with $i < j$ whenever $n_i \prec n_j$; it is a [topological order](/topological-sort/) of $(N, E)$. Its task sequence is $\alpha(n_1), \ldots, \alpha(n_k)$. The linearizations are the linear extensions of $\prec$; counting them is #P-complete in general, see [counting linear extensions](/counting-linear-extensions/).

**Kinds of networks.**

- $w$ is **totally ordered** if $\prec$ is a total order on $N$. It has one linearization and is written as a sequence of tasks.
- $w$ is **primitive** if $\alpha(n) \in O$ for every node $n$.
- A node is **minimal** if no node precedes it. The minimal nodes are those that some linearization puts first.
- The **empty network** has no nodes and one linearization, the empty sequence.

**Decomposition.** Let $u \in N$ and let $w' = (N', \prec', \alpha')$ be a network with $N' \cap N = \emptyset$. Replacing $u$ by $w'$ gives $(N'', \prec'', \alpha'')$ with $N'' = (N \setminus \{u\}) \cup N'$, $\alpha''$ the union of $\alpha$ and $\alpha'$ on $N''$, and

$$\prec'' \;=\; \prec|_{N \setminus \{u\}} \;\cup\; \prec' \;\cup\; \{(v, x) : v \prec u,\ x \in N'\} \;\cup\; \{(x, v) : u \prec v,\ x \in N'\}.$$

So every new node inherits the orderings of $u$. The result is again a strict partial order: a cycle through new nodes would give $v \prec u \prec v$ in $w$. If $w'$ is empty, $v \prec u \prec v'$ already gave $v \prec v'$ by transitivity, so the order around $u$ survives. An implementation that stores only the generating pairs $E$ must add these pairs explicitly. Every linearization of $w$ with $u$ replaced by a linearization of $w'$ is a linearization of the result. The converse fails: the new nodes may interleave with nodes that were unordered with $u$.

**Lifted networks.** Erol, Hendler and Nau let tasks have arguments, which may be variables, and attached to the network a formula of constraints: orderings $n \prec n'$, bindings $v = v'$, $v = c$ and $v \ne c$, and state constraints $(n, l)$, $(l, n)$ and $(n, l, n')$, which ask that the literal $l$ hold just after $n$, just before $n$, or at every point between $n$ and $n'$. The ground formalization above, without bindings or state constraints, is the one used for the tight complexity results of Alford, Bercher and Aha.

## Examples and non-examples

**A totally ordered method network.** The method *by-taxi* for the task $\mathit{travel}(x, y)$ has the network $\mathit{call\text{-}taxi} \prec \mathit{ride\text{-}taxi}(x, y) \prec \mathit{pay\text{-}driver}$. It has one linearization. This is the network used in the travel example of the [HTN decomposition](/htn-decomposition/) page.

**Splicing.** In the network $\mathit{get} \prec \mathit{travel} \prec \mathit{pay}$, replace $\mathit{travel}$ by $\mathit{call} \prec \mathit{ride}$. The result has the one task sequence $\mathit{get}, \mathit{call}, \mathit{ride}, \mathit{pay}$. If $\mathit{call}$ and $\mathit{ride}$ are unordered, the result has two: the new nodes may come in either order, but both stay between $\mathit{get}$ and $\mathit{pay}$.

**Interleaving.** Take two unordered nodes labelled $A$ and $B$, and replace them by $a_1 \prec a_2$ and $b_1 \prec b_2$. The result has $\binom{4}{2} = 6$ linearizations, all the shuffles of $a_1 a_2$ with $b_1 b_2$. Repeated, this interleaving is what lets partially ordered HTN problems encode the intersection of two context-free languages, which makes plan existence undecidable.

**Repeated tasks.** Two unordered nodes $n_1$ and $n_2$, both labelled $\mathit{pay}$, form a network with two linearizations but one task sequence, $\mathit{pay}, \mathit{pay}$. A set of tasks could not say that $\mathit{pay}$ must happen twice, and this is why the order is on nodes.

**The empty network.** A method with the empty network, such as the method *stop* in the STRIPS encoding on the [hierarchical task network](/hierarchical-task-network/) page, makes its task disappear. The order of the neighbours is kept, as shown above.

**Non-example: a cyclic order.** Nodes $n_1, n_2$ with the pairs $n_1 \prec n_2$ and $n_2 \prec n_1$ do not form a task network, because the closure is not irreflexive. No sequence of the two nodes respects both pairs.

**Non-example: a partial-order plan.** A [partial-order plan](/partial-order-plan/) also has steps with a partial order, but its steps are all primitive, it has START and FINISH steps for the initial state and the goal, and it records causal links. A task network has no links and may contain compound tasks, and it says nothing about which step supports which fact.

**Non-example: a goal.** A classical goal is a set of facts to make true. A task network is a set of things to do; the same final state may be reached by networks with different solutions, and a network may have no solution although its tasks would reach the goal in some other way.

The implementation tests check these definitions on random networks with fixed seeds: consistency against the existence of a linearization, the linearizations against a brute force over all permutations, and the decomposition rule against splicing, on several hundred networks with at most 6 nodes.

## Related definitions

- [Hierarchical task network](/hierarchical-task-network/): the model whose methods and problems are written with task networks.
- [HTN planning](/htn-planning/): the problem of decomposing an initial task network into an executable primitive one.
- [HTN decomposition](/htn-decomposition/): the forward planner that works on the minimal nodes of a task network.
- [Partial-order plan](/partial-order-plan/): the partially ordered steps of plan-space planning, with causal links.
- [Topological sort](/topological-sort/) and [counting linear extensions](/counting-linear-extensions/): computing one linearization, and counting all of them.
- [Context-free grammar](/context-free-grammar/): a totally ordered task network without preconditions is the right side of a production.

## References
