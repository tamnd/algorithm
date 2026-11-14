---
title: BDD-based switching activity is exact under the zero-delay and the transport delay models
proves: [correctness]
status: full
---

**Setting.** The pairs $(X_1, X_1'), \ldots, (X_n, X_n')$ are independent, and $P(X_i = v, X_i' = v') = J_i(v, v')$. All BDDs are reduced and ordered by $x_1 < x_1' < x_2 < x_2' < \cdots < x_n < x_n'$. For a BDD node $u$ write $f_u$ for its function of $(x, x')$. If $u$ is not a terminal and tests a variable of input $i$, then $f_u$ depends only on the variables of inputs $i, i + 1, \ldots, n$, because every path below $u$ tests only later variables.

**Lemma 1 (PAIR-PROB).** For every node $u$, PAIR-PROB$(u, J)$ returns $P(f_u(X, X') = 1)$.

*Proof.* By induction on the BDD in the order of the variables from the bottom. For a terminal, line L8 returns the constant value of $f_u$.

Suppose $u$ tests $x_i$. Shannon expansion on $x_i$ and then on $x_i'$ gives

$$ f_u \;=\; \sum_{v, v' \in \{0,1\}} [x_i = v]\,[x_i' = v']\; f_u|_{x_i = v,\, x_i' = v'}, $$

where the four terms are disjoint. The cofactor $f_u|_{x_i = v}$ is the function of the $v$ child $c$ of $u$. If $c$ tests $x_i'$, then $f_c|_{x_i' = v'}$ is the function of its $v'$ child. If $c$ does not test $x_i'$, then $c$ is a terminal or tests a later variable, so $f_c$ does not depend on $x_i'$ and $f_c|_{x_i' = v'} = f_c$. So the node $w_{v v'}$ that line L9 uses has $f_{w_{v v'}} = f_u|_{x_i = v, x_i' = v'}$, and it is a terminal or tests a variable of an input $j > i$. Hence $f_{w_{v v'}}(X, X')$ is a function of the pairs $(X_j, X_j')$ with $j > i$ and is independent of $(X_i, X_i')$. Taking probabilities,

$$ P(f_u = 1) \;=\; \sum_{v, v'} P(X_i = v, X_i' = v')\; P(f_{w_{v v'}} = 1) \;=\; \sum_{v, v'} J_i(v, v')\, \text{PAIR-PROB}(w_{v v'}, J) $$

by the induction hypothesis, which is line L9.

Suppose $u$ tests $x_i'$. Then $f_u$ does not depend on $x_i$, Shannon expansion on $x_i'$ gives $f_u = \sum_{v'} [x_i' = v'] f_{c_{v'}}$ for the children $c_{v'}$, each child depends only on the inputs $j > i$, and $P(X_i' = v') = J_i(0, v') + J_i(1, v')$. This is line L10.

The memo returns, for a node already seen, the value computed the first time, which by the above is the same. $\square$

**Theorem 1 (zero delay).** Under the zero-delay model, BDD-SWITCHING-ACTIVITY returns, for every node $y$, the expected number of transitions of $y$ in the cycle.

*Proof.* By induction in topological order, $F[y]$ and $F'[y]$ are the BDDs of $f_y(x)$ and $f_y(x')$: for a primary input this is line L2, and for a gate, APPLY computes the BDD of the gate function of its arguments, which by the induction hypothesis are the fanin functions. Under zero delay each node takes the value $f_y(x)$ before the change and $f_y(x')$ after it, with no intermediate values, so it makes one transition if $f_y(x) \ne f_y(x')$ and none otherwise. The expected number of transitions is $P(f_y(X) \oplus f_y(X') = 1)$, which Lemma 1 computes from the BDD $A$ of line L5. $\square$

**Theorem 2 (transport delay).** Let every gate $y$ have an integer delay $d_y \ge 1$, let the inputs change from $x$ to $x'$ at time 0, and let the value of $y$ at time $t \ge 0$ be its gate function applied to the values of its fanins at time $t - d_y$, every node having its value under $x$ before time 0. If $F_t[y]$ is the BDD of the value of $y$ at time $t$ as a function of $(x, x')$, built by the same recurrence with APPLY, then the expected number of transitions of $y$ is $\sum_{t = 0}^{T} \text{PAIR-PROB}(F_t[y] \oplus F_{t-1}[y], J)$, where $T$ is the latest arrival time.

*Proof.* By induction on $t$ and the topological order, $F_t[y]$ is the BDD of the value of $y$ at time $t$, since every value is a Boolean function of $(x, x')$ given by the recurrence. After time $T$ no node changes. The number of transitions of $y$ is $\sum_{t=0}^{T} [y(t) \ne y(t - 1)]$. Its expectation is the sum of the probabilities $P(F_t[y] \oplus F_{t-1}[y] = 1)$ by linearity of expectation, and Lemma 1 gives each of them. $\square$

**Remarks.** Neither theorem needs the absence of reconvergent fanout or the independence of $X_i$ and $X_i'$; only the independence of different pairs is used, in Lemma 1. Theorem 2 is exact for the transport delay model with integer delays; it is not a statement about inertial delays or real circuits.
