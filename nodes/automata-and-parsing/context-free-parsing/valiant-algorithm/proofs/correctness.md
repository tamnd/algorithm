---
title: Valiant's algorithm fills every cell of the recognition table with the right set of nonterminals, and it stops
proves: [correctness, termination]
status: full
---

We use the notation of the [context-free grammar](/context-free-grammar/) page and the pseudocode of the page: VALIANT (lines L1 to L4), COMPUTE (lines L5 to L7) and COMPLETE (lines L8 to L16). The grammar $G$ is in [Chomsky normal form](/chomsky-normal-form/): every production is $A \to BC$ with nonterminals $B$ and $C$, or $A \to a$ with a terminal $a$, and the only other production allowed is $S \to \varepsilon$, when $S$ is on no right side. The input is $w = a_1 \cdots a_n$, and $N$ is the least power of 2 with $N \ge n + 1$.

## The target values

For $0 \le i < j \le N$ let $T^*[i, j]$ be the set of nonterminals $A$ with $A \Rightarrow^* a_{i+1} \cdots a_j$, where $a_{n+1}, \ldots, a_N$ are a padding symbol that is not in $G$. For a set $K$ of positions let

$$P_K[i, j] = \{ (B, C) : \text{there is } k \in K \text{ with } i < k < j,\ B \in T^*[i, k],\ C \in T^*[k, j] \},$$

and write $P^*[i, j]$ for $P_K[i, j]$ with $K$ the set of all positions: the pairs that can be split anywhere.

**Lemma 1.** (a) $T^*[i, i+1] = \{ A : A \to a_{i+1} \text{ is in } G \}$. (b) If $j \ge i + 2$, then $T^*[i, j] = \{ A : A \to BC \text{ is in } G,\ (B, C) \in P^*[i, j] \}$. (c) $T^*[i, j] = \emptyset$ when $j > n$.

*Proof.* In Chomsky normal form, a nonterminal other than a start symbol with $S \to \varepsilon$ derives only nonempty strings, and $S$ is on no right side. So in a derivation $A \Rightarrow BC \Rightarrow^* x$, both $B$ and $C$ derive nonempty parts of $x$, and $|x| \ge 2$. Hence a one-letter string comes only from a production $A \to a$, which is (a). For $|x| \ge 2$ the first step must be some $A \to BC$, and $x = yz$ with $B \Rightarrow^* y$ and $C \Rightarrow^* z$, both nonempty; with $x = a_{i+1} \cdots a_j$ this is a split point $k$ with $i < k < j$, which is (b). For (c), no derived string contains the padding symbol. $\square$

Line L1 sets the terminal cells $T[i, i+1]$ to the value of Lemma 1(a) for $i < n$ and leaves them empty for $i \ge n$, which also agrees with Lemma 1(a), since no production has the padding symbol. All other cells of $T$ and all cells of $P$ start empty.

## The block products

For blocks of cells, $X \cdot Y$ is the matrix whose cell $[i, j]$ is the set of pairs $(B, C)$ with $B \in X[i, k]$ and $C \in Y[k, j]$ for some $k$ in the shared index range. The implementation computes it with one Boolean product for each pair $(B, C)$ that is the right side of a production, which gives the same pairs.

A product $T[r_0{:}r_1, k_0{:}k_1] \cdot T[k_0{:}k_1, c_0{:}c_1]$ added into $P[r_0{:}r_1, c_0{:}c_1]$ adds to each cell $(i, j)$ of the block exactly the pairs of the splits $k \in [k_0, k_1)$, computed from the current $T$. In every product of lines L13 to L15, $r_1 \le k_0$ and $k_1 \le c_0$, so $i < k < j$ holds for all $i$, $k$ and $j$ of the blocks. If the cells $T[i, k]$ and $T[k, j]$ that it reads already hold their final values $T^*$, the product adds exactly $P_{[k_0, k_1)}[i, j]$.

## Lemma 2: COMPLETE

Consider a call COMPLETE$(\ell, m, \ell', m')$ with $m - \ell = m' - \ell'$ a power of 2 and $m \le \ell'$. Its **rectangle** is the set of cells $(i, j)$ with $\ell \le i < m$ and $\ell' \le j < m'$. Suppose that, when the call starts,

1. $T[i, j] = T^*[i, j]$ for all $\ell \le i < j < m$ (the triangle of rows) and for all $\ell' \le i < j < m'$ (the triangle of columns);
2. $P[i, j] = P_{[m, \ell')}[i, j]$ for every cell of the rectangle (the splits in the gap between the two ranges are in);
3. every cell $(i, j)$ of the rectangle with $j \ge i + 2$ is still empty in $T$.

Then, when the call returns, $T[i, j] = T^*[i, j]$ and $P[i, j] = P^*[i, j]$ for every cell of the rectangle, and no cell outside the rectangle has changed, in $T$ or in $P$.

*Proof.* By induction on $s = m - \ell$.

*Base, $s = 1$.* The rectangle is the single cell $(\ell, \ell')$. Its splits $k$ with $\ell < k < \ell'$ all lie in $[m, \ell') = [\ell + 1, \ell')$, so condition 2 says $P[\ell, \ell'] = P^*[\ell, \ell']$. If $\ell' = \ell + 1$, the cell is a terminal cell, line L9 does nothing, and $T$ is right by line L1. Otherwise line L9 sets $T[\ell, \ell']$, empty by condition 3, to $\{ A : A \to BC,\ (B, C) \in P^*[\ell, \ell'] \}$, which is $T^*[\ell, \ell']$ by Lemma 1(b). Nothing else changes.

*Step, $s \ge 2$.* Let $a = (\ell + m)/2$ and $b = (\ell' + m')/2$, as in line L11. The rectangle splits into four quadrants of side $s/2$:

- $Q_1$: rows $[a, m)$, columns $[\ell', b)$, the quadrant nearest the diagonal;
- $Q_2$: rows $[\ell, a)$, columns $[\ell', b)$;
- $Q_3$: rows $[a, m)$, columns $[b, m')$;
- $Q_4$: rows $[\ell, a)$, columns $[b, m')$, the farthest one.

We check the three conditions for each of the four recursive calls, in order. The triangles that the calls need lie inside the triangles of condition 1 or inside quadrants already finished, and condition 3 holds because only the call for a quadrant writes $T$ in that quadrant.

- **Line L12, COMPLETE$(a, m, \ell', b)$ for $Q_1$.** Its triangles $[a, m)$ and $[\ell', b)$ are parts of the triangles of condition 1. Its gap is $[m, \ell')$, the same as ours, so condition 2 holds as it is. By induction, $Q_1$ is final afterwards.
- **Line L13, then COMPLETE$(\ell, a, \ell', b)$ for $Q_2$.** The gap of $Q_2$ is $[a, \ell') = [a, m) \cup [m, \ell')$. The cells of $Q_2$ have the splits $[m, \ell')$ by condition 2, and line L13 adds the splits $k \in [a, m)$, with $T[i, k]$ for $\ell \le i < a \le k < m$ in the triangle of rows (final by condition 1) and $T[k, j]$ in $Q_1$ (final). So $P = P_{[a, \ell')}$ on $Q_2$. The triangles are $[\ell, a)$, inside the triangle of rows, and $[\ell', b)$. By induction, $Q_2$ is final.
- **Line L14, then COMPLETE$(a, m, b, m')$ for $Q_3$.** The gap of $Q_3$ is $[m, b) = [m, \ell') \cup [\ell', b)$. Line L14 adds the splits $k \in [\ell', b)$, with $T[i, k]$ in $Q_1$ and $T[k, j]$ for $\ell' \le k < b \le j < m'$ in the triangle of columns, all final. The triangles are $[a, m)$ and $[b, m')$. By induction, $Q_3$ is final.
- **Line L15, then line L16, COMPLETE$(\ell, a, b, m')$ for $Q_4$.** The gap of $Q_4$ is $[a, b) = [a, m) \cup [m, \ell') \cup [\ell', b)$. Line L15 adds $k \in [a, m)$, reading $T[i, k]$ in the triangle of rows and $T[k, j]$ in $Q_3$, and $k \in [\ell', b)$, reading $T[i, k]$ in $Q_2$ and $T[k, j]$ in the triangle of columns. All are final. The triangles are $[\ell, a)$ and $[b, m')$. By induction, $Q_4$ is final.

Each cell of the rectangle is in exactly one quadrant, so it is final at the end, and its $P$ cell equals $P^*$ by the induction hypothesis. The products write only into quadrants of our rectangle, and the recursive calls change nothing outside their own quadrants, so nothing outside the rectangle changes. $\square$

## Lemma 3: COMPUTE

Consider a call COMPUTE$(\ell, m)$ with $m - \ell$ a power of 2, and suppose that, when it starts, every cell $(i, j)$ with $\ell \le i < j < m$ has $P[i, j] = \emptyset$ and is empty in $T$ unless it is a terminal cell. Then, when it returns, $T[i, j] = T^*[i, j]$ for all $\ell \le i < j < m$, and no cell outside this triangle has changed.

*Proof.* By induction on $m - \ell$. If $m - \ell = 1$, there is no cell and line L5 does nothing. Otherwise let $h = (\ell + m)/2$. Line L6 fills the triangles $[\ell, h)$ and $[h, m)$, by induction, without touching the rectangle of rows $[\ell, h)$ and columns $[h, m)$. On that rectangle, $P$ is still empty, which is $P_{[h, h)}$ because the gap is empty, and the non-terminal cells are empty in $T$. So line L7 meets the conditions of Lemma 2 and fills the rectangle. The two triangles and the rectangle make up the whole triangle. $\square$

## Theorem

VALIANT$(G, w)$ stops and returns true exactly when $w \in L(G)$. When it stops, $T[i, j] = T^*[i, j]$ for all $0 \le i < j \le N$, so the table holds every nonterminal that derives every substring of $w$.

*Proof.* After line L1, the conditions of Lemma 3 hold for COMPUTE$(0, N)$, so after line L2 every cell is final. If $n = 0$, then $w = \varepsilon$, and in Chomsky normal form $S \Rightarrow^* \varepsilon$ only by the production $S \to \varepsilon$, which line L3 tests. If $n \ge 1$, line L4 returns whether $S \in T^*[0, n]$, that is, whether $S \Rightarrow^* w$.

Termination: every recursive call has half the side of its caller, so the depth of the recursion is at most $\log_2 N$ for COMPUTE plus $\log_2 N$ for COMPLETE, and every call makes at most four recursive calls and a bounded number of block products. $\square$

## Remark: the number of products

By induction on $s$, a call COMPLETE of side $s$ makes $s^2 / t^2$ block products of side $t$ for every power of 2 with $t \le s/2$: it makes 4 of side $s/2$ itself, and its four calls of side $s/2$ make $4 (s/2)^2 / t^2 = s^2 / t^2$ of each smaller side. COMPUTE$(0, N)$ makes $2^d$ calls of COMPLETE of side $N / 2^{d+1}$ for $d = 0, 1, \ldots$, so the number of block products of side $t$ is

$$\sum_{d \,:\, N / 2^{d+1} \ge 2t} 2^d \frac{N^2}{4^{d+1} t^2} = \frac{N}{t} \left( \frac{N}{2t} - 1 \right).$$

Each block product costs one Boolean matrix product of side $t$ per pair $(B, C)$, which gives the time bound of the page.
