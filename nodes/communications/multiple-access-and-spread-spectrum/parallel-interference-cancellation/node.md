---
tag: 9G0E22
kind: algorithm
slug: parallel-interference-cancellation
name: Parallel interference cancellation
aliases:
- multistage interference cancellation
area: communications/multiple-access-and-spread-spectrum
level: advanced
summary: "Decides all users at once, subtracts each user's rebuilt interference from every other user, and repeats in stages; right decisions are a fixed point, but the stages can oscillate."
solves: [multiuser-detection]
model: real-ram
complexity:
  vars: {K: the number of users, N: the number of chips per symbol, J: the number of stages}
  time: {worst: O(K^2 N + J K^2)}
  space: {extra: O(K^2)}
properties: {deterministic: true, linear: false, needs_amplitudes: true, needs_noise_level: false, iterative: true, always_converges: false}
history:
  year: 1990
  people: [Mahesh K. Varanasi, Behnaam Aazhang]
  note: "Varanasi and Aazhang proposed the multistage detector for asynchronous CDMA in 1990 and analyzed it for synchronous CDMA in 1991, including a decorrelator first stage."
prereqs: [successive-interference-cancellation, decorrelating-detector]
see_also: [successive-interference-cancellation, decorrelating-detector, mmse-multiuser-detector, optimum-multiuser-detector, jacobi-method, near-far-problem, decision-feedback-equalizer, matched-filter]
sources:
  - paper: doi:10.1109/26.52662
    title: "Mahesh K. Varanasi and Behnaam Aazhang, Multistage detection in asynchronous code-division multiple-access communications, IEEE Transactions on Communications 38(4), 1990"
    locator: "the multistage detector, its stages, and its error analysis"
  - paper: doi:10.1109/26.87163
    title: "Mahesh K. Varanasi and Behnaam Aazhang, Near-optimum detection in synchronous code-division multiple-access systems, IEEE Transactions on Communications 39(5), 1991"
    locator: "the multistage detector for synchronous users and the decorrelator as its first stage"
  - book: isbn:9780521593731
    title: "Sergio Verdú, Multiuser Detection, Cambridge University Press, 1998"
    locator: "Chapter 7, Decision-driven multiuser detectors"
---

Parallel interference cancellation, or PIC, solves the [multiuser detection](/multiuser-detection/) problem in stages. Stage 0 decides every user, usually with its [matched filter](/matched-filter/). Each later stage rebuilds the signals of all users from the previous decisions, subtracts from each user the rebuilt signals of all the others, and decides again. All users are handled at the same time, so a stage has the delay of one cancellation, unlike [successive interference cancellation](/successive-interference-cancellation/), which handles the users one after another. If the decisions of a stage are all right, the next stage sees no interference at all and stays at the right answer. The method is not guaranteed to get there: a wrong decision doubles the interference it should remove, and with high correlations the stages can oscillate for ever, even without noise. A good first stage, such as the [decorrelating detector](/decorrelating-detector/), helps a lot. Without the sign decisions, PIC is the [Jacobi method](/jacobi-method/) for $R x = z$, and it converges to the decorrelator when the eigenvalues of $R$ lie between 0 and 2.

## In plain words

Every user's signal leaks a little into the receivers of the other users. PIC first makes a rough guess of what every user sent. Then, for each user, it takes out the leak that the guessed signals of all the other users would cause, and guesses again. It does this for all users at once and repeats a few times. If the guesses are right, taking out the leaks leaves each user alone with its noise, and the guesses stay right. If a guess is wrong, the receiver takes out the wrong leak, which makes things worse for the others. With strongly overlapping users, the guesses can flip back and forth and never settle.

## The problem

User $k = 1, \ldots, K$ sends one bit $b_k \in \{-1, +1\}$ per symbol interval with amplitude $A_k > 0$ and a signature $s_k$ of $N$ chips with $\|s_k\| = 1$. The users are synchronous, so the received chips in one interval are $y = S A b + w$, with $S = [s_1, \ldots, s_K]$, $A = \mathrm{diag}(A_k)$ and $w \sim \mathcal{N}(0, \sigma^2 I)$. The receiver knows the signatures and the amplitudes. The output is a decision $\hat b_k$ for each user. The matched filter outputs are $z = S^\top y = R A b + n$, with $R = S^\top S$ and $n \sim \mathcal{N}(0, \sigma^2 R)$.

## The algorithm

```pseudo id=main
PIC(z, R, A, J, b̂⁰)              ▷ b̂⁰ defaults to sgn(z)
L1  b̂ ← b̂⁰                       ▷ stage 0
L2  repeat J times
L3      for every user k, at the same time
L4          x_k ← z_k - Σ_{j≠k} R_kj A_j b̂_j   ▷ cancel all other users
L5          b̂'_k ← sgn(x_k)
L6      b̂ ← b̂'                      ▷ all users change together
L7  return b̂
```

Line L1 takes the first decisions, by default the matched filter signs; the decorrelator decisions are a better start. Lines L3 to L5 compute the new decision of every user from the old decisions of the others. Line L4 is the matched filter output of user $k$ after the rebuilt signals $A_j \hat b_j s_j$ of all other users are subtracted from $y$. Line L6 replaces all the decisions at once; using a new decision as soon as it is made would give a Gauss-Seidel form, which is a different method. Line L5 takes $+1$ for a zero output.

## Example

Three users with $N = 8$ chips use $s_1 = (1,1,1,1,1,1,1,1)/\sqrt 8$, $s_2 = (1,1,1,1,1,1,-1,-1)/\sqrt 8$ and $s_3 = (1,-1,1,-1,1,-1,1,1)/\sqrt 8$, so $R_{12} = 0.5$, $R_{13} = 0.25$ and $R_{23} = -0.25$. The amplitudes are $A = (1, 4, 2)$, the bits are $b = (+1, -1, +1)$, and $\sigma = 0.5$. One noisy draw gave $z = (-0.47, -4.21, 2.18)$.

| stage | $x_1$ | $x_2$ | $x_3$ | decisions |
|---|---|---|---|---|
| 0 | | | | $(-1, -1, +1)$, from $\mathrm{sgn}(z)$ |
| 1 | $1.03$ | $-3.21$ | $1.43$ | $(+1, -1, +1)$ |
| 2 | $1.03$ | $-4.21$ | $0.93$ | $(+1, -1, +1)$ |

At stage 1, user 1 gets $x_1 = -0.47 - (0.5)(4)(-1) - (0.25)(2)(+1) = 1.03$, because the strong user 2 was decided right at stage 0. User 2 still carries the wrong stage 0 decision on user 1, so $x_2 = -4.21 - (0.5)(1)(-1) - (-0.25)(2)(+1) = -3.21$, but it is strong enough to stay right. The stage 1 decisions are all right, so from stage 2 on each $x_k$ is $A_k b_k + n_k$ and nothing changes.

The stages can also fail. Take two users with $\rho = 0.9$, $A = (1, 0.8)$, $b = (+1, -1)$ and no noise. Then $z = (0.28, 0.1)$, and the stages give $(+1, +1)$, $(-1, -1)$, $(+1, +1)$, and so on for ever.

## Correctness

**Claim.** If the decisions of a stage are all right, then at the next stage $x_k = A_k b_k + n_k$ for every user, so without noise all later stages stay right, and with noise each user decides with the single-user error rate $Q(A_k / \sigma)$. For two users without noise and $A_1 \ge A_2$, stage 1 is right for both users when $A_1 > 2 |\rho| A_2$. In general the stages need not converge.

**Key step.** At stage $m$, $x_k = A_k b_k + \sum_{j \ne k} R_{kj} A_j (b_j - \hat b_j) + n_k$, where $\hat b$ holds the decisions of stage $m - 1$. Each term is 0 for a right decision and $2 R_{kj} A_j b_j$ for a wrong one. The full proof, with the oscillation example and the Jacobi form, is in the proofs folder.

## Complexity

With $z$ and $R$, which cost $O(K N)$ and $O(K^2 N)$, each stage computes $K$ sums of $K - 1$ terms, so $J$ stages cost $O(J K^2)$ in the [real RAM](/real-ram/). Done on the chips, a stage rebuilds the sum of all $K$ signals once, at $O(K N)$, and gives each user the sum minus its own signal; this avoids $R$. The users in one stage are independent, so a stage runs in parallel on $K$ processors.

## Properties

- **Right decisions are a fixed point.** From there every user sees only its own signal and noise.
- **Error doubling.** A wrong decision on user $j$ adds $2 R_{kj} A_j b_j$ to user $k$, twice the interference that the matched filter sees.
- **No convergence guarantee.** The stages can cycle, as the two-user example shows. In practice two to four stages are used.
- **Needs amplitudes.** The rebuilt signals need $A_j$, or estimates of it.
- **Linear form.** Removing the signs gives $x^{(m)} = \sum_{i=0}^{m} (I - R)^i z$, the Jacobi iteration for $R x = z$. It tends to $R^{-1} z$ if and only if every eigenvalue of $R$ lies in $(0, 2)$. For the example, the spectral radius of $R - I$ is $(1 + \sqrt 3)/4 \approx 0.68$. Three users with all correlations 0.6 give the eigenvalue 2.2, and the linear form diverges.
- **Low delay.** All users are processed together, so the delay is $J$ cancellations, not $K$.

## Variants and improvements

- **Decorrelator first stage.** Varanasi and Aazhang start from the decorrelator. Without noise its decisions are already right, so the later stages keep them.
- **Partial cancellation.** Subtract only a fraction $c_m < 1$ of the rebuilt interference at early stages, with $c_m$ growing toward 1. This limits the damage of wrong early decisions.
- **Soft decisions.** Rebuild with $\tanh(x_j A_j / \sigma^2)$ or a clipped value instead of the sign, which also limits error doubling.
- **Linear multistage detectors.** Truncating the series $\sum (I - R)^i$ or using a better polynomial in $R$ gives an approximation of the decorrelator or the MMSE detector without a matrix inverse.
- **Group-wise and hybrid forms.** Cancel successively between groups of users and in parallel within a group.
- **Iterative receivers for coded data.** Replace the sign by a soft decoder output, which leads to turbo multiuser detection.

## When to use it

Use PIC when the delay of [successive cancellation](/successive-interference-cancellation/) is too large, when the hardware can process all users in parallel, and when the powers are similar, where SIC orders badly. Start from a decorrelator or an MMSE detector when the correlations are large, and stop after a small fixed number of stages.

## Pitfalls

- **Assuming convergence.** The stages can cycle. Fix the number of stages, or stop when two stages agree.
- **Poor first stage with a strong interferer.** A wrong matched filter decision on a strong user doubles a large interference term. Start from a linear detector in near-far conditions.
- **Gauss-Seidel by accident.** Writing the new decisions into the same array during a stage gives a different, successive update. Keep the old decisions until the stage ends.
- **Wrong amplitudes.** Rebuilt signals with wrong amplitudes leave residual interference on every user at every stage.
- **The linear form with large correlations.** It diverges when an eigenvalue of $R$ is 2 or more, which can happen with many correlated users.

## Implementations

## History

Varanasi and Aazhang proposed the multistage detector for asynchronous CDMA in 1990. Its first stage is a conventional or decorrelating detector, and each later stage cancels the interference estimated from the previous stage. In 1991 they analyzed the synchronous case and showed that, with a decorrelator first stage, the error rate can come close to that of the optimum detector at a much lower cost. Later work added partial and soft cancellation to reduce error doubling, and the same structure returned in iterative receivers for coded CDMA.

## References
