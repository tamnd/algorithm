---
tag: 6JBPNF
kind: problem
slug: attribute-closure-problem
name: Attribute closure problem
aliases:
- closure of an attribute set
area: systems/database-algorithms
level: core
summary: "Given functional dependencies F and an attribute set X, compute X+, the set of all attributes that X determines under F. It takes linear time."
prereqs: [functional-dependency]
see_also: [attribute-closure-algorithm, armstrongs-axioms, dependency-implication-problem, minimal-cover-problem, horn-sat, horn-sat-forward-chaining, unit-propagation, transitive-closure]
sources:
  - paper: doi:10.1145/320064.320066
    title: Catriel Beeri and Philip A. Bernstein, Computational problems related to the design of normal form relational schemas, ACM Transactions on Database Systems 4(1), 30 to 59 (1979)
    locator: the membership problem for functional dependencies and its linear-time algorithm
  - paper: "W. W. Armstrong, Dependency structures of data base relationships, Information Processing 74 (Proceedings of the IFIP Congress 1974), North-Holland, 580 to 583"
    locator: the inference rules, whose completeness reduces implication to closure
  - book: isbn:9780201537710
    title: Serge Abiteboul, Richard Hull and Victor Vianu, Foundations of Databases, Addison-Wesley (1995)
    locator: Section 8.2 (functional and key dependencies, the closure of a set of attributes)
  - book: isbn:9780881751888
    title: Jeffrey D. Ullman, Principles of Database and Knowledge-Base Systems, Volume I, Computer Science Press (1988)
    locator: Section 7.3 (reasoning about functional dependencies, computing closures)
  - paper: doi:10.1016/0743-1066(84)90014-1
    title: William F. Dowling and Jean H. Gallier, Linear-time algorithms for testing the satisfiability of propositional Horn formulae, Journal of Logic Programming 1(3), 267 to 284 (1984)
    locator: the linear-time forward chaining for Horn clauses with a counter per clause
---

The attribute closure problem asks, for a set $F$ of [functional dependencies](/functional-dependency/) and a set $X$ of attributes, for the set $X^+$ of all attributes $A$ with $F \models X \to A$. Each question about the implication of FDs reduces to it: $F \models X \to Y$ if and only if $Y \subseteq X^+$. Keys, covers and normal form tests all call it many times. The [attribute closure algorithm](/attribute-closure-algorithm/) solves it in time linear in the size of $F$.

## In plain words

You have rules of the form "if you know these columns, you know that column". You start from some known columns. Which columns do you know at the end? Apply each rule whose conditions you already know, add what it gives, and repeat until nothing changes. The answer tells you whether a set of columns is a key: it is a key if you reach all columns. It also tells you whether one rule follows from the others. The problem is easy. The only care needed is to avoid scanning all rules again after each new column.

## Definition

**Input.** A finite attribute set $U$, a set $F = \{X_1 \to Y_1, \ldots, X_m \to Y_m\}$ of FDs over $U$, and a set $X \subseteq U$.

**Output.** The set

$$X^+_F = \{ A \in U : F \models X \to A \}.$$

By [Armstrong's axioms](/armstrongs-axioms/), $X^+_F$ is also the set of $A$ with $F \vdash X \to A$, and it is the least set $C$ with

1. $X \subseteq C$, and
2. for each $X_i \to Y_i$ in $F$, $X_i \subseteq C$ implies $Y_i \subseteq C$.

The input size is $|U| + \|F\|$, where $\|F\| = \sum_i (|X_i| + |Y_i|)$ is the number of attribute occurrences in $F$.

The map $X \mapsto X^+$ is a *closure operator*: $X \subseteq X^+$, $X \subseteq Y$ implies $X^+ \subseteq Y^+$, and $(X^+)^+ = X^+$. The sets $C$ with $C = C^+$ are the *closed sets* of $F$. They are closed under intersection, and they determine $F$ up to equivalence.

## Variants

- **Membership.** Given $F$ and one FD $X \to Y$, decide $F \models X \to Y$. Compute $X^+$ and test $Y \subseteq X^+$. See the [dependency implication problem](/dependency-implication-problem/).
- **Closure of $F$.** Compute $F^+$, the set of all implied FDs. Its size can be exponential: with $F = \emptyset$, the trivial FDs alone number $3^{|U|}$ (each attribute is in $Y$, in $X$ only, or in neither). Algorithms never list $F^+$, and they compute $X^+$ instead. The alias "FD closure" is often used for $F^+$, which is a different object.
- **Many closures of one $F$.** Key finding and cover computation ask for $X^+$ for many sets $X$. The index structures of the linear algorithm (one list of FDs per attribute) can be built once and reused, and only the counters are reset.
- **Closure with other dependencies.** With multivalued dependencies, the analogue is the *dependency basis* of $X$, computed in polynomial time (Beeri 1980). With inclusion dependencies added, implication is undecidable, so there is no closure algorithm.
- **Incremental closure.** Keep $X^+$ while FDs are added to $F$. The counter algorithm handles additions at the cost of the new FD plus the new attributes.

## Examples

Take Ullman's course schema $U = \{C, T, H, R, S, G\}$ (course, teacher, hour, room, student, grade) with

$$F = \{ C \to T,\ HR \to C,\ HT \to R,\ CS \to G,\ HS \to R \}.$$

| $X$ | FDs applied, in order | $X^+$ |
| --- | --- | --- |
| $HS$ | $HS \to R$, $HR \to C$, $C \to T$, $CS \to G$ | $CTHRSG$ |
| $CS$ | $C \to T$, $CS \to G$ | $CTSG$ |
| $HR$ | $HR \to C$, $C \to T$ | $CTHR$ |
| $T$ | none | $T$ |

So $HS$ is a superkey, because $HS^+ = U$. $F \models HR \to T$ holds, because $T \in HR^+$. $F \models CS \to H$ does not hold, because $H \notin CS^+$. The two-tuple relation that agrees exactly on $CTSG$ satisfies $F$ and violates $CS \to H$.

**Edge cases.** If $X = \emptyset$, then $X^+$ holds the attributes forced by FDs with empty left sides, and those that follow from them. If $F = \emptyset$, then $X^+ = X$. If $X = U$, then $X^+ = U$.

## Known algorithms

| algorithm | time | notes |
| --- | --- | --- |
| apply rules to fixpoint, rescanning $F$ | $O(|U| \cdot \|F\|)$ | each pass adds an attribute or stops, so at most $|U| + 1$ passes |
| [attribute closure algorithm](/attribute-closure-algorithm/), counters (Beeri and Bernstein 1979) | $O(|U| + \|F\|)$ | each FD keeps a count of left-side attributes not yet in the closure |
| derive with [Armstrong's axioms](/armstrongs-axioms/) | exponential | lists FDs of $F^+$; useful only as a definition |

The naive fixpoint is often fast in practice, because few passes are needed. Its worst case is a chain $A_1 \to A_2, \ldots, A_{n-1} \to A_n$ listed in reverse order, which needs one pass per attribute. The counter algorithm visits each occurrence of an attribute in a left side once.

## Bounds

- **Upper bound.** $O(|U| + \|F\|)$ time on a RAM, by the counter algorithm.
- **Lower bound.** $\Omega(|U| + \|F\|)$ in general. An algorithm that does not read some FD $V \to B$ cannot tell whether $V \subseteq X^+$ makes $B$ part of the answer. So the linear algorithm is optimal up to a constant factor.
- **Parallel complexity.** The problem is P-complete under logarithmic-space reductions, because Horn satisfiability is (see the reductions below). So a fast parallel algorithm for it is unlikely.

## Reductions

**To and from Horn satisfiability.** Map each attribute to a propositional variable, each FD $A_1 \cdots A_k \to B$ to the [Horn clause](/horn-clause/) $A_1 \wedge \cdots \wedge A_k \Rightarrow B$, and each $A \in X$ to the fact $A$. Then $X^+$ is the set of variables that are true in the least model of these clauses. In the other direction, a Horn formula is unsatisfiable if and only if a new attribute $\bot$ is in $\emptyset^+$, where each fact $p$ becomes $\emptyset \to p$ and each goal clause $\neg p_1 \vee \cdots \vee \neg p_k$ becomes $p_1 \cdots p_k \to \bot$. Both maps take linear time. The counter algorithm is the same as [forward chaining for Horn-SAT](/horn-sat-forward-chaining/) of Dowling and Gallier (1984), and the propagation step is [unit propagation](/unit-propagation/).

**Graph reachability.** If each left side has one attribute, the FDs form a directed graph on $U$, and $X^+$ is the set of nodes reachable from $X$. This is a [breadth-first search](/breadth-first-search/). Left sides with several attributes make it a reachability problem in a directed hypergraph, where an edge fires only when all its tail nodes are reached. The [transitive closure](/transitive-closure/) of the graph answers all single-attribute closures at once.

## Applications

- **Implication and equivalence.** $F \models X \to Y$ if $Y \subseteq X^+$. Two FD sets $F$ and $G$ are equivalent if each FD of one is implied by the other.
- **Keys.** $X$ is a superkey if $X^+ = U$. A key is found by removing attributes from $U$ while the closure stays $U$, with $|U|$ closure calls.
- **Minimal covers.** The [minimal cover](/minimal-cover-problem/) algorithm tests each attribute of each left side, and each FD, with one closure.
- **Normal forms.** The tests for [third normal form](/third-normal-form/) and [Boyce-Codd normal form](/boyce-codd-normal-form/) check whether left sides are superkeys. The [3NF synthesis](/third-normal-form-synthesis/) algorithm uses closures to find a key.
- **Query optimization.** An optimizer uses the FDs of the input relations to remove redundant grouping columns and sort keys: if $A \in X^+$, then grouping by $X$ and by $XA$ is the same.

## References
