---
title: Symbolic simulation gives the exact output function of every cycle
proves: [correctness]
status: full
---

**Setting.** $C$ is a synchronous circuit with primary inputs $X$, latches $S$, gates $g_1, \ldots, g_m$ in topological order and outputs $O$. Each gate $u$ has an operator $\mathrm{op}(u)$, a Boolean function of its fanins, and each latch $s$ has a next-state node $\mathrm{next}(s)$ and an initial value $\mathrm{init}(s) \in \{0, 1, ?\}$. The variables are $s^0$ for each latch with $\mathrm{init}(s) = {?}$ and $x_t$ for each input $x$ and each cycle $0 \le t < k$. A run is an assignment $\alpha$ of 0 or 1 to all variables. It fixes the unknown initial values and the input vector of every cycle, and every such choice is one assignment.

**Concrete semantics.** For a run $\alpha$, two-valued simulation defines $\sigma_0(s) = \mathrm{init}(s)$ if it is 0 or 1 and $\sigma_0(s) = \alpha(s^0)$ otherwise. In cycle $t$ it sets $\mathrm{val}_t(x) = \alpha(x_t)$ for $x \in X$, $\mathrm{val}_t(s) = \sigma_t(s)$ for $s \in S$, $\mathrm{val}_t(u) = \mathrm{op}(u)(\mathrm{val}_t \text{ of the fanins of } u)$ for each gate in topological order, and then $\sigma_{t+1}(s) = \mathrm{val}_t(\mathrm{next}(s))$.

**Claim.** After SYMBOLIC-SIMULATE($C$, $k$), for every cycle $t < k$, output $o$ and run $\alpha$, the BDD $O_t(o)$ evaluated at $\alpha$ is $\mathrm{val}_t(o)$ in the run $\alpha$. Moreover, for outputs $o, o'$ and cycles $t, t'$ of circuits simulated with the same manager and variables, $O_t(o) = O_{t'}(o')$ as nodes if and only if the two values agree in every run.

For a BDD $f$ write $f(\alpha)$ for its value at $\alpha$.

**Fact 1 (Apply).** For every binary operator $\circ$, Apply returns a BDD $h$ with $h(\alpha) = f(\alpha) \circ g(\alpha)$ for every $\alpha$, and negation returns $h$ with $h(\alpha) = 1 - f(\alpha)$ (Bryant 1986, see [Apply](/bdd-apply/)). A gate with $d$ fanins is folded as $d - 1$ applies of an associative operator, followed by a negation for NAND, NOR and XNOR, so by induction on $d$ the BDD of line L5 evaluates at every $\alpha$ to $\mathrm{op}(u)$ of the fanin values at $\alpha$.

**Lemma (invariant).** At the start of cycle $t$ (before line L3), $S(s)(\alpha) = \sigma_t(s)$ for every latch $s$ and every run $\alpha$. After line L5 of cycle $t$, $V(u)(\alpha) = \mathrm{val}_t(u)$ for every node $u$ and every run $\alpha$.

*Proof.* By induction on $t$, and inside a cycle on the position of $u$ in the order inputs, latches, $g_1, \ldots, g_m$.

*Base, $t = 0$, latches.* Line L1 sets $S(s)$ to the constant $\mathrm{init}(s)$ or to the BDD of the variable $s^0$. The constant evaluates to $\mathrm{init}(s) = \sigma_0(s)$, and the variable evaluates to $\alpha(s^0) = \sigma_0(s)$.

*Inside cycle $t$.* Assume the claim on $S$ at the start of cycle $t$. Line L3 sets $V(x)$ to the variable $x_t$, so $V(x)(\alpha) = \alpha(x_t) = \mathrm{val}_t(x)$. Line L4 sets $V(s) = S(s)$, so $V(s)(\alpha) = \sigma_t(s) = \mathrm{val}_t(s)$. Take the gates in topological order, and assume the claim for every node before $g_j$. All fanins of $g_j$ are inputs, latches or earlier gates, so their $V$ already holds and evaluates at $\alpha$ to their $\mathrm{val}_t$. By Fact 1, $V(g_j)(\alpha) = \mathrm{op}(g_j)(\mathrm{val}_t \text{ of the fanins}) = \mathrm{val}_t(g_j)$. No later step of cycle $t$ changes $V(g_j)$.

*Step to cycle $t + 1$.* Line L7 sets $S(s) = V(\mathrm{next}(s))$, which evaluates at $\alpha$ to $\mathrm{val}_t(\mathrm{next}(s)) = \sigma_{t+1}(s)$. This is the claim on $S$ at the start of cycle $t + 1$. $\square$

**Proof of the claim.** Line L6 copies $V(o)$ after line L5 of cycle $t$, and no later line changes the copy, so the Lemma gives $O_t(o)(\alpha) = \mathrm{val}_t(o)$ for every run $\alpha$. This is the first part.

For the second part, $O_t(o)$ and $O_{t'}(o')$ are reduced ordered BDDs of one manager over one variable order. Such a BDD is canonical: two of them are the same node exactly when they represent the same function of the variables (Bryant 1986, see [reduced ordered BDD](/reduced-ordered-bdd/)). The manager keeps this because MK returns the existing node of each triple and never makes a node with equal children. By the first part, the function of $O_t(o)$ maps each run to the value of $o$ in cycle $t$, and every assignment is a run. So the two nodes are equal exactly when the two values agree in every run. $\blacksquare$

**Consequence.** A property $P$ built from output values with Boolean operators holds in every run of length $k$ exactly when its BDD, built from the $O_t(o)$ by Apply, is the terminal 1. If it is not, a path from the root to the terminal 0 gives values for some variables, and any values for the others give a run in which $P$ is false.
