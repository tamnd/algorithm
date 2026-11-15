---
title: BURS states hold the relative least costs, and the reduction gives a least-cost tiling
proves: [correctness]
status: full
---

We use the grammar and the pseudocode of the page. The grammar has nonterminals, *base rules* $X \to \mathrm{op}(Y_1, \ldots, Y_k)$ and *chain rules* $X \to Y$, each with a cost $c \ge 0$. A *derivation* of a tree $T_v$ from $X$ is a base rule $X \to \mathrm{op}(Y_1, \ldots, Y_k)$ with $\mathrm{op} = \mathrm{op}(v)$ and a derivation of the $i$-th child of $v$ from $Y_i$ for each $i$, or a chain rule $X \to Y$ and a derivation of $T_v$ from $Y$. Its cost is the sum of the costs of its rules. Let $L_X(v)$ be the least cost of a derivation of $T_v$ from $X$, or $\infty$ if there is none.

## The grammar and the tilings

The normalizer gives each pattern of size more than 1 a fresh helper nonterminal for each inner node, with a base rule of cost 0. A pattern that is a single leaf becomes a chain rule from the nonterminal of that leaf to *reg*.

**Lemma 1.** The least cost of a tiling of $T$ is $L_{\mathrm{reg}}(\mathrm{root})$, and each derivation from *reg* gives a tiling of the same cost.

*Proof.* A helper nonterminal appears in the right side of exactly one rule, and it has exactly one rule. So a derivation that uses a helper at a node must use the whole chain of helpers of one pattern, which is one match of that pattern, and its cost is the cost of the pattern. A derivation from *reg* is therefore a choice of a pattern at the node, and derivations from *reg* of the holes, or from *con* or *var* of the constant and variable leaves, which cost 0. This is exactly a tiling, with the same cost. $\square$

## The states

A *state* is a finite set of entries $(X, \delta_X, \rho_X)$: a nonterminal, a number and a rule. For a node $v$ let $m(v) = \min_X L_X(v)$.

**Lemma 2 (invariant).** Let $s$ be the state that LABEL gives to $v$. Then $X$ has an entry in $s$ exactly when $L_X(v) < \infty$, and then $\delta_X = L_X(v) - m(v)$, and the rule $\rho_X$ starts a derivation of $T_v$ from $X$ of cost $L_X(v)$ whose other parts are least-cost derivations.

*Proof.* By induction on the height of $v$. Let $v$ have operator op and children $u_1, \ldots, u_k$ with states $s_1, \ldots, s_k$. By the induction hypothesis, $L_Y(u_i) = \delta^{(i)}_Y + m(u_i)$ for each $Y$ in $s_i$.

*Base rules (lines L2 and L3).* A derivation that starts with a base rule $X \to \mathrm{op}(Y_1, \ldots, Y_k)$ of cost $c$ has least cost
$$c + \sum_i L_{Y_i}(u_i) = \Big(c + \sum_i \delta^{(i)}_{Y_i}\Big) + M, \qquad M = \sum_i m(u_i),$$
because the parts are independent. Line L3 computes the term in brackets. The constant $M$ is the same for every base rule at $v$. So for each $X$, the rule with the least computed value is also the rule with the least true value, and the computed value is the true one minus $M$. Let $b_X$ be the least true cost of a derivation from $X$ that starts with a base rule. After line L3, the entry of $X$ is $b_X - M$, with its rule.

*Chain rules (line L4).* We have $L_X(v) = \min\big(b_X, \min_{X \to Y} (c + L_Y(v))\big)$. This is a shortest path problem: $L_X(v)$ is the least cost of a path from $X$ along chain rules to some $Y$, plus $b_Y$. The costs are not negative, so a least path never repeats a nonterminal. Line L4 relaxes the chain rules until no value falls, which is the Bellman-Ford method. Each value is always the cost of some path, so it never falls below $L_X(v) - M$. After $p$ passes, each value is at most the cost of each path with at most $p$ chain rules, so after one pass for each nonterminal all values are exact, and the next pass changes nothing. So the loop stops, and each value is $L_X(v) - M$. The rules that line L4 keeps form least paths. The whole computation subtracts the same $M$ from every value, so it does not change any choice.

*Normalizing (line L5).* The least value after line L4 is $m(v) - M$. Line L5 subtracts it, so $\delta_X = L_X(v) - m(v)$. $\square$

The values in a state depend only on op and the states of the children, not on $M$. So a state of a node is a function of op and the child states, and BUILD can compute this function once for each operator and each tuple of states. This is the reason why the shift by the minimum is needed: the absolute costs $L_X(v)$ grow with the tree and take infinitely many values, but the relative costs often take only a few.

**Lemma 3 (the tables are complete).** If BUILD stops, then for each tree, each lookup of LABEL finds an entry, and the state it finds is the state of Lemma 2.

*Proof.* By induction on the height of the tree. The state of a leaf is in the table by line L1. For an inner node, the child states are in the set of states by induction. BUILD stops only when every operator and every tuple of known states has an entry (line L6). That entry was computed with lines L2 to L5, so by Lemma 2 it is the right state. $\square$

**Theorem.** If BUILD stops and the root state has *reg*, then REDUCE(root, reg) emits a tiling of least cost.

*Proof.* REDUCE$(v, X)$ uses the rule $\rho_X$ of the state of $v$ (line L9). By Lemma 2 this rule starts a derivation of cost $L_X(v)$, provided that the parts below it are least-cost derivations. REDUCE then calls itself on the same node with the right side of a chain rule (line L10), or on each child with the nonterminal of the base rule (line L12), and by induction each call emits a least-cost derivation. The chain calls on one node follow a least path, so they never loop. So REDUCE emits a derivation of cost $L_{\mathrm{reg}}(\mathrm{root})$, and Lemma 1 turns it into a tiling of the same least cost. $\blacksquare$

**When BUILD stops.** The set of states is finite exactly when the relative costs $\delta_X$ that occur are bounded, because the costs are integers. Then the worklist of line L6 adds only finitely many states and stops. Some grammars give unbounded relative costs. For example, with the rules $x \to a$ and $y \to a$ of cost 0, and $x \to f(x)$ of cost 1 and $y \to f(y)$ of cost 2, the tree $f(f(\cdots f(a)))$ with $k$ copies of $f$ has $L_x = k$ and $L_y = 2k$, so its state has $\delta_y = k$, and the states never repeat. For such a grammar the tables are infinite, and a generator must stop with an error or fall back to the dynamic program at compile time.

**Time.** LABEL does one table lookup for each node, and REDUCE visits each node once for each nonterminal that the derivation uses there, which is a constant for a fixed grammar. So labeling and reducing take $\Theta(n)$ time for a tree with $n$ nodes. The cost of BUILD depends only on the grammar.
