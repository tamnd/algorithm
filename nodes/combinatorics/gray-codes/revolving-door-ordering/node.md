---
tag: JJSYG3
kind: algorithm
slug: revolving-door-ordering
name: Revolving door ordering
aliases:
- revolving door Gray code
- Nijenhuis-Wilf revolving door
- revolving door order
- Tang-Liu combination Gray code
area: combinatorics/gray-codes
level: advanced
summary: Gray code for fixed-size subsets in which each step swaps one element in and one element out.
solves: [combination-gray-code-generation]
model: word-ram
complexity:
  vars: {n: the size of the ground set, k: the size of each subset, N: the number of k-subsets (n choose k)}
  time: {worst: Θ(n + N), amortized: Θ(1)}
  space: {extra: Θ(n)}
properties: {in_place: true, deterministic: true, comparison: false, recursive: true}
history:
  year: 1973
  people: [D. T. Tang, C. N. Liu]
  note: Tang and Liu showed in 1973 that the strings of weight k in the reflected Gray code form a revolving door list. Bitner, Ehrlich and Reingold gave a loopless generator in 1976, and Payne and Ives a fast program in 1979.
prereqs: [binary-reflected-gray-code, binomial-coefficient, k-subset-enumeration]
see_also: [combination-gray-code-generation, ehrlich-loopless-combinations, chase-sequence, eades-mckay-algorithm, combinatorial-number-system, combinatorial-ranking-and-unranking, cool-lex-order, lexicographic-combinations]
sources:
  - book: isbn:9780201038040
    title: Donald E. Knuth, The Art of Computer Programming, Volume 4A, Combinatorial Algorithms, Part 1, Addison-Wesley, 2011
    locator: Section 7.2.1.3 (the revolving door Gray code, its recursive definition, the list (27) for s = t = 3, and Algorithm R, revolving-door combinations)
  - url: https://page.math.tu-berlin.de/~felsner/SemWS17-18/Ruskey-Comb-Gen.pdf
    title: Frank Ruskey, Combinatorial Generation, working version, University of Victoria, 1995 to 2003
    locator: Chapter 5, Section 5.3 (the recursion (5.4), Lemma 5.2 on the first and last subsets, and Algorithm 5.5, a CAT generator)
  - paper: doi:10.1109/T-C.1973.223681
    title: D. T. Tang and C. N. Liu, Distance-2 cyclic chaining of constant-weight codes, IEEE Transactions on Computers C-22(2), 176 to 180, 1973
    locator: the restriction of the reflected Gray code to a fixed weight
  - paper: doi:10.1145/355826.355830
    title: William H. Payne and Frederick M. Ives, Combination generators, ACM Transactions on Mathematical Software 5(2), 163 to 172, 1979
    locator: the revolving door generator that Knuth presents as Algorithm R
---

The revolving door ordering lists all $N = C(n, k)$ subsets of size $k$ of $[n] = \{1, \ldots, n\}$ so that each subset arises from the one before by removing one element and adding another, like people passing through a revolving door. It is defined by the recursion $R(n, k) = R(n-1, k),\ R(n-1, k-1)^R \cup \{n\}$, and it equals the list of strings with exactly $k$ ones in the [binary reflected Gray code](/binary-reflected-gray-code/), in that order. The recursive generator below takes $\Theta(N)$ time after $\Theta(n)$ setup, so $O(1)$ amortized per subset, and the order has a simple rank formula, an alternating sum of [binomial coefficients](/binomial-coefficient/). The list is cyclic: the last subset $\{1, \ldots, k-1, n\}$ is one swap away from the first, $\{1, \ldots, k\}$.

## In plain words

You must try every team of $k$ players chosen from $n$, and changing the team costs money for each player who leaves. A revolving door plan changes the team by one player out and one player in at each step, which is the smallest possible change.

The plan is built from smaller plans. First go through all teams without the last player, using the plan for $n - 1$ players. Then bring the last player in, and go through the teams of the other $k - 1$ players backward. Going backward makes the two halves meet at a pair of teams that differ by one swap.

## The problem

Given integers $n \ge 0$ and $0 \le k \le n$, visit every $k$-subset of $[n]$ once, so that two consecutive subsets $S$ and $S'$ satisfy $|S \setminus S'| = |S' \setminus S| = 1$. This is [combination Gray code generation](/combination-gray-code-generation/) under the transposition rule. Here $n$ is the size of the ground set, $k$ is the size of each subset, and $N = C(n, k)$. For $k > n$ there is nothing to visit. A subset is kept as a bit array $a_1 \ldots a_n$ with $a_e = 1$ when $e$ is in the subset, and the generator changes two entries per step and visits the array in place.

The list $R(m, t)$ of the $t$-subsets of $[m]$ is defined by $R(m, 0) = \emptyset$ (one empty subset), $R(m, m) = [m]$, and for $0 < t < m$

$$R(m, t) = R(m-1, t),\ \ R(m-1, t-1)^R \cup \{m\},$$

where $L^R$ is the list $L$ in reverse order and $L \cup \{m\}$ adds $m$ to each subset. For $0 < t < m$ the list starts at $\{1, \ldots, t\}$ and ends at $\{1, \ldots, t-1, m\}$.

## The algorithm

The walk keeps the current subset in $a$. In the forward direction it walks $R(m-1, t)$, swaps once, and walks $R(m-1, t-1)$ backward. The swap at the junction removes $x$ and adds $m$, where $x = t - 1$ if $t \ge 2$ and $x = m - 1$ if $t = 1$. In the reverse direction it does the same steps in the opposite order.

```pseudo id=main
REVOLVING-DOOR(n, k)                        ▷ 0 ≤ k ≤ n
L1  a ← 1^k 0^{n−k}                          ▷ the first subset {1, …, k}
L2  WALK(n, k, forward)

WALK(m, t, d)                               ▷ visits R(m, t), or its reverse if d = reverse
L3  if t = 0 or t = m then visit a; return  ▷ a single subset
L4  x ← t − 1 if t ≥ 2, else m − 1
L5  if d = forward then
L6      WALK(m − 1, t, forward)
L7      a_x ← 0; a_m ← 1                    ▷ x out, m in
L8      WALK(m − 1, t − 1, reverse)
L9  else
L10     WALK(m − 1, t − 1, forward)
L11     a_m ← 0; a_x ← 1                    ▷ m out, x in
L12     WALK(m − 1, t, reverse)
```

The calls never touch positions above $m$. The recursion depth is at most $n$, and an explicit stack replaces it in the implementation.

## Example

For $n = 5$ and $k = 3$ the generator visits these ten subsets. The swap column gives the element that leaves and the element that enters to reach the next subset.

| $r$ | subset | $a_1 \ldots a_5$ | swap | | $r$ | subset | $a_1 \ldots a_5$ | swap |
|---|---|---|---|---|---|---|---|---|
| 0 | 123 | 11100 | 2 out, 4 in | | 5 | 245 | 01011 | 2 out, 3 in |
| 1 | 134 | 10110 | 1 out, 2 in | | 6 | 345 | 00111 | 4 out, 1 in |
| 2 | 234 | 01110 | 3 out, 1 in | | 7 | 135 | 10101 | 1 out, 2 in |
| 3 | 124 | 11010 | 2 out, 5 in | | 8 | 235 | 01101 | 3 out, 1 in |
| 4 | 145 | 10011 | 1 out, 2 in | | 9 | 125 | 11001 | (wrap: 5 out, 3 in) |

The first half, rows 0 to 3, is $R(4, 3)$. The swap at row 3 is line L7 at the top level with $t = 3$, so $x = 2$: element 2 leaves and 5 enters. Rows 4 to 9 are $R(4, 2)$ backward with 5 added. With the elements renamed $0, \ldots, 5$ and written from the largest, the list for $n = 6$, $k = 3$ begins 210, 320, 321, 310, 430, 431, 432, 420, 421, 410 and matches Knuth's list (27); a script checked all 20 entries.

**Rank.** The subset $\{2, 4, 5\}$ has rank $(C(5, 3) - 1) - (C(4, 2) - 1) + (C(2, 1) - 1) = 9 - 5 + 1 = 5$, which is its row in the table.

## Correctness

The proof in `proofs/correctness.md` shows three things.

- **The list.** By induction on $m$, $R(m, t)$ contains each $t$-subset of $[m]$ once: the first part holds those without $m$ and the second part those with $m$, and $C(m-1, t) + C(m-1, t-1) = C(m, t)$. Its first subset is $\{1, \ldots, t\}$ and its last is $\{1, \ldots, t-1, m\}$ for $0 < t < m$.
- **One swap per step.** Inside each part this holds by induction, since reversing a list and adding $m$ to each subset keep the property. At the junction the last subset of $R(m-1, t)$ and the first subset of $R(m-1, t-1)^R \cup \{m\}$ differ by removing $x$ and adding $m$, with $x$ as in line L4.
- **The walk.** If WALK$(m, t, d)$ starts with $a$ equal to the first subset of its list (the last one if $d$ is reverse) on positions $1$ to $m$, then it visits the list in order, never touches positions above $m$, and ends at the last subset. Lines L7 and L11 do exactly the junction swaps.

**Link with the Gray code.** Prefixing bit $m$ to a string is the same as adding element $m$, so the recursion for $R$ is the recursion $\Gamma_m = 0\Gamma_{m-1},\ 1\Gamma_{m-1}^R$ of the reflected code restricted to weight $t$. This is the result of Tang and Liu (1973).

**Rank.** In $R(n, k)$ the subsets with largest element $x$ form the block $R(x-1, k-1)^R \cup \{x\}$ at positions $C(x-1, k)$ to $C(x, k) - 1$. Reading a reversed block gives the rank $r(T) = C(t_k, k) - 1 - r(T \setminus \{t_k\})$, and so

$$r(\{t_1 < \cdots < t_k\}) = \sum_{i=1}^{k} (-1)^{k-i} \bigl( C(t_i, i) - 1 \bigr).$$

## Complexity

- **Time.** The calls of WALK form a binary tree whose leaves are the $N$ visits. Every inner call has $0 < t < m$, so both of its children have nonempty lists, and a tree in which every inner node has two children has $N - 1$ inner nodes. Each call does $O(1)$ work outside its children, so the walk takes $\Theta(N)$ time, plus $\Theta(n)$ for line L1. The amortized time per subset is $O(1)$, so the generator is CAT.
- **Delay.** Between two visits the walk may return from and enter up to $n$ levels, so the worst-case delay is $\Theta(n)$, not $O(1)$. A loopless version exists: see [Ehrlich's loopless combination generation](/ehrlich-loopless-combinations/).
- **Space.** The array has $n$ entries and the recursion or the explicit stack has depth at most $n$: $\Theta(n)$ extra space.
- **Output.** Two entries of $a$ change per step. Copying each subset as a sorted list costs $\Theta(k)$ more per subset.
- **Rank and unrank.** The formula above uses $k$ binomial coefficients. Unranking picks $t_k$ as the least $x$ with $C(x, k) > r$, replaces $r$ by $C(x, k) - 1 - r$, and repeats with $k - 1$; with a table of binomial coefficients this costs $O(n)$ arithmetic operations.

## Properties

- **Cyclic.** For $0 < k < n$ the last subset $\{1, \ldots, k-1, n\}$ and the first $\{1, \ldots, k\}$ differ by swapping $k$ and $n$.
- **Genlex.** Subsets with the same largest elements appear together. In Knuth's index form $c_k \ldots c_1$ with $c_k > \cdots > c_1$, the values of $c_k$ increase, the values of $c_{k-1}$ for a fixed $c_k$ decrease, and so on, alternately.
- **Crossings.** A swap may move an element past other elements of the subset. The list for $n = 6$, $k = 3$ has nine steps in which two of the indices $c_3, c_2, c_1$ change at once, such as 210 to 320. The [Eades-McKay order](/eades-mckay-algorithm/) and [Chase's sequence](/chase-sequence/) avoid such crossings.
- **Weight of the Gray code.** Interleaving the lists $R(n, 0), R(n, 1), \ldots$ by position in $\Gamma_n$ gives back $\Gamma_n$.

## Variants and improvements

- **Loopless.** Bitner, Ehrlich and Reingold (1976) and Payne's Algorithm R in Knuth's presentation produce the same list with $O(1)$ worst-case work per subset: see [Ehrlich's loopless combination generation](/ehrlich-loopless-combinations/).
- **Homogeneous and near-perfect.** Restricting each swap so that the moving element jumps only over elements not in the subset gives the [Eades-McKay order](/eades-mckay-algorithm/). Restricting further to jumps of one or two places gives [Chase's sequence](/chase-sequence/).
- **Prefix shifts.** [Cool-lex order](/cool-lex-order/) changes each subset by rotating a prefix of its bit string, which is also one or two transpositions.
- **Lexicographic.** [Lexicographic combinations](/lexicographic-combinations/) and the [combinatorial number system](/combinatorial-number-system/) give the simplest ranking, but a step may change many elements.

## When to use it

Use the revolving door order when a value is computed over every $k$-subset and adding or removing one element updates it in $O(1)$ time, for example a sum of weights, a product, or a count of edges inside the subset with an adjacency matrix. Each step then costs one removal and one insertion. Use it also when you need exact rank and unrank in a Gray code order, for example to split the list between workers. If elements must not jump over each other, for example because their positions are physical, use the Eades-McKay or Chase order instead.

## Pitfalls

- **The swap for $t = 1$.** Line L4 with "$x \leftarrow t - 1$" for all $t$ gives $x = 0$ when $t = 1$, which is not an element. For $n = 3$, $k = 1$ the walk must go $\{1\}, \{2\}, \{3\}$, and the step from $\{2\}$ to $\{3\}$ removes $m - 1 = 2$. Line L4 must use $x = m - 1$ when $t = 1$.
- **The same swap in both directions.** Line L11 written as "$a_x \leftarrow 0$; $a_m \leftarrow 1$", copied from line L7, adds $m$ when it should remove it. Line L11 must undo line L7: $a_m \leftarrow 0$, $a_x \leftarrow 1$.
- **The wrong order in the reverse branch.** Line L10 must walk $R(m-1, t-1)$ forward before line L12 walks $R(m-1, t)$ backward, because the reverse of $A, B^R$ is $B, A^R$. Calling WALK$(m-1, t, \text{reverse})$ first starts from a subset that is not the current one.
- **The rank without the $-1$ terms.** Writing $\sum_i (-1)^{k-i} C(t_i, i)$ is off by $1$ when $k$ is odd. For $\{1, 2, 3\}$ it gives $1 - 1 + 1 = 1$ instead of 0.

## Implementations

## History

D. T. Tang and C. N. Liu proved in 1973 that the strings of weight $k$ in the reflected Gray code form a cyclic list in which consecutive strings differ in two bits. Bitner, Ehrlich and Reingold gave a loopless generator for it in 1976, and Payne and Ives published a fast combination generator in 1979, which Knuth presents as Algorithm R in Section 7.2.1.3. The name comes from the picture of two rooms joined by a revolving door that turns only when one person from each room is inside it, so each turn swaps two people (Ruskey, Section 5.3). Ruskey's Algorithm 5.5 is the recursive CAT form given here, and his Algorithm 5.7 is a loopless form.

## References
