---
tag: 05TNZG
kind: problem
slug: balanced-parentheses-generation
name: Generating balanced parentheses
aliases:
- Generating Dyck words
- Well-formed parentheses enumeration
- Generate parentheses
area: combinatorics/generating-partitions-and-trees
level: intro
summary: Enumerate all well-formed strings of n matched parenthesis pairs, which are counted by the Catalan numbers.
model: word-ram
complexity:
  vars: {n: the number of bracket pairs, N: the number of sequences (the Catalan number of n)}
  time: {worst: Θ(N)}
prereqs: [dyck-word, catalan-numbers, lexicographic-order]
see_also: [next-balanced-bracket-sequence, kth-balanced-bracket-sequence, balanced-bracket-sequence-ranking, counting-balanced-bracket-sequences, binary-tree-generation, ordered-tree-generation, constant-amortized-time-generation, generic-backtracking-algorithm]
sources:
  - book: isbn:9780201038040
    title: Donald E. Knuth, The Art of Computer Programming, Volume 4A, Combinatorial Algorithms, Part 1
    locator: Section 7.2.1.6, Generating all trees (Algorithm P, nested parentheses in lexicographic order)
  - url: https://page.math.tu-berlin.de/~felsner/SemWS17-18/Ruskey-Comb-Gen.pdf
    title: Frank Ruskey, Combinatorial Generation, working version, University of Victoria, 1995 to 2003
    locator: Section 4.6.1, Binary Trees, Ordered Trees (Algorithm 4.16, Theorem 4.1 and Lemma 4.4), Section 5.5.1, Well-formed Parentheses (Theorem 5.2), and the bibliographic remarks of Chapter 5 (Ruskey and Proskurowski 1990, Ruskey and Miller)
  - url: https://cp-algorithms.com/combinatorics/bracket_sequences.html
    title: cp-algorithms, Balanced bracket sequences
    locator: the sections on the next sequence, on the number of a sequence and on the k-th sequence
---

Generating balanced parentheses is the problem of listing every [Dyck word](/dyck-word/) of semilength $n$, that is, every string of $n$ opening and $n$ closing brackets in which no prefix has more closing than opening brackets, each exactly once. There are $N = C_n$ such strings, the $n$-th [Catalan number](/catalan-numbers/), so the output alone has $2nC_n$ characters. A lexicographic successor rule and a pruned backtracking search both solve it in $\Theta(N)$ total time when each string stays in one array and only the changes are written. Since Dyck words encode binary trees and ordered trees, the same algorithms list those [binary trees](/binary-tree-generation/) and [ordered trees](/ordered-tree-generation/).

## In plain words

You want every correct way to write a fixed number of bracket pairs, such as `(())` and `()()` for two pairs. A string is correct when, reading from left to right, you never close more brackets than you have opened, and at the end all brackets are closed.

The simple way is to build the string one character at a time. You may add an opening bracket while some are still unused. You may add a closing bracket while some opened bracket is still open. Every partial string built this way can still become a correct string, so the search never wastes work on a dead end.

A second way is to start from the first string in dictionary order and step to the next one each time, like an odometer. Each step changes only a short piece at the end on average.

## Definition

Fix $n \ge 0$. Let $D_n$ be the set of [Dyck words](/dyck-word/) of semilength $n$: words $w \in \{\texttt{(}, \texttt{)}\}^{2n}$ whose prefix heights $h_i(w) = \#\texttt{(} - \#\texttt{)}$ in $w_1 \cdots w_i$ satisfy $h_i \ge 0$ for all $i$ and $h_{2n} = 0$.

**Input:** an integer $n \ge 0$.

**Output:** a sequence $w^{(1)}, \ldots, w^{(N)}$ that contains each word of $D_n$ exactly once, with $N = |D_n| = C_n = \frac{1}{n+1}\binom{2n}{n}$.

**Cost model.** The [word RAM](/word-ram/). The current word lives in one array of $2n$ cells, and the algorithm visits it after each step. The cost of a step is the number of cells read and written, not $2n$. When each word must be copied out, add $2n$ per word. This is the usual convention of [constant amortized time](/constant-amortized-time-generation/) generation.

## Variants

- **Lexicographic order.** With $\texttt{(} < \texttt{)}$ the list starts at $\texttt{(}^n\texttt{)}^n$ and ends at $(\texttt{()})^n$. The step from one word to the next is [next balanced bracket sequence](/next-balanced-bracket-sequence/).
- **Gray code order.** Consecutive words differ by a small change, for example by one transposition of an opening and a closing bracket.
- **Direct access.** Compute the position of a word in the list ([ranking](/balanced-bracket-sequence-ranking/)), or the word at a given position ([unranking](/kth-balanced-bracket-sequence/)). See [ranking and unranking](/ranking-unranking/).
- **Counting.** Compute only $N$. This is [counting balanced bracket sequences](/counting-balanced-bracket-sequences/).
- **Restricted words.** Words with depth at most $k$, words with a given prefix, or words with several kinds of brackets. With $t$ kinds of brackets there are $t^n C_n$ words, because each matched pair picks its kind independently.
- **Random generation.** Draw one word of $D_n$ uniformly at random, for example by unranking a uniform integer in $[0, C_n)$.

## Examples

For $n = 3$ the $C_3 = 5$ words in lexicographic order are `((()))`, `(()())`, `(())()`, `()(())` and `()()()`.

For $n = 4$ the $C_4 = 14$ words in lexicographic order, with ranks 0 to 13, are `(((())))`, `((()()))`, `((())())`, `((()))()`, `(()(()))`, `(()()())`, `(()())()`, `(())(())`, `(())()()`, `()((()))`, `()(()())`, `()(())()`, `()()(())` and `()()()()`.

The table compares three sizes. The column "words with $n$ of each" is $\binom{2n}{n}$, the number of candidates of a generate-and-test method that places $n$ opening brackets in $2n$ positions. The last column is the number of nodes of the pruned search tree (prefixes of Dyck words, the empty prefix included).

| $n$ | $C_n$ | words with $n$ of each | nodes of the pruned search |
|---|---|---|---|
| 1 | 1 | 2 | 3 |
| 2 | 2 | 6 | 8 |
| 3 | 5 | 20 | 22 |
| 4 | 14 | 70 | 64 |
| 5 | 42 | 252 | 196 |
| 6 | 132 | 924 | 625 |
| 7 | 429 | 3432 | 2055 |
| 8 | 1430 | 12870 | 6917 |

Since $\binom{2n}{n} = (n+1) C_n$, the generate-and-test method tests $n + 1$ candidates for each word that it keeps. The pruned search has fewer than $6$ nodes per word in this range.

## Known algorithms

| method | order | cost of the full listing | worst step |
|---|---|---|---|
| [generate and test](/generate-and-test/) on $\binom{2n}{n}$ placements | any | $(n+1) C_n$ tests of $O(n)$ each | $O(n)$ |
| pruned [backtracking](/generic-backtracking-algorithm/) | lexicographic | $\Theta(C_n)$ | $O(n)$ |
| [lexicographic successor](/next-balanced-bracket-sequence/) | lexicographic | $\Theta(C_n)$ | $O(n)$ |
| [unrank](/kth-balanced-bracket-sequence/) each $k = 0, \ldots, C_n - 1$ | lexicographic | $\Theta(n C_n)$ | $O(n)$ |
| Gray code by transpositions (Ruskey and Proskurowski 1990) | one transposition per step | see Ruskey, Section 5.5.1 | see Ruskey, Section 5.5.1 |

- **Pruned backtracking.** Extend a prefix with $\texttt{(}$ while it has fewer than $n$ opening brackets, and with $\texttt{)}$ while its height is positive. Each node of the search tree is a prefix of some Dyck word, so no branch dies. With $\texttt{(}$ tried first, the leaves come in lexicographic order. The number of new nodes on the path to a leaf equals the number of cells that the lexicographic successor reads for the same step, so the search tree has $1 + \sum_w \mathrm{cost}(w)$ nodes, where $\mathrm{cost}(w)$ is the scan length of the successor rule.
- **Lexicographic successor.** From the right end, find the last opening bracket that can turn into a closing one, turn it, and fill the rest with the smallest completion. One step reads $2 + h + 2j$ cells, where the word ends in $\texttt{(}\,\texttt{)}^{h+1}(\texttt{()})^j$. This is at most twice the length of the final run of closing brackets of the next word, plus 2. The final runs of all words of $D_n$ have total length $\frac{3n}{n+2} C_n$ (by reversal, this is Ruskey's Theorem 4.1 on the first run), so the average step reads fewer than $8 + 2n/C_n$ cells. The proof is on the page of the algorithm.
- **Recursion by the first return.** Every nonempty word is $\texttt{(}u\texttt{)}v$ for unique Dyck words $u$ and $v$. Listing all pairs $(u, v)$ with $|u| + |v| = 2n - 2$ lists $D_n$. This is the natural method when the words stand for binary trees.
- **Gray codes.** Ruskey and Proskurowski give a list in which consecutive words differ by swapping one opening and one closing bracket. For the words that start with $\texttt{(}^k\texttt{)}$, Ruskey and Miller showed that no such list with *adjacent* swaps exists when $n$ is even, or when $n > 5$ is odd and $k$ is odd, except for $k \in \{0, 1, n - 1, n\}$ (Ruskey, Section 5.5.1).

## Bounds

- Any algorithm that visits each word does at least one step per word, so $\Omega(N)$ time is necessary. The lexicographic successor and the pruned search meet this bound, so the problem takes $\Theta(N)$ time in the cost model above.
- If each word must be written out in full, the output has $2nN$ characters, and $\Theta(nN)$ time is necessary and enough.
- The size grows as $C_n \sim \frac{4^n}{\sqrt{\pi}\, n^{3/2}}$. So $n = 20$ already gives $C_{20} = 6564120420$ words, and only small $n$ are practical for a full listing.
- Each single step of the lexicographic successor can take $\Theta(n)$ time, for example from $\texttt{(())}(\texttt{()})^{n-2}$ to $\texttt{()(}^{n-1}\texttt{)}^{n-1}$, which rewrites $2n - 1$ cells. So a loopless algorithm, with $O(1)$ time for every step, that keeps the word in an array must use an order in which consecutive words differ in $O(1)$ cells, a [Gray code](/gray-code/).

## Reductions

- **Binary trees and ordered trees.** The map $\varnothing \mapsto \varepsilon$, $(L, R) \mapsto \texttt{(}\,\mathrm{code}(L)\,\texttt{)}\,\mathrm{code}(R)$ is a bijection from binary trees with $n$ nodes to $D_n$, and the depth-first walk of an ordered tree with $n + 1$ nodes is another bijection. A generator for one family gives a generator for the other with $O(n)$ extra time per object, or $O(1)$ amortized when the change is local. See [binary tree generation](/binary-tree-generation/) and [ordered tree generation](/ordered-tree-generation/).
- **Other Catalan families.** Triangulations of a convex polygon with $n + 2$ sides ([Catalan triangulation theorem](/catalan-triangulation-theorem/)), full parenthesizations of a product of $n + 1$ factors ([counting parenthesizations](/counting-parenthesizations/)) and [stack-sortable permutations](/stack-sortable-permutations/) of length $n$ are also in bijection with $D_n$.
- **From unranking.** If unranking takes time $U(n)$, calling it for $k = 0, 1, \ldots, N - 1$ lists $D_n$ in time $N \cdot U(n)$.

## Applications

- Exhaustive tests of code that handles trees, parsers or expressions, on every input shape up to a given size.
- Listing all shapes of binary search trees, all evaluation orders of a chain of matrix products, or all triangulations of a small polygon.
- A standard exercise in [backtracking](/generic-backtracking-algorithm/), because the pruning rule is short and provably wastes no work.

## References
