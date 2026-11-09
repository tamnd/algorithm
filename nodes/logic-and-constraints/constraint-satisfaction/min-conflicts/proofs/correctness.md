---
title: Min-conflicts is sound but not complete
proves: [correctness]
status: full
---

We prove two claims about MIN-CONFLICTS (lines L1 to L7). First, every assignment it returns is a solution. Second, there is a CSP with a solution on which it returns failure for every step limit and every sequence of random choices.

## Setting

A CSP has variables $x_1, \ldots, x_n$, finite domains, and constraints. Each constraint $c$ has a nonempty scope $\text{vars}(c)$ and a relation. A complete assignment $\sigma$ violates $c$ if the restriction of $\sigma$ to $\text{vars}(c)$ is not in the relation of $c$. For a variable $x$, a value $v$ and a complete assignment $\sigma$, $\text{conflicts}(x, v, \sigma)$ is the number of constraints $c$ with $x \in \text{vars}(c)$ that are violated by $\sigma[x \mapsto v]$. The variable $x$ is conflicted in $\sigma$ if $\text{conflicts}(x, \sigma(x), \sigma) > 0$.

## Soundness

**Claim.** If MIN-CONFLICTS returns an assignment $\sigma$, then $\sigma$ satisfies every constraint.

**Proof.** The only line that returns an assignment is L3, and it does so only when no variable is conflicted in $\sigma$. Suppose that some constraint $c$ is violated by $\sigma$. Its scope is nonempty, so take any $x \in \text{vars}(c)$. Since $\sigma[x \mapsto \sigma(x)] = \sigma$, the constraint $c$ is one of the constraints on $x$ that are violated by $\sigma[x \mapsto \sigma(x)]$. So $\text{conflicts}(x, \sigma(x), \sigma) \geq 1$, and $x$ is conflicted. This contradicts the test at L3. So no constraint is violated, and $\sigma$ is a solution. $\blacksquare$

The claim does not depend on how L1 builds the first assignment or on the random choices at L4 and L5, because L3 checks the current assignment directly. Line L6 changes only the value of $x$, so $\sigma$ stays a complete assignment with values in the domains, since L5 picks $v$ from $D(x)$.

## Incompleteness

**Claim.** There is a CSP with a solution and a start assignment from which MIN-CONFLICTS returns failure for every step limit $s \geq 0$ and every result of the random choices.

**Proof.** Take three variables $a, b, c$ with domain $\{0, 1\}$ and the constraints

- $C_{ab}$ on $(a, b)$, which allows only $(1, 1)$,
- $C_{ac}$: $a = c$,
- $C_{bc}$: $b = c$.

The assignment $(1, 1, 1)$ satisfies all three, so the CSP has a solution. It is the only solution, since $C_{ab}$ forces $a = b = 1$ and then $C_{ac}$ forces $c = 1$.

Let the start at L1 be $\sigma_0 = (0, 0, 0)$. We show by induction on the number of steps that $\sigma = \sigma_0$ at the start of every iteration of the loop at L2.

Base: before the first iteration, $\sigma = \sigma_0$.

Step: assume $\sigma = \sigma_0$ at the start of an iteration. In $\sigma_0$, $C_{ac}$ and $C_{bc}$ hold and $C_{ab}$ is violated. So $a$ and $b$ are conflicted, and $c$ is not, since both constraints on $c$ hold. L3 does not return. L4 chooses $a$ or $b$.

- If L4 chooses $a$: for $v = 0$, $\sigma_0[a \mapsto 0] = (0, 0, 0)$ violates $C_{ab}$ only, so the count is 1. For $v = 1$, $(1, 0, 0)$ violates $C_{ab}$, since $(1, 0)$ is not allowed, and $C_{ac}$, since $1 \neq 0$. The count is 2. The unique smallest count is at $v = 0$, so L5 chooses 0 and L6 leaves $\sigma = \sigma_0$.
- If L4 chooses $b$: the same computation with $C_{bc}$ in place of $C_{ac}$ gives counts 1 for $v = 0$ and 2 for $v = 1$, so again $\sigma$ stays $\sigma_0$.

So $\sigma = \sigma_0$ at the start of the next iteration. Since $\sigma_0$ is not a solution, L3 never returns, and after $s$ iterations the loop ends and L7 returns failure. This holds for all $s$ and all random choices, because in both cases the choice at L5 is forced. $\blacksquare$

## Remarks

- The proof uses a fixed start. A random start at L1 picks $(0, 0, 0)$ with probability $1/8$, so with a random start the method also fails with positive probability for every step limit. This is enough to show that the method is not complete.
- MIN-CONFLICTS never returns "no solution". On a CSP without a solution, L3 never returns, by soundness, so every run ends at L7. A failure therefore gives no information about whether a solution exists.
