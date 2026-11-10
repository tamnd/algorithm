---
title: The variant with bins of size 1 + ε uses at most OPT bins and moves a bounded amount per arrival, with a sketch of the main scheme
proves: [correctness, time.worst]
status: sketch
---

**Setting.** Items $s_1, s_2, \ldots \in (0, 1]$ arrive one at a time. After item $t$ arrives, $\mathrm{OPT}(t)$ is the least number of bins of size 1 that hold $s_1, \ldots, s_t$, and $S(t) = s_1 + \cdots + s_t$. Fix $0 < \varepsilon \le 1$ and put $\rho = 1 + \varepsilon/4$. The algorithm of the page uses bins of size $1 + \varepsilon$. An item is *large* if its size is at least $\varepsilon/4$ and *small* otherwise. A large item of size $s$ gets the rounded size $r(s)$, the least power $\rho^{-j}$ with $j \ge 0$ that is at least $s$; this value never changes. Let $c$ be the number of rounded sizes seen so far. A *pattern* is a multiset of rounded sizes with sum at most $1 + \varepsilon$, the empty one included, and $d$ is the number of patterns. The matrix $A$ has one row per rounded size, where the entry of pattern $p$ is how many items of that size $p$ holds, and one more row of ones. $\Delta$ is the largest absolute value of a square subdeterminant of $A$. The state is a vector $y$ that gives the number of bins of each pattern, so $A y = (u, B)$ with $u$ the vector of counts of the large items by rounded size and $B$ the number of bins.

The theorem for this variant has a full proof, except for the proximity theorem of integer programming, which is cited. The main scheme of the paper, with bins of size 1, is a sketch at the end.

**Invariant.** After each arrival: (I1) every item that has arrived is in exactly one bin; (I2) the rounded sizes of the large items of each bin form its pattern; (I3) the original sizes in each bin sum to at most $1 + \varepsilon$; (I4) the number of bins is at most $\mathrm{OPT}(t)$.

**Lemma 1 (rounding).** For $\varepsilon/4 \le s \le 1$, $s \le r(s) < \rho\, s$ and $r(s) \le 1$.

*Proof.* The value $1 = \rho^0$ is at least $s$, so the least such power exists and is at most 1. If $r(s) = \rho^{-j}$, then $\rho^{-j-1} < s$ by the choice of $j$, so $r(s) < \rho s$. $\square$

**Lemma 2 (the rounded items fit in OPT bins).** The rounded large items of $s_1, \ldots, s_t$ fit into $\mathrm{OPT}(t)$ bins of size $1 + \varepsilon$, with the large items of each bin forming a pattern.

*Proof.* Take an optimal packing into $\mathrm{OPT}(t)$ unit bins and drop the small items. By Lemma 1, a bin of load at most 1 has rounded load less than $\rho \le 1 + \varepsilon$. $\square$

**Lemma 3 (Any Fit opens a bin only when needed).** Suppose Any Fit, at line L1 or L6, opens a new bin for a small item $s$ when the packing has $k$ bins. Then $k + 1 \le \mathrm{OPT}(t)$.

*Proof.* Each of the $k$ bins has load greater than $1 + \varepsilon - s > 1 + 3\varepsilon/4 > 1$. They hold only items that have arrived, so $S(t) > k$. Each unit bin holds at most 1, so $\mathrm{OPT}(t) \ge S(t) > k$, and $\mathrm{OPT}(t) \ge k + 1$ as both are integers. $\square$

**Lemma 4 (a new bin for a large item only when needed).** If line L5 runs on arrival $t$ with $B$ bins, then $B + 1 \le \mathrm{OPT}(t)$.

*Proof.* Line L5 runs only when the rounded large items do not fit in $B$ bins as patterns. By Lemma 2, $\mathrm{OPT}(t) > B$. $\square$

**The proximity theorem (cited).** Let $A$ be an integer matrix with $d$ columns and largest absolute subdeterminant $\Delta$. If $y \ge 0$ is an integer solution of $A y = b$, and $A x = b'$ has an integer solution $x \ge 0$, then it has an integer solution $y' \ge 0$ with $\lVert y' - y \rVert_\infty \le d \Delta (\lVert b - b' \rVert_\infty + 2)$. This is the theorem of Cook, Gerards, Schrijver and Tardos (1986) in the form that Epstein and Levin quote from Schrijver's book (Corollary 17.2a there). We use it, but do not prove it here.

**Lemma 5 (line L4).** If line L4 runs, it finds $y'$ with $A y' = (u, B)$, $y' \ge 0$ and $\lVert y' - y \rVert_\infty \le 3 d \Delta$.

*Proof.* Before the arrival, $A y = (u - e_r, B)$, where $e_r$ is the unit vector of the new rounded size $r$; if $r$ is a new size, add a zero row for it and the new patterns as zero entries of $y$, which keeps $A y$ the same. Line L4 runs only when the rounded items fit in $B$ bins, so $A x = (u, B)$ has a solution $x \ge 0$ in integers; add empty patterns to reach exactly $B$ bins. The right sides differ by 1 in one entry, so the proximity theorem gives a solution within $d \Delta (1 + 2) = 3 d \Delta$. Line L4 searches all radii up to this bound, so it finds one. $\square$

**Lemma 6 (line L6 keeps the invariant).** After line L6, (I1) to (I3) hold and there are $B$ bins before the small items are put back.

*Proof.* Let $z_p = \min(y_p, y'_p)$. Line L6 keeps $z_p$ bins of each pattern $p$ and empties the others. The emptied bins hold large items with count vector $A(y - z)$ restricted to the size rows, and with the new item the pool has $A(y - z) + e_r = A y' - A z = A (y' - z)$, so the pool fills exactly $y'_p - z_p \ge 0$ new bins of each pattern $p$. The number of bins is $\sum_p y'_p = B$. Each new bin has a pattern, so (I2) holds, and its original load is at most its rounded load, at most $1 + \varepsilon$. Any Fit puts each small item of the emptied bins into a bin with room, so (I1) and (I3) hold. $\square$

**Theorem (the variant with bins of size 1 + ε).** After every arrival, (I1) to (I4) hold. On the arrival of a large item $s$, the items moved to another bin have total size at most $3 d^2 \Delta (1 + \varepsilon)$, at most $12 (1 + \varepsilon) d^2 \Delta / \varepsilon$ times $s$. A small item moves nothing.

*Proof.* By induction on $t$. A small item goes by Any Fit, which keeps (I1) to (I3); if it opens a bin, Lemma 3 gives (I4), and otherwise the count does not change and $\mathrm{OPT}(t - 1) \le \mathrm{OPT}(t)$. A large item goes to line L5, where Lemma 4 gives (I4) and the new bin has the pattern $(r)$ and load $s \le 1$, or to lines L4 and L6, where Lemmas 5 and 6 give (I1) to (I3) with $B \le \mathrm{OPT}(t)$ bins, and Lemma 3 covers the bins that Any Fit opens for the small items put back. Only the emptied bins lose items, and their number is $\sum_p (y_p - z_p) \le \sum_p \lvert y_p - y'_p \rvert \le d \cdot 3 d \Delta$. Each has load at most $1 + \varepsilon$, and $s \ge \varepsilon/4$. $\square$

**Running time.** By Lemma 1, a rounded size is $\rho^{-j} \ge s \ge \varepsilon/4$, so $0 \le j \le \log_\rho(4/\varepsilon)$ and $c \le 1 + \log_\rho(4/\varepsilon)$. A pattern holds at most $q = \lfloor 4(1 + \varepsilon)/\varepsilon \rfloor$ items, since each rounded size is at least $\varepsilon/4$, so $d \le \binom{c + q}{q}$. The entries of $A$ are at most $q$, so by Hadamard's inequality $\Delta \le (q \sqrt{c + 1})^{c + 1}$. Line L4 searches the box of radius $3 d \Delta$ around $y$, of at most $(6 d \Delta + 1)^d$ points, and the feasibility test is an integer program in $d$ variables, so Lenstra's algorithm decides it in time $f(\varepsilon)$ times a polynomial in $\log n$. Line L6 touches at most $3 d^2 \Delta$ bins, and Any Fit with a search tree over bin loads places an item in $O(\log n)$ time. So each arrival takes time $f(\varepsilon)$ times a polynomial in $\log n$; Epstein and Levin state a bound of $f(\varepsilon) \log n$ per arrival for their scheme. The code tests feasibility by a table over all count vectors and finds $y'$ by a search over the box, which is exponential in the counts and only meant for small checks.

**The main scheme (sketch).** With bins of size 1, Epstein and Levin call items of size less than $\varepsilon/2$ small and pack them by Any Fit, as above. The large items are kept in the groups of a revised form of the linear grouping of [Fernandez de la Vega and Lueker](/fernandez-de-la-vega-lueker-aptas/): with $m = 2/\varepsilon^2$, the large items are sorted and split into $M$ groups of equal size $K$, with $4m + 1 \le M \le 8m + 1$, and each group is rounded up to its largest item. The paper has three kinds of steps. In a regular step, the new item joins its group and the largest item of each group moves up to the next group, so the rounded instance changes in few entries. The other two steps create a new set of groups or join two sets, so that the number of groups stays in its range as the number of large items grows. In each case the rounded instance is the right side of a pattern program as above, the proximity theorem bounds the change of $y$, and the result is at most $(1 + \varepsilon)\,\mathrm{OPT}(t) + 1$ bins with migration factor bounded by a function of $1/\varepsilon$.
