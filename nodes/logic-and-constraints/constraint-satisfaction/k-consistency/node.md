---
tag: NP38DP
kind: concept
slug: k-consistency
name: k-consistency
aliases:
- strong k-consistency
- i-consistency
area: logic-and-constraints/constraint-satisfaction
level: advanced
summary: Any consistent assignment to k-1 variables can be extended to any k-th variable; strong k-consistency holds for all levels up to k.
prereqs: [path-consistency, arc-consistency]
see_also: [node-consistency, freuder-theorem, singleton-arc-consistency, bucket-elimination, csp-dichotomy-theorem, constraint-language-polymorphisms, datalog, treewidth]
sources:
  - paper: "Eugene C. Freuder, Synthesizing constraint expressions, Communications of the ACM 21(11), 1978, pages 958 to 966"
    locator: the definition of k-consistency and an algorithm that adds constraints of increasing arity until the network is globally consistent
  - paper: doi:10.1145/322290.322292
    title: Eugene C. Freuder, A sufficient condition for backtrack-free search, Journal of the ACM 29(1), 1982
    locator: pages 24 to 32 (strong k-consistency, and backtrack-free search when the width is less than k)
  - paper: "Martin C. Cooper, An optimal k-consistency algorithm, Artificial Intelligence 41(1), 1989, pages 89 to 95"
    locator: an algorithm that enforces k-consistency in O(n^k d^k) time, which is optimal
  - book: isbn:9781558608900
    title: Rina Dechter, Constraint Processing, Morgan Kaufmann, 2003
    locator: Chapter 3 (i-consistency and strong i-consistency) and Chapter 4 (directional i-consistency and adaptive consistency)
  - paper: doi:10.1137/S0097539794266766
    title: Tomás Feder and Moshe Y. Vardi, The computational structure of monotone monadic SNP and constraint satisfaction, a study through Datalog and group theory, SIAM Journal on Computing 28(1), 1998
    locator: pages 57 to 104 (bounded width, its link with Datalog programs, and the dichotomy conjecture)
  - paper: doi:10.1145/2556646
    title: Libor Barto and Marcin Kozik, Constraint satisfaction problems solvable by local consistency methods, Journal of the ACM 61(1), 2014
    locator: the characterization of the constraint languages of bounded width
---

$k$-consistency is a local consistency of a [constraint satisfaction problem](/constraint-satisfaction-problem/): every consistent assignment to any $k - 1$ variables can be extended to any $k$-th variable so that the larger assignment is still consistent. A problem is strongly $k$-consistent if it is $j$-consistent for every $j \le k$. Freuder (1978) defined the hierarchy, whose first levels are [node consistency](/node-consistency/) ($k = 1$), [arc consistency](/arc-consistency/) ($k = 2$) and [path consistency](/path-consistency/) ($k = 3$). Strong $n$-consistency means that a search finds a solution without backtracking, and by [Freuder's theorem](/freuder-theorem/) strong $(w+1)$-consistency is enough when the constraint graph has width $w$.

## In plain words

Pick any few unknowns and give them values that break no rule among themselves. $k$-consistency says: whatever such choice you make for one fewer than $k$ unknowns, any other unknown can still get a value that fits. With $k = 2$ this is the "every value has a partner" rule of arc consistency. With larger $k$ the test looks at more unknowns at once and catches more dead ends.

If the test holds for all sizes up to the number of unknowns, you can choose values one at a time and never get stuck. Making a problem $k$-consistent costs time that grows like the number of unknowns to the power $k$, and it can add new rules on groups of $k - 1$ unknowns.

## The idea

**Notation.** $n$ variables, $m$ constraints, domains of size at most $d$, and $k$ the consistency level. A partial assignment to a set $Y$ of variables is *consistent* if it satisfies every constraint whose scope lies inside $Y$ (unary constraints included).

**Definition (Freuder 1978).** A CSP is *$k$-consistent* if for every set $Y$ of $k - 1$ variables, every consistent assignment to $Y$, and every variable $x \notin Y$, there is a value $a \in D_x$ such that the assignment extended by $x = a$ is consistent. It is *strongly $k$-consistent* if it is $j$-consistent for $j = 1, \ldots, k$. 1-consistency asks that each domain have a value satisfying the unary constraints; on node consistent domains, 2-consistency is arc consistency and 3-consistency is path consistency.

**$k$-consistency does not imply $(k-1)$-consistency.** Take $x, y, z \in \{0, 1\}$ with $R_{xy} = R_{xz} = \{(0, 0), (0, 1)\}$ and no constraint on $y, z$. Every consistent pair extends to the third variable: a pair with $x = 0$ extends by $0$, and any pair of $y, z$ extends by $x = 0$. So the problem is 3-consistent. The value $x = 1$ is a consistent assignment of one variable that does not extend to $y$, so it is not 2-consistent. This is why results use *strong* consistency.

**Backtrack-free search.** Let the variables be ordered $x_1, \ldots, x_n$, and let a search assign them in this order, each time choosing a value consistent with the earlier ones. The search is *backtrack-free* if it never meets a variable with no such value.

> **Proposition.** If a CSP is strongly $n$-consistent and no domain is empty, then for every order a search is backtrack-free and so finds a solution.
>
> *Proof.* The empty assignment is consistent. Assume the first $i - 1$ variables, $i \le n$, have a consistent assignment. By $i$-consistency, with $Y = \{x_1, \ldots, x_{i-1}\}$ of size $i - 1$, the variable $x_i$ has a value that keeps the assignment consistent. After $n$ steps all variables are assigned and every constraint lies inside the assigned set, so the assignment is a solution. $\square$

Such a CSP is called *globally consistent*. [Freuder's theorem](/freuder-theorem/) improves the proposition: if the order has width $w$, strong $(w+1)$-consistency is enough, because each new variable is constrained by at most $w$ earlier ones.

**Enforcing $k$-consistency.** If a consistent assignment to $Y$ does not extend to some $x$, it is a *nogood*, and adding the constraint that forbids it keeps all solutions. Repeating this until no nogood of size $k - 1$ remains gives a $k$-consistent problem. As for arc consistency, the result is unique: the union of $k$-consistent tightenings is $k$-consistent, so there is a largest one. Freuder (1978) built constraints of growing arity this way, and Cooper (1989) gave an algorithm that enforces $k$-consistency in $O(n^k d^k)$ time, which is optimal. The cost is polynomial for fixed $k$, but the added constraints of arity $k - 1$ can change the constraint graph, and with it the width.

**Adaptive consistency.** Along a fixed order, *directional* $i$-consistency asks only that assignments of earlier variables extend to later ones. Enforcing it from the last variable to the first with $i$ adapted to each variable's number of earlier neighbours in the induced graph is [bucket elimination](/bucket-elimination/), whose cost is exponential in the induced width $w^\ast$ and not in $n$.

**Bounded width.** For a fixed constraint language $\Gamma$, CSP($\Gamma$) has *bounded width* if some fixed level of local consistency decides every instance: whenever the closure has no empty constraint, there is a solution. Feder and Vardi (1998) linked bounded width to Datalog programs. Barto and Kozik (2014) proved that a core language has bounded width exactly when it cannot express, in the algebraic sense of [polymorphisms](/constraint-language-polymorphisms/), linear equations over a finite abelian group (its algebra omits types 1 and 2 of tame congruence theory). Horn clauses and 2-SAT have bounded width; linear equations over GF(2) do not, though they are in P by Gaussian elimination.

## Examples

**The hierarchy on 3-colouring.** For graph 3-colouring, the triangle with 3 colours is strongly 3-consistent and has 6 solutions. The complete graph $K_4$ with 3 colours is strongly 3-consistent: each consistent assignment to 2 vertices uses 2 colours and leaves a third colour for any other vertex. It is not 4-consistent: an assignment of 3 different colours to 3 vertices does not extend to the fourth. Since $K_4$ has 4 vertices, strong 4-consistency is global consistency here, and enforcing it deletes every value, which proves that there is no solution.

**Trees.** A tree-shaped binary CSP has an order of width 1, so strong 2-consistency (node and arc consistency) gives backtrack-free search. This is the base of the [tree-structured CSP algorithm](/tree-structured-csp/).

**Linear equations.** Take a graph $G$ in which every vertex has degree 3, put a Boolean variable on each edge, and at each vertex $v$ add the equation that the XOR of its three edge variables is $c_v \in \{0, 1\}$, with $\sum_v c_v$ odd. Each edge variable occurs in two equations, so the XOR of all equations gives $0 = 1$, and there is no solution. Gaussian elimination finds this in polynomial time. If $G$ is a good expander and large compared with $k$, every set of few equations has a solution, and strong $k$-consistency finds no conflict. Feder and Vardi (1998) used such systems to show that linear equations over GF(2) do not have bounded width.

**Binary Boolean constraints.** Each binary relation on $\{0, 1\}$ is closed under the majority operation. So strong 3-consistency, which is strong path consistency, decides 2-SAT, while arc consistency does not.

## Where it is used

- **Theory of tractability.** The levels of $k$-consistency define bounded width, one of the two main algorithmic ideas of the [CSP dichotomy theorem](/csp-dichotomy-theorem/); the other is the few-subpowers or Mal'tsev method, which covers linear equations.
- **Backtrack-free search.** [Freuder's theorem](/freuder-theorem/) uses strong $(w+1)$-consistency on graphs of width $w$, and [bucket elimination](/bucket-elimination/) uses directional consistency to the induced width.
- **Logic and games.** $k$-consistency matches the existential $k$-pebble game and Datalog programs of bounded width, which link CSPs with [Datalog](/datalog/) and finite model theory.
- **Practical solvers.** Solvers seldom go beyond $k = 3$. They use [singleton arc consistency](/singleton-arc-consistency/), [path consistency](/path-consistency/) on small or temporal networks, or nogood learning during search instead.

## References
