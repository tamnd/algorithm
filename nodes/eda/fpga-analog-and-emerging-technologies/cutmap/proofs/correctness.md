---
title: CutMap returns a valid LUT mapping with the same outputs and the least possible depth
proves: [correctness]
status: full
---

We use the notation of the page. $N$ is a $K$-bounded network, a directed acyclic graph whose sources are the primary inputs (PIs). A *cut* of a gate $v$ is a set $C$ of nodes with $v \notin C$ that meets every path from a PI to $v$. It is $K$-feasible if $|C| \le K$. The *cone* of $v$ over $C$ is the set of nodes $w$ with a path from $w$ to $v$ that has no node of $C$ (including $v$ and excluding $C$). The label $\ell$ is as on the page, and $D = \max_o \ell(o)$.

**Lemma 1 (the cut lists).** For every gate $v$, every set in the list of $v$ made by cut enumeration is a $K$-feasible cut of $v$, and every minimal $K$-feasible cut of $v$ is in the list.

*Proof.* By induction in topological order. Every set in the list is a union over the fanins $f$ of $v$ of either $\{f\}$ or a set from the list of $f$, and has at most $K$ nodes. A path from a PI to $v$ passes a fanin $f$ last. If $\{f\}$ was taken, the path meets it. Otherwise it meets the cut of $f$, by induction. So the union is a cut of $v$.

Now let $C$ be a minimal cut of $v$ with $|C| \le K$. For a fanin $f$ in $C$ take $\{f\}$. A fanin $f$ that is a PI is in $C$, because the path $f, v$ must meet $C$ and $v \notin C$. For a gate fanin $f \notin C$, every path from a PI to $f$ extends to a path to $v$, which meets $C$ at a node before $v$, so $C \cap (\text{nodes with a path to } f)$ is a cut of $f$. It contains a minimal cut $C_f$ of $f$ with $|C_f| \le K$, which is in the list of $f$ by induction. The union $U$ of the chosen sets is a subset of $C$ and a cut of $v$ by the first part, so $U = C$ by the minimality of $C$. The enumeration made $U$, and it is not removed as dominated, because no strict subset of $C$ is a cut of $v$. $\square$

**Lemma 2 (labels).** The labels computed from the lists equal $1 + \min_C \max_{u \in C} \ell(u)$ over all $K$-feasible cuts $C$ of $v$.

*Proof.* Each listed set is a $K$-feasible cut (Lemma 1), so the computed minimum is at least the true one. A cut $C$ that reaches the true minimum contains a minimal cut $C' \subseteq C$, with $|C'| \le K$ and $\max_{C'} \ell \le \max_C \ell$, and $C'$ is in the list. So the computed minimum is at most the true one. $\square$

**Lemma 3 (order).** Every root is visited once at line L2, and when it is visited, its value $r(u)$ does not change again.

*Proof.* A gate $u$ becomes a root at line L8 when it is in the cut of a root $v$. A node of a cut of $v$ has a path to $v$, so it comes before $v$ in topological order, and after $v$ in the reverse order of line L2. So the loop reaches $u$ after it was added. The value $r(u)$ changes only at line L9 while some root $v$ with $u \in C_v$ is visited, and every such $v$ comes before $u$ in the reverse order. $\square$

**Lemma 4 (invariant).** For every root $u$, $\ell(u) \le r(u)$ at all times after $r(u)$ is first set, and the set $F$ of line L4 is never empty.

*Proof.* At line L1, $r(o) = D \ge \ell(o)$ for each output. Let $v$ be the root visited at line L2, with $\ell(v) \le r(v)$. By Lemma 2 there is a listed cut of height $\ell(v) - 1 \le r(v) - 1 = b$, so $F$ is not empty. Every node $u$ of the chosen cut $C^*$ has $\ell(u) \le b = r(v) - 1$. Every value of $r$ is at most $D$, by line L1 and line L9. If $r(u)$ was not set, line L9 sets it to $\min(D, r(v) - 1) = r(v) - 1 \ge \ell(u)$. If $r(u)$ was set, then $\ell(u) \le r(u)$ already, and the minimum of two values that are both at least $\ell(u)$ is at least $\ell(u)$. $\square$

**Theorem 5 (valid mapping, same function).** Every LUT has at most $K$ inputs, every gate input of a LUT is a root with its own LUT, and the LUT network computes the same value as $N$ at every root, for every input vector.

*Proof.* The cut of each LUT is in a list, so it has at most $K$ nodes. Every gate of $C^*$ becomes a root at line L8, and it gets its LUT when it is visited (Lemma 3, Lemma 4). The LUT of $v$ evaluates the gates of the cone of $v$ over $C^*$, reading the values of the nodes of $C^*$. This is well defined: a node of the cone that is a PI would give a path from a PI to $v$ that misses $C^*$, which is not possible because $C^*$ is a cut. By induction in topological order over the roots, each node of $C^*$ is a PI or a root whose LUT gives the value of the node in $N$, so the LUT of $v$ gives the value of $v$ in $N$. $\square$

**Theorem 6 (depth).** The LUT depth of every root $u$ is at most $r(u)$. In particular, every output has depth at most $D$.

*Proof.* By induction in topological order. The depth of a root $v$ is $1 + \max_{u \in C^*} \mathrm{depth}(u)$, where a PI has depth 0. A gate $u \in C^*$ has $r(u) \le r(v) - 1$ after line L9, and this value is final when the depth of $u$ is fixed (Lemma 3), so $\mathrm{depth}(u) \le r(u) \le r(v) - 1$ by induction. A PI has depth $0 \le r(v) - 1$, because $r(v) \ge \ell(v) \ge 1$ by Lemma 4. So $\mathrm{depth}(v) \le r(v)$. $\square$

**Theorem 7 (optimal depth, cited).** No $K$-LUT mapping of $N$ has depth below $D$, so the depth of CutMap is exactly $D$.

*Proof.* Cong and Ding proved for FlowMap that the label $\ell(v)$ is the least depth of a LUT that computes $v$ in any $K$-LUT mapping of a $K$-bounded network. The proof is on the [FlowMap page](/flowmap/) and is not repeated here. With Lemma 2, the labels used by CutMap are those labels. So every mapping has an output of depth at least $D$, and with Theorem 6 the depth of CutMap is exactly $D$. $\square$

**Relaxed bound.** If the caller gives a bound $D' \ge D$, line L1 sets $r(o) = D'$ and the proofs of Lemma 4 and Theorem 6 go through with $D'$ in place of $D$, so the depth is at most $D'$.

**What is not proved.** Nothing here says that the number of LUTs is least. The choice at line L5 is greedy, and the page reports measured counts only. The reduction against FlowMap (15% in the abstract of Cong and Hwang 1995, 13% in the survey of Cong and Ding 1996, Section 5.4) is measured by those authors, not proved.
