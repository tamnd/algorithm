---
tag: 8Z57H1
kind: definition
slug: dyck-word
name: Dyck word
aliases:
- Balanced parentheses word
- Dyck path
- balanced bracket sequence
- well-formed parentheses
area: combinatorics/generating-partitions-and-trees
level: intro
summary: A string of matched parentheses (or up and down steps that never go below the axis); Dyck words encode ordered trees.
prereqs: [catalan-numbers]
see_also: [dyck-language, balanced-parentheses, reflection-principle, cycle-lemma, balanced-parentheses-generation, ordered-tree-generation, binary-tree-generation, level-sequence]
sources:
  - book: isbn:9780201038040
    title: Donald E. Knuth, The Art of Computer Programming, Volume 4A, Combinatorial Algorithms, Part 1
    locator: Section 7.2.1.6, Generating all trees (nested parentheses, their correspondence with forests and binary trees, and the path diagram)
  - book: isbn:9780201558029
    title: Ronald L. Graham, Donald E. Knuth and Oren Patashnik, Concrete Mathematics, second edition
    locator: Section 7.5, Convolutions (balanced sequences, the Catalan numbers and Raney's cycle lemma)
  - url: https://page.math.tu-berlin.de/~felsner/SemWS17-18/Ruskey-Comb-Gen.pdf
    title: Frank Ruskey, Combinatorial Generation, working version, University of Victoria, 1995 to 2003
    locator: Section 2.10.1, Ordered Trees (well-formed parentheses and their bijections with ordered and binary trees)
  - url: https://oeis.org/A000108
    title: OEIS A000108, Catalan numbers
    locator: the terms 1, 1, 2, 5, 14, 42, 132 and the list of Dyck path interpretations
---

A Dyck word of semilength $n$ is a string of $n$ opening and $n$ closing brackets in which no prefix has more closing than opening brackets. Drawn as a lattice path with an up step for each opening bracket and a down step for each closing bracket, it is a *Dyck path*: a path from height 0 back to height 0 that never goes below the axis. There are $C_n = \frac{1}{n+1}\binom{2n}{n}$ Dyck words of semilength $n$, the [Catalan numbers](/catalan-numbers/). They are the standard code for ordered trees, binary trees and many other Catalan families, and the set of all of them is the one-pair [Dyck language](/dyck-language/).

## Definition

Let $\Sigma = \{\texttt{(}, \texttt{)}\}$. For a word $w = w_1 \cdots w_m \in \Sigma^*$ and $0 \le i \le m$, the *height* (or *balance*) of the prefix of length $i$ is

$$h_i(w) = \#\{j \le i : w_j = \texttt{(}\} - \#\{j \le i : w_j = \texttt{)}\}.$$

**Dyck word.** $w$ is a Dyck word if $h_i(w) \ge 0$ for all $0 \le i \le m$ and $h_m(w) = 0$. Then $m = 2n$ is even, $w$ has exactly $n$ opening brackets, and $n$ is the *semilength*. The empty word $\varepsilon$ is the unique Dyck word of semilength 0. We write $D_n$ for the set of Dyck words of semilength $n$.

**Dyck path.** Read $\texttt{(}$ as the step $(1, 1)$ and $\texttt{)}$ as the step $(1, -1)$. The word $w$ becomes the path through the points $(i, h_i(w))$. The conditions say that the path starts and ends on the axis and never goes below it. Some authors write $U$ and $D$, or $1$ and $0$, for the two letters.

**Matching pairs.** In a Dyck word, the opening bracket at position $i$ is matched with the first position $j > i$ with $h_j = h_{i-1}$. Each bracket has exactly one partner, and two pairs are either nested or disjoint, never crossing. The *depth* or *height* of $w$ is $\max_i h_i(w)$.

**First-return decomposition.** Each nonempty Dyck word $w$ can be written in exactly one way as

$$w = \texttt{(}\, u \,\texttt{)}\, v, \qquad u, v \text{ Dyck words}.$$

*Proof.* Let $j$ be the least index $j \ge 1$ with $h_j = 0$. It exists because $h_{2n} = 0$. Then $w_1 = \texttt{(}$, since $h_1 \ge 0$ and $h_1 = \pm 1$. Also $w_j = \texttt{)}$, since $h_{j-1} \ge 1$ by the choice of $j$. Set $u = w_2 \cdots w_{j-1}$ and $v = w_{j+1} \cdots w_{2n}$. Inside $u$ the height is $h_i - 1 \ge 0$ for $1 \le i \le j - 1$, and it ends at $h_{j-1} - 1 = 0$, so $u$ is a Dyck word. The heights of $v$ are $h_i - h_j = h_i \ge 0$ for $i \ge j$, ending at 0, so $v$ is a Dyck word. Any other split $w = \texttt{(}u'\texttt{)}v'$ with Dyck words $u'$ and $v'$ returns to height 0 first after $\texttt{(}u'\texttt{)}$, so it has the same $j$ and the same parts. $\square$

The decomposition gives the recurrence $C_0 = 1$ and $C_{n+1} = \sum_{k=0}^{n} C_k C_{n-k}$, with $k$ the semilength of $u$.

**The count.** $|D_n| = \binom{2n}{n} - \binom{2n}{n-1} = \frac{1}{n+1}\binom{2n}{n}$ for $n \ge 0$.

*Proof.* A word with $n$ of each bracket that is not a Dyck word has a first index $i$ with $h_i = -1$. Swap every bracket in the suffix $w_{i+1} \cdots w_{2n}$, opening for closing and back. The suffix went from height $-1$ to height $0$, so after the swap it goes from $-1$ to $-2$, and the result has $n + 1$ closing and $n - 1$ opening brackets. This is a bijection onto all words with $n - 1$ opening and $n + 1$ closing brackets: such a word ends at height $-2$, so it has a first index with $h_i = -1$, and the same swap after that index maps it back. This is the [reflection principle](/reflection-principle/). So $|D_n| = \binom{2n}{n} - \binom{2n}{n-1}$, and $\binom{2n}{n-1} = \frac{n}{n+1}\binom{2n}{n}$ gives the second form. $\square$

**Standard order.** On this site, lists of Dyck words use [lexicographic order](/lexicographic-order/) with $\texttt{(} < \texttt{)}$. The first word of semilength $n$ is $\texttt{(}^n\texttt{)}^n$, the deepest one, and the last is $(\texttt{()})^n$, the flattest one.

## Examples and non-examples

**All words of semilength 3**, in lexicographic order, with $C_3 = 5$:

| word | heights $h_1, \ldots, h_6$ | depth | first-return split $\texttt{(}u\texttt{)}v$ |
|---|---|---|---|
| `((()))` | 1 2 3 2 1 0 | 3 | $u$ = `(())`, $v = \varepsilon$ |
| `(()())` | 1 2 1 2 1 0 | 2 | $u$ = `()()`, $v = \varepsilon$ |
| `(())()` | 1 2 1 0 1 0 | 2 | $u$ = `()`, $v$ = `()` |
| `()(())` | 1 0 1 2 1 0 | 2 | $u = \varepsilon$, $v$ = `(())` |
| `()()()` | 1 0 1 0 1 0 | 1 | $u = \varepsilon$, $v$ = `()()` |

The counts for $n = 0, 1, \ldots, 10$ are $1, 1, 2, 5, 14, 42, 132, 429, 1430, 4862, 16796$ (OEIS A000108). Of the $\binom{8}{4} = 70$ words with four brackets of each kind, $C_4 = 14$ are Dyck words and $\binom{8}{3} = 56$ are not.

**Non-examples.**

- `())(()`: the counts of each bracket are equal, but the prefix `())` has height $-1$.
- `(()`: no prefix goes below 0, but the final height is 1.
- `)(`: the first prefix already has height $-1$. The reflection of the proof swaps the suffix `(` and gives `))`, a word with no opening and two closing brackets.
- `([)]` with two kinds of brackets: each kind alone is balanced, but the pairs cross. It is not in the Dyck language on two kinds of brackets. With one kind of bracket, `(())` is a Dyck word, so crossing is a question only for several kinds.

**Codes for trees.** Three standard bijections use Dyck words of semilength $n$:

- **Ordered trees with $n + 1$ nodes.** Walk around the tree in depth-first order. Write `(` when the walk goes down an edge and `)` when it comes back up. The word `(()())` is the root with one child, and that child has two leaf children. This is the code of [ordered tree generation](/ordered-tree-generation/). The heights $h_i$ at the opening brackets are the depths of the non-root nodes, which is the [level sequence](/level-sequence/) of the tree.
- **Binary trees with $n$ nodes.** Map the empty tree to $\varepsilon$, and a node with left subtree $L$ and right subtree $R$ to $\texttt{(}\,\mathrm{code}(L)\,\texttt{)}\,\mathrm{code}(R)$. The first-return decomposition shows that this is a bijection. See [binary tree generation](/binary-tree-generation/).
- **Stack operations.** Read `(` as a push and `)` as a pop. A word of $n$ pushes and $n$ pops is a valid sequence of stack operations on an empty stack exactly when it is a Dyck word, which links Dyck words to [stack-sortable permutations](/stack-sortable-permutations/).

## Related definitions

- [Dyck language](/dyck-language/): the set of all Dyck words, a context-free language, and its form with several kinds of brackets.
- [Balanced parentheses](/balanced-parentheses/): the decision problem "is this word a Dyck word?", solved with a counter or a stack in linear time.
- [Catalan numbers](/catalan-numbers/): the counts $C_n$; [counting balanced bracket sequences](/counting-balanced-bracket-sequences/) is the counting problem.
- [Ballot theorem](/ballot-theorem/) and [ballot numbers](/ballot-number/): the number of prefixes of Dyck words, or of paths that stay above the axis, with a given end height. The table $d(i, j)$ of [bracket sequence ranking](/balanced-bracket-sequence-ranking/) holds these numbers.
- [Cycle lemma](/cycle-lemma/): among the $2n + 1$ rotations of a word with $n$ opening and $n + 1$ closing brackets, exactly one is a Dyck word followed by a closing bracket. This gives $C_n = \frac{1}{2n+1}\binom{2n+1}{n}$.
- [Level sequence](/level-sequence/): the list of node depths of an ordered tree in preorder, the same data as the heights of a Dyck word.
- Generation and ranking: [generating balanced parentheses](/balanced-parentheses-generation/), [next balanced bracket sequence](/next-balanced-bracket-sequence/), [ranking](/balanced-bracket-sequence-ranking/) and [unranking](/kth-balanced-bracket-sequence/), and [Zaks' sequences](/zaks-tree-generation/).
- [Succinct trees](/balanced-parentheses-representation/): an ordered tree with $n$ nodes stored as its Dyck word in $2n$ bits, with fast navigation.

## References
