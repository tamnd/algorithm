---
tag: ZS9SA0
kind: definition
slug: stuttering-equivalence
name: Stuttering equivalence
aliases:
- Stutter-invariant equivalence
- Stutter bisimulation
- Stuttering bisimilarity
area: logic-and-constraints/model-checking
level: advanced
summary: An equivalence that ignores finite repetitions of the same label along paths; for finite Kripke structures it coincides with agreement on all CTL* formulas without the next operator.
prereqs: [bisimulation, kripke-structure, ctl-star, linear-temporal-logic]
see_also: [bisimulation, simulation-relation, trace-equivalence, equivalence-checking, partial-order-reduction, partition-refinement, ctl-star, linear-temporal-logic]
sources:
  - paper: doi:10.1016/0304-3975(88)90098-9
    title: Michael C. Browne, Edmund M. Clarke and Orna Grumberg, Characterizing finite Kripke structures in propositional temporal logic, Theoretical Computer Science 59, 1988
    locator: pages 115 to 131 (stuttering equivalence of states, and its characterization by CTL* without the next operator for finite structures)
  - paper: doi:10.1007/BFb0032063
    title: Jan Friso Groote and Frits Vaandrager, An efficient algorithm for branching bisimulation and stuttering equivalence, ICALP 1990, LNCS 443
    locator: pages 626 to 638 (the splitting of blocks by reachability inside a block, and the O(mn) time bound)
  - paper: doi:10.1145/201019.201032
    title: Rocco De Nicola and Frits Vaandrager, Three logics for branching bisimulation, Journal of the ACM 42(2), 1995
    locator: pages 458 to 487 (the relation between branching bisimulation and the stuttering equivalence of Browne, Clarke and Grumberg, and the role of divergence)
  - book: isbn:9780262026499
    title: Christel Baier and Joost-Pieter Katoen, Principles of Model Checking, MIT Press, 2008
    locator: Sections 7.7 and 7.8 (stutter trace equivalence, stutter bisimulation, divergence-sensitive stutter bisimulation and CTL* without next)
---

Stuttering equivalence relates states, or paths, of [Kripke structures](/kripke-structure/) whose behaviours differ only in how many times a label is repeated in a row. A path that shows the labels $p, p, p, q, q, r, \ldots$ and one that shows $p, q, r, \ldots$ are stuttering equivalent, because each block of equal labels in one corresponds to a block of the same label in the other. For paths, this is the reason why [LTL](/linear-temporal-logic/) without the next operator $\mathbf{X}$ cannot tell such paths apart, which is the basis of [partial order reduction](/partial-order-reduction/). For states, Browne, Clarke and Grumberg (1988) defined a branching version and proved that, in finite Kripke structures, two states are stuttering equivalent if and only if they satisfy the same formulas of CTL\* without $\mathbf{X}$, and that CTL without $\mathbf{X}$ already suffices. De Nicola and Vaandrager (1995) showed that this equivalence is the *divergence-sensitive* form of branching bisimulation. It is coarser than [bisimulation](/bisimulation/), which also respects the number of steps. Groote and Vaandrager (1990) gave an $O(mn)$ algorithm for it, so a model checker can reduce a structure modulo stuttering before it checks properties without $\mathbf{X}$.

## Definition

Let $M = (S, R_T, L)$ be a Kripke structure with a total transition relation and labelling $L : S \to 2^{\mathit{AP}}$.

**Stuttering equivalent paths.** Two infinite paths $\pi = s_0 s_1 \ldots$ and $\rho = t_0 t_1 \ldots$ are *stuttering equivalent* if they can be cut into finite nonempty blocks $\pi = B_1 B_2 \ldots$ and $\rho = C_1 C_2 \ldots$ such that, for each $i$, all states in $B_i$ and in $C_i$ have the same label. Equivalently, the label sequences become equal after each maximal run of a repeated label is replaced by one copy of it.

**Stutter invariance.** An LTL formula $\varphi$ is *stutter invariant* if, for any two stuttering equivalent paths, $\varphi$ holds on both or on neither. Every formula of LTL without $\mathbf{X}$ is stutter invariant, by induction on the formula. Peled and Wilke (1997) proved the converse: every stutter invariant LTL property can be written without $\mathbf{X}$.

**Stutter bisimulation.** A symmetric relation $R \subseteq S \times S$ is a *divergence-blind stutter bisimulation* if for every $(s, t) \in R$:

1. $L(s) = L(t)$, and
2. for every $s'$ with $(s, s') \in R_T$, either $(s', t) \in R$, or there is a path $t = t_0 \to t_1 \to \cdots \to t_k$ with $k \ge 1$, $(s, t_i) \in R$ for all $i < k$, and $(s', t_k) \in R$.

So a step of $s$ that changes its class can be matched by some steps of $t$ that stay in the class of $s$, followed by one step into the class of $s'$, and a step that stays in the class needs no match. The union of all such relations is an equivalence, the greatest fixed point of the conditions, as for bisimulation.

**Divergence.** Call $s$ *divergent* for a relation $R$ if there is an infinite path $s = u_0 \to u_1 \to \cdots$ with $(s, u_i) \in R$ for all $i$. A stutter bisimulation is *divergence-sensitive* if, in addition, for every $(s, t) \in R$, $s$ is divergent if and only if $t$ is. *Stuttering equivalence* $\approx$ is the largest divergence-sensitive stutter bisimulation.

**Theorem (Browne, Clarke and Grumberg, 1988; in this form De Nicola and Vaandrager, 1995).** For a finite Kripke structure with a total transition relation and states $s, t$, the following are equivalent: $s \approx t$; $s$ and $t$ satisfy the same CTL\* formulas without $\mathbf{X}$; $s$ and $t$ satisfy the same CTL formulas without $\mathbf{X}$. Browne, Clarke and Grumberg defined the equivalence with a decreasing sequence of relations on paths, cut into corresponding blocks; De Nicola and Vaandrager showed that this is the same relation as divergence-sensitive branching bisimulation, written above for Kripke structures.

**Computation (Groote and Vaandrager, 1990).** Start with the partition by labels. A block $B$ is split by another block $C$ into the states of $B$ that can reach, by a path inside $B$, a state with a successor in $C$, and the other states of $B$. When no split is possible, the partition is the divergence-blind stuttering equivalence. With cycles inside blocks contracted first and careful bookkeeping, the time is $O(mn)$ for $n$ states and $m$ transitions. Divergence can be handled by marking the states that can stay in their own class forever, so that they cannot be merged with states that cannot. Later algorithms, such as that of Groote, Jansen, Keiren and Wijs (2017), reach $O(m \log n)$ for branching bisimulation.

## Examples and non-examples

**Equivalent, not bisimilar.** Let $s_0 \to s_1 \to s_2 \to s_2$ with $L(s_0) = L(s_1) = \{p\}$ and $L(s_2) = \{q\}$, and $t_0 \to t_2 \to t_2$ with $L(t_0) = \{p\}$ and $L(t_2) = \{q\}$. The relation that relates $s_0$, $s_1$ and $t_0$ to each other, and $s_2$ to $t_2$, is a divergence-sensitive stutter bisimulation: the step $s_0 \to s_1$ stays in the class, and the step $s_1 \to s_2$ is matched by $t_0 \to t_2$. No state is divergent in a $p$-class. So $s_0 \approx t_0$. But $s_0 \not\sim t_0$, because $s_0 \models \mathbf{EX}\,p$ and $t_0 \not\models \mathbf{EX}\,p$.

**Divergence matters.** Let $u_0 \to u_0$ and $u_0 \to u_2 \to u_2$, with $L(u_0) = \{p\}$ and $L(u_2) = \{q\}$. Compare $u_0$ with $t_0$ above. The divergence-blind conditions hold for the relation that relates $u_0$ with $t_0$ and $u_2$ with $t_2$, since the self-loop of $u_0$ stays in the class. But $u_0$ is divergent and $t_0$ is not, so $u_0 \not\approx t_0$. The CTL formula $\mathbf{EG}\,p$, which has no $\mathbf{X}$, holds at $u_0$ and fails at $t_0$. This is why the divergence condition is part of the definition.

**Not equivalent.** Let $v_0 \to v_1$ and $v_0 \to v_2$, with $L(v_0) = \{p\}$, $L(v_1) = \{q\}$, $L(v_2) = \{r\}$, and self-loops on $v_1$ and $v_2$. Let $w_0 \to w_1 \to w_2$ with $L(w_0) = L(w_1) = \{p\}$, $L(w_2) = \{q\}$, a self-loop on $w_2$, and an extra step $w_0 \to w_3$ to a state labelled $\{r\}$ with a self-loop. Then $w_1$ has no path to $r$, but $w_0$ does, so $w_0$ and $w_1$ are in different classes, and $\mathbf{E}[p\, \mathbf{U}\, (p \wedge \neg \mathbf{E}[p\, \mathbf{U}\, r])]$ holds at $w_0$ and fails at $v_0$. So $v_0 \not\approx w_0$, although both have the same paths up to stuttering.

**Stuttering paths.** The paths with labels $p\,p\,q\,q\,q\,r^\omega$ and $p\,q\,r^\omega$ are stuttering equivalent. The LTL formula $\mathbf{X}\,q$ holds on the second and fails on the first; the formula $p\, \mathbf{U}\, q$ holds on both.

## Related definitions

- [Bisimulation](/bisimulation/): each step must be matched by exactly one step. Bisimilarity implies stuttering equivalence and preserves all of CTL\*, including $\mathbf{X}$.
- Branching bisimulation and weak bisimulation: the corresponding notions for labelled transition systems with an internal action $\tau$, where $\tau$-steps inside a class play the role of stuttering steps. Branching bisimulation keeps the branching structure at intermediate states, weak bisimulation does not.
- Stutter trace equivalence: equality of the sets of paths up to stuttering. It is the linear-time counterpart and preserves LTL without $\mathbf{X}$; it relates to stuttering equivalence as [trace equivalence](/trace-equivalence/) relates to bisimilarity.
- [Simulation relation](/simulation-relation/): stuttering simulations preserve the universal fragment of CTL\* without $\mathbf{X}$.
- [Partial order reduction](/partial-order-reduction/): the reduced state graph is stutter trace equivalent, or for branching-time versions stuttering equivalent, to the full one.
- [Equivalence checking](/equivalence-checking/): the decision problem and its algorithms.

## References
