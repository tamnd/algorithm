---
title: Clustered voltage scaling returns a legal timed set, and under additive delays the largest one
proves: [correctness]
status: full
---

**Setting.** The circuit is a DAG of gates with primary inputs at time 0, a set $O$ of output gates that drive registers, delays $0 \le d_H(g) \le d_L(g)$ and a converter delay $\ell_c \ge 0$. For a set $L$ of low gates, $d_L$ applies to the gates of $L$ and $d_H$ to the others. The delay of a path $\pi = (g_1, \ldots, g_k)$ from a gate driven by a primary input to an output gate $g_k \in O$ is

$$ D_L(\pi) = \sum_{i=1}^{k} d_L(g_i)[g_i \in L] + d_H(g_i)[g_i \notin L] \;+\; \ell_c [g_k \in L]. $$

The worst output time $W(L) = \max_o a(o) + \ell_c [o \in L]$ equals $\max_\pi D_L(\pi)$ over all such paths, by the usual longest path recursion. $L$ meets $T$ when $W(L) \le T$, and $L$ is legal when every gate fanout of every gate of $L$ is in $L$. Call $L$ feasible when it is legal and meets $T$.

**Lemma 1 (monotone delay).** If $L \subseteq L'$ then $W(L) \le W(L')$.

*Proof.* For each path, $D_{L'}(\pi) - D_L(\pi)$ is a sum of terms $d_L(g) - d_H(g) \ge 0$ and possibly $\ell_c \ge 0$. Take the maximum over paths. $\square$

**Lemma 2 (invariants).** After each pass of lines L2 to L6, $L$ is feasible.

*Proof.* At line L1, $L = \emptyset$ is legal, and it meets $T$ by the check of line L1. Line L4 adds $g$ only when every gate driven by $g$ is in $L$, so $L \cup \{g\}$ is legal: the gates of $L$ keep their fanouts in $L$, and $g$ has its fanouts in $L$. If $L \cup \{g\}$ misses $T$, line L6 returns to $L$. $\square$

**Lemma 3 (suffix).** If $L$ is legal and $\pi = (g_1, \ldots, g_k)$ is a path of gates, then $\{i : g_i \in L\}$ is a set of the form $\{j, j+1, \ldots, k\}$, possibly empty.

*Proof.* If $g_i \in L$ and $i < k$, then $g_{i+1}$ is a gate driven by $g_i$, so $g_{i+1} \in L$ by legality. $\square$

**Lemma 4 (union).** If $L_1$ and $L_2$ are feasible, so is $L_1 \cup L_2$.

*Proof.* Legality: each gate of $L_1 \cup L_2$ lies in $L_1$ or in $L_2$, and its gate fanouts lie in the same set. Timing: fix a path $\pi$. By Lemma 3 its low gates under $L_1$ are a suffix starting at $j_1$, and under $L_2$ a suffix starting at $j_2$ (with $j = k + 1$ for an empty suffix). Its low gates under $L_1 \cup L_2$ are the union of the two suffixes, which is the longer one. Say $j_1 \le j_2$. Then $\pi$ has the same low gates under $L_1 \cup L_2$ as under $L_1$. The delay $D_L(\pi)$ depends only on which gates of $\pi$ are in $L$, since each gate's delay depends only on its own supply and the converter term only on $g_k$. So $D_{L_1 \cup L_2}(\pi) = D_{L_1}(\pi) \le W(L_1) \le T$. The case $j_2 < j_1$ is the same with $L_2$. Taking the maximum over paths gives $W(L_1 \cup L_2) \le T$. $\square$

So if any feasible set exists, the union of all feasible sets is feasible, and it is the largest feasible set $L^*$.

**Theorem.** If the circuit meets $T$ with every gate high, line L7 returns $L^*$.

*Proof.* Let $R$ be the returned set. By Lemma 2, $R$ is feasible, so $R \subseteq L^*$. Suppose that $L^* \not\subseteq R$. Let $h$ be the first gate of $L^* \setminus R$ in the order of line L2, and let $R_h$ be the value of $L$ when line L2 reaches $h$.

Every gate $f$ driven by $h$ is in $L^*$ by legality of $L^*$. The order of line L2 is reverse topological, so $f$ comes before $h$. Since $h$ is the first gate of $L^*$ that is missing from $R$, the gate $f$ is in $R$. A gate is added to $L$ only at line L4 and is removed only at line L6 in the same pass, so a gate of $R$ that comes before $h$ is in $R_h$. So every gate driven by $h$ is in $R_h$, the test of line L3 holds, and line L4 tries $R_h \cup \{h\}$. Since $h \notin R$, line L5 found $W(R_h \cup \{h\}) > T$.

But $R_h$ is feasible by Lemma 2 and $L^*$ is feasible, so $R_h \cup L^*$ is feasible by Lemma 4. Since $h \in L^*$, we have $R_h \cup \{h\} \subseteq R_h \cup L^*$, and Lemma 1 gives $W(R_h \cup \{h\}) \le W(R_h \cup L^*) \le T$. This contradicts the result of line L5. So $L^* \subseteq R$, and $R = L^*$. $\square$

**Corollary.** For any nonnegative weights $w_g$, such as $w_g = \alpha_g C_g (V_H^2 - V_L^2) f$, the result has the largest total weight among all feasible sets, and every reverse topological order gives the same result.

*Proof.* Every feasible set is a subset of $L^*$, and the weights are nonnegative. The set $L^*$ does not depend on the order. $\square$

**Where the proof stops.** Lemma 4 uses that the delay of a gate depends only on its own supply. If the delay of $g$ also depends on the supply of its driver, through the input slope, or on the supplies of the gates it drives, through their input capacitance, the delay of a path is no longer fixed by its set of low gates alone, Lemma 4 can fail, and the greedy is then only a heuristic. The tests check the theorem on random circuits of up to 9 gates against all subsets.

**Why the rule is needed (physics, not a theorem of this page).** In static CMOS, a gate on $V_H$ whose input is high at $V_L$ has a PMOS transistor with its source at $V_H$ and its gate at $V_L$, so $V_{GS} = V_L - V_H$. The PMOS conducts when $V_H - V_L > |V_{Tp}|$, while the NMOS of the same input also conducts, so a static current flows from $V_H$ to ground. A low input to a low gate, or a high gate driving a low gate, has no such problem, since a high level at $V_H$ turns the PMOS of a low gate fully off.
