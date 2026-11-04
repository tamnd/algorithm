---
tag: 05V44P
kind: concept
slug: certifying-algorithms
name: Certifying algorithms
aliases:
- Certifying algorithm
- Checker-based correctness
area: foundations/correctness-and-invariants
level: research
summary: Algorithms that output both a result and a certificate, together with a simple checker that verifies the result.
prereqs: [correctness, specification, postcondition]
see_also: [program-verification, property-based-testing, bipartite-graph, bellman-ford, negative-cycle, potential-function-reduced-costs, breadth-first-search, planarity-testing]
sources:
  - paper: doi:10.1016/j.cosrev.2010.09.009
    title: Ross M. McConnell, Kurt Mehlhorn, Stefan Näher and Pascal Schweitzer, Certifying algorithms, Computer Science Review 5(2), 2011
    locator: pp. 119 to 161; Section 1 (history), Section 2.1 (bipartiteness), Section 2.4 (shortest path trees), Section 2.6 (the LEDA planarity test), Section 4 (relation to program checking), Sections 5.1 to 5.3 and 5.5 (the definitions, simplicity and checkability), Section 8.2 (linear programming duality)
  - paper: doi:10.1145/200836.200880
    title: Manuel Blum and Sampath Kannan, Designing programs that check their work, Journal of the ACM 42(1), 1995 (first version STOC 1989)
    locator: pp. 269 to 291
  - book: isbn:9780321295354
    title: Jon Kleinberg and Éva Tardos, Algorithm Design
    locator: Section 3.4, Testing bipartiteness (breadth-first search and the odd cycle)
  - book: isbn:9780262046305
    title: Cormen, Leiserson, Rivest and Stein, Introduction to Algorithms, fourth edition
    locator: Chapter 22, Single-source shortest paths (Section 22.1, the Bellman-Ford algorithm, and the properties of relaxation and of the predecessor subgraph)
---

A certifying algorithm is an algorithm that, with each answer, outputs a witness that proves the answer correct for this input. A separate program, the checker, reads the input, the answer and the witness, and accepts only when the witness really proves the answer. The checker is much simpler than the algorithm, so you can prove it correct once, and then you do not need to trust the algorithm. The idea grew out of program checking (Blum and Kannan, 1989) and the checkers that Mehlhorn and Näher added to the LEDA library in the 1990s. McConnell, Mehlhorn, Näher and Schweitzer (2011) survey it.

## In plain words

Think of a clerk who must tell you if a long list of numbers is in order. A clerk who says only "no" asks for your trust. A clerk who says "no" and points to two neighbours in the wrong order gives you a fact that you can check in a second.

A certifying algorithm gives the answer and a proof of it, in a form that a short program can check. If the algorithm has a bug and the answer is wrong, no proof can be right, and the checker finds this.

For a question with a yes or no answer, the algorithm needs a proof for each answer. To tell if a graph can be split into two sides with no edge inside a side, the proof of "yes" is the split, and the proof of "no" is a cycle with an odd number of edges.

## The idea

**Definition.** The definitions follow Section 5 of the survey. A problem is given by an *I/O specification* $(\varphi, \psi)$: the input $x \in X$ must satisfy the [precondition](/precondition/) $\varphi(x)$, and an output $y \in Y$ is correct when the [postcondition](/postcondition/) $\psi(x, y)$ holds. Let $Y^\perp = Y \cup \{\perp\}$, where the answer $\perp$ means "the input violates the precondition". A *witness predicate* is a predicate $W(x, y, w)$ on inputs, answers in $Y^\perp$ and witnesses, with this property.

1. *Witness property.* For all $x$, $y$ and $w$:
$$ (y = \perp \wedge W(x, y, w)) \implies \neg\varphi(x), \qquad (y \in Y \wedge W(x, y, w)) \implies \neg\varphi(x) \vee \psi(x, y). $$
The second line says: if the input is legal, the answer is correct. This is a mathematical statement. It is proved once, and it does not depend on the algorithm.

A *certifying algorithm* for $(\varphi, \psi)$ and $W$ halts on every input $x$ and outputs a pair $(y, w)$ with $W(x, y, w)$. Two variants change the strength of the guarantee.

- *Strongly certifying.* The witness predicate satisfies the stronger implication $(y \in Y \wedge W(x, y, w)) \implies \psi(x, y)$. So each run proves either that the input is illegal or that the answer is correct, and it says which. Binary search on an array that should be sorted is certifying but not strongly certifying: it outputs an index $i$ with $A[i] = z$, or an index with $A[i] < z < A[i+1]$, and this proves the answer only when the array is sorted. To check that the array is sorted costs linear time.
- *Weakly certifying.* The algorithm must halt only on inputs that satisfy $\varphi$. When it halts, its output satisfies $W$.

When $\varphi$ is always true, the three notions are the same. Two more requirements make the idea useful, and they separate a certifying algorithm from an algorithm that is simply run twice.

2. *Checkability.* $W$ is easy to decide. In the examples below a program decides it in time linear in the size of $x$, $y$ and $w$, and the program is short enough to prove correct, or to verify formally.
3. *Simplicity.* The witness property has an elementary proof.

The checker decides $W(x, y, w)$ on the input $x$ that the user gave, the output $y$ and the witness $w$. If it accepts, then $y$ is correct (or the input is illegal), whatever program computed $y$ and $w$. A failed check shows a fault in the algorithm, in its implementation, or in the machine. The user must trust only the witness property and the code of the checker.

**What makes it useful.**

- The checker is simple, often a few lines and a time linear in the size of the input, so it is easier to prove correct, or to test, than the algorithm.
- The checker reads the original input. If the algorithm works on a copy that is wrong, the checker finds it.
- The guarantee is for each run. It is not a proof that the algorithm is correct for all inputs. It is a proof that this answer is correct.
- The checker must be trusted. A fault in the checker, or a witness predicate that is too weak, gives false acceptance.

**Contrast with other ways to get confidence.** A proof of the algorithm with [Hoare logic](/hoare-logic/) or a tool for [program verification](/program-verification/) makes one large proof for all inputs. [Property-based testing](/property-based-testing/) tries many inputs. A program checker in the sense of Blum and Kannan may call the program again on other inputs, may use randomness, and may itself be complex. A certifying algorithm hands over a witness, and its checker is simple and deterministic. It looks like the verifier of the class [NP](/np/), which also checks a [certificate](/certificate/). The difference is that here the algorithm itself must produce the witness, and a witness is needed for both answers.

## Examples

### Bipartiteness

An undirected graph $G = (V, E)$ with no loops is *bipartite* ([bipartite graph](/bipartite-graph/)) when there is a *proper 2-coloring*: a map $c : V \to \{0, 1\}$ with $c(u) \ne c(v)$ for each edge $\{u, v\}$. This is Section 2.1 of the survey.

- *Output "bipartite", witness:* a map $c$.
- *Output "not bipartite", witness:* a list $v_0, \dots, v_{k-1}$ of $k$ distinct vertices with $k$ odd and $k \ge 3$, such that $\{v_i, v_{(i+1) \bmod k}\}$ is an edge for each $i$. This is an *odd cycle*.

*Checker.* For a coloring: test that $c$ assigns a value in $\{0, 1\}$ to every vertex of $V$, and that $c(u) \ne c(v)$ for each edge. For a cycle: test that $k$ is odd and at least 3, that the vertices are distinct, and that each consecutive pair, including the pair $v_{k-1}, v_0$, is an edge. With adjacency lists sorted, or a hash set of the edges, each test takes time linear in the size of $G$ and the witness.

*The witness property.* A coloring that passes the test is a proper 2-coloring, so $G$ is bipartite by definition. Suppose that $G$ has a proper 2-coloring $c$ and also an odd cycle as above. Then $c(v_{i+1}) \ne c(v_i)$ with only two colors, so $c(v_i) = c(v_0)$ when $i$ is even. The index $k - 1$ is even, so $c(v_{k-1}) = c(v_0)$, and this contradicts the edge $\{v_{k-1}, v_0\}$. So a cycle that passes the test proves that $G$ is not bipartite.

*The algorithm.* Run [breadth-first search](/breadth-first-search/) from an unvisited vertex of each component, with parent pointers, and let $\ell(v)$ be the level of $v$. Along an edge, the levels differ by at most 1. If $\ell(u) \not\equiv \ell(v) \pmod 2$ for each edge, output $c(v) = \ell(v) \bmod 2$. Otherwise some edge $\{u, v\}$ has $\ell(u) = \ell(v) = d$, because levels that differ by at most 1 and have equal parity are equal. Both lie in one tree, so the paths in the tree from $u$ and from $v$ to the root meet first at a vertex $a$ with level $d - m$ for some $m \ge 1$ ($m \ge 1$ because $u \ne v$). The two tree paths from $u$ to $a$ and from $v$ to $a$ share only $a$, and each has $m$ edges. With the edge $\{u, v\}$ they form a cycle with $2m + 1$ edges, which is odd. This is the witness. The whole algorithm runs in $O(|V| + |E|)$ time, the same as the plain test of [bipartiteness](/bipartiteness-testing/).

*An instance.* For the 4-cycle with edges $\{0,1\}, \{1,2\}, \{2,3\}, \{3,0\}$ the algorithm outputs $c = (0, 1, 0, 1)$. For the graph with vertices $0, \dots, 4$ and edges $\{0,1\}, \{1,2\}, \{2,0\}, \{2,3\}, \{3,4\}$, a search from 0 puts 1 and 2 on level 1, the edge $\{1, 2\}$ joins two vertices of one level, and the output is the odd cycle $1, 0, 2$, with 3 edges.

### Shortest paths

Let $G = (V, E)$ be a directed graph with at most one edge for each ordered pair, integer weights $w(u, v)$ that may be negative, and a source $s$. Let $\mathrm{dist}(s, v)$ be the infimum of the weights of the walks from $s$ to $v$: it is $\infty$ if there is no walk, and $-\infty$ if the weights have no lower bound. The certifying version of the [Bellman-Ford algorithm](/bellman-ford/) outputs one of two answers. The survey treats the case of positive weights in Section 2.4. The version here allows any integer weights.

- *Distances.* Labels $d(v) \in \mathbb{Z} \cup \{\infty\}$ and a parent $p(v)$ for each vertex $v \ne s$ with $d(v) < \infty$. The claim is that $d(v) = \mathrm{dist}(s, v)$ for each $v$.
- *A [negative cycle](/negative-cycle/)* reachable from $s$: a list of distinct vertices $c_0, \dots, c_{k-1}$ whose edges $(c_i, c_{(i+1) \bmod k})$ form a cycle of total weight below 0, such that $c_0$ is reachable from $s$. The claim is that some distance is $-\infty$.

*The algorithm.* The textbook version returns only a boolean when a negative cycle is reachable. The certifying version runs $|V|$ passes over all edges instead of $|V| - 1$, with $d(s) = 0$ and $d(v) = \infty$ at the start. Each relaxation of an edge $(u, v)$, when $d(u) + w(u, v) < d(v)$, sets $d(v) \leftarrow d(u) + w(u, v)$ and $p(v) \leftarrow u$. If the last pass relaxes no edge, output $d$ and $p$. Otherwise let $x$ be a vertex whose label falls in the last pass. Follow parent pointers from $x$ for $|V|$ steps to a vertex $y$, then follow them from $y$ until $y$ comes back, and output the vertices met, in reverse order.

*Why the output of the algorithm passes the check.* Two facts hold at every moment of the run. (a) For each $v$ with a parent, $d(v) \ge d(p(v)) + w(p(v), v)$: the relaxation that set $p(v)$ made this an equality, later $d(p(v))$ can only fall, and $d(v)$ changes only together with $p(v)$. (b) After pass $i$, $d(v)$ is at most the least weight of a walk from $s$ to $v$ with at most $i$ edges (the path-relaxation property of CLRS, Chapter 22).

- *No relaxation in the last pass.* Then the labels are a fixed point of relaxation: condition 2 below holds. Every finite label other than $d(s)$ was set by a relaxation, so it has a parent. Suppose that the parent pointers had a cycle, and let $(u, v)$ be the parent edge of the cycle that was set last. Just before it was set, $d(v) > d(u) + w(u, v)$, and fact (a) held for the other edges of the cycle. Summing around the cycle gives a weight below 0. But the labels on the cycle are finite, and condition 2 summed around the cycle gives a weight of at least 0, a contradiction. So a parent walk from a vertex with a finite label has no cycle, and it ends at the only such vertex without a parent, $s$. The parent pointers form a tree rooted at $s$, and condition 3 holds with equality because condition 2 and fact (a) together give $d(v) = d(p(v)) + w(p(v), v)$.
- *A relaxation in the last pass.* Suppose that the parent walk from $x$ has no cycle. Then it ends at a vertex with no parent, which is $s$, along $s = u_0, \dots, u_j = x$ with $j \le |V| - 1$. Since $s$ has no parent, it was never relaxed, so $d(s) = 0$, and fact (a) summed along the walk gives $d(x) \ge w(u_0, \dots, u_j)$, which by fact (b) is at least the value of $d(x)$ after pass $|V| - 1$. But $d(x)$ fell in pass $|V|$, a contradiction. So the walk from $x$ enters a cycle of parent pointers, and after $|V|$ steps it is on that cycle. The same sum as in the first case shows that each cycle of parent pointers has weight below 0. Each vertex with a finite label is reachable from $s$, so the cycle is reachable.

*Checker for distances.* Accept when all four conditions hold.

1. $d(s) = 0$.
2. For each edge $(u, v)$: $d(v) \le d(u) + w(u, v)$, where $\infty$ is allowed on both sides. In words, the *reduced cost* $w(u, v) + d(u) - d(v)$ is not negative: the labels are a feasible potential, as in [potential functions and reduced costs](/potential-function-reduced-costs/).
3. For each $v \ne s$ with $d(v) < \infty$: $(p(v), v)$ is an edge and $d(v) = d(p(v)) + w(p(v), v)$. The reduced cost of the parent edge is 0.
4. For each $v \ne s$ with $d(v) < \infty$: following parent pointers from $v$ reaches $s$.

Condition 4 is checked in linear time: build, for each vertex $u$, the list of the vertices $v$ with $p(v) = u$, run a search from $s$ along these lists, and test that it reaches every vertex with a finite label. A vertex that the search misses has a parent walk that ends in a cycle. Checking each vertex by its own walk would cost $\Theta(|V|^2)$ time on a long path.

*The witness property.* Assume that the four conditions hold. Take a vertex $v$.

- If $d(v) < \infty$: following parents from $v$ gives a path $s = u_0, \dots, u_j = v$ by condition 4. Its weight is $\sum (d(u_{i+1}) - d(u_i)) = d(v) - d(s) = d(v)$, because each edge is tight (condition 3). So $\mathrm{dist}(s, v) \le d(v)$. Now take any walk $s = x_0, \dots, x_k = v$ in $G$. By condition 2, $d(x_{i+1}) - d(x_i) \le w(x_i, x_{i+1})$, and the sum is $d(v) - d(s) = d(v) \le$ the weight of the walk. So $d(v) \le \mathrm{dist}(s, v)$. Hence $d(v) = \mathrm{dist}(s, v)$.
- If $d(v) = \infty$: suppose that a walk from $s$ to $v$ exists. All labels on it are finite by condition 2 and induction along the walk, because $d(s) = 0$. This contradicts $d(v) = \infty$. So $\mathrm{dist}(s, v) = \infty$.

The same sum shows that a graph with a negative cycle reachable from $s$ cannot pass the check: the labels on the cycle are finite, and summing condition 2 around the cycle gives $0 \le$ its weight.

*Checker for a negative cycle.* Test that the vertices are distinct, that each consecutive pair $c_i, c_{(i+1) \bmod k}$ is an edge, that the sum of the weights is below 0, and that $c_0$ is reachable from $s$ (by a search). If such a cycle exists, then for each integer $M$ a walk from $s$ to $c_0$ followed by enough turns of the cycle has weight below $-M$, so $\mathrm{dist}(s, c_0) = -\infty$.

*An instance.* Vertices $s, a, b, c$ with edges $(s, a)$ of weight 4, $(s, b)$ of 5, $(a, b)$ of $-2$, $(b, c)$ of 3 and $(a, c)$ of 6. The labels are $d = (0, 4, 2, 5)$, with parents $p(a) = s$, $p(b) = a$, $p(c) = b$. The reduced costs of the five edges, in the order above, are $0, 3, 0, 0, 5$. All are at least 0, and the three parent edges have cost 0. For the graph with edges $(0, 1)$ of weight 1, $(1, 2)$ of $-3$ and $(2, 1)$ of 1 and source 0, the output is the cycle $1, 2$ with weight $-2$.

**Non-examples.**

- *Labels without parents.* In the first instance above, $d = (0, -1, -3, -6)$ passes conditions 1 and 2, but its values are too small. Condition 2 alone gives only $d(v) \le \mathrm{dist}(s, v)$. The tight parent edges in conditions 3 and 4 give the other half.
- *Parents without condition 4.* Take the edges $(s, u)$ of weight 1, and $(u, v)$ and $(v, u)$ of weight 0 (Figure 4 of the survey). The labels $d(s) = d(u) = d(v) = 0$ with $p(u) = v$ and $p(v) = u$ pass conditions 1 to 3, but $\mathrm{dist}(s, u) = 1$. The parent walk from $u$ never reaches $s$, so condition 4 rejects them.
- *A "yes" without a witness.* An algorithm that prints only "bipartite" is not certifying. The user must trust the code.
- *A witness for another input.* A coloring of a different graph proves nothing. The checker must test the witness against the original input.

## Where it is used

- *Graph libraries.* The LEDA library has checkers for its network flow and matching algorithms, for connectivity, for [planarity testing](/planarity-testing/) and for basic geometric algorithms (Section 4 of the survey). Its first planarity test, of 1991, declared some planar graphs non-planar. A user reported a planar graph that it rejected in 1993, and the corrected, certifying test outputs either an embedding in the plane or a [Kuratowski](/kuratowski-theorem/) subgraph (Section 2.6 of the survey).
- *Problems with the same pattern.* A maximum flow with a minimum cut of the same value ([max-flow min-cut theorem](/max-flow-min-cut-theorem/)). A linear program that outputs a primal and a dual solution of equal value ([LP duality](/lp-duality/)), a [Farkas](/farkas-lemma/) certificate of infeasibility, or a feasible point with an improving ray when the program is unbounded. The extended [Euclidean algorithm](/extended-euclidean-algorithm/): the coefficients $x$ and $y$ with $g = xa + yb$, together with the test that $g$ divides $a$ and $b$, prove that $g = \gcd(a, b)$. A [primality certificate](/primality-certificate/) such as a [Pratt certificate](/pratt-certificate/).
- *Testing.* A property such as "the output is sorted and is a permutation of the input" is a checker. A test harness can apply it to each output of a program, as in [property-based testing](/property-based-testing/) and [differential testing](/differential-testing/).

## References
