---
title: The pairwise anomaly classes of a firewall policy are computed exactly, and the redundant rules can be removed
proves: [correctness, complexity]
status: full
---

We use the pseudocode ANOMALIES of the page. A policy is a list of rules $R_1, \ldots, R_m$. Each rule has a box $B_i = I_{i,1} \times \cdots \times I_{i,d}$, a product of $d$ non-empty closed integer intervals, and an action. A packet $p$ is a point of the header space. The decision of the policy on $p$ is the action of the first rule whose box contains $p$, or a default action when there is none. For $x < y$ we write $a_x, a_y$ for the actions.

**Lemma 1 (relations of boxes).** RELATION$(B_x, B_y)$ returns DISJOINT if $B_x \cap B_y = \emptyset$, EQUAL if $B_x = B_y$, SUBSET if $B_x \subsetneq B_y$, SUPERSET if $B_x \supsetneq B_y$, and CORRELATED otherwise.

*Proof.* A point is in $B_x \cap B_y$ if and only if each coordinate is in both intervals, so the boxes meet if and only if each pair of intervals meets. Since all intervals are non-empty, $B_x \subseteq B_y$ if and only if $I_{x,j} \subseteq I_{y,j}$ for each $j$: if one interval of $B_x$ has a point $v$ outside the matching interval of $B_y$, then a point of $B_x$ with coordinate $v$ and any other coordinates in $B_x$ is not in $B_y$. The code tests these interval conditions, and the five cases follow. $\square$

**Claim 1 (exact classes).** For each pair $x < y$, ANOMALIES reports

- shadowing if $B_y \subseteq B_x$ and $a_x \ne a_y$;
- redundancy-later, with $R_y$ removable, if $B_y \subseteq B_x$ and $a_x = a_y$;
- generalization if $B_x \subsetneq B_y$ and $a_x \ne a_y$;
- redundancy-earlier, with $R_x$ removable, if $B_x \subsetneq B_y$, $a_x = a_y$, and no $z$ with $x < z < y$ has $B_z \cap B_x \ne \emptyset$ and $a_z \ne a_x$;
- correlation if the boxes meet, neither contains the other, and $a_x \ne a_y$;

and nothing else.

*Proof.* Fix $x$. The inner loop of line L4 runs $y = x + 1, \ldots, m$ in order. We show the invariant: when the iteration for $y$ starts, blocked is true if and only if some $z$ with $x < z < y$ has $B_z \cap B_x \ne \emptyset$ and $a_z \ne a_x$. Line L3 makes it true for $y = x + 1$. Line L11 sets blocked exactly when the current $y$ meets $B_x$ (line L6) and has another action, so the invariant holds for $y + 1$.

By Lemma 1 the test of line L6 skips exactly the disjoint pairs. Line L7 handles EQUAL and SUPERSET, which together mean $B_y \subseteq B_x$. Line L8 handles SUBSET with different actions. Line L9 is reached with SUBSET only when the actions are the same, and by the invariant it reports exactly when no such $z$ exists. Line L10 handles CORRELATED with different actions. The remaining cases, SUBSET with the same action and blocked, and CORRELATED with the same action, report nothing. $\square$

**Claim 2 (meaning of the classes).**

1. If $R_y$ is shadowed or later-redundant, $R_y$ decides no packet.
2. If $R_y$ is later-redundant, removing it changes no decision.
3. If $R_x$ is earlier-redundant with $R_y$, removing $R_x$ changes no decision.

*Proof.* (1) Each $p \in B_y$ is in $B_x$ with $x < y$, so the first match of $p$ is at most $x$. (2) By (1) no packet has $R_y$ as its first match, and the first match of each packet is the same rule with or without $R_y$.

(3) Let $p$ be a packet. If $p \notin B_x$, then $R_x$ is not a match of $p$, and the first match is the same rule with or without $R_x$. If the first match of $p$ is a rule before $x$, it stays the first match. Otherwise the first match of $p$ is $R_x$ and the decision is $a_x$. After removing $R_x$, the first match of $p$ is the first $z > x$ with $p \in B_z$. If $x < z < y$, then $B_z$ meets $B_x$ at $p$, and by the condition $a_z = a_x$. If there is no such $z$, then $p \in B_x \subseteq B_y$, so $R_y$ is the first match, and $a_y = a_x$. In each case the decision stays $a_x$. $\square$

**Remark (the condition of line L9).** The condition must cover every rule between $x$ and $y$ that meets $B_x$ with another action, including one inside $B_x$. With $B_1 \subsetneq B_3$, $a_1 = a_3$ and $B_2 \subsetneq B_1$ with $a_2 \ne a_1$, the pair $(R_1, R_2)$ is a shadowing anomaly, not a generalization or a correlation, but removing $R_1$ changes the decision on $B_2$ from $a_1$ to $a_2$. A condition that only looks for generalization and correlation anomalies of $R_x$ would call $R_1$ removable here. The test checks this case.

**Limits.** The classes are pairwise. A rule can be covered by the union of earlier rules without being inside any one of them, and then it decides no packet but no pair reports shadowing. The function IS-DEAD of the code finds this by subtracting each earlier box from the boxes that remain. Subtracting one box from another gives at most $2d$ disjoint boxes, so it is exact, but the number of pieces can grow exponentially with the number of rules.

**Cost.** Line L5 costs $O(d)$ by Lemma 1, and lines L6 to L11 cost $O(1)$ more, for each of the $m(m-1)/2$ pairs. So ANOMALIES takes $\Theta(m^2 d)$ time on the word-RAM, and $O(1)$ extra space besides the output, which has at most $m(m-1)/2$ entries. $\blacksquare$
