---
tag: FW51SZ
kind: definition
slug: nondeterministic-logspace
name: NL (NLOGSPACE)
aliases:
- NL
- NLOGSPACE
area: complexity/complexity-classes
level: core
summary: The decision problems that a nondeterministic Turing machine solves with O(log n) work space. Directed reachability is complete for NL under logspace reductions.
prereqs: [logspace, nondeterministic-turing-machine, graph-reachability]
see_also: [savitch-theorem, immerman-szelepcsenyi-theorem, 2-sat, symmetric-logspace, randomized-logspace, nc, pspace, strongly-connected-components]
sources:
  - book: isbn:9781133187790
    title: Michael Sipser, Introduction to the Theory of Computation, third edition, Cengage (2013)
    locator: Section 8.4, The Classes L and NL; Section 8.5, NL-Completeness; Section 8.6, NL Equals coNL
  - book: isbn:9780521424264
    title: Sanjeev Arora and Boaz Barak, Computational Complexity, A Modern Approach, Cambridge University Press (2009)
    locator: Chapter 4, Space Complexity (NL, the certificate definition and NL-completeness)
  - paper: doi:10.1016/S0022-0000(75)80050-X
    title: Neil D. Jones, Space-bounded reducibility among combinatorial problems, Journal of Computer and System Sciences 11(1), 68 to 85 (1975)
    locator: logspace reductions; directed reachability is complete for nondeterministic log space
  - paper: doi:10.1007/BF01683259
    title: Neil D. Jones, Y. Edmund Lien and William T. Laaser, New problems complete for nondeterministic log space, Mathematical Systems Theory 10(1), 1 to 17 (1976)
    locator: the unsatisfiability of 2-CNF formulas is complete for NL
  - paper: doi:10.1137/0217058
    title: Neil Immerman, Nondeterministic space is closed under complementation, SIAM Journal on Computing 17(5), 935 to 938 (1988)
    locator: NL equals coNL
---

NL, also written NLOGSPACE, is the class of decision problems that a nondeterministic Turing machine decides with $O(\log n)$ cells of work tape, with the input on a read-only tape. It is the class of problems whose yes-instances have a path of polynomial length through a graph of polynomial size that a logspace machine can explore one step at a time. Directed [graph reachability](/graph-reachability/) is the typical problem, and it is NL-complete under logspace reductions. NL lies between L and P. It is a subset of $\mathsf{DSPACE}(\log^2 n)$ by [Savitch's theorem](/savitch-theorem/), and it is closed under complement by the [Immerman-Szelepcsényi theorem](/immerman-szelepcsenyi-theorem/). Whether NL equals L is open.

## Definition

**Model.** The machine is a [nondeterministic Turing machine](/nondeterministic-turing-machine/) with a read-only input tape and $k$ work tapes, as for [L](/logspace/). Only the work tapes count toward the space. The machine accepts $x$ if at least one computation branch accepts.

**Definition.** $\mathsf{NSPACE}(s(n))$ is the class of languages $A$ such that a nondeterministic machine accepts exactly the strings in $A$, and every branch on every input of length $n$ halts and uses at most $c \cdot s(n)$ work cells, for a constant $c$. Then

$$\mathsf{NL} = \mathsf{NSPACE}(\log n).$$

The halting condition costs nothing. A machine with space $c \log n$ has at most $N = n^{O(1)}$ configurations, as on the page for [L](/logspace/). An accepting branch can be cut to one that repeats no configuration, so it has fewer than $N$ steps. A counter of $O(\log n)$ bits can stop every branch after $N$ steps without losing an accepting branch.

**Certificate definition.** A language $A$ is in NL if and only if there are a polynomial $p$ and a deterministic logspace machine $V$ with a second input tape, the certificate tape, whose head moves only to the right, such that for every $x$:

$$x \in A \iff \exists u \in \{0,1\}^{p(|x|)} : V \text{ accepts } (x, u).$$

From a nondeterministic machine, take $u$ to be the sequence of its choices. From $V$, guess the bits of $u$ one at a time, when $V$ reads them. The read-once condition matters: $V$ cannot store $u$, and a nondeterministic machine cannot read its earlier guesses again. With a certificate tape that $V$ may read in both directions, the same definition gives NP (Arora and Barak, Chapter 4).

**NL-completeness.** A language $B$ is *NL-complete* if $B \in \mathsf{NL}$ and $A \le_{\mathrm{L}} B$ for every $A \in \mathsf{NL}$, where $\le_{\mathrm{L}}$ is the logspace many-one reduction defined on the page for [L](/logspace/). Polynomial-time reductions are useless here: since $\mathsf{NL} \subseteq \mathsf{P}$, a polynomial-time reduction can solve the instance itself, so every language in NL other than the empty set and the set of all strings would be complete. Logspace reductions compose, so if one NL-complete language is in L, then $\mathsf{L} = \mathsf{NL}$.

**Theorem (Jones 1975).** PATH $= \{\langle G, s, t\rangle : G$ is a directed graph with a path from $s$ to $t\}$ is NL-complete.

*Membership.* The machine keeps a current vertex $v$, which starts at $s$, and a step counter. At each step, it accepts if $v = t$; otherwise it guesses a vertex $w$, checks on the input that $(v, w)$ is an edge, rejects if it is not, and sets $v \leftarrow w$. It rejects after $n - 1$ steps. The vertex and the counter take $O(\log n)$ bits. Some branch accepts if and only if a path from $s$ to $t$ exists, because a shortest path has at most $n - 1$ edges.

*Hardness.* Let $M$ decide $A$ in space $c \log n$. Change $M$ so that before it accepts, it erases its work tapes and moves all heads to the left end. Then it has one accepting configuration $C_{\mathrm{acc}}$. The *configuration graph* $G_{M,x}$ has one vertex for each configuration of $M$ on $x$ and an edge $C \to C'$ if $M$ can go from $C$ to $C'$ in one step. Then $x \in A$ if and only if $C_{\mathrm{acc}}$ is reachable from the start configuration $C_0$ in $G_{M,x}$. The reduction outputs $\langle G_{M,x}, C_0, C_{\mathrm{acc}}\rangle$. A configuration is a string of $O(\log n)$ bits, so the transducer can go through all pairs $(C, C')$ in order. For each pair, it reads the input symbol under the input head of $C$ and checks the transition table of $M$, which is fixed. It writes the edge when the move is legal. This takes $O(\log n)$ space, and the output has $n^{O(1)}$ edges. $\square$

## Examples and non-examples

**2-SAT.** The unsatisfiability of a formula in 2-CNF is NL-complete under logspace reductions (Jones, Lien and Laaser 1976). Because NL is closed under complement, satisfiability of 2-CNF formulas is NL-complete as well. See [2-SAT](/2-sat/) for the linear-time algorithm.

- *2-UNSAT is in NL.* Each clause $(a \lor b)$ gives the edges $\lnot a \to b$ and $\lnot b \to a$ of the implication graph. The formula is unsatisfiable if and only if some variable $x$ has a path from $x$ to $\lnot x$ and a path from $\lnot x$ to $x$. An NL machine guesses $x$ and the two paths.
- *PATH reduces to 2-UNSAT.* Given $\langle G, s, t\rangle$, make one variable $x_v$ for each vertex $v$, the clause $(\lnot x_u \lor x_v)$ for each edge $u \to v$, and the two unit clauses $(x_s)$ and $(\lnot x_t)$, each written as a 2-clause with the literal twice. Each clause depends on one edge, so a logspace transducer writes the formula in one pass, and its size is $O(|E|)$ clauses.
- *Path implies unsatisfiable.* Let $s = v_0 \to v_1 \to \cdots \to v_k = t$ be a path. A satisfying assignment must set $x_s$ true, and then the clauses for the edges force $x_{v_1}, \ldots, x_{v_k}$ true in turn. That makes $x_t$ true, which contradicts $(\lnot x_t)$.
- *Unsatisfiable implies a path.* Suppose no path exists. Set $x_v$ true exactly when $v$ is reachable from $s$. Then $(x_s)$ holds, $(\lnot x_t)$ holds, and a clause $(\lnot x_u \lor x_v)$ can only fail if $u$ is reachable and $v$ is not, which is impossible since $u \to v$ is an edge. So the formula is satisfiable.

*Worked example.* Take the vertices 0 to 4 and the edges $0 \to 1$, $1 \to 2$, $2 \to 0$, $2 \to 3$ and $4 \to 3$. The formula has the clauses $(\lnot x_0 \lor x_1)$, $(\lnot x_1 \lor x_2)$, $(\lnot x_2 \lor x_0)$, $(\lnot x_2 \lor x_3)$ and $(\lnot x_4 \lor x_3)$, plus the unit clauses. For $s = 0$ and $t = 3$, the path $0 \to 1 \to 2 \to 3$ forces $x_0, x_1, x_2, x_3$ true against $(\lnot x_3)$, so the formula is unsatisfiable. For $s = 0$ and $t = 4$, the vertices reachable from 0 are 0, 1, 2 and 3. The assignment $x_0 = x_1 = x_2 = x_3 = 1$, $x_4 = 0$ satisfies every clause, and indeed 4 is not reachable.

**Strong connectivity.** Whether a directed graph is strongly connected is in NL: the machine goes through all ordered pairs $(u, v)$ and guesses a path from $u$ to $v$ for each, and it rejects as soon as a guess fails. An accepting branch exists if and only if every pair is connected. See [strongly connected components](/strongly-connected-components/).

**Acyclicity.** A directed graph has a cycle if and only if some vertex $v$ reaches itself by a path of length at least 1, and an NL machine can guess $v$ and the path. So acyclicity is in coNL, and by $\mathsf{NL} = \mathsf{coNL}$ it is in NL. No direct NL algorithm for it is obvious: the machine must certify that something does not exist, and the inductive counting of the [Immerman-Szelepcsényi theorem](/immerman-szelepcsenyi-theorem/) is how it does that.

**Undirected reachability.** It is in NL, and in fact in L by Reingold's theorem. See [SL](/symmetric-logspace/).

**QSAT (not in NL).** [QSAT](/qsat/) is PSPACE-complete under logspace reductions, and $\mathsf{NL} \subseteq \mathsf{DSPACE}(\log^2 n) \subsetneq \mathsf{PSPACE}$ by Savitch's theorem and the [space hierarchy theorem](/space-hierarchy-theorem/). So QSAT is not in NL. This is an unconditional non-example.

**Circuit value (not known to be in NL).** The [circuit value problem](/circuit-value-problem/) is P-complete under logspace reductions, so it is in NL if and only if $\mathsf{NL} = \mathsf{P}$, which is open.

## Related definitions

- **L.** $\mathsf{L} \subseteq \mathsf{NL}$, since a deterministic machine is a nondeterministic one with one choice. Whether the inclusion is strict is open. See [L](/logspace/).
- **coNL.** The class of complements of languages in NL. $\mathsf{NL} = \mathsf{coNL}$ (Immerman 1988; Szelepcsényi 1988). The same statement for time, NP against coNP, is open, and NL = coNL says nothing about it.
- **Deterministic space.** $\mathsf{NL} \subseteq \mathsf{DSPACE}(\log^2 n)$ by [Savitch's theorem](/savitch-theorem/), and $\mathsf{NL} \subseteq \mathsf{P}$ by a search of the configuration graph, which has polynomial size.
- **Circuits.** $\mathsf{NL} \subseteq \mathsf{NC}^2$ (Borodin 1977): reachability in $G$ is computed by $\lceil \log_2 n \rceil$ squarings of the Boolean adjacency matrix with self-loops added. See [NC](/nc/).
- **SL and RL.** Both are subsets of NL. SL equals L. See [symmetric logspace](/symmetric-logspace/) and [randomized logspace](/randomized-logspace/).
- **PSPACE.** $\mathsf{NL} \ne \mathsf{PSPACE}$, as shown above. See [PSPACE](/pspace/).

## References
