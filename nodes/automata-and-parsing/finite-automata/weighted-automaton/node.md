---
tag: DJ9Y9H
kind: model
slug: weighted-automaton
name: Weighted automaton
aliases:
- weighted finite automaton
- WFA
- K-automaton
area: automata-and-parsing/finite-automata
level: advanced
summary: Automaton whose transitions carry weights from a semiring, computing a weight for each string.
prereqs: [nondeterministic-finite-automaton, matrix-power]
see_also: [probabilistic-finite-automaton, finite-state-transducer, hidden-markov-model, viterbi-algorithm, shortest-path, unambiguous-nfa, nfa-determinization, kleene-algebra]
sources:
  - paper: "Marcel-Paul Schützenberger, On the definition of a family of automata, Information and Control 4(2-3) (1961)"
    locator: pp. 245 to 270 (automata with multiplicities, recognizable and rational series, and the reduction of a representation over a field)
  - book: isbn:9783642014918
    title: Manfred Droste, Werner Kuich and Heiko Vogler (eds.), Handbook of Weighted Automata, Springer, 2009
    locator: Part I, the chapters on semirings and formal power series and on weighted automata (the Kleene-Schützenberger theorem)
  - book: isbn:9780521844253
    title: Jacques Sakarovitch, Elements of Automata Theory, Cambridge University Press, 2009
    locator: Chapter III, Automata with multiplicities (weighted automata, their behavior, and reduction over a field)
  - paper: "Daniel Krob, The equality problem for rational series with multiplicities in the tropical semiring is undecidable, International Journal of Algebra and Computation 4(3) (1994)"
    locator: pp. 405 to 425
  - paper: "Mehryar Mohri, Finite-state transducers in language and speech processing, Computational Linguistics 23(2) (1997)"
    locator: pp. 269 to 311 (determinization of weighted automata over the tropical semiring, the twins property, and the minimization of deterministic weighted automata)
---

A weighted automaton is a finite automaton whose transitions, initial states and final states carry weights from a semiring; it maps each string to the semiring sum, over all accepting paths, of the product of the weights along the path. With the Boolean semiring it is an [NFA](/nondeterministic-finite-automaton/), with the non-negative reals and stochastic matrices a [probabilistic automaton](/probabilistic-finite-automaton/), with $(\min, +)$ a machine for least costs, and with the natural numbers a counter of paths. Schützenberger (1961) introduced the model; over a field, equivalence and minimization are linear algebra and run in polynomial time, while over the tropical semiring equivalence is undecidable (Krob, 1994).

## The machine

**Semiring.** A semiring $(K, \oplus, \otimes, \bar 0, \bar 1)$ has a commutative monoid $(K, \oplus, \bar 0)$, a monoid $(K, \otimes, \bar 1)$, distributivity of $\otimes$ over $\oplus$ on both sides, and $\bar 0 \otimes x = x \otimes \bar 0 = \bar 0$. Common semirings:

| semiring | $K$ | $\oplus$ | $\otimes$ | $\bar 0$ | $\bar 1$ | the weight of a string is |
|---|---|---|---|---|---|---|
| Boolean | $\{0, 1\}$ | or | and | 0 | 1 | whether it is accepted |
| natural numbers | $\mathbb{N}$ | $+$ | $\times$ | 0 | 1 | the number of accepting paths |
| probability | $\mathbb{R}_{\ge 0}$ | $+$ | $\times$ | 0 | 1 | a probability or a sum of products |
| tropical | $\mathbb{N} \cup \{\infty\}$ or $\mathbb{R} \cup \{\infty\}$ | $\min$ | $+$ | $\infty$ | 0 | the cost of a cheapest path |
| Viterbi | $[0, 1]$ | $\max$ | $\times$ | 0 | 1 | the probability of a best path |

**Automaton.** A weighted automaton over $K$ and $\Sigma$ is $A = (Q, \Sigma, \lambda, \mu, \rho)$ with a finite set of states $Q = \{1, \ldots, n\}$, a row vector $\lambda \in K^{1 \times n}$ of initial weights, a matrix $\mu(a) \in K^{n \times n}$ for each $a \in \Sigma$, and a column vector $\rho \in K^{n \times 1}$ of final weights. An entry $\mu(a)_{pq} \ne \bar 0$ is a transition $p \xrightarrow{a} q$ with that weight. There are no $\varepsilon$-moves, and absent transitions have weight $\bar 0$, so the automaton is complete in the matrix sense. Extend $\mu$ to strings by $\mu(a_1 \cdots a_\ell) = \mu(a_1) \otimes \cdots \otimes \mu(a_\ell)$ and $\mu(\varepsilon) = I$. The *behavior* of $A$ is the function

$$[\![A]\!](w) = \lambda \otimes \mu(w) \otimes \rho = \bigoplus_{p_0, \ldots, p_\ell} \lambda_{p_0} \otimes \mu(a_1)_{p_0 p_1} \otimes \cdots \otimes \mu(a_\ell)_{p_{\ell-1} p_\ell} \otimes \rho_{p_\ell},$$

a sum over all paths labeled $w$, which is a *formal power series* $\Sigma^* \to K$. A series is *recognizable* if some weighted automaton has it as behavior.

**Determinism.** $A$ is *deterministic* (or *sequential*) if $\lambda$ has one non-zero entry and each row of each $\mu(a)$ has at most one non-zero entry. Then each string has at most one path.

## What it counts

- **Semiring operations.** Computing $[\![A]\!](w)$ by $\ell$ vector-matrix products costs $O(\ell (n + m))$ semiring operations, where $m$ is the number of transitions. On the [word RAM](/word-ram/) with numbers of bounded size, this is the time; with exact rationals or big integers, the size of the numbers also counts.
- **Dimension.** The size of a weighted automaton is its number of states $n$, also called the dimension of the linear representation $(\lambda, \mu, \rho)$.
- **Sums over all strings.** Quantities such as $\bigoplus_w [\![A]\!](w)$, the total weight, are [shortest-path](/shortest-path/) problems in a general semiring on the graph of the automaton, and need the sum of infinitely many terms to be well defined (for example, non-negative costs in the tropical semiring).

## Relation to other models

- **NFAs.** An NFA is a weighted automaton over the Boolean semiring. Over $\mathbb{N}$, the same automaton counts accepting paths, which equals the indicator of the language exactly when the NFA is [unambiguous](/unambiguous-nfa/).
- **Probabilistic automata and HMMs.** A [probabilistic finite automaton](/probabilistic-finite-automaton/) is a weighted automaton over the probability semiring with stochastic matrices. The forward algorithm of a [hidden Markov model](/hidden-markov-model/) computes a behavior over the probability semiring, and the [Viterbi algorithm](/viterbi-algorithm/) the same over the Viterbi semiring.
- **Transducers.** A [finite-state transducer](/finite-state-transducer/) is a weighted automaton over a semiring of sets of output strings, with union and concatenation; speech and language tools combine both kinds of weights.
- **Rational expressions.** The Kleene-Schützenberger theorem: a series is recognizable if and only if it is rational, that is, built from polynomials by $\oplus$, the Cauchy product and the star, where the star is defined. This extends [Kleene's theorem](/kleene-theorem/) from the Boolean case.

## Known results in the model

### Examples

**Binary value over $\mathbb{N}$.** Let $\Sigma = \{0, 1\}$, $n = 2$, $\lambda = (1, 0)$, $\rho = (0, 1)^{\mathsf T}$ and

$$\mu(0) = \begin{pmatrix} 1 & 0 \\ 0 & 2 \end{pmatrix}, \qquad \mu(1) = \begin{pmatrix} 1 & 1 \\ 0 & 2 \end{pmatrix}.$$

If $(1, v)$ is the row vector after a prefix, the symbol $b$ gives $(1, 2v + b)$. So $[\![A]\!](w)$ is the number written by $w$ in binary: $[\![A]\!](101) = 5$, $[\![A]\!](0110) = 6$, $[\![A]\!](111) = 7$. No automaton of dimension 1 has this behavior, by the Hankel rank below.

**Minimum of two counts over the tropical semiring.** Let $A$ have two states, both with initial and final weight 0. State 1 has loops $a : 1$ and $b : 0$, and state 2 has loops $a : 0$ and $b : 1$. The path that stays in state 1 costs $|w|_a$, the one in state 2 costs $|w|_b$, so $[\![A]\!](w) = \min(|w|_a, |w|_b)$; for example $[\![A]\!](abab) = 2$ and $[\![A]\!](bbba) = 1$.

### Not every weighted automaton can be made deterministic

The subset construction of the [Rabin-Scott theorem](/rabin-scott-theorem/) has no general analogue. **Claim.** No deterministic weighted automaton over the tropical semiring $(\mathbb{N} \cup \{\infty\}, \min, +)$ has the behavior $f(w) = \min(|w|_a, |w|_b)$. *Proof.* Suppose $D$ with $k$ states does. On a deterministic automaton, $f(w)$ is the sum $c(w)$ of the weights along the unique path for $w$, plus the final weight of its last state. Every $f(w)$ is finite, so every string has a path. Among $a^0, a^1, \ldots, a^k$ two strings $a^i$ and $a^j$ with $i < j$ reach the same state $q$. For every $z$, $f(a^i z) - c(a^i) = f(a^j z) - c(a^j)$, because both sides are the cost of $z$ from $q$ plus the final weight. With $z = \varepsilon$: $f(a^i) = f(a^j) = 0$, so $c(a^i) = c(a^j)$. With $z = b^j$: $f(a^i b^j) = i$ and $f(a^j b^j) = j$, so $c(a^j) - c(a^i) = j - i > 0$. This is a contradiction. $\square$ Mohri (1997) gave a determinization algorithm for the tropical semiring that terminates under the *twins property*, a condition on the cycles of the automaton that this example violates.

### Over a field: equivalence and minimization by linear algebra

Let $K$ be a field, such as $\mathbb{Q}$ or $\mathbb{R}$, or a subsemiring of a field such as $\mathbb{N}$, viewed inside $\mathbb{Q}$.

- **Equivalence.** Two automata $A$ and $B$ have the same behavior if and only if the difference automaton, with $\lambda = (\lambda_A, \lambda_B)$, block diagonal $\mu$, and $\rho = (\rho_A, -\rho_B)$, has behavior 0. Search the vectors $\lambda \mu(w)$ in breadth-first order and keep a basis of their span; the behavior is 0 if and only if each basis vector times $\rho$ is 0. At most $n_A + n_B$ vectors are kept, so the test takes polynomially many field operations (Schützenberger, 1961). The same method decides equivalence of probabilistic automata.
- **Minimization.** The *Hankel matrix* of a series $f$ has rows and columns indexed by $\Sigma^*$ and entry $f(uv)$ at $(u, v)$. If $A$ has dimension $n$, then $H = P S$ with $P_{u, \cdot} = \lambda \mu(u)$ and $S_{\cdot, v} = \mu(v) \rho$, so $\mathrm{rank}\, H \le n$. Conversely, a series whose Hankel matrix has finite rank $r$ has a representation of dimension $r$, and it is computed from $A$ by keeping a basis of the reachable vectors $\lambda\mu(u)$ and then of the co-reachable vectors $\mu(v)\rho$. So the minimal dimension is the Hankel rank, computed in polynomial time. For the binary value series, the rows for $\varepsilon$ and $1$ already give rank 2, so the example is minimal.
- **Minimal automata are not unique** as weighted graphs, but they are unique up to a change of basis: all minimal representations are similar by an invertible matrix.

### Over other semirings

- **Tropical semiring.** Equivalence of weighted automata over $(\mathbb{N} \cup \{\infty\}, \min, +)$ is undecidable (Krob, 1994). For deterministic automata it is decidable, for example by putting both in a normal form with weight pushing and minimization (Mohri, 1997) and comparing the results.
- **Boolean semiring.** Equivalence is [NFA equivalence](/nfa-equivalence/), which is PSPACE-complete.
- **Evaluation and best paths.** In every semiring, the weight of one string is computed by the vector-matrix products above, and the best path over all strings by generic shortest-distance algorithms when the semiring sum is well defined.

### Pitfalls

- **Which semiring.** The same graph with the same numbers has different behaviors in different semirings; state the semiring with the automaton.
- **Infinite sums.** With $\varepsilon$-transitions or with sums over all strings, cycles can make the sum diverge; in the tropical semiring a negative cycle makes the minimum $-\infty$.
- **Floating point.** Equivalence tests over $\mathbb{R}$ rely on exact zero tests; with floating point numbers they need a tolerance and lose their guarantee.

## References
