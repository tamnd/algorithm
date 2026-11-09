---
tag: 4QB2GQ
kind: problem
slug: dont-care-minimization
name: Don't-care-based function minimization
aliases:
- incompletely specified function minimization
- care-set minimization
area: logic-and-constraints/binary-decision-diagrams
level: advanced
summary: Given BDDs of f and a care set c, find the smallest BDD of a g that equals f wherever c is 1. The problem is NP-complete even for a fixed order, so tools use heuristics.
prereqs: [reduced-ordered-bdd, generalized-cofactor, bdd-canonicity]
see_also: [generalized-cofactor, variable-ordering, graph-coloring, symbolic-reachability, cofactor, bdd-apply, reduced-ordered-bdd, chromatic-number]
sources:
  - paper: "Martin Sauerhoff, Ingo Wegener, On the complexity of minimizing the OBDD size for incompletely specified functions, IEEE Transactions on Computer-Aided Design of Integrated Circuits and Systems 15(11), 1996, pages 1435 to 1437"
    title: On the complexity of minimizing the OBDD size for incompletely specified functions
    locator: main theorem (NP-completeness for a fixed variable order)
  - paper: "Thomas R. Shiple, Ramin Hojati, Alberto L. Sangiovanni-Vincentelli, Robert K. Brayton, Heuristic minimization of BDDs using don't cares, Proceedings of the 31st Design Automation Conference (DAC), 1994"
    title: Heuristic minimization of BDDs using don't cares
    locator: the framework of matching heuristics, sibling substitution, and the comparison with constrain and restrict
  - paper: "Youpyo Hong, Peter A. Beerel, Jerry R. Burch, Kenneth L. McMillan, Safe BDD minimization using don't cares, Proceedings of the 34th Design Automation Conference (DAC), 1997"
    title: Safe BDD minimization using don't cares
    locator: heuristics whose result is never larger than the input BDD
  - paper: "Olivier Coudert, Jean Christophe Madre, A unified framework for the formal verification of sequential circuits, Proceedings of the IEEE International Conference on Computer-Aided Design (ICCAD), 1990"
    title: A unified framework for the formal verification of sequential circuits
    locator: the restrict operator, used to simplify with a care set
---

Don't-care minimization asks for the smallest [reduced ordered BDD](/reduced-ordered-bdd/) of a function that is fixed only on part of the input space. The input is a function $f$ and a care set $c$, both given as BDDs with the same variable order. Every $g$ with $g(x) = f(x)$ wherever $c(x) = 1$ is a correct answer, and we want one with the fewest nodes. Such incompletely specified functions arise often: the next-state functions of a circuit matter only on the reachable states, and a frontier set in [symbolic reachability](/symbolic-reachability/) can be replaced by any set between the frontier and the reached set. Sauerhoff and Wegener (1996) proved that the decision version is NP-complete, even with the order fixed. So tools use heuristics: the [generalized cofactors](/generalized-cofactor/) constrain and restrict of Coudert and Madre, the matching heuristics of Shiple, Hojati, Sangiovanni-Vincentelli and Brayton (1994), and the safe heuristics of Hong, Beerel, Burch and McMillan (1997). None of them has a guarantee, and constrain and restrict can return a larger BDD than $f$.

## In plain words

Sometimes we only need the answers of a yes-or-no function in some cases, and the other cases never happen or do not matter. Then we may choose any answers in the other cases. A good choice can make the diagram of the function much smaller, because parts that were different can become equal and be shared. The question is which answers to choose. Trying all choices takes far too long, and the problem is known to be hard in general. So programs use quick rules that look at one node at a time. These rules often help a lot, but they do not always find the best choice, and some of them can even make the diagram bigger.

## Definition

**Input:** a variable order $x_1 < \cdots < x_n$, the reduced ordered BDDs of $f$ and of a care set $c \ne 0$ in that order, and an integer $k$ for the decision version.

**Feasible solutions:** the functions $g$ with $g(x) = f(x)$ for each $x$ with $c(x) = 1$. Equivalently, $g$ lies in the interval

$$f \wedge c \;\le\; g \;\le\; f \vee \neg c,$$

where $\le$ is pointwise. The points with $c(x) = 0$ form the don't-care set.

**Goal:** minimize the size of the reduced ordered BDD of $g$ in the given order. The decision version asks whether some feasible $g$ has at most $k$ nodes.

The problem is also stated with the interval $[L, U]$, $L \le U$, as input; then $f = L$ and $c = L \vee \neg U$. The order is part of the input and is not changed.

## Variants

- **Free order.** Minimize over all orders and all feasible $g$. For $c = 1$ this is the [variable ordering problem](/variable-ordering/), which is NP-complete, so this variant is NP-hard too.
- **Several outputs.** Minimize a shared BDD of several functions, each with its own care set.
- **One level.** Minimize the number of nodes on one level; this is close to [graph coloring](/graph-coloring/) (see Bounds).
- **Safe minimization.** Return a $g$ that is never larger than $f$. Any heuristic becomes safe by keeping $f$ when the result is larger.
- **Other representations.** The same question for sum-of-products formulas is two-level logic minimization with don't cares, a different problem with its own heuristics, such as Espresso.

## Examples

**The heuristics miss the optimum.** Take the order $x_1 < x_2$, $f = x_1 \wedge x_2$ (4 nodes with the sinks) and $c = x_1 \vee \neg x_2$. The only don't-care point is $(x_1, x_2) = (0, 1)$. Setting $g(0, 1) = 1$ gives $g = x_2$, with 3 nodes. This is optimal. A constant does not fit, since $f$ takes both values on the care set. The other functions with 3 nodes are $x_1$, $\neg x_1$ and $\neg x_2$, and each differs from $f$ at a care point: $(1, 0)$, $(0, 0)$ and $(1, 1)$.

Restrict and constrain both return $f$. At the top variable $x_1$, the care cofactors are $c|_{x_1 = 0} = \neg x_2$ and $c|_{x_1 = 1} = 1$. Neither is 0, so the recursion keeps the node $x_1$ with the children $0 \downarrow \neg x_2 = 0$ and $x_2 \downarrow 1 = x_2$. The optimum needs *sibling substitution*: the low child 0 and the high child $x_2$ agree on the care set $\neg x_2$ of the low child, so the low child can be replaced by $x_2$, and then the node is redundant.

**Restrict can grow.** In the measurement below, 7 of the 3000 pairs give a restrict result larger than $f$, and 97 give a constrain result larger than $f$. The [generalized cofactor](/generalized-cofactor/) page gives a case with $n = 3$ where constrain doubles the size.

**Measured quality.** 3000 random pairs $(f, c)$ with $n = 4$, each truth table entry an independent fair bit, the seed 1996, and the natural order. The exact optimum is found by trying all completions of the don't-care set. The numbers are the mean BDD sizes with the sinks.

| $f$ | constrain | restrict | min$(f$, restrict$)$ | exact optimum |
|---|---|---|---|---|
| 9.41 | 6.47 | 6.29 | 6.29 | 5.51 |

Restrict was optimal in 1409 of the 3000 pairs. These numbers are for small random functions only and say nothing about the worst case.

## Known algorithms

**Exact search.** Try all $2^{d}$ completions of the $d$ don't-care points, or search level by level over the possible subfunctions. This is exponential and works only for small $n$.

**Constrain and restrict** (Coudert, Berthet and Madre, 1989; Coudert and Madre, 1990). One recursive pass over the BDDs of $f$ and $c$. Where the care set has no point on one side of a variable, the result does not test that variable. Constrain takes $O(\lvert f \rvert \cdot \lvert c \rvert)$ expected time. Both can return a BDD larger than $f$. See the [generalized cofactor](/generalized-cofactor/) page for the algorithms and their proofs.

**Matching heuristics** (Shiple, Hojati, Sangiovanni-Vincentelli and Brayton, 1994). The recursion carries a care set with each node. At a node, if the two children agree on the points that both care about, replace both by one common extension, which removes the node; if one child agrees with the other on its own care set, replace it by the other child, which is sibling substitution. The paper compares several such rules, one-sided and two-sided, with constrain and restrict on benchmark circuits, and shows that such operators can increase the size.

**Safe heuristics** (Hong, Beerel, Burch and McMillan, 1997). They change only parts of the BDD where the change cannot add nodes, so the result is never larger than $f$.

**Level-based methods.** For one level, the subfunctions below it with their care sets form a compatibility graph, and a small coloring of the conflicts gives few nodes on that level (see Bounds). Heuristics color level by level from the top, which fixes the care sets of the next levels.

## Bounds

**Membership in NP.** *Proof.* A certificate is a reduced ordered BDD $G$ with at most $k$ nodes. Check that it is reduced and ordered, then check feasibility: $g \wedge c = f \wedge c$, with two [APPLY](/bdd-apply/) calls and a comparison of ids. This takes time polynomial in $k$ and the input sizes. If a feasible $g$ with at most $k$ nodes exists, its reduced BDD is such a certificate. $\square$

**NP-hardness** (Sauerhoff and Wegener, 1996): deciding whether a feasible $g$ has at most $k$ nodes is NP-complete for a fixed order. The published reduction is not reproduced here. *Proof idea.* The following facts show where the hardness comes from. They are proved below, but they do not give the reduction.

**Lemma 1 (common extension).** Partial functions $p_1, \ldots, p_m$, each given by a value function and a care set, have a common extension if and only if every two of them have one.

*Proof.* If all have a common extension, so does every pair. Conversely, if every pair agrees at every point where both care, then at each point all the $p_j$ that care there have the same value. Define $h$ at that point as this value, or 0 if no $p_j$ cares. Then $h$ extends all of them. $\square$

**Lemma 2 (level lower bound).** For $1 \le i \le n + 1$ and each $a \in \{0, 1\}^{i-1}$, let $p_a$ be the partial function $(f|_a, c|_a)$ of $x_i, \ldots, x_n$, with $x_1, \ldots, x_{i-1}$ fixed to $a$. Let $H_i$ be the graph on the distinct partial functions $p_a$, with an edge between two that conflict, that is, differ at a point where both care. Then every feasible $g$ has at least $\chi(H_i)$ nodes, where $\chi$ is the [chromatic number](/chromatic-number/).

*Proof.* Let $g$ be feasible. For each $a$, the function $g|_a$ extends $p_a$, since $g$ agrees with $f$ on $c$. Give $p_a$ the color $g|_a$. Two conflicting partial functions cannot have the same extension, so this is a proper coloring, and it uses as many colors as there are distinct functions $g|_a$. In the reduced BDD of $g$, the path for $a$ from the root ends at a node of the function $g|_a$, and distinct functions give distinct nodes by [canonicity](/bdd-canonicity/). So $g$ has at least as many nodes as colors, which is at least $\chi(H_i)$. $\square$

By Lemma 1, a set of $p_a$ with no conflicts can all be given one function $g|_a$, so on one level the problem is to color $H_i$. Coloring is NP-hard, but the levels interact: the choice on one level changes the partial functions on the lower levels, and the size counts all levels. A reduction must control these effects, which is what the published proof does.

**Trivial bounds.** The optimum is at most $\lvert f \rvert$, since $f$ is feasible, and at least $\max_i \chi(H_i)$ by Lemma 2. For $c = 1$ the only feasible $g$ is $f$, so the problem is easy.

**No guarantee for the heuristics.** Constrain and restrict can return a BDD larger than $f$, and the example above shows a case where both miss the optimum. No approximation ratio is known for any of the heuristics above.

## Reductions

- **From the variable ordering problem.** With $c = 1$ and the order free, the problem is the [variable ordering problem](/variable-ordering/), so the free-order variant is NP-hard by Bollig and Wegener (1996). The fixed-order NP-completeness of Sauerhoff and Wegener is a separate result: it needs the don't cares, since for $c = 1$ and a fixed order the problem is trivial.
- **Relation to graph coloring.** By Lemmas 1 and 2, minimizing the nodes of one level is coloring the conflict graph of the partial subfunctions.
- **To the generalized cofactor.** Constrain and restrict are fast feasible answers: each returns a $g$ in the interval, so it is an upper bound for the optimum when it is smaller than $f$.

## Applications

- **Reachability.** In breadth-first [symbolic reachability](/symbolic-reachability/), the next image only needs a set $S$ with $F \le S \le R$, where $F$ is the frontier and $R$ is the set reached so far. Restrict$(F, \neg R \vee F)$ picks a small such $S$.
- **Image computation and transition relations.** The next-state functions of a circuit need to be right only on the reachable states, so they are simplified with that care set before image computation.
- **Logic synthesis.** Don't cares from the environment of a block, such as unreachable states or unobservable outputs, allow smaller multi-level circuits; BDDs of the simplified functions guide the synthesis.
- **Verification by cases.** When a property is checked under an assumption $c$, simplify the BDDs with care set $c$ first.

## References
