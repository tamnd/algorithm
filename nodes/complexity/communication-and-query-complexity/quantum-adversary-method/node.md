---
tag: 88EHPQ
kind: technique
slug: quantum-adversary-method
name: Quantum adversary method
aliases:
- Ambainis adversary method
- adversary bound
- positive-weight adversary
- quantum adversary bound
area: complexity/communication-and-query-complexity
level: research
summary: "A lower bound on quantum query complexity: put weights on pairs of inputs with different values, and compare the spectral norm of the weight matrix with what one query can change."
prereqs: [quantum-query-model, adversary-argument, eigenvalue]
see_also: [quantum-query-complexity, polynomial-method, grover-optimality, hybrid-argument, element-distinctness-lower-bound, ambainis-element-distinctness, certificate-complexity, perron-frobenius-theorem]
sources:
  - paper: doi:10.1006/jcss.2002.1826
    title: "Andris Ambainis, Quantum lower bounds by quantum arguments, Journal of Computer and System Sciences 64(4), 2002, pages 750-767"
    locator: the main theorem (the unweighted bound Omega(sqrt(m m' / (l l')))) and its use for search, the AND of ORs and inverting a permutation
  - paper: doi:10.4086/toc.2006.v002a001
    title: "Robert Špalek and Mario Szegedy, All quantum adversary methods are equivalent, Theory of Computing 2(1), 2006, pages 1-18"
    locator: the equivalence of the spectral, weighted, Kolmogorov and other forms, and the limit sqrt(C_0 C_1) for total functions
  - paper: doi:10.1145/1250790.1250867
    title: "Peter Høyer, Troy Lee and Robert Špalek, Negative weights make adversaries stronger, 39th ACM Symposium on Theory of Computing (STOC 2007), pages 526-535"
    locator: the general adversary bound with negative weights, Q(f) = Omega(ADV±(f)), and examples where it beats the positive bound
  - paper: doi:10.1137/1.9781611973082.44
    title: Ben W. Reichardt, Reflections for quantum query algorithms, Proceedings of the 22nd ACM-SIAM Symposium on Discrete Algorithms (SODA 2011)
    locator: pp. 560 to 569 (the general adversary bound is tight up to a constant for every Boolean function)
  - paper: doi:10.1109/FOCS.2011.75
    title: "Troy Lee, Rajat Mittal, Ben W. Reichardt, Robert Špalek and Mario Szegedy, Quantum query complexity of state conversion, 52nd IEEE Symposium on Foundations of Computer Science (FOCS 2011), pages 344-353"
    locator: the tightness of the general adversary bound for functions with non-Boolean inputs and outputs
  - url: https://arxiv.org/abs/1907.09415
    title: Ronald de Wolf, Quantum Computing, Lecture Notes, arXiv:1907.09415
    locator: Chapter 11, Section 11.3 (the quantum adversary method, applied to search)
---

The quantum adversary method is a way to prove lower bounds on the number of queries of a quantum algorithm in the [quantum query model](/quantum-query-model/). It picks pairs of inputs $(x, y)$ with $f(x) \ne f(y)$ and gives each pair a weight. At the start, the algorithm is in the same state on $x$ and on $y$. At the end, the states must be almost orthogonal, so that a measurement can tell them apart. The method bounds how much one query can move the states apart, measured over all the weighted pairs at once. Ambainis introduced it in 2000; the general form with negative weights, due to Høyer, Lee and Špalek, is tight up to a constant factor for every Boolean function. Do not confuse it with the classical [adversary argument](/adversary-argument/), in which an adversary answers the queries of a deterministic algorithm.

## In plain words

Take two inputs that need different answers, but that differ in only a few places. Before any question, the quantum program is in the same state on both inputs. To give different answers at the end, the program must make the two states very different. A question to a position where the two inputs agree does not move the states apart at all. A question to a position where they differ moves them apart only a little, if the program spreads its attention over many positions. Now take a large set of such pairs, where each input has many partners and each position matters for only a few of them. Then each question makes only a small amount of progress on the whole set, and many questions are necessary. The method turns this count into a number with a matrix.

## When it applies

Use the method to find a lower bound on $Q(f)$, the bounded-error [quantum query complexity](/quantum-query-complexity/). It applies to total and partial functions, with inputs over any finite alphabet and with any output set. It works best when there are many pairs of inputs with different values that differ in few positions, and each position separates only a few of these pairs. This is the case for search, for compositions of AND and OR, and for problems on graphs given by adjacency queries.

It does not apply to classical algorithms directly. For a bound on $R(f)$, use the classical [adversary argument](/adversary-argument/) or [Yao's minimax principle](/yao-minimax-principle/). The positive-weight form also has a hard limit that is set by the certificates of $f$ (see Pitfalls), so for some problems the [polynomial method](/polynomial-method/) or the form with negative weights must be used.

## The template

Let $f$ be a function on a domain $S \subseteq \Sigma^n$. An **adversary matrix** is a real symmetric matrix $\Gamma$, with rows and columns indexed by $S$, such that $\Gamma[x, y] = 0$ when $f(x) = f(y)$. For each position $i$, let $D_i$ be the 0-1 matrix with $D_i[x, y] = 1$ exactly when $x_i \ne y_i$, and let $\Gamma_i = \Gamma \circ D_i$ be the entrywise product. Write $\|\cdot\|$ for the spectral norm, the largest absolute [eigenvalue](/eigenvalue/) of a symmetric matrix. The positive-weight bound is

$$\mathrm{ADV}(f) = \max_{\Gamma \ge 0} \frac{\|\Gamma\|}{\max_i \|\Gamma_i\|} ,$$

where the maximum is over adversary matrices with nonnegative entries.

```pseudo id=template
ADVERSARY-BOUND(f)             ▷ f on a domain S, n positions
L1  X ← HARD-INPUTS-0(f)          ▷ hole: inputs with value 0
L2  Y ← HARD-INPUTS-1(f)          ▷ hole: inputs with value 1
L3  Γ ← WEIGHTS(X, Y)             ▷ hole: Γ[x,y] ≥ 0, nonzero only on pairs in X × Y and Y × X
L4  A ← ‖Γ‖                       ▷ spectral norm
L5  B ← max over i of ‖Γ ∘ D_i‖   ▷ D_i[x,y] = 1 exactly when x_i ≠ y_i
L6  return Q_ε(f) ≥ c(ε) · A / B   ▷ c(ε) = (1 - 2·sqrt(ε(1 - ε)))/2
```

The holes are the two sets of hard inputs and the weights. A good choice puts weight on pairs that differ in few positions. With all weights equal to $1$ on a relation $R \subseteq X \times Y$, the bound takes the form of Ambainis' first theorem. Suppose each $x \in X$ has at least $m$ partners in $Y$, each $y \in Y$ has at least $m'$ partners in $X$, and for each $x$ and each position $i$ at most $\ell$ partners $y$ of $x$ have $y_i \ne x_i$, and for each $y$ and $i$ at most $\ell'$ partners $x$ of $y$ have $x_i \ne y_i$. Then $Q(f) = \Omega(\sqrt{m m' / (\ell \ell')})$.

**Why the bound holds.** Let $\delta$ be a unit eigenvector of $\Gamma$ for the eigenvalue $\|\Gamma\|$. Since $\Gamma \ge 0$, the [Perron-Frobenius theorem](/perron-frobenius-theorem/) lets us take $\delta \ge 0$. For an algorithm with states $|\psi_x^t\rangle$ after $t$ queries, define the progress measure

$$W_t = \sum_{x, y} \Gamma[x, y] \, \delta_x \delta_y \, \langle \psi_x^t | \psi_y^t \rangle .$$

1. **Start.** All states are equal at $t = 0$, so $W_0 = \delta^{T} \Gamma \delta = \|\Gamma\|$.
2. **End.** If the algorithm outputs $f(x)$ with probability at least $1 - \varepsilon$, then for each pair with $f(x) \ne f(y)$ the final states satisfy $|\langle \psi_x^T | \psi_y^T \rangle| \le 2\sqrt{\varepsilon(1 - \varepsilon)}$. Only such pairs have weight, so $|W_T| \le 2\sqrt{\varepsilon(1-\varepsilon)} \, \|\Gamma\|$.
3. **One step.** The maps $U_t$ do not depend on the input, so they do not change any inner product. Use the phase oracle with a control qubit, and write the part of $|\psi_x^t\rangle$ with control $1$ and index $i$ as $|i\rangle|\phi_{x,i}\rangle$. One query multiplies this part by $(-1)^{x_i}$, so the inner product of the states for $x$ and $y$ changes by $-2 \sum_{i : x_i \ne y_i} \langle \phi_{x,i} | \phi_{y,i} \rangle$. With $u_x = \delta_x \|\phi_{x,i}\|$ and $\Gamma_i \ge 0$,

$$\Big| \sum_{x,y} \Gamma_i[x,y] \, \delta_x \delta_y \langle \phi_{x,i} | \phi_{y,i} \rangle \Big| \le u^{T} \Gamma_i u \le \|\Gamma_i\| \sum_x \delta_x^2 \|\phi_{x,i}\|^2 .$$

Add over $i$. Since $\sum_i \|\phi_{x,i}\|^2 \le 1$ and $\sum_x \delta_x^2 = 1$, one query changes $W$ by at most $2 \max_i \|\Gamma_i\|$.

So $T \cdot 2 \max_i \|\Gamma_i\| \ge (1 - 2\sqrt{\varepsilon(1-\varepsilon)}) \|\Gamma\|$, which is line L6. At $\varepsilon = 1/3$ the constant $c(1/3)$ is about $0.0286$; at $\varepsilon = 0$ it is $1/2$.

## Classic examples

**Search (OR of $n$ bits).** Let $X = \{0^n\}$ and $Y = \{e_1, \ldots, e_n\}$, where $e_j$ has a single 1 at position $j$. Put weight 1 on each pair $(0^n, e_j)$. Then $\Gamma$ is the adjacency matrix of a star with $n$ leaves, so $\|\Gamma\| = \sqrt n$. The matrix $\Gamma_i$ keeps only the edge to $e_i$, so $\|\Gamma_i\| = 1$. For $n = 4, 9, 16$ the norms are $2, 3, 4$ and each $\|\Gamma_i\|$ is $1$. The bound is $Q(\mathrm{OR}_n) = \Omega(\sqrt n)$, so [Grover search](/grover-search/) is optimal up to a constant factor. In the unweighted form, $m = n$, $m' = 1$ and $\ell = \ell' = 1$.

**PARITY of $n$ bits.** Let $X$ be the strings of even weight and $Y$ the strings of odd weight, and put weight 1 on each pair at Hamming distance 1. Then $\Gamma$ is the adjacency matrix of the $n$-dimensional hypercube, which is $n$-regular, so $\|\Gamma\| = n$. Each $\Gamma_i$ is a perfect matching along direction $i$, with norm 1. The bound is $\Omega(n)$. A run for $n = 3, 4, 5$ gives the ratios $3, 4, 5$. The exact answer is $\lceil n/2 \rceil$, so here the method gives the right order but a weak constant.

**AND of ORs.** Let $n = k^2$ and $f(x) = \bigwedge_{b=1}^{k} \bigvee_{j=1}^{k} x_{b,j}$. Let $Y$ be the inputs with exactly one 1 in each block, so $f = 1$. Let $X$ be the inputs with one block of zeros and exactly one 1 in each other block, so $f = 0$. Relate $x$ and $y$ when they differ in one bit. Each $x$ has $m = k$ partners (put a 1 anywhere in its zero block), each $y$ has $m' = k$ partners (clear the 1 of any block), and a position separates a given input from at most one partner, so $\ell = \ell' = 1$. The bound is $\Omega(\sqrt{k \cdot k}) = \Omega(\sqrt n)$. A run gives $|X| = |Y| = 4$ and ratio $2$ for $k = 2$, and $|X| = |Y| = 27$ and ratio $3$ for $k = 3$. This was the first $\Omega(\sqrt n)$ bound for this function.

**Inverting a permutation.** The input is a permutation $\pi$ of $\{1, \ldots, n\}$, given by queries $i \mapsto \pi(i)$, and the task is to find the $i$ with $\pi(i) = 1$ and output a bit of it. Ambainis related permutations that differ by a swap of two values and proved $\Omega(\sqrt n)$, which matches Grover search for the position of the value 1.

## Variations

- **Weighted forms.** Ambainis later allowed weights on pairs and on positions. Barnum, Saks and Szegedy gave the spectral form above, and Laplante and Magniez gave a form based on Kolmogorov complexity. Špalek and Szegedy proved that all these forms give the same number, $\mathrm{ADV}(f)$.
- **Negative weights.** Høyer, Lee and Špalek allowed $\Gamma$ to have negative entries. The step bound then uses $|\mathrm{tr}(\Gamma_i M)| \le \|\Gamma_i\| \, \|M\|_{tr}$ for a positive semidefinite matrix $M$ in place of the argument with $u^T \Gamma_i u$. The result is the general adversary bound $\mathrm{ADV}^{\pm}(f) \ge \mathrm{ADV}(f)$, with $Q(f) = \Omega(\mathrm{ADV}^{\pm}(f))$. They gave a function where $\mathrm{ADV}^{\pm}$ is larger than $\mathrm{ADV}$ by a power.
- **Tightness.** Reichardt showed $Q(f) = \Theta(\mathrm{ADV}^{\pm}(f))$ for every Boolean $f$, by an algorithm built from the dual of the adversary program. Lee, Mittal, Reichardt, Špalek and Szegedy extended this to functions with non-Boolean inputs and outputs, and to the task of state conversion.
## Pitfalls

- **The certificate barrier.** For total Boolean $f$, $\mathrm{ADV}(f) \le \sqrt{C_0(f) \, C_1(f)}$, where $C_0$ and $C_1$ are the [certificate complexities](/certificate-complexity/) for value 0 and value 1. For partial functions a similar limit is $\min(\sqrt{C_0 n}, \sqrt{C_1 n})$. Element distinctness has 1-certificates of size 2, so the positive-weight bound is at most $O(\sqrt n)$, while the true value is $\Theta(n^{2/3})$. Use the polynomial method, as in the [element distinctness lower bound](/element-distinctness-lower-bound/), or negative weights.
- **Weights on equal values.** A pair with $f(x) = f(y)$ must have weight 0. Otherwise step 2 of the proof fails, because such states need not be far apart at the end.
- **Wrong norm.** The bound uses the spectral norm of $\Gamma_i$, not its largest entry. For OR, let $X = \{0^n\}$ and let $Y$ be all $2^n - 1$ nonzero strings, with weight 1 on each pair. Then $\|\Gamma\| = \sqrt{2^n - 1}$, and $\Gamma_i$ is a star with $2^{n-1}$ leaves, so $\|\Gamma_i\| = 2^{(n-1)/2}$ and the true ratio is less than $\sqrt 2$. With the largest entry, 1, in place of $\|\Gamma_i\|$, the ratio would be $\sqrt{2^n - 1}$, which is more than $n$ for $n \ge 6$ and so cannot be a lower bound.
- **Constants.** The method gives the order of $Q(f)$, not exact counts. For PARITY it gives $\Omega(n)$, but the polynomial method gives the exact $\lceil n/2 \rceil$.
- **Classical and quantum.** A bound found with the classical adversary argument is a bound on $D^{dt}(f)$, and it says nothing about $Q(f)$. OR has $D^{dt} = n$ but $Q = \Theta(\sqrt n)$.

## Exercises

1. Compute $\|\Gamma\|$ and $\|\Gamma_i\|$ for the star matrix of search with $n = 25$, and give the bound for $\varepsilon = 1/3$ with the constant $c(1/3)$.
2. Use the unweighted form to prove $Q(\mathrm{AND}_n) = \Omega(\sqrt n)$.
3. For the majority of $n$ bits, with $n$ odd, relate inputs of weight $(n-1)/2$ and $(n+1)/2$ at Hamming distance 1. Find $m$, $m'$, $\ell$, $\ell'$ and show $Q(\mathrm{MAJ}_n) = \Omega(n)$.
4. Show that the threshold function "at least $k$ ones" has $Q = \Omega(\sqrt{k(n - k + 1)})$ with the unweighted form.
5. Prove that $\mathrm{ADV}(f) \le n$ for every $f$ on $n$ positions.
6. Explain with certificates why no positive-weight matrix proves $\Omega(n^{2/3})$ for element distinctness.

## References
