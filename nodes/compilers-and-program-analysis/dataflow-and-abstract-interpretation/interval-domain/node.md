---
tag: 86D96R
kind: definition
slug: interval-domain
name: Interval abstract domain
aliases:
- box domain
area: compilers-and-program-analysis/dataflow-and-abstract-interpretation
level: core
summary: Abstracts each numeric variable by a lower and an upper bound, a non-relational domain of infinite height that needs widening.
prereqs: [abstract-domain, galois-connection]
see_also: [abstract-interpretation, widening-operator, narrowing-operator, octagon-domain, interval-arithmetic, integer-overflow, reduced-product, weak-topological-ordering]
sources:
  - paper: "Patrick Cousot and Radhia Cousot, Static determination of dynamic properties of programs, Proceedings of the Second International Symposium on Programming, B. Robinet (ed.), Dunod, Paris, 1976, pages 106 to 130"
    locator: the interval analysis of programs, its abstract operations, and the widening and narrowing that make it stop
  - paper: doi:10.1145/512950.512973
    title: "Patrick Cousot and Radhia Cousot, Abstract interpretation: a unified lattice model for static analysis of programs by construction or approximation of fixpoints, POPL 1977, pages 238 to 252"
    locator: the interval example of an abstract interpretation with an infinite ascending chain and its widening
  - book: isbn:9780262043410
    title: Xavier Rival and Kwangkeun Yi, Introduction to Static Analysis, An Abstract Interpretation Perspective, MIT Press, 2020
    locator: Chapter 2 and Chapter 3 (the interval domain as a non-relational abstraction, its operations, and the analysis of conditions and loops)
  - book: isbn:9783540654100
    title: Flemming Nielson, Hanne Riis Nielson and Chris Hankin, Principles of Program Analysis, Springer, 1999
    locator: Chapter 4 (Abstract Interpretation), the interval lattice and its widening as the running example
---

The interval domain describes each integer name by a lower and an upper bound, such as $0 \le i \le 10$. A state of the analysis keeps one interval per name, so it describes a box in the space of values. It is the simplest numeric domain that can bound the range of a loop counter, prove that a divisor is never 0 or that an index stays inside an array, and it costs $O(v)$ per operation for $v$ names. It keeps no relation between two names, and it has infinite ascending chains, so an analysis with it needs a [widening](/widening-operator/).

## Definition

The general domain, its meaning and its Galois connection with sets of integers are on the [abstract interpretation](/abstract-interpretation/) page; this page gives the parts that an analyzer of the toy IR needs. The order is the Cousot order: lower is more precise, and $\bot$ means that no state reaches the point.

**The lattice for one name.** The elements are $\bot$ and the pairs $[l, u]$ with $l \in \mathbb{Z} \cup \{-\infty\}$, $u \in \mathbb{Z} \cup \{+\infty\}$ and $l \le u$. The order is inclusion of meanings: $[l, u] \sqsubseteq [l', u']$ when $l' \le l$ and $u \le u'$. The join is $[\min(l, l'), \max(u, u')]$, and the meet is $[\max(l, l'), \min(u, u')]$, or $\bot$ when that pair is empty. The top element is $[-\infty, +\infty]$. The height is infinite: $[0, 0] \sqsubset [0, 1] \sqsubset [0, 2] \sqsubset \cdots$ never stops. The map $\alpha(S) = [\inf S, \sup S]$ makes a Galois insertion with $\mathcal{P}(\mathbb{Z})$, so every operation below can be compared with the best one, $\alpha \circ f \circ \gamma$.

**The state.** A state is a map from the names $V$ to intervals, or $\bot$. A map in which some name has $\bot$ is the same as $\bot$. This is the non-relational construction of the [abstract domain](/abstract-domain/) page, and its meaning is the box $\gamma(m) = \prod_{x \in V} \gamma(m(x))$. Join, meet and $\sqsubseteq$ work name by name.

**Transfer functions.** Let $m$ be the state before the instruction, and write $[a, b]$ and $[c, d]$ for the intervals of the operands, with $[k, k]$ for a constant $k$. An instruction `x = ...` sets $m(x)$ and keeps the other names.

| instruction | new interval of `x` | best? |
|---|---|---|
| `x = k` | $[k, k]$ | yes |
| `x = y` | $m(y)$ | yes |
| `x = y + z` | $[a + c, b + d]$ | yes |
| `x = y - z` | $[a - d, b - c]$ | yes |
| `x = y * z` | $[\min P, \max P]$ with $P = \{ac, ad, bc, bd\}$ and $0 \cdot \infty = 0$ | yes |
| `x = y / z` | split $[c, d]$ into its negative part and its positive part, divide by each part using the four corners, and join | yes |
| `x = y % z` | with $M = \max(\lvert c \rvert, \lvert d \rvert)$: $[0, \min(b, M - 1)]$ if $a \ge 0$, $[\max(a, 1 - M), 0]$ if $b \le 0$, else $[1 - M, M - 1]$ | sound, not best |
| `x = y < z` | $[1, 1]$ if $b < c$, $[0, 0]$ if $a \ge d$, else $[0, 1]$ | yes |
| `x = y op z`, other op | $[0, 1]$ for a comparison, a simple bound or $\top$ for the bit operations | sound |

"Best" means that the result is $\alpha$ of the set of all concrete results, for any operand intervals that do not contain $\pm\infty$; a check over all operand intervals inside $[-7, 7]$ confirms the claim for `/` and the soundness of the `%` rule. Division truncates toward zero, as in the toy IR. For a divisor of one sign, the truncated quotient is monotone in each operand, so the extremes are at the corners. The value 0 is left out of the divisor because a run with divisor 0 traps and does not reach the next instruction. If $[c, d] = [0, 0]$, the result is $\bot$: no run gets past the instruction. When an operand bound is infinite, a corner uses the limits, for example $y / (+\infty) = 0$ and $(+\infty) / 2 = +\infty$.

**Guards.** Suppose the block ends with `t = y < z` followed by `br t L1 L2`, and neither name changes between the two. On the edge to `L1` the condition $y < z$ holds, so the state is refined:

$$ m(y) := m(y) \sqcap [-\infty, d - 1], \qquad m(z) := m(z) \sqcap [a + 1, +\infty]. $$

On the edge to `L2`, $y \ge z$ holds, and $m(y) := m(y) \sqcap [c, +\infty]$, $m(z) := m(z) \sqcap [-\infty, b]$. The other comparisons are similar. If a meet gives $\bot$, the whole state is $\bot$ and the edge is dead. A guard on a name that the block does not compare directly gives no refinement.

**Equations and the solution.** The equations have the shape $F^\sharp$ given on the [abstract domain](/abstract-domain/) page: at each block, the join over the incoming edges of the edge transformer. The *join over all paths*, the analogue of the [meet-over-all-paths solution](/meet-over-all-paths-solution/) in this order, is more precise than the fixed point, because the transfer functions are monotone but do not distribute over the join (see the example below). An analyzer computes the fixed point side. Plain iteration from $\bot$ may run forever, so the analyzer applies a [widening](/widening-operator/) at a set of points that cuts every cycle, such as the heads of a [weak topological ordering](/weak-topological-ordering/), and then a few steps of [narrowing](/narrowing-operator/). The result is a map $X$ with $F^\sharp(X) \sqsubseteq X$, not in general the least fixed point of $F^\sharp$.

**Soundness.** Each transfer function and each guard is sound, and the join is sound. By the claim on the [abstract domain](/abstract-domain/) page, any $X$ with $F^\sharp(X) \sqsubseteq X$ satisfies $\mathit{Coll}(\ell) \subseteq \gamma(X(\ell))$ at each block $\ell$.

**Precision.** The domain loses information in three ways. It forgets relations between names at each join. It treats two uses of one name as independent, so `x * x` and `y - x` lose the link between the operands. And the widening jumps over the exact bound, which narrowing only partly recovers.

**Cost.** In the word-RAM model, with each bound in one word, a state takes $O(v)$ space, and a join, a meet, a test $\sqsubseteq$ or a widening takes $O(v)$ time. A transfer function changes one name, so it takes $O(1)$ time if the state is updated in place, or $O(v)$ if it is copied. With widening at the chosen points, the value at each such point changes at most $2v + 1$ times: once from $\bot$, then at most once for each of the $2v$ bounds.

## Examples and non-examples

**An absolute value and a division.** The parameter `x` has the precondition $-5 \le x \le 7$.

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
  e = y + 1
  q = 100 / e
  ret q
```

The guard on `t = x < 0` refines `x` on each edge. The results at the end of each block are in the table, with the exact sets for comparison.

| point | interval result | exact set |
|---|---|---|
| neg | $x \in [-5, -1]$, $y \in [1, 5]$ | same |
| pos | $x \in [0, 7]$, $y \in [0, 7]$ | same |
| join, after the join | $x \in [-5, 7]$, $y \in [0, 7]$ | $y = \lvert x \rvert$ |
| `d = y - x` | $d \in [-7, 12]$ | $\{0, 2, 4, 6, 8, 10\}$ |
| `e = y + 1` | $e \in [1, 8]$ | $\{1, \dots, 8\}$ |
| `q = 100 / e` | $q \in [12, 100]$ | $\{12, 14, 16, 20, 25, 33, 50, 100\}$ |

The analysis proves that $e \ge 1$, so the division never traps; that is the main use of the domain. It cannot prove $d \ge 0$: after the join it knows $y \in [0, 7]$ and $x \in [-5, 7]$ but not $y = \lvert x \rvert$, and $y - x$ is computed as if the two were unrelated. A relational domain such as the [octagon domain](/octagon-domain/) keeps $y \ge x$ and $y \ge -x$ and proves $d \ge 0$.

**The fixed point is less precise than the join over paths.** Two paths reach a block, one with $x = 1, y = 2$ and one with $x = 2, y = 1$, and the block computes `z = x + y`. On each path the result is $[3, 3]$, so the join over paths gives $z \in [3, 3]$. The fixed point first joins the states, $x, y \in [1, 2]$, and then adds: $z \in [2, 4]$. Addition does not distribute over the join of states.

**A loop.** The block that sums `i` from 0 to 9 into `s` is analyzed step by step on the [widening operator](/widening-operator/) and [narrowing operator](/narrowing-operator/) pages. The result at the exit is $i \in [10, 10]$ and $s \in [0, +\infty]$. The upper bound of `s` is lost because it depends on the number of passes, which the domain does not track.

**Non-example: one interval for the whole state.** A single pair of bounds for all names together, $\min_x \rho(x) \ge l$ and $\max_x \rho(x) \le u$, is a domain too, but it is not this one: it cannot say that `i` is small and `n` is large at the same time. The interval domain has one pair per name.

**Non-example: machine integers.** On a machine with 32-bit integers that wrap around, `y + 1` with $y \in [0, 2^{31} - 1]$ gives a result in $[-2^{31}, 2^{31} - 1]$, not $[1, 2^{31}]$. The table above is sound only for the unbounded integers of the toy IR. An analyzer for C either reports an [integer overflow](/integer-overflow/) and continues with the wrapped range, or uses intervals modulo $2^{32}$.

**Non-example: interval arithmetic.** [Interval arithmetic](/interval-arithmetic/) on floating-point numbers uses the same operations with outward rounding, and it bounds the error of one computation. The interval domain is that arithmetic plus a join, guards and a widening, so that it can run over a control flow graph with loops.

## Related definitions

- [Abstract domain](/abstract-domain/): the general definition and the non-relational construction used here.
- [Galois connection](/galois-connection/): the interval insertion, and the best transformer that the table is compared with.
- [Widening operator](/widening-operator/) and [narrowing operator](/narrowing-operator/): the operators that make the analysis stop and then recover precision.
- [Weak topological ordering](/weak-topological-ordering/): an order of the blocks and a set of widening points.
- [Octagon domain](/octagon-domain/) and [polyhedra domain](/polyhedra-domain/): relational domains that keep the facts that intervals lose, at a higher cost.
- [Reduced product](/reduced-product/): a combination with other domains, such as parity or congruences.
- [Constant propagation problem](/constant-propagation-problem/): the analysis with intervals of width 0, of finite height.
- [Abstract interpretation](/abstract-interpretation/): the general technique, with the interval widening and a worked loop.

## References
