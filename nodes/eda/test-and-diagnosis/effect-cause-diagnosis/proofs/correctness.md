---
title: Effect-cause diagnosis returns exactly the single stuck-at faults that reproduce the observed response
proves: [correctness]
status: full
---

We use the notation of the page. The circuit $C$ is combinational, so its lines can be ordered so that each line is a primary input or is computed from lines earlier in the order. A fan-out branch is a line computed from its stem by the identity. The fan-in cone $\mathrm{cone}(u)$ of a line $u$ is the set of lines with a path to $u$, $u$ included. For a fault $f$ = "$\ell$ stuck at $v$" and a test $t$, write $g(u)$ for the value of line $u$ in the good circuit on $t$ and $h(u)$ for its value in $C$ with $f$ on $t$. In the faulty circuit $h(\ell) = v$, and every other line is computed by its gate from the faulty values of its inputs.

**Lemma 1 (reach).** If $\ell \notin \mathrm{cone}(u)$, then $h(u) = g(u)$.

*Proof.* By induction along the order. Let $\ell \notin \mathrm{cone}(u)$. Then $u \ne \ell$, since $u \in \mathrm{cone}(u)$. If $u$ is a primary input, both circuits give it the value of the test. Otherwise $u$ is computed by the same gate in both circuits from its inputs $u_1, \ldots, u_r$, which come earlier in the order. Each $\mathrm{cone}(u_i)$ is a subset of $\mathrm{cone}(u)$, so $\ell \notin \mathrm{cone}(u_i)$, and by the induction hypothesis $h(u_i) = g(u_i)$. So the gate gives the same value, $h(u) = g(u)$. $\blacksquare$

**Lemma 2 (excitation).** If $g(\ell) = v$, then $h(u) = g(u)$ for every line $u$.

*Proof.* By induction along the order. For $u = \ell$, $h(\ell) = v = g(\ell)$. For a primary input $u \ne \ell$ both values are the test value. For any other $u \ne \ell$, the inputs come earlier, have equal values by the induction hypothesis, and the same gate gives the same value. $\blacksquare$

**Theorem 1.** Let at least one test fail. Then `EFFECT-CAUSE` returns exactly the set $A$ of single stuck-at faults $f$ such that $C$ with $f$ gives $z_j$ on every test $t_j$.

*Proof.* Line L8 adds a fault to KEPT only when it gives $z_j$ on every $t_j$, so KEPT $\subseteq A$. For the other direction, let $f$ = "$\ell$ stuck at $v$" be in $A$.

*It survives lines L3 to L5.* Let $o$ be an output that line L4 visits, so $o$ is wrong on some failing test $t_j$, that is $z_j(o) \ne g_j(o)$. Since $f \in A$, $h_j(o) = z_j(o) \ne g_j(o)$, and by Lemma 1 this forces $\ell \in \mathrm{cone}(o)$. So $\ell$ is in every set intersected in line L5, and $\ell \in S$.

*Line L6 makes it.* Let $j \in$ FAIL. Some output differs between $z_j$ and $g_j$, so $h_j \ne g_j$ on that output, and by Lemma 2 $g_j(\ell) \ne v$, that is $g_j(\ell) = 1 - v$. This holds for every $j \in$ FAIL, so $\ell$ has the single good value $1 - v$ on all failing tests, and line L6 puts the fault "$\ell$ stuck at $1 - (1 - v)$" = $f$ in CAND.

*Line L8 keeps it.* Since $f \in A$, the test of line L8 succeeds, and $f$ is added to KEPT.

So $A \subseteq$ KEPT, and KEPT $= A$. Line L9 returns it. $\blacksquare$

**Corollary 1 (same as a full dictionary).** If $D$ is the set of all single stuck-at faults, then $A$ is the answer of `lookup_full` of the [fault dictionary](/fault-dictionary/) on the same tests and outputs, by Theorem 1 of that page.

**Corollary 2 (the true fault is kept).** If the chip behaves like $C$ with a single stuck-at fault $f$ and some test fails, then $f \in A$, so the answer contains $f$.

**Remark (no failing test).** If no test fails, line L2 returns the empty set. Every fault that no test detects reproduces such a response, so the empty answer means only that there is nothing to diagnose, and Theorem 1 is stated for at least one failing test.

**Count of simulations.** Line L6 makes at most one fault per line of $S$, so line L8 simulates at most $|S| \le L$ faults, at most half of the $2L$ single stuck-at faults. $\blacksquare$
