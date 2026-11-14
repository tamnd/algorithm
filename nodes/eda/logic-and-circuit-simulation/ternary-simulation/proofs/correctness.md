---
title: Ternary evaluation is monotone and sound, and Eichelberger's two phases bound every run under any delays
proves: [correctness]
status: full
---

**Setting.** The values are $0, 1, X$ with the information order $0 \sqsubseteq X$, $1 \sqsubseteq X$, and $v \sqsubseteq v$ for each $v$. Vectors are ordered position by position. A *completion* of a vector $u$ is a binary vector $v$ with $v \sqsubseteq u$. For a Boolean function $f$ of $k$ arguments, its *exact extension* is $\hat f(u) = $ the common value of $f$ on all completions of $u$ if they all agree, and $X$ otherwise. Equivalently, $\hat f(u)$ is the least upper bound of $\{f(v) : v \sqsubseteq u \text{ binary}\}$.

A circuit has primary inputs and $n$ gates, possibly in loops. For inputs $u$ and a state $s$ (the gate outputs), $F(u, s)$ evaluates every gate once with the tables. Lines L1 to L11 refer to the pseudocode of the page.

**Lemma 1 (gate tables).** For AND, OR, NAND, NOR, XOR, XNOR, NOT and BUF with distinct inputs, Kleene's tables are the exact extensions. So each table is monotone, $u \sqsubseteq u' \Rightarrow \hat f(u) \sqsubseteq \hat f(u')$, and agrees with $f$ on binary inputs.

*Proof.* AND: if some input is 0, every completion gives 0, and the table gives 0. If all inputs are 1, the table gives 1. Otherwise there is an X and no 0; setting all X to 1 gives 1 and setting one X to 0 gives 0, so the completions disagree, and the table gives X. OR is dual, and NAND, NOR, XNOR and NOT are these followed by negation, which maps the set of completion values $\{0\}, \{1\}, \{0, 1\}$ to $\{1\}, \{0\}, \{0, 1\}$. XOR: if all inputs are binary, the table gives the parity. If one input is X, flipping it flips the result, so the completions disagree and the table gives X. Monotonicity: if $u \sqsubseteq u'$, every completion of $u$ is a completion of $u'$, so the set of values only grows, and its least upper bound can only go up. The tests check all tables with up to three inputs against all completions. $\square$

**Lemma 2 ($F$ is monotone).** If $u \sqsubseteq u'$ and $s \sqsubseteq s'$, then $F(u, s) \sqsubseteq F(u', s')$.

*Proof.* Each component of $F$ is a gate table applied to some components of $(u, s)$, and these grow from $(u, s)$ to $(u', s')$. Apply Lemma 1. $\square$

**Theorem 1 (soundness of three-valued evaluation).** Let the circuit have no loop, let $u$ be an input vector with values in $\{0, 1, X\}$, and let $e(u)$ be the result of evaluating the gates in topological order with the tables. For every completion $v$ of $u$ and every net $m$, $e(v)_m \sqsubseteq e(u)_m$. So if $e(u)_m$ is 0 or 1, every completion gives the same value.

*Proof.* Induction in topological order. Inputs: $v \sqsubseteq u$. A gate whose inputs satisfy the claim gets $\hat f(\text{inputs under } v) \sqsubseteq \hat f(\text{inputs under } u)$ by Lemma 1, and on the binary inputs under $v$, $\hat f = f$. $\square$

Iterating $F(u, \cdot)$ from the all-X state gives the same result $e(u)$ on a loop-free circuit: the sequence descends by Lemma 2 (since $F(u, \mathbf{X}) \sqsubseteq \mathbf{X}$), and after $k$ steps every net of level at most $k$ has its value $e(u)$. This is the function `evaluate` of the implementation.

**Theorem 2 (exactness without fanout).** If every input and every gate output feeds at most one gate input, then for every net $m$, $e(u)_m$ is the least upper bound of $e(v)_m$ over the completions $v$ of $u$.

*Proof.* Induction in topological order. The subcircuits feeding the different inputs of a gate $g$ use disjoint sets of primary inputs, since there is no fanout. So as $v$ ranges over the completions of $u$, the vector of values at the inputs of $g$ ranges over the product $S_1 \times \cdots \times S_k$, where $S_i$ is the set of values of input $i$. By induction, the value of input $i$ under $u$ is the least upper bound of $S_i$, whose completions are exactly the elements of $S_i$. By Lemma 1 the table of $g$ gives the least upper bound of $f$ over $S_1 \times \cdots \times S_k$, which is the least upper bound of the values of $\mathrm{out}(g)$ over the completions. $\square$

**X pessimism.** With fanout, Theorem 2 fails. In $y = \mathrm{OR}(\mathrm{AND}(s, a), \mathrm{AND}(\mathrm{NOT}(s), b))$ with $a = b = 1$ and $s = X$: the two AND gates give X and X, so $y = \mathrm{OR}(X, X) = X$. Both completions give $y = 1$. The tables see two X values but not that one is the complement of the other. The simplest case is $x \lor \lnot x$ with $x = X$, which gives X instead of 1.

**Theorem 3 (phase A).** Let $F(a, s_0) = s_0$ and $\hat a = \mathrm{lub}(a, b)$ (L1). The sequence $s^0 = s_0$, $s^{h+1} = F(\hat a, s^h)$ of L2 to L6 is increasing. It stops after at most $n$ steps that change the state, and its last element $s_A$ is the least fixed point of $F(\hat a, \cdot)$ above $s_0$.

*Proof.* $a \sqsubseteq \hat a$, so $s^1 = F(\hat a, s_0) \sqsupseteq F(a, s_0) = s_0$ by Lemma 2. If $s^{h+1} \sqsupseteq s^h$, then $s^{h+2} = F(\hat a, s^{h+1}) \sqsupseteq F(\hat a, s^h) = s^{h+1}$. In an increasing chain, a step that changes the state turns at least one binary component into X, and there are $n$ components, so at most $n$ steps change it. The last element satisfies $F(\hat a, s_A) = s_A$ and $s_A \sqsupseteq s_0$. If $r$ is any fixed point of $F(\hat a, \cdot)$ with $r \sqsupseteq s_0$, then $s^h \sqsubseteq r$ for all $h$, by induction: $s^{h+1} = F(\hat a, s^h) \sqsubseteq F(\hat a, r) = r$. $\square$

**Theorem 4 (phase B).** The sequence $t^0 = s_A$, $t^{h+1} = F(b, t^h)$ of L7 to L10 is decreasing, stops after at most $n$ changing steps, and its last element $t_B$ is the greatest fixed point of $F(b, \cdot)$ below $s_A$.

*Proof.* $b \sqsubseteq \hat a$, so $t^1 = F(b, s_A) \sqsubseteq F(\hat a, s_A) = s_A$. Induction with Lemma 2 shows that the sequence decreases. Each changing step turns at least one X into a binary value, and a binary value never changes in a decreasing chain, so at most $n$ steps change it. If $r = F(b, r)$ and $r \sqsubseteq s_A$, then $r \sqsubseteq t^h$ for all $h$ by the same induction. $\square$

**Delay model.** Consider a run in continuous or discrete time, with binary values. Before time 0 the inputs are $a$ and the gates are in $s_0$. From time 0 each primary input has its new value; a gate may see the change of an input or of another gate later, after any wire delay, and its output may change after any gate delay. We need only one property: each value that a gate output takes is its value in $s_0$ or the gate function applied to a vector of values that its inputs, as seen through their wires, held at earlier times; and each input, as seen by a gate, has a value from $a$ or $b$. Transport delays, inertial delays, gate and wire delays of any size, and the multiple-winner race model all have this property. We also assume that each bounded interval of time holds finitely many changes.

**Theorem 5 (every value is below $s_A$).** In every such run, at every time, the value of every gate output $m$ satisfies $\mathrm{value}(m) \sqsubseteq (s_A)_m$. In particular, a net with $(s_A)_m \in \{0, 1\}$ keeps its value $(s_0)_m$ for ever, so it has no glitch.

*Proof.* The input values seen by gates are in $\{a_i, b_i\}$, and both are $\sqsubseteq \hat a_i$. The change times are well ordered, so we can use induction over them. The values before the first change are those of $s_0 \sqsubseteq s_A$. When gate $g$ takes a new value, it is $f_g(w)$ for a vector $w$ of earlier values of its inputs. By induction each component of $w$ is $\sqsubseteq$ the matching component of $(\hat a, s_A)$. By Lemma 1, $f_g(w) = \hat f_g(w) \sqsubseteq \hat f_g$ at $(\hat a, s_A)$, which is $F(\hat a, s_A)_g = (s_A)_g$. If $(s_A)_m$ is binary, every value of $m$ equals it, and $(s_0)_m \sqsubseteq (s_A)_m$ gives $(s_A)_m = (s_0)_m$. $\square$

**Theorem 6 (stable end states are below $t_B$).** If such a run reaches a state $r$ that is stable under $b$, that is, $F(b, r) = r$, then $r \sqsubseteq t_B$.

*Proof.* By Theorem 5, $r \sqsubseteq s_A$, so by Theorem 4, $r$ is below the greatest fixed point of $F(b, \cdot)$ under $s_A$, which is $t_B$. $\square$

So if $(t_B)_m$ is binary, every run that settles ends with that value on $m$, and if $t_B$ is binary everywhere, every run that settles ends in the same state. Theorems 5 and 6 are the soundness of Eichelberger's procedure. The converse, that every X of $s_A$ is a real change in some run with gate and wire delays, and that $t_B$ is exactly the least upper bound of the possible final behaviors, is the theorem of Brzozowski and Seger (1987), cited on the page and not proved here.
