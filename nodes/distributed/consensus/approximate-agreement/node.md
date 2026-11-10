---
tag: F7F5QK
kind: problem
slug: approximate-agreement
name: Approximate agreement problem
aliases:
- Approximate agreement
- Byzantine approximate agreement
- epsilon-agreement
area: distributed/consensus
level: advanced
summary: Processes with real inputs output values within ε of each other and inside the range of the correct inputs. Unlike consensus, it is solvable in the asynchronous model with faults.
prereqs: [consensus-problem, byzantine-failure-model, asynchronous-model]
see_also: [approximate-agreement-algorithm, consensus-problem, k-set-agreement, flp-impossibility, byzantine-fault-tolerance, clock-synchronization, byzantine-reliable-broadcast, synchronous-model]
sources:
  - paper: doi:10.1145/5925.5931
    title: Danny Dolev, Nancy A. Lynch, Shlomit S. Pinter, Eugene W. Stark and William E. Weihl, Reaching approximate agreement in the presence of faults, Journal of the ACM 33(3), 1986, pages 499 to 516
    locator: the definition of approximate agreement, the synchronous algorithm for n > 3t and the asynchronous algorithm for n > 5t
  - paper: doi:10.1007/BF01843568
    title: Michael J. Fischer, Nancy A. Lynch and Michael Merritt, Easy impossibility proofs for distributed consensus problems, Distributed Computing 1(1), 1986, pages 26 to 39
    locator: the impossibility of Byzantine approximate agreement with n ≤ 3t
  - paper: doi:10.1007/11516798_17
    title: Ittai Abraham, Yonatan Amit and Danny Dolev, Optimal resilience asynchronous approximate agreement, Proceedings of the 8th International Conference on Principles of Distributed Systems (OPODIS), LNCS 3544, 2004, pages 229 to 239
    locator: the asynchronous Byzantine algorithm for n > 3t
  - book: isbn:9781558603486
    title: Nancy A. Lynch, Distributed Algorithms, Morgan Kaufmann, 1996
    locator: Section 7.2 (approximate agreement)
---

The approximate agreement problem asks $n$ processes, each with a real input, to output real values that are within a given $\varepsilon > 0$ of each other and inside the range of the inputs of the correct processes. It relaxes the [consensus problem](/consensus-problem/): outputs need to be close, not equal. Dolev, Lynch, Pinter, Stark and Weihl (1986) introduced it and showed that, unlike consensus, it can be solved in the [asynchronous model](/asynchronous-model/) with faulty processes, even [Byzantine](/byzantine-failure-model/) ones. With Byzantine faults it needs $n > 3t$ processes; their asynchronous algorithm needs $n > 5t$, and Abraham, Amit and Dolev (2004) reached $n > 3t$.

## In plain words

Several clocks must show nearly the same time. They do not need to agree to the second, only to within, say, one second. Some clocks may be broken and even report false times on purpose.

The rule has two parts. The final times of the working clocks must be within one second of each other. And each final time must lie between the earliest and the latest time that a working clock started with, so that a broken clock cannot push everyone to a time that no working clock ever showed.

Exact agreement is impossible in some settings where this weaker goal is easy. Each round, everyone moves toward the middle, and the gap shrinks.

## Definition

There are $n$ processes, of which at most $t$ are faulty. Each correct process $p$ has an input $x_p \in \mathbb{R}$. A number $\varepsilon > 0$ is known to all. A protocol solves **approximate agreement** if, in every run, each correct process $p$ outputs a value $y_p$ such that:

- **Agreement.** $|y_p - y_q| \le \varepsilon$ for any two correct processes $p$ and $q$.
- **Validity.** $\min_{q} x_q \le y_p \le \max_{q} x_q$, where $q$ ranges over the correct processes.
- **Termination.** Every correct process outputs a value.

Validity is about correct inputs only. With Byzantine faults, a faulty process can claim any input, so a validity rule that used all inputs would allow any output.

## Variants

- **Failure model.** [Crash failures](/crash-failure/) or Byzantine failures.
- **Timing.** [Synchronous](/synchronous-model/) rounds or the asynchronous model.
- **Known or unknown range.** If a bound $\Delta$ on the spread of the inputs is known, the number of rounds can be fixed in advance. If not, the processes estimate it from the values they see first.
- **Multidimensional approximate agreement.** Inputs and outputs are vectors in $\mathbb{R}^d$, and validity asks for outputs inside the convex hull of the correct inputs. The number of processes needed grows with $d$.
- **Approximate agreement on graphs.** Outputs are vertices of a graph, and agreement asks for adjacent or equal vertices.

## Examples

**Agreement on a temperature.** Four sensors, one of them faulty, read $20.0$, $20.4$ and $21.0$ (the correct ones) and the faulty one claims $35$ to some and $-5$ to others, with $\varepsilon = 0.1$. Valid outputs lie in $[20.0, 21.0]$, and any two differ by at most $0.1$. For example, outputs $20.51$, $20.55$ and $20.6$ are correct; an output of $22$ breaks validity even if all agree on it.

**One round of the trimmed midpoint.** With $n = 4$, $t = 1$ and correct values 0, 4 and 8, the [approximate agreement algorithm](/approximate-agreement-algorithm/) produces 2, 2 and 6 after one round: the spread goes from 8 to 4, whatever the faulty process sends.

**Non-example.** Each process outputs the mean of all values it receives. One faulty value $10^9$ moves the mean far outside the correct range, which breaks validity.

## Known algorithms

- **Trimmed midpoint, synchronous, $n > 3t$.** Each round, drop the $t$ smallest and $t$ largest received values and take the midpoint of the rest. The spread halves each round. See [approximate agreement algorithm](/approximate-agreement-algorithm/), with a full proof.
- **DLPSW synchronous algorithm, $n > 3t$.** Drop $t$ values at each end, take every $t$-th of the remaining values and average them. It converges faster than the midpoint when $n$ is large compared to $t$.
- **DLPSW asynchronous algorithm, $n > 5t$.** Each round, wait for $n - t$ values, drop $2t$ at each end, then select and average.
- **Abraham, Amit and Dolev, asynchronous, $n > 3t$.** Uses [reliable broadcast](/byzantine-reliable-broadcast/) and a witness step, so that any two correct processes base their round on many common values.
- **Crash failures, asynchronous, $n > 2t$.** Each round, wait for $n - t$ values and take the midpoint of their range. Any two sets of $n - t$ senders share a process, since $2(n - t) > n$, so the two ranges share a value and the midpoints differ by at most half the old spread.

## Bounds

- **Solvable in the asynchronous model.** The [FLP impossibility](/flp-impossibility/) result does not apply. Its proof needs a decision that flips between two discrete values, while here outputs can move by small steps and validity allows any value in a range.
- **Byzantine faults need $n > 3t$.** Fischer, Lynch and Merritt (1986) proved that no algorithm solves Byzantine approximate agreement with $n \le 3t$, in any timing model, by the same kind of argument as for Byzantine consensus. The tests of the [algorithm page](/approximate-agreement-algorithm/) show a run with $n = 3$, $t = 1$ in which the trimmed midpoint never converges.
- **Crash faults in the asynchronous model need $n > 2t$.** With $n \le 2t$, split the processes into two groups of at most $t$. Each group must output without hearing from the other, since the other could have crashed, so each group outputs inside the range of its own inputs, and these ranges can be far apart.
- **Asynchronous Byzantine faults.** The original algorithm of 1986 needs $n > 5t$, and the 2004 algorithm of Abraham, Amit and Dolev needs only $n > 3t$, which is optimal.
- **Rounds.** With the trimmed midpoint, $\lceil \log_2(\Delta/\varepsilon) \rceil$ rounds are enough. The number of rounds always grows with $\log(\Delta/\varepsilon)$, since a round can shrink the spread only by a bounded factor that depends on $n$ and $t$.

## Reductions

- **Consensus solves it.** A consensus protocol whose decision is the input of a correct process gives outputs that are equal (so within any $\varepsilon$) and valid. With Byzantine faults, this needs the strong form of validity.
- **It does not solve consensus.** Approximate agreement is solvable in the asynchronous model and consensus is not, so no reduction in that direction exists. In particular, rounding the outputs of approximate agreement on inputs 0 and 1 does not give binary consensus: two outputs near $1/2$ can round differently.
- **Relation to set agreement.** [k-set agreement](/k-set-agreement/) relaxes consensus by allowing a few distinct values; approximate agreement relaxes it by allowing close values. Both are standard examples of tasks between trivial and consensus.

## Applications

- **Clock synchronization.** Fault-tolerant clock synchronization algorithms collect clock readings, drop the extreme ones and average the rest, which is one round of approximate agreement per resynchronization. See [clock synchronization](/clock-synchronization/).
- **Sensor fusion.** Redundant sensors in a control system agree on a reading that a few faulty sensors cannot move outside the range of the good ones.
- **Robots and drones.** Mobile agents converge to nearby positions or headings by repeated approximate agreement.
- **Robust aggregation.** Training with many workers can combine updates by trimmed means, so that a few faulty workers cannot pull the result outside the range of the correct ones.

## References
