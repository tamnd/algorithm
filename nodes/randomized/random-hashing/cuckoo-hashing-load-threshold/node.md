---
tag: 9GW344
kind: theorem
slug: cuckoo-hashing-load-threshold
name: Cuckoo hashing load threshold
aliases:
- 50 percent load threshold for cuckoo hashing
- cuckoo graph threshold
- orientability threshold for cuckoo hashing
area: randomized/random-hashing
level: advanced
summary: Two-choice cuckoo hashing succeeds with high probability only while the load factor stays below one half.
prereqs: [cuckoo-hashing, erdos-renyi-giant-component-theorem, linearity-of-expectation, azuma-inequality]
see_also: [cuckoo-hashing, cuckoo-filter, k-independent-hashing, tabulation-hashing, power-of-two-choices, bipartite-matching, giant-component, load-factor]
sources:
  - paper: doi:10.1016/j.jalgor.2003.12.002
    title: Rasmus Pagh and Flemming Friche Rodler, Cuckoo hashing, Journal of Algorithms 51(2), 122 to 144, 2004
    locator: the analysis of the cuckoo graph (the probability that a rehash is needed is O(1/n) when each table has at least (1 + ε)n cells)
  - paper: doi:10.1137/080728743
    title: Adam Kirsch, Michael Mitzenmacher and Udi Wieder, More robust hashing, cuckoo hashing with a stash, SIAM Journal on Computing 39(4), 1543 to 1561, 2009
    locator: the main theorem on the failure probability with a stash of constant size s
  - paper: doi:10.1007/978-3-642-14165-2_19
    title: Martin Dietzfelbinger, Andreas Goerdt, Michael Mitzenmacher, Andrea Montanari, Rasmus Pagh and Michael Rink, Tight thresholds for cuckoo hashing via XORSAT, ICALP 2010, Lecture Notes in Computer Science 6198, 213 to 225
    locator: the load thresholds for k hash functions and one key per cell, k at least 3
  - paper: doi:10.1002/rsa.20426
    title: Nikolaos Fountoulakis and Konstantinos Panagiotou, Sharp load thresholds for cuckoo hashing, Random Structures and Algorithms 41(3), 2012
    locator: the critical load for each number k of hash functions, k at least 3
  - paper: doi:10.1007/s00224-004-1195-x
    title: Dimitris Fotakis, Rasmus Pagh, Peter Sanders and Paul Spirakis, Space efficient hash tables with worst case constant access time, Theory of Computing Systems 38, 229 to 248, 2005
    locator: d-ary cuckoo hashing and the number of hash functions needed for load 1 - ε
---

## Statement

Cuckoo hashing with two choices stores $n$ keys in two tables $T_1$ and $T_2$ of $r$ cells each, one key per cell, key $x$ in $T_1[h_1(x)]$ or in $T_2[h_2(x)]$. The *load* is $n/(2r)$, the fraction of the $2r$ cells in use. The *cuckoo graph* is the bipartite multigraph with the $2r$ cells as vertices and one edge $\{T_1[h_1(x)], T_2[h_2(x)]\}$ for each key $x$. Assume that $h_1$ and $h_2$ are fully random and independent.

**Theorem.**

1. *(Placement.)* The $n$ keys can be stored, each in one of its two cells, if and only if every connected component of the cuckoo graph has at most as many edges as vertices.
2. *(Below load 1/2, Pagh and Rodler 2004.)* Let $q = n/r < 1$, so the load is $q/2 < 1/2$. The probability that the keys cannot be stored is at most
$$\frac{4}{r} \cdot \frac{q(1+q)}{(1-q)^3}.$$
For $r \ge (1 + \varepsilon)n$ with a constant $\varepsilon > 0$ this is $O(1/n)$.
3. *(Above load 1/2.)* If $n \ge (1 + \varepsilon) r$ for a constant $\varepsilon > 0$, the keys cannot be stored with probability $1 - o(1)$. For $n \ge c\,r$ with $c > c^* \approx 1.594$, the root of $c = 2(1 - e^{-c})$, the failure probability is $1 - e^{-\Omega(n)}$, by a short counting proof given below.

So the load $1/2$ is a sharp threshold for two-choice cuckoo hashing: below it the table can be built except with probability $O(1/n)$, above it the table almost surely cannot.

## In plain words

Each key has two possible homes. Draw a dot for each home and a line for each key between its two homes. A group of connected dots can hold its keys exactly when it has no more lines than dots, because each key needs its own home inside its group.

When there are fewer keys than half the homes, the drawing is mostly small trees with a few single loops, and a group with two loops is rare: its chance shrinks like one over the number of keys. When there are more keys than half the homes, the drawing almost surely has one giant group with far more lines than dots, and the keys do not fit.

## Proof

**Part 1.** A placement maps each key to one of its two cells, with no cell used twice. So in a placement each key of a component uses a distinct cell of that component, and a component with more edges than vertices cannot be placed. Conversely, let a component have $e \le v$ edges. Since it is connected, $e \ge v - 1$. If $e = v - 1$, it is a tree: root it at any vertex and store each key in the endpoint of its edge that is farther from the root. If $e = v$, it has exactly one cycle: store the keys of the cycle by going around it in one direction, each key in the next cell, and store the keys of the trees that hang from the cycle in the endpoint farther from the cycle. In both cases each cell gets at most one key.

**A minimal obstruction.** Let a component have more edges than vertices. Take a spanning tree of it and two edges not in the tree, and then remove leaves again and again. What is left is connected, has some number $t$ of vertices and exactly $t + 1$ edges, and has no vertex of degree 1. Such a graph is one of two shapes:

- a *theta*: two vertices joined by three internally disjoint paths of $\ell_1, \ell_2, \ell_3 \ge 1$ edges, with $\ell_1 + \ell_2 + \ell_3 = t + 1$;
- a *dumbbell*: two cycles of $c_1, c_2 \ge 1$ edges joined by a path of $\ell \ge 0$ edges, with $c_1 + c_2 + \ell = t + 1$ (for $\ell = 0$ the cycles share a vertex).

In both cases the number of parameter choices for a given $t$ is at most $(t + 1)^2$. Call such a subgraph a *bicycle*. So the keys cannot be placed only if the cuckoo graph contains a bicycle.

**Part 2.** Count the expected number of bicycles with $t$ vertices. Fix a shape and an order of its $t$ vertices and $t + 1$ edges.

- *Cells.* The first vertex goes to one of $2r$ cells. Each edge joins $T_1$ to $T_2$, so the shape must be bipartite and the table of each other vertex is then fixed. So there are at most $2r \cdot r^{t-1} = 2r^t$ ways to map the vertices to cells.
- *Keys.* There are at most $n^{t+1}$ ways to assign distinct keys to the $t + 1$ edges.
- *Probability.* A key realizes a given edge $\{T_1[i], T_2[j]\}$ when $h_1(x) = i$ and $h_2(x) = j$, with probability $1/r^2$. Distinct keys are independent, so all $t + 1$ edges are realized with probability $r^{-2(t+1)}$.

Summing over the two kinds of shape, at most $(t+1)^2$ parameter choices each, and all $t \ge 1$, the expected number of bicycles is at most
$$\sum_{t \ge 1} 2 (t+1)^2 \cdot 2r^t \cdot n^{t+1} \cdot r^{-2(t+1)} = \frac{4}{r} \sum_{t \ge 1} (t+1)^2 q^{t+1} \le \frac{4}{r} \sum_{j \ge 1} j^2 q^j = \frac{4}{r} \cdot \frac{q(1+q)}{(1-q)^3}.$$
By [Markov's inequality](/markov-inequality/), the probability that at least one bicycle exists, and so the probability of failure, is at most this value. For $q = 1/(1 + \varepsilon)$ it is $O(1/(\varepsilon^3 r)) = O(1/n)$ for constant $\varepsilon$.

**Part 3, the counting bound.** A placement needs at least $n$ distinct cells, all of them the cell of some key. Let $X$ be the number of cells that are $h_1(x)$ or $h_2(x)$ for some key $x$. A fixed cell of $T_1$ is missed by all $n$ keys with probability $(1 - 1/r)^n \ge e^{-n/(r-1)}$, so $E[X] \le 2r(1 - e^{-n/(r-1)})$. If $n = c\,r$ with $c > c^*$, then $2(1 - e^{-c}) < c$, so for large $r$ there is a $\delta > 0$ with $E[X] \le (1 - \delta) n$. Reveal the keys one at a time. Changing the cells of one key changes $X$ by at most 2, so by the [Azuma inequality](/azuma-inequality/) for the Doob martingale, $\Pr[X \ge n] \le \Pr[X - E[X] \ge \delta n] \le \exp(-\delta^2 n^2 / (8n)) = e^{-\Omega(n)}$.

**Part 3, the full threshold.** For $1 < c \le c^*$ the counting bound is not enough. The cuckoo graph with $n = c\,r$ edges is a random bipartite multigraph of average degree $c$ on each side, and like the Erdős-Rényi graph it has a phase transition at average degree 1: for $c > 1$ it has, with probability $1 - o(1)$, a [giant component](/giant-component/) with a linear number of vertices and more edges than vertices, so part 1 rules out a placement. See the [giant component theorem](/erdos-renyi-giant-component-theorem/) for the classical graph. $\blacksquare$

## Consequences

- **The table design.** Two-choice cuckoo hashing must keep $r \ge (1 + \varepsilon) n$, so it uses a little more than twice the space of the keys. An insert rebuilds the table with new hash functions when the walk gets too long, and part 2 makes this rare: the expected number of rebuilds while inserting $n$ keys is $O(1)$, and Pagh and Rodler show $O(1)$ expected amortized time per insert. See [cuckoo hashing](/cuckoo-hashing/).
- **A stash.** Kirsch, Mitzenmacher and Wieder (2009) add a stash of constant size $s$ for the keys that do not fit. The keys fit with a stash of size $s$ when the total excess $\sum_{\text{components}} \max(0, e - v)$ is at most $s$, and they show the failure probability drops from $\Theta(1/n)$ to $O(1/n^{s+1})$.
- **More choices.** With $d \ge 3$ cells per key in one table, the threshold rises. The thresholds were found in 2010 by Dietzfelbinger, Goerdt, Mitzenmacher, Montanari, Pagh and Rink, by Fountoulakis and Panagiotou, and by Frieze and Melsted: about $0.918$ for $d = 3$ and about $0.977$ for $d = 4$. Fotakis, Pagh, Sanders and Spirakis showed that $d = O(\log(1/\varepsilon))$ choices give load $1 - \varepsilon$.
- **Buckets.** Cells that hold several keys raise the threshold with only two choices. With buckets of 2 keys the threshold is close to $0.9$, and with buckets of 4 it is above $0.95$. The [cuckoo filter](/cuckoo-filter/) uses buckets of 4.
- **Weaker hash functions.** Pagh and Rodler used hash functions with $O(\log n)$-wise independence, as in [k-independent hashing](/k-independent-hashing/). Pătrașcu and Thorup proved that simple [tabulation hashing](/tabulation-hashing/) also works for cuckoo hashing, with a failure probability that falls polynomially in $n$, though more slowly than $1/n$.

## Tightness

**Measured threshold.** The table gives the number of seeded trials in which all keys could be placed, tested with part 1 and a union-find structure, for two tables of $r = 2^{15}$ cells and fully random cells from Python's `random.Random(2024)`, 40 trials per load:

| load $n/(2r)$ | 0.46 | 0.48 | 0.49 | 0.50 | 0.51 | 0.52 | 0.54 |
|---|---|---|---|---|---|---|---|
| trials that fit | 39 | 39 | 38 | 32 | 22 | 4 | 0 |

The change from almost always to almost never is centered near load $0.5$ and gets sharper as $r$ grows.

**Measured O(1/n) failure.** At load $0.4$ ($q = 0.8$), the measured failure rate and $n$ times it were:

| $r$ | $n$ | failures | trials | rate | $n \cdot$ rate |
|---|---|---|---|---|---|
| 250 | 200 | 236 | 20000 | 0.0118 | 2.36 |
| 500 | 400 | 155 | 20000 | 0.00775 | 3.10 |
| 1000 | 800 | 97 | 20000 | 0.00485 | 3.88 |
| 2000 | 1600 | 57 | 20000 | 0.00285 | 4.56 |
| 4000 | 3200 | 30 | 20000 | 0.0015 | 4.80 |

The rate falls roughly like $1/n$, with $n \cdot$ rate leveling off near 5. The bound of part 2 is $720/r$ at $q = 0.8$, between 120 and 150 times the measured rate for $r \ge 1000$: the order $1/n$ is right, the constant is loose. With a stash of one key, the failures at $r = 250, 500, 1000$ dropped from $238, 147, 88$ to $6, 8, 2$ in 20000 trials.

**Measured thresholds with more choices.** With one table of 30000 cells and 20 trials per load, $d = 3$ choices fit in 20, 20, 18, 3 and 0 trials at loads $0.90, 0.91, 0.915, 0.92, 0.93$, and $d = 4$ choices fit in 20, 20, 17, 0, 0 trials at loads $0.96, 0.97, 0.975, 0.98, 0.99$. Two choices of buckets of size 2, with 15000 buckets, fit in all 20 trials at load $0.89$ and in none at $0.90$. These agree with the thresholds cited above.

**The model matters.** The theorem assumes fully random hash functions. With a weak family such as plain [multiply-shift](/multiply-shift-hashing/) or a pairwise independent one, structured key sets can create many keys with the same pair of cells, and three keys with the same two cells already form a component with 2 vertices and 3 edges.

## History

Rasmus Pagh and Flemming Friche Rodler presented cuckoo hashing at ESA 2001, with the journal version in 2004, and analyzed it through the cuckoo graph, with failure probability $O(1/n)$ below load $1/2$. Devroye and Morin and later Kutzelnigg and Drmota gave sharper analyses of the two-choice case. Fotakis, Pagh, Sanders and Spirakis introduced $d$-ary cuckoo hashing in 2003, and Dietzfelbinger and Weidling studied buckets in 2007. The exact thresholds for $d \ge 3$ choices came in 2010 from three independent groups, one of them through the link with random XORSAT. Kirsch, Mitzenmacher and Wieder added the stash in 2008, with the journal version in 2009.

## References
