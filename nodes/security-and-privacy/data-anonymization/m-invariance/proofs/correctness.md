---
title: The one-pass check decides m-invariance exactly
proves: [correctness]
status: full
---

A release $T^*(j)$ is a partition of the tuples published at time $j$ into QI groups, where each tuple is a record or a counterfeit. The **signature** $\sigma(G)$ of a group $G$ is the set of distinct sensitive values in $G$. A release is **$m$-unique** if every group has at least $m$ tuples and no two tuples of a group share a sensitive value. Each record occurs in at most one group per release, and the releases that contain a record $t$ form an interval $[x, y]$, its lifespan. For $x \le j \le y$, let $G_j(t)$ be the group of release $j$ that holds $t$. The sequence $T^*(1), \ldots, T^*(n)$ is **$m$-invariant** if (a) every release is $m$-unique and (b) for every record $t$ with lifespan $[x, y]$, the groups $G_x(t), \ldots, G_y(t)$ all have the same signature.

**Claim 1 (invariant).** Each time line L2 starts a new release $j$, if the check has not returned, then all groups of releases $1, \ldots, j-1$ are $m$-unique, and for each record $t$ seen so far, all its hosting groups in those releases have one signature, which is stored in $S[t]$. Records not seen so far are not keys of $S$.

*Proof.* It holds before release 1, with an empty map from line L1. Suppose it holds when release $j$ starts and the check does not return during release $j$. Line L4 did not return, so every group of release $j$ is $m$-unique. Take a record $t$ of release $j$ in group $G$. If $t$ was seen before, line L7 did not return, so $S[t] = \sigma(G)$, and by the invariant all earlier hosting groups of $t$ have signature $S[t]$. So all hosting groups of $t$ up to release $j$ share one signature. If $t$ is new, line L8 stores $\sigma(G)$, which is the signature of its only hosting group so far. Records of earlier releases that are not in release $j$ keep their entries. $\square$

**Claim 2 (exactness).** M-INVARIANT returns true if and only if the sequence is $m$-invariant.

*Proof.* If it returns true, Claim 1 after the last release gives (a), and gives (b) because the hosting groups $G_x(t), \ldots, G_y(t)$ are all the hosting groups of $t$. Conversely, suppose it returns false. If line L4 returns, the current group has fewer than $m$ tuples or two tuples with one value, so (a) fails. If line L7 returns at record $t$ in group $G$ of release $j$, then $t$ was seen in an earlier release, and by Claim 1 its earlier hosting groups have signature $S[t] \ne \sigma(G)$, so (b) fails for $t$. $\blacksquare$

The check compares all hosting groups of a record, so it does not need the lifespan to be an interval. The interval is needed for the next claim.

**Claim 3 (Lemma 4 of Xiao and Tao).** Suppose $T^*(1), \ldots, T^*(n-1)$ is $m$-invariant. Then $T^*(1), \ldots, T^*(n)$ is $m$-invariant if and only if $T^*(n)$ is $m$-unique and every record $t$ in both $T(n-1)$ and $T(n)$ has $\sigma(G_{n-1}(t)) = \sigma(G_n(t))$.

*Proof.* The conditions are necessary by (a) and (b). For sufficiency, (a) holds for the first $n-1$ releases by assumption and for release $n$ by the first condition. For (b), take a record $t$. If $n$ is not in its lifespan, (b) for $t$ is the assumption. If its lifespan is $[n, n]$, there is one group. Otherwise its lifespan is $[x, n]$ with $x < n$, and since the lifespan is an interval, $t$ is in $T(n-1)$. The assumption gives one signature for $G_x(t), \ldots, G_{n-1}(t)$, and the second condition extends it to $G_n(t)$. $\square$

**Claim 4 (the persistent set is large).** If the sequence is $m$-invariant, then for every record $t$ the intersection of the signatures of its hosting groups has at least $m$ values and contains the sensitive value of $t$.

*Proof.* By (b) the intersection equals $\sigma(G_x(t))$. By (a), $G_x(t)$ has at least $m$ tuples with pairwise different values, so $|\sigma(G_x(t))| = |G_x(t)| \ge m$. The value of $t$ is in $\sigma(G_j(t))$ for each $j$. $\square$

The candidate set $t.CSS(j)$ of the paper is the union of the signatures of all groups whose QI ranges cover the QI values of $t$, so it contains $\sigma(G_j(t))$. By Claim 4 the intersection of the candidate sets has at least $m$ values, so for $m \ge 2$ the full disclosure of Lemma 1 of the paper cannot happen. The bound of $1/m$ on the disclosure risk is Lemma 3 of the paper, proved there under its random-world model; it is not proved here.

**Cost.** Each tuple is read once at lines L4 to L6. Building a signature takes $O(|G|)$ expected time with hashing, and the comparison at line L7 takes $O(|G|)$, so the total is $O(\sum_G |G|^2) = O(N s)$, where $N$ is the number of tuples over all releases and $s$ is the largest group size.
