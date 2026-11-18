---
title: The HRU greedy algorithm gets at least 1 - (1 - 1/k)^k of the best benefit of k views, and greedy by benefit per unit space gets at least 1 - 1/e of the best benefit in the space it uses
proves: [correctness]
status: full
---

**Setting.** A finite set $V$ of views has a top view $t$ and a relation $w \preceq v$ ("$w$ can be answered from $v$"), which is reflexive, transitive, and has $w \preceq t$ for every $w$. Each view has a size $|v| > 0$ and each query $w$ a weight $q_w \ge 0$ (1 in the plain model). For a set $S$ of views with $t \in S$, the cost of $w$ is $C_S(w) = \min\{|u| : u \in S,\ w \preceq u\}$, which exists because $t \in S$. The total cost is $T(S) = \sum_w q_w C_S(w)$. For a set $X$ of views, the benefit is $f(X) = T(\{t\}) - T(\{t\} \cup X)$. The benefit of a view $v$ for $S$ is

$$B(v, S) = \sum_{w \preceq v} q_w \max\big(0,\ C_S(w) - |v|\big).$$

Line L3 computes this value, and lines L4 and L5 add a view with the largest one.

**Lemma 1 (benefit is the gain).** For $t \in S$, $T(S) - T(S \cup \{v\}) = B(v, S)$.

*Proof.* Adding $v$ changes only the costs of the views $w \preceq v$, and for such $w$ the new cost is $\min(C_S(w), |v|)$. The drop is $\max(0, C_S(w) - |v|)$, and the total drop is the weighted sum of these. $\square$

So, for $S = \{t\} \cup X$, $f(X \cup \{v\}) - f(X) = B(v, \{t\} \cup X)$, and the sum of the gains that line L4 records is the benefit of the chosen set.

**Lemma 2 (monotone and submodular).** If $S \subseteq S'$, then $C_{S'}(w) \le C_S(w)$ for every $w$, $B(v, S') \le B(v, S)$ for every $v$, and $f$ is monotone.

*Proof.* A minimum over a larger set is not larger. Each term $\max(0, C(w) - |v|)$ is a nondecreasing function of $C(w)$, so the benefit cannot grow when $S$ grows. Monotonicity follows from Lemma 1, because each benefit is at least 0. $\square$

Lemma 2 says that $f$ is a monotone [submodular function](/submodular-function/): the gain of a view never grows when other views are added.

**Lemma 3 (gain of a set).** For $t \in S$ and any set $Y$ of views, $T(S) - T(S \cup Y) \le \sum_{y \in Y} B(y, S)$.

*Proof.* Add the views of $Y$ one at a time, $y_1, \ldots, y_m$. By Lemma 1, the drop in step $i$ is $B(y_i, S \cup \{y_1, \ldots, y_{i-1}\})$, which is at most $B(y_i, S)$ by Lemma 2. Sum over $i$. $\square$

**Theorem 1 (fixed number of views).** Let the greedy algorithm choose $k$ views with total benefit $B_{greedy}$, and let $B_{opt}$ be the largest benefit of any $k$ views. Then $B_{greedy} \ge \big(1 - (1 - 1/k)^k\big) B_{opt} > (1 - 1/e)\,B_{opt}$.

*Proof.* Let $O$ be an optimal set of $k$ views, $G_i$ the set after $i$ choices, $b_{i+1}$ the benefit of choice $i+1$, and $g_i = B_{opt} - f(G_i)$. Every view of $O$ is either in $G_i$, where its benefit for $\{t\} \cup G_i$ is 0, or a candidate of line L4, whose benefit is at most $b_{i+1}$. By monotonicity and Lemma 3,

$$B_{opt} = f(O) \le f(G_i \cup O) \le f(G_i) + \sum_{o \in O} B(o, \{t\} \cup G_i) \le f(G_i) + k\, b_{i+1}.$$

So $g_i \le k\, b_{i+1} = k (g_i - g_{i+1})$, that is, $g_{i+1} \le (1 - 1/k)\, g_i$. With $g_0 = B_{opt}$, this gives $g_k \le (1 - 1/k)^k B_{opt}$ and $f(G_k) \ge (1 - (1 - 1/k)^k) B_{opt}$. Finally $1 - x < e^{-x}$ for $x > 0$, so $(1 - 1/k)^k < e^{-1}$. $\blacksquare$

If fewer than $k$ views besides $t$ exist, the greedy algorithm stores them all and is optimal. For $k = 1$ the bound is 1: the first choice is the best single view.

**Tightness for $k = 2$.** In Example 4.2 of the paper, the top view $a$ has size 200, three views $b$, $c$ and $d$ below it have sizes 100, 99 and 100, and four chains of 20 views of size 100 hang below them: $b$ answers chains 1 and 2, $c$ chains 2 and 3, and $d$ chains 3 and 4. Greedy first takes $c$, with benefit $41 \cdot 101 = 4141$, and then $b$ or $d$, with benefit $21 \cdot 100 = 2100$, so $B_{greedy} = 6241$. The set $\{b, d\}$ improves 82 views by 100 each, so $B_{opt} = 8200$, and the ratio is about 0.761. With the size of $c$ closer to 100 and chains of $L$ views, the ratio is $\frac{(2L+1)\cdot 100 + (L+1)\cdot 100}{(4L+2)\cdot 100} \to 3/4 = 1 - (1 - 1/2)^2$.

**Theorem 2 (benefit per unit space).** Run greedy with the rule "add the view with the largest $B(v, S)/|v|$" and stop at any step. Let $G$ be the chosen views, $s = \sum_{v \in G} |v|$ their space, and $B^*$ the largest benefit of any set of views of total size at most $s$. Then $f(G) \ge (1 - 1/e)\,B^*$.

*Proof.* Let $O$ be a set of size at most $s$ with benefit $B^*$, and $\sigma = \sum_{o \in O} |o| \le s$; if $B^* = 0$ there is nothing to prove, so $\sigma > 0$. Let $v_1, \ldots, v_m$ be the chosen views with sizes $c_i$ and gains $b_i$, $G_i$ the first $i$ of them, and $g_i = B^* - f(G_i)$. Each view $o \in O$ has $B(o, \{t\} \cup G_{i-1}) \le |o|\, b_i / c_i$, because $v_i$ has the largest ratio, or because the benefit of $o$ is 0. By Lemma 3,

$$B^* \le f(G_{i-1}) + \sum_{o \in O} |o|\,\frac{b_i}{c_i} = f(G_{i-1}) + \sigma\,\frac{b_i}{c_i},$$

so $g_{i-1} \le \frac{\sigma}{c_i}(g_{i-1} - g_i)$, that is, $g_i \le (1 - c_i/\sigma)\, g_{i-1}$. If some $c_i \ge \sigma$, then $g_i \le 0$, and $g$ stays at most 0 because $f$ is monotone. Otherwise every factor is in $[0, 1)$, and with $1 - x \le e^{-x}$,

$$g_m \le B^* \prod_{i=1}^{m} \Big(1 - \frac{c_i}{\sigma}\Big) \le B^* e^{-s/\sigma} \le B^* e^{-1},$$

because $s \ge \sigma$. So $f(G) \ge (1 - 1/e) B^*$. $\blacksquare$

This is the form of the second theorem of Harinarayan, Rajaraman and Ullman: the comparison is with the best use of the space that greedy actually used. Against a fixed limit $L$ the bound does not hold if greedy skips a view that does not fit. With a view of size 1 and benefit 2 and a view of size $L$ and benefit $1.9L$, greedy takes the small view first and then has no room, so it gets 2 while the best choice gets $1.9L$.

**Work.** Precompute, for each view, the set of views below it; with $n$ views this takes $O(n^2)$ space. Keep $C_S(w)$ for every $w$. Line L3 then costs $O(|\{w \preceq v\}|) = O(n)$ per view and $O(n^2)$ per round, and the update after line L5 costs $O(n)$. With $k$ rounds the time is $O(k n^2)$. For the cube on $d$ dimensions, $n = 2^d$ and the views below the view on a set $A$ are the $2^{|A|}$ subsets of $A$, so a round costs $\sum_A 2^{|A|} = 3^d$.
