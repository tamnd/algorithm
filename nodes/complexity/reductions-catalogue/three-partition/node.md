---
tag: BT39FH
kind: problem
slug: three-partition
name: 3-partition problem
aliases:
- 3-partition
area: complexity/reductions-catalogue
level: advanced
summary: Split 3m numbers, each strictly between B/4 and B/2, into m triples that each sum to B. Strongly NP-complete, so it stays hard when the numbers are written in unary.
prereqs: [np-complete, strong-np-hardness, three-dimensional-matching]
see_also: [partition-problem, bin-packing-np-hardness, makespan-minimization, scheduling-with-release-times-and-deadlines, tetris-problem, no-fptas-for-strongly-np-hard-problems, pseudo-polynomial-time, unary-encoding]
sources:
  - paper: doi:10.1137/0204035
    title: Michael R. Garey and David S. Johnson, Complexity results for multiprocessor scheduling under resource constraints, SIAM Journal on Computing 4(4), 1975
    locator: the proof that 3-PARTITION is NP-complete in the strong sense, and its use for scheduling
  - book: isbn:9780716710455
    title: Michael R. Garey and David S. Johnson, Computers and Intractability, A Guide to the Theory of NP-Completeness, W. H. Freeman, 1979
    locator: Section 4.2 (number problems and strong NP-completeness, with the reductions from 3DM through 4-PARTITION to 3-PARTITION) and Appendix A3.2, problem SP15
---

The 3-partition problem asks whether $3m$ positive integers can be split into $m$ groups of three with the same sum. It is the standard source of strong NP-hardness: Garey and Johnson (1975) proved that it stays [NP-complete](/np-complete/) even when every number is bounded by a polynomial in the length of the input. So, unlike the [partition problem](/partition-problem/), it has no [pseudo-polynomial](/pseudo-polynomial-time/) algorithm unless P = NP. Most proofs that packing and scheduling problems are [strongly NP-hard](/strong-np-hardness/), such as [bin packing](/bin-packing-np-hardness/), start from it.

## In plain words

A baker has a pile of cakes of different weights and wants to fill boxes. Each box must hold exactly three cakes, and every box must weigh the same.

When there are only two boxes, a table of all reachable weights solves the problem quickly, as long as the weights are small numbers. With many boxes that trick fails. The difficulty does not come from large weights; it comes from the number of ways to group the cakes. Even when all the weights are small numbers, no fast method is known. This is why the problem is called strongly hard, and why it is the usual starting point for showing that packing and scheduling problems are hard.

## Definition

**Instance.** A positive integer $B$ and a multiset of $3m$ positive integers $a_1, \ldots, a_{3m}$ with $\sum_i a_i = mB$ and $B/4 < a_i < B/2$ for every $i$.

**Question.** Can the indices be split into $m$ disjoint sets $A_1, \ldots, A_m$ with $\sum_{i \in A_j} a_i = B$ for every $j$?

The bounds on $a_i$ force every set $A_j$ to have exactly three elements: two numbers sum to less than $B$, and four numbers sum to more than $B$. Some authors drop the bounds and ask for $m$ triples with sum $B$; the problem stays strongly NP-complete.

**Encoding.** The numbers are written in binary. The certificate is the list of triples, and the verifier checks that they use every index once and that each sums to $B$, in time polynomial in the input length on the [multitape Turing machine](/multitape-turing-machine/). So the problem is in NP.

**Complexity.** NP-complete in the strong sense (Garey and Johnson 1975): it is NP-complete even when the numbers are written in [unary](/unary-encoding/). It is problem SP15 in Garey and Johnson (1979).

## Variants

- **Two groups.** With two groups and no size limit the problem is the [partition problem](/partition-problem/), which is only weakly NP-complete; a dynamic program over the reachable sums solves it in pseudo-polynomial time.
- **4-partition.** Split $4m$ numbers with $B/5 < a_i < B/3$ into $m$ groups of four with sum $B$. It is also strongly NP-complete, and Garey and Johnson use it as a step from [3-dimensional matching](/three-dimensional-matching/) to 3-partition.
- **Numerical 3-dimensional matching.** Given three lists $x$, $y$, $z$ of $m$ numbers each, split them into $m$ triples with one number from each list and the same sum $B$. It is a strongly NP-complete special case of the same idea.
- **Fixed $m$.** For each fixed number $m$ of groups, a dynamic program over the sums of the first $m - 1$ groups runs in pseudo-polynomial time. The hardness needs $m$ to be part of the input.

## Examples

**A yes-instance.** Take $B = 20$ and the numbers $6, 6, 7, 7, 7, 7$. All of them are between $5$ and $10$, and they sum to $40 = 2 \cdot 20$. The split $\{6, 7, 7\}, \{6, 7, 7\}$ works, and a script that listed all splits found no other.

**A no-instance.** Take $B = 24$ and the numbers $7, 7, 7, 9, 9, 9$. They are between $6$ and $12$ and sum to $48$. The possible triple sums are $21, 23, 25$ and $27$, so no triple sums to $24$.

**The reduction from 4-partition.** Take $m = 1$, $B = 17$ and $a = (4, 4, 4, 5)$; every $a_i$ is between $17/5$ and $17/3$, and $\{1, 2, 3, 4\}$ is a 4-partition. The construction in the Reductions section gives $B' = 64 \cdot 17 + 4 = 1092$ and 21 numbers:

- $w_1 = w_2 = w_3 = 357$ and $w_4 = 361$;
- for the pairs $12, 13, 14, 23, 24, 34$, the numbers $u = 378, 378, 374, 378, 374, 374$ and $\bar u = 374, 374, 378, 374, 378, 378$;
- five fillers of $340$.

All 21 numbers are between $273$ and $546$. A script listed the 3-partitions of this multiset and found exactly one. It has the triples $w_1 + w_2 + u_{12} = 357 + 357 + 378$, $w_3 + w_4 + u_{34} = 357 + 361 + 374$, $\bar u_{12} + \bar u_{34} + 340 = 374 + 378 + 340$, and $u_{ij} + \bar u_{ij} + 340$ for each of the four pairs $13, 14, 23, 24$. Each sums to $1092$, and the third triple is where the 4-set $\{1, 2, 3, 4\}$ shows.

## Known algorithms

- **Dynamic programming over subsets.** Fill the groups one after the other. A set $S$ of used numbers is reachable if the numbers of $S$ can be ordered so that each completed group sums to $B$; the current group then holds $\sum_{i \in S} a_i \bmod B$. This decides the problem in $O(2^n n)$ time with $n = 3m$.
- **No pseudo-polynomial algorithm.** Because the problem is strongly NP-complete, an algorithm with time polynomial in $n$ and $B$ would give P = NP. For the same reason, problems that contain it, such as [bin packing](/bin-packing-np-hardness/) and [makespan minimization](/makespan-minimization/) on many machines, have no [FPTAS](/no-fptas-for-strongly-np-hard-problems/) unless P = NP.

## Bounds

- **Strong NP-completeness.** No algorithm runs in time polynomial in $n$ and $\max_i a_i$ unless P = NP.
- **Unary input.** Since the reductions above make numbers of polynomial size, the problem stays NP-complete when every $a_i$ is written in unary, so the input length is $\sum_i a_i$.

## Reductions

Garey and Johnson prove strong NP-completeness through the chain 3DM to 4-PARTITION to 3-PARTITION. Both steps are Karp reductions, and both make numbers whose size is bounded by a polynomial in the input length. That property is what makes the result strong: a pseudo-polynomial algorithm for 3-partition, run on these instances, would take polynomial time.

**From 4-partition (Karp reduction).** Let $a_1, \ldots, a_{4m}$ with sum $mB$ and $B/5 < a_i < B/3$ be an instance of 4-partition. For each $i$ and each pair $\{i, j\}$, write $s_{ij} = a_i + a_j$.

*Map.* Make the numbers
$$w_i = 4(5B + a_i) + 1, \quad u_{ij} = 4(6B - s_{ij}) + 2, \quad \bar u_{ij} = 4(5B + s_{ij}) + 2,$$
for every $i$ and every pair $i < j$, plus $\binom{4m}{2} - m$ fillers equal to $20B$, and set $B' = 64B + 4$.

*Cost.* There are $4m + 2\binom{4m}{2} + \binom{4m}{2} - m = 24m^2 - 3m$ numbers, all at most $32B$. So the map takes polynomial time, and the largest number grows only by a constant factor. One can check that all numbers lie strictly between $B'/4 = 16B + 1$ and $B'/2 = 32B + 2$ and that they sum to $(8m^2 - m) B'$.

*If a 4-partition exists, then a 3-partition exists.* For each group $\{i, j, k, l\}$ of the 4-partition, form the triples $w_i + w_j + u_{ij}$, $w_k + w_l + u_{kl}$ and $\bar u_{ij} + \bar u_{kl} + 20B$. The first two sum to $64B + 4$ by the definitions, and the third sums to $60B + 4(a_i + a_j + a_k + a_l) + 4 = 64B + 4$. This uses $2m$ of the pairs. For each of the other $\binom{4m}{2} - 2m$ pairs, form $u_{ij} + \bar u_{ij} + 20B = 64B + 4$. Every number is used once; in particular the fillers used are $m + \binom{4m}{2} - 2m$, which is their number.

*If a 3-partition exists, then a 4-partition exists.* Take any 3-partition. Modulo 4, the $w$'s are 1, the $u$'s and $\bar u$'s are 2, the fillers are 0, and $B'$ is 0. A triple with residue sum 0 has the residues $\{1, 1, 2\}$, $\{2, 2, 0\}$ or $\{0, 0, 0\}$. Three fillers sum to $60B \ne B'$. So each triple is either two $w$'s and one $u$ or $\bar u$ (a *$w$-triple*), or two $u$'s or $\bar u$'s and a filler (an *$f$-triple*). Writing out the sums gives:

- $w_i + w_j + u_{kl} = B'$ if and only if $s_{kl} = s_{ij}$, and $w_i + w_j + \bar u_{kl} = B'$ if and only if $s_{kl} = B - s_{ij}$;
- in an $f$-triple, $u_{ij} + \bar u_{kl}$ fits if and only if $s_{ij} = s_{kl}$, and $u_{ij} + u_{kl}$ or $\bar u_{ij} + \bar u_{kl}$ fits if and only if $s_{ij} + s_{kl} = B$.

The $w$-triples pair up the $4m$ indices into $2m$ *$w$-pairs*. Let $P$ be the multiset of their sums $s_{ij}$. Now use this fact: *a multiset $M$ can be split into pairs with sum $B$ if and only if every value $x \ne B/2$ occurs in $M$ as often as $B - x$, and $B/2$ occurs an even number of times.* For a multiset $M$, let $f_M(x)$ be the number of times $x$ occurs minus the number of times $B - x$ occurs.

Let $U$ and $\bar U$ be the multisets of the values $s$ of the $u$'s and the $\bar u$'s that are in $f$-triples. Let $P_1$ be the sums of the $w$-pairs that took a $u$, and $P_2$ the sums of those that took a $\bar u$. All pair sums $s_{ij}$ form a multiset $\mathcal{A}$, so $U = \mathcal{A} - P_1$ and $\bar U = \mathcal{A} - \{B - p : p \in P_2\}$, and therefore $f_{\bar U} - f_U = f_{P_1} + f_{P_2} = f_P$. On the other side, an $f$-triple with $u_{ij} + \bar u_{kl}$ adds the same value to $U$ and to $\bar U$, and an $f$-triple with two $u$'s or two $\bar u$'s adds two values with sum $B$, which adds 0 to $f$. So $f_{\bar U} - f_U = 0$, and $f_P = 0$. The same count for the value $B/2$ shows that it occurs in $P$ an even number of times. By the fact above, the $w$-pairs can be grouped two by two with sums $B$. The $w$-pairs are disjoint, so this grouping is a 4-partition.

**From 3-dimensional matching to 4-partition (Karp reduction, sketch).** Let $M \subseteq W \times X \times Y$ be a 3DM instance with $\lvert W \rvert = \lvert X \rvert = \lvert Y \rvert = q$ and $k = \lvert M \rvert$, and let $r = 32q$. If some element is in no triple, output a fixed no-instance. Otherwise, one choice of sizes that works, a variant of Garey and Johnson's, is:

- for each $w_i \in W$, one *actual* number $10r^4 + ir + 1$ and, for each other triple that contains $w_i$, one *dummy* number $11r^4 + ir + 1$;
- for each $x_j$, an actual number $10r^4 + jr^2 + 2$ and dummies $11r^4 + jr^2 + 2$;
- for each $y_l$, an actual number $10r^4 + lr^3 + 4$ and dummies $8r^4 + lr^3 + 4$;
- for each triple $(w_i, x_j, y_l) \in M$, the number $10r^4 - lr^3 - jr^2 - ir + 8$;
- $B = 40r^4 + 15$.

All numbers lie strictly between $B/5$ and $B/3$, and there are $4k$ of them, summing to $kB$. In a group of four with sum $B$, the last digits $1, 2, 4, 8$ in base $r$ force one number of each kind. The digits for $r$, $r^2$ and $r^3$ then force the three element numbers to have the indices of the triple number. Finally, the coefficients of $r^4$ sum to 40 only as $10 + 10 + 10 + 10$ or $11 + 11 + 8 + 10$, so a group uses all actual numbers or all dummies. The $q$ groups with actual numbers form a matching. The numbers have $O(\log q)$ bits, so the instance is polynomial even in unary. A script checked the equivalence on all 255 nonempty sets of triples for $q = 2$ and on random instances for $q = 3$.

## Applications

- **Bin packing and scheduling.** With $m$ bins of size $B$, a 3-partition instance is a bin packing instance, and with $m$ machines and deadline $B$ it is a scheduling instance. This gives strong NP-hardness of [bin packing](/bin-packing-np-hardness/), of [makespan minimization](/makespan-minimization/) when the number of machines is part of the input, and of [scheduling with release times and deadlines](/scheduling-with-release-times-and-deadlines/).
- **Puzzles and games.** Hardness proofs for packing puzzles and for [Tetris](/tetris-problem/) encode the numbers of a 3-partition instance as piece sizes. Because the problem is strongly NP-hard, the sizes can be written in unary as rows or blocks.
- **No FPTAS.** For an optimization problem with integer values bounded by a polynomial in the input length and the largest number, strong NP-hardness from 3-partition rules out a [fully polynomial-time approximation scheme](/no-fptas-for-strongly-np-hard-problems/) unless P = NP.

## References
