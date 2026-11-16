---
tag: JWQHX7
kind: technique
slug: divide-and-color
name: Divide and color
area: complexity/parameterized-complexity
level: research
summary: "Split the vertices at random into two halves, solve the two halves of the pattern recursively, and repeat about 2^k times per level. For k-path this gives randomized 4^k time with polynomial space."
prereqs: [color-coding, parameterized-longest-path]
see_also: [k-path-color-coding, representative-families, monte-carlo-algorithm, one-sided-error, fixed-parameter-tractable, recurrence-relation]
sources:
  - paper: doi:10.1137/080716475
    title: "Jianer Chen, Joachim Kneis, Songjian Lu, Daniel Mölle, Stefan Richter, Peter Rossmanith, Sing-Hoi Sze and Fenghui Zhang, Randomized divide-and-conquer: improved path, matching, and packing algorithms, SIAM Journal on Computing 38(6), 2526-2547 (2009)"
    locator: the randomized divide-and-conquer method and k-path in time O(4^k k^2.7 m) with polynomial space
  - paper: doi:10.1007/11917496_6
    title: "Joachim Kneis, Daniel Mölle, Stefan Richter and Peter Rossmanith, Divide-and-Color, 32nd International Workshop on Graph-Theoretic Concepts in Computer Science (WG 2006), Lecture Notes in Computer Science 4271, 58-67"
    locator: the method under this name, with k-path as the main example
  - book: isbn:9783319212746
    title: Marek Cygan, Fedor V. Fomin, Lukasz Kowalik, Daniel Lokshtanov, Daniel Marx, Marcin Pilipczuk, Michal Pilipczuk and Saket Saurabh, Parameterized Algorithms, Springer, 2015
    locator: Section 5.4, A divide and color algorithm for Longest Path, and the derandomization in Chapter 5
---

Divide and color is a randomized method for finding a pattern with $k$ vertices, such as a path, in a graph with $n$ vertices and $m$ edges. It is a form of [color coding](/color-coding/) with only two colors, used recursively. Color the vertices at random with two colors, say left and right. A fixed solution splits well, with its first half on the left and its second half on the right, with probability $2^{-k}$. Then solve the two halves recursively, each in the subgraph of its own color, and join them along an edge. The two halves cannot share a vertex, because they lie in disjoint vertex sets. To make the recursion succeed, each level repeats the random split about $2^k$ times. For [k-path](/parameterized-longest-path/) the running time is $4^k k^{O(1)} \cdot \mathrm{poly}(n)$, and Chen et al. (2009) proved the bound $O(4^k k^{2.7} m)$. Unlike color coding, the method needs only polynomial space. The method was found at the same time by Kneis, Mölle, Richter and Rossmanith (WG 2006), who named it, and by Chen, Lu, Sze and Zhang; the journal version merges both.

## In plain words

You look for a chain of a few people in a big crowd, with no person used twice. Send each person at random to the left room or the right room. With some luck, the first half of the chain is in the left room and the second half in the right room.

Now solve two smaller jobs: find a half chain in the left room, and a half chain in the right room that starts next to the end of the left one. The two halves can never share a person, because the rooms are apart. Each smaller job uses the same trick again.

One random split rarely works, so try many splits at each step. The work grows fast with the length of the chain, but slowly with the size of the crowd, and you never need a big table.

## When it applies

- The solution is a set of $k$ vertices or elements that can be cut into two parts of about $k/2$ each, such that each part is a smaller solution of the same kind, and the parts must be disjoint.
- Joining two partial solutions is easy once they are known to be disjoint, for example by an edge between the end of one and the start of the other.
- Polynomial space matters, or the table of color coding with $2^k$ sets per vertex is too large.
- One-sided error is acceptable, or a deterministic bound with an extra $4^{o(k)}$ factor is acceptable.

## The template

The template has three holes. SPLIT$(S)$ cuts a solution $S$ with $k$ elements into two ordered parts $S_1$ and $S_2$ of sizes $\lceil k/2 \rceil$ and $\lfloor k/2 \rfloor$; it is used only in the analysis. SUB$(I, X)$ is the instance $I$ restricted to the element set $X$. JOIN$(B_1, I_R)$ prepares the right instance from the answers $B_1$ of the left half. The procedure returns a set of answers: for $k$-path, the set of end vertices of $k$-paths that start in a given set $A$.

```pseudo id=main
DC(I, A, k)                          ▷ a set of answers, each one correct
L1  if k = 1 then return the base answers of I and A
L2  B ← ∅
L3  repeat r(k) times
L4      put each element in L with probability 1/2, else in R
L5      B_1 ← DC(SUB(I, L), A ∩ L, ⌈k/2⌉)
L6      A_2 ← JOIN(B_1, SUB(I, R))
L7      B ← B ∪ DC(SUB(I, R), A_2, ⌊k/2⌋)
L8  return B
```

For $k$-path the base answers at L1 are the vertices of $A$ (a path of one vertex), and JOIN returns the vertices of $R$ that have a neighbor in $B_1$. The top call is DC$(G, V, k)$, and $G$ has a $k$-path exactly when the answer is not empty.

**Lemma (soundness).** Every vertex in the answer of DC$(G, A, k)$ is the last vertex of a $k$-path of $G$ whose first vertex is in $A$.

*Proof.* By induction on $k$. For $k = 1$ it is clear. Let $v$ come from line L7. By induction, $v$ is the end of a $\lfloor k/2 \rfloor$-path $P_2$ in $G[R]$ that starts at some $w \in A_2$. By the definition of JOIN, $w$ has a neighbor $u \in B_1$, and by induction $u$ is the end of a $\lceil k/2 \rceil$-path $P_1$ in $G[L]$ that starts in $A$. Since $L$ and $R$ are disjoint, $P_1$ followed by $P_2$ is a path with $k$ vertices. $\square$

**Lemma (completeness).** Let $r(k) = \lceil 4 \ln 2 \cdot 2^k \rceil$. If $G$ has a $k$-path from a vertex of $A$ to $v$, then $v$ is in the answer of DC$(G, A, k)$ with probability at least $1/2$.

*Proof.* By induction on $k$; the case $k = 1$ is clear. Fix such a path $P$, with first part $P_1$ (the first $\lceil k/2 \rceil$ vertices) ending at $u$ and second part $P_2$ starting at $w$ and ending at $v$. One repetition puts $P_1$ into $L$ and $P_2$ into $R$ with probability $2^{-k}$. Given that, $P_1$ is a path of $G[L]$ from $A \cap L$, so by induction $u \in B_1$ with probability at least $1/2$. If $u \in B_1$, then $w \in A_2$, and by induction, with fresh random bits, $v$ is in the answer of L7 with probability at least $1/2$. So one repetition succeeds with probability at least $2^{-k}/4$, and all $r(k)$ repetitions fail with probability at most $(1 - 2^{-k}/4)^{r(k)} \le e^{-r(k) 2^{-k}/4} \le e^{-\ln 2} = 1/2$. $\square$

Repeating the top call $\lceil \log_2(1/\delta) \rceil$ times lowers the error to $\delta$, and the error stays one-sided by the soundness lemma.

**Running time.** Let $N(k)$ be the number of base calls. Then $N(1) = 1$ and $N(k) = r(k) \, (N(\lceil k/2 \rceil) + N(\lfloor k/2 \rfloor))$. For $k$ a power of 2, unrolling gives $N(k) = \prod_{j} 2 r(k/2^j)$ over the $\log_2 k$ levels, which is about $2^{k + k/2 + k/4 + \cdots} (8 \ln 2)^{\log_2 k} = 4^k k^{O(1)}$. Each call does $O(n + m)$ work besides its children, so the time is $4^k k^{O(1)} (n + m)$. The recursion has depth $\log_2 k$, and each level stores a few vertex sets, so the space is $O((n + m) \log k)$.

The numbers from a run of the recurrence:

| $k$ | $r(k)$ | base calls $N(k)$ | $4^k$ | $N(k)/4^k$ | $(2e)^k$ |
|---|---|---|---|---|---|
| 2 | 12 | 24 | 16 | 1.5 | 30 |
| 4 | 45 | 2160 | 256 | 8.4 | 874 |
| 8 | 710 | $3.07 \cdot 10^6$ | 65536 | 46.8 | $7.6 \cdot 10^5$ |
| 16 | 181705 | $1.11 \cdot 10^{12}$ | $4.3 \cdot 10^9$ | 260 | $5.8 \cdot 10^{11}$ |

The factor $k^{O(1)}$ is large in this simple form: up to $k = 16$ it does more base calls than color coding does colorings times color sets. The gain is in the space and in the base of the exponent for large $k$. Chen et al. use a sharper split and analysis to reach $O(4^k k^{2.7} m)$.

## Classic examples

### k-path

This is the main example. Take the graph $G$ with the vertices $a, \ldots, f$ and the edges $ab$, $bc$, $cd$, $de$, $be$ and $ef$, and $k = 4$. It has 9 paths with 4 vertices. Of the $2^6 = 64$ splits of the vertices, 26 put the first two vertices of some 4-path on the left and the last two on the right, as a full enumeration shows. A run of DC with only one repetition per call, instead of $r(k)$, found a 4-path in 5.6% of 20000 runs with the seed 5; with $r(4) = 45$ and $r(2) = 12$ the run with the seed 1 returned all six vertices as ends of 4-paths, which is the right set. See [k-path by color coding](/k-path-color-coding/) for the color coding algorithm on the same graph.

### Packing and matching

Chen et al. applied the method to packing problems, where the solution is a family of $k$ disjoint small sets, such as $k$ disjoint triangles or a matching in a 3-partite hypergraph. A random split of the elements into two halves, with half of the sets on each side, again gives disjointness for free. The method gave the best randomized bounds for several of these problems at the time.

### Directed paths and trees

The proof above never uses that the edges are undirected: for a directed graph, JOIN takes the out-neighbors of $B_1$. For a tree pattern with $k$ vertices, split at a vertex whose removal leaves parts with at most $k/2$ vertices each, and recurse on the parts.

## Variations

- **Derandomization.** Replace the random splits by an explicit family of splits that contains, for every set of $k$ vertices and every cut of it into a left part and a right part, a split that puts each part on its side. An $(n, k)$-universal set, a family of subsets of $V$ that shows every pattern on every $k$ vertices, does this, and Naor, Schulman and Srinivasan built such families of size $2^k k^{O(\log k)} \log n$. With these in place of the $r(k)$ random splits, the time becomes deterministic $4^{k + o(k)} m$ for $k$-path, as stated in the conference version of Chen et al. (SODA 2007).
- **Unbalanced splits.** Put each element on the left with a probability other than $1/2$, or cut the solution at a point other than the middle. This is useful when the two parts have different costs.
- **Color coding.** With $k$ colors at once instead of a recursion of 2-colorings, the method becomes plain color coding: $(2e)^k$ time but $2^k n$ space. See [color coding](/color-coding/).
- **Representative families.** The deterministic method of [representative families](/representative-families/) replaces the random split by a family of sets that is guaranteed to contain a good extension, and gives deterministic $O(2.619^k n \log n)$ time for $k$-path.

## Pitfalls

- **No repetition inside the recursion.** If only the top level repeats, one try must split well at each of the $\log_2 k$ levels, and each level succeeds with probability $2^{-k}$. A try then succeeds with probability about $2^{-k \log_2 k} = k^{-k}$, and the top level needs about $k^k$ tries. The repetition at every level is what keeps the base at 4.
- **Dependent random bits.** The two recursive calls of one repetition must use fresh random bits. The proof conditions on the left call and then uses that the right call is independent.
- **Joining without disjointness.** Joining a left part and a right part found in the same vertex set, not in $L$ and $R$, can make a walk that repeats a vertex. The split into disjoint sets is the whole point.
- **Odd k.** For odd $k$ the halves have sizes $\lceil k/2 \rceil$ and $\lfloor k/2 \rfloor$. Using $k/2$ for both loses a vertex.
- **Large polynomial factors.** The simple form does more work than color coding for $k$ up to about 16, as the table shows. Do not assume that $4^k$ beats $(2e)^k$ in practice for small $k$.

## Exercises

1. Show that the recurrence $N(k) = c \cdot 2^k \cdot 2 N(k/2)$ with $N(1) = 1$ gives $N(k) = 4^{k - 1} (2c)^{\log_2 k}$ for $k$ a power of 2.
2. Write DC for directed graphs and prove its soundness.
3. Use divide and color to decide whether a graph has $k$ vertex-disjoint triangles in time $2^{O(k)} n^{O(1)}$ and polynomial space.
4. Give an unbalanced version that cuts the path into parts of sizes $k/3$ and $2k/3$ and puts each vertex on the left with probability $1/3$. What is the base of its running time?

## References
