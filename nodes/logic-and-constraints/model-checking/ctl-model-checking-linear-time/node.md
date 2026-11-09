---
tag: 1SVYG1
kind: theorem
slug: ctl-model-checking-linear-time
name: Linear-time complexity of CTL model checking
aliases:
- Clarke-Emerson-Sistla theorem
- CTL model checking in linear time
area: logic-and-constraints/model-checking
level: core
summary: CTL model checking takes time O(|M||phi|), linear in the structure and in the formula. EG costs linear time through strongly connected components, and fairness keeps the bound polynomial.
prereqs: [computation-tree-logic, ctl-labelling-algorithm, tarjan-scc]
see_also: [ctl-labelling-algorithm, ctl-model-checking, computation-tree-logic, fairness, strongly-connected-components, tarjan-scc, ltl-model-checking-pspace-completeness, mu-calculus-model-checking]
sources:
  - paper: doi:10.1145/5397.5399
    title: Edmund M. Clarke, E. Allen Emerson and A. Prasad Sistla, Automatic verification of finite-state concurrent systems using temporal logic specifications, ACM Transactions on Programming Languages and Systems 8(2), 1986, pages 244 to 263
    locator: the theorem that CTL model checking takes time O(|M| |f|), the SCC procedure for EG, and the extension to fairness constraints
  - book: isbn:9780262026499
    title: Christel Baier and Joost-Pieter Katoen, Principles of Model Checking, MIT Press, 2008
    locator: Chapter 6, Section 6.4 (the time complexity of CTL model checking, with the SCC-based algorithm for EG) and Section 6.5 (the complexity of fair CTL model checking)
  - book: isbn:9780262032704
    title: Edmund M. Clarke, Orna Grumberg and Doron A. Peled, Model Checking, MIT Press, 1999
    locator: Chapter 4, Section 4.1 (the linear-time bound for CTL, and the bound with fairness constraints)
  - paper: doi:10.1016/0167-6423(87)90036-0
    title: E. Allen Emerson and Chin-Laung Lei, Modalities for model checking, branching time logic strikes back, Science of Computer Programming 8(3), 1987, pages 275 to 306
    locator: polynomial-time model checking of fair CTL with strong fairness constraints
---

The linear-time theorem for CTL says that whether a finite [Kripke structure](/kripke-structure/) satisfies a [CTL](/computation-tree-logic/) formula can be decided in time proportional to the size of the structure times the size of the formula. Clarke, Emerson and Sistla proved it in 1983 (journal version 1986), and it is the reason CTL became the first practical specification logic for model checking. The key step is the operator $\mathsf{EG}$: a naive fixed-point iteration for it can take $|S|$ rounds, but [strongly connected components](/strongly-connected-components/) give it in one linear pass. This page is the bound and its proof. The [CTL labelling algorithm](/ctl-labelling-algorithm/) is the algorithm that the proof analyses, and [CTL model checking](/ctl-model-checking/) is the problem, with its other bounds.

## Statement

Let $M = (S, I, R, L)$ be a finite Kripke structure with a total transition relation, given by adjacency lists, and let $|M| = |S| + |R|$. Let $\varphi$ be a CTL formula with $|\varphi|$ symbols.

**Theorem (Clarke, Emerson and Sistla 1986).** The set $[\![\varphi]\!] = \{s \in S : s \models \varphi\}$ can be computed in time $O(|M| \cdot |\varphi|)$. So $M \models \varphi$ can be decided in this time.

**With fairness.** Let the path quantifiers range over the paths that are fair for a list of $k$ requirements: justice sets $J \subseteq S$ (visit $J$ infinitely often) and compassion pairs $(p, q)$ (if $p$ is visited infinitely often, so is $q$). Then $[\![\varphi]\!]$ can be computed in time

- $O(|\varphi| \cdot (|M| + k\,|S|))$ when all requirements are justice sets, and
- $O(|\varphi| \cdot (k + 1) \cdot (|M| + k\,|S|))$ in general.

Both are $O(|M| \cdot |\varphi| \cdot k^2)$ at most, polynomial in all three parameters.

## In plain words

Checking a CTL formula costs about as much as reading the graph once for each part of the formula. A formula with ten operators on a graph with a million edges costs about ten million steps, not more.

Most operators are easy: they are one look at each state, or one backward search. The operator "there is a path that stays forever in good states" looks harder, because "forever" seems to need many rounds. The trick is that a path that stays forever in a finite set of good states must run around a loop of good states. The loops are exactly the tightly connected groups of the good part of the graph, and one standard graph search finds all of them at once.

Fairness rules add a factor that depends only on how many rules there are.

## Proof

**Step 1: the formula as a DAG of subformulas.** Rewrite $\varphi$ in the adequate set $\{\neg, \wedge, \mathsf{EX}, \mathsf{EU}, \mathsf{EG}\}$, or keep $\mathsf{AU}$ with its own counter-based procedure. The rewrite rules (for example $\mathsf{AF}\,\alpha = \neg\mathsf{EG}\,\neg\alpha$) copy subformulas, so we represent the result as a DAG in which equal subformulas are one node. Each rule adds a constant number of new nodes per operator of $\varphi$, so the DAG has $O(|\varphi|)$ nodes. A post-order of the DAG visits each node after its children, in time $O(|\varphi|)$.

**Step 2: each node costs $O(|M|)$.** For a node $\psi$ whose children already have their sets $A = [\![\alpha]\!]$ and $B = [\![\beta]\!]$, stored as arrays of Booleans indexed by state:

- *Atoms and Booleans.* One pass over $S$ (and over the labels, whose total size is part of the input).
- *$\mathsf{EX}\,\alpha$.* One pass over the edges: mark $s$ if some $(s, t) \in R$ has $t \in A$. $O(|S| + |R|)$.
- *$\mathsf{E}[\alpha\,\mathsf{U}\,\beta]$.* Backward [breadth-first search](/breadth-first-search/) from $B$ along reversed edges, entering only states of $A$. Each state enters the queue at most once, and each reversed edge is scanned once, when its target leaves the queue. $O(|S| + |R|)$. By the least fixed-point characterization $\mathsf{E}[\alpha\,\mathsf{U}\,\beta] = \mu Z.\, \beta \vee (\alpha \wedge \mathsf{EX}\,Z)$, this search computes the right set (the [labelling algorithm](/ctl-labelling-algorithm/) proves it as Lemma 1).
- *$\mathsf{A}[\alpha\,\mathsf{U}\,\beta]$, if kept.* The same search, with a counter per state for the successors not yet in the set. $O(|S| + |R|)$.
- *$\mathsf{EG}\,\alpha$.* See step 3. $O(|S| + |R|)$.

The predecessor lists used by the backward searches are built once, in $O(|M|)$ time.

**Step 3: $\mathsf{EG}$ by strongly connected components.** Let $M_A$ be the subgraph of $M$ on $A$, and call a strongly connected component of $M_A$ *nontrivial* if it has at least one edge of $M_A$ (two or more states, or one state with a self-loop).

*Lemma.* $s \models \mathsf{EG}\,\alpha$ if and only if $s \in A$ and there is a path inside $A$ from $s$ to a state of a nontrivial component of $M_A$.

*Proof.* ($\Rightarrow$) Let $\pi = s_0 s_1 \ldots$ be a path from $s$ with every $s_i \in A$. As $A$ is finite, some state repeats: $s_i = s_j$ with $i < j$. The cycle $s_i \ldots s_j$ lies in $M_A$, so its states belong to one component of $M_A$, and that component contains the edge $(s_i, s_{i+1})$, so it is nontrivial. The prefix $s_0 \ldots s_i$ is the path inside $A$. ($\Leftarrow$) In a nontrivial component $C$, each state $t$ lies on a cycle inside $C$: if $|C| \ge 2$, go from $t$ to another state of $C$ and back; otherwise use the self-loop. Follow the path inside $A$ from $s$ to $t$, then this cycle forever. Every state on this path is in $A$. $\blacksquare$

So $[\![\mathsf{EG}\,\alpha]\!]$ is computed in two linear passes: [Tarjan's algorithm](/tarjan-scc/) on $M_A$ in $O(|S| + |R|)$ time, which marks the nontrivial components, and a backward breadth-first search inside $A$ from the marked states, which is the $\mathsf{EU}$ procedure with target the marked states. By contrast, the fixed-point iteration $Z_0 = A$, $Z_{i+1} = A \cap \mathit{pre}_\exists(Z_i)$ removes possibly one state per round: on a path of $n$ states in $A$ that ends outside $A$, it needs $n$ rounds, $\Theta(|S| \cdot |M|)$ time in total. The components avoid this.

**Step 4: the sum.** $O(|\varphi|)$ nodes, each $O(|M|)$, plus $O(|M| + |\varphi|)$ for the setup, give $O(|M| \cdot |\varphi|)$. The correctness of each step is proved in the [correctness proof of the labelling algorithm](/ctl-labelling-algorithm/). $\blacksquare$

**Fairness.** A path is fair if and only if each of its suffixes is fair, because the requirements depend only on the set $\mathit{inf}(\pi)$ of states visited infinitely often. Let $\mathit{fair} = [\![\mathsf{E}_f\mathsf{G}\,\mathit{true}]\!]$. Then $\mathsf{E}_f\mathsf{X}\,\alpha = \mathsf{EX}(\alpha \wedge \mathit{fair})$ and $\mathsf{E}_f[\alpha\,\mathsf{U}\,\beta] = \mathsf{E}[\alpha\,\mathsf{U}\,(\beta \wedge \mathit{fair})]$, so these cost $O(|M|)$ as before, and $\mathit{fair}$ is computed once. It remains to compute $\mathsf{E}_f\mathsf{G}\,\alpha$.

*Justice.* Call a nontrivial component $C$ of $M_A$ *fair* if it meets each justice set. Then $s \models \mathsf{E}_f\mathsf{G}\,\alpha$ iff $s$ reaches a fair component inside $A$. If $\pi$ is a fair path inside $A$, the set $\mathit{inf}(\pi)$ is strongly connected in $M_A$ and contains an edge, so it lies in one nontrivial component, which then meets each justice set. Conversely, a fair component contains a cycle through one state of each justice set. Testing each component against $k$ sets costs $O(k\,|S|)$, so $\mathsf{E}_f\mathsf{G}$ costs $O(|M| + k\,|S|)$.

*Compassion.* Run the following refinement on the parts of $A$, starting with the single part $A$: split the part into components of $M_A$ restricted to it; drop the trivial ones; a component $C$ is *bad* for the pair $(p, q)$ when $C \cap p \ne \emptyset$ and $C \cap q = \emptyset$. If $C$ is bad for no pair (and meets each justice set, written as the pair $(S, J)$), keep $C$ as good. Otherwise put $C \setminus \bigcup \{p : C \text{ is bad for } (p, q)\}$ back as a new part.

- *Sound.* In a good component, a cycle through all its states has $\mathit{inf} = C$, which satisfies each pair. So each good state has a fair path inside $A$.
- *Complete.* Let $\pi$ be a fair path inside $A$ and $D = \mathit{inf}(\pi)$. $D$ is strongly connected with an edge, so in each part that contains $D$, it lies inside one nontrivial component $C$. If $C$ is bad for $(p, q)$, then $D \cap q \subseteq C \cap q = \emptyset$, so $D \cap p = \emptyset$ by fairness, and $D$ lies in the new part. The parts shrink, so eventually $D$ lies in a good component.
- *Cost.* When a pair makes $C$ bad, its $p$-states are removed from all later parts below $C$, so the pair can never make one of them bad again. So each chain of refinements has at most $k + 1$ levels. The parts at one level are disjoint, so each level costs $O(|M| + k\,|S|)$, and $\mathsf{E}_f\mathsf{G}$ costs $O((k + 1)(|M| + k\,|S|))$.

Then a backward search inside $A$ from the good components gives $\mathsf{E}_f\mathsf{G}\,\alpha$, and summing over the $O(|\varphi|)$ subformulas gives the bounds in the statement. $\blacksquare$

## Consequences

- **CTL model checking is in P**, and it is in fact P-complete ([CTL model checking](/ctl-model-checking/)). The cost is dominated by $|M|$, which is the size that grows in practice.
- **CTL against LTL.** [LTL model checking](/ltl-model-checking/) takes $O(|M| \cdot 2^{O(|\varphi|)})$ time and is PSPACE-complete ([LTL model checking PSPACE-completeness](/ltl-model-checking-pspace-completeness/)). Both are linear in $|M|$; they differ in the formula. This was a large part of the early debate between branching and linear time.
- **Alternation-free fixed points.** The same idea, one linear pass per fixed point by a backward search with counters, gives linear time for the alternation-free [modal mu-calculus](/modal-mu-calculus/) (Cleaveland and Steffen 1993), which contains CTL. For nested alternating fixed points no linear algorithm is known; see [mu-calculus model checking](/mu-calculus-model-checking/).
- **Witnesses for free.** The searches of the proof leave parent links and components, from which a witness path or lasso for $\mathsf{EU}$ and $\mathsf{EG}$ is read off in linear time.
- **Symbolic model checking** does not inherit the bound. With [BDDs](/binary-decision-diagram/) the natural form is fixed-point iteration, which may need up to $|S|$ rounds for $\mathsf{EG}$; SCC-based symbolic algorithms exist, with a number of symbolic steps that depends on the structure.

## Tightness

- **Reading the input.** Any algorithm must read $M$ and $\varphi$, so $\Omega(|M| + |\varphi|)$ time is needed.
- **The global output.** The labelling computes $[\![\psi]\!]$ for every subformula. On a directed cycle of $n$ states with $p$ in $n/2$ consecutive states, the sets of $\mathsf{EX}\,p$, $\mathsf{EX}\,\mathsf{EX}\,p$, and so on, up to depth $n - 1$, are rotations of each other, each with $n/2$ states, so writing them all takes $\Omega(|S| \cdot |\varphi|)$ time. An algorithm that only answers for the initial states is not bound by this argument, and this page does not claim a general lower bound of the form $\Omega(|M| \cdot |\varphi|)$.
- **Without the SCC step** the same algorithm takes $\Theta(|S| \cdot |M| \cdot |\varphi|)$ time in the worst case, by the example in step 3.
- **Beyond CTL.** The bound depends on the rule that each temporal operator has its own path quantifier. For CTL+, which allows Boolean combinations of temporal operators under one quantifier, model checking is $\Delta_2^p$-complete (Laroussinie, Markey and Schnoebelen 2001), and for [CTL*](/ctl-star/) and LTL it is PSPACE-complete, so a polynomial bound in $|\varphi|$ is unlikely for them.
- **Parallel time.** Since CTL model checking is P-complete, it has no polylogarithmic-time parallel algorithm unless $\mathrm{NC} = \mathrm{P}$.

## History

Clarke and Emerson (1981) defined CTL and model checked it by fixed-point iteration, in polynomial time. Queille and Sifakis (1982) independently built a model checker based on fixed points. Clarke, Emerson and Sistla presented the linear algorithm, with strongly connected components for $\mathsf{EG}$, at POPL 1983, and the journal version in ACM TOPLAS (1986) added fairness constraints. Emerson and Lei (1985, journal version 1987) extended polynomial-time model checking to fair CTL with strong fairness. The EMC model checker, built on the algorithm, verified circuits and protocols with tens of thousands of states in the 1980s.

## References
