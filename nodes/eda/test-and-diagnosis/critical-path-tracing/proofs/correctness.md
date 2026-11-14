---
title: Critical path tracing is exact in fanout-free regions and needs a check at stems
proves: [correctness]
status: full
---

Let $C$ be a combinational circuit with lines $0, \ldots, L - 1$ in topological order, so every input of a line has a smaller index. A primary output line has no fanout in the line model, since a net with an output and another sink gets a branch line for each. Fix a two-valued vector $t$ with good values $g(k)$. For a set $U$ of lines, the $U$-flipped circuit is the good circuit with the value of each line of $U$ replaced by its complement. A line $k$ is **critical** if the $\{k\}$-flipped circuit differs from the good circuit at some primary output.

**Lemma 1 (critical lines give the detected faults).** The vector $t$ detects the fault $k$ stuck at $v$ if and only if $v = \lnot g(k)$ and $k$ is critical.

*Proof.* The faulty circuit is the good circuit with $k$ forced to $v$. If $v = g(k)$, it computes the good values on every line. If $v = \lnot g(k)$, it is the $\{k\}$-flipped circuit. $\square$

For a gate line $k$ with input $j$, the input $j$ is **sensitive** if changing the value of $j$ alone, with the other inputs at their good values, changes the gate output.

**Lemma 2 (sensitive inputs).** For AND, NAND, OR and NOR with controlling value $c$, all inputs are sensitive if none is at $c$, only the input at $c$ is sensitive if exactly one is, and no input is sensitive if two or more are. For a buffer, an inverter, a fanout branch, XOR and XNOR, all inputs are sensitive.

*Proof.* An AND-type gate has one output value when some input is at $c$ and the other when none is. With no input at $c$, flipping one input puts it at $c$ and changes the output. With exactly one input at $c$, flipping it leaves no input at $c$, while flipping another input leaves the first one at $c$. With two or more at $c$, flipping one input leaves another at $c$. A one-input gate is one to one, and XOR and XNOR change the output whenever one input changes. $\square$

Call a line with exactly one fanout a **tree line**, and a line with no fanout or with two or more fanouts a **root**. From a tree line $\ell$, following the single fanout repeatedly gives a chain $\ell = k_0, k_1, \ldots, k_m = r$ where $k_0, \ldots, k_{m-1}$ are tree lines and $r$ is a root, with $m \ge 1$. The chain is unique, and the lines whose chain ends at $r$, with $r$ itself, form the fanout-free region of $r$.

**Lemma 3 (the cone of a tree line).** Let $\mathrm{cone}(x)$ be the set of lines reachable from $x$, $x$ included. Then $\mathrm{cone}(\ell) = \{k_0, \ldots, k_{m-1}\} \cup \mathrm{cone}(r)$, and no $k_i$ with $i < m$ lies in $\mathrm{cone}(r)$.

*Proof.* A path from $\ell$ must leave each $k_i$ with $i < m$ through its only fanout $k_{i+1}$, so it follows the chain until it reaches $r$, or it ends earlier. A line $k_i$ with $i < m$ precedes $r$ in topological order, so it is not reachable from $r$. $\square$

**Theorem 1 (exact in fanout-free regions).** A tree line $\ell$ with chain $k_0, \ldots, k_m = r$ is critical if and only if $k_i$ is a sensitive input of $k_{i+1}$ for every $i < m$ and $r$ is critical.

*Proof.* In the $\{\ell\}$-flipped circuit, only the lines of $\mathrm{cone}(\ell)$ can differ from the good values, by induction in topological order. For $i < m$, let $j$ be an input of $k_{i+1}$ other than $k_i$, a side input. Then $j$ precedes $k_{i+1}$, and $k_{i+1}$ is $r$ or precedes it, so $j$ precedes $r$ and is not in $\mathrm{cone}(r)$. Also $j$ is not a chain line $k_{i'}$ with $i' \ne i$, since the only fanout of $k_{i'}$ is $k_{i'+1} \ne k_{i+1}$. By Lemma 3, $j \notin \mathrm{cone}(\ell)$, so every side input keeps its good value.

Assume that every step is sensitive. By induction over $i$, $k_i$ flips: $k_0 = \ell$ flips, and if $k_i$ flips while the side inputs of $k_{i+1}$ keep their good values, then $k_{i+1}$ flips because $k_i$ is sensitive. So $r$ flips. A line of $\mathrm{cone}(r)$ has each input in $\mathrm{cone}(r)$ or outside $\mathrm{cone}(\ell)$, by Lemma 3, and the second kind keeps its good value. So, by induction in topological order, the values in $\mathrm{cone}(r)$, and at the outputs, are those of the $\{r\}$-flipped circuit, and $\ell$ is critical exactly when $r$ is.

Assume that some step is not sensitive, and let $i$ be the first such step. Then $k_0, \ldots, k_i$ flip, and $k_{i+1}$ keeps its good value, since its side inputs keep theirs and $k_i$ is not sensitive. The only fanout of $k_{i'}$ with $i' < i$ is the chain line $k_{i'+1}$, and the only fanout of $k_i$ is $k_{i+1}$. So no line outside $\{k_0, \ldots, k_i\}$ has a flipped input, and by induction in topological order no such line changes. A primary output has no fanout, so it is not one of the tree lines $k_0, \ldots, k_i$, and no output changes. $\square$

**Corollary (the trace).** Lines L6 to L9 mark, for a critical root $r$, exactly the lines of the region of $r$ whose chain is sensitive at every step, and they mark nothing for a root that is not critical. With line L4, which marks every primary output, and line L5, which decides each stem by its definition, every line is marked exactly when it is critical. A root with no fanout that is not a primary output has an empty effect on the outputs and is not critical. With Lemma 1, line L10 reports exactly the detected alive faults, and line L11 drops them as serial simulation does. $\square$

**Theorem 2 (stems need a check).** There is no rule that decides whether a stem is critical from whether its branches are critical.

*Proof.* We give three cases. The first shows that "some branch is critical" is not necessary, and the other two show that no function of the branch pattern works.

First, at the vector $abc = 111$, $g = \mathrm{NAND}(a, b_g)$, $h = \mathrm{NAND}(b_h, c)$, $z = \mathrm{NAND}(g, h)$, where $b_g$ and $b_h$ are the branches of the stem $b$. The good values are $g = h = 0$ and $z = 1$. Flipping $b_g$ alone gives $g = 1$ with $h = 0$, so $z = 1$: $b_g$ is not critical, and in the same way $b_h$ is not critical. Flipping $b$ flips both branches, so $g = h = 1$ and $z = 0$: the stem is critical.

Second, the multiplexer $p = \mathrm{AND}(a_p, b)$, $n = \mathrm{NOT}(a_n)$, $q = \mathrm{AND}(n, c)$, $z = \mathrm{OR}(p, q)$, where $a_p$ and $a_n$ are the branches of the stem $a$, at the vector $abc = 111$. The good values are $p = 1$, $n = 0$, $q = 0$ and $z = 1$. Flipping $a_p$ alone gives $p = 0$ with $q = 0$, so $z = 0$: the branch $a_p$ is critical. Flipping $a_n$ alone gives $n = 1$ and $q = 1$ with $p = 1$, so $z = 1$: the branch $a_n$ is not critical. Flipping $a$ gives $p = 0$, $n = 1$ and $q = 1$, so $z = 1$: the stem is not critical.

Third, the same multiplexer at the vector $abc = 110$. The good values are $p = 1$, $n = 0$, $q = 0$ and $z = 1$. Flipping $a_p$ alone gives $z = 0$, so $a_p$ is critical. Flipping $a_n$ alone gives $n = 1$ but $q = 0$ since $c = 0$, so $a_n$ is not critical. Flipping $a$ gives $p = 0$ and $q = 0$, so $z = 0$: the stem is critical.

The second and third cases have the same branch pattern, $a_p$ critical and $a_n$ not, and opposite answers for the stem. So the criticality of a stem is not a function of the criticality of its branches. $\square$

**Theorem 3 (stems with no reconvergence).** If the cones of the branches of a stem are pairwise disjoint, the stem is critical if and only if some branch is critical.

*Proof.* Flipping the stem flips all its branches. Since the cones are disjoint, each line of the cone of a branch $b$ has all its inputs either in that cone or outside the cone of the stem, so its value in the stem-flipped circuit equals its value in the $\{b\}$-flipped circuit, by induction in topological order. Each output lies in at most one branch cone, so an output changes when the stem flips exactly when it changes when that branch flips. $\square$
