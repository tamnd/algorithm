---
tag: 1MB9PX
kind: algorithm
slug: alphatensor
name: AlphaTensor
aliases:
- AlphaTensor matrix multiplication search
- TensorGame
area: algebra/matrix-multiplication
level: research
summary: Reinforcement-learning search that plays a game of subtracting rank-one tensors; it found a 4×4 algorithm using 47 multiplications over GF(2) and a 4×5 by 5×5 one with 76.
model: word-ram
complexity:
  vars: {R: the move limit, d: the number of entries of the target tensor, s: the number of entries in one move}
  time: {worst: O(R d), average: O(R d), best: Θ(d)}
  space: {extra: O(d + R s)}
properties: {deterministic: false, recursive: false, in_place: false}
history:
  year: 2022
  people: [Alhussein Fawzi, Matej Balog, Aja Huang, Thomas Hubert, Bernardino Romera-Paredes, Pushmeet Kohli]
  note: Published in Nature by a DeepMind team of thirteen authors. The scheme of rank 47 for 4×4 matrices over GF(2) beat the 49 of Strassen applied twice.
prereqs: [tensor-rank, strassen-algorithm, monte-carlo-tree-search]
see_also: [matrix-multiplication-tensor, bilinear-complexity, laderman-algorithm, matrix-multiplication-exponent, coppersmith-winograd-algorithm, sat, reinforce]
sources:
  - paper: doi:10.1038/s41586-022-05172-4
    title: Alhussein Fawzi et al., Discovering faster matrix multiplication algorithms with reinforcement learning, Nature 610 (2022)
    locator: pp. 47 to 53 (TensorGame, the network and the search, the table of ranks for sizes up to 5 with 47 for 4×4 over GF(2) and 76 for 4×5 by 5×5, and the algorithms tuned for GPU and TPU)
  - paper: doi:10.1126/science.aar6404
    title: David Silver et al., A general reinforcement learning algorithm that masters chess, shogi, and Go through self-play, Science 362 (2018)
    locator: pp. 1140 to 1144 (AlphaZero, the self-play and tree search method that AlphaTensor adapts)
  - paper: "Manuel Kauers and Jakob Moosbauer, The FBHHRBNRSSSHK-algorithm for multiplication in Z2^(5×5) is still not optimal, ACM Communications in Computer Algebra 56(3) (2022), arXiv:2210.04045"
    locator: the scheme of rank 95 for 5×5 over GF(2), one below AlphaTensor's 96
  - paper: "Manuel Kauers and Jakob Moosbauer, Flip graphs for matrix multiplication, ISSAC 2023, arXiv:2212.01175"
    locator: the flip graph, flips and reductions, and the random walks that find small schemes
  - paper: "Marijn J. H. Heule, Manuel Kauers and Martina Seidl, New ways to multiply 3×3-matrices, Journal of Symbolic Computation 104 (2021)"
    locator: SAT search over GF(2) and lifting of the schemes to the integers
  - paper: doi:10.1007/BF02165411
    title: Volker Strassen, Gaussian elimination is not optimal, Numerische Mathematik 13 (1969)
    locator: pp. 354 to 356 (the rank 7 scheme for 2×2, which TensorGame recovers)
---

AlphaTensor is a reinforcement learning system from DeepMind (Fawzi and others, 2022) that searches for small fast matrix multiplication algorithms. It treats the search as a single-player game, TensorGame. The board is a [matrix multiplication tensor](/matrix-multiplication-tensor/) $\langle n, m, p \rangle$, and each move subtracts a rank-one tensor $u \otimes v \otimes w$ whose entries come from a small set such as $\{-2, -1, 0, 1, 2\}$. Reaching the zero tensor in $t$ moves gives a bilinear algorithm with $t$ multiplications, that is a proof that the [tensor rank](/tensor-rank/) is at most $t$. The moves are chosen by Monte Carlo tree search guided by a neural network, as in AlphaZero. Its best known results are a scheme for $4 \times 4$ matrices with $47$ multiplications over $\mathbb{F}_2$, against $49$ from [Strassen's algorithm](/strassen-algorithm/) used twice, and a scheme for $4 \times 5$ by $5 \times 5$ with $76$ multiplications over any ring, against $80$.

## In plain words

A fast way to multiply small matrices is a list of products, each of a sum of entries of $A$ with a sum of entries of $B$. Adding the products in the right way gives every entry of $C$. Finding such a list with few products is a hard puzzle.

AlphaTensor turns the puzzle into a game. The position is a three-dimensional array of numbers. Each move removes one simple pattern from the array, and each move costs a point. The game is won when the array is all zeros, and the moves made are then exactly the products of a correct algorithm. A neural network learns, from many games, which moves look promising, and a tree search uses it to plan ahead. The output is checked exactly, so a found algorithm is certainly correct, whatever the network did.

## The problem

The target is the tensor $T = \langle n, m, p \rangle$ of the product of an $n \times m$ matrix $A$ and an $m \times p$ matrix $B$. It has $d = nm \cdot mp \cdot np$ entries, indexed by $((i, j), (j', k), (i', k'))$, with a $1$ when $j = j'$, $k = k'$ and $i = i'$, and $0$ otherwise. A decomposition of rank $t$ is a list of $t$ triples with
$$T = \sum_{r=1}^{t} u^{(r)} \otimes v^{(r)} \otimes w^{(r)},$$
where $u^{(r)}$ is an $n \times m$ array of coefficients of $A$, $v^{(r)}$ an $m \times p$ array of coefficients of $B$, and $w^{(r)}$ says how much of the $r$-th product goes into each entry of $C$. Such a list is a bilinear algorithm with $t$ multiplications:
$$M_r = \Big(\sum_{i,j} u^{(r)}_{ij} a_{ij}\Big)\Big(\sum_{j,k} v^{(r)}_{jk} b_{jk}\Big), \qquad c_{ik} = \sum_{r} w^{(r)}_{ik} M_r.$$
It uses no commutativity, so it applies to blocks and can recurse.

The arithmetic matters. A decomposition with integer coefficients that holds over $\mathbb{Z}$ works over every ring. A decomposition that holds only modulo $2$ gives an algorithm only over rings of characteristic $2$, such as $\mathbb{F}_2$ and its extensions. AlphaTensor searched in both settings. The goal is the smallest $t$ for each small shape; for $n, m, p \le 5$ the exact ranks are mostly unknown.

## The algorithm

One game of TensorGame, with a policy that proposes moves:

```pseudo id=main
ALPHATENSOR(T, F, R_limit, policy)       ▷ T a tensor, F the allowed coefficients
L1  S ← T; t ← 0; factors ← empty list
L2  while S ≠ 0 and t < R_limit do
L3    (u, v, w) ← policy(S, t)          ▷ in AlphaTensor: tree search guided by the network, entries in F
L4    S ← S − u ⊗ v ⊗ w; append (u, v, w) to factors; t ← t + 1
L5  if S = 0 then return factors with reward −t
L6  return failure with reward −t − γ(S)  ▷ γ(S) is an upper bound on the rank of S
```

Line L3 is the only place where learning enters. In AlphaTensor the policy runs a sampled Monte Carlo tree search from the position $S$: the network gives a value estimate of $S$ and a distribution over moves, the search samples candidate moves from that distribution, since the set of all moves is far too large to list, and it picks the most visited one. Line L4 is exact integer or modular arithmetic. Line L6 punishes games that run out of moves; the paper uses an upper bound on the rank of what is left. The implementation on this page uses the sum of the ranks of the slices of $S$, which is such a bound.

Around the game is the training loop, which is not implemented here:

1. **Self-play.** Play many games on the target tensors with the current network and search. Store each position with the search's move counts and the final reward.
2. **Synthetic demonstrations.** Sample random lists of rank-one tensors with entries in F, add them up, and train the network to play these lists back. This is cheap supervised data, since the answer is known by construction.
3. **Change of basis.** Present each target in a random basis, $T' = (P \otimes Q \otimes R) T$ for invertible $P$, $Q$, $R$. A decomposition of $T'$ maps back to one of $T$ with the same rank, so this gives many different starting positions for one problem.
4. **Train.** Fit the network to predict the search's moves and the final reward, and repeat.

A single agent was trained on all target sizes with $n, m, p \le 5$, once in standard arithmetic and once modulo $2$.

## Example

Play TensorGame on $\langle 2, 2, 2 \rangle$, a $4 \times 4 \times 4$ array with $8$ ones, using Strassen's seven products as the moves. The table gives, after each move, the number of nonzero entries of $S$ and the bound $\gamma(S)$ from the sum of slice ranks. All entries of $S$ stay in $\{-1, 0, 1\}$.

| moves played | 0 | 1 | 2 | 3 | 4 | 5 | 6 | 7 |
|---|---|---|---|---|---|---|---|---|
| nonzero entries of $S$ | 8 | 12 | 12 | 12 | 10 | 8 | 4 | 0 |
| $\gamma(S)$ | 8 | 10 | 8 | 7 | 6 | 4 | 2 | 0 |

The first move is $M_1 = (a_{11} + a_{22})(b_{11} + b_{22})$ into $c_{11}$ and $c_{22}$, which is $8$ entries of $u \otimes v \otimes w$. Two of them cancel ones of $T$, and the other six are new, so $S$ goes from $8$ to $12$ nonzero entries. After all seven moves $S = 0$, and the reward is $-7$. Playing the eight products of the triple loop instead gives $-8$. With the move limit set to $5$, the triple loop's game ends with $3$ ones left and $\gamma = 3$, so the reward is $-5 - 3 = -8$. A script reproduces the table.

Over $\mathbb{F}_2$, a random walk on the flip graph (Kauers and Moosbauer), started from the triple loop, reaches a scheme of rank $7$ after a few dozen to a few thousand flips; ten seeds took between $54$ and $3757$. The run with seed $1$ found, writing each array row by row,

| $r$ | $u$ | $v$ | $w$ |
|---|---|---|---|
| 1 | $a_{21}$ | $b_{11}$ | $c_{21}, c_{22}$ |
| 2 | $a_{12} + a_{22}$ | $b_{11} + b_{12} + b_{21} + b_{22}$ | $c_{11}$ |
| 3 | $a_{11} + a_{12}$ | $b_{22}$ | $c_{12}, c_{22}$ |
| 4 | $a_{22}$ | $b_{21}$ | $c_{11}, c_{21}$ |
| 5 | $a_{11} + a_{12} + a_{22}$ | $b_{11} + b_{12} + b_{22}$ | $c_{11}, c_{22}$ |
| 6 | $a_{11} + a_{12} + a_{21} + a_{22}$ | $b_{11} + b_{12}$ | $c_{22}$ |
| 7 | $a_{11}$ | $b_{12} + b_{22}$ | $c_{11}, c_{12}$ |

It is correct modulo $2$ and wrong over $\mathbb{Z}$; the script checks both. Replaying it as moves wins TensorGame over $\mathbb{F}_2$ in $7$ moves.

## Correctness

A won game is a proof by construction. Line L4 keeps the invariant
$$T = S + \sum_{r=1}^{t} u^{(r)} \otimes v^{(r)} \otimes w^{(r)},$$
which holds at L1 with $t = 0$ and is preserved by each move. When the loop stops with $S = 0$, the factors are a decomposition of $T$ of rank $t$. Since the arithmetic is exact, over $\mathbb{Z}$ or modulo a prime, no error can enter, and the decomposition is correct whatever policy chose the moves. A decomposition of $\langle n, m, p \rangle$ is a correct bilinear algorithm by the identity in the problem section, and block multiplication makes its recursive use correct. If the game is lost, nothing is claimed, and $\gamma(S)$ only affects the reward.

The game terminates because $t$ grows by one on each move and the loop stops at $R_{\text{limit}}$. The proofs section writes out the invariant and the reward bound. The search itself has no guarantee: the network and the tree search are heuristics, and failing to find a rank $t$ scheme says nothing about whether one exists.

## Complexity

- **One game.** At most $R_{\text{limit}}$ moves. Each subtracts a rank-one tensor and tests $S$ for zero in $O(d)$ time, with $d = n^2 m^2 p^2$ for $\langle n, m, p \rangle$. So $O(R_{\text{limit}}\, d)$ time without the calls to the policy, and $O(d + R_{\text{limit}}\, s)$ space with $s = nm + mp + np$. These counts are proved but small. The real cost is the policy.
- **The search.** The number of possible moves is $|F|^{s}$, about $5^{48} \approx 3.6 \cdot 10^{33}$ for $\langle 4, 4, 4 \rangle$ with five coefficients. That is why the tree search samples moves instead of listing them. Training used large amounts of accelerator time; the cost is reported, not bounded, and no guarantee on finding a scheme exists.
- **The algorithms found.** A rank $t$ scheme for $\langle n, n, n \rangle$, used recursively, multiplies $N \times N$ matrices in $O(N^{\log_n t})$ operations. For the rank $47$ scheme over $\mathbb{F}_2$ this is $\log_4 47 \approx 2.7773$, below $\log_2 7 \approx 2.8074$, but valid only in characteristic $2$. For a scheme for $\langle n, m, p \rangle$ the exponent is $3 \log t / \log(nmp)$, which is $3 \log 76 / \log 100 \approx 2.8212$ for the $76$ scheme, worse than Strassen asymptotically but better than the earlier $80$ (about $2.8546$). None of these improves the bounds on the [exponent ω](/matrix-multiplication-exponent/), which are far lower.
- **Speed in practice.** AlphaTensor was also run with a reward that included the measured running time of the algorithm on a given GPU or TPU, for matrices of size $8192$. The paper reports speedups of roughly $10$ to $20$ percent over the standard algorithm on that hardware. These are observed timings on specific machines, not proved bounds, and were not checked here.

## Properties

- **Exact output.** Every scheme it reports is checked exactly. The learning only affects which schemes are found.
- **Randomized and incomplete.** The search is random, and it can neither prove a lower bound nor show that its best rank is optimal.
- **Arithmetic-dependent.** A scheme found modulo $2$ may fail over $\mathbb{Z}$, as in the example. Schemes over $\mathbb{Z}$ with coefficients in F work over every ring.
- **Many schemes.** For a fixed size it found many inequivalent schemes of the same rank, for example for $\langle 4, 4, 4 \rangle$ in standard arithmetic at rank $49$. These differ in the number of additions and in numerical stability.
- **Bounded coefficients.** All entries lie in $\{-2, -1, 0, 1, 2\}$, which keeps the additions cheap and the schemes small.

## Variants and improvements

- **Flip graphs.** Kauers and Moosbauer (2022) started from AlphaTensor's rank $96$ scheme for $5 \times 5$ over $\mathbb{F}_2$ and reached $95$ by a random walk on the flip graph. A flip rewrites two terms that share a factor, $a \otimes b \otimes c + a \otimes b' \otimes c'$, as $a \otimes (b + b') \otimes c + a \otimes b' \otimes (c' - c)$, which has the same sum. A reduction merges two terms that share two factors and lowers the rank. No learning is involved, and the method has since matched or improved many of AlphaTensor's ranks.
- **SAT solving.** Heule, Kauers and Seidl (2021) encoded schemes over $\mathbb{F}_2$ as [SAT](/sat/) instances and found thousands of rank $23$ schemes for $3 \times 3$, then lifted them to $\mathbb{Z}$, as for [Laderman's scheme](/laderman-algorithm/).
- **Numerical optimization.** Alternating least squares over the reals finds approximate decompositions that are then rounded to exact ones; Smirnov used it in 2013 for many small formats.
- **Later systems.** DeepMind's AlphaEvolve (2025) is reported to have found a rank $48$ scheme for $4 \times 4$ with complex coefficients, the first below $49$ in characteristic $0$. This is taken from the announcement and not checked here.
- **Hardware rewards.** Replacing the reward $-1$ per move by a measured running time finds schemes tuned to one machine instead of the fewest multiplications.

## When to use it

TensorGame is a good framing for any search for small tensor decompositions: the state, the moves and the exact check are simple, and the policy can be anything from random choice to a large network. Use the schemes AlphaTensor published, which are public and checkable, rather than retraining the system; retraining needs large compute. For a new small shape, try cheaper methods first: flip graph walks and SAT solvers have matched or beaten it on many sizes. For multiplying matrices in practice, a new scheme helps only if its saving in multiplications survives the extra additions, which usually means large blocks or expensive entries.

## Pitfalls

- **Characteristic 2 only.** The $47$ for $4 \times 4$ is over $\mathbb{F}_2$. It does not give a $47$ product algorithm for real or integer matrices; in characteristic $0$ the best was still $49$ at the time.
- **Not a bound on ω.** Small schemes give exponents near $2.8$. The asymptotic records come from the [Coppersmith-Winograd line](/coppersmith-winograd-algorithm/) and are far lower.
- **Trusting without checking.** Always verify a published scheme against the tensor, or against the triple loop on random inputs, over the ring you will use. Typing errors in signs are common.
- **Counting only multiplications.** A rank $47$ or $76$ scheme has many more additions than the schoolbook loop for one level; the saving appears only when the entries are large blocks.
- **Floating point.** Schemes with coefficients $\pm 2$ and long chains of additions can have worse error constants than Strassen's.

## Implementations

## History

Strassen's 1969 scheme of rank $7$ for $2 \times 2$ matrices started the search for small schemes. Laderman found rank $23$ for $3 \times 3$ in 1976, and later work used hand analysis, numerical optimization and SAT solvers. In 2018 DeepMind's AlphaZero learned to play chess, shogi and Go by self-play and tree search. In October 2022 Fawzi and coworkers published AlphaTensor in Nature, which applied the same method to TensorGame and found the rank $47$ scheme for $4 \times 4$ over $\mathbb{F}_2$, improving on the $49$ that had stood since Strassen. Within weeks, Kauers and Moosbauer improved its $5 \times 5$ scheme over $\mathbb{F}_2$ from $96$ to $95$ with flip graphs, without learning.

## References
