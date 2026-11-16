---
tag: 9MJ0B6
kind: theorem
slug: mop-mfp-coincidence-theorem
name: MOP-MFP coincidence theorem
aliases:
- Kildall's theorem
- Kam-Ullman coincidence theorem
area: compilers-and-program-analysis/dataflow-and-abstract-interpretation
level: core
summary: In a distributive framework the maximal fixed-point solution equals the meet-over-all-paths solution; in a monotone one it is below it.
prereqs: [meet-over-all-paths-solution, maximal-fixed-point-solution, distributive-dataflow-framework]
see_also: [monotone-dataflow-framework, worklist-dataflow-algorithm, kleene-fixed-point-theorem, kam-ullman-iteration-bound, constant-propagation-problem, ifds-framework, functional-approach-interprocedural, knaster-tarski-theorem]
sources:
  - paper: doi:10.1145/512927.512945
    title: "Gary A. Kildall, A unified approach to global program optimization, Proceedings of the 1st ACM SIGACT-SIGPLAN Symposium on Principles of Programming Languages (POPL 1973), 194-206"
    locator: the whole paper (the lattice framework, the iterative algorithm from the top element, and the result that it reaches the meet over all paths when the functions are distributive)
  - paper: doi:10.1007/BF00290339
    title: "John B. Kam and Jeffrey D. Ullman, Monotone data flow analysis frameworks, Acta Informatica 7(3), 1977, 305-317"
    locator: the whole paper (monotone frameworks, the maximal fixed point below the meet over all paths, a gap in some instance of every monotone framework that is not distributive, and no algorithm for the meet over all paths in general)
  - book: isbn:9780321486813
    title: Alfred V. Aho, Monica S. Lam, Ravi Sethi and Jeffrey D. Ullman, Compilers, Principles, Techniques, and Tools, second edition, Pearson Addison-Wesley, 2007
    locator: Section 9.3.4 (Meaning of a Data-Flow Solution, the maximum fixedpoint against the meet-over-paths solution)
  - book: isbn:9783540654100
    title: Flemming Nielson, Hanne Riis Nielson and Chris Hankin, Principles of Program Analysis, Springer, 1999
    locator: Section 2.4 (Equation Solving, the MFP and MOP solutions and when they agree), in the join convention
---

The MOP-MFP coincidence theorem compares the two answers of a [dataflow analysis](/dataflow-analysis/). The [maximal fixed-point solution](/maximal-fixed-point-solution/) (MFP) is what an iterative solver computes. The [meet-over-all-paths solution](/meet-over-all-paths-solution/) (MOP) is the ideal answer, the meet of the facts that each path produces. In every [monotone dataflow framework](/monotone-dataflow-framework/), MFP is below MOP, so it is safe; in a [distributive dataflow framework](/distributive-dataflow-framework/) where every block is reachable, the two are equal. The definitions of the two solutions are on their own pages; this page states the theorem in full, proves it through an exact description of the iterates of the solver, and shows which hypotheses it needs.

## Statement

The page uses the meet convention of Kildall and the dragon book. $(L, \sqcap)$ is a meet semilattice with top $\top$, $x \sqsubseteq y$ means $x \sqcap y = x$, and $L$ has finite height $h$. Lower facts are weaker and safer. Turning the order upside down gives the join convention of [abstract interpretation](/abstract-interpretation/), where the same theorem speaks of least fixed points and joins.

**The instance.** A [control flow graph](/control-flow-graph/) $G = (V, E)$ with $n$ blocks and an entry block $s$, a monotone transfer function $f_B \in F$ for each block $B$, and a boundary value $\iota \in L$. Let $init(s) = \iota$ and $init(B) = \top$ for $B \ne s$. The equation function is

$$F(X)[B] = init(B) \sqcap \mathop{\large\sqcap}_{(P, B) \in E} f_P(X[P]),$$

where $X$ gives each block the fact at its start and the empty meet is $\top$. MFP is the greatest fixed point of $F$.

**Paths and walks.** A *walk* of length $k$ is a sequence of blocks $w = (B_0, B_1, \ldots, B_k)$ with $(B_{i-1}, B_i) \in E$ for each $i$. Its function is $f_w = f_{B_{k-1}} \circ \cdots \circ f_{B_0}$, the identity when $k = 0$. A *path* to $B$ is a walk with $B_0 = s$ and $B_k = B$. Write $\mathrm{Paths}_{<j}(B)$ for the paths to $B$ of length less than $j$, and $\mathrm{Walks}_j(B)$ for the walks of length exactly $j$ that end at $B$, from any start block. Then

$$\mathrm{MOP}[B] = \mathop{\large\sqcap}_{\pi \text{ a path to } B} f_\pi(\iota).$$

**The iterates.** $X_0 = \top$ at every block, and $X_{j+1} = F(X_j)$. Define the *path bound*

$$R_j[B] = \mathop{\large\sqcap}_{\pi \in \mathrm{Paths}_{<j}(B)} f_\pi(\iota) \;\sqcap \mathop{\large\sqcap}_{w \in \mathrm{Walks}_j(B)} f_w(\top).$$

**Theorem.** For every instance of a monotone framework of finite height:

1. $X_j[B] \sqsubseteq R_j[B]$ for every $j \ge 0$ and every block $B$.
2. The iterates reach MFP after finitely many steps, and $\mathrm{MFP}[B] \sqsubseteq \mathrm{MOP}[B]$ for every block $B$.
3. If moreover every $f_B$ is distributive, $f_B(x \sqcap y) = f_B(x) \sqcap f_B(y)$, and every block is reachable from $s$, then $X_j[B] = R_j[B]$ for every $j$ and $B$, and $\mathrm{MFP} = \mathrm{MOP}$.

Part 3 is the coincidence theorem. Part 1 gives more than the usual statement: the $j$-th iterate is exactly the meet of the facts of the paths shorter than $j$ and of the facts that walks of length $j$ produce from $\top$. A backward problem is the same on the reverse CFG, with the `ret` blocks in place of $s$.

## In plain words

An analysis can be exact in two ways. The ideal way follows every route from the start to a point, works out what each route proves, and keeps only what all routes agree on. The practical way gives every point a note and lets neighbors exchange notes until nothing changes, so it combines facts where routes meet instead of at the end.

Combining early can only lose information, never invent it, so the practical answer is never wrong where the ideal one is right. The theorem says when it loses nothing: when the effect of each block on a combined fact is the same as combining the effects on each fact. The proof watches the note exchange round by round and shows that after a given number of rounds a note holds exactly what the short routes prove, plus a hopeful guess that shrinks each round.

## Proof

Two facts are used. First, the iterates go down and stop: $X_0 \sqsupseteq X_1 \sqsupseteq \cdots$, and $X_J = X_{J+1} = \cdots = \mathrm{MFP}$ for some $J \le n h$. This is proved on the [maximal fixed-point solution](/maximal-fixed-point-solution/) page. Second, the meet over the infinite set of paths exists, because in a semilattice of finite height with a top every nonempty set has a greatest lower bound (proved on the [distributive dataflow framework](/distributive-dataflow-framework/) page); the meet of the empty set is $\top$.

**Lemma 1 (splitting the last edge).** For every $j \ge 0$ and block $B$:

- the paths to $B$ of length less than $j + 1$ are the path $(s)$ when $B = s$, together with the paths $\pi \cdot B$ for an edge $(P, B)$ and a path $\pi \in \mathrm{Paths}_{<j}(P)$;
- the walks of length $j + 1$ that end at $B$ are the walks $w \cdot B$ for an edge $(P, B)$ and a walk $w \in \mathrm{Walks}_j(P)$;
- in both cases $f_{\pi \cdot B} = f_P \circ f_\pi$ and $f_{w \cdot B} = f_P \circ f_w$.

*Proof.* Remove the last block of a path or walk of length at least 1; what remains ends at a predecessor $P$ of $B$ and is one edge shorter. The only path of length 0 is $(s)$. The function of a walk applies the function of each block except the last, so adding $B$ at the end adds $f_P$ on the outside. $\square$

Let $S_j(B)$ be the set of the elements met in $R_j[B]$, that is $\{f_\pi(\iota) : \pi \in \mathrm{Paths}_{<j}(B)\} \cup \{f_w(\top) : w \in \mathrm{Walks}_j(B)\}$. It is finite, since $G$ is finite and the lengths are bounded, so $R_j[B] = \mathop{\large\sqcap} S_j(B)$ is a finite meet.

**Lemma 2 (the meet of the set is nonempty when $B$ is reachable).** If $B$ is reachable from $s$, then $S_j(B)$ is not empty for every $j$.

*Proof.* For $j = 0$, the walk $(B)$ is in $\mathrm{Walks}_0(B)$. For $j \ge 1$, take a path $\pi$ to $B$ of some length $\ell$. If $\ell < j$, then $\pi \in \mathrm{Paths}_{<j}(B)$. Otherwise the last $j$ edges of $\pi$ form a walk in $\mathrm{Walks}_j(B)$. $\square$

**Part 1.** Induction on $j$. For $j = 0$, $\mathrm{Paths}_{<0}(B)$ is empty and $\mathrm{Walks}_0(B) = \{(B)\}$ with the identity function, so $R_0[B] = \top = X_0[B]$. Assume $X_j[P] \sqsubseteq R_j[P]$ for every $P$. For each $r \in S_j(P)$ we have $R_j[P] \sqsubseteq r$, so monotonicity gives $f_P(X_j[P]) \sqsubseteq f_P(R_j[P]) \sqsubseteq f_P(r)$. So $f_P(X_j[P])$ is a lower bound of $\{f_P(r) : r \in S_j(P)\}$, and

$$X_{j+1}[B] = init(B) \sqcap \mathop{\large\sqcap}_{(P, B) \in E} f_P(X_j[P]) \;\sqsubseteq\; init(B) \sqcap \mathop{\large\sqcap}_{(P, B) \in E} \; \mathop{\large\sqcap}_{r \in S_j(P)} f_P(r).$$

By Lemma 1, the right side meets exactly the elements of $S_{j+1}(B)$: the term $init(s) = \iota = f_{(s)}(\iota)$ is the path $(s)$, the term $init(B) = \top$ for $B \ne s$ changes nothing, and the other terms are $f_P(f_\pi(\iota)) = f_{\pi \cdot B}(\iota)$ and $f_P(f_w(\top)) = f_{w \cdot B}(\top)$. So $X_{j+1}[B] \sqsubseteq R_{j+1}[B]$. $\square$

**Part 2.** Take $J$ with $X_j = \mathrm{MFP}$ for all $j \ge J$. Let $\pi$ be a path to $B$ of length $\ell$, and $j = \max(J, \ell + 1)$. Then $\pi \in \mathrm{Paths}_{<j}(B)$, so by part 1, $\mathrm{MFP}[B] = X_j[B] \sqsubseteq R_j[B] \sqsubseteq f_\pi(\iota)$. So $\mathrm{MFP}[B]$ is a lower bound of all path facts, and therefore $\mathrm{MFP}[B] \sqsubseteq \mathrm{MOP}[B]$. If no path reaches $B$, then $\mathrm{MOP}[B] = \top$ and the claim is trivial. $\square$

**Part 3, the iterates.** Repeat the induction of part 1 with equalities. The only step that was an inequality is $f_P(R_j[P]) \sqsubseteq \mathop{\large\sqcap}_{r \in S_j(P)} f_P(r)$. A distributive function satisfies $f(x_1 \sqcap \cdots \sqcap x_k) = f(x_1) \sqcap \cdots \sqcap f(x_k)$ for every $k \ge 1$, by induction on $k$. By Lemma 2, $S_j(P)$ is a nonempty finite set, so the step is an equality, and with $X_j[P] = R_j[P]$ we get $f_P(X_j[P]) = \mathop{\large\sqcap}_{r \in S_j(P)} f_P(r)$. So $X_{j+1}[B] = R_{j+1}[B]$. The nonempty condition matters: for the empty set the left side would be $f_P(\top)$ and the right side $\top$, and these differ for most functions. $\square$

**Part 3, MOP is below MFP.** We show $\mathrm{MOP}[B] \sqsubseteq r$ for every $r \in S_j(B)$. If $r = f_\pi(\iota)$ for a path $\pi$, this holds because $\mathrm{MOP}[B]$ is the meet over all paths. If $r = f_w(\top)$ for a walk $w = (B_0, \ldots, B_j)$ with $B_j = B$, take a path $\alpha$ from $s$ to $B_0$, which exists because $B_0$ is reachable. Joining $\alpha$ and $w$ at $B_0$ gives a path $\alpha w$ to $B$ with $f_{\alpha w} = f_w \circ f_\alpha$. Since $f_\alpha(\iota) \sqsubseteq \top$ and $f_w$ is monotone,

$$\mathrm{MOP}[B] \sqsubseteq f_{\alpha w}(\iota) = f_w(f_\alpha(\iota)) \sqsubseteq f_w(\top) = r.$$

So $\mathrm{MOP}[B]$ is a lower bound of $S_j(B)$, hence $\mathrm{MOP}[B] \sqsubseteq R_j[B] = X_j[B]$ for every $j$. With $j \ge J$ this gives $\mathrm{MOP}[B] \sqsubseteq \mathrm{MFP}[B]$, and part 2 gives the other direction. $\blacksquare$

**A worked example.** Take [reaching definitions](/reaching-definitions/) (meet $= \cup$, $\top = \emptyset$, $\iota = \emptyset$) on this loop, with the definitions $d_1$ of `i` in `entry`, $d_3$ of `t` in `head` and $d_2$ of `i` in `body`:

```
entry:
  i = 0
  jump head
head:
  t = i < n
  br t body exit
body:
  i = i + 1
  jump head
exit:
  ret i
```

The edges are entry to head, head to body, body to head and head to exit. The iterates at `head` are $X_0 = \emptyset$, $X_1 = \{d_1, d_2\}$ and $X_2 = X_3 = \{d_1, d_2, d_3\}$. Part 3 predicts $X_1$: no path to `head` is shorter than one edge, and the walks of length 1 that end at `head` are (entry, head), which gives $f_{entry}(\emptyset) = \{d_1\}$, and (body, head), which gives $f_{body}(\emptyset) = \{d_2\}$. At $j = 2$ the path (entry, head) gives $\{d_1\}$ and the only walk of length 2, (head, body, head), gives $\{d_2, d_3\}$. The fixed point $\{d_1, d_2, d_3\}$ is also MOP: the path (entry, head) brings $d_1$, and the path (entry, head, body, head) brings $d_2$ and $d_3$.

## Consequences

- **Iterative solvers are exact for the bit-vector problems.** The four classic [gen-kill problems](/gen-kill-problem/) are distributive, so the [worklist dataflow algorithm](/worklist-dataflow-algorithm/), round-robin iteration and every other fair order compute MOP on a CFG whose blocks are all reachable. How many rounds that takes is the subject of the [Kam-Ullman iteration bound](/kam-ullman-iteration-bound/).
- **An early stop is unsafe.** By part 1, an iterate that is not yet stable still holds the terms $f_w(\top)$ of walks that start from the optimistic value. In the example, $X_1[\text{head}] = \{d_1, d_2\}$ misses $d_3$, which does reach `head`. A solver must run to the fixed point before a client uses its facts.
- **Monotone frameworks are safe.** Part 2 needs no distributivity and no reachability. So [constant propagation](/constant-propagation-problem/), which is monotone but not distributive, has a safe MFP even where it is less precise than MOP.
- **MOP is not computable in general.** Kam and Ullman (1977) proved that no algorithm computes the MOP solution of every instance of every monotone framework. The fixed point is therefore the answer that analyses compute; the theorem says when it is also the ideal one.
- **Interprocedural analysis.** Across procedures the ideal answer is the meet over valid paths, in which returns match calls (see [interprocedural dataflow analysis](/interprocedural-dataflow-analysis/)). The [functional approach](/functional-approach-interprocedural/) of Sharir and Pnueli and the [IFDS framework](/ifds-framework/) and [IDE framework](/ide-framework/) reach that ideal for distributive problems, by the same argument applied to summary functions.

## Tightness

- **Distributivity is needed.** Let $f \in F$ and $x, y \in L$ with $f(x \sqcap y) \ne f(x) \sqcap f(y)$, and let $g_1, g_2 \in F$ produce $x = g_1(\iota)$ and $y = g_2(\iota)$. Build a diamond: the entry has the identity function and two successors $A$ and $C$ with the functions $g_1$ and $g_2$, both go to a block $J$ with the function $f$, and $J$ goes to an exit. The two paths give $\mathrm{MOP}[\text{exit}] = f(x) \sqcap f(y)$. MFP meets first, so $\mathrm{MFP}[J] = x \sqcap y$ and $\mathrm{MFP}[\text{exit}] = f(x \sqcap y)$, which is strictly below $f(x) \sqcap f(y)$ by monotonicity and the choice of $f$. Constant propagation with $(x, y) = (2, 3)$ on one branch and $(3, 2)$ on the other, followed by `z = x + y`, is this case: MOP finds $z = 5$ and MFP does not. Kam and Ullman (1977) showed that every monotone framework that is not distributive has an instance where MFP differs from MOP.
- **Reachability is needed.** A block that the entry does not reach still passes its function value to its successors in every solution of the equations, while MOP ignores it. The [distributive dataflow framework](/distributive-dataflow-framework/) page gives an instance where this makes MFP strictly below MOP.
- **Distributivity is not necessary on a given instance.** If every block has at most one predecessor, the CFG is a tree, each block has exactly one path, no meet is ever taken, and MFP = MOP for every monotone framework.
- **Finite height is needed for the finite iteration.** Take $L = \mathbb{Z} \cup \{-\infty, +\infty\}$ with the meet $\min$ and $\top = +\infty$, an entry with the identity and $\iota = 0$, and a loop block $H$ with a self-loop and $f_H(x) = x - 1$, which is distributive. The iterates at $H$ are $+\infty, +\infty, 0, -1, -2, \ldots$ and never stop. The greatest fixed point and MOP are both $-\infty$, but they are reached only in the limit. Abstract interpreters on such lattices use a [widening operator](/widening-operator/).

## History

Kildall (1973) set dataflow analysis in a semilattice with distributive transfer functions. He gave the iterative algorithm that starts from the top element and showed that it computes the meet over all paths. Kam and Ullman (1977) noticed that useful analyses, constant propagation first, are monotone but not distributive. They defined monotone frameworks, proved that the maximal fixed point exists and is below the meet over all paths, showed that every monotone framework that is not distributive has an instance with a gap, and proved that the meet over all paths cannot be computed in general. Textbooks give the result in both conventions: the dragon book with meets, and Nielson, Nielson and Hankin with joins and least fixed points.

## References
