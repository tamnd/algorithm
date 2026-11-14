---
title: Priority cuts keep the functions, do not lose depth in the area passes, and are exact with unlimited cuts
proves: [correctness]
status: full
---

Let $G$ be a directed acyclic graph whose sources are the primary inputs (PIs), with the gates in topological order and a set of outputs. A cut of $v$ is a set of nodes that meets every path from a PI to $v$, and it is $k$-feasible if it has at most $k$ nodes. Write $\mathrm{arr}(v)$ for the arrival time of $v$ as set at line L10, with $\mathrm{arr} = 0$ for a PI, and $\mathrm{dep}(B) = 1 + \max_{u \in B} \mathrm{arr}(u)$ for a cut $B$. The mapping is the set of gates reached from the outputs through best: an output gate is in it, and if $v$ is in it, every gate of $\mathrm{best}(v)$ is in it.

**Lemma 1 (every kept cut is a k-feasible cut).** At every moment, every set in $P(v)$, and $\mathrm{best}(v)$, is a $k$-feasible cut of $v$ that does not contain $v$.

*Proof.* Induction on the time of the change. When $v$ is visited, line L5 forms sets $c_1 \cup \cdots \cup c_d$ where each $c_i$ is $\{u_i\}$ or a set of $P(u_i)$ for the fanin $u_i$. Each $c_i$ is a cut of $u_i$: $\{u_i\}$ is, and the sets of $P(u_i)$ are by induction. The union is a cut of $v$, since every path from a PI to $v$ ends with an edge $u_i \to v$ and its part before that edge meets $c_i$ (Lemma 3 of the proof of [cut enumeration](/cut-enumeration/)). It has at most $k$ nodes by the test of line L5. It does not contain $v$, because each $c_i$ lies in the cone of $u_i$ and $G$ is acyclic. Line L6 adds the old $\mathrm{best}(v)$, which is such a cut by induction. Line L9 picks from these sets. $\square$

**Theorem 1 (the mapping keeps the functions).** Each LUT of the returned mapping, for gate $v$ over $\mathrm{best}(v)$, can compute $v$ as a function of the leaves, and the LUT network computes every output.

*Proof.* A gate is a function of the values on any of its cuts: if two input vectors give the same values on the cut, every path from a PI to $v$ passes through the cut, so the values of the gates between the cut and $v$ agree, by induction in topological order. So the LUT of $v$ stores the function of $v$ in terms of $\mathrm{best}(v)$. The leaves are PIs or gates of the mapping, and by induction in topological order every LUT output equals its gate. $\square$

**Theorem 2 (the area passes do not raise the depth).** Let $D$ be the largest arrival time of an output after the depth pass. After each later pass, every output has arrival time at most $D$, and the arrival time of each gate is the depth of its LUT in the final LUT network.

*Proof.* A node is visited once per pass, after all its fanins, and line L10 sets $\mathrm{arr}(v)$ from the arrival times of the leaves of $\mathrm{best}(v)$, which do not change later in the pass, since the leaves come before $v$. So at the end of a pass, $\mathrm{arr}$ is the depth function of the mapping given by best. This is the second claim.

Assume that before an area pass, the mapping has all outputs at arrival time at most $D$; this holds after the depth pass by the choice of $D$. Line L3 sets $\mathrm{req}(o) = D$ for each output and, going backward, $\mathrm{req}(u) = \min(\mathrm{req}(u), \mathrm{req}(w) - 1)$ for each gate $w$ of the mapping and each $u \in \mathrm{best}(w)$, with $\mathrm{req} = \infty$ for nodes outside the mapping. Write $\mathrm{arr}_0$ and $\mathrm{best}_0$ for the values before the pass.

*Claim A: $\mathrm{arr}_0(u) \le \mathrm{req}(u)$ for every node $u$ with a finite required time.* Induction backward. For an output, $\mathrm{arr}_0(o) \le D$. For another node, $\mathrm{req}(u) = \mathrm{req}(w) - 1$ for some $w$ of the mapping with $u \in \mathrm{best}_0(w)$, and $\mathrm{arr}_0(u) \le \mathrm{arr}_0(w) - 1 \le \mathrm{req}(w) - 1$.

*Claim B: after the pass, $\mathrm{arr}(v) \le \mathrm{req}(v)$ for every node $v$ with a finite required time.* Induction in topological order. A PI has $\mathrm{arr} = 0 = \mathrm{arr}_0 \le \mathrm{req}$ by Claim A. Let $v$ be a gate with a finite required time. Then $v$ is in the old mapping, and every $u \in \mathrm{best}_0(v)$ has $\mathrm{req}(u) \le \mathrm{req}(v) - 1$. By induction $\mathrm{arr}(u) \le \mathrm{req}(u)$, so $\mathrm{dep}(\mathrm{best}_0(v)) \le \mathrm{req}(v)$, and the cut is not late. Line L6 makes it a candidate. Line L8 puts every late cut after every cut that is not late, so the chosen cut is not late, and $\mathrm{arr}(v) \le \mathrm{req}(v)$.

Claim B at the outputs gives arrival times at most $D$ after the pass, which keeps the assumption for the next pass. $\square$

**Theorem 3 (the exact area pass does not add LUTs).** The number of LUTs of the mapping after the exact area pass is at most the number before it.

*Proof.* Let $r(u)$ be the reference count of gate $u$. The invariant is that $r(u)$ equals the number of uses of $u$ in the current mapping: once per output that is $u$, and once per gate $w$ of the mapping with $u \in \mathrm{best}(w)$. Then the mapping is the set $S$ of gates with $r > 0$. Line L3 sets up the invariant. Referencing a cut $B$ of $v$ adds one use to each gate of $B$, and when a count goes from 0 to 1 that gate joins $S$ and its own best cut is referenced in turn. The returned value is $1 + $ the number of gates that join $S$. Dereferencing is the exact reverse, with $1 + $ the number of gates that leave $S$.

Let $v$ be a gate of the mapping when it is visited, and $|S| = A$. Line L7 dereferences $\mathrm{best}_0(v)$, which returns $a_0 = 1 + $ the number of gates that leave. Now $v$ still has $r(v) > 0$, but its cut is not counted. The exact area of a candidate $B$ is the value of referencing $B$ in this state, then dereferencing it, which restores the state. For $B = \mathrm{best}_0(v)$, referencing reverses line L7 exactly, so its exact area is $a_0$. If line L9 picks $B^*$ with exact area $a^*$, line L11 references it, and the new size is $A - (a_0 - 1) + (a^* - 1) = A - a_0 + a^*$.

By Theorem 2, $\mathrm{best}_0(v)$ is not late. Line L8 sorts the cuts that are not late by exact area first, so $a^* \le a_0$, and $|S|$ does not grow. A gate that is not in the mapping when it is visited changes only its own best cut, which no LUT of the mapping uses, so $S$ does not change. If such a gate joins the mapping later, through the cut of a later gate, its LUTs are counted in the exact area of that cut. By induction over the visits, the final $|S|$ is at most the first. $\square$

**Theorem 4 (unlimited cuts give the least depth).** If $C$ is at least the number of candidates of every node, the depth pass sets $\mathrm{arr}(v)$ to the least depth of $v$ over all $k$-LUT mappings, for every node $v$.

*Proof.* With no limit, $P(v)$ is the whole set $A$ of line L8, and in the depth pass line L6 adds nothing. Lines L5 and L9 are then the algorithm CUTS of [cut enumeration](/cut-enumeration/), with $P(u) \cup \{\{u\}\}$ in the role of $\Phi(u)$. By its theorem, $P(v)$ is the set of minimal $k$-feasible cuts of $v$ other than $\{v\}$. Let $d(v)$ be the least of $\mathrm{dep}$ over all $k$-feasible cuts of $v$ without $v$, computed from the values $d$ of the leaves, with $d = 0$ at the PIs. A minimal cut inside a cut has no larger depth, so the minimum over minimal cuts is the same. The depth key sorts first by depth, so line L10 sets $\mathrm{arr}(v) = d(v)$ by induction in topological order. By Lemma 1 of the proof of [FlowMap](/flowmap/), $d(v)$ is the least depth of $v$ in any $k$-LUT mapping. $\square$

**Corollary.** For any $C$, the depth after all passes is at least the least depth and at most the depth $D$ of the first pass. The lower bound holds for every mapping by Lemma 1 of the FlowMap proof, and the upper bound is Theorem 2.

**Termination.** Each pass visits each gate once, and every step handles finite sets. Referencing and dereferencing recurse only into gates whose count crosses 0, and each recursion goes to earlier nodes, so they end.
