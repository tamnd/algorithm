---
tag: MBVMJN
kind: model
slug: read-once-branching-program
name: Read-once branching program
aliases:
- read-once BP
area: logic-and-constraints/binary-decision-diagrams
level: advanced
summary: A branching program in which every path tests each variable at most once. It is the same model as the free BDD (FBDD), and it is strictly stronger than the OBDD.
prereqs: [branching-program, binary-decision-diagram, ordered-binary-decision-diagram]
see_also: [free-binary-decision-diagram, ordered-binary-decision-diagram, branching-program, decision-tree, hidden-weighted-bit-lower-bound, multiplier-bdd-lower-bound, polynomial-identity-testing, model-counting]
sources:
  - book: isbn:9780898714586
    title: Ingo Wegener, Branching Programs and Binary Decision Diagrams, Theory and Applications, SIAM, 2000
    locator: Chapter 6, Free BDDs (FBDDs) and read-once BPs
  - paper: "Manuel Blum, Ashok K. Chandra, Mark N. Wegman, Equivalence of free Boolean graphs can be decided probabilistically in polynomial time, Information Processing Letters 10(2), 1980, pages 80 to 82"
    title: Equivalence of free Boolean graphs can be decided probabilistically in polynomial time
    locator: the randomized equivalence test by arithmetization
  - paper: "Jordan Gergov, Christoph Meinel, Efficient Boolean manipulation with OBDD's can be extended to FBDD's, IEEE Transactions on Computers 43(10), 1994, pages 1197 to 1209"
    title: Efficient Boolean manipulation with OBDD's can be extended to FBDD's
    locator: graph orders (types) and polynomial operations on FBDDs of one type
  - paper: "Detlef Sieling, Ingo Wegener, Graph driven BDDs, a new data structure for Boolean functions, Theoretical Computer Science 141, 1995, pages 283 to 310"
    title: Graph driven BDDs, a new data structure for Boolean functions
    locator: graph-driven BDDs and the polynomial size of the hidden weighted bit function
  - book: isbn:9780201038040
    title: Donald E. Knuth, The Art of Computer Programming, Volume 4A, Combinatorial Algorithms Part 1, 2011
    locator: Section 7.1.4, Binary decision diagrams (free BDDs in the exercises)
---

A read-once branching program is a [branching program](/branching-program/) in which no path tests a variable twice. As a data structure it is called a free BDD, or FBDD; see [free binary decision diagram](/free-binary-decision-diagram/) for the reduction rules and the operations. The model sits between [OBDDs](/ordered-binary-decision-diagram/), which also fix one order of the variables for all paths, and general branching programs, which may test a variable many times. Many questions that are easy for OBDDs stay easy for read-once programs, for example satisfiability and counting. Equivalence has a randomized polynomial test, but no deterministic polynomial algorithm is known. The model is exponentially stronger than OBDDs: the [hidden weighted bit function](/hidden-weighted-bit-lower-bound/) has read-once programs of quadratic size, but only exponential OBDDs.

## The machine

A **branching program** over the variables $x_1, \ldots, x_n$ is a directed acyclic graph with one source, the root. Each sink has a label 0 or 1. Each other node $v$ has a label $\mathrm{var}(v) \in \{1, \ldots, n\}$ and two outgoing edges, the 0-edge to $\mathrm{lo}(v)$ and the 1-edge to $\mathrm{hi}(v)$. On an input $a \in \{0, 1\}^n$, the **computation path** starts at the root, and at a node $v$ it follows the $a_{\mathrm{var}(v)}$-edge. The program computes the label of the sink where the path ends.

A **path** of the graph is any directed path from the root, whether or not an input follows it. The program is **read-once** if every path of the graph contains at most one node with label $i$, for each $i$. This is the *syntactic* condition, and it is the standard meaning of "read-once branching program" and of "free BDD". In this encyclopedia the two names denote the same model.

The weaker *semantic* condition only asks that every computation path tests each variable at most once. A path that tests $x_i$ twice, and takes the 0-edge the first time and the 1-edge the second time, is *inconsistent*: no input follows it. A semantic read-once program may contain such paths, and a syntactic one may not. Syntactic read-once implies semantic read-once; the converse is false.

**Example.** The program with the nodes

- $u$: tests $x_1$, with $\mathrm{lo}(u) = v$ and $\mathrm{hi}(u) = w$;
- $v$: tests $x_2$, with $\mathrm{lo}(v) = 0$ and $\mathrm{hi}(v) = w'$;
- $w$: tests $x_3$, with $\mathrm{lo}(w) = 0$ and $\mathrm{hi}(w) = w'$;
- $w'$: tests $x_4$, with $\mathrm{lo}(w') = 0$ and $\mathrm{hi}(w') = 1$

computes $(\neg x_1 x_2 \vee x_1 x_3) \wedge x_4$. Every path tests each variable at most once, so it is read-once. The two paths through $v$ and $w$ test $x_2$ and $x_3$ in different places, so no single order of the variables fits both, but the node $w'$ is shared.

**OBDDs as a special case.** A read-once program is an OBDD for the order $\pi$ if every edge goes from a variable to a later variable in $\pi$. Then each path tests the variables in the order $\pi$, which is the read-once condition with one order for all paths.

## What it counts

The **size** of a program is its number of nodes, with the sinks. This is the space of the data structure and the measure of all lower bounds in the model. The **length** of a computation path is at most $n$, since the path tests each variable at most once, so evaluation takes $O(n)$ steps.

A read-once program can also be read as a test of a single input, or as a description of the set of inputs that it accepts. The second view gives the algorithmic questions below; each has its cost given in the size $|G|$ of the program.

**Theorem (consistent paths).** In a syntactic read-once program, every path from the root to a sink is followed by some input. So the program computes the constant 0 if and only if no 1-sink is reachable from the root.

*Proof.* Let the path test the variables $x_{i_1}, \ldots, x_{i_k}$ and take the edges $b_1, \ldots, b_k$. The indices are distinct by the read-once condition, so the partial assignment $x_{i_j} = b_j$ is consistent. Any input that extends it follows the path. $\square$

So satisfiability takes $O(|G|)$ time by a graph search. For semantic read-once programs this argument fails, since an inconsistent path may reach the 1-sink while no input does.

**Theorem (counting).** For a syntactic read-once program, let $p(v)$ be the probability that a uniformly random input, started at $v$, reaches the 1-sink. Then $p(1) = 1$, $p(0) = 0$, and $p(v) = \tfrac12 p(\mathrm{lo}(v)) + \tfrac12 p(\mathrm{hi}(v))$ for inner nodes. The number of satisfying inputs is $2^n p(\mathrm{root})$, and the program computes all values in $O(|G|)$ arithmetic operations.

*Proof.* At $v$, the input takes the 0-edge or the 1-edge with probability $\tfrac12$ each, depending on $a_{\mathrm{var}(v)}$. No path below $v$ tests $x_{\mathrm{var}(v)}$ again, so the event of reaching the 1-sink from the child depends only on the other variables, and it is independent of $a_{\mathrm{var}(v)}$. This gives the recurrence. $\square$

This is the same computation as [BDD satisfy-count](/bdd-satisfy-count/), without the factors for skipped levels. It is the basis of [model counting](/model-counting/) with decision diagrams.

## Relation to other models

- **Decision trees.** A [decision tree](/decision-tree/) in which no path tests a variable twice is a read-once program whose graph is a tree. Every function has one with $2^{n+1} - 1$ nodes. Read-once programs can share subgraphs, so they can be exponentially smaller.
- **OBDDs.** Every OBDD is a read-once program. The converse fails by an exponential factor: the hidden weighted bit function has a read-once program with at most $n(n+1)$ inner nodes and needs about $2^{n/5}$ nodes in every OBDD.
- **Read-$k$ programs and general branching programs.** A read-$k$ program allows each variable at most $k$ times on a path. General branching programs have no limit, and their size is closely related to space complexity. Each step of this chain is strictly stronger for some explicit functions.
- **Graph-driven BDDs.** A *graph order* (or *type*) is a read-once program with a single sink in which every path from the root to the sink tests every variable exactly once. It fixes the order of the variables as a function of the bits read so far. A read-once program *respects* the graph order if on every input it tests the variables in the order that the graph order gives for that input. Gergov and Meinel (1994) and Sieling and Wegener (1995) showed that for a fixed graph order, the reduced program is canonical, and the operations of OBDDs, such as [apply](/bdd-apply/), run in polynomial time. OBDDs are the case of a graph order that is a single chain.
- **Nondeterministic and parity programs.** Allowing nodes that guess, or that sum their two children modulo 2, gives other models with their own lower bounds.

## Known results in the model

- **Evaluation, satisfiability, counting.** $O(n)$, $O(|G|)$ and $O(|G|)$ arithmetic operations, by the two theorems above.
- **Equivalence.** Blum, Chandra and Wegman (1980) gave a randomized test. Replace each node by a polynomial: the sinks are 0 and 1, and a node $v$ testing $x_i$ is $(1 - x_i)\, P(\mathrm{lo}(v)) + x_i\, P(\mathrm{hi}(v))$. For a read-once program the root polynomial is multilinear, and it agrees with the function on $\{0, 1\}^n$. Two multilinear polynomials that agree on $\{0, 1\}^n$ are equal, so two programs compute the same function if and only if their polynomials are equal. Evaluate both at a random point of $S^n$ for a large finite field; by the [Schwartz-Zippel lemma](/schwartz-zippel-lemma/), different polynomials agree there with probability at most $n/|S|$. This is an instance of [polynomial identity testing](/polynomial-identity-testing/). No deterministic polynomial algorithm for the equivalence of two read-once programs is known.
- **Operations.** Negation is easy: exchange the sinks. The conjunction of two read-once programs can need exponential size when their orders conflict, and deciding whether it is satisfiable is [NP-complete](/np-complete/), even for two OBDDs with different orders. *Proof.* Take a CNF formula and give each occurrence of a variable its own new variable. The first OBDD checks that every clause has a true literal; the clauses use disjoint new variables, so with the order clause by clause it has linear size. The second OBDD checks that all copies of each old variable are equal; with the order variable by variable it also has linear size. The conjunction is satisfiable if and only if the formula is. $\square$ With one fixed graph order, the operations are polynomial, as for OBDDs.
- **Lower bounds.** Exponential lower bounds for explicit functions in this model were among the first lower bounds for branching programs; early ones are due to Žák (1984) and Wegener (1988). The middle bit of [integer multiplication](/multiplier-bdd-lower-bound/) needs exponential size even here, by results of Ponzio (1995) and Bollig and Woelfel (2001). The standard method is a cut argument: in a read-once program, the subfunctions reached after a fixed set of tests on many paths must be distinct, and an explicit function can force many of them.
- **Upper bounds.** The hidden weighted bit function has read-once programs of size $O(n^2)$, and so do many functions that are hard for OBDDs because no single order suits all inputs.

## References
