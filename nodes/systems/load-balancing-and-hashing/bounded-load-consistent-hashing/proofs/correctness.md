---
title: After every update no bin is over the capacity, no ball passes a bin with room, and the loads do not depend on the order of the updates
proves: [correctness]
status: full
---

We use the pseudocode of the page. There are $n \ge 1$ bins at distinct points of the ring and $m$ balls, and $\text{CAP} = \lceil c\, m / n \rceil$ with $c = 1 + \varepsilon > 1$. For a ball $x$, $\text{start}(x)$ is the first bin at or after the hash of $x$, and $a(x)$ is the bin that holds $x$. The walk $W(x)$ is the list of bins from $\text{start}(x)$ clockwise to $a(x)$, and $|W(x)|$ is the number of steps from $\text{start}(x)$ to $a(x)$. The ball $x$ *passes* a bin $b$ when $b$ is on $W(x)$ and $b \ne a(x)$. A bin is *full* when its load is at least CAP. The two invariants are:

- **(C)** every bin has load at most CAP;
- **(I)** every bin that some ball passes is full.

**Lemma 1 (there is room).** $n \cdot \text{CAP} \ge c\, m > m - 1$. So if at most $m - 1$ balls are in the bins, some bin has load less than CAP. If all $m$ balls are in the bins and some bin has load more than CAP, some other bin has load less than CAP.

*Proof.* $n \lceil c m / n \rceil \ge c m$. For $m \ge 1$, $c\, m > m$; for $m = 0$ the claims are empty. If all bins had load at least CAP and one had more, the total would be more than $n \cdot \text{CAP} \ge m$. $\square$

**Lemma 2 (insertion).** Lines L2 to L5 stop and put $x$ in a bin with load less than CAP, and $x$ passes only full bins.

*Proof.* Before line L5, the other $m - 1$ balls are in the bins, so by Lemma 1 some bin has room, and the walk of line L3 reaches it within $n$ steps. Every bin that the walk skips has load at least CAP. $\square$

**Lemma 3 (the shed phase).** Lines L9 to L11 stop. After them every bin has load at most CAP, and no bin has gone from load at most CAP to more.

*Proof.* Each move of line L11 takes a ball from a bin with load more than CAP and puts it in a bin with load less than CAP, which exists by Lemma 1. So the sum of $\max(\text{load} - \text{CAP}, 0)$ over the bins drops by 1, and no bin goes over CAP. $\square$

**Lemma 4 (the fill phase keeps (C) and stops).** Each move of line L16 puts a ball into a bin with load less than CAP, and the loop of lines L12 to L17 stops.

*Proof.* The first claim is the test of line L15. For the second, let $\Phi = \sum_x |W(x)|$. A move of line L16 takes a ball $x$ that passes $b$ and puts it in $b$. The new walk of $x$ is the part of the old walk up to $b$, which is shorter by at least one step. No other walk changes. So $\Phi$ drops by at least 1 at each move, and $\Phi \ge 0$, so there are finitely many moves. A sweep of line L14 with no move ends the loop at line L17, and each sweep is finite. $\square$

**Lemma 5 (a sweep with no move gives (I)).** If a full sweep of lines L14 to L16 makes no move, then (I) holds.

*Proof.* Suppose that a ball $x$ passes a bin with load less than CAP. Let $j$ be the last such bin on $W(x)$ before $a(x)$. The bins strictly between $j$ and $a(x)$ are on $W(x)$ after $j$, so they are full. When the sweep visits $j$, line L15 looks at the bins after $j$, through full bins, up to and including the next bin with load less than CAP. That next bin is $a(x)$ or a bin after it, so the scan looks at the balls of $a(x)$ and finds $x$, which passes $j$. Then line L16 moves a ball. Since the sweep made no move, the state when it visited $j$ is the final state, and this is a contradiction. $\square$

**Theorem 1 (the invariants).** After each INSERT and each DELETE, (C) and (I) hold. The same holds after adding a bin and running REPAIR, and after removing a bin, putting each of its balls into the first bin with room from its start, and running REPAIR.

*Proof.* REPAIR ends with the fill phase, which by Lemma 4 stops and never puts a bin over CAP, and which starts after Lemma 3 has put every bin at or under CAP. The insertion of Lemma 2, and the walks of a bin removal, also put a ball only into a bin with room. So (C) holds at the end. The fill phase ends with a sweep with no move, so (I) holds by Lemma 5. $\square$

**Theorem 2 (the loads depend only on the hashes and CAP).** Fix the bin points, the ball hashes and CAP. Any two assignments $S$ and $T$ that satisfy (C) and (I) give every bin the same load.

*Proof.* For a bin $j$, let $A_j$ be the number of balls with $\text{start} = j$, and $o(j)$ the number of balls that pass $j$. A ball whose walk contains $j$ either starts at $j$ or passes the bin before $j$. So with $r_j = A_j + o(j-1)$, the balls in $j$ and the balls that pass $j$ number $r_j$, and $\text{load}(j) + o(j) = r_j$. If $o(j) > 0$, then $j$ is full by (I), and $\text{load}(j) = \text{CAP}$ by (C). So in both cases

$$\text{load}(j) = \min(\text{CAP},\, r_j), \qquad o(j) = r_j - \text{load}(j),$$

and both values grow (weakly) with $o(j - 1)$.

If every bin in $S$ is full, then all loads in $S$ are CAP, the total is $m = n\,\text{CAP}$, and since every load in $T$ is at most CAP, all loads in $T$ are CAP too. Otherwise let $b_0$ be a bin with load less than CAP in $S$. By (I), $o_S(b_0) = 0 \le o_T(b_0)$. Go once around the ring from the bin after $b_0$ to $b_0$ itself. By the rule above and induction, $o_T(j) \ge o_S(j)$ and $\text{load}_T(j) \ge \text{load}_S(j)$ at every bin. Both assignments place all $m$ balls, so the loads have the same sum, and every inequality is an equality. $\square$

So the loads after a sequence of updates are the loads of inserting the final set of balls in any order, and the capacity bound $\lceil (1+\varepsilon) m / n \rceil$ holds for every bin at all times. The bound on the expected number of moves per update is Theorems 3 and 4 of Mirrokni, Thorup and Zadimoghaddam, which assume random hashes. $\blacksquare$
