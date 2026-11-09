---
title: The region graph decides location reachability for timed automata
proves: [correctness, termination, complexity]
status: full
---

**Setting.** $A$ is a diagonal-free timed automaton with clocks $x_1, \ldots, x_n$, locations $L$, initial location $\ell_0$ and edges $(\ell, g, Y, \ell')$. Guards are conjunctions of atomic constraints $x \sim c$ with $\sim \in \{<, \le, =, \ge, >\}$ and $c \in \mathbb{N}$. Invariants are conjunctions of constraints $x < c$ or $x \le c$. The constant $c_x$ is the largest constant compared with $x$, or 0. A state is $(\ell, v)$ with $v$ a valuation that satisfies $\mathrm{Inv}(\ell)$. The initial state is $(\ell_0, \mathbf{0})$, and we assume $\mathbf{0}$ satisfies $\mathrm{Inv}(\ell_0)$. The steps are:

- a delay $(\ell, v) \to (\ell, v + d)$ for $d \ge 0$ when $v + d$ satisfies $\mathrm{Inv}(\ell)$;
- an action $(\ell, v) \to (\ell', v[Y := 0])$ for an edge $(\ell, g, Y, \ell')$ when $v$ satisfies $g$ and $v[Y := 0]$ satisfies $\mathrm{Inv}(\ell')$.

Region equivalence $\cong$, the code $(\mathit{ints}, \mathit{zero}, \mathit{order})$ and the region graph are as defined on the page. Clock $x$ is bounded in $v$ when $v(x) \le c_x$.

**Fact 1.** If $v + t$ satisfies $\mathrm{Inv}(\ell)$, then $v + s$ satisfies it for all $0 \le s \le t$.

*Proof.* Each atomic invariant is $x < c$ or $x \le c$, and $(v + s)(x) \le (v + t)(x)$. $\square$

**Lemma 1 (codes).** The map that sends $v$ to its code is constant on each region. It maps different regions to different codes, and every code of the stated shape is the code of some valuation.

*Proof.* The code of $v$ is defined from the three quantities that the definition of $\cong$ compares. Condition 1 fixes $\mathit{ints}$, and it also fixes which clocks are bounded. Condition 2 fixes $\mathit{zero}$. Condition 3 fixes the preorder of the fractional parts on the other bounded clocks, which is the same as the ordered list of sets in $\mathit{order}$. So $v \cong v'$ if and only if $v$ and $v'$ have the same code. Given a code, let $m$ be the number of sets in $\mathit{order}$. Set $v(x) = \mathit{ints}[x]$ for $x \in \mathit{zero}$, set $v(x) = \mathit{ints}[x] + k/(m + 1)$ for $x$ in the $k$-th set, and set $v(x) = c_x + 1$ for the clocks above their constants. This $v$ has the given code. $\square$

**Lemma 2 (constraints).** If $v \cong v'$ and $c \le c_x$, then $v$ satisfies $x \sim c$ if and only if $v'$ does. SATISFIES returns this common answer.

*Proof.* Let $t = v(x)$. If $t > c_x$, then $t > c$, so $x \sim c$ holds exactly when $\sim$ is $>$ or $\ge$. This depends only on the code, and it is line S1. If $t$ is an integer $i \le c_x$, the truth of $i \sim c$ depends only on $i = \mathit{ints}[x]$, which is line S2. If $i < t < i + 1$ with $i \le c_x$, then because $c$ is an integer, $t \sim c$ has the same truth as $i + 1/2 \sim c$, which is line S3. In each case the answer depends only on the code, so it is the same for $v'$ by Lemma 1. $\square$

**Lemma 3 (reset).** If $v \cong v'$, then $v[Y := 0] \cong v'[Y := 0]$. The code of $v[Y := 0]$ is RESET applied to the code of $v$.

*Proof.* After the reset, the clocks in $Y$ have value 0. Each of them is bounded, with integer part 0 and a zero fractional part. The other clocks keep their values. So $\mathit{ints}[x]$ becomes 0 for $x \in Y$, $Y$ joins $\mathit{zero}$, and $Y$ leaves the sets of $\mathit{order}$. The relative order of the fractional parts of the clocks outside $Y$ does not change. Sets that become empty are dropped, because the preorder has no empty classes. The result depends only on the code of $v$ and on $Y$. By Lemma 1, $v'[Y := 0]$ has the same code. $\square$

**Lemma 4 (time).** Let $v$ have code $r$, and suppose some clock is bounded in $v$. Then there is a $\delta > 0$ such that:

- every $v + s$ with $0 < s < \delta$ has code $\mathrm{succ}(r)$ when $r$ has a zero fractional part on some bounded clock;
- otherwise every $v + s$ with $0 \le s < \delta$ has code $r$, and $v + \delta$ has code $\mathrm{succ}(r)$.

Here $\mathrm{succ}(r)$ is the output of TIME-SUCC on $r$. If no clock is bounded in $v$, then every $v + s$ has code $r$, and TIME-SUCC returns none.

*Proof.* Clocks above their constants stay above them, so their part of the code never changes.

*Case 1: $\mathit{zero} \ne \emptyset$.* Let $f$ be the largest fractional part of a bounded clock, which is less than 1. Take $\delta = 1 - f$ if some bounded clock has a nonzero fractional part, and $\delta = 1$ otherwise. For $0 < s < \delta$, look at each clock of $\mathit{zero}$ with value $i$. If $i = c_x$, then $v(x) + s > c_x$, and the clock is above its constant. This is line L3. If $i < c_x$, then $i < v(x) + s < i + 1 \le c_x$, so the clock stays bounded, keeps its integer part, and has fractional part $s$. A bounded clock $y$ outside $\mathit{zero}$ has $\mathrm{fr}(v(y)) + s < f + \delta \le 1$. So it keeps its integer part, and its fractional part grows by $s$. This also shows it stays bounded, because $\lfloor v(y) \rfloor < c_y$ when $v(y)$ is not an integer and $v(y) \le c_y$. Since $0 < s < \mathrm{fr}(v(y)) + s$, the clocks that were in $\mathit{zero}$ and stay bounded share the smallest fractional part, $s$. The order of the others is kept. No bounded clock has a zero fractional part. This is the code built by lines L4 and L5, and it does not depend on $s$.

*Case 2: $\mathit{zero} = \emptyset$ and $\mathit{order}$ is not empty.* Let $f$ be the largest fractional part, which belongs to the clocks of the last set $S$, and let $\delta = 1 - f > 0$. For $0 \le s < \delta$, every bounded clock keeps its integer part, and its fractional part grows by $s$ and stays in $(0, 1)$. So the code stays $r$. At $s = \delta$, each clock of $S$ reaches $\lfloor v(x) \rfloor + 1$, which is still at most $c_x$, as shown in Case 1. The other bounded clocks have fractional parts in $(\delta, 1)$, so they keep their integer parts and their order. So $v + \delta$ has the code from line L9: $S$ gets integer parts one higher and forms $\mathit{zero}$, and $S$ leaves $\mathit{order}$.

*Case 3: no clock is bounded.* Then $\mathit{zero}$ and $\mathit{order}$ are empty. All clocks stay above their constants, so the code never changes. Line L6 returns none. $\square$

**Corollary 1.** As $s$ goes from 0 to $\infty$, the code of $v + s$ goes through $r, \mathrm{succ}(r), \mathrm{succ}^2(r), \ldots$ in this order. It skips none, and it ends in the code where every clock is above its constant. That code is reached at a finite time.

*Proof.* Apply Lemma 4 again at each point where the code changes. A step of Case 1 is followed by a step of Case 2 or Case 3. Each step of Case 2 moves some clock to a higher integer. A clock can do this at most $c_x + 1$ times before Case 1 moves it above its constant. So after finitely many steps no clock is bounded. The time at which each code begins depends only on $v$, and it increases with each step. $\square$

**Theorem 1 (soundness).** If $(\ell, r)$ is reachable in the region graph, then some state $(\ell, v)$ with $v \in r$ is reachable in $A$.

*Proof.* We use induction on the length of a path from $(\ell_0, r_0)$, where $r_0$ is the region of $\mathbf{0}$. The base case is the state $(\ell_0, \mathbf{0})$. For the step, suppose $(\ell, v)$ is reachable with $v \in r$.

- *Delay edge* to $(\ell, \mathrm{succ}(r))$. By Lemma 4 there is a $d > 0$ with $v + d \in \mathrm{succ}(r)$. The edge exists only when $\mathrm{succ}(r)$ satisfies $\mathrm{Inv}(\ell)$, so by Lemma 2 $v + d$ satisfies it. So the delay $d$ is a step of $A$.
- *Action edge* for $(\ell, g, Y, \ell')$. The region $r$ satisfies $g$, so $v$ satisfies $g$ by Lemma 2. Also $v[Y := 0] \in r[Y := 0]$ by Lemma 3, and that region satisfies $\mathrm{Inv}(\ell')$. So the action is a step of $A$.

In both cases the new state of $A$ lies in the new region. $\square$

**Theorem 2 (completeness).** If $(\ell, v)$ is reachable in $A$, then $(\ell, [v])$ is reachable in the region graph, where $[v]$ is the region of $v$.

*Proof.* We use induction on the number of steps. The base case is $(\ell_0, [\mathbf{0}])$, which is the start node. For an action step, $v$ satisfies $g$ and $v[Y := 0]$ satisfies $\mathrm{Inv}(\ell')$. By Lemmas 2 and 3, $[v]$ satisfies $g$ and $[v[Y := 0]] = [v][Y := 0]$ satisfies $\mathrm{Inv}(\ell')$. So there is an action edge from $(\ell, [v])$ to $(\ell', [v[Y := 0]])$.

For a delay step $(\ell, v) \to (\ell, v + d)$, Corollary 1 says the regions of $v + s$ for $0 \le s \le d$ are $[v], \mathrm{succ}([v]), \ldots, \mathrm{succ}^k([v]) = [v + d]$ for some $k$. Each of them contains some $v + s$ with $s \le d$. That valuation satisfies $\mathrm{Inv}(\ell)$ by Fact 1, so the region satisfies it by Lemma 2. Hence the delay edges $(\ell, \mathrm{succ}^{j}([v])) \to (\ell, \mathrm{succ}^{j+1}([v]))$ exist for $j < k$. $\square$

**Corollary 2.** A location $\ell$ is reachable in $A$ if and only if REGION-REACH returns a node $(\ell, r)$ for some $r$.

*Proof.* REGION-REACH is a graph search from the start node that follows exactly the delay and action edges. The edges are computed by TIME-SUCC, SATISFIES and RESET, which are correct by Lemmas 2 to 4. So it returns exactly the reachable nodes. Theorems 1 and 2 finish the proof. $\square$

**Theorem 3 (number of regions).** The number of regions is at most $n! \, 2^{n-1} \prod_x (2 c_x + 2)$ for $n \ge 1$. For $n = 1$ it is exactly $2 c_x + 2$.

*Proof.* By Lemma 1 we count codes. For each clock $x$, choose one of three kinds: an integer value in $\{0, \ldots, c_x\}$, an open interval $(i, i + 1)$ with $0 \le i < c_x$, or "above $c_x$". That is $2 c_x + 2$ choices. The choices fix $\mathit{ints}$ and $\mathit{zero}$, and they fix the set $F$ of clocks in open intervals. The rest of the code is an ordered partition of $F$ into nonempty sets. Write the sets in order, and list the elements of each set in increasing index. This gives a permutation of $F$. To get the partition back, we also need to know, for each of the $|F| - 1$ adjacent pairs in the permutation, whether a new set starts between them. So there are at most $|F|! \, 2^{|F| - 1} \le n! \, 2^{n-1}$ ordered partitions when $F$ is not empty, and one when it is empty. Multiplying gives the bound. For $n = 1$, $F$ has at most one element and there is one ordered partition, so the count is exactly $2 c_x + 2$. $\square$

**Theorem 4 (termination and cost).** REGION-REACH terminates. It visits at most $|L|$ times the bound of Theorem 3 nodes, and it runs in $O(r (|L| + |E|) n)$ time when each guard and invariant has $O(n)$ atomic constraints and the edges are indexed by source location.

*Proof.* Each node enters the stack at most once, because it is added to the set of seen nodes at the same time. There are finitely many nodes, by Theorem 3. For each popped node $(\ell, r)$, TIME-SUCC takes $O(n)$ time. Each edge from $\ell$ takes $O(n)$ time for SATISFIES, RESET and the invariant test. Summed over the regions, the edges from all locations give $O(r |E| n)$, and the time successors give $O(r |L| n)$. Hashing a code of $O(n)$ words takes $O(n)$ expected time. $\blacksquare$
