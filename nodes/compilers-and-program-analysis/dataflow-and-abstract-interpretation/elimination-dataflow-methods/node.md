---
tag: 9STKDE
kind: technique
slug: elimination-dataflow-methods
name: Elimination methods for dataflow analysis
aliases:
- Allen-Cocke interval analysis
- interval-based dataflow analysis
area: compilers-and-program-analysis/dataflow-and-abstract-interpretation
level: advanced
summary: Solve dataflow equations by substitution, like Gaussian elimination, with functions as coefficients and a loop closure in place of division.
prereqs: [distributive-dataflow-framework, reducible-flow-graph, gen-kill-problem]
see_also: [worklist-dataflow-algorithm, kam-ullman-iteration-bound, mop-mfp-coincidence-theorem, gaussian-elimination, state-elimination, floyd-warshall, loop-nesting-forest, interval-domain]
sources:
  - paper: doi:10.1145/360018.360025
    title: "Frances E. Allen and John Cocke, A program data flow analysis procedure, Communications of the ACM 19(3), 1976, 137-147"
    locator: the whole paper (intervals of a flow graph, the derived graph, and the dataflow solution computed interval by interval)
  - paper: doi:10.1145/321921.321939
    title: "Susan L. Graham and Mark Wegman, A fast and usually linear algorithm for global flow analysis, Journal of the ACM 23(1), 1976, 172-202"
    locator: the whole paper (an elimination algorithm with O(e log e) function operations on reducible flow graphs)
  - paper: doi:10.1145/322261.322273
    title: "Robert Endre Tarjan, Fast algorithms for solving path problems, Journal of the ACM 28(3), 1981, 594-614"
    locator: the whole paper (path expressions of a flow graph and their use to solve path problems such as dataflow analysis)
  - paper: doi:10.1145/322261.322272
    title: "Robert Endre Tarjan, A unified approach to path problems, Journal of the ACM 28(3), 1981, 577-593"
    locator: the whole paper (path problems solved by evaluating path expressions in an algebra, with Gaussian elimination as the general method)
  - paper: doi:10.1145/27632.27649
    title: "Barbara G. Ryder and Marvin C. Paull, Elimination algorithms for data flow analysis, ACM Computing Surveys 18(3), 1986, 277-316"
    locator: the whole survey (the Allen-Cocke, Graham-Wegman and Tarjan methods and their common two-phase structure)
---

An elimination method solves the equations of a [dataflow analysis](/dataflow-analysis/) the way Gaussian elimination solves linear equations. It takes one unknown at a time, writes it in terms of the others, and substitutes it away. The coefficients are transfer functions, addition is the meet, multiplication is composition, and a loop is handled by a closure $f^*$ in place of division. The iterative solvers of the [worklist dataflow algorithm](/worklist-dataflow-algorithm/) instead repeat the equations until nothing changes. Allen and Cocke (1976) organized the elimination around *intervals*. These intervals are single-entry regions of the control flow graph in the sense of Allen and Cocke, not the [interval domain](/interval-domain/) of numeric abstract interpretation.

## In plain words

An iterative solver passes notes around a loop until they stop changing. An elimination method looks at the loop once. It works out what one trip around the loop does to a fact, then what any number of trips does, and writes that down as a single summary. A loop becomes one step, and a loop nest becomes a nest of steps.

So the method has two phases. On the way up, it builds summaries for bigger and bigger regions, until the whole procedure is one region. On the way down, it starts from the fact at the entry and pushes it through the summaries to every block. Each phase looks at each part of the program a small number of times, whatever the loops are.

## When it applies

- The framework is distributive. The method substitutes one equation into another, and that is exact only if the functions distribute over the meet. The [gen-kill problems](/gen-kill-problem/) qualify.
- The transfer functions have a small representation that is closed under composition, under pointwise meet and under closure. For gen-kill, a function is a pair of sets (gen, kill), and all three operations give pairs again.
- The closure $f^* = \mathrm{id} \sqcap f \sqcap f^2 \sqcap \cdots$ is easy to compute. For gen-kill, $f \circ f = f$, so $f^* = \mathrm{id} \sqcap f$.
- The graph is [reducible](/reducible-flow-graph/), for the interval and loop-based orders. The general substitution works on any graph, but its cost on irreducible graphs can be cubic.
- You need more than one answer from one graph: the summaries can be reused when only the boundary value changes, and a small edit of the program changes only the summaries of the regions that contain it.

## The template

Write the equations of a forward problem with one unknown $X_v$ per block, for the fact at its start:

$$X_v = b_v \sqcap \mathop{\large\sqcap}_{u} a_{u,v}(X_u).$$

At the start, $a_{u,v} = f_u$ for each edge $(u, v)$, $b_s = \iota$ for the entry $s$, and $b_v = \top$ otherwise. A missing entry $a_{u,v}$ stands for the constant function $\top$. The holes are ORDER, the elimination order of the blocks, and the four operations on functions: COMPOSE, MEET, STAR and APPLY.

```pseudo id=main
ELIMINATE(v_1, ..., v_n)               ▷ the blocks in the chosen ORDER
L1  for k ← 1 to n do                  ▷ phase 1: substitute v_k away
L2      c ← STAR(a[v_k, v_k]); delete a[v_k, v_k]
L3      b[v_k] ← c(b[v_k])
L4      for each entry a[u, v_k] do a[u, v_k] ← c ∘ a[u, v_k]
L5      for each w after v_k with an entry a[v_k, w] do
L6          b[w] ← b[w] ⊓ a[v_k, w](b[v_k])
L7          for each entry a[u, v_k] do a[u, w] ← a[u, w] ⊓ (a[v_k, w] ∘ a[u, v_k])
L8          delete a[v_k, w]
L9  for k ← n down to 1 do             ▷ phase 2: back substitution
L10     X[v_k] ← b[v_k] ⊓ ⊓ over entries a[u, v_k] of a[u, v_k](X[u])
L11 return X
```

Lines L2 to L4 solve the equation of $v_k$ for $X_{v_k}$: a self term $a(X) \sqcap r$ becomes $a^*(r)$. Lines L5 to L8 put the result into every later equation that uses $X_{v_k}$. After phase 1, the equation of $v_k$ uses only blocks after $v_k$, so phase 2 can solve the equations from the last to the first.

**Correctness.** Assume a distributive framework of finite height, with every block reachable.

*Lemma A (the closure).* For a distributive $a$ and any $r$, the greatest $x$ with $x = r \sqcap a(x)$ is $a^*(r) = \mathop{\large\sqcap}_{i \ge 0} a^i(r)$. The partial meets $y_k = \mathop{\large\sqcap}_{i \le k} a^i(r)$ go down, so they stop at some $y$ by finite height. By distributivity, $r \sqcap a(y_k) = y_{k+1}$, so $y = r \sqcap a(y)$. If $x = r \sqcap a(x)$, then $x \sqsubseteq r$, and $x \sqsubseteq a^i(r)$ gives $x \sqsubseteq a(x) \sqsubseteq a^{i+1}(r)$. So $x \sqsubseteq y$.

*Lemma B (each step keeps the greatest solution).* Lines L5 to L8 replace $a_{v,w}(X_v)$ in the equation of $w$ by $a_{v,w}$ applied to the right side of the equation of $v$, and distribute. Since the equation of $v$ stays in the system, this keeps the set of solutions exactly. Lines L2 to L4 replace $X_v = R(X) \sqcap a(X_v)$ by $X_v = a^*(R(X))$, where $R$ does not use $X_v$. By Lemma A, every solution of the new system solves the old one. Let $Y$ be the greatest solution of the old system, and let $Y'$ be $Y$ with $Y'_v = a^*(R(Y))$. Then $Y'_v \sqsupseteq Y_v$ by Lemma A, so $Y'$ is below the right sides of the old equations at every block. A vector with this property is below the greatest solution, by the dual of part 3 of the [Kleene fixed-point theorem](/kleene-fixed-point-theorem/). So $Y' \sqsubseteq Y$, hence $Y' = Y$ and $Y_v = a^*(R(Y))$, and $Y$ solves the new system. The two systems therefore have the same greatest solution.

After phase 1 the system is triangular with no self terms, so it has exactly one solution, which phase 2 computes. By Lemma B, it is the greatest solution of the original equations, the [maximal fixed-point solution](/maximal-fixed-point-solution/). By the [MOP-MFP coincidence theorem](/mop-mfp-coincidence-theorem/), it is also the meet over all paths.

**Cost.** Each step of phase 1 composes every entry of column $v_k$ with every later row that uses $v_k$. In the worst case the rows fill in and phase 1 uses $O(n^3)$ function operations, as in Gaussian elimination. An order that follows the loop structure keeps the rows short. On a reducible graph, Graham and Wegman reach $O(m \log m)$ function operations for $m$ edges. For gen-kill problems over $u$ facts, each function operation costs $O(u / w)$ word operations, for word size $w$.

### Walk-through: reaching definitions on one loop

Take the loop of the [MOP-MFP coincidence theorem](/mop-mfp-coincidence-theorem/) page: `entry` defines $d_1$ (of `i`), `head` defines $d_3$, `body` defines $d_2$ (of `i`, so it kills $d_1$), and the edges are entry to head, head to body, body to head and head to exit. The meet is $\cup$, and a function is a pair (gen, kill). The equations are

$$X_{entry} = \emptyset, \quad X_{head} = f_{entry}(X_{entry}) \cup f_{body}(X_{body}), \quad X_{body} = f_{head}(X_{head}), \quad X_{exit} = f_{head}(X_{head}).$$

Eliminate in the order entry, body, head, exit.

1. `entry` has $b = \emptyset$ and no self term. Substituting it into `head` gives $b_{head} = f_{entry}(\emptyset) = \{d_1\}$.
2. `body` has no self term. Substituting it into `head` gives the self term $a_{head,head} = f_{body} \circ f_{head}$, with gen $\{d_2\} \cup (\{d_3\} - \{d_1\}) = \{d_2, d_3\}$ and kill $\{d_1\}$.
3. `head` now reads $X_{head} = \{d_1\} \cup a_{head,head}(X_{head})$. Its closure is $a^*(x) = x \cup \{d_2, d_3\}$, so $X_{head} = \{d_1, d_2, d_3\}$. Substituting into `exit` gives $b_{exit} = f_{head}(\{d_1, d_2, d_3\}) = \{d_1, d_2, d_3\}$.
4. Back substitution gives $X_{body} = f_{head}(X_{head}) = \{d_1, d_2, d_3\}$ and $X_{entry} = \emptyset$.

This is the same answer that the iterative solver reaches in its second pass. Elimination found it with one closure and no repeated pass.

## Classic examples

- **Allen-Cocke intervals.** For a header $h$, the interval $I(h)$ starts as $\{h\}$ and grows by any block other than the entry whose predecessors all lie in $I(h)$. The entry is the first header, and every block outside the intervals so far that has a predecessor inside one becomes a new header. This splits the blocks into intervals, and every cycle inside an interval passes through its header. Collapsing each interval to one node gives the derived graph, and repeating gives a sequence of smaller graphs. The sequence ends in a single node exactly when the graph is reducible. Phase 1 computes the function from the header to each block of each interval, with a closure at the header, then works on the derived graph. Phase 2 goes back down the sequence (Allen and Cocke, 1976).
- **Graham-Wegman.** An elimination method for reducible graphs that needs $O(m \log m)$ function operations (Graham and Wegman, 1976).
- **Tarjan's path expressions.** A *path expression* is a regular expression over the edges of the graph whose words are exactly the paths from the entry to a block. Evaluating it with composition for concatenation, meet for union and closure for star gives the meet-over-paths solution of a distributive problem. Tarjan (1981) builds path expressions for all blocks at once, quickly on reducible graphs, and solves any path problem in the same way.
- **Gaussian elimination and its relatives.** With numbers as coefficients, the template is [Gaussian elimination](/gaussian-elimination/) without pivoting. With regular expressions, it is the [state elimination](/state-elimination/) method that turns an automaton into a regular expression. With $(\min, +)$, it computes shortest paths like [Floyd-Warshall](/floyd-warshall/).

## Variations

- **Loop-based orders.** Eliminate the blocks of each innermost loop first, using the [loop nesting forest](/loop-nesting-forest/). Each loop becomes one node with a closure at its header. This is the interval idea organized by [natural loops](/natural-loop/).
- **Regions beyond loops.** A method can also recognize if-then-else regions, sequences and other shapes, and summarize each with one function.
- **Incremental update.** After a small edit, recompute the summaries of the regions that contain the edit and redo phase 2.
- **Several boundary values.** Phase 1 does not depend on $\iota$. Run phase 2 again for each boundary value.
- **Hybrid solvers.** Eliminate the reducible parts and iterate on the rest.

## Pitfalls

- **Frameworks that are not distributive.** For [constant propagation](/constant-propagation-problem/), substituting one equation into another is no longer exact, and the meet of two transfer functions has no small form. Elimination is a method for distributive problems with compact functions.
- **Irreducible graphs.** The interval sequence stops before a single node. Either split nodes, which can make the graph much larger, or fall back to general elimination or to iteration on the irreducible part.
- **A closure that is not finite.** On a lattice of infinite height, $a^*$ may need infinitely many terms. Bit-vector problems avoid this because their functions are idempotent.
- **Unreachable blocks.** As for any fixed-point method, a block that the entry does not reach can still send facts to its successors. Remove unreachable blocks first if the meet over paths is wanted.
- **More code, little speed in practice.** On ordinary code, round-robin iteration in reverse postorder needs few passes by the [Kam-Ullman iteration bound](/kam-ullman-iteration-bound/). Most compilers therefore use iteration, and keep elimination for incremental or repeated analysis.

## Exercises

1. Show that for gen-kill functions with the meet $\cup$, the composition $f_2 \circ f_1$ has gen $g_2 \cup (g_1 - k_2)$ and kill $k_1 \cup k_2$, and that $f^*(x) = x \cup g$.
2. Repeat the walk-through for [available expressions](/available-expressions/) on the same loop, where `head` computes `i < n` and `body` redefines `i`. What closure do you get at `head`?
   <details><summary>Hint</summary>With the meet $\cap$, $f^*(x) = x \cap f(x) = x - k$ when gen and kill are disjoint.</details>
3. Compute the intervals and the derived sequence of a graph with two nested loops. How many levels does it have?
4. Give an irreducible graph with three blocks and show that its derived sequence stops at a graph with more than one node.
5. Eliminate the blocks of the walk-through in the order head, body, entry, exit. Do the rows fill in more or less than with the order used above?

## References
