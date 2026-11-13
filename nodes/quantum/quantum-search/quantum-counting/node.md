---
tag: STRRDC
kind: algorithm
slug: quantum-counting
name: Quantum counting
aliases:
- Brassard-Høyer-Tapp counting
area: quantum/quantum-search
level: advanced
summary: Phase estimation on the Grover iteration with P - 1 queries. It estimates the number M of marked items within 2π√(M(N-M))/P + π²N/P² with probability at least 8/π².
solves: [counting-marked-items]
model: quantum-query-model
complexity:
  vars: {N: the number of items, M: the number of marked items, P: the number of phase estimation steps (a power of 2)}
  queries: {worst: P - 1}
  time: {worst: O(P log N + (log P)^2)}
  space: {extra: O(log P)}
properties: {deterministic: false, exact: false, oracle: phase, uses_qft: true, needs_m: false, error: additive}
history:
  year: 1998
  people: [Gilles Brassard, Peter Høyer, Alain Tapp, Michele Mosca]
  note: Boyer, Brassard, Høyer and Tapp sketched the method in 1996. Brassard, Høyer and Tapp gave it at ICALP 1998, and Brassard, Høyer, Mosca and Tapp gave the full error analysis with amplitude estimation.
prereqs: [counting-marked-items, grover-search, quantum-phase-estimation]
see_also: [amplitude-amplification, bbht-search, quantum-fourier-transform, phase-estimation-problem, median-trick, approximate-counting, monte-carlo-integration, grover-optimality]
sources:
  - paper: doi:10.1007/BFb0055105
    title: "Gilles Brassard, Peter Høyer and Alain Tapp, Quantum counting, Proceedings of ICALP 1998, Lecture Notes in Computer Science 1443, Springer, 1998, pages 820-831 (arXiv:quant-ph/9805082)"
    locator: the whole paper (the algorithm Count, with the Fourier transform of the Grover iteration)
  - paper: arxiv:quant-ph/0005055
    title: "Gilles Brassard, Peter Høyer, Michele Mosca and Alain Tapp, Quantum amplitude amplification and estimation, in Quantum Computation and Information, Contemporary Mathematics 305, American Mathematical Society, 2002"
    locator: "the estimation results: Theorem 12 (amplitude estimation, with the 8/pi^2 bound), Theorem 13 (the counting error bound), Theorem 15 (relative error) and Theorem 17 (exact counting)"
  - paper: arxiv:quant-ph/9605034
    title: "Michel Boyer, Gilles Brassard, Peter Høyer and Alain Tapp, Tight bounds on quantum searching, Fortschritte der Physik 46(4-5), 1998, pages 493-505"
    locator: Section 5 (the first sketch of quantum counting)
  - book: isbn:9781107002173
    title: Michael A. Nielsen and Isaac L. Chuang, Quantum Computation and Quantum Information, 10th anniversary edition, Cambridge University Press, 2010
    locator: Chapter 6, Section 6.3 (quantum counting), and Chapter 5, Section 5.2 (phase estimation)
  - paper: arxiv:1908.10846
    title: "Scott Aaronson and Patrick Rall, Quantum approximate counting, simplified, Symposium on Simplicity in Algorithms (SOSA) 2020, pages 24-32"
    locator: the main result (relative-error counting with O(sqrt(N/K)/epsilon) queries and no Fourier transform)
  - paper: arxiv:1904.10246
    title: "Yohichi Suzuki, Shumpei Uno, Rudy Raymond, Tomoki Tanaka, Tamiya Onodera and Naoki Yamamoto, Amplitude estimation without phase estimation, Quantum Information Processing 19, article 75, 2020"
    locator: the main method (maximum likelihood estimation from Grover runs of several lengths)
  - paper: arxiv:1912.05559
    title: "Dmitry Grinko, Julien Gacon, Christa Zoufal and Stefan Woerner, Iterative quantum amplitude estimation, npj Quantum Information 7, article 52, 2021"
    locator: the main algorithm
---

Quantum counting is an algorithm that estimates the number $M$ of marked items among $N$, for a function given as an oracle. It applies [quantum phase estimation](/quantum-phase-estimation/) to the Grover iteration $G$, whose eigenvalues $e^{\pm 2i\theta}$ fix $\sin^2\theta = M/N$. This page is the algorithm; the problem it solves is [counting marked items](/counting-marked-items/). With $P - 1$ queries the estimate is within $2\pi\sqrt{M(N-M)}/P + \pi^2N/P^2$ of $M$ with probability at least $8/\pi^2$, so the error falls as $1/P$, not as $1/\sqrt{P}$ as for classical sampling.

## In plain words

Grover's search turns the state of the computer a little with each step, toward the marked items. The angle of one turn depends only on the share of marked items. If you know the angle, you know the count.

Quantum counting measures this angle. It runs Grover steps 1, 2, 4, 8 and so on times, each run controlled by one extra qubit. The extra qubits then hold the angle as a wave pattern, and a Fourier transform turns the pattern into a number you can read. With twice the steps, the error in the angle halves. A classical sample needs four times the questions to halve its error.

## The problem

The input is a number $N$, a function $f : \{0, 1, \ldots, N-1\} \to \{0, 1\}$ given as a [quantum oracle](/quantum-oracle/), and a number of steps $P = 2^t$. The output is an estimate $\tilde M$ of $M = |\{x : f(x) = 1\}|$. The cost is the number of oracle calls in the [quantum query model](/quantum-query-model/).

The algorithm uses the Grover iteration $G = D\,O_f$ of [Grover's search](/grover-search/), where $O_f|x\rangle = (-1)^{f(x)}|x\rangle$ and $D$ is the [Grover diffusion operator](/grover-diffusion-operator/). Let $\theta \in [0, \pi/2]$ be the angle with $\sin^2\theta = M/N$. On the plane of the uniform states of the marked and the unmarked items, $G$ is the rotation by $2\theta$, so its eigenvalues there are $e^{2i\theta}$ and $e^{-2i\theta}$. The search register has $n = \lceil \log_2 N \rceil$ qubits and the counting register $t$ qubits. As on [quantum state](/quantum-state/), qubit 0 of each register is its least significant bit.

## The algorithm

```pseudo id=main
QUANTUM-COUNTING(O_f, N, t)                 ▷ P = 2^t
L1  prepare |0⟩^t |s⟩                       ▷ |s⟩ is the uniform state on N items
L2  apply H to each counting qubit
L3  for j ← 0 to t - 1
L4      controlled on counting qubit j, apply G^(2^j)   ▷ 2^j queries
L5  apply QFT^(-1) to the counting register
L6  measure the counting register; let y be the result
L7  θ̃ ← π y / P
L8  return M̃ = N sin²(θ̃)
```

Lines L1 to L6 are phase estimation of $G$ with the input $|s\rangle$, which is not an eigenvector but a sum of the two eigenvectors $|\psi_+\rangle$ and $|\psi_-\rangle$ with equal weight. The eigenvalue $e^{2i\theta}$ has the phase $\omega_+ = \theta/\pi$ and $e^{-2i\theta}$ the phase $\omega_- = 1 - \theta/\pi$. The outcome $y$ is near $P\omega_+$ or near $P\omega_-$. Both give the same estimate, because $\sin^2(\pi - \theta) = \sin^2\theta$. The inverse [quantum Fourier transform](/quantum-fourier-transform/) maps $|y\rangle$ to $P^{-1/2}\sum_k e^{-2\pi i yk/P}|k\rangle$.

## Example

Let $N = 16$ and $M = 3$, so $\theta = \arcsin\sqrt{3/16} = 0.4478$, and take $t = 4$, so $P = 16$. Then $P\omega_+ = 16\theta/\pi = 2.281$ and $P\omega_- = 13.719$. The exact distribution of $y$ is symmetric under $y \mapsto 16 - y$:

| $y$ (and $16 - y$) | $\Pr[y]$ | $\tilde M = 16\sin^2(\pi y/16)$ |
|---|---|---|
| 0 | 0.0124 | 0 |
| 1 | 0.0220 | 0.609 |
| 2 | 0.3855 | 2.343 |
| 3 | 0.0603 | 4.939 |
| 4 | 0.0119 | 8 |
| 5 | 0.0057 | 11.061 |
| 6 | 0.0038 | 13.657 |
| 7 | 0.0031 | 15.391 |
| 8 | 0.0029 | 16 |

The two most likely outcomes, $y = 2$ and $y = 14$, have probability $0.771$ together and give $\tilde M = 2.343$. The error bound for $P = 16$ is $2\pi\sqrt{3 \cdot 13}/16 + \pi^2 \cdot 16/256 = 3.069$, and the outcomes $y \in \{0, 1, 2, 3, 13, 14, 15\}$ stay within it, with probability $0.948$. More counting qubits make the bound smaller:

| $t$ | queries $P - 1$ | error bound | $\Pr[\lvert\tilde M - 3\rvert \le \text{bound}]$ | largest $\Pr[y]$ |
|---|---|---|---|---|
| 4 | 15 | 3.069 | 0.948 | 0.386 |
| 5 | 31 | 1.380 | 0.821 | 0.255 |
| 6 | 63 | 0.652 | 0.970 | 0.476 |
| 7 | 127 | 0.316 | 0.903 | 0.408 |

The probability changes with $t$ because it depends on where $P\omega_+$ falls between two grid points; it never goes below $8/\pi^2 = 0.811$.

## Correctness

Claim 2 of the proof writes $G$ as the rotation by $2\theta$ and finds its eigenvectors $|\psi_\pm\rangle = (|\alpha\rangle \mp i|\beta\rangle)/\sqrt2$, with $|s\rangle = (e^{i\theta}|\psi_+\rangle + e^{-i\theta}|\psi_-\rangle)/\sqrt2$. Lines L3 and L4 apply $G^y$ to the term $|y\rangle$. For each eigenvector the inverse Fourier transform gives outcome $k$ with probability $\sin^2(\pi\delta)/(P^2\sin^2(\pi\delta/P))$, where $\delta = P\omega - k$, and the two grid points next to $P\omega$ get at least $8/\pi^2$ together. Each of these points gives an angle $\tilde\theta$ within $\pi/P$ of $\theta$ or of $\pi - \theta$, and $N|\sin^2\tilde\theta - \sin^2\theta| \le 2|\varepsilon|\sqrt{M(N-M)} + N\varepsilon^2$ for $|\varepsilon| \le \pi/P$ gives the bound. For $M = 0$ and $M = N$, $|s\rangle$ is an eigenvector with phase $0$ or $1/2$, and the output is exact. The full proof is in proofs/correctness.md.

## Complexity

Line L4 makes $2^j$ queries for $j = 0, \ldots, t-1$, so a run makes exactly $P - 1$ queries. Each Grover iteration costs $O(\log N)$ gates besides the oracle, and the inverse Fourier transform costs $O(t^2) = O((\log P)^2)$ gates. The extra space is the $t$ counting qubits, plus the work space of the oracle.

The error is additive: $|\tilde M - M| \le 2\pi\sqrt{M(N-M)}/P + \pi^2N/P^2$ with probability at least $8/\pi^2$. Three uses of this bound:

- **About $\sqrt N$ queries.** With $P \approx \sqrt N$ the error is at most $2\pi\sqrt{M} + \pi^2$, so the estimate is good to about the square root of the count.
- **Relative error $\varepsilon$.** If $P \ge 4\pi\sqrt{N/M}/\varepsilon$ and $\varepsilon \le 1$, the error is at most $\varepsilon M/2 + \varepsilon^2M/16 \le \varepsilon M$. For $N = 2^{20}$, $M = 1000$ and $\varepsilon = 0.1$ this gives $P = 4096$, so 4095 queries and a bound of $50.3$, against about $N/(\varepsilon^2 M) \approx 10^5$ samples for a classical estimate. Since $M$ is not known, Theorem 15 of Brassard, Høyer, Mosca and Tapp first finds a $P$ of the right size by doubling, for $O(\sqrt{N/M}/\varepsilon)$ expected queries in total.
- **Smaller failure probability.** $O(\log(1/\eta))$ runs and the [median](/median-trick/) of the estimates fail with probability at most $\eta$.

## Properties

- **Bounded error, additive.** The error bound holds with probability at least $8/\pi^2 \approx 0.81$, not with certainty.
- **No knowledge of $M$.** The algorithm needs only $N$ and $t$. The value of $t$ fixes the cost and the precision.
- **Exact at the ends.** $M = 0$ gives $\tilde M = 0$ and $M = N$ gives $\tilde M = N$ with certainty.
- **Symmetric outcomes.** $y$ and $P - y$ have the same probability and the same estimate. Because $G$, $H$ and $|s\rangle$ are real, the forward Fourier transform in line L5 gives the same distribution as the inverse.
- **Fixed queries.** The number of queries is $P - 1$ for every input; only the outcome is random.

## Variants and improvements

- **Amplitude estimation.** Brassard, Høyer, Mosca and Tapp replace the uniform state by $A|0\rangle$ for any algorithm $A$ and estimate the probability $a$ that $A$ succeeds. This is the same circuit with the iteration of [amplitude amplification](/amplitude-amplification/). Its use for mean estimation gives the quadratic speedup over [Monte Carlo integration](/monte-carlo-integration/).
- **Relative and exact counting.** Theorem 15 of the same paper gives relative error $\varepsilon$ with $O(\sqrt{N/M}/\varepsilon)$ expected queries, and Theorem 17 gives the exact $M$ with $O(\sqrt{(M+1)(N-M+1)})$ expected queries.
- **Counting without a Fourier transform.** Aaronson and Rall give relative-error counting with $O(\sqrt{N/M}/\varepsilon)$ queries from Grover runs of chosen lengths and no counting register. Suzuki and others fit $\theta$ by maximum likelihood from such runs, and Grinko, Gacon, Zoufal and Woerner narrow an interval for $\theta$ step by step. These versions need fewer qubits and shorter circuits.
- **Phase estimation with one qubit.** The counting register can be one qubit that is measured and reused, with classical feedback in place of the Fourier transform. See the [phase estimation problem](/phase-estimation-problem/).

## When to use it

Use quantum counting when you need the number of solutions, or the success probability of a quantum subroutine, to a stated precision. Mean estimation and the tuning of [Grover's search](/grover-search/) are the main uses. To find one marked item when $M$ is not known, [BBHT search](/bbht-search/) is cheaper, because it does not estimate $M$ first. On hardware with few qubits and short circuits, the versions without a Fourier transform are often better. Classically, [approximate counting](/approximate-counting/) with the structure of the problem can beat any oracle method.

## Pitfalls

- **The same power on every qubit.** "L4 controlled on counting qubit $j$, apply $G$" makes the counting state $\sum_y |y\rangle G^{\mathrm{popcount}(y)}|s\rangle$, which is not a phase pattern. Use "L4 controlled on counting qubit $j$, apply $G^{2^j}$".
- **Bit order.** "L4 controlled on counting qubit $t - 1 - j$, apply $G^{2^j}$", with an inverse Fourier transform for the order of these pages, applies $G$ a bit-reversed number of times, so the phases do not form the pattern that the transform focuses. In the example the probability of the error bound falls from $0.948$ to $0.368$. Keep qubit $j$ with $G^{2^j}$, or change the Fourier transform to match.
- **A factor 2 in the angle.** "L7 $\tilde\theta \leftarrow 2\pi y/P$" takes the eigenphase $2\theta$ for $\theta$. Use "L7 $\tilde\theta \leftarrow \pi y/P$".
- **A linear estimate.** "L8 return $\tilde M = N y/P$" treats the phase as the share of marked items. Use "L8 return $\tilde M = N\sin^2(\tilde\theta)$".
- **Expecting relative error from a fixed $P$.** The bound is additive. For small $M$ the bound can be larger than $M$. For $M = 1$ and $N = 2^{20}$ it is $2.19$ at $P = 4096$ and first falls below 1 at $P = 8192$, eight times $\sqrt N$.
- **Counting bit-oracle queries.** The phase oracle is one call of a bit oracle with the target in $|-\rangle$. A controlled $G$ needs a controlled oracle, or the oracle inside the controlled block; the query count stays $P - 1$.

## Implementations

## History

Boyer, Brassard, Høyer and Tapp sketched the idea of estimating the number of solutions from the period of Grover's iteration in Section 5 of their 1996 paper on searching. Brassard, Høyer and Tapp gave quantum counting at ICALP 1998, with the Fourier transform of the iteration in place of a period search. Brassard, Høyer, Mosca and Tapp then put counting into the general frame of amplitude estimation, with the error bound of this page, the relative-error version and the exact version. From 2019 on, Suzuki and others, Aaronson and Rall, and Grinko and others gave versions that avoid the Fourier transform.

## References
