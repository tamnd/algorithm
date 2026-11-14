---
title: Cutpoint equivalence checking answers exactly, and its cut differences are false negatives only until the cut moves back
proves: [correctness]
status: full
---

**Setting.** The two circuits are combined into one product netlist with primary inputs $x_1, \ldots, x_n$ and the gates of both circuits in topological order. The BDD variable of $x_i$ has index $i - 1$. Every node $u$ computes a function $[\![u]\!] : \{0, 1\}^n \to \{0, 1\}$. Line L8 creates cut variables with indices $n, n + 1, \ldots$ in the order of creation and gives each cut variable $v$ a BDD $\mathrm{def}(v)$.

**Lemma 1 (definitions point down).** For every cut variable $v$, every variable in the support of $\mathrm{def}(v)$ is smaller than $v$.

*Proof.* Line L8 sets $\mathrm{def}(v) = R(r)$ for the next free index $v$. $R(r)$ was built at line L4 from BDDs that existed before, and every variable that existed before has a smaller index than the new one. $\square$

**Meaning of a BDD.** By Lemma 1 we can define, by induction on the variable index, the value of each variable at an input vector $a \in \{0, 1\}^n$: the variable of $x_i$ has the value $a_i$, and a cut variable $v$ has the value $\mu(\mathrm{def}(v))(a)$. For a BDD $G$, $\mu(G)(a)$ is the value of $G$ when every variable in it has this value. So $\mu$ is evaluation at one point per input vector, and therefore $\mu(G \circ H) = \mu(G) \circ \mu(H)$ for every gate operator $\circ$, and $\mu(G[v := \mathrm{def}(v)]) = \mu(G)$, because the substituted function has the same value at the point as $v$ itself.

**Lemma 2 (RESOLVE).** RESOLVE($G$) terminates. Its result $G'$ satisfies $\mu(G') = \mu(G)$, and if $G' \ne 0$, then the support of $G'$ has primary input variables only. Hence RESOLVE($G$) $= 0$ if and only if $\mu(G) = 0$.

*Proof.* Each pass of lines L14 to L16 replaces the largest cut variable $v$ in the support by $\mathrm{def}(v)$. The other cut variables in the support are smaller than $v$, and so is every variable of $\mathrm{def}(v)$ by Lemma 1. So the largest cut variable in the support decreases strictly at each pass, and the loop stops after at most $C$ passes for $C$ cut variables. Each pass keeps $\mu$, as shown above. The loop stops only when $G' = 0$ or the support has no cut variable. In the second case $G'$ is a BDD over the primary inputs, so $\mu(G') = G'$. Then $\mu(G) = G' \ne 0$. In the first case $\mu(G) = \mu(0) = 0$. $\square$

**Lemma 3 (invariant).** After line L3 has processed a node $u$, and until the end of the run, $\mu(R(u)) = [\![u]\!]$ and $\mu(F(u)) = [\![u]\!]$.

*Proof.* Induction over the nodes in topological order. For a primary input, $F$ and $R$ are its variable, and $\mu$ gives $a_i$. For a gate $u$, line L4 applies the gate to $F$ of the fanins, which were processed before, so $\mu(R(u)) = [\![u]\!]$ by the induction hypothesis and the first property of $\mu$. Line L5 copies it to $F(u)$. Line L9 sets $F(u) = v_r$ only when RESOLVE($R(u) \oplus R(r)$) $= 0$, so $\mu(R(u)) = \mu(R(r))$ by Lemma 2. When $v_r$ is made at line L8, $\mathrm{def}(v_r) = R(r)$, so $\mu(v_r) = \mu(R(r)) = [\![r]\!] = [\![u]\!]$. Line L8 also changes $F(r)$ to $v_r$, and $\mu(v_r) = [\![r]\!]$, so the claim for $r$ stays true. Nothing else changes $R$ or $F$. $\square$

**Theorem (correctness).** The algorithm returns "equivalent" if and only if $[\![o]\!] = [\![o']\!]$ for every output pair $(o, o')$. When it returns "different", the input vector it returns gives different values on some pair.

*Proof.* At line L11, $\mu(F(o) \oplus F(o')) = [\![o]\!] \oplus [\![o']\!]$ by Lemma 3. By Lemma 2, the result $G$ of RESOLVE is 0 exactly when this function is 0, that is, when the outputs agree on every input vector. If every pair gives 0, line L13 returns "equivalent". If some pair gives $G \ne 0$, then $G$ is a BDD over the primary inputs and $G = [\![o]\!] \oplus [\![o']\!]$. A satisfying path of $G$ fixes some inputs; every completion of it satisfies $G$, so the vector of line L12 (with 0 for the free inputs) separates $o$ and $o'$. $\blacksquare$

**Remark (false negatives).** The cut miter $G$ at line L11 or L7, read as a function of free variables, may be satisfiable while $\mu(G) = 0$. A satisfying point of $G$ that gives a cut variable $v$ a value that $\mathrm{def}(v)$ cannot take at the same inputs is not a point of any real input vector. This is the false negative. Lemma 2 shows that moving the cut back, one cut variable at a time, removes every such point and never removes a real one.

**Remark (simulation).** The signatures of line L2 only choose which pairs to compare. A wrong guess costs one RESOLVE and changes nothing in Lemmas 1 to 3, so the answer does not depend on the random vectors.
