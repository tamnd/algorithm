---
tag: RFWPGY
kind: definition
slug: octagon-domain
name: Octagon abstract domain
aliases:
- octagons
area: compilers-and-program-analysis/dataflow-and-abstract-interpretation
level: advanced
summary: A relational domain of constraints plus or minus x plus or minus y <= c, kept in a difference-bound matrix with cubic time closure.
prereqs: [abstract-domain, interval-domain, difference-bound-matrix]
see_also: [polyhedra-domain, widening-operator, narrowing-operator, floyd-warshall, difference-constraints, galois-connection, reduced-product, weak-topological-ordering]
sources:
  - paper: doi:10.1007/s10990-006-8609-1
    title: "Antoine Miné, The octagon abstract domain, Higher-Order and Symbolic Computation 19(1), 2006, pages 31 to 100"
    locator: the encoding of octagonal constraints in a difference-bound matrix over the positive and negative forms of each name, coherence, strong closure, the lattice operations, the transfer functions, and the widening whose left argument must not be closed
  - paper: doi:10.1109/WCRE.2001.957836
    title: "Antoine Miné, The octagon abstract domain, Proceedings of the Eighth Working Conference on Reverse Engineering (WCRE 2001), IEEE, 2001"
    locator: the first presentation of the domain and of its cubic closure
  - paper: doi:10.1007/s10703-009-0073-1
    title: "Roberto Bagnara, Patricia M. Hill and Enea Zaffanella, Weakly-relational shapes for numeric abstractions: improved algorithms and proofs of correctness, Formal Methods in System Design 35(3), 2009, pages 279 to 323"
    locator: the proof that one strengthening pass after the shortest-path closure gives the strong closure, and the semantic view of octagons as shapes
  - paper: doi:10.1007/978-3-540-78163-9_6
    title: "Roberto Bagnara, Patricia M. Hill and Enea Zaffanella, An improved tight closure algorithm for integer octagonal constraints, VMCAI 2008, LNCS 4905, pages 8 to 21"
    locator: the tight closure of integer octagons in cubic time, with the rounding of the unary bounds and the test for emptiness
  - book: isbn:9780262043410
    title: Xavier Rival and Kwangkeun Yi, Introduction to Static Analysis, An Abstract Interpretation Perspective, MIT Press, 2020
    locator: Chapter 3 (relational abstract domains for numeric states, among them octagons and convex polyhedra)
---

The octagon domain describes the numeric names of a program by constraints of the form $\pm x \pm y \le c$, such as $x + y \le 10$ or $x - y \le 3$, together with bounds $\pm x \le c$ on one name. In the plane, such a set is a polygon with at most eight sides, which gives the domain its name. It keeps relations between names that the [interval domain](/interval-domain/) loses, but it costs much less than the [polyhedra domain](/polyhedra-domain/): $O(v^2)$ space and $O(v^3)$ time for its most expensive operation, for $v$ names. Antoine Miné introduced it in 2001. An octagon is stored as a [difference-bound matrix](/difference-bound-matrix/) over two copies of each name, one for $+x$ and one for $-x$, so the closure of the matrix is a shortest-path computation followed by one extra step.

## Definition

The order is the Cousot order: lower is more precise, and $\bot$ means that no state reaches the point. On the dataflow pages that use Kildall's convention the order is the other way round. The general framework is on the [abstract domain](/abstract-domain/) page.

**Octagonal constraints.** Let the names be $x_0, \ldots, x_{v-1}$. An octagonal constraint is $\pm x_i \pm x_j \le c$ with $i \ne j$, or $\pm x_i \le c$. A bound on one name is the same as $\pm x_i \pm x_i \le 2c$, so it needs no special case below.

**The doubled names.** For each name $x_i$ take two forms, $w_{2i} = x_i$ and $w_{2i+1} = -x_i$. For an index $a$ write $\bar a$ for the index of the other form of the same name, so $\bar a = a \oplus 1$ (flip the last bit) and $w_{\bar a} = -w_a$. Each octagonal constraint becomes one or two differences $w_a - w_b \le c$:

| constraint | differences |
|---|---|
| $x_i - x_j \le c$ | $w_{2i} - w_{2j} \le c$ and $w_{2j+1} - w_{2i+1} \le c$ |
| $x_i + x_j \le c$ | $w_{2i} - w_{2j+1} \le c$ and $w_{2j} - w_{2i+1} \le c$ |
| $-x_i - x_j \le c$ | $w_{2i+1} - w_{2j} \le c$ and $w_{2j+1} - w_{2i} \le c$ |
| $x_i \le c$ | $w_{2i} - w_{2i+1} \le 2c$ |
| $-x_i \le c$ | $w_{2i+1} - w_{2i} \le 2c$ |

**The matrix.** An octagon is $\bot$ or a $2v \times 2v$ matrix $m$ with entries in $\mathbb{Z} \cup \{+\infty\}$ (or $\mathbb{Q} \cup \{+\infty\}$ for rational names). The entry $m[a][b]$ is a bound on $w_a - w_b$, so $m$ is a difference-bound matrix over the $2v$ forms. Its meaning is

$$ \gamma(m) = \{\, x \in \mathbb{Z}^v : w_a - w_b \le m[a][b] \text{ for all } a, b, \text{ where } w_{2i} = x_i,\ w_{2i+1} = -x_i \,\}. $$

The two differences in one row of the table are the same fact, since $w_a - w_b = w_{\bar b} - w_{\bar a}$. A matrix is *coherent* when $m[a][b] = m[\bar b][\bar a]$ for all $a, b$. Every operation below keeps matrices coherent, so half the matrix can be stored.

**Strong closure.** Many matrices have the same meaning. The [difference-bound matrix](/difference-bound-matrix/) page computes the tightest bounds of a DBM as all-pairs shortest paths with [Floyd-Warshall](/floyd-warshall/). For octagons this is not enough, because the forms are linked by $w_{\bar a} = -w_a$. From $x \le 1$ and $y \le 2$ follows $x + y \le 3$, but no path in the graph of the matrix gives it. One more rule is needed. The entry $m[a][\bar a]$ bounds $w_a - w_{\bar a} = 2w_a$, and $m[\bar b][b]$ bounds $-2w_b$, so

$$ w_a - w_b \le \tfrac{1}{2}\bigl(m[a][\bar a] + m[\bar b][b]\bigr). $$

The *strong closure* $m^\bullet$ is computed in two steps:

1. Run Floyd-Warshall on $m$, as on a DBM with $2v$ vertices. If some diagonal entry becomes negative, the octagon is empty, and the result is $\bot$.
2. For all $a, b$, set $m[a][b] \leftarrow \min\bigl(m[a][b], \tfrac{1}{2}(m[a][\bar a] + m[\bar b][b])\bigr)$.

Miné's first algorithm applied the strengthening of step 2 inside every round of Floyd-Warshall. Bagnara, Hill and Zaffanella (2009) proved that one pass at the end gives the same result. Step 1 costs $(2v)^3 = 8v^3$ updates and step 2 costs $4v^2$, so the closure takes $O(v^3)$ time. For a non-empty octagon over the rationals, $m^\bullet[a][b] = \sup\{\, w_a - w_b : x \in \gamma(m) \,\}$ for every pair: each entry is the best bound that the octagon implies. So two octagons have the same meaning if and only if they have the same strong closure, and the strong closure is a normal form.

**Integers.** Over $\mathbb{Z}$ the strong closure can miss facts, because $2x \le 3$ means $x \le 1$. The *tight closure* rounds each unary bound $m[a][\bar a]$ down to an even number between steps 1 and 2. The integer octagon is then empty exactly when step 1 finds a negative diagonal entry or, after the rounding, some $m[a][\bar a] + m[\bar a][a] < 0$. Bagnara, Hill and Zaffanella (2008) showed that this also takes $O(v^3)$ time. This is notable, because integer linear constraints in general are NP-hard to solve.

**Order, join and meet.** Let $m$ and $n$ be octagons that are not $\bot$.

- $m \sqsubseteq n$ when $m^\bullet[a][b] \le n[a][b]$ for all $a, b$. This is exact: it holds if and only if $\gamma(m) \subseteq \gamma(n)$. Only the left side needs to be closed.
- $m \sqcup n$ is the entry-wise maximum of $m^\bullet$ and $n^\bullet$. It is the least octagon that contains both, so the join is the best one. The result is again strongly closed. The maximum of matrices that are not closed is still sound, but it can lose relations (see the examples).
- $m \sqcap n$ is the entry-wise minimum. It is exact: $\gamma(m \sqcap n) = \gamma(m) \cap \gamma(n)$. It is not closed in general.

**Abstraction.** Over $\mathbb{Z}$, the map $\alpha(S)[a][b] = \sup\{\, w_a - w_b : x \in S \,\}$ is a [Galois connection](/galois-connection/) between sets of integer points and matrices. It is not a Galois insertion on all matrices, because many matrices share a meaning; on tightly closed matrices plus $\bot$ it is. Over the rationals, with rational bounds, there is no best abstraction in general: the sup of $x + y$ over the rational points of the disk $x^2 + y^2 \le 1$ is $\sqrt 2$, and there is no least rational bound above it.

**Transfer functions.** On a closed matrix:

- $x_i \leftarrow x_i + c$ is exact. Add $c$ to the bounds of $w_{2i} - w_b$, subtract it from those of $w_{2i+1} - w_b$, and do the reverse on column $2i$ and $2i+1$. Cost $O(v)$.
- $x_i \leftarrow c$, $x_i \leftarrow x_j + c$ and $x_i \leftarrow -x_j + c$ are exact. Forget $x_i$ (set its rows and columns to $+\infty$, except the diagonal), then add the new constraints, for example $x_i - x_j \le c$ and $x_j - x_i \le -c$. Cost $O(v^2)$, with the incremental closure for the few new constraints.
- Any other assignment forgets $x_i$ and then bounds it by [interval](/interval-domain/) arithmetic on the bounds of the operands. This is sound but not best.
- A guard $\pm x_i \pm x_j \le c$ is exact: take the meet with the constraint and close again, in $O(v^2)$ time for one constraint. Other guards, such as $x < 2y$, are applied through their interval bounds or ignored.

**Widening and narrowing.** The [widening](/widening-operator/) keeps the stable bounds and drops the others:

$$ (m \mathbin{\nabla} n)[a][b] = \begin{cases} m[a][b] & \text{if } n[a][b] \le m[a][b], \\ +\infty & \text{otherwise.} \end{cases} $$

The right argument may be closed, and should be, for precision. The left argument must be the previous widened iterate exactly as it is, and must not be closed. Each strict widening step then turns at least one finite entry into $+\infty$, so a chain of widened iterates that starts from a matrix has at most $4v^2$ strict steps. Closing the left argument can make $+\infty$ entries finite again, and Miné (2006) gives a sequence where the iteration then never stops. The [narrowing](/narrowing-operator/) replaces only the $+\infty$ entries: $(m \mathbin{\Delta} n)[a][b] = n[a][b]$ if $m[a][b] = +\infty$, and $m[a][b]$ otherwise.

**Cost.** An octagon takes $4v^2$ entries, or about $2v^2$ with coherence. Closure, and so an exact inclusion test or a join on unclosed inputs, costs $O(v^3)$. Join, meet, widening and the simple transfer functions cost $O(v^2)$ on closed inputs.

## Examples and non-examples

**Strengthening.** Take $x = x_0$ and $y = x_1$, with $x \le 1$ and $y \le 2$. Then $m[0][1] = 2$ and $m[2][3] = 4$, and all other entries off the diagonal are $+\infty$. Floyd-Warshall finds no new bound, since no path leads from form 0 to form 3. Step 2 gives $m[0][3] = \tfrac{1}{2}(m[0][1] + m[2][3]) = 3$, which is $w_0 - w_3 = x + y \le 3$.

**An absolute value.** The [interval domain](/interval-domain/) page analyzes this program, where the parameter `x` has the precondition $-5 \le x \le 7$:

```
entry:
  t = x < 0
  br t neg pos
neg:
  y = 0 - x
  jump join
pos:
  y = x
  jump join
join:
  d = y - x
  ret d
```

In `neg` the octagon holds $-5 \le x \le -1$ and $x + y = 0$; in `pos` it holds $0 \le x \le 7$ and $y - x = 0$. After closure each branch bounds all four sums and differences, and the join takes the larger bound of each.

| bound | `neg` | `pos` | join |
|---|---|---|---|
| $x$ | $[-5, -1]$ | $[0, 7]$ | $[-5, 7]$ |
| $y$ | $[1, 5]$ | $[0, 7]$ | $[0, 7]$ |
| $y - x$ | $[2, 10]$ | $[0, 0]$ | $[0, 10]$ |
| $x + y$ | $[0, 0]$ | $[0, 14]$ | $[0, 14]$ |

So `d` $\in [0, 10]$, and the true set is $\{0, 2, \ldots, 10\}$. The intervals give $d \in [-7, 12]$, because they lose $y \ge x$ and $y \ge -x$.

**A loop with two counters.**

```
entry:
  x = 0
  y = 10
  jump head
head:
  t = x < 10
  br t body exit
body:
  x = x + 1
  y = y - 1
  jump head
exit:
  ret y
```

The analysis widens at `head`, the head of the loop in the [weak topological ordering](/weak-topological-ordering/). The guard on the edge to `body` adds $x \le 9$; the guard on the edge to `exit` adds $x \ge 10$. Both assignments in `body` are exact.

| step | point | $x$ | $y$ | $x + y$ | $y - x$ |
|---|---|---|---|---|---|
| 1 | head | $[0, 0]$ | $[10, 10]$ | $[10, 10]$ | $[10, 10]$ |
| 1 | end of body | $[1, 1]$ | $[9, 9]$ | $[10, 10]$ | $[8, 8]$ |
| 2 | head, before widening | $[0, 1]$ | $[9, 10]$ | $[10, 10]$ | $[8, 10]$ |
| 2 | head, after widening | $[0, +\infty]$ | $[-\infty, 10]$ | $[10, 10]$ | $[-\infty, 10]$ |
| 2 | end of body | $[1, 10]$ | $[0, 9]$ | $[10, 10]$ | $[-10, 8]$ |
| 3 | head | stable | | | |
| | exit | $[10, +\infty]$ | $[-\infty, 0]$ | $[10, 10]$ | $[-\infty, -10]$ |
| | head, after narrowing | $[0, 10]$ | $[0, 10]$ | $[10, 10]$ | $[-10, 10]$ |
| | exit, after narrowing | $[10, 10]$ | $[0, 0]$ | $[10, 10]$ | $[-10, -10]$ |

The relation $x + y = 10$ is stable from the start, so the widening keeps it. With it, the guard $x \le 9$ in the body gives $y \ge 1$, and the exit gets $y = 0$ after one narrowing step. Intervals alone get $y \in [-\infty, 10]$ at exit, even with narrowing, because nothing bounds $y$ from below.

**A join without closure.** In the loop above, the state after `entry` holds only the unary bounds $x = 0$ and $y = 10$. If the analyzer takes the entry-wise maximum with the state $x = 1$, $y = 9$ without closing either matrix first, the entries for $x + y$ are $+\infty$ in both, so the result is the box $[0, 1] \times [9, 10]$ and the relation $x + y = 10$ is gone. The join must close its arguments.

**Not octagonal.** The constraint $x \le 2y$ has a coefficient 2, and $x + y + z \le 1$ has three names. An octagon can only keep their consequences of the form $\pm x \pm y \le c$. The [polyhedra domain](/polyhedra-domain/) keeps them exactly.

**A widening that closes its left argument.** Using $(m^\bullet) \mathbin{\nabla} n$ in place of $m \mathbin{\nabla} n$ looks harmless, since $m^\bullet$ has the same meaning as $m$. It is not a widening: an entry dropped to $+\infty$ by one step can come back as a finite sum of other entries after the closure, and Miné (2006) gives an increasing chain on which the iterates then never stabilize.

## Related definitions

- [Difference-bound matrix](/difference-bound-matrix/): the zones $x - y \le c$, used for the clocks of timed automata. An octagon is a DBM over the $2v$ forms, with coherence and the extra strengthening step.
- [Difference constraints](/difference-constraints/): systems $x_j - x_i \le c$ solved by shortest paths, the graph view behind both DBMs and octagons.
- [Interval domain](/interval-domain/): the octagons with only unary constraints; an octagon analysis costs about $v^2$ times more per operation.
- [Polyhedra domain](/polyhedra-domain/): any linear constraints, more precise and exponential in the worst case. Octagons sit between intervals and polyhedra.
- [Reduced product](/reduced-product/): octagons are often combined with other domains, such as congruences, by a reduced product.
- [Widening operator](/widening-operator/) and [narrowing operator](/narrowing-operator/): the general definitions behind the octagon widening and narrowing.

## References
