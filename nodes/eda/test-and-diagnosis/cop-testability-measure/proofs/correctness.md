---
title: COP is exact on fanout-free circuits and can be wrong under reconvergence
proves: [correctness]
status: full
---

Let $C$ be a combinational circuit whose primary inputs are independent, with $\Pr[x_i = 1] = p_i$. Lines are the stems and fanout branches of the [PODEM](/podem/) page. For a line $k$ with good value $v_k$, let $E_k$ be the event that forcing $k$ to $\lnot v_k$ changes some primary output. So $\Pr[E_k]$ is the probability that the [Boolean difference](/transition-density/) of the outputs with respect to $k$ is 1, and a vector detects $k$ stuck at $s$ exactly when $v_k = \lnot s$ and $E_k$ holds. The page computes $C[k]$ at lines L1 to L7, $O[k]$ at lines L8 to L12 and the detection estimate at line L13.

The circuit is **fanout-free** when every net feeds at most one sink (a gate input or a primary output). Then there are no fanout branches, every line other than a primary output has exactly one fanout or none, and following the fanouts from a line $k$ leads to one primary output $\mathrm{root}(k)$. Let $T(k)$ be the set of primary inputs from which $k$ is reached.

**Lemma 1 (the trees).** In a fanout-free circuit, the sets $T(j)$ of the inputs $j$ of one gate are pairwise disjoint. Every path from an input of $T(k)$ to $\mathrm{root}(k)$ passes through $k$.

*Proof.* If an input $x$ were in $T(j_1)$ and in $T(j_2)$, there would be two paths from $x$ to the gate, and the first line where they split would have two fanouts. For the second claim, a path from $x \in T(k)$ follows single fanouts, so it is the unique path out of $x$, and it passes $k$ because $k$ is reached from $x$. $\square$

**Lemma 2 (controllability).** In a fanout-free circuit, $C[k] = \Pr[v_k = 1]$ for every line $k$.

*Proof.* Induction in topological order. A primary input gets $p_k$ at line L2. A gate $k$ with inputs $j_1, \ldots, j_m$ has a value that is a function of the values of the $j_i$, and the value of $j_i$ is a function of the inputs in $T(j_i)$. These sets are disjoint by Lemma 1, so the input values are independent. For independent events, $\Pr[\text{all } j_i = 1] = \prod C[j_i]$ (line L4), $\Pr[\text{some } j_i = 1] = 1 - \prod (1 - C[j_i])$ (line L5), and the parity of $j_1, \ldots, j_i$ is 1 with probability $c (1 - C[j_i]) + (1 - c) C[j_i]$ if the parity of the first $i - 1$ is 1 with probability $c$ (line L6). Line L7 takes the complement for an inverting gate. This is the exactness argument of [signal probability propagation](/signal-probability-propagation/). $\square$

**Lemma 3 (observability).** In a fanout-free circuit, $O[k] = \Pr[E_k]$ for every line $k$.

*Proof.* Induction in reverse topological order. If $k$ is a primary output, $E_k$ always holds, and line L9 gives 1. If $k$ has no fanout and is not an output, $E_k$ never holds and $O[k] = 0$. Otherwise $k$ has one fanout gate $g$ (line L11), and $\mathrm{root}(k) = \mathrm{root}(g)$. No other output is reached from $k$. By Lemma 1, the output $\mathrm{root}(g)$ is a function $F(v_g, Y)$ of the value of $g$ and of the inputs $Y$ outside $T(g)$, so $E_g$ is the event $F(0, Y) \ne F(1, Y)$ and depends on $Y$ only.

Forcing $k$ to its complement changes $g$ exactly when every other input $j$ of $g$ is non-controlling: for AND and NAND that is $v_j = 1$, for OR and NOR it is $v_j = 0$, and for XOR, XNOR, NOT and BUF a change of one input always changes the output. If $g$ changes, the output changes exactly when $E_g$ holds, because the rest of the circuit sees $k$ only through $g$. If $g$ does not change, nothing else changes. So $E_k$ is the intersection of $E_g$ and of the events "$j$ is non-controlling" for the side inputs $j$ of $g$.

The event for $j$ depends on $T(j)$ only. The sets $T(j)$ are disjoint from each other, they lie inside $T(g)$, and $E_g$ depends on inputs outside $T(g)$. So all these events are independent, and $\Pr[E_k] = \Pr[E_g] \prod_j \Pr[j \text{ non-controlling}]$. By induction $\Pr[E_g] = O[g]$, and by Lemma 2 the factor for $j$ is $C[j]$, $1 - C[j]$ or 1, which is $S_g(j)$ of line L12. $\square$

**Theorem 1.** In a fanout-free circuit, line L13 gives the exact probability that a random vector detects the fault $k$ stuck at $s$.

*Proof.* The vector detects the fault exactly when $v_k = \lnot s$ and $E_k$ holds. The value $v_k$ depends on $T(k)$ only, and by the argument of Lemma 3, $E_k$ depends on the inputs outside $T(k)$ only. So the events are independent, and the probability is $\Pr[v_k = 1] \Pr[E_k] = C[k] O[k]$ for $s = 0$ and $(1 - C[k]) O[k]$ for $s = 1$, by Lemmas 2 and 3. $\square$

**Theorem 2 (reconvergence).** On circuits with reconvergent fanout, COP can be wrong in $C$, in $O$ and in the detection estimate. The error can go either way, and COP can give a positive detection estimate to a [redundant fault](/redundant-fault/).

*Proof.* By examples, with every $p_i = 1/2$.

1. Let $x = ab$, $y = ac$ and $z = xy$. Then $z = abc$ and $\Pr[z = 1] = 1/8$, but line L4 gives $C[z] = C[x] C[y] = 1/16$, because it treats $x$ and $y$ as independent although both read $a$. Forcing $a$ to its complement changes $z$ exactly when $b = c = 1$, so $\Pr[E_a] = 1/4$. Each branch of $a$ gets $O = 1/8$, and line L10 gives $O[a] = 1 - (7/8)^2 = 15/64 < 1/4$. The branch of $a$ into $x$ stuck at 1 makes $z = b \cdot ac = abc$, so the fault is redundant, but line L13 gives $(1 - 1/2) \cdot 1/8 = 1/16$.
2. Let $z = a \oplus a$, with two branches of $a$ into the XOR gate. Then $z = 0$ always and $\Pr[E_a] = 0$. COP gives $C[z] = 1/2$, each branch gets $O = 1$, and line L10 gives $O[a] = 1 > 0$.

So the stem rule of line L10 is neither an upper nor a lower bound. $\square$

**What is not proved here.** Computing the exact signal probability of a general circuit is #P-hard, as the signal probability page shows from Valiant's result. So no polynomial-time rule is exact on all circuits unless P = #P (in the usual sense of counting complexity). How far COP is from the exact values on real circuits, and how well it predicts random-pattern [fault coverage](/fault-coverage/), are measured results, not theorems.
