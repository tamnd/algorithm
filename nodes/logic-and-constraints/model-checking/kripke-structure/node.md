---
tag: N8EBZT
kind: definition
slug: kripke-structure
name: Kripke structure
aliases:
- Kripke model
- Kripke frame with a labelling
area: logic-and-constraints/model-checking
level: intro
summary: A finite graph of states with a total transition relation, a set of initial states, and a labelling that says which atomic propositions are true in each state.
prereqs: [directed-graph]
see_also: [labelled-transition-system, computation-tree-logic, temporal-logic, reachability-problem, state-explosion-problem, bisimulation, ctl-model-checking, linear-temporal-logic]
sources:
  - book: isbn:9780262026499
    title: Christel Baier and Joost-Pieter Katoen, Principles of Model Checking, MIT Press, 2008
    locator: Chapter 2, Section 2.1 (transition systems with a labelling function; Kripke structures are the case without actions), and Section 2.2 (interleaving and parallel composition)
  - book: isbn:9780262032704
    title: Edmund M. Clarke, Orna Grumberg and Doron A. Peled, Model Checking, MIT Press, 1999
    locator: Chapter 2 (modelling systems as Kripke structures, with a total transition relation) and Chapter 3 (paths and the semantics of CTL* over Kripke structures)
  - paper: "Saul A. Kripke, Semantical considerations on modal logic, Acta Philosophica Fennica 16, 1963, pages 83 to 94"
    locator: the relational semantics of modal logic (worlds, an accessibility relation and a valuation)
---

A Kripke structure is a finite [directed graph](/directed-graph/) whose vertices are the states of a system, whose edges are its possible steps, and whose states are labelled with the atomic propositions that are true in them. It is the standard model of a finite-state system for [temporal logic](/temporal-logic/) and model checking. The name comes from Saul Kripke's relational semantics of modal logic (1963), where the states are "possible worlds".

## Definition

Fix a finite set $AP$ of *atomic propositions*. A **Kripke structure** over $AP$ is a tuple $M = (S, I, R, L)$ where

- $S$ is a finite set of *states*,
- $I \subseteq S$ is a non-empty set of *initial states*,
- $R \subseteq S \times S$ is the *transition relation*, and it is **total**: for each $s \in S$ there is a $t \in S$ with $(s, t) \in R$,
- $L : S \to 2^{AP}$ is the *labelling function*: $L(s)$ is the set of atomic propositions that are true in $s$.

We write $R(s) = \{t : (s, t) \in R\}$ for the successors of $s$. A **path** from $s$ is an infinite sequence $\pi = s_0 s_1 s_2 \ldots$ with $s_0 = s$ and $(s_i, s_{i+1}) \in R$ for each $i \ge 0$. We write $\pi[i] = s_i$ and $\pi^i = s_i s_{i+1} \ldots$ for the suffix. Because $R$ is total, each finite path extends to an infinite one, so each state has at least one path. The **trace** of $\pi$ is the word $L(s_0) L(s_1) L(s_2) \ldots \in (2^{AP})^\omega$. The **computation tree** of $s$ is the unfolding of $M$ from $s$: its nodes are the finite paths from $s$, and the children of a node are its one-step extensions.

**Size.** On the pages of this area, $|S|$ is the number of states, $|R|$ the number of transitions, and $|M| = |S| + |R|$. A model checking algorithm that runs in $O(|M|)$ time per formula symbol is linear in the size of the graph, stored as [adjacency lists](/adjacency-list/). The size of a formula $\varphi$ is $|\varphi|$, the number of its symbols.

**Conventions that vary.** Some books drop $I$ and speak of a state $s$ of $M$. Some allow $S$ to be infinite. Some allow states with no successor; then the semantics of $\mathsf{AX}$ and of path formulas needs a rule for finite paths. Baier and Katoen allow *terminal states* in a transition system, but they assume that there are none when they define the semantics of CTL and LTL. A standard fix is to add a self-loop to each state with no successor, and to mark it with a new proposition $\mathit{dead}$, as the page on [deadlock detection](/deadlock-freedom-checking/) does.

## Examples and non-examples

**A mutual exclusion protocol.** Two processes share a semaphore $y \in \{0, 1\}$. Process $i$ moves from $n_i$ (non-critical) to $w_i$ (waiting), from $w_i$ to $c_i$ (critical) only when $y = 1$, and then sets $y = 0$, and from $c_i$ back to $n_i$, which sets $y = 1$. At each step one process moves (interleaving). A state is a triple $(\ell_1, \ell_2, y)$, so the full product has $3 \cdot 3 \cdot 2 = 18$ states. From the initial state $(n, n, 1)$, only 8 states are reachable, with 14 transitions:

| state | label | successors |
|---|---|---|
| $(n, n, 1)$ | $n_1, n_2$ | $(w, n, 1)$, $(n, w, 1)$ |
| $(w, n, 1)$ | $w_1, n_2$ | $(c, n, 0)$, $(w, w, 1)$ |
| $(n, w, 1)$ | $n_1, w_2$ | $(w, w, 1)$, $(n, c, 0)$ |
| $(c, n, 0)$ | $c_1, n_2$ | $(n, n, 1)$, $(c, w, 0)$ |
| $(w, w, 1)$ | $w_1, w_2$ | $(c, w, 0)$, $(w, c, 0)$ |
| $(n, c, 0)$ | $n_1, c_2$ | $(w, c, 0)$, $(n, n, 1)$ |
| $(c, w, 0)$ | $c_1, w_2$ | $(n, w, 1)$ |
| $(w, c, 0)$ | $w_1, c_2$ | $(w, n, 1)$ |

Each state has a successor, so $R$ is total. No reachable state has the label $c_1$ and $c_2$ together, so the [safety property](/safety-property/) "never both critical" holds. The structure also has the path $(w,n,1)\,(w,w,1)\,(w,c,0)\,(w,n,1) \ldots$ on which process 1 waits forever, which is why the page on [fairness](/fairness/) uses this example.

**A program.** A program with $k$ Boolean variables and a program counter with $c$ values gives a Kripke structure with at most $c \cdot 2^k$ states. The propositions are the variables and the program locations. This is the source of the [state explosion problem](/state-explosion-problem/): the structure is exponential in the program text.

**Non-example: a state with no successor.** The graph $s \to t$ with no edge out of $t$ is not a Kripke structure in the sense above, because $R$ is not total at $t$. The formula $\mathsf{AG}\,\mathsf{EX}\,\mathit{true}$ is the CTL statement that no reachable state is a dead end.

**Non-example: labels on edges.** A graph whose edges carry action names, such as $s \xrightarrow{\mathit{send}} t$, is a [labelled transition system](/labelled-transition-system/). It carries its information on the transitions, not on the states. The two models convert into each other, as the related definitions below show.

## Related definitions

- **Labelled transition system.** A [labelled transition system](/labelled-transition-system/) $(S, \mathit{Act}, \to, s_0)$ labels the transitions with actions. To turn it into a Kripke structure, make a state for each pair (state, last action) and label it with that action. To go the other way, put the label of the target state on each edge.
- **Kripke frame.** In modal logic, a frame is the pair $(S, R)$ with no labelling and no totality condition, and a Kripke model is a frame with a valuation. The modal operators $\Diamond$ and $\Box$ of the [modal mu-calculus](/modal-mu-calculus/) quantify over $R(s)$.
- **Fair Kripke structure.** A structure with fairness constraints, sets $F_1, \ldots, F_k \subseteq S$ that a fair path must visit infinitely often. See [fairness](/fairness/).
- **Product.** The synchronous or interleaved product of several structures models a system of processes. The size of the product is the product of the sizes.
- **Bisimulation.** Two states are [bisimilar](/bisimulation/) when they have the same labels and each step of one is matched by a step of the other to a bisimilar state. Bisimilar states satisfy the same CTL, CTL* and mu-calculus formulas.
- **Logics on Kripke structures.** [Computation tree logic](/computation-tree-logic/) and [CTL*](/ctl-star/) speak about the computation tree. [Linear temporal logic](/linear-temporal-logic/) speaks about the traces of the paths from the initial states.

## References
