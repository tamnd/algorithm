---
title: Quartet MaxCut returns a tree on the taxa, counts its displayed quartets exactly, and finds the best ratio cut
proves: [correctness]
status: full
---

**Setting.** The input is a finite set $S$ of taxa and a list $Q$ of quartets $ab|cd$, each on four distinct taxa of $S$. An unrooted tree $T$ whose leaves are the taxa *displays* $ab|cd$ if some edge of $T$ has $a, b$ on one side and $c, d$ on the other. For a cut $(S_1, S_2)$ of $S$ and a quartet $q$, the *good* edges of $q$ are $ac, ad, bc, bd$ and the *bad* edges are $ab, cd$. $G$ and $B$ count the good and bad edges, over all quartets, whose ends are on different sides. We prove four claims: the procedure stops, it returns a tree whose leaves are exactly $S$, the count `satisfied` equals the number of quartets of $Q$ that the tree displays, and the cut of lines L4 and L5 has the largest ratio $G/B$ when the cut search is exact.

**Fact 1 (one quartet per four taxa).** A tree displays at most one of the three quartets on a set of four taxa.

*Proof.* Suppose that the edge $e$ separates $\{a, b\}$ from $\{c, d\}$ and the edge $f$ separates $\{a, c\}$ from $\{b, d\}$. Removing $e$ leaves two components, one with $a, b$ and one with $c, d$. The path from $a$ to $b$ lies in the first component, so it does not use $e$, and the path from $c$ to $d$ does not use $e$ either. The edge $f$ is on the path from $a$ to $b$, because it separates them, and on the path from $c$ to $d$. So $f \ne e$ lies on a path inside the first component and on a path inside the second component, which is impossible, because the components are disjoint. The other pairs of quartets are handled in the same way. $\square$

**Fact 2 (display depends only on the restriction).** Whether $T$ displays a quartet on $\{a, b, c, d\}$ depends only on the subtree $T(a, b, c, d)$ spanned by the four leaves, up to vertices of degree 2.

*Proof.* An edge of $T$ that separates $a, b$ from $c, d$ lies on the paths from $a$ to $c$ and from $b$ to $d$, so it is an edge of the spanned subtree. An edge of the spanned subtree separates the four leaves in the same way in $T$ and in the subtree. $\square$

**Lemma 1 (the join).** Let $T_1$ be a tree with leaf set $S_1 \cup \{x_1\}$ and $T_2$ a tree with leaf set $S_2 \cup \{x_2\}$, where $S_1 \cap S_2 = \emptyset$, $|S_1|, |S_2| \ge 2$, and every internal vertex has degree at least 3. Let $p$ and $q$ be the neighbors of $x_1$ and $x_2$. The join $T$ removes $x_1$ and $x_2$ with their edges and adds the edge $pq$. Then:

1. $T$ is a tree with leaf set $S_1 \cup S_2$, and every internal vertex has degree at least 3.
2. The edge $pq$ has exactly $S_1$ on one side.
3. For each $z \in S_2$, the subtree of $T$ spanned by $S_1 \cup \{z\}$ is $T_1$ with $x_1$ renamed to $z$, up to vertices of degree 2. The same holds with the roles of the two sides exchanged.

*Proof.* Removing a leaf from a tree leaves a tree, and joining two disjoint trees by one edge gives a tree. The vertex $p$ loses the edge to $x_1$ and gains the edge to $q$, so its degree is unchanged, and the same holds for $q$. No other degree changes, and $x_1$, $x_2$ were the only removed leaves, so part 1 holds. Removing $pq$ gives back $T_1 - x_1$ and $T_2 - x_2$, which proves part 2. For part 3, the path in $T$ from a leaf $s \in S_1$ to $z$ runs inside $T_1 - x_1$ from $s$ to $p$, then along $pq$, then inside $T_2 - x_2$ from $q$ to $z$. So the subtree spanned by $S_1 \cup \{z\}$ consists of the subtree of $T_1 - x_1$ spanned by $S_1 \cup \{p\}$, plus a path from $p$ to $z$. In $T_1$, the subtree spanned by $S_1 \cup \{x_1\}$ is the same subtree of $T_1 - x_1$, plus the edge from $p$ to $x_1$. Up to degree 2 vertices on the path from $p$ to $z$, the two are equal after renaming. $\square$

**Lemma 2 (termination and the shape of the output).** Every subproblem has at least one taxon, every quartet of a subproblem has four distinct taxa of that subproblem, and every subproblem that is split has strictly larger size than its two children. So the procedure stops and returns a tree with leaf set $S$ in which every internal vertex has degree at least 3.

*Proof.* Line L3 only allows cuts with $|S_1|, |S_2| \ge 2$, so a subproblem of size $s \ge 4$ has children of sizes $|S_1| + 1 \le s - 1$ and $|S_2| + 1 \le s - 1$. A quartet sent to the side $S_1$ in line L9 has three or four taxa in $S_1$, and at most one taxon in $S_2$, which is replaced by the new taxon $x_1$. So it has four distinct taxa of $S_1 \cup \{x_1\}$. The same holds for $S_2$. A base case of line L2 returns a star, which is a tree with the right leaves and with a center of degree at least 3 when it has three or more leaves. By induction from the leaves of the recursion, using Lemma 1 part 1, every subproblem returns a tree with its own leaf set. $\square$

**Lemma 3 (the count is exact).** For every subproblem $(S, Q)$, the number of quartets that the procedure counts as satisfied while it solves this subproblem and all subproblems below it equals the number of quartets of $Q$ displayed by the returned tree.

*Proof.* Induction on the size of the subproblem. In a base case, the star has no edge that separates two leaves from two leaves, so it displays no quartet, and nothing is counted. This includes the case $|S| \le 3$, where $Q$ is empty by Lemma 2. Now let $(S_1, S_2)$ be the cut, and let $T$ be the join of $T_1$ and $T_2$. Take a quartet $q = ab|cd$ of $Q$.

- If $q$ has two taxa on each side and $\{a, b\}$ is one side, line L8 counts it. By Lemma 1 part 2, the edge $pq$ of $T$ separates $a, b$ from $c, d$, so $T$ displays $q$.
- If $q$ has two taxa on each side but the sides are not $\{a, b\}$ and $\{c, d\}$, line L8 does not count it. The edge $pq$ makes $T$ display the other quartet on these four taxa, the one whose pairs are the two sides. By Fact 1, $T$ does not display $q$.
- If $q$ has three or four taxa in $S_1$, line L9 sends $q'$ to the first child, where $q'$ is $q$ with its taxon $z$ in $S_2$, if there is one, replaced by $x_1$. By Fact 2 and Lemma 1 part 3, $T$ displays $q$ exactly when $T_1$ displays $q'$. If all four taxa are in $S_1$, the same holds with $q' = q$, because the subtree of $T$ spanned by $S_1$ is that of $T_1$.
- The case of three or four taxa in $S_2$ is symmetric.

Each quartet is in exactly one case, so the number of quartets of $Q$ displayed by $T$ is the number counted in line L8 for this cut, plus the numbers of quartets of the two children that their trees display. By induction, the latter equal the counts made below the children. $\square$

**Lemma 4 (Dinkelbach's iteration).** Suppose that line L4 and every step of line L5 return a cut that maximizes $G - \alpha B$ over all cuts with two or more taxa on each side. Then the loop stops after at most $2m + 1$ steps, where $m = |Q|$. When it stops with $B > 0$, the cut has the largest ratio $G/B$ among all allowed cuts with $B > 0$, and every allowed cut with $B = 0$ has $G = 0$. When it stops with $B = 0$, the cut has $G > 0$ or no allowed cut has $G > 0$.

*Proof.* Write $c_t$ for the cut after step $t$ and $\alpha_t = G(c_t) / B(c_t)$, with $\alpha_{-1} = 0$ the value used in line L4. The loop moves from $c_t$ to $c_{t+1}$ only if $G(c_{t+1}) - \alpha_t B(c_{t+1}) > 0 = G(c_t) - \alpha_t B(c_t)$. If $B(c_{t+1}) > 0$, dividing gives $\alpha_{t+1} > \alpha_t$. If $B(c_{t+1}) = 0$, the loop stops on the next test. Also $c_t$ maximized $G - \alpha_{t-1} B$, so $G(c_t) - \alpha_{t-1} B(c_t) \ge G(c_{t+1}) - \alpha_{t-1} B(c_{t+1})$. Adding this to the strict inequality above gives $(\alpha_t - \alpha_{t-1}) (B(c_t) - B(c_{t+1})) > 0$. For $t \ge 1$ the first factor is positive, so $B(c_{t+1}) < B(c_t)$. For $t = 0$ we have $\alpha_0 \ge 0 = \alpha_{-1}$, and the same argument gives $B(c_1) < B(c_0)$ when $\alpha_0 > 0$. If $\alpha_0 = 0$, then $G(c_0) = 0$ is the largest value of $G$, so every cut has $G = 0$ and the loop stops at once. So $B$ strictly decreases along the loop. Each quartet adds at most 2 to $B$, so $0 \le B \le 2m$, and there are at most $2m + 1$ steps.

If the loop stops with $B(c_t) > 0$, then $\max (G - \alpha_t B) \le 0$, so every allowed cut $c$ has $G(c) \le \alpha_t B(c)$. For $B(c) > 0$ this says $G(c)/B(c) \le \alpha_t$. For $B(c) = 0$ it says $G(c) \le 0$, so $G(c) = 0$. If the loop stops with $B(c_t) = 0$, either $G(c_t) > 0$, which is the best possible kind of cut, or $c_t = c_0$ with $G(c_0) = 0$, which is the largest $G$. $\square$

**Theorem.** QUARTET-MAX-CUT returns a tree whose leaves are exactly the input taxa and whose internal vertices have degree at least 3, and the returned count is the number of input quartets that this tree displays. With an exact cut search, the cut at each subproblem has the largest ratio of good to bad edges.

*Proof.* Lemmas 2, 3 and 4. $\blacksquare$

The theorem does not claim that the tree displays the largest possible number of quartets. Maximum quartet consistency is NP-hard, and the method is a heuristic. The test file checks the count against a brute force over all binary trees on up to six taxa, where the result is never above the optimum, and it is often equal to it.
