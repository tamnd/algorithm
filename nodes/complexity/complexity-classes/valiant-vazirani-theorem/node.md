---
tag: YARBYX
kind: theorem
slug: valiant-vazirani-theorem
name: Valiant-Vazirani theorem
aliases:
- unique SAT randomized reduction
area: complexity/complexity-classes
level: research
summary: A randomized polynomial-time map sends a satisfiable formula to one with exactly one solution with probability at least 1/(8n) and keeps unsatisfiable formulas unsatisfiable.
prereqs: [sat, rp, pairwise-independence, universal-hash-family]
see_also: [unambiguous-polynomial-time, toda-theorem, rp, parsimonious-reduction, xor-sat, pairwise-independence, universal-hash-family, jerrum-valiant-vazirani-theorem]
sources:
  - paper: doi:10.1016/0304-3975(86)90135-0
    title: Leslie G. Valiant and Vijay V. Vazirani, NP is as easy as detecting unique solutions, Theoretical Computer Science 47(1), 85 to 93 (1986)
    locator: the main theorem (the randomized reduction from SAT to unique SAT) and the corollary for parity SAT
  - paper: doi:10.1007/s00037-013-0059-7
    title: Holger Dell, Valentine Kabanets, Dieter van Melkebeek and Osamu Watanabe, Is Valiant-Vazirani's isolation probability improvable?, Computational Complexity 22(2), 345 to 383 (2013)
    locator: the result that isolation with probability above 2/3 implies NP in P/poly
  - paper: doi:10.1137/0220053
    title: Seinosuke Toda, PP is as hard as the polynomial-time hierarchy, SIAM Journal on Computing 20(5), 865 to 877 (1991)
    locator: the use of the isolation step in the proof that PH is in BP.parity-P
  - paper: doi:10.1007/BF02579206
    title: Ketan Mulmuley, Umesh V. Vazirani and Vijay V. Vazirani, Matching is as easy as matrix inversion, Combinatorica 7(1), 105 to 113 (1987)
    locator: the isolating lemma
  - book: isbn:9780521424264
    title: Sanjeev Arora and Boaz Barak, Computational Complexity, A Modern Approach, Cambridge University Press (2009)
    locator: Chapter 17, Complexity of counting (the Valiant-Vazirani theorem and Toda's theorem)
  - book: isbn:9780521884730
    title: Oded Goldreich, Computational Complexity, A Conceptual Perspective, Cambridge University Press (2008)
    locator: Chapter 6, Randomness and counting (unique solutions and the reduction to them)
---

The Valiant-Vazirani theorem says that finding out whether a Boolean formula is satisfiable is no harder, under randomized reductions, than doing it for formulas that have at most one satisfying assignment. A randomized polynomial-time map adds random parity constraints to a formula $\varphi$ with $n$ variables. If $\varphi$ is unsatisfiable, the new formula is unsatisfiable. If $\varphi$ is satisfiable, the new formula has exactly one satisfying assignment with probability at least $1/(8n)$. So if the promise problem of unique satisfiability had a polynomial-time algorithm, then $\mathsf{NP} = \mathsf{RP}$. The isolation step is also the first step of [Toda's theorem](/toda-theorem/).

## Statement

**Theorem (Valiant and Vazirani 1986).** There is a randomized polynomial-time algorithm that maps a CNF formula $\varphi$ in $n$ variables to a CNF formula $\psi$ such that:

- if $\varphi$ is unsatisfiable, then $\psi$ is unsatisfiable (with probability $1$);
- if $\varphi$ is satisfiable, then $\Pr[\psi \text{ has exactly one satisfying assignment}] \ge 1/(8n)$.

The promise problem USAT has as yes-instances the formulas with exactly one satisfying assignment and as no-instances the unsatisfiable formulas; on other formulas any answer is allowed. The theorem is a randomized reduction from [SAT](/sat/) to USAT with one-sided error.

**Corollary.** If USAT is solved by a deterministic polynomial-time algorithm, or by a randomized one with one-sided error, then $\mathsf{NP} = \mathsf{RP}$. If it is solved with two-sided bounded error, then $\mathsf{NP} \subseteq \mathsf{BPP}$.

## In plain words

Suppose a formula has some solutions, but we do not know how many. Add a few random conditions, each of which keeps about half of the solutions and removes the others. If we add the right number of conditions for the size of the solution set, there is a fair chance that exactly one solution is left. We do not know the right number, so we guess it at random, and the guess is right often enough. A formula with no solutions keeps no solutions whatever we add. So a method that only works when there is at most one solution can still decide whether any solution exists, with some help from random choices.

## Proof

Let $S \subseteq \{0,1\}^n$ be the set of satisfying assignments of $\varphi$. If $S = \emptyset$, every formula of the form $\varphi \land (\ldots)$ is unsatisfiable, which gives the first part. Now let $S \ne \emptyset$.

*The hash family.* For $k \ge 1$, choose a uniform $k \times n$ matrix $A$ and a uniform vector $b \in \{0,1\}^k$ over $\mathrm{GF}(2)$, and let $h(x) = Ax + b$. For $x \ne y$, the pair $(h(x), h(y))$ is uniform on $\{0,1\}^k \times \{0,1\}^k$, so the family is [pairwise independent](/pairwise-independence/) (a [universal hash family](/universal-hash-family/)). Let $p = 2^{-k}$, so $\Pr[h(x) = 0] = p$ and $\Pr[h(x) = 0 \land h(y) = 0] = p^2$ for $x \ne y$.

*Isolation for the right $k$.* Choose $k$ with $2^{k-2} \le |S| \le 2^{k-1}$, so $1/4 \le |S| p \le 1/2$. Such a $k$ exists in $\{2, \ldots, n + 1\}$ because $1 \le |S| \le 2^n$. For $x \in S$, let $E_x$ be the event that $h(x) = 0$ and $h(y) \ne 0$ for every other $y \in S$. These events are disjoint, and exactly one solution survives if and only if one of them happens. By pairwise independence and the [union bound](/union-bound/),

$$\Pr[E_x] \ge \Pr[h(x) = 0] - \sum_{y \in S, y \ne x} \Pr[h(x) = 0 \land h(y) = 0] \ge p - |S| p^2.$$

Summing over $x \in S$,

$$\Pr[\text{exactly one survives}] \ge |S| p \,(1 - |S| p) \ge \tfrac{1}{4} \cdot \tfrac{1}{2} = \tfrac{1}{8},$$

because $t(1 - t) \ge 1/8$ for $t \in [1/4, 1/2]$.

*Guessing $k$.* The algorithm does not know $|S|$, so it chooses $k$ uniformly from $\{2, \ldots, n + 1\}$. It is right with probability $1/n$, so the success probability is at least $1/(8n)$.

*Back to CNF.* The condition $h(x) = 0$ is $k$ equations of the form $x_{i_1} \oplus \cdots \oplus x_{i_t} = c$. Write each one with new variables and the constraints $z_1 = x_{i_1}$, $z_j = z_{j-1} \oplus x_{i_j}$ for $2 \le j \le t$, and $z_t = c$. Each constraint $z_j = z_{j-1} \oplus x_{i_j}$ is $4$ clauses of width $3$. The values of the new variables are determined by $x$, so the conversion is [parsimonious](/parsimonious-reduction/): the new CNF formula $\psi$ has exactly as many satisfying assignments as there are $x \in S$ with $h(x) = 0$. $\square$

*Proof of the corollary.* Given $\varphi$, repeat the reduction $8n$ times and run the USAT algorithm on each $\psi$. Accept if it accepts some $\psi$. If $\varphi$ is unsatisfiable, every $\psi$ is unsatisfiable, a no-instance of USAT, so the algorithm never accepts. If $\varphi$ is satisfiable, some $\psi$ has exactly one solution with probability at least $1 - (1 - 1/(8n))^{8n} \ge 1 - 1/e$. So $\mathsf{SAT} \in \mathsf{RP}$ and $\mathsf{NP} = \mathsf{RP}$.

**Example.** Let $\varphi = (x_1 \lor x_2) \land (x_3 \lor x_4) \land (\lnot x_1 \lor \lnot x_3)$, with $n = 4$. Its satisfying assignments $x_1x_2x_3x_4$ are $0101$, $0110$, $0111$, $1001$ and $1101$, so $|S| = 5$, and the right $k$ is $4$, since $4 \le 5 \le 8$. Exact probabilities over all choices of $(A, b)$:

| $k$ | $\Pr[\text{exactly one survives}]$ | $\Pr[\text{none survives}]$ |
|---|---|---|
| 1 | $5/32 \approx 0.156$ | $1/32 \approx 0.031$ |
| 2 | $405/1024 \approx 0.396$ | $0.237$ |
| 3 | $12005/32768 \approx 0.366$ | $0.513$ |
| 4 | $253125/1048576 \approx 0.241$ | $0.724$ |
| 5 | $4617605/33554432 \approx 0.138$ | $0.853$ |

For $k = 4$, the proof guarantees $|S|p(1 - |S|p) = (5/16)(11/16) \approx 0.215$, and the true value is $0.241$. With $k$ uniform in $\{2, 3, 4, 5\}$, the success probability is $0.285$, far above the bound $1/(8n) = 1/32$. Here $k = 2$ and $k = 3$ do better than the $k$ of the proof; the analysis only needs one good $k$.

## Consequences

- *Unique solutions are not easier.* Problems with a promise of at most one solution are as hard as the general problem under randomized reductions. This holds for every NP-complete problem with a parsimonious reduction from SAT, because such a reduction keeps a unique solution unique.
- *Parity of the number of solutions.* A formula with exactly one solution has an odd number of solutions, and an unsatisfiable one has an even number. So the same reduction maps SAT to the problem of whether the number of satisfying assignments is odd, and $\mathsf{NP} \subseteq \mathsf{RP}^{\oplus\mathsf{P}}$, where $\oplus\mathsf{P}$ is the class of languages decided by the parity of the number of accepting paths of a nondeterministic polynomial-time machine. Valiant and Vazirani noted this, and Toda (1991) started from it to prove that the whole [polynomial hierarchy](/polynomial-hierarchy/) is in $\mathsf{BP} \cdot \oplus\mathsf{P}$ and then in $\mathsf{P}^{\mathsf{PP}}$.
- *Unambiguous machines.* [UP](/unambiguous-polynomial-time/) is the class of languages accepted by nondeterministic machines with at most one accepting path. The theorem shows that SAT reduces to a promise version of UP by randomized reductions. It does not show $\mathsf{UP} = \mathsf{NP}$.
- *Other isolation results.* The isolation lemma of Mulmuley, Vazirani and Vazirani (1987) isolates a minimum-weight set by random weights instead of hashing, and it is the base of a randomized parallel algorithm for [perfect matching](/perfect-matching/). It is a later and different technique.

## Tightness

- *The success probability.* The reduction succeeds with probability $\Theta(1/n)$, and repetition is needed to make it useful. Dell, Kabanets, van Melkebeek and Watanabe (2013) showed that a randomized polynomial-time isolation procedure of this kind with success probability above $2/3$ would imply $\mathsf{NP} \subseteq \mathsf{P/poly}$, which is believed to be false. So a large improvement is unlikely.
- *Randomness.* No deterministic polynomial-time reduction from SAT to USAT is known. Such a reduction would give $\mathsf{NP} = \mathsf{P}$ from a polynomial-time USAT algorithm, with no randomness.
- *Pairwise independence is enough.* The proof uses only pairwise independence of $h$, which is why a random affine map with $O(nk)$ random bits suffices. A fully random function would need $2^n k$ bits.

## History

Valiant and Vazirani presented the result at STOC 1985, and the journal version appeared in Theoretical Computer Science in 1986 with the title "NP is as easy as detecting unique solutions". The same paper showed that parity SAT is NP-hard under randomized reductions. Toda (1991) used the reduction as a step in his proof that the polynomial hierarchy is in $\mathsf{P}^{\mathsf{PP}}$. Dell, Kabanets, van Melkebeek and Watanabe (CCC 2012, journal 2013) studied whether the probability $\Omega(1/n)$ can be raised.

## References
