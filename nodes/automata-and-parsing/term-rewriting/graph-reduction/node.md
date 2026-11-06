---
tag: 76B256
kind: technique
slug: graph-reduction
name: Graph reduction
aliases:
- graph-based lazy evaluation
area: automata-and-parsing/term-rewriting
level: advanced
summary: Implements lambda and functional evaluation by sharing subterms as graph nodes.
prereqs: [term-rewriting-system, outermost-reduction, term-dag]
see_also: [term-graph-rewriting, combinatory-logic, beta-reduction, innermost-reduction, reduction-strategy, hash-consing, cheney-copying-collector, lambda-calculus]
sources:
  - book: isbn:9780134533339
    title: Simon L. Peyton Jones, The Implementation of Functional Programming Languages, Prentice Hall, 1987
    locator: Part II, Graph reduction, Chapters 10 to 12 (program representation as a graph, selecting the next redex, graph reduction of lambda expressions with indirection nodes), and Chapter 18 on the G-machine
  - paper: doi:10.1007/3-540-17945-3_8
    title: Hendrik P. Barendregt, Marko C. J. D. van Eekelen, John R. W. Glauert, J. Richard Kennaway, Marinus J. Plasmeijer and M. Ronan Sleep, Term graph rewriting, PARLE Parallel Architectures and Languages Europe, Lecture Notes in Computer Science 259 (1987)
    locator: pp. 141 to 158 (term graphs, graph rewriting of term rewrite rules, soundness with respect to term rewriting, and the orthogonal case)
  - paper: doi:10.1002/spe.4380090105
    title: David A. Turner, A new implementation technique for applicative languages, Software, Practice and Experience 9(1) (1979)
    locator: pp. 31 to 49 (combinator graphs, reduction by overwriting the root of the redex, and cyclic graphs for recursion)
  - paper: doi:10.1145/502874.502880
    title: Thomas Johnsson, Efficient compilation of lazy evaluation, Proceedings of the 1984 SIGPLAN Symposium on Compiler Construction
    locator: pp. 58 to 69 (the G-machine, compiling graph reduction to code)
  - paper: doi:10.1017/S0956796800000319
    title: Simon L. Peyton Jones, Implementing lazy functional languages on stock hardware, the Spineless Tagless G-machine, Journal of Functional Programming 2(2) (1992)
    locator: pp. 127 to 202
---

**Graph reduction** evaluates an expression by rewriting a graph instead of a tree. A subexpression that occurs in several places is stored once, as a node with several pointers to it. Each rewrite step overwrites the root node of the redex with its result, so every place that uses the node sees the result, and the work is done once. Wadsworth introduced the idea in 1971 for the [lambda calculus](/lambda-calculus/), to get call by need: arguments are evaluated only when needed, as in [outermost reduction](/outermost-reduction/), and at most once, as in [innermost reduction](/innermost-reduction/). It is the basis of the implementations of lazy functional languages such as Miranda and Haskell, through Turner's combinator machine, the G-machine and the STG machine. For first-order [term rewriting systems](/term-rewriting-system/) the same method is called [term graph rewriting](/term-graph-rewriting/).

## In plain words

When a rule copies an argument, for example "double of x is x plus x", a rewriter that works on trees makes two copies of x. If x is not yet computed, the work to compute it is now done twice, and a copy of a copy is done four times.

Graph reduction does not copy. It draws the expression as boxes joined by arrows, and both places that use x point to the same box. When the box is computed, the new value is written into that box, so all arrows to it see the value at once.

So you can delay work until it is needed, which avoids work whose result is never used, and still do each piece of work only once.

## When it applies

- **The rules copy arguments.** A rule is duplicating when a variable occurs more often on the right side than on the left, as in $dbl(x) \to add(x, x)$, the rule $S\,x\,y\,z \to x\,z\,(y\,z)$ of [combinatory logic](/combinatory-logic/), or a [beta step](/beta-reduction/) whose bound variable occurs twice. Without copying rules, sharing saves nothing.
- **The strategy is outermost.** Outermost reduction on trees can copy an unevaluated argument and then evaluate each copy. Innermost reduction evaluates arguments before they are copied, but it does work for arguments that are later erased, and it can run forever where outermost reduction stops. Graph reduction with an outermost strategy avoids both costs.
- **The value of a node does not depend on where it is used.** Overwriting a shared node is correct only if every user would have computed the same result. This holds for confluent systems and for pure functional programs, which have no side effects.
- **The system is left-linear,** or the matcher can test the equality of shared subgraphs. For a left side such as $eq(x, x)$, two different nodes can stand for equal terms.

## The template

We use the notation of the term rewriting pages: a signature $\Sigma$, variables $V$, terms $T(\Sigma, V)$, rules $l \to r$, positions as sequences of positive integers, substitutions $\sigma$, and $\to^*$ for the reflexive transitive closure.

**Term graphs.** A **term graph** is a finite set of nodes and a root node. Each node $n$ is either a **function node**, with a label $f \in \Sigma$ and a list of $k$ successor nodes when $f$ has arity $k$, or an **indirection** to one other node. The **unravelling** $U(n)$ is the term read off by following the pointers: $U(n) = f(U(n_1), \ldots, U(n_k))$ for a function node, and $U(n) = U(m)$ for an indirection to $m$. In this page the graphs are acyclic, so unravellings are finite. A rule $l \to r$ **matches** at a node $n$ with a map $\sigma$ from the variables of $l$ to nodes if the unravelling of the pattern instance is $U(n)$, that is, if $l$ with each variable $x$ replaced by $U(\sigma(x))$ equals $U(n)$; the matcher follows indirections and does not copy.

```pseudo id=main
GRAPH-NORMALIZE(root, R)
L1  loop
L2      find the first node n, in a depth-first walk from root that visits each node once, and a rule l → r of R that matches at n with σ          ▷ hole: the strategy
L3      if there is none then return root
L4      if r is a variable x then
L5          make n an indirection to σ(x)
L6      else
L7          build a new node for each non-variable proper subterm of r, with σ(x) for each variable x, and no copies of σ(x)
L8          overwrite n with the label of r and the successor list of its new root
```

The hole is the strategy of line L2. The leftmost-outermost choice gives lazy evaluation when the walk stops at the first redex on the path of the evaluation, as functional language implementations do for the head of the expression. Lines L7 and L8 are the point of the method: the redex node is updated in place, so that all its users see the result, and the arguments are shared, never copied. An indirection in line L5 keeps the sharing when the result is an existing node; copying the content of $\sigma(x)$ into $n$ instead would create two nodes for one value and could duplicate later work.

**Why it is sound.** Let a step contract the redex at node $n$ in an acyclic graph with root $\rho$, and let $P$ be the set of positions $p$ of $U(\rho)$ whose path from $\rho$ ends at $n$.

**Lemma.** $U(\rho) \to^+ U'(\rho)$, where $U'$ is the unravelling after the step, by contracting the redex $U(n)$ at every position of $P$. Moreover, $U(\rho)$ is a normal form if and only if no rule matches at any node.

*Proof.* $P$ is not empty, because $n$ is reachable from $\rho$ (line L2 finds it in a walk from $\rho$). No position in $P$ is a proper prefix of another: if $p$ and $pq$ with $q \neq ()$ both led to $n$, then the path $q$ would lead from $n$ to $n$, a cycle. So the positions of $P$ are parallel, and the subterm at each of them is $U(n) = l\tau$, where $\tau(x) = U(\sigma(x))$. After the step, the new content of $n$ unravels to $r\tau$: in line L5 this is $U(\sigma(x)) = x\tau$, and in lines L7 and L8 the new nodes unravel to the subterms of $r$ with $x\tau$ at each variable. No other node changes its label or successors, and the nodes $\sigma(x)$ are reachable from $n$ and do not reach $n$ (no cycles), so their unravellings do not change. So $U'(\rho)$ is $U(\rho)$ with $l\tau$ replaced by $r\tau$ at every position of $P$, and these are $|P| \ge 1$ rewrite steps at parallel positions. For the second claim, every position of $U(\rho)$ is the end of a path from $\rho$ to some node $m$, and the subterm there is $U(m)$. By the definition of matching, a rule applies to that subterm if and only if it matches at $m$. $\blacksquare$

So every graph step is a sequence of term steps, a stop in line L3 gives a [normal form](/normal-form/) of the start term, and in a confluent system it is the normal form. One graph step does the work of all the copies of the redex at once. Barendregt and others (1987) prove soundness in general, and study when graph reduction also finds every normal form; for orthogonal systems it does.

**Cost.** One step costs the size of the right side plus the matching, and the redex search can be made incremental with a stack of the nodes on the current path (the spine). The space that becomes unreachable after a step is reclaimed by a garbage collector, such as a [copying collector](/cheney-copying-collector/).

## Classic examples

The step counts below were computed by a program that runs three strategies to normal form on the same term: leftmost-innermost on trees, leftmost-outermost on trees, and leftmost-outermost on graphs as in the template.

**Doubling.** Take the rules $dbl(x) \to add(x, x)$, $add(0, y) \to y$ and $add(s(x), y) \to s(add(x, y))$, and the term $dbl^k(s(0))$, whose normal form is $s^{2^k}(0)$.

| $k$ | innermost on trees | outermost on trees | outermost on graphs |
| --- | --- | --- | --- |
| 1 | 3 | 3 | 3 |
| 2 | 7 | 10 | 7 |
| 3 | 13 | 26 | 13 |
| 4 | 23 | 62 | 23 |

Outermost reduction on trees copies the unevaluated $dbl^{k-1}(s(0))$ and evaluates both copies, so its cost roughly doubles with each $k$. On graphs, the two arguments of $add$ are one node, evaluated once, and the count equals the innermost count $2k + 2^k - 1$: one step for each $dbl$, and $2^j + 1$ steps for the addition of two copies of $2^j$.

**Erasing.** With $first(x, y) \to x$ and $loop \to loop$, the term $first(0, loop)$ has the normal form $0$, reached in one outermost step on trees or graphs. Innermost reduction rewrites $loop$ forever. Graph reduction keeps this advantage of outermost reduction and adds the sharing.

**Combinators.** In Turner's method a program is compiled to a combinator graph. The rule $S\,f\,g\,x \to f\,x\,(g\,x)$ builds two application nodes whose argument pointers both point to the one node of $x$, so $x$ is evaluated at most once. The node of the redex $S\,f\,g\,x$ is overwritten with the new application, so other references to it see the result.

**Recursion as a cycle.** The fixed point rule $Y\,f \to f\,(Y\,f)$ can be implemented by overwriting the node of $Y\,f$ with the application of $f$ to that same node. The graph becomes cyclic, it unravels to the infinite term $f\,(f\,(f\,\ldots))$, and repeated unfolding uses constant space.

**Checks.** We made 150 random left-linear, non-overlapping constructor systems over $f/1$, $h/2$ and constructors $c/1$, $a$, $b$. The systems include 38 empty systems and duplicating and erasing rules. We reduced 3 random ground terms per system. In all 405 runs that stopped within a step bound of 300, the graph strategy reached the same normal form as leftmost-outermost reduction on trees and never used more steps. In 6 of these runs it used fewer steps. We set aside 45 runs that did not stop within the bound, or that grew too large.

## Variations

- **Template instantiation.** The simplest implementation: line L7 copies the body of a function definition, a template, with pointers to the arguments. Peyton Jones (1987) develops it for the lambda calculus and for supercombinators, the functions without free variables that lambda lifting produces.
- **Compiled graph reduction.** The G-machine (Johnsson, 1984) compiles each function into code that builds its result graph, instead of interpreting the template. The Spineless Tagless G-machine of the Glasgow Haskell Compiler (Peyton Jones, 1992) avoids building the spine of applications and updates a node only when it may be shared.
- **Maximal sharing.** [Hash-consing](/hash-consing/) shares every pair of equal subterms, so the graph is a minimal [term DAG](/term-dag/). This makes equality tests constant time, which helps non-left-linear rules, at the cost of a hash table lookup for each new node.
- **Parallel graph reduction.** Different redexes of a graph can be reduced on different processors, with care for nodes that several processors may want to evaluate at once.
- **Optimal reduction.** For the lambda calculus, sharing of subterms is not enough to avoid all copying of work inside function bodies. Lamping's algorithm, based on Lévy's notion of optimal reduction, shares such work too, with a more complex graph.

## Pitfalls

- **Returning a new node instead of updating the old one.** If a step builds the result elsewhere and only the parent pointer is changed, other users of the redex node still see the redex, and the work is done again.
- **Copying the content of an existing node.** For a rule $r = x$, copying the node $\sigma(x)$ into the redex node creates two nodes with the same value but separate futures. Use an indirection, and remove indirections later during garbage collection.
- **Pointer equality for non-linear rules.** Two distinct nodes can have equal unravellings. Testing $eq(x, x)$ by pointer equality misses matches; test the unravellings, or use maximal sharing.
- **Side effects.** Updating a shared node is correct only when the value of the node is the same for all users. A language with side effects that are performed during evaluation breaks this.
- **Space leaks.** A shared node that is kept reachable by an unevaluated expression keeps its whole subgraph alive. Lazy programs can use far more memory than the step count suggests.
- **Deep recursion.** The walk of line L2 and the garbage collector should use an explicit stack or pointer reversal, because graphs can be very deep.

## Exercises

1. Prove that on the doubling example the graph strategy takes $2k + 2^k - 1$ steps for $dbl^k(s(0))$.
2. Show a graph and a rule where copying the content of $\sigma(x)$ in line L5, instead of using an indirection, makes the graph reduction do more steps.
3. For a cyclic graph, explain why the proof of the lemma fails, and give a rule and a cyclic graph where one graph step corresponds to infinitely many term steps.
4. Give a non-left-linear rule and a term graph where pointer equality and equality of unravellings give different results.

## References
