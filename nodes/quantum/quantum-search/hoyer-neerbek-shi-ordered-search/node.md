---
tag: M3Z7WG
kind: algorithm
slug: hoyer-neerbek-shi-ordered-search
name: Høyer-Neerbek-Shi ordered search
aliases:
- HNS ordered search
area: quantum/quantum-search
level: research
summary: An exact quantum algorithm that finds the first 1 in a monotone string of N bits with log_3 N + O(1), about 0.631 log2 N, queries. Binary search needs log2 N.
solves: [quantum-ordered-search]
model: quantum-query-model
complexity:
  vars: {N: the length of the sorted list}
  queries: {worst: log_3 N + O(1)}
  space: {extra: O((log N)^2)}
properties: {deterministic: true, exact: true, oracle: bit}
history:
  year: 2001
  people: [Peter Høyer, Jan Neerbek, Yaoyun Shi]
  note: Presented at ICALP 2001 together with the lower bound (1/pi)(ln N - 1); the journal version appeared in Algorithmica in 2002.
prereqs: [quantum-ordered-search, binary-search, quantum-oracle, phase-kickback]
see_also: [quantum-query-complexity, quantum-adversary-method, search-lower-bound, grover-search, unstructured-search]
sources:
  - paper: doi:10.1007/3-540-48224-5_29
    title: "Peter Høyer, Jan Neerbek and Yaoyun Shi, Quantum complexities of ordered searching, sorting, and element distinctness, Proceedings of ICALP 2001, LNCS 2076, pages 346-357"
    locator: Section 4 (the algorithm), with the numbering of arXiv:quant-ph/0102078v2, Lemma 11 (the fair and tight covering), Lemma 12 (the recursion) and Theorem 13 (exact, log_3 N + O(1) queries); Theorem 1 (the lower bound)
  - paper: doi:10.1007/s00453-002-0976-3
    title: "Peter Høyer, Jan Neerbek and Yaoyun Shi, Quantum complexities of ordered searching, sorting, and element distinctness, Algorithmica 34(4), 2002, pages 429-448"
    locator: the journal version; this page follows the arXiv version for its numbering
  - paper: arxiv:quant-ph/9901059
    title: "Edward Farhi, Jeffrey Goldstone, Sam Gutmann and Michael Sipser, Invariant quantum algorithms for insertion into an ordered list, arXiv:quant-ph/9901059, 1999"
    locator: the whole paper (the earlier exact algorithm with about 0.526 log2 N queries)
  - paper: doi:10.1103/PhysRevA.75.032335
    title: "Andrew M. Childs, Andrew J. Landahl and Pablo A. Parrilo, Quantum algorithms for the ordered search problem via semidefinite programming, Physical Review A 75, 032335, 2007"
    locator: the abstract and the main result (exact, about 0.433 log2 N queries)
  - paper: doi:10.1109/FOCS.2008.58
    title: "Michael Ben-Or and Avinatan Hassidim, The Bayesian learner is optimal for noisy binary search (and pretty good for quantum as well), Proceedings of the 49th IEEE FOCS, 2008, pages 221-230"
    locator: the quantum part (zero error, about 0.32 log2 N expected queries); section not checked
---

The Høyer-Neerbek-Shi algorithm solves [quantum ordered search](/quantum-ordered-search/): given a monotone bit string $x_0 \le x_1 \le \cdots \le x_{N-1}$ with $x_{N-1} = 1$ through a [quantum oracle](/quantum-oracle/), find the first position $f(x)$ with $x_{f(x)} = 1$. It is *exact*: it outputs $f(x)$ with probability 1, and it makes at most $\log_3 N + O(1) \approx 0.631 \lg N$ queries, against $\lceil \lg N \rceil$ for [binary search](/binary-search/). Its idea is to run several smaller searches in parallel, one for each "color" of a pebbling of the search tree, and then combine their answers with one more query by interference. Høyer, Neerbek and Shi stated it in the same 2001 paper as the lower bound $\frac{1}{\pi}(\ln N - 1) \approx 0.221 \lg N$. The algorithm does not meet that bound; other exact algorithms use fewer queries (see Variants).

## In plain words

Binary search on a sorted list asks one question and throws away half of the list. To find an item among a thousand, it asks ten questions.

This method splits the list in a cleverer way. It marks the nodes of the binary search tree with several colors, so that every path from the top to the bottom crosses each color once. For each color, the colored nodes cut the list into pieces. Finding the right piece is a smaller sorted search, about a third of the size. The quantum computer does these smaller searches for all colors at the same time. Each one tells where the item is at a different level of the tree. One last question, used on all these levels together, makes the wrong answers cancel and leaves only the right item. So each round cuts the list to about a third instead of a half.

## The problem

The input is $N$ and a monotone string $x \in \{0,1\}^N$ with $x_{N-1} = 1$, so the answer $f(x) = \min\{i : x_i = 1\}$ exists. The algorithm uses the bit oracle $O_x|i\rangle|b\rangle = |i\rangle|b \oplus x_i\rangle$, and also its phase form $(-1)^{x_i}$, made with the same call and an ancilla in the state $(|0\rangle - |1\rangle)/\sqrt{2}$ by [phase kickback](/phase-kickback/). The cost is the number of oracle calls in the [quantum query model](/quantum-query-model/), and the result is exact. A sorted array with a key gives such a string by $x_i = [y_i \ge z]$; see the problem page.

## The algorithm

**The tree.** Label the $N$ leaves of a binary tree $T$ with $0, \ldots, N-1$ from left to right. For an internal vertex $v$, let $i(v)$ be the rightmost leaf of its left subtree. Binary search walks down from the root and at $v$ goes left if $x_{i(v)} = 1$ and right otherwise; it ends at the leaf $f(x)$. For a vertex $u$ let $\Phi_u = \sum_{\ell} 2^{-d(u,\ell)/2} |\ell\rangle$, the sum over the leaves $\ell$ below $u$ at distance $d(u, \ell)$. In a complete subtree this is the uniform state on the leaves of $u$.

**The pebbling.** Put pebbles of $2^s$ colors on internal vertices so that (A) each path from the root to a leaf holds exactly one pebble of each color, and (B) each pebbled vertex $v$ holds $p_v$ pebbles, at least as many as all its proper ancestors together, and exactly as many if any ancestor holds a pebble (the paper calls this *tight*). For a color $c$, let $V_c$ be the set of vertices with a pebble of color $c$. By (A), the vertices of $V_c$ cut the leaves into consecutive intervals, so finding the vertex of $V_c$ above $f(x)$ is an ordered search on $|V_c|$ items, with the bits $y_v = x_{r(v)}$, where $r(v)$ is the rightmost leaf below $v$.

**The unitaries.** $U_1$ colors a vertex: $|v\rangle|0\rangle \mapsto |v\rangle\, p_v^{-1/2} \sum_{c} |c\rangle$, the sum over the colors on $v$. $O'_x$ makes one query: if the parent of $v$ holds no pebble, $|v\rangle|0\rangle \mapsto |v\rangle|x_{i(v)}\rangle$; otherwise $|v\rangle \mapsto (-1)^{x_{i(v)}}|v\rangle$. $U_2$ maps $|v, 0\rangle \mapsto \Phi_{\mathrm{right}(v)}$ and $|v, 1\rangle \mapsto \Phi_{\mathrm{left}(v)}$ for the first case, and $|v\rangle \mapsto (\Phi_{\mathrm{right}(v)} - \Phi_{\mathrm{left}(v)})/\sqrt{2}$ for the second.

```pseudo id=main
HNS-SEARCH(O_x, N)                   ▷ x monotone, x_{N-1} = 1; the leaf register ends in |f(x)⟩
L1  if N = 1 then the leaf register holds |0⟩; return
L2  choose s and a tight pebbling of a tree T with N leaves by 2^s colors
L3  prepare 2^(-s/2) Σ_c |c⟩ in the color register
L4  for all colors c in parallel:
L5      HNS-SEARCH on V_c with the bits y_v = x_{r(v)}   ▷ all branches share each query
L6  ▷ now the state is 2^(-s/2) Σ_c |v_c⟩|c⟩, v_c the vertex of V_c above f(x)
L7  apply U_1^† to remove the colors      ▷ 2^(-s/2) Σ_v sqrt(p_v) |v⟩ over the pebbled ancestors of f(x)
L8  apply O'_x                            ▷ one query
L9  apply U_2                             ▷ the state is |f(x)⟩
L10 measure the leaf register and return the result
```

The query count obeys $F(1) = 0$ and $F(N) = 1 + \max_c F(|V_c|)$. A branch that finishes early waits: its query target is put in the state $(|0\rangle + |1\rangle)/\sqrt{2}$, which a bit flip does not change. Høyer, Neerbek and Shi give a tree with a fair and tight covering, where every color has $\lfloor N/3 + \lg N \rfloor$ pebbles and $s = \lfloor \log_4(N/2) \rfloor$ (Lemma 11). This gives $F(N) \le F(\lfloor N/3 + \lg N \rfloor + 1) + 1$ and so $F(N) = \log_3 N + O(1)$ (Lemma 12, Theorem 13).

**The pebbling of the implementation.** The Python file uses a simple tight pebbling of its own. It pads $N$ to an even number with $x_i = 1$. It cuts the leaves into *blocks*: complete binary trees of height $h \le s + 1$, most of them of height $s + 1$. In a block of height $h$, let $p = 2^{s+1-h}$. The root and the vertices at depth 1 hold $p$ pebbles each, and a vertex at depth $j \ge 2$ holds $2^{j-1} p$; all vertices at one depth hold the same colors. A path in a block then holds $p + p + 2p + \cdots + 2^{h-2}p = 2^s$ pebbles, one of each color, and each vertex below the root holds exactly as many pebbles as its ancestors. The colors go to the depths greedily: the least loaded colors go to the deepest level. Above the blocks the tree holds no pebbles. The program picks $s \le 4$ to make $F$ smallest. For blocks of height $s+1$, the average $|V_c|$ is $N (1/3 + 1/(6 \cdot 4^s))$, close to the paper's $N/3$.

## Example

Take $N = 10$ and $x = 0000001111$, so $f(x) = 6$. The program picks $s = 1$, two colors $\{0, 1\}$, and three blocks: leaves 0 to 3 (height 2), leaves 4 to 7 (height 2) and leaves 8 to 9 (height 1).

| block | root colors | depth 1 colors |
|---|---|---|
| leaves 0-3 | 1 | 0 (on both vertices) |
| leaves 4-7 | 0 | 1 (on both vertices) |
| leaves 8-9 | 0 and 1 | none |

So $V_0 = \{[0,1], [2,3], [4,7], [8,9]\}$ and $V_1 = \{[0,3], [4,5], [6,7], [8,9]\}$, written as leaf intervals. Each is an ordered search on 4 items.

1. For color 0 the bits are $y = (x_1, x_3, x_7, x_9) = (0, 0, 1, 1)$, with answer $[4,7]$. For color 1 they are $(x_3, x_5, x_7, x_9) = (0, 0, 1, 1)$, with answer $[6,7]$. Both searches run in parallel. A search on 4 items takes 2 queries (it is the $s = 0$ case, a quantum form of binary search). The state is $(|[4,7]\rangle|0\rangle + |[6,7]\rangle|1\rangle)/\sqrt{2}$.
2. Each of the two vertices holds one pebble, so $U_1^\dagger$ gives $(|[4,7]\rangle + |[6,7]\rangle)/\sqrt{2}$.
3. The query: $[4,7]$ is a block root, so it reads $x_5 = 0$ into the ancilla; $[6,7]$ has a pebbled parent, so it gets the phase $(-1)^{x_6} = -1$.
4. $U_2$ maps $|[4,7], 0\rangle$ to $\Phi_{[6,7]} = (|6\rangle + |7\rangle)/\sqrt{2}$, and $-|[6,7]\rangle$ to $-(|7\rangle - |6\rangle)/\sqrt{2}$. The sum is $\frac{1}{\sqrt{2}}\big(\frac{|6\rangle + |7\rangle}{\sqrt{2}} + \frac{|6\rangle - |7\rangle}{\sqrt{2}}\big) = |6\rangle$.

The answer comes with probability 1 after 3 queries. Binary search needs $\lceil \lg 10 \rceil = 4$.

Query counts of the implementation, from its exact recursion for $F$ (no randomness):

| $N$ | $2^6$ | $2^9$ | $2^{12}$ | $2^{16}$ |
|---|---|---|---|---|
| this implementation | 5 | 7 | 9 | 12 |
| binary search, $\lceil \lg N \rceil$ | 6 | 9 | 12 | 16 |
| $\log_3 N$ | 3.79 | 5.68 | 7.57 | 10.09 |
| lower bound $\frac{1}{\pi}(\ln N - 1)$ | 1.01 | 1.67 | 2.33 | 3.21 |

The smallest $N$ where it beats binary search is $N = 9$, with 3 queries. It searches up to 10 items with 3 queries and up to 28 with 4.

The Python file runs the algorithm on the exact amplitudes of the vertex and color registers. It builds the pebbling, runs the parallel subproblems recursively, applies $U_1^\dagger$, $O'_x$ and $U_2$, and returns the amplitudes of the leaf register. Its tests check that the final state is $|f(x)\rangle$ to within $10^{-9}$ for every monotone string of length $N \le 64$. They also check that the pebbling meets (A) and the tight form of (B) for $N < 200$, that $U_2$ on blocks of height 1 to 4 is unitary, and that the query count never exceeds $\lceil \lg N \rceil$ and stays above the lower bound for $N < 600$.

## Correctness

The proof is by induction on $N$. By (A), the leaf $f(x)$ has exactly one ancestor $v_c$ in each $V_c$, and the bits $y_v = x_{r(v)}$ are monotone with first 1 at $v_c$. So by induction line L5 leaves $|v_c\rangle|c\rangle$ in branch $c$, with no garbage. The state $2^{-s/2}\sum_c |v_c\rangle|c\rangle$ regroups as $2^{-s/2}\sum_v \sqrt{p_v}\, U_1|v\rangle|0\rangle$ over the pebbled ancestors $v$ of $f(x)$, so $U_1^\dagger$ gives line L7. Tightness fixes the amplitudes: in a block of height $h$, they are $2^{(1-h)/2}$ at the root and $2^{(j-h)/2}$ at depth $j \ge 1$. After $O'_x$ and $U_2$, the amplitude of a leaf $\ell \ne f(x)$ is a sum that telescopes to $0$, and the amplitude of $f(x)$ is $2^{1-h} + \sum_{j=1}^{h-1} 2^{j-h} = 1$. The full proof, with the check that $U_2$ is unitary, is in [the correctness proof](proofs/correctness.md).

## Complexity

- **Queries.** $F(N) = 1 + \max_c F(|V_c|)$ with $F(1) = 0$, exact, in the quantum query model with the bit oracle. With the covering of Lemma 11, $F(N) = \log_3 N + O(1)$ (Theorem 13). With $s = 0$ the recursion is $F(N) = 1 + F(\lceil N/2 \rceil)$, which is binary search, so the algorithm never needs more than $\lceil \lg N \rceil$ queries.
- **Qubits.** Each level of the recursion holds a vertex register of $O(\log N)$ qubits, a color register of $s = O(\log N)$ qubits and one ancilla. With $O(\log N)$ levels this is $O((\log N)^2)$ qubits for the construction as written. All ancillas and color registers return to $|0\rangle$.
- **Gates.** The paper counts only queries. $U_1$ and $U_2$ depend only on the tree, not on $x$. On a block, $U_2$ is a Haar wavelet transform, which has efficient circuits, but this page does not give a gate count.
- **Lower bound.** Every exact algorithm needs more than $\frac{1}{\pi}(\ln N - 1)$ queries (Theorem 1 of the same paper). So the gap between this algorithm and the lower bound is a factor of about $2.86$.

## Properties

- Exact: the final state is a basis state, so there is no error to amplify.
- The queries of all colors in one round are made by a single oracle call, on a superposition over the colors. The parallel searches are not independent classical runs.
- Recursive and non-adaptive in structure: the tree, the pebbling and the unitaries are fixed before any query.
- It uses the bit oracle in the last step for block roots and the phase form for other vertices; one ancilla controls which form a branch sees.
- It is not translation invariant, unlike the algorithms of Farhi, Goldstone, Gutmann and Sipser.

## Variants and improvements

- **Farhi, Goldstone, Gutmann and Sipser (1999).** Exact, translation-invariant algorithms, with $3 \log_{52} N \approx 0.526 \lg N$ queries. Høyer, Neerbek and Shi call their own construction "radically different" from this one.
- **Childs, Landahl and Parrilo (2007).** A semidefinite program finds translation-invariant algorithms; the result is exact with about $0.433 \lg N$ queries.
- **Ben-Or and Hassidim (2008).** A zero-error algorithm with about $0.32 \lg N$ expected queries.
- **Lower bound side.** Childs and Lee (ICALP 2008) show that the adversary method cannot prove more than $\frac{1}{\pi}\ln N + O(1)$. A 2026 preprint of Carolan and Childs claims algorithms that meet $\frac{1}{\pi}\ln N + o(\log N)$; see the problem page.

## When to use it

- To teach how parallel subproblems and interference beat the halving of binary search. The construction is explicit, and each step can be checked by hand on small $N$.
- Not as a practical search method. The saving is a constant factor in queries, and each quantum query of a stored list needs a [quantum random access memory](/quantum-random-access-memory/). A classical binary search on a stored array costs $\lceil \lg N \rceil$ cheap comparisons.
- If the goal is the fewest queries, the algorithms of Childs, Landahl and Parrilo, or of Ben-Or and Hassidim, use fewer.

## Pitfalls

- **$\frac{1}{\pi}\ln N$ is the lower bound, not this algorithm's count.** The same paper proves both. The algorithm uses about $0.631 \lg N$ queries, while $\frac{1}{\pi}\ln N \approx 0.221 \lg N$.
- **Grover search does not help.** [Grover search](/grover-search/) needs about $\sqrt{N}$ queries, much more than $\lg N$, because it ignores the order.
- **Ancestors without pebbles.** The tightness rule (B) is what makes the amplitudes telescope. A pebbling that satisfies (A) only gives a state with the right support but the wrong amplitudes, and the final measurement then fails with positive probability.
- **Padding.** For odd $N$ the tree needs a dummy leaf. It must hold $x_i = 1$, so the answer does not change, and its bit is known without a query.
- **Waiting branches.** A branch whose subproblem is smaller must not disturb the shared query. Its target must be in the state $(|0\rangle + |1\rangle)/\sqrt{2}$, or controlled off.

## Implementations

## History

Buhrman and de Wolf (Information Processing Letters, 1999) proved the first lower bound that grows with $N$, and Farhi, Goldstone, Gutmann and Sipser improved it and gave the first exact algorithm with $c \lg N$ queries for some $c < 1$ (1998 and 1999). Ambainis proved $\frac{1}{12}\lg N - O(1)$ at FOCS 1999. Høyer, Neerbek and Shi presented both the lower bound $\frac{1}{\pi}(\ln N - 1)$ and this algorithm at ICALP 2001, with the journal version in Algorithmica in 2002. Later work improved the constant of the algorithms but not of the lower bound.

## References
