---
tag: N3W415
kind: technique
slug: doubling-trick
name: Doubling trick
aliases:
- doubling strategy
- guess and double
area: online-and-streaming/competitive-analysis
level: intro
summary: When an algorithm needs an unknown parameter, guess it, double the guess each time it fails, and restart. For a regret bound α sqrt(T) this costs only a factor sqrt(2)/(sqrt(2) - 1) ≈ 3.41.
prereqs: [regret, geometric-series]
see_also: [online-gradient-descent, multiplicative-weights-update, exponential-search, array-doubling, linear-search-problem, exponential-backoff, competitive-ratio, iterative-deepening-search]
sources:
  - book: isbn:9780521841085
    title: Nicolo Cesa-Bianchi and Gabor Lugosi, Prediction, Learning, and Games, Cambridge University Press, 2006
    locator: Section 2.3 (bounds that hold uniformly over time, the doubling trick and the factor sqrt(2)/(sqrt(2) - 1)) and the exercises of Chapter 2
  - paper: doi:10.1145/258128.258179
    title: "Nicolo Cesa-Bianchi, Yoav Freund, David Haussler, David P. Helmbold, Robert E. Schapire and Manfred K. Warmuth, How to use expert advice, Journal of the ACM 44(3) (1997), 427-485"
    locator: the use of doubling to handle an unknown horizon and an unknown loss of the best expert
  - paper: doi:10.1137/S0097539701398375
    title: "Peter Auer, Nicolo Cesa-Bianchi, Yoav Freund and Robert E. Schapire, The nonstochastic multiarmed bandit problem, SIAM Journal on Computing 32(1) (2002), 48-77"
    locator: Section 4 (Exp3.1, which runs Exp3 in epochs with a doubling guess of the best total reward)
  - paper: doi:10.1016/0020-0190(76)90071-5
    title: "Jon Louis Bentley and Andrew Chi-Chih Yao, An almost optimal algorithm for unbounded searching, Information Processing Letters 5(3) (1976), 82-87"
    locator: the doubling search for an unbounded sorted list, with about 2 log2 p comparisons
  - paper: doi:10.1006/inco.1993.1054
    title: "Ricardo A. Baeza-Yates, Joseph C. Culberson and Gregory J. E. Rawlins, Searching in the plane, Information and Computation 106(2) (1993), 234-252"
    locator: the doubling strategy on the line (the cow path problem) and its optimal competitive ratio 9
---

The doubling trick turns an algorithm that needs to know a parameter in advance, such as the number of rounds $T$, the size of the answer, or the optimal cost, into one that does not. It guesses a value, runs the algorithm tuned for that guess, and when the guess turns out too small it doubles the guess and starts again. Because the costs of the phases grow geometrically, the last phase dominates, and the total is within a constant factor of the cost with the right guess: for a [regret](/regret/) bound $\alpha\sqrt{T}$ the factor is $\sqrt2/(\sqrt2 - 1) = 2 + \sqrt2 \approx 3.41$. The same idea gives [exponential search](/exponential-search/), [array doubling](/array-doubling/) and the 9-competitive strategy for the [linear search problem](/linear-search-problem/).

## In plain words

Sometimes a good plan needs a number that you do not know yet, such as how long a game will last. Guess a small number and play as if it were right. If the game goes on past your guess, take twice the guess and start over with a fresh plan.

This seems wasteful, because you throw away earlier work. But each new phase is twice as long as the one before, so all the earlier phases together are about as long as the last one. You lose at most a constant factor compared with a player who knew the number from the start. The method is simple and works with almost any algorithm, so it is a standard first step before a more careful design.

## When it applies

- An algorithm $A(N)$ has a good guarantee when it knows a parameter $N$, and the parameter is unknown. Examples are the horizon $T$, the loss $L^*$ of the best expert, the position $p$ of a target, or the optimal cost.
- The guarantee of $A(N)$ holds for every **prefix** of the input of length at most $N$, or the algorithm can **detect** that its guess was too small. Without one of the two, the algorithm does not know when to restart.
- The cost of a phase with guess $N$ grows at least geometrically in the number of doublings, such as $\alpha N^\gamma$ with $\gamma > 0$ or $cN$. The geometric sum is then a constant times its last term.
- Restarting is allowed: the phases may forget their state, and the total cost is at most the sum of the costs of the phases. For regret, this holds because the best fixed action of the whole input is at least as costly as the sum of the best actions of the phases.

## The template

```pseudo id=main
DOUBLING(A, N_0)
L1  m ← 0
L2  repeat
L3      N ← 2^m · N_0                      ▷ the current guess
L4      start a fresh copy of A tuned for N
L5      run it until the input ends or the guess is shown too small
L6      m ← m + 1
L7  until the input ends
```

For an unknown horizon, line L5 runs the copy for exactly $2^m N_0$ rounds. For an unknown target or optimal cost, it runs until the copy reports failure.

**Theorem (unknown horizon).** Let $A(N)$ have regret at most $\alpha\sqrt N$ on every input of length $t \le N$. Then DOUBLING with $N_0 = 1$ has regret at most $\frac{\sqrt2}{\sqrt2 - 1}\,\alpha\sqrt T$ on every input of every length $T \ge 1$.

*Proof.* Phase $m$ covers the rounds $2^m, \ldots, 2^{m+1} - 1$, so phases $0, \ldots, m-1$ cover $2^m - 1$ rounds. Let $M$ be the last phase that starts, so $2^M - 1 < T$, which gives $2^M \le T$. Phase $m$ sees at most $2^m$ rounds, so its regret against the best action of that phase is at most $\alpha\sqrt{2^m}$, also if it is the last phase and is cut short, by the prefix condition. Let $L^{(m)}(i)$ be the loss of action $i$ in phase $m$. The best action of the whole input pays $\min_i\sum_m L^{(m)}(i) \ge \sum_m \min_i L^{(m)}(i)$. So the total regret is at most the sum of the regrets of the phases:

$$R_T \le \sum_{m=0}^{M}\alpha\sqrt{2^m} = \alpha\,\frac{\sqrt2^{\,M+1} - 1}{\sqrt2 - 1} < \alpha\,\frac{\sqrt2}{\sqrt2 - 1}\sqrt{2^M} \le \frac{\sqrt2}{\sqrt2 - 1}\,\alpha\sqrt T. \qquad \square$$

The same proof for a bound $\alpha N^\gamma$ with $\gamma > 0$ gives the factor $\frac{2^\gamma}{2^\gamma - 1}$. For $\gamma = 1/2$ it is $2 + \sqrt2 \approx 3.414$, and for $\gamma = 1$ it is $2$. The analysis is tight: at $T = 2^M$ a new phase has just started, the sum is $\alpha(\sqrt2^{M+1} - 1)/(\sqrt2 - 1)$, and the ratio to $\alpha\sqrt T$ tends to $2 + \sqrt2$ as $M$ grows.

## Classic examples

- **Hedge with unknown $T$.** [Hedge](/multiplicative-weights-update/) with $\eta = \sqrt{8\ln n/N}$ has regret at most $\frac{\ln n}{\eta} + \frac{\eta t}{8} \le \sqrt{(N/2)\ln n}$ for every $t \le N$, so the prefix condition holds with $\alpha = \sqrt{(\ln n)/2}$. Doubling gives regret at most $(2 + \sqrt2)\sqrt{(T/2)\ln n} \approx 2.41\sqrt{T\ln n}$. For $n = 2$ and $T = 100$ the phases have lengths $1, 2, 4, 8, 16, 32$ and $37$, and the sum of the phase bounds is about $14.66$, against $5.89$ for Hedge tuned for $T = 100$, a ratio of about $2.49$.
- **Unknown loss of the best expert.** Bounds of the form $O(\sqrt{L^*\ln n} + \ln n)$ need $L^*$ to set $\eta$. Guess $L^* \le 4^m$, and restart when the best expert of the phase passes the guess (Cesa-Bianchi et al. 1997). Exp3.1 does the same for the [multi-armed bandit](/multi-armed-bandit/) with a guess of the best total reward (Auer et al. 2002).
- **Exponential search.** To find a key in a sorted list of unknown length, probe the positions $1, 2, 4, \ldots$ until an entry is at least the key, then binary search in the last range. This takes about $2\log_2 p$ comparisons for a key at position $p$ (Bentley and Yao 1976); see [exponential search](/exponential-search/).
- **Array doubling.** A [dynamic array](/dynamic-array/) doubles its capacity when it is full. The copies cost $1 + 2 + 4 + \cdots < 2n$ for $n$ appends, so each append costs $O(1)$ amortized; see [array doubling](/array-doubling/).
- **Searching on a line.** A target lies at an unknown distance $d \ge 1$ on one side of the start. Walk to $+1$, back to $-2$, to $+4$, and so on. The total distance is at most $9d$, and no deterministic strategy has a smaller competitive ratio (Baeza-Yates, Culberson and Rawlins 1993); see the [linear search problem](/linear-search-problem/).
- **Contention.** [Exponential backoff](/exponential-backoff/) doubles the waiting window after each collision, which is a doubling guess of the number of competing senders.

## Variations

- **Guess the optimal cost.** If an online algorithm $A(\Lambda)$ costs at most $c\Lambda$ when $\Lambda \ge \mathrm{OPT}$, and it detects when $\Lambda < \mathrm{OPT}$, run it with $\Lambda = 2^m\Lambda_0$ and double after each failure. The final guess is less than $2\,\mathrm{OPT}$ (if $\Lambda_0 \le \mathrm{OPT}$), and the costs of the phases sum to less than $2c$ times the final guess, so the total is at most $4c \cdot \mathrm{OPT}$. This is a standard step in online load balancing and online clustering.
- **Other growth factors.** Phases of length $b^m$ for a real $b > 1$ cover $(b^M - 1)/(b - 1)$ rounds before phase $M$, so $b^M < (b - 1)T + 1$. The same sum gives, for large $T$, the factor $\frac{\sqrt{b(b-1)}}{\sqrt b - 1}$ for a bound $\alpha\sqrt N$. It is $3.41$ for $b = 2$, $3.46$ for $b = 4$, and least, about $3.33$, near $b = 2.618$. So $b = 2$ is close to the best, and it is the usual choice.
- **Randomized starting point.** Choosing the first guess at random lowers the expected ratio. For the line search, a random start with growth factor about $3.59$ gives the optimal randomized ratio of about $4.59$ (Kao, Reif and Tate 1996).
- **Anytime algorithms in place of doubling.** Many algorithms can change their parameter smoothly, such as [online gradient descent](/online-gradient-descent/) with $\eta_t = D/(G\sqrt t)$, which has regret $\frac32 GD\sqrt T$ against $2 + \sqrt2$ times $GD\sqrt T$ with restarts. Smooth tuning keeps the learned state and often gives better constants.

## Pitfalls

- **Logarithmic bounds do not survive.** If $A(N)$ has regret $\alpha\ln N$, as for strongly convex losses, the phases cost $\sum_{m \le M}\alpha m\ln 2 = \Theta(\alpha\log^2 T)$. The trick turns $O(\log T)$ into $O(\log^2 T)$; use an anytime step size.
- **The bound must hold for every prefix.** If $A(N)$ is only good at the end of $N$ rounds, the last phase, cut short, can have a large regret. Hedge and online gradient descent with fixed tuned steps satisfy the prefix condition; some algorithms with a planned schedule do not.
- **Restarts throw away information.** Each phase starts from scratch. In practice a restart can make the algorithm much worse for a while after each doubling, even when the bound is fine.
- **High-probability bounds.** For randomized algorithms, the failure probability of each phase must be set so that the sum over all phases stays small, for example $\delta/(m + 1)^2$ in phase $m$.
- **Guessing the optimal cost needs a test.** The variation that guesses $\mathrm{OPT}$ works only if the algorithm can tell, online, that the guess is too small.

## Exercises

1. Show that phases of lengths $1, 2, 4, \ldots$ cover exactly $2^M - 1$ rounds before phase $M$, and use it to show that the last phase index satisfies $2^M \le T$.
2. Prove the factor $\frac{2^\gamma}{2^\gamma - 1}$ for a bound $\alpha N^\gamma$, and check that it is $2$ for $\gamma = 1$.
3. Show that for $T = 2^M$ the sum of the phase bounds divided by $\alpha\sqrt T$ tends to $2 + \sqrt2$, so the analysis cannot be improved.
4. Show that the doubling strategy for searching on a line, with turning points $(-2)^m$, walks at most $9d$ for a target at distance $d \ge 1$. Hint: the worst case is a target just past a turning point.
5. Apply the trick to a regret bound $\alpha\ln N$ and show that the result is $\Theta(\alpha\log^2 T)$.

## References
