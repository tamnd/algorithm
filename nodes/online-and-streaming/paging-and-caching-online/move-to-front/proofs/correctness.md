---
title: Move-to-front is (2 - 1/n)-competitive, and no deterministic rule beats 2n/(n + 1)
proves: [correctness]
status: full
---

**Model.** A list holds $n$ distinct items. An access to the item at position $i$ costs $i$. After an access, the item may move nearer the front with free exchanges. Any other swap of two adjacent items is a paid exchange of cost $1$. For an algorithm $A$ on a sequence $\sigma$ of $m$ requests, let $C_A$ be its total cost, $P_A$ its number of paid exchanges and $F_A$ its number of free exchanges. So $C_A$ is the sum of the access costs plus $P_A$.

**Theorem 1 (Sleator and Tarjan).** Let MTF and $A$ start from the same list. Then

$$\mathrm{MTF}(\sigma) \le 2 (C_A - P_A) + P_A - F_A - m \le 2\,C_A - m .$$

*Proof.* Let $\Phi$ be the number of inversions between the two lists: the number of unordered pairs $\{y, z\}$ of items that are in one order in the list of MTF and in the other order in the list of $A$. Then $\Phi \ge 0$, and $\Phi = 0$ at the start. For each request, let $A$ make its paid exchanges first, then let both algorithms access the item, then let MTF move it to the front, then let $A$ make its free exchanges.

*Paid exchanges of $A$.* One swap of adjacent items in the list of $A$ changes the order of exactly one pair, so $\Phi$ changes by $\pm 1$, and $A$ pays $1$. So these steps add at most $P_A$ to $\Phi$ in total.

*The access.* Let the request be $x$, at position $k$ in the list of MTF and at position $j$ in the list of $A$. Of the $k - 1$ items before $x$ in the list of MTF, let $v$ also be before $x$ in the list of $A$. Then $v \le j - 1$, and the other $k - 1 - v$ items are behind $x$ in the list of $A$. MTF pays $k$. When MTF moves $x$ to the front, only the pairs of $x$ with these $k - 1$ items change order. The $v$ items become inversions, and the $k - 1 - v$ items stop being inversions. So

$$k + \Delta\Phi = k + v - (k - 1 - v) = 2v + 1 \le 2j - 1 .$$

*Free exchanges of $A$.* Now $x$ is at the front of the list of MTF. A free exchange moves $x$ in front of an item $y$ in the list of $A$. The pair $\{x, y\}$ then has $x$ first in both lists, and it had $y$ first in the list of $A$ before. So each free exchange lowers $\Phi$ by $1$.

*Sum.* Let $j_t$ be the access cost of $A$ for request $t$. Adding all steps,

$$\mathrm{MTF}(\sigma) + \Phi_{\mathrm{end}} - \Phi_0 \le \sum_t (2 j_t - 1) + P_A - F_A = 2(C_A - P_A) - m + P_A - F_A .$$

With $\Phi_0 = 0$ and $\Phi_{\mathrm{end}} \ge 0$ this is the first bound. The second one follows from $P_A \ge 0$ and $F_A \ge 0$. $\square$

**Corollary 2.** $\mathrm{MTF}(\sigma) \le (2 - 1/n)\,\mathrm{OPT}(\sigma)$.

*Proof.* Take $A$ optimal in Theorem 1, so $\mathrm{MTF}(\sigma) \le 2\,\mathrm{OPT}(\sigma) - m$. The rule that never moves an item pays at most $n$ per access, so $\mathrm{OPT}(\sigma) \le nm$, that is $m \ge \mathrm{OPT}(\sigma)/n$. $\square$

**Corollary 3 (static lists).** Let $S$ be the access cost of serving $\sigma$ from a fixed list $L^*$, and let $\mathrm{inv}(L_0, L^*)$ be the number of inversions between the start list $L_0$ and $L^*$. Then $\mathrm{MTF}(\sigma) \le 2S + \mathrm{inv}(L_0, L^*) - m$.

*Proof.* Let $A$ first sort $L_0$ into $L^*$ with $\mathrm{inv}(L_0, L^*)$ paid exchanges (bubble sort uses exactly this many swaps), and then never move. Then $C_A - P_A = S$, $P_A = \mathrm{inv}(L_0, L^*)$ and $F_A = 0$, and the first bound of Theorem 1 gives the claim. $\square$

The best fixed list sorts the items by decreasing number of requests: if $y$ is requested more often than $z$ but $z$ is before $y$, then swapping them in $L^*$ lowers $S$.

**Theorem 4 (lower bound).** For each deterministic online algorithm ALG, each $n \ge 1$ and each $c < 2n/(n+1)$, there is no constant $b$ with $\mathrm{ALG}(\sigma) \le c \cdot \mathrm{OPT}(\sigma) + b$ for all $\sigma$.

*Proof.* The adversary always requests the item that is last in the list of ALG just before the request. To serve it, ALG must bring it to the front of its scan: if paid exchanges move it forward by $d$ places, it pays $d$ for them and $n - d$ for the access. So ALG pays at least $n$ per request, and $\mathrm{ALG}(\sigma) \ge nm$.

For the optimum, consider the $n!$ algorithms that first sort the start list into a fixed list $L^*$, with at most $\binom{n}{2}$ paid exchanges, and then never move. Over all $L^*$, each item is at each position equally often, so the average access cost is $(n+1)/2$ per request. So some $L^*$ has total cost at most $m(n+1)/2 + n(n-1)/2$, and

$$\frac{\mathrm{ALG}(\sigma)}{\mathrm{OPT}(\sigma)} \ge \frac{nm}{m(n+1)/2 + n(n-1)/2} \to \frac{2n}{n+1} \quad (m \to \infty).$$

If $\mathrm{ALG}(\sigma) \le c \cdot \mathrm{OPT}(\sigma) + b$ held for all $\sigma$, then $nm \le c\,(m(n+1)/2 + n(n-1)/2) + b$ for all $m$, which fails for large $m$ when $c < 2n/(n+1)$. $\blacksquare$

The tests check Theorem 1 against an exact offline optimum with paid and free exchanges for lists of up to four items, check Corollary 3 against every fixed list of up to five items, and reproduce the sequence of Theorem 4.
