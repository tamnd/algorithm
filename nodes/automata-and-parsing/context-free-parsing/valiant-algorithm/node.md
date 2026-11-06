---
tag: 44TRAH
kind: algorithm
slug: valiant-algorithm
name: Valiant's algorithm
aliases:
- Valiant parser
area: automata-and-parsing/context-free-parsing
level: research
summary: Reduces CFG recognition to Boolean matrix multiplication, giving sub-cubic time.
solves: [context-free-language-recognition]
model: word-ram
complexity:
  vars: {n: the input length, g: the grammar size, ω: an exponent above 2 such that n by n Boolean matrices multiply in O(n^ω) time}
  time: {worst: O(g n^ω), best: Θ(g n^2)}
  space: {extra: O(g n^2)}
properties: {deterministic: true, recursive: true, online: false}
history:
  year: 1975
  people: [Leslie G. Valiant]
  note: Valiant showed that the CYK table is a transitive closure that can be computed with fast Boolean matrix multiplication, the first general context-free recognizer faster than cubic; Rytter and Okhotin later gave simpler formulations.
prereqs: [cyk-algorithm, boolean-matrix-multiplication, chomsky-normal-form]
see_also: [valiant-lee-theorem, strassen-algorithm, matrix-multiplication-exponent, four-russians-method, transitive-closure, combinatorial-bmm-conjecture, earley-parser, chomsky-normal-form-conversion]
sources:
  - paper: doi:10.1016/S0022-0000(75)80046-8
    title: Leslie G. Valiant, General context-free recognition in less than cubic time, Journal of Computer and System Sciences 10(2) (1975)
    locator: pp. 308 to 315
  - paper: doi:10.1016/j.tcs.2013.09.011
    title: Alexander Okhotin, Parsing by matrix multiplication generalized to Boolean grammars, Theoretical Computer Science 516 (2014)
    locator: pp. 101 to 120 (the recursive procedures compute and complete, their correctness and their running time)
  - paper: doi:10.1016/0304-3975(94)00265-k
    title: Wojciech Rytter, Context-free recognition via shortest paths computation, a version of Valiant's algorithm, Theoretical Computer Science 143(2) (1995)
    locator: pp. 343 to 352
  - paper: doi:10.1145/505241.505242
    title: Lillian Lee, Fast context-free grammar parsing requires fast Boolean matrix multiplication, Journal of the ACM 49(1) (2002)
    locator: pp. 1 to 15
  - paper: doi:10.1137/16m1061771
    title: Amir Abboud, Arturs Backurs and Virginia Vassilevska Williams, If the current clique algorithms are optimal, so is Valiant's parser, SIAM Journal on Computing 47(6) (2018)
    locator: pp. 2527 to 2555
---

Valiant's algorithm decides whether a string of length $n$ is in the language of a [context-free grammar](/context-free-grammar/) by computing the table of the [CYK algorithm](/cyk-algorithm/) with [Boolean matrix multiplication](/boolean-matrix-multiplication/) instead of three nested loops. With [Strassen's algorithm](/strassen-algorithm/) it takes $O(|G|\, n^{2.81})$ time, and with the best known matrix products $O(|G|\, n^{\omega})$ for any $\omega$ above the [matrix multiplication exponent](/matrix-multiplication-exponent/), which is less than 2.372. Leslie Valiant published it in 1975; it was the first general context-free recognizer faster than cubic, and it is still the asymptotically fastest one known. The method is mainly of theoretical interest: its products pay off only for very long inputs, and Lee showed that no general parser of the same kind can be much faster unless matrix multiplication is.

## In plain words

The CYK method fills a triangle of boxes. The box for a stretch of the input says which grammar symbols can produce that stretch. A box is found by trying every place to cut the stretch in two and looking at the boxes of the two halves.

Valiant groups this work. He cuts the triangle into big square blocks and asks, for a whole block at once, which cuts are possible through a whole other block. That question is the same as multiplying two tables of yes and no values, and there are fast tricks for multiplying such tables.

The difficulty is the order: a block may only be used after its boxes are complete. The algorithm splits the triangle in half again and again and handles the four quarters of each square in a fixed order, so that every block it reads is already finished.

## The problem

We use the notation of the [context-free grammar](/context-free-grammar/) page: productions $A \to \alpha \mid \beta$, $\varepsilon$ for the empty string, $S$ for the start symbol, $n$ for the input length and $|G|$ for the grammar size. Given a grammar $G$ and a string $w = a_1 \cdots a_n$, decide whether $w \in L(G)$; this is [context-free language recognition](/context-free-language-recognition/).

The grammar must be in [Chomsky normal form](/chomsky-normal-form/): every production is $A \to BC$ or $A \to a$, plus $S \to \varepsilon$ when $S$ is on no right side. Any grammar can be brought to this form with a [conversion](/chomsky-normal-form-conversion/) that keeps the language and makes the grammar at most quadratically larger.

The algorithm fills the same table as CYK. For positions $0 \le i < j \le n$,

$$T[i, j] = \{ A : A \Rightarrow^* a_{i+1} \cdots a_j \},$$

and $w \in L(G)$ exactly when $S \in T[0, n]$ (or, for $n = 0$, when $S \to \varepsilon$ is a production). For $j \ge i + 2$, CYK computes

$$P[i, j] = \{ (B, C) : B \in T[i, k],\ C \in T[k, j] \text{ for some } k \text{ with } i < k < j \}, \qquad T[i, j] = \{ A : A \to BC,\ (B, C) \in P[i, j] \}.$$

For one pair $(B, C)$, the matrix of $P$ restricted to that pair is a Boolean matrix product: if $X_B[i, k]$ is 1 when $B \in T[i, k]$, then the pair is in $P[i, j]$ when $(X_B X_C)[i, j] = 1$. The catch is that $X_B$ and $X_C$ are the table being computed, so the products must be arranged so that each one reads only finished cells.

## The algorithm

We pad the positions $0, \ldots, n$ to $0, \ldots, N - 1$, where $N$ is the least power of 2 with $N \ge n + 1$; cells beyond the input stay empty. For blocks of cells, $X \cdot Y$ is the matrix whose cell $[i, j]$ holds the pairs $(B, C)$ with $B \in X[i, k]$ and $C \in Y[k, j]$ for some shared index $k$. It is computed by one Boolean matrix product for each pair $(B, C)$ that is the right side of a production. $T[r_0{:}r_1, c_0{:}c_1]$ is the block of rows $r_0, \ldots, r_1 - 1$ and columns $c_0, \ldots, c_1 - 1$.

The recursion is the one of Okhotin (2014). COMPUTE$(\ell, m)$ finishes the triangle of cells $(i, j)$ with $\ell \le i < j < m$. COMPLETE$(\ell, m, \ell', m')$, with $m \le \ell'$, finishes the square of rows $[\ell, m)$ and columns $[\ell', m')$, assuming that the triangles over $[\ell, m)$ and over $[\ell', m')$ are finished and that $P$ already holds the splits $k$ in the gap $[m, \ell')$ between them.

```pseudo id=main
VALIANT(G, w)                                  ▷ G in Chomsky normal form
L1  T[i, i+1] ← {A : A → a_{i+1}} for 0 ≤ i < n; all other cells of T and P are empty
L2  COMPUTE(0, N)                              ▷ N: least power of 2 with N ≥ n + 1
L3  if n = 0 then return whether S → ε is in G
L4  return S ∈ T[0, n]

COMPUTE(ℓ, m)                                  ▷ finishes T[i, j] for ℓ ≤ i < j < m
L5  if m − ℓ ≥ 2 then
L6      h ← (ℓ + m)/2; COMPUTE(ℓ, h); COMPUTE(h, m)
L7      COMPLETE(ℓ, h, h, m)

COMPLETE(ℓ, m, ℓ', m')                         ▷ rows [ℓ, m), columns [ℓ', m'), gap [m, ℓ') done
L8  if m − ℓ = 1 then
L9      if ℓ' ≥ ℓ + 2 then T[ℓ, ℓ'] ← {A : A → BC with (B, C) ∈ P[ℓ, ℓ']}
L10     return
L11 a ← (ℓ + m)/2; b ← (ℓ' + m')/2
L12 COMPLETE(a, m, ℓ', b)                      ▷ the quarter nearest the diagonal
L13 P[ℓ:a, ℓ':b] ∪= T[ℓ:a, a:m] · T[a:m, ℓ':b]; COMPLETE(ℓ, a, ℓ', b)
L14 P[a:m, b:m'] ∪= T[a:m, ℓ':b] · T[ℓ':b, b:m']; COMPLETE(a, m, b, m')
L15 P[ℓ:a, b:m'] ∪= T[ℓ:a, a:m] · T[a:m, b:m'] ∪ T[ℓ:a, ℓ':b] · T[ℓ':b, b:m']
L16 COMPLETE(ℓ, a, b, m')                      ▷ the farthest quarter last
```

In a call of COMPLETE, the splits of a cell $(i, j)$ of the square fall into three ranges: $k < m$ (through the triangle of rows), $k$ in the gap (already in $P$), and $k \ge \ell'$ (through the triangle of columns). Lines L13 to L15 add, for each quarter, exactly the splits that become available when the quarters before it are finished. Line L12 needs nothing new, because its gap is the gap of the caller. Each quarter is a call of the same kind with half the side, so the recursion has depth $O(\log n)$.

The implementation keeps one Boolean matrix per nonterminal for $T$ and one per pair $(B, C)$ for $P$, with each row stored as an integer used as a bitset. The multiplication is a parameter; the default ORs the rows of the second factor selected by the set bits of each row of the first. It also skips a product when one factor is all zero, and it converts any grammar to Chomsky normal form first if asked.

## Example

Take the grammar of the [CYK](/cyk-algorithm/) page, from Hopcroft, Motwani and Ullman,

$$S \to AB \mid BC, \qquad A \to BA \mid a, \qquad B \to CC \mid b, \qquad C \to AB \mid a,$$

and $w = baaba$, so $n = 5$ and $N = 8$. The table is the one CYK computes; with 0-based spans:

| length | $(0, \cdot)$ | $(1, \cdot)$ | $(2, \cdot)$ | $(3, \cdot)$ | $(4, \cdot)$ |
| --- | --- | --- | --- | --- | --- |
| 1 | $\{B\}$ | $\{A, C\}$ | $\{A, C\}$ | $\{B\}$ | $\{A, C\}$ |
| 2 | $\{A, S\}$ | $\{B\}$ | $\{C, S\}$ | $\{A, S\}$ | |
| 3 | $\emptyset$ | $\{B\}$ | $\{B\}$ | | |
| 4 | $\emptyset$ | $\{A, C, S\}$ | | | |
| 5 | $\{A, C, S\}$ | | | | |

So $S \in T[0, 5]$ and $baaba \in L(G)$. What differs from CYK is the order of the cells. The 8 positions $0, \ldots, 7$ give 28 cells $(i, j)$ with $i < j \le 7$; 7 of them are terminal cells (t) set by line L1, and the other 21 are finished by line L9 in this order (columns 6 and 7 are padding and end up empty):

| $i$ \ $j$ | 1 | 2 | 3 | 4 | 5 | 6 | 7 |
| --- | --- | --- | --- | --- | --- | --- | --- |
| 0 | t | 1 | 3 | 11 | 13 | 19 | 21 |
| 1 | | t | 2 | 10 | 12 | 18 | 20 |
| 2 | | | t | 7 | 9 | 15 | 17 |
| 3 | | | | t | 8 | 14 | 16 |
| 4 | | | | | t | 4 | 6 |
| 5 | | | | | | t | 5 |
| 6 | | | | | | | t |

COMPUTE$(0, 4)$ finishes the triangle over positions 0 to 3 (cells 1 to 3), COMPUTE$(4, 8)$ the triangle over 4 to 7 (cells 4 to 6), and COMPLETE$(0, 4, 4, 8)$ the square of rows 0 to 3 and columns 4 to 7, one quarter at a time: rows 2 and 3 with columns 4 and 5 (cells 7 to 9), then rows 0 and 1 with columns 4 and 5 (10 to 13), then rows 2 and 3 with columns 6 and 7 (14 to 17), and last rows 0 and 1 with columns 6 and 7 (18 to 21).

Follow the cell $(0, 5)$, which has the splits $k = 1, 2, 3, 4$. It lies in the second quarter of the top call, so line L13 of COMPLETE$(0, 4, 4, 8)$ brings in $k = 2$ and $k = 3$ with a product of $2 \times 2$ blocks, $T[0{:}2, 2{:}4] \cdot T[2{:}4, 4{:}6]$. Inside COMPLETE$(0, 2, 4, 6)$ the cell is in the last quarter, and line L15 brings in $k = 1$ through $T[0{:}1, 1{:}2] \cdot T[1{:}2, 5{:}6]$ and $k = 4$ through $T[0{:}1, 4{:}5] \cdot T[4{:}5, 5{:}6]$. The split $k = 1$ gives the pairs $(B, A)$, $(B, C)$ and $(B, S)$, from $T[0, 1] = \{B\}$ and $T[1, 5] = \{A, C, S\}$, and the productions $A \to BA$ and $S \to BC$ put $A$ and $S$ into $T[0, 5]$. The split $k = 2$ gives $(A, B)$ and $(S, B)$, from $T[0, 2] = \{A, S\}$ and $T[2, 5] = \{B\}$, and $C \to AB$ adds $C$. The splits $k = 3$ and $k = 4$ give nothing, because $T[0, 3]$ and $T[0, 4]$ are empty. So $T[0, 5] = \{A, C, S\}$.

Over the whole run there are 24 block products of side 1 and 4 of side 2, for each pair $(B, C)$, and the implementation makes 15 actual Boolean products, because it skips the ones with an all-zero factor. The tests check the table, the order of the cells, the products for $(0, 5)$ and these counts.

## Correctness

The full proof is in [proofs/correctness.md](proofs/correctness.md). In Chomsky normal form, a string of length at least 2 is derived from $A$ exactly when it splits into two nonempty parts derived by $B$ and $C$ for some production $A \to BC$, so a cell is right when its $P$ cell holds the pairs of all its splits and the cells it reads are right.

The main lemma is about COMPLETE$(\ell, m, \ell', m')$: if the two triangles are finished and $P$ holds exactly the splits in the gap $[m, \ell')$, then the call finishes its square, and it changes nothing outside it. The proof is by induction on the side. For a single cell, all its splits lie in the gap, so line L9 is the CYK rule. For a larger square, each quarter's gap is the caller's gap plus the ranges added by lines L13 to L15, and each of these products reads only cells of the two triangles or of quarters finished before; for example, the farthest quarter needs the splits through the triangle of rows, which pass through the third quarter, and the splits through the triangle of columns, which pass through the second. COMPUTE then finishes a triangle from its two halves and the square between them, whose gap is empty.

## Complexity

Let $M(t)$ be the time to multiply two $t \times t$ Boolean matrices, and let $p \le |G|$ be the number of distinct pairs $(B, C)$ on right sides. A call of COMPLETE of side $s$ makes 4 block products of side $s/2$ and 4 calls of side $s/2$, and COMPUTE of side $s$ makes 2 calls of side $s/2$ and one COMPLETE of side $s/2$. Counting through the recursion, COMPUTE$(0, N)$ makes

$$\frac{N}{t} \left( \frac{N}{2t} - 1 \right)$$

block products of side $t$, for $t = 1, 2, 4, \ldots, N/4$:

| $N$ | side 1 | side 2 | side 4 | side 8 | side 16 |
| --- | --- | --- | --- | --- | --- |
| 8 | 24 | 4 | | | |
| 16 | 112 | 24 | 4 | | |
| 32 | 480 | 112 | 24 | 4 | |
| 64 | 1984 | 480 | 112 | 24 | 4 |

Each block product is $p$ Boolean products, so the products cost $p \sum_t \frac{N^2}{2t^2} M(t)$. If $M(t) = O(t^\omega)$ with $\omega > 2$, the terms grow geometrically with $t$ and the largest side, $t = N/4$, dominates: the total is $O(p\, N^\omega) = O(|G|\, n^\omega)$. The $N^2/2$ cells at line L9 cost $O(p)$ each, which adds $O(|G|\, n^2)$. With the naive product, $M(t) = \Theta(t^3)$ and the algorithm takes $\Theta(|G|\, n^3)$ time like CYK; with [Strassen's algorithm](/strassen-algorithm/), $O(|G|\, n^{2.81})$. If $M$ grows only like $t^2$ times a slowly growing factor, the sum loses at most a factor $\log n$.

The space is the tables $T$ and $P$: one $N \times N$ Boolean matrix per nonterminal and per pair, $O(|G|\, n^2)$ cells; with bitset rows, each machine word holds many cells. The products need temporary blocks of at most the same size. The recursion depth is $2 \log_2 N$.

The best case of the implementation is $\Theta(|G|\, n^2)$: when all blocks are zero, every product is skipped, and only the cell updates remain. The worst case of the plain pseudocode does not depend on the input beyond $n$ and $|G|$.

## Properties

- **Computes the whole table.** Like CYK, it finds every nonterminal for every substring, not only the answer for $S$. That is the c-parsing output that [Lee's theorem](/valiant-lee-theorem/) is about, and a parse tree can be read back from it in $O(|G|\, n^2)$ further time by trying the splits of each cell.
- **Not online.** All of $w$ must be known before the first product, and the result for a prefix is not available early.
- **Deterministic, exact and combinatorial in structure.** The only nonclassical part is the matrix product, which can be any algorithm; a fast one usually works over the integers and thresholds the result.
- **Needs Chomsky normal form.** Lines L1 and L9 rely on binary productions and no $\varepsilon$ inside.

## Variants and improvements

- **Valiant's original formulation.** Valiant phrased the problem as the transitive closure of an upper triangular matrix over a nonassociative product of sets of nonterminals, and showed that this closure can be computed in the time of a constant number of matrix products of decreasing sizes, by a divide and conquer close to the one above. The original is harder to read; the version here follows Okhotin.
- **Rytter's version.** Rytter (1995) gave a simpler presentation in terms of shortest paths and a simpler proof, with the same bound.
- **Boolean and conjunctive grammars.** Okhotin (2014) showed that the same recursion works for conjunctive and Boolean grammars, which add intersection and complement to the rules, because each cell still depends only on the pairs of its splits.
- **Combinatorial speedups.** Without algebraic matrix multiplication, the [method of four Russians](/four-russians-method/) gives $M(t) = O(t^3 / \log t)$, and the same recursion then takes $O(|G|\, n^3 / \log n)$ time. Abboud, Backurs and Vassilevska Williams show that a combinatorial algorithm much faster than cubic would give faster combinatorial [clique](/clique-decision/) algorithms.
- **Probabilistic grammars.** For the most probable parse, the products become max-times or min-plus products, which have no known truly subcubic algorithm; Valiant's method does not speed up the probabilistic CKY in general.

## When to use it

Almost never in practice. The method is the reason we know that general context-free recognition is not inherently cubic, and it shows that recognition is no harder than Boolean matrix multiplication. For real inputs, the constant factors of fast matrix multiplication and the cost of converting to Chomsky normal form make the [CYK algorithm](/cyk-algorithm/), the [Earley parser](/earley-parser/) or GLR faster, and deterministic grammars admit linear-time parsers. A bitset version of the recursion can help for long inputs and small grammars, where the products become word operations, but a bitset CYK gets most of the same gain more simply.

## Pitfalls

- **Wrong order of the quarters.** The farthest quarter needs both the second and the third quarters; doing it before either one reads unfinished cells and silently misses parses. The near quarter must come first.
- **Splits counted twice or missed.** Each split $k$ of a cell must be added in exactly one product. A common slip is to include the gap twice, or to forget the range $[\ell', b)$ at line L15.
- **Forgetting the padding.** The recursion needs a power of 2 for the number of positions, which is $n + 1$, not $n$. The padding cells must stay empty, so the padding must not match any terminal.
- **Non-CNF input.** A unit production or an $\varepsilon$-production inside the grammar breaks the rule of line L9, and the table is then wrong without any error. Convert first, and treat the empty input separately.
- **Expecting a speedup.** The products of small blocks dominate in practice; with $n$ in the thousands, a well-written cubic parser is faster.
- **Counting instead of OR.** Fast matrix products such as Strassen's work over the integers, where an entry counts the splits. The entry must be turned back into a Boolean (nonzero or zero) before it is used, and the counts can grow to $n$, so they must not overflow a small integer type.

## Implementations

## History

Kasami and Younger had shown in the 1960s that context-free recognition takes $O(n^3)$ time, and for a decade no general method was known to be faster. Leslie Valiant showed in 1975 that the CYK table is the transitive closure of a triangular matrix under a nonassociative product, and that this closure can be computed with Boolean matrix multiplication, so Strassen's algorithm gives $O(n^{2.81})$ recognition. Rytter (1995) and Okhotin (2014) gave simpler formulations, the latter extended to Boolean grammars. In the other direction, Lillian Lee showed in 1997 (journal version 2002) that a fast general parser yields fast Boolean matrix multiplication, and Abboud, Backurs and Vassilevska Williams showed in 2015 that even for one fixed grammar, recognition faster than Valiant's method would give faster algorithms for finding cliques.

## References
