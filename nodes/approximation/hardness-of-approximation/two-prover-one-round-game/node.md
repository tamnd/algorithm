---
tag: P8ZS94
kind: definition
slug: two-prover-one-round-game
name: Two-prover one-round game
aliases:
- two-prover game
- PCP game
- 2P1R game
area: approximation/hardness-of-approximation
level: advanced
summary: A verifier sends one random question to each of two provers who cannot communicate, and accepts by a fixed predicate of the questions and answers; the value is the best acceptance probability.
prereqs: [probabilistically-checkable-proof, gap-problem, 3-sat]
see_also: [label-cover, parallel-repetition-theorem, unique-games-conjecture, multi-prover-interactive-proofs, pcp-theorem, gap-amplification, hastad-3bit-pcp]
sources:
  - book: isbn:9780521424264
    title: Sanjeev Arora and Boaz Barak, Computational Complexity, A Modern Approach, Cambridge University Press, 2009
    locator: Chapter 22, Section 22.3 (hardness of 2CSP over large alphabets, two-prover games, projection games and parallel repetition)
  - paper: doi:10.1145/129712.129783
    title: Uriel Feige and László Lovász, Two-prover one-round proof systems, their power and their problems, Proceedings of the 24th ACM Symposium on Theory of Computing (STOC), 1992
    locator: the definition of two-prover one-round proof systems and the value of a game
  - paper: "Michael Ben-Or, Shafi Goldwasser, Joe Kilian and Avi Wigderson, Multi-prover interactive proofs, how to remove intractability assumptions, Proceedings of the 20th ACM Symposium on Theory of Computing (STOC), 1988"
    locator: the model of several provers who cannot communicate
  - paper: "Ran Raz, A parallel repetition theorem, SIAM Journal on Computing 27(3), 763 to 803, 1998"
    locator: the definition of a game and of its value as used for parallel repetition
---

A two-prover one-round game is a protocol in which a verifier picks a pair of questions $(x, y)$ at random, sends $x$ to the first prover and $y$ to the second, receives one answer from each, and accepts by a fixed predicate of the four values. The provers agree on a strategy in advance but cannot communicate after they see their questions. The *value* of the game is the largest acceptance probability that any strategy achieves. Computing the value of a [projection game](/label-cover/) with constant answer size within a constant gap is [NP-hard](/np-hard/) by the [PCP theorem](/pcp-theorem/), and this is the starting point of most tight hardness of approximation results.

## Definition

A *two-prover one-round game* is a tuple $G = (X, Y, A, B, \mu, V)$, where $X$ and $Y$ are finite sets of questions, $A$ and $B$ are finite sets of answers, $\mu$ is a probability distribution on $X \times Y$, and $V : X \times Y \times A \times B \to \{0, 1\}$ is the verifier's predicate. A *strategy* is a pair of functions $f : X \to A$ and $g : Y \to B$. The *value* of $G$ is

$$\operatorname{val}(G) = \max_{f : X \to A,\ g : Y \to B} \ \Pr_{(x, y) \sim \mu}\big[V(x, y, f(x), g(y)) = 1\big] .$$

**Randomized strategies do not help.** Suppose the provers share a random string $r$ and answer $f_r(x)$ and $g_r(y)$. The acceptance probability is $\mathbb{E}_r[p(f_r, g_r)]$, where $p(f, g)$ is the acceptance probability of the deterministic pair. An average is at most the maximum, so it is at most $\operatorname{val}(G)$. The same holds for private randomness, which is a special case.

**Special classes.**
- $G$ is a *projection game* if for each $(x, y)$ in the support of $\mu$ there is a map $\pi_{xy} : A \to B$ with $V(x, y, a, b) = 1$ exactly when $\pi_{xy}(a) = b$. With the questions as the two sides of a bipartite graph, the edge distribution $\mu$ and the labels $A$ and $B$, this is an instance of [label cover](/label-cover/), and $\operatorname{val}(G)$ is the largest fraction of edges (weighted by $\mu$) that a labeling satisfies.
- $G$ is a *unique game* if $A = B$ and each $\pi_{xy}$ is a bijection. This is the class of the [Unique Games Conjecture](/unique-games-conjecture/).
- $G$ is *free* if $\mu$ is a product distribution, so the two questions are independent.

**As a proof system.** A two-prover one-round proof system for a language $L$ is a polynomial-time verifier that, on input $w$, builds a game $G_w$ and plays it once. It has completeness $c$ and soundness $s$ if $w \in L$ implies $\operatorname{val}(G_w) \ge c$ and $w \notin L$ implies $\operatorname{val}(G_w) \le s$. The provers stand for a proof: the two strategy tables $f$ and $g$ are a proof that the verifier reads at two places. This is the bridge to [probabilistically checkable proofs](/probabilistically-checkable-proof/) with two queries over a large alphabet, and to the [gap problem](/gap-problem/) "is $\operatorname{val}(G) = 1$ or is $\operatorname{val}(G) \le s$?".

**The hardness ratio.** On this site a maximization ratio means $\mathrm{ALG} \ge \alpha \cdot \mathrm{OPT}$ with $\alpha \le 1$. If the gap problem with completeness $c$ and soundness $s$ is NP-hard, then no polynomial-time algorithm approximates $\operatorname{val}$ within a ratio $\alpha > s/c$ unless P = NP.

## Examples and non-examples

**The clause-variable game.** Let $\varphi$ be a 3CNF formula with $m$ clauses on variables $v_1, \ldots, v_N$. The verifier picks a clause $C$ uniformly and one of its three variables $v$ uniformly. The first prover receives $C$ and answers an assignment to the three variables of $C$. The second prover receives $v$ and answers a bit. The verifier accepts if the first answer satisfies $C$ and agrees with the second answer on $v$. This is a projection game: the first answer determines the only accepted second answer. Answers have size $8$ and $2$.

- *Completeness.* If $\varphi$ is satisfiable, both provers answer from one satisfying assignment, and the verifier always accepts, so $\operatorname{val} = 1$.
- *Soundness, in full.* Suppose every assignment leaves at least an $\varepsilon$ fraction of the clauses unsatisfied. Fix a strategy $(f, g)$. The second prover's answers form an assignment $\sigma = g$, which leaves a set $U$ of at least $\varepsilon m$ clauses unsatisfied. For $C \in U$, either $f(C)$ does not satisfy $C$ and the verifier rejects for every choice of $v$, or $f(C)$ satisfies $C$ and so differs from $\sigma$ on at least one variable of $C$, and the verifier picks that variable with probability at least $1/3$. So the verifier rejects with probability at least $\Pr[C \in U] / 3 \ge \varepsilon/3$, and $\operatorname{val} \le 1 - \varepsilon/3$. $\square$

By the PCP theorem there is an $\varepsilon_0 > 0$ such that it is NP-hard to tell satisfiable 3CNF formulas from those where every assignment leaves an $\varepsilon_0$ fraction unsatisfied ([Max 3SAT inapproximability](/max-3sat-inapproximability/)). So it is NP-hard to tell projection games of value $1$ from those of value at most $1 - \varepsilon_0/3$. The [parallel repetition theorem](/parallel-repetition-theorem/) then lowers the soundness to any constant $\delta > 0$.

*A number.* The formula on three variables that contains all $8$ clauses with three distinct literals has every assignment violating exactly $1$ clause, so $\varepsilon = 1/8$ and $\operatorname{val} \le 23/24$. This is attained: answer by any assignment $\sigma$ on the variables, and on the one violated clause answer an assignment that differs from $\sigma$ in exactly one variable. So the value is exactly $23/24$.

**The CHSH game.** $X = Y = A = B = \{0, 1\}$, $\mu$ uniform, and the verifier accepts if $a \oplus b = x \wedge y$. It is a free unique game: for each pair of questions, $b = a \oplus (x \wedge y)$ is a bijection of $a$. *Value $3/4$, in full.* A deterministic strategy is four bits $f(0), f(1), g(0), g(1)$. The four conditions $f(x) \oplus g(y) = x \wedge y$ summed over all $(x, y)$ give $0$ on the left (each bit appears twice) and $1$ on the right, so at most $3$ of the $4$ hold. The strategy $f = g = 0$ satisfies $3$.

**The odd cycle game.** Let $m$ be odd. The verifier picks a vertex $v$ of the cycle $C_m$ uniformly, and with probability $1/2$ sends $v$ to both provers, else $v$ to the first and $v + 1 \bmod m$ to the second. Each prover answers a color in $\{0, 1\}$. The verifier accepts if the colors are equal on equal questions and different on adjacent questions. *Value $1 - \tfrac{1}{2m}$, in full.* The $2m$ question pairs are equally likely. If all $m$ pairs $(v, v)$ pass then $f = g$, and if also all $m$ pairs $(v, v+1)$ pass then $f$ is a proper 2-coloring of an odd cycle, which does not exist. So at least one pair fails. A 2-coloring with one monochromatic edge, used by both provers, fails exactly one pair. For $m = 3, 5, 7$ the values are $5/6$, $9/10$ and $13/14$. The [parallel repetition](/parallel-repetition-theorem/) page uses this game to show how slowly the value of a repeated game can fall.

**Non-example: one prover.** If one prover receives both questions, the clause-variable game has value $1$ for every formula: the prover answers any satisfying assignment of $C$ and copies its value at $v$. The value no longer measures satisfiability. The provers' inability to communicate is what forces the second prover's answers to be one fixed assignment.

**Non-example: more rounds.** A protocol in which the verifier sends a second question after it sees the first answers is not a one-round game, and its value is not given by the formula above with fixed tables $f$ and $g$.

## Related definitions

- **Label cover.** The [label cover](/label-cover/) problem is the value of a projection game, written as a bipartite graph with labels. Most hardness reductions start from it.
- **Unique game.** A game whose constraints are bijections. The [Unique Games Conjecture](/unique-games-conjecture/) says that its gap version $1 - \varepsilon$ versus $\delta$ is NP-hard.
- **Parallel repetition.** The game $G^{\otimes k}$ asks $k$ independent question pairs at once and accepts when all $k$ checks pass. The [parallel repetition theorem](/parallel-repetition-theorem/) bounds its value.
- **Multi-prover interactive proofs.** [MIP](/multi-prover-interactive-proofs/) allows several provers and polynomially many rounds. With two provers and one round it already captures NEXP ([MIP = NEXP](/mip-equals-nexp/)).
- **Gap amplification.** [Gap amplification](/gap-amplification/) is another way to raise the gap of a constraint graph, used in Dinur's proof of the PCP theorem.

## References
