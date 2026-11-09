---
tag: G25ZD9
kind: theorem
slug: ltl-model-checking-pspace-completeness
name: PSPACE-completeness of LTL model checking
aliases:
- Sistla-Clarke theorem
area: logic-and-constraints/model-checking
level: advanced
summary: LTL model checking and LTL satisfiability are PSPACE-complete (Sistla and Clarke 1985). Model checking takes O(|M| 2^O(|φ|)) time, linear in the structure.
prereqs: [ltl-model-checking, ltl-satisfiability, linear-temporal-logic, pspace, ltl-to-buchi-translation]
see_also: [savitch-theorem, regex-equivalence-pspace-completeness, automata-theoretic-approach, nested-depth-first-search, ctl-model-checking, cook-levin-theorem, graph-reachability, state-explosion-problem]
sources:
  - paper: "A. Prasad Sistla and Edmund M. Clarke, The complexity of propositional linear temporal logics, Journal of the ACM 32(3), 1985"
    locator: PSPACE-completeness of satisfiability and model checking for LTL with X and U, and the results for the fragments with F only, with F and X, and with U only
  - paper: "Orna Lichtenstein and Amir Pnueli, Checking that finite state concurrent programs satisfy their linear specification, 12th ACM Symposium on Principles of Programming Languages (POPL 1985)"
    locator: the tableau algorithm whose time is linear in the program and exponential in the formula
  - paper: "Moshe Y. Vardi and Pierre Wolper, An automata-theoretic approach to automatic program verification, First IEEE Symposium on Logic in Computer Science (LICS 1986)"
    locator: model checking and satisfiability by Büchi automata, and the polynomial-space algorithm that builds the automaton on the fly
  - book: isbn:9780262026499
    title: Christel Baier and Joost-Pieter Katoen, Principles of Model Checking, MIT Press, 2008
    locator: Chapter 5, Section 5.2 (the complexity of LTL model checking, the polynomial-space upper bound and the PSPACE-hardness proof by the encoding of a space-bounded Turing machine)
---

LTL model checking and LTL satisfiability are both [PSPACE](/pspace/)-complete. This is the theorem of Sistla and Clarke (1985). The same proof gives the standard algorithm, whose time is linear in the size of the [Kripke structure](/kripke-structure/) and exponential in the size of the formula. The hardness holds already for one fixed structure, so the exponential cost in the formula cannot be removed unless P = PSPACE.

## Statement

The formulas are those of [linear temporal logic](/linear-temporal-logic/), built from atomic propositions with $\neg$, $\wedge$, $\mathsf{X}$ and $\mathsf{U}$; the operators $\mathsf{F}$ and $\mathsf{G}$ are abbreviations. The size $|\varphi|$ is the number of symbols of $\varphi$. A Kripke structure $M = (S, I, R, L)$ is as on the [Kripke structure](/kripke-structure/) page, with a total relation $R$ and size $|M| = |S| + |R|$, and $M \models \varphi$ means that the trace of every path from an initial state satisfies $\varphi$.

**Theorem** (Sistla and Clarke, 1985). The following problems are PSPACE-complete under polynomial-time many-one reductions.

1. **[Satisfiability](/ltl-satisfiability/).** Given $\varphi$, is there an infinite word $\sigma \in (2^{AP})^\omega$ with $\sigma \models \varphi$?
2. **[Model checking](/ltl-model-checking/).** Given $M$ and $\varphi$, does $M \models \varphi$ hold?

The model checking problem is PSPACE-hard already for one fixed structure $M_0$ and a fixed set of propositions. It can be decided in time $O(|M| \cdot 2^{O(|\varphi|)})$ and in space $O((|\varphi| + \log |M|)^2)$.

## In plain words

To check a temporal formula against a system, the standard method turns the formula into an automaton and searches the combination of the system and the automaton for a bad cycle. The automaton can have a number of states that is exponential in the length of the formula, so the time is exponential in the formula. But the search need not store the whole automaton. It can walk through it one state at a time and keep only a few states in memory, so memory stays modest.

The theorem says that this is the best possible in general. Any problem that a computer can solve with a modest amount of memory can be written as a question about one temporal formula, checked against one small system. A method that is fast in the length of the formula would make all of these problems fast, which is believed to be impossible.

## Proof

The proof has three parts: a lasso lemma for the product with an automaton, the upper bounds, and the lower bounds by the encoding of a Turing machine.

**The automaton.** The page on [LTL to Büchi translation](/ltl-to-buchi-translation/) builds, for a formula $\psi$, a generalized [Büchi automaton](/buchi-automaton/) $A_\psi$ with these properties, proved in full in its correctness proof:

- the states are the *elementary sets* of $\psi$, subsets of the closure of $\psi$, so there are at most $2^{|\psi|}$ states, and a state is written with $O(|\psi|)$ bits;
- whether a set is a state, whether it is initial, its label $\lambda(B) \subseteq AP_\psi$, whether $B \to C$ is a transition, and whether $B$ is in the acceptance set $F_i$ can each be decided in time polynomial in $|\psi|$ and in space $O(|\psi|)$ from the bits of $B$ and $C$;
- there are $k \le |\psi|$ acceptance sets, and $A_\psi$ accepts exactly the words that satisfy $\psi$.

**The product.** For $M$ and $\psi$, the *product graph* $P$ has the vertices $(s, B)$ with $L(s) \cap AP_\psi = \lambda(B)$, the edges $(s, B) \to (t, C)$ with $(s, t) \in R$ and $B \to C$, the initial vertices $(s, B)$ with $s \in I$ and $B$ initial, and the sets $\hat F_i = \{(s, B) : B \in F_i\}$. A path $\pi$ of $M$ from $I$ and an accepting run of $A_\psi$ on the trace of $\pi$ pair into a path of $P$ from an initial vertex that meets each $\hat F_i$ infinitely often, and each such path of $P$ splits back into a path of $M$ and an accepting run on its trace. Since $M \not\models \varphi$ iff the trace of some path satisfies $\neg\varphi$, we get, with $\psi = \neg\varphi$:

$$M \not\models \varphi \iff P \text{ has a path from an initial vertex that meets each } \hat F_i \text{ infinitely often.} \tag{1}$$

For satisfiability, drop $M$: $\psi$ is satisfiable iff the graph of $A_\psi$ itself has such a path. This is the case of (1) for the structure with one state for each subset of $AP_\psi$, but the argument below never builds that structure.

**Lemma 1 (lasso).** Let $G$ be a finite graph with initial vertices and sets $F_1, \ldots, F_k$. The following are equivalent.

1. $G$ has an infinite path from an initial vertex that meets each $F_i$ infinitely often.
2. There are a vertex $v$ reachable from an initial vertex and a closed walk from $v$ to $v$, with at least one edge, that meets each $F_i$.
3. Some nontrivial strongly connected component $C$ of $G$, reachable from an initial vertex, meets each $F_i$. A component is nontrivial if it has at least one edge.

*Proof.* (1 ⇒ 2.) Let $\rho$ be such a path. Only finitely many vertices exist, so there is a position $N$ after which every vertex on $\rho$ occurs infinitely often. Let $v = \rho_N$. After position $N$, $\rho$ meets $F_1$, then $F_2$, and so on up to $F_k$, and then meets $v$ again. That segment is a closed walk from $v$ that meets each $F_i$, and the prefix of $\rho$ up to $N$ reaches $v$.

(2 ⇒ 3.) All vertices of a closed walk lie in one strongly connected component, and this component has an edge.

(3 ⇒ 1.) Since $C$ is strongly connected and has an edge, there is a closed walk inside $C$ through all vertices of $C$, from a vertex $v$ of $C$. Go from an initial vertex to $v$ and then repeat this walk forever. $\square$

In statement 2, the walk can be chosen short: a shortest path to $v$ has fewer than $|G|$ edges, and the closed walk can be cut into $k + 1$ simple paths, from $v$ to a vertex of $F_1$, from there to a vertex of $F_2$, and so on, and back to $v$. So a closed walk of at most $(k + 1)|G|$ edges exists when any does.

**Upper bound in time.** The product $P$ has at most $|S| \cdot 2^{|\psi|}$ vertices and at most $|R| \cdot 4^{|\psi|}$ edges. Build the part reachable from the initial vertices, compute its strongly connected components with [Tarjan's algorithm](/tarjan-scc/), and test statement 3 of Lemma 1, which takes $O(k)$ per vertex. With (1) this decides $M \models \varphi$ in time $O(|M| \cdot 2^{O(|\varphi|)})$, since $|\psi| = |\varphi| + 1$. The [nested depth-first search](/nested-depth-first-search/) after degeneralization gives the same bound.

**Upper bound in space.** The following nondeterministic procedure decides $M \not\models \varphi$. It stores the current vertex $u$, a vertex $v$, a vector $b$ of $k$ bits, and a counter.

- Guess an initial vertex $u$ of $P$ and check it.
- Repeat at most $|P|$ times: either guess a successor $u'$ of $u$, check the edge, and set $u \leftarrow u'$; or stop the loop.
- Set $v \leftarrow u$ and $b \leftarrow 0^k$. Repeat at most $(k + 1)|P|$ times: guess a successor $u'$ of $u$, check the edge, set $u \leftarrow u'$, and set bit $i$ of $b$ for each $i$ with $u \in \hat F_i$. Accept when $u = v$ and all bits of $b$ are set.

A branch accepts exactly when it has found a stem and a closed walk as in statement 2 of Lemma 1, and the bounds on the lengths lose nothing, by the remark after the lemma. So the procedure accepts iff $M \not\models \varphi$. A vertex takes $O(\log |S| + |\varphi|)$ bits, the counter takes $O(\log |S| + |\varphi|)$ bits, and each check reads the input $M$ and runs the local tests of the automaton in space $O(|\varphi| + \log |M|)$. So the complement of model checking is in nondeterministic space $O(|\varphi| + \log |M|)$. By [Savitch's theorem](/savitch-theorem/) it is in deterministic space $O((|\varphi| + \log |M|)^2)$, and a deterministic machine decides model checking itself in the same space by flipping the answer. The same procedure on the graph of $A_\varphi$ alone decides satisfiability in space $O(|\varphi|^2)$. Both problems are in PSPACE.

**Lower bound: the machine.** Fix a language $A$ that is PSPACE-complete, for example [QBF](/qbf/), and a deterministic single-tape [Turing machine](/turing-machine/) $T$ that decides it, with states $Q$, start state $q_0$, accepting state $q_{\mathrm{acc}}$, tape alphabet $\Gamma$ with blank $\sqcup$, and a polynomial $p$ with $p(n) \ge n$, such that on inputs of length $n$:

- $T$ uses only cells $1$ to $p(n)$, and never moves left from cell $1$ or right from cell $p(n)$;
- each move writes a symbol, changes the state, and moves the head one cell left, one cell right, or not at all; a halting state loops forever on itself without changing the tape.

These are standard normalizations. Let $\Delta_0 = \Gamma \cup (Q \times \Gamma)$ and $\Delta = \Delta_0 \cup \{\#\}$. A configuration is a string of $p = p(n)$ letters of $\Delta_0$ with exactly one letter in $Q \times \Gamma$, which marks the head, the state and the symbol under the head. All of $Q$, $\Gamma$ and $\Delta$ are fixed, because $T$ is fixed.

**Lemma 2 (windows).** There is a function $f : \Delta^3 \to \Delta_0$ such that for every configuration $C$ with successor $C'$ and every cell $1 \le j \le p$, $C'[j] = f(C[j-1], C[j], C[j+1])$, where we put $C[0] = C[p+1] = \#$.

*Proof.* Cell $j$ changes in one move only if the head is at $j - 1$, $j$ or $j + 1$, and then the change is fixed by the state and the symbol under the head. Let $\delta(q, a) = (q', b, D)$. If $C[j] = (q, a)$, then $C'[j]$ is $(q', b)$ when $D$ is "stay" and $b$ otherwise. If $C[j - 1] = (q, a)$ and $D$ is "right", then $C'[j] = (q', C[j])$; if $C[j + 1] = (q, a)$ and $D$ is "left", then $C'[j] = (q', C[j])$. In all other cases $C'[j] = C[j]$. Each case reads only the three letters, so these rules define $f$ on the windows that occur in configurations; define $f$ in any way on the others. $\square$

**Lower bound: the formula.** Use the letters of $\Delta$ as atomic propositions. A word is read as the infinite string $\# C_0 \# C_1 \# C_2 \cdots$, one letter per position, so that position $0$ holds $\#$, the letters of $C_i$ are at positions $i(p + 1) + 1$ to $i(p + 1) + p$, and $\#$ is at the multiples of $p + 1$. Write $\mathsf{X}^j$ for $j$ nested $\mathsf{X}$. For an input $x = x_1 \cdots x_n$, let $C_0 = (q_0, x_1)\, x_2 \cdots x_n \sqcup^{p - n}$ (with $C_0 = (q_0, \sqcup) \sqcup^{p-1}$ when $n = 0$), and let $\psi_x$ be the conjunction of:

- **Start:** $\# \wedge \bigwedge_{j=1}^{p} \mathsf{X}^j\, C_0[j] \wedge \mathsf{X}^{p+1} \#$;
- **Shape:** $\mathsf{G}\bigl(\# \to \bigwedge_{j=1}^{p} \mathsf{X}^j \neg\# \wedge \mathsf{X}^{p+1} \#\bigr)$;
- **Step:** $\mathsf{G} \bigwedge_{(a, b, c) \in \Delta^3,\ b \ne \#} \bigl(a \wedge \mathsf{X} b \wedge \mathsf{X}^2 c \to \mathsf{X}^{p+2} f(a, b, c)\bigr)$;
- **Accept:** $\mathsf{F} \bigvee_{a \in \Gamma} (q_{\mathrm{acc}}, a)$.

Start and Shape have size $O(p^2)$, and Step has $|\Delta|^3$ conjuncts of size $O(p)$, so $|\psi_x| = O(p(n)^2)$, and $\psi_x$ is computed from $x$ in polynomial time. Let $\theta = \mathsf{G}\bigl(\bigvee_{a \in \Delta} a \wedge \bigwedge_{a \ne b} \neg(a \wedge b)\bigr)$, which says that exactly one letter holds at each position; its size depends only on $T$.

**Lemma 3.** Let $\sigma$ be a word in which exactly one letter of $\Delta$ holds at each position. Then $\sigma$ satisfies Start, Shape and Step iff $\sigma = \# C_0 \# C_1 \# \cdots$ where $C_0 C_1 C_2 \ldots$ is the computation of $T$ on $x$. Hence $\theta \wedge \psi_x$ is satisfiable iff $T$ accepts $x$.

*Proof.* The computation word satisfies Start and Shape by its form, and Step by Lemma 2: if position $m$ holds $a$ and positions $m+1$, $m+2$ hold $b \ne \#$ and $c$, then $b$ is cell $j$ of some $C_i$, $a$ and $c$ are cells $j - 1$ and $j + 1$ (or $\#$ at the ends), and position $m + p + 2$ is cell $j$ of $C_{i+1}$.

Conversely, Start and Shape force $\#$ exactly at the multiples of $p + 1$ and force $C_0$ after position $0$. Suppose that $\sigma$ agrees with the computation word up to position $m - 1$, where $m \ge p + 2$ is not a multiple of $p + 1$. Then $m - p - 1$ is a cell position, so the conjunct of Step at position $m - p - 2$ for the three letters there fires, and it forces letter $f(a, b, c)$ at $m$, which is the letter of the computation word by Lemma 2. By induction, $\sigma$ is the computation word.

So the only word that satisfies $\theta \wedge \psi_x$ without Accept is the computation word, and Accept holds on it iff the computation reaches $q_{\mathrm{acc}}$, that is, iff $T$ accepts $x$. $\square$

**Hardness of satisfiability.** The map $x \mapsto \theta \wedge \psi_x$ is a polynomial-time reduction from $A$ to satisfiability. Since $A$ is PSPACE-complete, satisfiability is PSPACE-hard.

**Hardness of model checking for a fixed structure.** Let $M_0$ be the structure with states $\Delta$, the single initial state $\#$, all transitions $\Delta \times \Delta$, and labels $L(a) = \{a\}$. It depends only on $T$. The traces of the paths of $M_0$ are exactly the words that start with $\#$ and have exactly one letter at each position. By Lemma 3, $T$ accepts $x$ iff some path of $M_0$ satisfies $\psi_x$, iff $M_0 \not\models \neg\psi_x$. So $x \mapsto \neg\psi_x$ reduces the complement of $A$ to model checking on $M_0$. Every language $B$ in PSPACE has its complement in PSPACE, which reduces to $A$, so $\overline{B}$ reduces to the complement of $A$, and $B$ reduces to model checking on $M_0$. So model checking is PSPACE-hard for the fixed structure $M_0$ and the fixed set $AP = \Delta$. $\blacksquare$

## Consequences

- **The automata-based algorithm is the right shape.** The time $O(|M| \cdot 2^{O(|\varphi|)})$ of the [automata-theoretic approach](/automata-theoretic-approach/) is linear in the system, which is usually large, and exponential only in the formula, which is usually short. Lichtenstein and Pnueli (1985) made this point with the same bound.
- **Fixed formula.** For a fixed $\varphi$, the space bound $O(|\varphi| + \log |M|)$ of the nondeterministic procedure is $O(\log |M|)$, so the complement is in nondeterministic [logarithmic space](/logspace/), and so is the problem itself by the [Immerman-Szelepcsényi theorem](/immerman-szelepcsenyi-theorem/). It is hard for this class already for $\varphi = \mathsf{G}\neg p$, since $M \not\models \mathsf{G}\neg p$ iff a state labelled $p$ is reachable, which is [graph reachability](/graph-reachability/).
- **Concurrent systems.** If $M$ is given as a product of $n$ components, $|S|$ can be exponential in the input, but $\log |S|$ is polynomial in it. The space-bounded procedure only stores states, so the problem stays in PSPACE in the size of the components. This is the space side of the [state explosion problem](/state-explosion-problem/).
- **Validity.** $\varphi$ is valid iff $\neg\varphi$ is unsatisfiable, so LTL validity is PSPACE-complete, since PSPACE is closed under complement.
- **Contrast with branching time.** [CTL model checking](/ctl-model-checking/) takes $O(|M| \cdot |\varphi|)$ time, polynomial in both inputs. The jump to PSPACE comes from the path quantifier over formulas with nested temporal operators.
- **Fragments.** Sistla and Clarke also show that for the fragment with only $\mathsf{F}$ and the Boolean connectives, satisfiability and the existential form of model checking are NP-complete, and that the fragments with $\mathsf{F}$ and $\mathsf{X}$, and with $\mathsf{U}$ only, are PSPACE-complete again.

## Tightness

- **The exponent in the formula.** Model checking is PSPACE-hard for the fixed structure $M_0$. A decision procedure for $M_0$ that runs in time polynomial in $|\varphi|$ would put a PSPACE-complete problem in P, so the factor $2^{O(|\varphi|)}$ cannot be made polynomial unless P = PSPACE.
- **The factor in the structure.** The time is linear in $|M|$, and an algorithm must read all of $M$ in the worst case, so this factor cannot be improved.
- **The operators.** Hardness needs operators that can count distances. Without $\mathsf{X}$ and $\mathsf{U}$, in the fragment with only $\mathsf{F}$, the problems are in NP, so they are not PSPACE-hard unless NP = PSPACE.
- **The propositions.** The proof uses the fixed set $\Delta$ of propositions, so the hardness does not come from a growing alphabet.

## History

Pnueli proposed linear temporal logic for programs in 1977. Sistla and Clarke announced the complexity results at STOC 1982 and published them in the Journal of the ACM in 1985. In the same year, Lichtenstein and Pnueli gave a tableau algorithm for model checking whose time is linear in the program and exponential in the formula, and argued that the size of the program is the important parameter. Vardi and Wolper (1986) recast satisfiability and model checking as questions about Büchi automata, and gave the polynomial-space algorithm that builds the automaton for the formula on the fly, as in the space bound above. The encoding of a Turing machine as a temporal formula follows the same plan as the earlier proofs of Meyer and Stockmeyer for [regular expressions](/regex-equivalence-pspace-completeness/).

## References
