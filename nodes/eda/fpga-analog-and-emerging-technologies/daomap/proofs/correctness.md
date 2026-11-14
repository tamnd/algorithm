---
title: DAOmap returns a valid LUT mapping with the same outputs and the least possible depth, for any costs
proves: [correctness]
status: full
---

We use the notation of the page. $N$ is a $K$-bounded network, a directed acyclic graph whose sources are the primary inputs (PIs). A *cut* of a gate $v$ is a set $C$ of nodes with $v \notin C$ that meets every path from a PI to $v$, and it is $K$-feasible if $|C| \le K$. $\mathrm{arr}$ is computed at line L1, $D = \max_o \mathrm{arr}(o)$, and the slack of a cut $C$ of a root $v$ is $s(C) = r(v) - 1 - \max_{u \in C} \mathrm{arr}(u)$.

**Lemma 1 (cut lists and arrival times).** Every listed set of a gate $v$ is a $K$-feasible cut of $v$, every minimal $K$-feasible cut of $v$ is listed, and $\mathrm{arr}(v) = 1 + \min_C \max_{u \in C} \mathrm{arr}(u)$ over all $K$-feasible cuts $C$ of $v$.

*Proof.* The enumeration is the same as on the [CutMap proof](/cutmap/), Lemmas 1 and 2: a listed set is a union over the fanins $f$ of $\{f\}$ or a cut of $f$, so it meets every path into $v$; and a minimal cut $C$ of $v$ splits into $\{f\}$ for the fanins in $C$ and, for every other fanin $f$, a minimal cut of $f$ inside $C$, which is listed by induction, and their union is $C$ by minimality. A least-height cut contains a minimal cut of no greater height, so the minimum over the list equals the minimum over all cuts. $\square$

By Lemma 1, $\mathrm{arr}$ is the FlowMap label $\ell$.

**Lemma 2 (order).** Every root is visited once in a pass, after all roots that read it, so $r(u)$ is final when $u$ is visited.

*Proof.* A gate $u$ joins the roots at line L8 only when it is in the cut of a root $v$. Then $u$ has a path to $v$, so $u$ comes before $v$ in topological order and after $v$ at line L5. The value $r(u)$ changes only at line L8 while such a $v$ is visited. $\square$

**Lemma 3 (invariant, and a cut always exists).** In each pass, $\mathrm{arr}(u) \le r(u)$ for every root $u$ once $r(u)$ is set, and the set of cuts at line L6 or line L7 is not empty.

*Proof.* At line L4, $r(o) = D \ge \mathrm{arr}(o)$. Let $v$ be visited with $\mathrm{arr}(v) \le r(v)$. By Lemma 1 there is a listed cut $C_0$ with $\max_{u \in C_0} \mathrm{arr}(u) = \mathrm{arr}(v) - 1$, so $s(C_0) = r(v) - \mathrm{arr}(v) \ge 0$. If $r(v) = \mathrm{arr}(v)$, then $s(C_0) = 0$ and line L6 has a candidate. Otherwise $s(C_0) > 0$ and line L7 has a candidate. In both cases the chosen cut $C^*$ has $s(C^*) \ge 0$, so every $u \in C^*$ has $\mathrm{arr}(u) \le r(v) - 1$. All values of $r$ are at most $D$, so line L8 sets $r(u)$ to $r(v) - 1 \ge \mathrm{arr}(u)$ the first time, and later to a minimum of two values that are both at least $\mathrm{arr}(u)$. $\square$

The proof uses nothing about $A_C$, the share, the weight 0.3 or the tentative roots. They only decide which cut of nonnegative slack is taken.

**Theorem 4 (valid mapping, same function).** In each pass, every LUT has at most $K$ inputs, every gate input of a LUT has its own LUT, and the LUT network computes the value of $N$ at every root for every input vector.

*Proof.* Each chosen cut is listed, so it has at most $K$ nodes. Every gate of $C^*$ becomes a root at line L8 and is visited later (Lemma 2), where it gets a LUT (Lemma 3). The LUT of $v$ evaluates the gates between $C^*$ and $v$ from the values of $C^*$; no PI outside $C^*$ is reached, since $C^*$ is a cut. By induction in topological order over the roots, each node of $C^*$ carries its value in $N$, so $v$ does too. $\square$

**Theorem 5 (depth).** In each pass, the LUT depth of every root $u$ is at most $r(u)$, so every output has depth at most $D$.

*Proof.* By induction in topological order. A PI has depth 0. For a root $v$ with LUT $C^*$, each gate $u \in C^*$ has final $r(u) \le r(v) - 1$ and depth at most $r(u)$ by induction, and a PI in $C^*$ has depth $0 \le r(v) - 1$ because $r(v) \ge \mathrm{arr}(v) \ge 1$. So the depth of $v$ is at most $1 + (r(v) - 1) = r(v)$. $\square$

**Theorem 6 (optimal depth, cited).** No $K$-LUT mapping of $N$ has depth below $D$. So every pass, and the mapping returned at line L10, has depth exactly $D$.

*Proof.* Cong and Ding proved that the FlowMap label $\ell(v)$ is the least depth of $v$ in any $K$-LUT mapping of a $K$-bounded network; the proof is on the [FlowMap page](/flowmap/). By Lemma 1, $\mathrm{arr} = \ell$, so some output needs depth $D$ in every mapping. Theorem 5 gives the upper bound. Line L10 returns one of the pass mappings. $\square$

**What is not proved.** Nothing here bounds the number of LUTs. The area flow $A_v$ is an estimate and, as Chen and Cong note, it is not a lower bound on the area under the depth constraint. The LUT savings against CutMap are measured results of Chen and Cong (2004), not theorems.
