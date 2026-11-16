---
tag: ADH092
kind: theorem
slug: kam-ullman-iteration-bound
name: Kam-Ullman iteration bound
aliases:
- rapid framework bound
area: compilers-and-program-analysis/dataflow-and-abstract-interpretation
level: advanced
summary: Round-robin dataflow iteration in reverse postorder stops after d + 2 passes for rapid distributive frameworks, where d is the loop-connectedness depth.
prereqs: [mop-mfp-coincidence-theorem, depth-first-orders, gen-kill-problem]
see_also: [worklist-dataflow-algorithm, maximal-fixed-point-solution, reducible-flow-graph, natural-loop, dfs-forest, constant-propagation-problem, elimination-dataflow-methods, reaching-definitions]
sources:
  - paper: doi:10.1145/321921.321938
    title: "John B. Kam and Jeffrey D. Ullman, Global data flow analysis and iterative algorithms, Journal of the ACM 23(1), 1976, 158-171"
    locator: the whole paper (the condition on the functions under which the depth-first version of Kildall's algorithm meets the bit-vector iteration bound, and examples that fail it)
  - paper: doi:10.1007/BF00290339
    title: "John B. Kam and Jeffrey D. Ullman, Monotone data flow analysis frameworks, Acta Informatica 7(3), 1977, 305-317"
    locator: the whole paper (monotone frameworks, where constant propagation is the standard framework that is not distributive)
  - book: isbn:9780321486813
    title: Alfred V. Aho, Monica S. Lam, Ravi Sethi and Jeffrey D. Ullman, Compilers, Principles, Techniques, and Tools, second edition, Pearson Addison-Wesley, 2007
    locator: Section 9.6 (Loops in Flow Graphs, depth-first ordering, retreating edges, the depth of a flow graph) and Section 9.6.7 (Speed of Convergence of Iterative Data-Flow Algorithms)
---

The Kam-Ullman iteration bound says how many sweeps a simple dataflow solver needs. The solver visits the blocks in a fixed order, again and again, and stops after a sweep that changes nothing. For a *rapid* distributive framework, which covers every [gen-kill problem](/gen-kill-problem/), and the visit order of [reverse postorder](/depth-first-orders/), the solver stops after at most $d + 2$ sweeps. Here $d$ is the largest number of back edges on a path without repeated blocks, a small number in real code. The bound does not depend on the height of the lattice or on the number of blocks.

## Statement

The page uses the meet convention of the [MOP-MFP coincidence theorem](/mop-mfp-coincidence-theorem/): a meet semilattice $(L, \sqcap)$ of finite height with top $\top$, lower facts are safer, and the answer is the greatest fixed point (MFP). Turning the order upside down gives the join convention, with the same proof.

**The instance.** A [control flow graph](/control-flow-graph/) with $n$ blocks and $m$ edges, an entry block $s$, a transfer function $f_B \in F$ for each block, and a boundary value $\iota$. The set $F$ contains the identity and is closed under composition, as in every [monotone dataflow framework](/monotone-dataflow-framework/). Let $init(s) = \iota$ and $init(B) = \top$ for $B \ne s$.

**Rapid.** The framework is *rapid* if

$$x \sqcap f(\top) \;\sqsubseteq\; f(x) \qquad \text{for all } f \in F \text{ and } x \in L.$$

In words, running a function on a fact $x$ loses nothing beyond what it loses on the optimistic value $\top$ and what $x$ itself already lacks. Gen-kill functions $f(x) = g \cup (x - k)$ are rapid. With the meet $\cup$, the order is $\supseteq$ and $\top = \emptyset$, so $x \sqcap f(\top) = x \cup g \supseteq g \cup (x - k) = f(x)$. With the meet $\cap$, the order is $\subseteq$ and $\top$ is the universe $U$, so $x \cap f(U) = x \cap (g \cup (U - k)) = (x \cap g) \cup (x - k) \subseteq f(x)$.

**The solver (round robin).** Fix a linear order $B_1, \ldots, B_n$ of the blocks. Start with $IN[B] = \top$ for every $B$. A *pass* visits the blocks in this order and at each block $u$ sets

$$IN[u] := init(u) \sqcap \mathop{\large\sqcap}_{(p, u) \in E} f_p(IN[p]),$$

using the newest values of its predecessors. The solver runs passes until a pass changes no value.

**Depth.** An edge $(u, v)$ is *retreating* for the order if $v$ is not after $u$, that is $v = u$ or $v$ comes before $u$. Let $d$ be the largest number of retreating edges on a *simple* path, a path with no repeated block, starting at any block. For reverse postorder, the retreating edges are exactly the back edges of the [depth-first spanning tree](/dfs-forest/), the edges from a block to one of its ancestors in the tree. On a [reducible flow graph](/reducible-flow-graph/) they are the back edges of the [natural loops](/natural-loop/), whatever tree the search builds, so $d$ is a property of the graph and is called its *loop-connectedness depth*.

**Theorem.** Let the framework be distributive and rapid, and let every block be reachable from $s$. Then, for every visit order, the values after pass $d + 1$ are the MFP solution, which here equals the meet over all paths, and the solver stops after at most $d + 2$ passes. With reverse postorder, $d$ is the loop-connectedness depth.

A backward problem is the same on the reverse CFG, with the reverse postorder of the reverse CFG. Each pass applies $n$ transfer functions and at most $m$ meets, so the solver does $O((d + 2)(n + m))$ lattice operations.

## In plain words

Picture facts flowing along the edges of the program. In one sweep in the right order, a fact flows forward along every edge that goes down the page. It can only climb back up a loop edge at the next sweep. So a fact that travels along a route with three loop edges needs about four sweeps.

Routes in a loop can repeat blocks forever, so this alone gives no bound. The rapid property saves the day: going around a loop a second time never teaches anything that one turn plus the facts already present did not. So only routes without repeated blocks matter, and on those routes the number of loop edges is small. One more sweep then confirms that nothing changes.

## Proof

Let $X$ denote the current value of the array $IN$, and let $\mathrm{MFP}$ and $\mathrm{MOP}$ be as on the [MOP-MFP coincidence theorem](/mop-mfp-coincidence-theorem/) page. Walks, paths and their functions $f_w$ are defined there: for $w = (u_0, \ldots, u_k)$, $f_w = f_{u_{k-1}} \circ \cdots \circ f_{u_0}$.

**Lemma 1 (the solver goes down and stays above MFP).** At every moment, each value of $IN$ is at most its previous values and at least $\mathrm{MFP}$. When a pass changes nothing, $IN = \mathrm{MFP}$, and the solver stops after finitely many passes.

*Proof.* Both claims are by induction on the number of updates. The first update of $IN[u]$ gives a value below $\top$. A later update uses the current values of the predecessors, which are below the values used by the previous update of $u$, so by monotonicity the new value is below the old one. For the second claim, if every $IN[p] \sqsupseteq \mathrm{MFP}[p]$, then the new value $init(u) \sqcap \mathop{\large\sqcap}_p f_p(IN[p]) \sqsupseteq init(u) \sqcap \mathop{\large\sqcap}_p f_p(\mathrm{MFP}[p]) = \mathrm{MFP}[u]$, because MFP is a fixed point. A pass that changes nothing leaves $IN$ equal to the right side of the equations, so $IN$ is a fixed point. It is above the greatest fixed point MFP, so it equals MFP. Each value can fall at most $h$ times, so at most $n h + 1$ passes run. $\square$

**Lemma 2 (how fast a route is covered).** For a walk $w = (u_0, \ldots, u_k)$, let $r(w)$ be the number of retreating edges among its edges, and $r'(w)$ the number among its edges except the first.

- (a) If $w$ is a path, so $u_0 = s$, then $IN[u_k] \sqsubseteq f_w(\iota)$ from the end of pass $r(w) + 1$ on.
- (b) For any walk with $k \ge 1$, $IN[u_k] \sqsubseteq f_w(\top)$ from the end of pass $r'(w) + 1$ on.

*Proof.* By Lemma 1, once a bound holds it holds forever, so it is enough to show it right after the visit of $u_k$ in the stated pass. For (a), use induction on $k$, with the stronger claim that the bound holds right after the visit of $u_k$ in pass $r(w) + 1$. For $k = 0$, the visit of $s$ in pass 1 meets in $init(s) = \iota$. For $k \ge 1$, let $w'$ be $w$ without its last block, and $q = r(w') + 1$. By induction, $IN[u_{k-1}] \sqsubseteq f_{w'}(\iota)$ right after the visit of $u_{k-1}$ in pass $q$. If the edge $(u_{k-1}, u_k)$ is not retreating, $u_k$ comes after $u_{k-1}$, so its visit in the same pass $q = r(w) + 1$ meets in $f_{u_{k-1}}(IN[u_{k-1}]) \sqsubseteq f_{u_{k-1}}(f_{w'}(\iota)) = f_w(\iota)$. If the edge is retreating, the visit of $u_k$ in pass $q + 1 = r(w) + 1$ does the same. For (b), the base case is $k = 1$: every value of $IN[u_0]$ is below $\top$, so the visit of $u_1$ in pass 1 meets in $f_{u_0}(IN[u_0]) \sqsubseteq f_{u_0}(\top)$, whatever the order of $u_0$ and $u_1$. The step is the same as in (a). $\square$

Call a walk $w = (u_0, \ldots, u_k)$ with $k \ge 1$ *tail-simple* if $(u_1, \ldots, u_k)$ is a simple path; $u_0$ may equal one of the other blocks. A simple path $\sigma$ has $r(\sigma) \le d$, and a tail-simple walk $w$ has $r'(w) \le d$, because $r'(w)$ counts the retreating edges of the simple path $(u_1, \ldots, u_k)$. For a block $v$, let $T(v)$ be the finite set of the values $f_\sigma(\iota)$ for the simple paths $\sigma$ to $v$ and $f_w(\top)$ for the tail-simple walks $w$ that end at $v$.

**Lemma 3 (only simple routes matter).** If the framework is distributive and rapid, then $\mathop{\large\sqcap} T(v) \sqsubseteq f_w(\top)$ for every walk $w$ of length at least 1 that ends at $v$, and $\mathop{\large\sqcap} T(v) \sqsubseteq f_\pi(\iota)$ for every path $\pi$ to $v$.

*Proof.* The key step is this. Let $w = (u_0, \ldots, u_k)$ be any walk with $u_i = u_j$ for some $i < j$. Split it into the part $\alpha = (u_0, \ldots, u_i)$, the cycle $\gamma = (u_i, \ldots, u_j)$ and the rest $\delta = (u_j, \ldots, u_k)$. Let $y$ be the start value of $w$, either $\iota$ or $\top$, and $x = f_\alpha(y)$. The function $f_\gamma$ is in $F$, so the rapid property gives $f_\gamma(x) \sqsupseteq x \sqcap f_\gamma(\top)$. Apply $f_\delta$, which is monotone, and then distributive:

$$f_w(y) = f_\delta(f_\gamma(x)) \;\sqsupseteq\; f_\delta(x \sqcap f_\gamma(\top)) = f_\delta(f_\alpha(y)) \sqcap f_\delta(f_\gamma(\top)) = f_{\alpha\delta}(y) \sqcap f_{\gamma\delta}(\top).$$

Here $\alpha\delta$ is $w$ with the cycle cut out, of length $k - (j - i)$, and $\gamma\delta$ is the walk $(u_i, \ldots, u_k)$, of length $k - i$. When $j = k$, $f_\delta$ is the identity and distributivity is not needed.

*Walks.* Induction on the length $k$ of $w$. If $w$ is tail-simple, its value is in $T(v)$. Otherwise two of $u_1, \ldots, u_k$ are equal, so the key step applies with $1 \le i < j$. Both $\alpha\delta$ and $\gamma\delta$ are shorter than $k$, have length at least 1 and end at $v$. By induction, $\mathop{\large\sqcap} T(v)$ is below both values, hence below their meet, hence below $f_w(\top)$.

*Paths.* Induction on the length of $\pi$. If $\pi$ is simple, its value is in $T(v)$. Otherwise the key step applies with $y = \iota$. The path $\alpha\delta$ is shorter, so the induction covers it, and the walk $\gamma\delta$ has length $k - i \ge j - i \ge 1$, so the walk case covers it. $\square$

**The theorem.** Look at the end of pass $d + 1$. Every element of $T(v)$ comes from a simple path $\sigma$ with $r(\sigma) + 1 \le d + 1$ or from a tail-simple walk $w$ with $r'(w) + 1 \le d + 1$. By Lemma 2, $IN[v]$ is below each of them, so $IN[v] \sqsubseteq \mathop{\large\sqcap} T(v)$. By Lemma 3, this is below $f_\pi(\iota)$ for every path $\pi$ to $v$, so $IN[v] \sqsubseteq \mathrm{MOP}[v]$. Every block is reachable and the framework is distributive, so $\mathrm{MOP} = \mathrm{MFP}$ by the [coincidence theorem](/mop-mfp-coincidence-theorem/). With Lemma 1, $\mathrm{MFP} \sqsubseteq IN \sqsubseteq \mathrm{MFP}$, so $IN = \mathrm{MFP}$ after pass $d + 1$. Pass $d + 2$ recomputes every value from a fixed point and changes nothing, so the solver stops. $\blacksquare$

**A worked example.** [Reaching definitions](/reaching-definitions/) on the loop of the coincidence theorem page: `entry` defines $d_1$, `head` defines $d_3$, `body` defines $d_2$, and the edges are entry to head, head to body, body to head and head to exit. A depth-first search from `entry` that visits `body` last gives the reverse postorder entry, head, exit, body. The only retreating edge is (body, head), so $d = 1$.

| pass | IN[head] | IN[exit] | IN[body] |
|---|---|---|---|
| 1 | $\{d_1, d_2\}$ | $\{d_1, d_2, d_3\}$ | $\{d_1, d_2, d_3\}$ |
| 2 | $\{d_1, d_2, d_3\}$ | $\{d_1, d_2, d_3\}$ | $\{d_1, d_2, d_3\}$ |
| 3 | no change | no change | no change |

In pass 1, `head` already gets $d_2$ from `body`, because $f_{body}(\emptyset) = \{d_2\}$; this is the free first edge of Lemma 2 (b). The definition $d_3$ needs the walk (head, body, head), whose second edge is retreating, so it arrives in pass 2. Pass 3 $= d + 2$ only confirms the result.

## Consequences

- **Bit-vector problems are fast.** [Reaching definitions](/reaching-definitions/), [live variables](/live-variable-analysis/), [available expressions](/available-expressions/) and [very busy expressions](/very-busy-expressions/) are gen-kill problems, so round robin in reverse postorder costs $O((d + 2)(n + m))$ bit-vector operations. Loops in real programs are seldom nested deeply, so $d$ is small and the cost is close to linear.
- **The order matters.** For reverse postorder, the retreating edges are only the back edges of the search tree. A bad order makes many edges retreating and raises $d$ in the theorem.
- **The bound does not need the lattice height.** A general bound for the [worklist dataflow algorithm](/worklist-dataflow-algorithm/) is $O((n + m) h)$, because each value can fall $h$ times. For rapid frameworks the passes depend only on the loops, even when $h$ is the number of definitions.
- **Each value is right after $d + 1$ passes.** A solver that knows $d$ can skip the last pass. Solvers usually do not compute $d$, so they run the extra pass.
- **Elimination methods are an alternative.** [Elimination dataflow methods](/elimination-dataflow-methods/) solve the equations by substitution on the loop structure, so their cost does not depend on $d$.

## Tightness

**$d + 2$ passes can be needed.** The loop above needs exactly $3 = d + 2$ passes. With two nested loops, entry to OH, OH to IH and exit, IH to IB1 and OL, IB1 to IB2, IB2 to IH, and OL to OH, and one definition in IB1, the depth is 2 and the solver needs exactly 4 passes. The definition reaches IB2 in pass 1, IH and OL in pass 2 after the retreating edge (IB2, IH), and OH and exit in pass 3 after the retreating edge (OL, OH). Pass 4 confirms.

**The rapid property is needed.** [Constant propagation](/constant-propagation-problem/) is not rapid. Take this loop, with $n$ and $t$ unknown parameters:

```
entry:
  x1 = 0
  x2 = 0
  x3 = 0
  x4 = 0
  jump head
head:
  br t body exit
body:
  x1 = x2
  x2 = x3
  x3 = x4
  x4 = n
  jump head
exit:
  ret x1
```

Here $d = 1$, so the bound would be 3 passes. Each pass moves "not a constant" one step along the chain: `x4` at `head` in pass 2, `x3` in pass 3, `x2` in pass 4 and `x1` in pass 5. Pass 6 confirms, so the solver needs 6 passes, and with $k$ variables in the chain it needs $k + 2$. The rapid property fails: for the environment $x$ with all four variables equal to 0, $f_{body}(\top)$ is all $\top$, so $x \sqcap f_{body}(\top) = x$, but $f_{body}(x)$ has $x_4$ not constant, which is not above 0.

**A bad order is slow.** On a straight chain of $n$ blocks, each adding a definition, reverse postorder needs 2 passes. Visiting the chain from its end makes every edge retreating, and the solver needs $n$ passes.

## History

Hecht and Ullman proved an iteration bound for the bit-vector methods in depth-first order. Kam and Ullman (1976) asked when the depth-first version of Kildall's general algorithm meets the same bound. They found a condition on the function space that is both necessary and sufficient, the rapid condition, and showed that several techniques Kildall found useful fail it. In their 1977 paper they set out the monotone frameworks, where constant propagation is the standard example of a framework that is not distributive. The dragon book presents the bound through depth-first ordering and the depth of a flow graph, and counts $d + 2$ passes. The version on this page proves the bound for any visit order and also assumes distributivity, which every gen-kill problem has.

## References
