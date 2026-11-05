---
tag: PS9ANF
kind: model
slug: probabilistic-finite-automaton
name: Probabilistic finite automaton
aliases:
- PFA
- Rabin probabilistic automaton
- stochastic automaton
area: automata-and-parsing/finite-automata
level: advanced
summary: Automaton whose transitions are probabilistic, accepting with a probability threshold.
prereqs: [deterministic-finite-automaton, markov-chain, myhill-nerode-theorem]
see_also: [weighted-automaton, hidden-markov-model, acceptance-probability, nondeterministic-finite-automaton, two-way-finite-automaton, probabilistic-turing-machine, regular-language, unambiguous-nfa]
sources:
  - paper: "Michael O. Rabin, Probabilistic automata, Information and Control 6(3) (1963)"
    locator: pp. 230 to 245 (the definition, cutpoints, the theorem on isolated cutpoints, and the example with uncountably many languages)
  - paper: "Wen-Guey Tzeng, A polynomial-time algorithm for the equivalence of probabilistic automata, SIAM Journal on Computing 21(2) (1992)"
    locator: pp. 216 to 227 (equivalence of the acceptance functions in polynomial time)
  - book: "Azaria Paz, Introduction to Probabilistic Automata, Academic Press, 1971"
    locator: Chapter 3, on stochastic languages and cutpoints (the undecidability of emptiness with a cutpoint)
  - paper: "Rūsiņš Freivalds, Probabilistic two-way machines, Mathematical Foundations of Computer Science (MFCS 1981), Lecture Notes in Computer Science 118"
    locator: pp. 33 to 45 (a two-way probabilistic automaton with isolated cutpoint for a language that is not regular)
---

A probabilistic finite automaton (PFA) is a finite automaton that, on each input symbol, moves to a random next state according to a fixed probability distribution, and accepts a string when the probability of ending in an accepting state is above a threshold, the *cutpoint*. Rabin (1963) defined the model and proved that with an *isolated* cutpoint a PFA recognizes only [regular languages](/regular-language/), while with an arbitrary cutpoint even a two-state PFA defines uncountably many languages. Equivalence of two PFAs, as functions from strings to probabilities, is decidable in polynomial time (Tzeng, 1992), but emptiness with a cutpoint is undecidable.

## The machine

A PFA is $A = (Q, \Sigma, (M_a)_{a \in \Sigma}, \pi, \eta)$ where $Q = \{1, \ldots, n\}$ is a finite set of states, each $M_a$ is an $n \times n$ *stochastic* matrix (non-negative entries, each row with sum 1), $\pi$ is a probability row vector, the initial distribution, and $\eta \in \{0, 1\}^n$ is the indicator column vector of the set $F$ of accepting states. Entry $(M_a)_{pq}$ is the probability of moving from $p$ to $q$ on $a$. There are no $\varepsilon$-moves, and every state has a distribution on every symbol, so $A$ is complete in the sense of a DFA.

For $w = a_1 \cdots a_\ell$ let $M_w = M_{a_1} M_{a_2} \cdots M_{a_\ell}$, with $M_\varepsilon = I$. The *acceptance probability* is

$$P_A(w) = \pi M_w \eta,$$

the probability that the [Markov chain](/markov-chain/) driven by $w$ ends in $F$. For a cutpoint $\lambda \in [0, 1)$ the language of $A$ is

$$L_{A, \lambda} = \{ w \in \Sigma^* : P_A(w) > \lambda \}.$$

The cutpoint is *isolated* if there is $\delta > 0$ with $|P_A(w) - \lambda| \ge \delta$ for all $w \in \Sigma^*$. A language of the form $L_{A, \lambda}$ is a *stochastic language*.

A [DFA](/deterministic-finite-automaton/) is the special case where each $M_a$ has entries 0 and 1 and $\pi$ is a unit vector; any cutpoint in $[0, 1)$ then gives $L(A)$, and it is isolated.

## What it counts

- **Acceptance probability.** The basic quantity is $P_A(w)$, computed by $\ell$ vector-matrix products in $O(\ell n^2)$ arithmetic operations, or $O(\ell (n + m))$ for $m$ non-zero entries. With rational entries, the number of digits grows linearly in $\ell$, so exact computation stays polynomial.
- **Gap.** With an isolated cutpoint, $\delta$ measures how sure the automaton is, and the theorem below bounds the size of an equivalent DFA in terms of $\delta$.
- **States.** As for other finite automata, the number of states is the size measure.

## Relation to other models

- **DFAs and NFAs.** Every DFA is a PFA. A PFA with cutpoint 0 accepts $w$ if and only if some run with positive probability ends in $F$, which is the language of the NFA with the same non-zero transitions; so cutpoint 0 gives exactly the regular languages.
- **Weighted automata.** A PFA is a [weighted automaton](/weighted-automaton/) over the real numbers with $+$ and $\times$, with stochastic matrices. Many results, such as the equivalence test below, hold for all weighted automata over a field.
- **Hidden Markov models.** A [hidden Markov model](/hidden-markov-model/) emits symbols instead of reading them, and it defines a probability distribution on strings of each length. The forward algorithm of an HMM is the same vector-matrix product.
- **Two-way motion.** Two-way PFAs with an isolated cutpoint recognize some languages that are not regular, such as $\{a^k b^k : k \ge 0\}$ (Freivalds, 1981), unlike [two-way deterministic automata](/two-way-finite-automaton/).
- **Probabilistic Turing machines.** A PFA is a [probabilistic Turing machine](/probabilistic-turing-machine/) with a one-way read-only input and no work tape. The isolated cutpoint corresponds to bounded error.

## Known results in the model

### Isolated cutpoints give regular languages

**Theorem (Rabin, 1963).** If $\lambda$ is isolated for $A$ with gap $\delta > 0$, then $L_{A, \lambda}$ is regular. The proof below shows that its minimal DFA has at most $(1 + 1/\delta)^{n - 1}$ states.

*Proof.* For a string $x$ let $p_x = \pi M_x$, a probability vector. Let $x$ and $y$ be in different classes of the [Myhill-Nerode](/myhill-nerode-theorem/) relation of $L = L_{A, \lambda}$. Then some $z$ has $xz \in L$ and $yz \notin L$, or the reverse, so $P_A(xz) \ge \lambda + \delta$ and $P_A(yz) \le \lambda - \delta$, or the reverse, and $|P_A(xz) - P_A(yz)| \ge 2\delta$. Let $v = M_z \eta$; its entries are in $[0, 1]$, since $M_z$ is stochastic. The vector $d = p_x - p_y$ has entry sum 0, so $d \cdot v = d \cdot (v - \tfrac12 \mathbf 1)$, and each entry of $v - \tfrac12 \mathbf 1$ is in $[-\tfrac12, \tfrac12]$. So

$$2\delta \le |P_A(xz) - P_A(yz)| = |d \cdot v| \le \tfrac12 \lVert d \rVert_1,$$

and $\lVert p_x - p_y \rVert_1 \ge 4\delta$.

Now count. All $p_x$ lie in the simplex $\Delta = \{ p \ge 0 : \sum_i p_i = 1 \}$, which spans an affine space $H$ of dimension $n - 1$. Let $K = \{ u : \sum_i u_i = 0, \lVert u \rVert_1 \le 1 \}$, a convex body in the direction space of $H$. Pick one string $x_c$ in each Myhill-Nerode class $c$. The sets $p_{x_c} + 2\delta K$ have pairwise disjoint interiors, since their centers are at $\ell_1$ distance at least $4\delta$. They all lie in $p_0 + (2 + 2\delta) K$ for any fixed $p_0 \in \Delta$, since $\lVert p - p_0 \rVert_1 \le 2$ for $p \in \Delta$. Comparing $(n - 1)$-dimensional volumes, the number of classes is at most

$$\frac{\mathrm{vol}((2 + 2\delta) K)}{\mathrm{vol}(2\delta K)} = \left(\frac{2 + 2\delta}{2\delta}\right)^{n - 1} = \left(1 + \frac{1}{\delta}\right)^{n - 1}.$$

So $L$ has finitely many classes and is regular. $\square$

### Arbitrary cutpoints give uncountably many languages

Rabin's example over $\{0, 1\}$ has two states $s_0$ (start) and $s_1$ (accepting). On 0, $s_0$ stays, and $s_1$ moves to $s_0$ or stays with probability $\tfrac12$ each. On 1, $s_1$ stays, and $s_0$ moves to $s_1$ or stays with probability $\tfrac12$ each. If $p$ is the probability of being in $s_1$, a symbol $b$ maps $p$ to $(b + p)/2$. So $P_A(a_1 \cdots a_\ell)$ is the binary fraction $0.a_\ell a_{\ell - 1} \cdots a_1$, the input read backwards.

| $w$ | 1 | 10 | 01 | 11 | 110 | 011 | 1101 | 0001 |
|---|---|---|---|---|---|---|---|---|
| $P_A(w)$ | 1/2 | 1/4 | 1/2 | 3/4 | 3/8 | 3/4 | 11/16 | 1/2 |

For cutpoints $\lambda < \lambda'$ in $[0, 1)$ there is a dyadic fraction $P_A(w)$ in $(\lambda, \lambda']$, since these values are dense, and this $w$ is in $L_{A, \lambda}$ but not in $L_{A, \lambda'}$. So the languages $L_{A, \lambda}$ are pairwise different, and there are uncountably many of them. Only countably many languages are regular, so most of them are not regular, and no cutpoint near them is isolated.

### Decision problems

- **Equivalence of the functions** $P_A = P_B$ is decidable in polynomial time (Tzeng, 1992). Let $v_w = (\pi_A M^A_w, \pi_B M^B_w) \in \mathbb{R}^{n_A + n_B}$ and $\theta = (\eta_A, -\eta_B)$, so that $P_A(w) - P_B(w) = v_w \cdot \theta$. Search strings in breadth-first order, and keep $v_w$ only when it is linearly independent of the kept vectors, using [Gaussian elimination](/gaussian-elimination/); extend only kept strings. At most $n_A + n_B$ vectors are kept, and every $v_w$ lies in their span, since $v_{wa} = v_w \cdot \mathrm{diag}(M^A_a, M^B_a)$ is linear in $v_w$. So $P_A = P_B$ if and only if $v_w \cdot \theta = 0$ for each kept $w$. With exact rational arithmetic the time is polynomial.
- **Emptiness with a cutpoint** (is $L_{A, \lambda} \ne \emptyset$?) is undecidable (Paz, 1971).
- **Emptiness with cutpoint 0** is decidable, by the NFA of the non-zero transitions.

### Pitfalls

- **Strict and non-strict inequality.** $P_A(w) > \lambda$ and $P_A(w) \ge \lambda$ can give different languages; with an isolated cutpoint they agree.
- **Isolation is not a property of the automaton alone.** It depends on $\lambda$: one PFA can have isolated and non-isolated cutpoints.
- **Floating point.** Products of many stochastic matrices lose precision; equivalence and threshold questions need exact rational arithmetic, or an error analysis.

## References
