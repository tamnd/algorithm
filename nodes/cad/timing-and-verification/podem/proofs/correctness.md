---
title: PODEM returns a test exactly when the fault is detectable
proves: [correctness]
status: full
---

Let $C$ be a combinational circuit with $n$ primary inputs and lines in topological order, and let $(\ell, s)$ be the fault "line $\ell$ stuck at $s$". An assignment $A$ gives each primary input a value in $\{0, 1, X\}$. Line L3 computes, for each line $k$, a good value $g_A(k)$ and a faulty value $b_A(k)$ by three-valued simulation. In the faulty circuit, line $\ell$ has the value $s$ whatever its inputs are. A line has an *effect* under $A$ when $g_A(k)$ and $b_A(k)$ are both in $\{0, 1\}$ and differ, that is, when it carries D or D'. A line *has an X* when $g_A(k) = X$ or $b_A(k) = X$. A *completion* of $A$ is an assignment with values in $\{0, 1\}$ only that agrees with $A$ wherever $A$ is not X. A two-valued vector $\tau$ detects the fault when some primary output has $g_\tau(o) \ne b_\tau(o)$.

**Fact (three-valued simulation).** The three-valued rules for AND, OR, NAND, NOR, NOT, BUF, XOR and XNOR give X exactly when the output is not fixed by the inputs that are not X. So if $A'$ is a completion of $A$ and $g_A(k) \ne X$, then $g_{A'}(k) = g_A(k)$, and the same holds for $b$. On two-valued inputs the rules give the true values.

*Proof.* Induction over the lines in topological order, with the gate rules checked one by one. $\square$

**Lemma 1 (paths of differences).** Let $\tau$ be a two-valued vector that detects the fault at output $o$. Then there are lines $\ell = p_0, p_1, \ldots, p_r = o$, each $p_{i+1}$ a fanout of $p_i$, with $g_\tau(p_i) \ne b_\tau(p_i)$ for every $i$.

*Proof.* A primary input other than $\ell$ has the same value in both circuits. A line $k \ne \ell$ that is not a primary input has the same gate in both circuits, so if all its inputs agree, then $k$ agrees. So every line $k \ne \ell$ with $g_\tau(k) \ne b_\tau(k)$ has an input with the same property. Start at $o$ and step to such an input until the walk reaches $\ell$. The walk stops, because the lines are in topological order, and it can stop only at $\ell$. Reverse it. $\square$

**Lemma 2 (soundness of line L4).** If line L4 returns $A$, then every completion of $A$ detects the fault.

*Proof.* Some output $o$ has an effect under $A$. By the Fact, every completion $A'$ has $g_{A'}(o) = g_A(o) \ne b_A(o) = b_{A'}(o)$. $\square$

**Lemma 3 (safe pruning at line L5).** If the test of line L5 fails for $A$, then no completion of $A$ detects the fault.

*Proof.* The test fails in two cases.

Case 1: $g_A(\ell) = s$. By the Fact, every completion $\tau$ has $g_\tau(\ell) = s = b_\tau(\ell)$. Then the two circuits have the same value on every line, by induction in topological order, and $\tau$ detects nothing.

Case 2: $g_A(\ell) = \lnot s$, and no gate of the D-frontier has an X-path, that is, a path of lines that all have an X, from the gate to a primary output. Suppose that a completion $\tau$ detects the fault at $o$, and take the path $p_0, \ldots, p_r$ of Lemma 1. Line $p_0 = \ell$ has an effect under $A$. Line $o$ has none, since line L4 did not return. Let $j$ be the largest index such that $p_j$ has an effect under $A$, so $j < r$. For $i > j$, line $p_i$ differs under $\tau$, so by the Fact it cannot have two equal known values under $A$, and it has no effect. So $p_i$ has an X. Line $p_{j+1}$ is not a fanout branch: a branch copies its stem in both circuits, and $p_{j+1} \ne \ell$, so it would have the effect of $p_j$. So $p_{j+1}$ is a gate with an X and an input with an effect, which is a gate of the D-frontier, and $p_{j+1}, \ldots, p_r$ is an X-path from it to an output. This contradicts the case. $\square$

**Lemma 4 (the objective and the backtrace are defined).** When the test of line L5 holds and line L4 did not return, line L6 returns a line with an X, and line L7 returns a primary input whose value in $A$ is X.

*Proof.* If $g_A(\ell) = X$, line L13 returns $\ell$, which has an X. Otherwise, case 2 of Lemma 3 does not hold, so some D-frontier gate $G$ has an X-path. A gate with an X has an input with an X, because a gate whose inputs are all known in a circuit is known in that circuit, except for the faulty value of $\ell$, which is always $s$. So line L15 finds an input $j$ with an X. The same argument shows that the loop of lines L17 to L20 always finds an input with an X at line L18, and that it moves to an earlier line each time, so it stops at a primary input $p$ that has an X. Since $b_A(p) = s$ when $p = \ell$, the X of $p$ is its good value, and the good value of a primary input is its value in $A$. $\square$

**Lemma 5 (the search tree).** The stack holds entries for distinct primary inputs, and the values of $A$ are X exactly at the inputs without an entry. Each pass of the loop of line L2 visits a different node of a binary tree of depth at most $n$, so the loop runs at most $2^{n+1} - 1$ times.

*Proof.* Line L8 assigns an input with value X, by Lemma 4, and pushes it. Lines L10 and L12 pop entries and reset their inputs to X, or flip the top entry. So the stack is a path from the root of a tree whose nodes are the stacks, and each entry adds one input, which bounds the depth by $n$. The choice at lines L6 and L7 depends only on $A$, which the stack fixes, so each node has at most the two children "first value" and "flipped value". Line L12 moves from the first child of a node to the second, and line L10 leaves a node only after both of its children are done. This is a depth-first walk in which each node is entered once. A binary tree of depth $n$ has at most $2^{n+1} - 1$ nodes. $\square$

**Theorem.** PODEM stops. It returns an assignment exactly when the fault is detectable, and then every completion of the assignment detects the fault. It returns "untestable" exactly when the fault is redundant.

*Proof.* It stops by Lemma 5. A returned assignment is a test by Lemma 2, and then the fault is detectable. Now suppose that a two-valued vector $\tau$ detects the fault, and follow the nodes of the tree whose assignments agree with $\tau$, starting at the root, where every input is X. At such a node, either line L4 returns, or the test of line L5 holds by Lemma 3, since $\tau$ is a completion. In the second case lines L6 to L8 assign one more input, and one of the two children agrees with $\tau$. The search enters both children before it leaves the node, so it reaches that child unless it returns first. The depth is at most $n$, and at depth $n$ the assignment is $\tau$, where line L4 returns. So PODEM returns an assignment before the stack can become empty at line L11. $\square$
