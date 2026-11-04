---
tag: XGRR4T
kind: theorem
slug: yao-minimax-principle
name: Yao's minimax principle
aliases:
- Yao's lemma
- Yao's principle
- distributional lower bound
- distributional lower bound principle
area: foundations/lower-bounds
level: advanced
summary: The best deterministic algorithm on any input distribution costs at most the worst-case expected cost of a randomized algorithm, so a hard distribution bounds randomized algorithms.
prereqs: [randomized-algorithm, expected-value, minimax-theorem]
see_also: [las-vegas-algorithm, monte-carlo-algorithm, zero-sum-game, randomized-query-complexity, game-tree-evaluation, adversary-argument, markov-inequality, decision-tree-model]
sources:
  - paper: doi:10.1109/SFCS.1977.24
    title: "Andrew Chi-Chih Yao, Probabilistic computations: Toward a unified measure of complexity, 18th Annual Symposium on Foundations of Computer Science (FOCS 1977), 222-227"
    locator: the minimax principle for Las Vegas algorithms and its form for algorithms with error
  - paper: doi:10.1007/BF01448847
    title: "John von Neumann, Zur Theorie der Gesellschaftsspiele, Mathematische Annalen 100(1) (1928), 295-320"
    locator: the minimax theorem for finite two-person zero-sum games
  - book: isbn:9780521474658
    title: Rajeev Motwani and Prabhakar Raghavan, Randomized Algorithms, Cambridge University Press, 1995
    locator: Chapter 2, Section 2.2, The minimax principle
  - book: isbn:9780521424264
    title: Sanjeev Arora and Boaz Barak, Computational Complexity, A Modern Approach, Cambridge University Press, 2009
    locator: Chapter 12, Section 12.4.1, Note 12.8 (Yao's min-max lemma)
  - paper: doi:10.1109/SFCS.1986.44
    title: "Michael Saks and Avi Wigderson, Probabilistic Boolean decision trees and the complexity of evaluating game trees, 27th Annual Symposium on Foundations of Computer Science (FOCS 1986), 29-38"
    locator: the lower bound for randomized evaluation of AND-OR trees
---

Yao's minimax principle turns a lower bound for [randomized algorithms](/randomized-algorithm/) into a lower bound for deterministic algorithms on random inputs. It says: for every distribution on the inputs, the expected cost of the best deterministic algorithm on that distribution is at most the worst-case expected cost of any randomized algorithm. So to prove that every randomized algorithm needs expected cost $L$ on some input, it is enough to find one input distribution on which every deterministic algorithm has average cost at least $L$. Yao stated it in 1977, as a consequence of von Neumann's [minimax theorem](/minimax-theorem/).

## Statement

Fix the input size. Let $\mathcal{I}$ be a finite set of inputs and $\mathcal{A}$ a finite set of deterministic algorithms. Let $C(I, A) \ge 0$ be the cost of $A$ on $I$, for example the number of queries in the [decision tree model](/decision-tree-model/). A *randomized algorithm* is a probability distribution $q$ on $\mathcal{A}$: it draws $A \sim q$ and runs $A$. An *input distribution* is a probability distribution $p$ on $\mathcal{I}$. Write $C(p, A) = \mathbb{E}_{I \sim p}[C(I, A)]$ and $C(I, q) = \mathbb{E}_{A \sim q}[C(I, A)]$.

**Theorem 1 (Las Vegas form).** Let every algorithm in $\mathcal{A}$ be correct on every input in $\mathcal{I}$. For every input distribution $p$ and every randomized algorithm $q$,

$$\min_{A \in \mathcal{A}} C(p, A) \ \le\ \max_{I \in \mathcal{I}} C(I, q).$$

Moreover, with $p$ ranging over all distributions on $\mathcal{I}$ and $q$ over all distributions on $\mathcal{A}$,

$$\max_{p} \min_{A \in \mathcal{A}} C(p, A) \ =\ \min_{q} \max_{I \in \mathcal{I}} C(I, q).$$

The left side is the *distributional complexity* and the right side is the *randomized complexity* of the problem for the class $\mathcal{A}$.

For algorithms that may err, let $\mathcal{A}$ be any finite set of deterministic algorithms, and let $e(I, A) = 1$ if $A$ gives a wrong answer on $I$ and $e(I, A) = 0$ otherwise. Write $e(p, A) = \mathbb{E}_{I \sim p}[e(I, A)]$.

**Theorem 2 (Monte Carlo form).** Let $\varepsilon \ge 0$, and let $q$ be a randomized algorithm with error at most $\varepsilon$ on every input: $\mathbb{E}_{A \sim q}[e(I, A)] \le \varepsilon$ for all $I \in \mathcal{I}$. Let $T = \max_{I} C(I, q)$. Then for every input distribution $p$ and every $\alpha$ with $0 < \alpha < 1$ there is an $A$ with $q(A) > 0$ such that

$$e(p, A) \le \varepsilon/\alpha \qquad\text{and}\qquad C(p, A) \le T/(1 - \alpha).$$

With $\alpha = 1/2$: there is a deterministic $A$ with error at most $2\varepsilon$ under $p$, and

$$\tfrac{1}{2} \min_{A :\ e(p, A) \le 2\varepsilon} C(p, A) \ \le\ \max_{I \in \mathcal{I}} C(I, q).$$

So a lower bound $L$ on the expected cost of every deterministic algorithm that errs with probability at most $2\varepsilon$ under $p$ gives the lower bound $L/2$ on the worst-case expected cost of every randomized algorithm with error at most $\varepsilon$.

## In plain words

Think of a game. You pick an algorithm, and an opponent picks the input. You pay the running time. A randomized algorithm is a way to pick the algorithm by a coin toss, and the opponent may also pick the input by a coin toss.

The principle says that you can prove a lower bound for the coin-tossing algorithm without knowing anything about its coins. Choose a way to draw hard inputs. Show that every fixed algorithm, even one built to know how you draw the inputs, has a high average cost. Then each randomized algorithm also has a high average cost on at least one input, because it is only a mix of fixed algorithms.

Von Neumann's theorem on games adds that this method is complete: the best such bound is always the true answer.

## Proof

**Theorem 1, the inequality.** Both expectations are finite sums, so their order can be swapped:

$$\mathbb{E}_{A \sim q}\big[C(p, A)\big] = \sum_{A}\sum_{I} q(A)\,p(I)\,C(I, A) = \mathbb{E}_{I \sim p}\big[C(I, q)\big].$$

The left side is an average of the numbers $C(p, A)$, so it is at least their minimum $\min_A C(p, A)$. The right side is an average of the numbers $C(I, q)$, so it is at most their maximum $\max_I C(I, q)$. Together these give the inequality. $\square$

**Theorem 1, the equality.** Consider the [zero-sum game](/zero-sum-game/) with the matrix $M[I, A] = C(I, A)$, where one player chooses a row $I$ and wants a high cost, and the other chooses a column $A$ and wants a low cost. For a mixed strategy $p$ of the row player, the best reply of the column player is a pure strategy, because $C(p, q') = \sum_A q'(A) C(p, A)$ is an average of the values $C(p, A)$; so $\min_{q'} C(p, q') = \min_A C(p, A)$. In the same way $\max_{p'} C(p', q) = \max_I C(I, q)$. The [minimax theorem](/minimax-theorem/) of von Neumann (1928) says that for a finite matrix game $\max_p \min_{q'} C(p, q') = \min_q \max_{p'} C(p', q)$. With the two remarks this is the claimed equality. The inequality "$\le$" is the part proved above; only "$\ge$" needs von Neumann's theorem, and the lower bounds use only "$\le$". $\square$

**Theorem 2.** First let $\varepsilon > 0$ and $T > 0$. By the swap of finite sums as above,

$$\mathbb{E}_{A \sim q}[e(p, A)] = \mathbb{E}_{I \sim p}\,\mathbb{E}_{A \sim q}[e(I, A)] \le \varepsilon, \qquad \mathbb{E}_{A \sim q}[C(p, A)] = \mathbb{E}_{I \sim p}[C(I, q)] \le T.$$

Let $Z(A) = \alpha\, e(p, A)/\varepsilon + (1 - \alpha)\, C(p, A)/T$. By linearity of expectation, $\mathbb{E}_{A \sim q}[Z(A)] \le \alpha + (1 - \alpha) = 1$. A random variable is at most its mean with positive probability, so some $A$ with $q(A) > 0$ has $Z(A) \le 1$. Both terms of $Z(A)$ are non-negative, so each is at most 1: $\alpha\, e(p, A)/\varepsilon \le 1$ and $(1 - \alpha)\, C(p, A)/T \le 1$. These are the two claims.

If $\varepsilon = 0$, then $\sum_A q(A) e(I, A) = 0$ with non-negative terms, so $e(I, A) = 0$ for every $I$ and every $A$ with $q(A) > 0$. Pick such an $A$ with $C(p, A) \le \mathbb{E}_{A \sim q}[C(p, A)] \le T$. If $T = 0$, then in the same way $C(I, A) = 0$ for every $I$ and every $A$ with $q(A) > 0$; pick such an $A$ with $e(p, A) \le \mathbb{E}_{A \sim q}[e(p, A)] \le \varepsilon$. In both cases the claims hold.

The last display follows with $\alpha = 1/2$: the $A$ found has $e(p, A) \le 2\varepsilon$, so it is one of the algorithms in the minimum, and $C(p, A) \le 2T$. $\square$

The argument is a joint form of [Markov's inequality](/markov-inequality/). Two separate uses of Markov's inequality, each with probability $1/2$ of failure, would not be enough, since the two bad events could cover all algorithms.

### Example: find a 1

The input is an array of $n$ bits with exactly $k \ge 1$ ones. An algorithm probes positions until it sees a 1, and the cost is the number of probes. Until it finds a 1 every probe answers 0, so a deterministic algorithm that never probes a position twice is fixed by an order of the positions. So $\mathcal{A}$ is the set of the $n!$ orders, and $\mathcal{I}$ is the set of the $\binom{n}{k}$ inputs.

- *Deterministic worst case.* For each order, the adversary puts the $n - k$ zeros on the first $n - k$ positions of the order. So every deterministic algorithm needs $n - k + 1$ probes on some input, and probing in any order achieves this.
- *Randomized upper bound.* Probe in a uniformly random order. Fix the input. A position that holds a 0 is probed before all $k$ ones with probability $1/(k + 1)$, since each of these $k + 1$ positions is first among them with equal chance. By [linearity of expectation](/linearity-of-expectation/) the expected number of zeros probed is $(n - k)/(k + 1)$, so the expected cost is $(n + 1)/(k + 1)$ on every input.
- *Randomized lower bound.* Let $p$ be uniform on $\mathcal{I}$. For a fixed order, the set of ones is a uniformly random $k$-set, and the same argument gives $C(p, A) = (n + 1)/(k + 1)$ for every order $A$. By Theorem 1, every randomized algorithm has some input with expected cost at least $(n + 1)/(k + 1)$.

So the random order is optimal, and the value of the game is $(n + 1)/(k + 1)$.

| $n$ | $k$ | deterministic worst case | randomized complexity |
|---|---|---|---|
| 4 | 2 | 3 | 5/3 |
| 6 | 3 | 4 | 7/4 |
| 8 | 4 | 5 | 9/5 |
| 5 | 1 | 5 | 3 |

With half the bits equal to 1, a deterministic algorithm needs $n/2 + 1$ probes, while randomization needs fewer than 2 in expectation.

## Consequences

- **The usual recipe.** To show that every randomized algorithm of a class has expected cost at least $L$ on some input of size $n$, give one distribution $p$ on inputs of size $n$ and prove $C(p, A) \ge L$ for every deterministic $A$ of the class. The proof for deterministic algorithms may use the fact that $A$ knows $p$.
- **Completeness.** By the equality in Theorem 1, for a finite class the best bound that the recipe can give is exactly the randomized complexity. So if a lower bound on the randomized complexity is true, some input distribution proves it.
- **Game trees.** Saks and Wigderson (1986) used a hard distribution of this kind to show that randomized evaluation of a complete binary AND-OR tree with $n$ leaves needs expected $\Omega(n^{\gamma})$ leaf queries with $\gamma = \lg\bigl((1 + \sqrt{33})/4\bigr) \approx 0.7537$, which matches the known randomized algorithm. See [game tree evaluation](/game-tree-evaluation/).
- **Other models.** The same averaging works for any cost: comparisons, cell probes, bits of communication in [communication complexity](/communication-complexity/), queries in [randomized query complexity](/randomized-query-complexity/).

### Pitfalls

- **The worst input, not a random input.** The principle bounds the expected cost of a randomized algorithm on its worst input. It does not bound its cost on the input distribution $p$; a randomized algorithm can do very well on a random input.
- **The deterministic algorithm may depend on $p$.** The lower bound must hold for every deterministic algorithm, including those tuned to $p$. A distribution that is hard only for "natural" algorithms proves nothing.
- **Finite sets.** The theorem is stated for a fixed input size, a finite set of inputs and a finite set of algorithms. In a query model of fixed size this holds after removing repeated queries. For a Las Vegas algorithm whose running time is unbounded, first cut the runs at a large bound, or use the inequality, which holds whenever $p$ and $q$ have finite support.
- **Error costs a factor.** With errors, Theorem 1 does not apply as stated, because the deterministic algorithms in $q$ are not correct. Theorem 2 loses a factor 2 in the cost and a factor 2 in the error (or $1/(1-\alpha)$ and $1/\alpha$). The error bound $\varepsilon$ must hold on every input, not only on average.
- **A distribution with tiny support.** If $p$ puts all its weight on one input, some deterministic algorithm answers that input at once. A good hard distribution spreads its weight so that no single algorithm guesses well.

## Tightness

- **The inequality can be strict for a given $p$ and $q$.** In the find-a-1 game with $n = 4$ and $k = 2$, the point mass $p$ on one input gives $\min_A C(p, A) = 1$, while every $q$ has $\max_I C(I, q) \ge 5/3$. Equality needs the best $p$ and the best $q$, and von Neumann's theorem says that they exist.
- **The factor 2 in Theorem 2.** The trade-off between $\varepsilon/\alpha$ and $T/(1-\alpha)$ is what the averaging gives; a lower bound proved for error $2\varepsilon$ under $p$ transfers to error $\varepsilon$ in the worst case. Taking $\alpha$ close to 1 keeps the error near $\varepsilon$ at the price of a large factor in the cost.

## History

Von Neumann (1928) proved the minimax theorem for finite two-person zero-sum games. Yao (1977) observed that the randomized complexity of a problem is the value of a game between the designer of the algorithm and the chooser of the input, and stated the two forms above as a way to prove lower bounds for randomized algorithms. The textbooks of Motwani and Raghavan (1995) and Arora and Barak (2009) present it as the main tool for randomized lower bounds in query models. Saks and Wigderson (1986) gave one of its best-known uses, the tight bound for evaluating AND-OR trees.

## References
