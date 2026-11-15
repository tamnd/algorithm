---
title: STOKE returns only equivalent programs, its chain samples exp(-beta cost), and it is complete in the limit
proves: [correctness]
status: full
---

**Setting.** The machine, the programs of $L$ slots, the cost $c(R) = \mathrm{eq}(R; \tau) + \mathrm{perf}(R)$, the four moves and the acceptance rule are as on the page. $\mathcal{P}$ is the finite set of programs with $L$ slots, and $\mathcal{I}$ the finite set of inputs, with $I = |\mathcal{I}|$. STOKE is lines L1 to L10 of the page. We write $R \equiv T$ when $R$ and $T$ give the same output on every input in $\mathcal{I}$.

## Theorem 1: soundness

*Claim.* The program returned in L10 is equivalent to $T$, whatever the tests, the seed and the number of steps.

*Proof.* Invariant: $\mathit{best} \equiv T$. L2 sets $\mathit{best} = T$. The only other assignment is in L8, and it runs only when $R$ and $T$ agree on every input of $\mathcal{I}$; dropping unused slots does not change the output, since an unused slot does nothing. L10 returns $\mathit{best}$. $\square$

*The test condition alone is not enough.* L7 asks for $\mathrm{eq}(R; \tau) = 0$, which only says that $R$ is right on the inputs of $\tau$. If $\tau \ne \mathcal{I}$, there are programs right on $\tau$ and wrong elsewhere: the page gives `r0 = r0 | r1`, which is right on $(0, 0)$ and $(1, 2)$ for the target $x + y$ and wrong on $(1, 1)$, and a three-instruction program found by the chain that is right on four tests and wrong on 233 of the 256 inputs. So a version of STOKE that accepts in L7 without L8 is not sound.

## Theorem 2: with fixed tests, the chain has stationary distribution $\pi(R) \propto e^{-\beta c(R)}$ and converges to it

Fix the tests. Lines L4 to L6 then define a Markov chain on $\mathcal{P}$ with kernel $K = \frac14 (K_{\mathrm{opc}} + K_{\mathrm{opd}} + K_{\mathrm{swp}} + K_{\mathrm{ins}})$, one kernel per move. Each $K_m$ proposes $R^*$ from $R$ with probability $q_m(R \to R^*)$ and accepts it with probability

$$\alpha_m(R, R^*) = \min\left(1,\; \frac{q_m(R^* \to R)}{q_m(R \to R^*)}\, e^{-\beta (c(R^*) - c(R))}\right).$$

**Step 1: the Hastings factor of each move.** We show that for $R \ne R^*$ with $q_m(R \to R^*) > 0$, the ratio $q_m(R^* \to R) / q_m(R \to R^*)$ is the factor $h$ that the implementation uses: 1 for the first three moves, and $q(R_i)/q(R^*_i)$ for the instruction move.

- *Opcode.* $R^*$ differs from $R$ in the operator of one slot $i$. Both directions pick slot $i$ with probability $1/L$ and then the other operator with probability $1/(|\mathit{ops}| - 1)$. No other slot gives the same change. So the two probabilities are equal.
- *Operand.* $R^*$ differs in one operand place $k$ of one slot $i$, and the instruction kind is the same in $R$ and $R^*$, so both directions have the same number of places and the same pool. Each direction has probability $\frac1L \cdot \frac{1}{\#\text{places}} \cdot \frac{1}{|\text{pool}| - 1}$.
- *Swap.* $R^*$ is $R$ with slots $i \ne j$ swapped. Both directions choose the ordered pairs $(i, j)$ or $(j, i)$, with total probability $2/L^2$ each.
- *Instruction.* $R^*$ differs from $R$ only in slot $i$. From $R$, the move picks slot $i$ with probability $1/L$ and then the new content with probability $q(R^*_i)$, where $q(\text{unused}) = p_u$ and $q(\text{an instruction}) = (1 - p_u)/N$. The reverse picks the old content with probability $q(R_i)$. So the ratio is $q(R_i)/q(R^*_i)$.

**Step 2: detailed balance for each move.** Let $R \ne R^*$, and write $a = \pi(R)\, q_m(R \to R^*)$ and $b = \pi(R^*)\, q_m(R^* \to R)$. If both proposals are 0, both sides below are 0. Otherwise both are positive, by Step 1 (each move can be undone by the same kind of move). Since $\pi(R^*)/\pi(R) = e^{-\beta (c(R^*) - c(R))}$, we have $\alpha_m(R, R^*) = \min(1, b/a)$ and $\alpha_m(R^*, R) = \min(1, a/b)$. Then

$$\pi(R)\, K_m(R, R^*) = a \min(1, b/a) = \min(a, b) = b \min(1, a/b) = \pi(R^*)\, K_m(R^*, R).$$

**Step 3: the mixture.** The move is chosen with probability $\frac14$ each, independently of the state. So $\pi(R) K(R, R^*) = \frac14 \sum_m \pi(R) K_m(R, R^*) = \frac14 \sum_m \pi(R^*) K_m(R^*, R) = \pi(R^*) K(R^*, R)$ for $R \ne R^*$. Summing detailed balance over $R$ gives $\sum_R \pi(R) K(R, R^*) = \pi(R^*)$: $\pi$ is stationary.

**Step 4: convergence.** The chain is *irreducible*: given $R$ and $R'$, the $L$ instruction moves that set slot $1, \ldots, L$ to the content of $R'$ each have positive proposal probability, and every acceptance probability is positive, because $h > 0$ and $e^{x} > 0$. It is *aperiodic*: the instruction move that picks a slot and proposes its current content leaves the program unchanged, with positive probability. A finite irreducible aperiodic chain has a unique stationary distribution, and the distribution of its state converges to it from any start. So the chain converges to $\pi$. $\square$

*Without the Hastings factor.* If the instruction move uses $h = 1$ while $p_u \ne 1/(N + 1)$, Step 2 fails for a pair that differs in one slot, one unused and one not, and $\pi$ is in general not stationary. The page measures this on a machine with 361 programs: with $p_u = 0.5$, the visit frequencies are at total variation distance 0.027 from $\pi$ with the factor and 0.68 without it.

## Theorem 3: completeness in the limit

Let $\ell^* = \min\{\mathrm{perf}(R) : R \in \mathcal{P}, R \equiv T\}$. The set is not empty if $T$ fits in $L$ slots, as L1 assumes.

*Claim.* If the chain runs forever, then with probability 1 there is a step after which $\mathrm{perf}(\mathit{best}) = \ell^*$.

*Proof.* Each time L9 runs, the program $R$ is right on all tests ($\mathrm{eq} = 0$) and wrong on the input $x$ that L9 adds, so $x$ was not a test yet. So L9 runs at most $I$ times, and the tests change at most $I$ times. Let $\sigma$ be the step of the last change, or 0 if none.

After step $\sigma$, the tests are fixed, so the chain moves by the fixed kernel $K$ of Theorem 2, which is irreducible on the finite set $\mathcal{P}$. An irreducible chain on a finite set visits every state infinitely often with probability 1, from any start. Formally: for each of the at most $I + 1$ possible values of the test set, the chain after the time that set is reached is the chain of Theorem 2, and it hits every state with probability 1. A union over finitely many events of probability 0 has probability 0.

Pick $R^{\mathrm{opt}} \in \mathcal{P}$ with $R^{\mathrm{opt}} \equiv T$ and $\mathrm{perf}(R^{\mathrm{opt}}) = \ell^*$. When the chain visits it after $\sigma$, $\mathrm{eq}(R^{\mathrm{opt}}; \tau) = 0$ because it is right on every input. If $\mathrm{perf}(\mathit{best}) > \ell^*$ at that time, L7 holds, the check in L8 passes, and $\mathit{best}$ gets length $\ell^*$. By Theorem 1, $\mathit{best} \equiv T$ always, so its length is never below $\ell^*$, and L7 only lets it go down. $\square$

*What the theorem does not say.* It gives no bound on the number of steps. The time to visit a given program can be exponential in $L$, and in practice it depends on $\beta$, $p_u$ and the cost landscape, as the experiments on the page show. A finite run is a heuristic search with a sound filter.
