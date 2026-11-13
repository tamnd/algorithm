---
title: MM returns a cheapest path with admissible heuristics, and expands no state beyond the middle
proves: [correctness]
status: full
---

We use the pseudocode of the page. Each action cost is positive and at least $\epsilon \ge 0$, each state has finitely many successors and predecessors, $h_F(u)$ is at most the cost of a cheapest path from $u$ to $t$, and $h_B(u)$ is at most the cost of a cheapest path from $s$ to $u$. We write $d(u, v)$ for the cost of a cheapest path from $u$ to $v$, and $C^* = d(s, t)$ when $t$ can be reached. In the backward direction, an action of $n$ is a pair $(m, c)$ with an action of cost $c$ from $m$ to $n$. A state has a value in direction $D$ once $g_D$ is set for it.

**Fact 1 (real paths).** For each state $u$ with a value, $g_F(u)$ is the cost of a path from $s$ to $u$ and $g_B(u)$ the cost of a path from $u$ to $t$, so $g_F(u) \ge d(s, u)$ and $g_B(u) \ge d(u, t)$. These values never rise. The forward parents lead from $u$ back to $s$ along a path of cost at most $g_F(u)$, and the backward parents lead from $u$ to $t$ along a path of cost at most $g_B(u)$.

*Proof.* Line L1 sets $g_F(s) = 0$ and $g_B(t) = 0$, and line L11 sets $g_D(m) = g_D(n) + c$ for an action between $n$ and $m$, so by induction each value is the cost of a path. Line L9 lets line L11 change a value only to a smaller one. When the parent of $m$ is set to $n$, $g_D(m) > g_D(n)$, and this stays true, since $g_D(n)$ can only fall and a new value of $g_D(m)$ comes with a new parent. So the parents strictly lower $g_D$ and end at the root of the direction, whose value 0 never changes, since a new value would be positive. By induction along the parents, the path costs at most $g_D(u)$. $\square$

**Fact 2 (open and closed).** In each direction, a state with a value is in exactly one of $\mathrm{OPEN}_D$ and $\mathrm{CLOSED}_D$. It is in $\mathrm{CLOSED}_D$ if and only if it has been expanded in direction $D$ since its value $g_D$ was last set.

*Proof.* Line L1 puts each root in its open list. Line L7 moves the expanded state from OPEN to CLOSED, and lines L10 and L11 take a state out of both and put it in OPEN when its value is set. $\square$

**Lemma 3 (the bound U).** At each moment, $U$ is $\infty$ or the cost of a path from $s$ to $t$, so $U \ge C^*$. Also $U \le g_F(x) + g_B(x)$ for every state $x$ with a value in both directions.

*Proof.* Line L2 sets $U = 0$ if $s = t$, which is the cost of the empty path, and $U = \infty$ otherwise. Then the only state that could have both values is $s = t$, with the sum 0. Line L12 sets $U$ to $g_F(m) + g_B(m)$, which by Fact 1 is the cost of a path from $s$ to $m$ and then from $m$ to $t$. A value changes only at line L11, and line L12 then compares the new sum for $m$ with $U$. The sums of the other states do not change, and $U$ only falls. So the second claim holds after each step. $\square$

Now let $t$ be reachable from $s$, and let $P = (p_0, \ldots, p_k)$ be a cheapest path from $s = p_0$ to $t = p_k$. Write $a_l = d(s, p_l)$. Since the prefixes and suffixes of $P$ are cheapest paths, $d(p_l, t) = C^* - a_l$, and $a_l$ rises along $P$ by at least $\epsilon$ at each action. Call $p_l$ *forward done* if $g_F(p_l) = a_l$ and $p_l$ is in $\mathrm{CLOSED}_F$, and *backward done* if $g_B(p_l) = C^* - a_l$ and $p_l$ is in $\mathrm{CLOSED}_B$. By Facts 1 and 2, a state that is forward done stays forward done: its value cannot fall below $a_l$, so it is never set again. The same holds backward.

**Lemma 4 (the frontier on P).** Let $i$ be the least index such that $p_i$ is not forward done, or $i = k + 1$ if there is none. If $i \le k$, then $g_F(p_i) = a_i$ and $p_i$ is in $\mathrm{OPEN}_F$. In the same way, let $j$ be the largest index such that $p_j$ is not backward done, or $j = -1$ if there is none. If $j \ge 0$, then $g_B(p_j) = C^* - a_j$ and $p_j$ is in $\mathrm{OPEN}_B$.

*Proof.* If $i = 0$, then $g_F(s) = 0 = a_0$ by Fact 1. If $i > 0$, then $p_{i-1}$ was expanded with $g_F(p_{i-1}) = a_{i-1}$, and at that expansion line L9 found $g_F(p_i) \le a_{i-1} + c = a_i$ or line L11 set it to $a_i$. By Fact 1 the value is $a_i$ from then on. So $p_i$ has the value $a_i$. It is not forward done, so by Fact 2 it is not in $\mathrm{CLOSED}_F$ and so it is in $\mathrm{OPEN}_F$. The backward claim is the same argument from $p_k$ toward $p_0$. $\square$

**Lemma 5 (a good pair).** If $t$ is reachable and $U > C^*$ at the start of a pass of the loop, then $i < j$, both open lists are not empty, and $C$, $\mathit{fmin}_F$, $\mathit{fmin}_B$ and $\mathit{gmin}_F + \mathit{gmin}_B + \epsilon$ are all at most $C^*$.

*Proof.* First we show that $i < j$. If $i > j$, take $x = p_{i-1}$ when $i - 1 > j$: it is forward done because $i - 1 < i$ and backward done because $i - 1 > j$. When $i = j + 1$, take $x = p_i$ if $i \le k$: it has $g_F = a_i$ by Lemma 4 and is backward done because $i > j$. If $i = k + 1 = j + 1$, take $x = t$, which is forward done and has $g_B(t) = 0 = C^* - a_k$. If $i = j$, take $x = p_i$, which has both values by Lemma 4. In each case $x = p_l$ has $g_F(x) = a_l$ and $g_B(x) = C^* - a_l$, so Lemma 3 gives $U \le C^*$, which is false. So $i < j$, and then $0 \le i < j \le k$.

By Lemma 4, $p_i$ is in $\mathrm{OPEN}_F$ with $g_F = a_i$ and $p_j$ is in $\mathrm{OPEN}_B$ with $g_B = C^* - a_j$. Then:

- $\mathit{fmin}_F \le a_i + h_F(p_i) \le a_i + (C^* - a_i) = C^*$, and $\mathit{fmin}_B \le (C^* - a_j) + h_B(p_j) \le (C^* - a_j) + a_j = C^*$.
- $\mathit{gmin}_F + \mathit{gmin}_B + \epsilon \le a_i + C^* - a_j + \epsilon \le C^*$, since the part of $P$ from $p_i$ to $p_j$ has at least one action, so $a_j - a_i \ge \epsilon$.
- If $a_i \le C^*/2$, then $pr_F(p_i) = \max(a_i + h_F(p_i), 2 a_i) \le C^*$. Otherwise $a_j \ge a_i > C^*/2$, so $2(C^* - a_j) < C^*$ and $pr_B(p_j) \le C^*$. In both cases $C \le C^*$. $\square$

**Theorem 6 (optimality).** If $t$ is reachable from $s$ and MM ends, it returns a path from $s$ to $t$ of cost $C^*$.

*Proof.* While $U > C^*$, Lemma 5 says that both open lists are not empty and that the bound of line L5 is at most $C^* < U$, so the loop goes on. So when the loop ends, $U \le C^*$, and by Lemma 3, $U = C^*$. Then line L14 runs. MEET is the state of the last change of $U$, so $U = g_F(\text{MEET}) + g_B(\text{MEET})$ at that moment, and both values can only have fallen since. By Fact 1, the forward parents give a path from $s$ to MEET and the backward parents a path from MEET to $t$, of total cost at most $U = C^*$. No path from $s$ to $t$ costs less than $C^*$, so this path costs $C^*$. $\square$

**Theorem 7 (meeting in the middle).** If $t$ is reachable, each state $n$ that MM expands in direction $D$ has $pr_D(n) \le C^*$, so $g_D(n) \le C^*/2$ and $f_D(n) \le C^*$.

*Proof.* At line L6, $pr_D(n) = C$. If $U > C^*$, Lemma 5 gives $C \le C^*$. If $U \le C^*$, the loop did not stop at line L5, so $C < U \le C^*$. The bounds on $g_D$ and $f_D$ follow from $pr_D = \max(f_D, 2 g_D)$. $\square$

**Theorem 8 (termination and failure).** On a finite graph, MM ends. It returns failure only if $t$ cannot be reached from $s$.

*Proof.* Let $\delta > 0$ be the least action cost. Each value $g_D(u)$ is the cost of a path and only falls from the first value $g_0$ that it gets. A path of cost at most $g_0$ has at most $g_0 / \delta$ actions, so there are finitely many such paths, and $g_D(u)$ changes finitely often. By Fact 2, a state is expanded in direction $D$ at most once for each value of $g_D$. So there are finitely many expansions, and since each pass of the loop either expands a state or leaves the loop, MM ends. If $t$ is reachable, Theorem 6 shows that MM returns a path. If $t$ is not reachable, Lemma 3 says that $U = \infty$ at all times, and MM returns failure at line L13. $\square$

**Remark.** The paper updates $U$ only when the generated state is in the other open list. The proof above uses the test at line L12 against every state with a value in the other direction, which gives the second claim of Lemma 3 at all times. The choice of the direction and of $n$ among the states of priority $C$ plays no part in the proof, so any rule for ties gives the same guarantees.
