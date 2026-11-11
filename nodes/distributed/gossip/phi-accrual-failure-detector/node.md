---
tag: TY0JW4
kind: algorithm
slug: phi-accrual-failure-detector
name: Phi accrual failure detector
aliases:
- accrual failure detector
- φ accrual failure detector
- phi accrual detector
area: distributed/gossip
level: advanced
summary: A failure detector that outputs a suspicion level phi = -log10 of the probability that the next heartbeat is still to come, from a window of past inter-arrival times.
solves: [failure-detection]
model: asynchronous-model
complexity:
  vars: {w: the window size}
  time: {worst: O(1)}
  space: {extra: O(w)}
properties: {deterministic: true, recursive: false}
prereqs: [failure-detection, failure-detector, variance]
see_also: [failure-detection, failure-detector, eventually-perfect-failure-detector, swim, membership-management, exponential-moving-average, variance, churn]
sources:
  - paper: doi:10.1109/RELDIS.2004.1353004
    title: Naohiro Hayashibara, Xavier Défago, Rami Yared and Takuya Katayama, The φ accrual failure detector, 23rd IEEE International Symposium on Reliable Distributed Systems (SRDS), 2004
    locator: pages 66 to 78 (accrual failure detectors, the definition phi = -log10 P_later(t_now - T_last) with a normal model over a sliding window, the threshold Phi and its mistake rate, and the evaluation on a wide-area heartbeat trace)
  - paper: doi:10.1109/TC.2002.1004315
    title: Wei Chen, Sam Toueg and Marcos K. Aguilera, On the quality of service of failure detectors, IEEE Transactions on Computers 51(5), 2002
    locator: the QoS metrics detection time, mistake recurrence time and mistake duration, used in the evaluation of the phi detector
  - paper: "Shannon R. Bowling, Mohammad T. Khasawneh, Sittichai Kaewkuekool and Byung Rae Cho, A logistic approximation to the cumulative normal distribution, Journal of Industrial Engineering and Management 2(1), 2009"
    locator: the approximation 1 / (1 + exp(-1.5976 y - 0.070566 y^3)) used by Akka
---

The phi accrual failure detector, from Hayashibara, Défago, Yared and Katayama (2004), is a heartbeat [failure detector](/failure-detector/) that outputs a number instead of a yes or no answer. From a sliding window of past heartbeat inter-arrival times it estimates the distribution of the next one, and at time $t_{now}$ it outputs $\varphi = -\log_{10} P_{later}(t_{now} - T_{last})$, where $P_{later}(x)$ is the probability that a heartbeat comes more than $x$ after the previous one. Each application compares $\varphi$ with its own threshold $\Phi$: if the model is right, a live process is wrongly suspected in a fraction $10^{-\Phi}$ of heartbeat intervals. Apache Cassandra and Akka use variants of it.

## In plain words

A friend sends you a message every minute. If one message is two seconds late, you do not worry. If it is ten minutes late, you start to think something is wrong.

This detector turns that feeling into a number. It remembers how late the messages usually are and how much the delay changes. When a message is overdue, it asks: how often does a message come this late when everything is fine? If this happens once in ten times, the number is 1. Once in a hundred, the number is 2. Once in a thousand, 3.

Each program that uses the detector picks its own limit. A program that must act fast uses a low limit and accepts some false alarms. A program that must not make mistakes uses a high limit and waits longer.

## The problem

A binary failure detector with a fixed timeout mixes two jobs: watching the network, and deciding how much risk to take. One timeout cannot suit both an application that needs fast reactions and one that cannot afford a wrong suspicion, and a fixed timeout does not follow changes in network delay. See [failure detection](/failure-detection/) for the quality of service metrics of Chen, Toueg and Aguilera: detection time, mistake recurrence time and mistake duration. An *accrual* failure detector outputs a suspicion level that grows without bound after a crash and stays bounded for a live process, and leaves the threshold to the application.

## The algorithm

The monitored process $q$ sends a heartbeat every $\Delta_i$ time units. The monitor $p$ keeps the last $w$ inter-arrival times in a window $W$ and the arrival time $T_{last}$ of the latest heartbeat. The paper models the inter-arrival time as normal with the mean $\mu$ and the variance $\sigma^2$ of the window.

```pseudo id=main
ON-HEARTBEAT(t)
L1  if there was an earlier heartbeat: append t − T_last to W, and remove the oldest value if |W| > w
L2  T_last ← t
L3  μ ← mean(W); σ ← standard deviation(W)
PHI(t_now)
L4  x ← t_now − T_last
L5  P_later ← 1 − F(x), where F is the normal CDF with mean μ and standard deviation σ
L6  return −log10(P_later)
SUSPECT(t_now, Φ)
L7  return PHI(t_now) ≥ Φ
```

Keeping running sums of the values and their squares makes each step $O(1)$. The output is not boolean, so different applications can read the same detector with different thresholds, and one application can take softer actions at a low $\varphi$ and harder ones at a high $\varphi$.

## Example

**The mistake rate.** Assume the inter-arrival times are independent with CDF $F$, and the detector knows $F$. After a heartbeat, $\varphi$ reaches $\Phi$ at the time $\tau_\Phi$ with $1 - F(\tau_\Phi) = 10^{-\Phi}$. A live process is wrongly suspected in an interval exactly when the next heartbeat comes after $\tau_\Phi$, which has probability $1 - F(\tau_\Phi) = 10^{-\Phi}$. For a normal model, $\tau_\Phi = \mu + z_\Phi \sigma$, with $z_1 = 1.28$, $z_2 = 2.33$, $z_3 = 3.09$ and $z_8 = 5.61$.

**Simulation.** With 100000 normal inter-arrival times of mean 100 and standard deviation 10, and a window of 1000, the fraction of intervals in which $\varphi$ reached $\Phi$ before the next heartbeat was:

| $\Phi$ | 1 | 2 | 3 | 4 |
|---|---|---|---|---|
| measured (200000 intervals) | 0.1002 | 0.00991 | 0.000985 | 0.00011 |
| $10^{-\Phi}$ | 0.1 | 0.01 | 0.001 | 0.0001 |

If the model is wrong, the guarantee is gone. With exponential inter-arrival times of mean 100, the normal model gives wrong suspicions in 0.037 of the intervals at $\Phi = 2$ and 0.017 at $\Phi = 3$, almost 4 and 17 times the nominal rates, because the exponential tail is much heavier than the normal one.

**After a crash.** No heartbeat comes, $x$ grows, and $\varphi$ grows without bound: for a normal model it grows like $(x - \mu)^2 / (2 \sigma^2 \ln 10)$. With $\mu = 100$ and $\sigma = 14$, $\Phi = 8$ is reached 80 time units after the expected arrival.

## Correctness

The proved claims are: $\varphi$ is a nondecreasing function of the time since the last heartbeat, equal to $\log_{10} 2$ at the mean for a normal model; after a crash, $\varphi$ tends to infinity, so every threshold is eventually crossed (accruement, which gives completeness); while heartbeats keep arriving at intervals bounded by some $B$, $\varphi$ stays bounded (upper bound); and if the inter-arrival times are independent with the CDF used by the detector, the probability that a given interval contains a wrong suspicion at threshold $\Phi$ is exactly $10^{-\Phi}$. The full proof is below.

With an estimated mean and variance the rate is only close to $10^{-\Phi}$, and with a wrong model it can be far off, as the example shows.

## Complexity

- **Per heartbeat.** $O(1)$ with running sums; $O(w)$ if the mean and variance are recomputed.
- **Per query.** $O(1)$: one evaluation of the normal tail.
- **Space.** $O(w)$ for the window. Both Cassandra and Akka use windows of up to 1000 intervals.

## Properties

- **Accrual.** The output is a level, so one detector serves many applications with different thresholds.
- **Adaptive.** The window follows changes of the network delay; a larger window is smoother but slower to adapt.
- **Calibrated under the model.** The threshold $\Phi$ has a direct meaning, a wrong suspicion rate of $10^{-\Phi}$ per interval, when the model fits.
- **Eventually perfect behaviour.** If, after some time, heartbeat delays are bounded, a threshold above the bound of $\varphi$ gives no more wrong suspicions, and every crash is detected, as an [eventually perfect failure detector](/eventually-perfect-failure-detector/) requires.

## Variants and improvements

- **Apache Cassandra.** Its gossip failure detector keeps up to 1000 inter-arrival times per endpoint and models them as exponential, so $P_{later}(x) = e^{-x / \mu}$ and $\varphi = x / (\mu \ln 10)$; the source code cites issue CASSANDRA-2597 for this change from the normal model. A node is convicted when $\varphi$ exceeds `phi_convict_threshold`, which `cassandra.yaml` documents with a default of 8, so a node is marked down after about $8 \ln 10 \approx 18.4$ mean intervals of silence.
- **Akka.** The Akka failure detector keeps the normal model but computes the tail with the logistic approximation $F(y) \approx 1 / (1 + e^{-1.5976 y - 0.070566 y^3})$, adds an acceptable heartbeat pause to the mean, and uses at least a minimum standard deviation. A node is available while $\varphi$ is below the threshold. With the reference settings of Akka Cluster (heartbeats every second, a threshold of 8, an acceptable pause of 3 s and a minimum standard deviation of 100 ms) and steady heartbeats, $\varphi$ reaches 8 about 4.5 s after the last heartbeat. The approximation is close for $|y| \le 2$ and gives larger values in the far tail: 7.30 instead of 6.54 at $y = 5$.
- **Other accrual detectors.** Satzger et al. (2007) used an empirical distribution of the window, and other designs use the exponential or a heavy-tailed model, to fit networks where the normal tail is too light.

## When to use it

Use the phi accrual detector when a process monitors a few others by heartbeats over links whose delay changes, and when several consumers need different trade-offs between detection time and mistakes. It is the standard choice in Cassandra and Akka clusters. For a large group in which every member must watch every other, combine it with a scalable scheme such as [SWIM](/swim/), which probes random members instead of watching all of them.

## Pitfalls

- **Heavy tails.** Garbage collection pauses and network bursts give inter-arrival times far heavier than normal. The nominal rate $10^{-\Phi}$ is then much too small, which is why Akka adds an acceptable pause and a minimum standard deviation.
- **Too little variance.** With very regular heartbeats, $\sigma$ is tiny and a small delay gives a huge $\varphi$. A floor on $\sigma$ avoids this.
- **Numerical tail.** Computing $1 - F(x)$ directly loses all precision beyond about 8 standard deviations; use the complementary error function or the logarithm of the tail.
- **Cold start.** With few samples the mean and variance are unreliable; implementations seed the window with an expected interval.
- **Indirect heartbeats.** When heartbeats travel by gossip, as in Cassandra, the inter-arrival times include the gossip delay, and their distribution is not the heartbeat schedule.

## Implementations

## History

Chen, Toueg and Aguilera (2002) defined quality of service metrics for failure detectors and an adaptive detector based on estimated arrival times. Hayashibara, Défago, Yared and Katayama introduced accrual failure detectors and the phi detector at SRDS 2004, and evaluated it on a heartbeat trace over a wide-area link between Japan and Switzerland against the detectors of Chen et al. and of Bertier et al. Défago and coauthors later gave the formal definition of accrual failure detectors and their relation to the classes of Chandra and Toueg. Cassandra adopted the phi detector for its gossip layer, and Akka for remoting and clustering.

## References
