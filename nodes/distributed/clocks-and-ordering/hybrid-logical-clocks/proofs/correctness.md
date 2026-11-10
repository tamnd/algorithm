---
title: Hybrid logical clocks respect causality and stay close to physical time
proves: [correctness]
status: full
---

**Model.** There are $N$ processes. Each event $f$ happens at a real time $t_f$, and the process reads its physical clock $pt.f$, a positive integer. Real time respects causality: if $g \to f$ then $t_g \le t_f$. The clocks of a process never go back, and two clocks never differ by more than $\varepsilon$ at the same real time. Together these give the *skew bound*: if $t_g \le t_f$, then $pt.g \le pt.f + \varepsilon$. Indeed, if $g$ is at process $j$ and $f$ at process $k$, then $pt.g = pt_j(t_g) \le pt_k(t_g) + \varepsilon \le pt_k(t_f) + \varepsilon = pt.f + \varepsilon$. Each process starts with $l = c = 0$. We write $(l.f, c.f)$ for the timestamp of event $f$, and $<$ on timestamps is the lexicographic order.

For an event $f$, its *direct predecessors* are the previous event of the same process, if any, and, if $f$ is a receive, the matching send. The happened-before relation $\to$ is the transitive closure of the direct predecessor relation.

**Lemma 1.** For every event $f$, $l.f \ge pt.f$, and $l.f \ge l.g$ for every direct predecessor $g$.

*Proof.* Lines L3 and L5 set $l$ to a maximum over the old $l$ (the $l$ of the previous event, or $0$), the physical reading $pt.f$, and for a receive the $l$ of the message, which is $l$ of the send. $\square$

**Theorem 1 (causality).** If $e \to f$, then $(l.e, c.e) < (l.f, c.f)$.

*Proof.* The lexicographic order is transitive, so it is enough to check a direct predecessor $g$ of $f$. By Lemma 1, $l.g \le l.f$. If $l.g < l.f$ we are done, so assume $l.f = l.g$.

- $f$ is a send or a local event and $g$ the previous event. Then $l.f = l.g$ is the old value, and line L4 sets $c.f = c.g + 1$.
- $f$ is a receive and $g$ the previous event. If also $l.f = l_m$, line L6 sets $c.f = \max(c.g, c_m) + 1 > c.g$. Otherwise line L7 sets $c.f = c.g + 1$.
- $f$ is a receive and $g$ the send. If also $l.f$ equals the old value, line L6 gives $c.f > c_m = c.g$. Otherwise line L8 gives $c.f = c_m + 1 = c.g + 1$.

In each case $c.g < c.f$. $\blacksquare$

**Lemma 2.** For every event $f$ there is an event $g$ with $g = f$ or $g \to f$ such that $l.f = pt.g$.

*Proof.* By induction along $\to$. The value $l.f$ is the largest of $pt.f$, the old $l$, and $l_m$. Since $pt.f \ge 1$, the initial old value $0$ is never larger than $pt.f$. If $l.f = pt.f$, take $g = f$. If $l.f$ equals the $l$ of a direct predecessor $h$, use the claim for $h$ and transitivity. $\square$

**Corollary 1 (closeness).** For every event $f$, $0 \le l.f - pt.f \le \varepsilon$.

*Proof.* The lower bound is Lemma 1. For the upper bound, take $g$ from Lemma 2. Then $t_g \le t_f$, so $l.f = pt.g \le pt.f + \varepsilon$ by the skew bound. $\square$

**Lemma 3 (what $c$ counts).** For every event $f$, $c.f \le |\{g : g \to f \text{ and } l.g = l.f\}|$.

*Proof.* By induction on $c.f$. If $c.f = 0$ there is nothing to show. If $c.f = k > 0$, the rule that set $c.f$ took $1$ plus the $c$ of a direct predecessor $h$ with $l.h = l.f$. Lines L4 and L7 use the previous event, whose $l$ is the old value equal to $l.f$. Line L8 uses the send, whose $l$ is $l_m = l.f$. Line L6 uses whichever of the two has the larger $c$, and both have $l = l.f$. The predecessor is a real event and not the initial state, because the initial $l$ is $0 < pt.f \le l.f$. So $c.h \ge k - 1$, and by induction there are at least $k - 1$ events $g \to h$ with $l.g = l.h$. Together with $h$, these are at least $k$ events $g \to f$ with $l.g = l.f$. $\square$

**Corollary 2 (bounded counter).** If the readings of each process strictly increase from one event to the next, then $c.f \le N(\varepsilon + 1)$ for every event $f$.

*Proof.* Let $L = l.f$. Every event $g$ with $l.g = L$ has $pt.g \le L$ by Lemma 1 and $pt.g \ge L - \varepsilon$ by Corollary 1. So $pt.g$ takes one of $\varepsilon + 1$ integer values. Each process has at most one event per value, since its readings strictly increase. So at most $N(\varepsilon + 1)$ events have $l = L$, and Lemma 3 gives the bound. $\blacksquare$
