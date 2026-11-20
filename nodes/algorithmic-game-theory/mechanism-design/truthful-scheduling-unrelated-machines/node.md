---
tag: CMVE8S
kind: problem
slug: truthful-scheduling-unrelated-machines
name: Truthful scheduling on unrelated machines
aliases:
- Nisan-Ronen scheduling problem
area: algorithmic-game-theory/mechanism-design
level: advanced
summary: "Assign jobs to selfish machines that privately know their processing times, with payments that make truth telling dominant, to minimize the makespan. VCG has ratio n."
prereqs: [unrelated-machine-scheduling, vcg-mechanism, cycle-monotonicity]
see_also: [nisan-ronen-conjecture, lenstra-shmoys-tardos, unrelated-makespan-inapproximability, uniform-machine-scheduling, truthful-in-expectation, monotone-allocation-rule, load-balancing-game, makespan]
sources:
  - paper: doi:10.1006/game.1999.0790
    title: "Noam Nisan and Amir Ronen, Algorithmic mechanism design, Games and Economic Behavior 35(1-2) (2001), 166-196 (conference version in STOC 1999)"
    locator: the scheduling problem for unrelated machines, the VCG upper bound n, the lower bound 2 for deterministic truthful mechanisms, and the randomized mechanism for two machines
  - paper: doi:10.1145/3564246.3585176
    title: "George Christodoulou, Elias Koutsoupias and Annamaria Kovacs, A proof of the Nisan-Ronen conjecture, Proceedings of the 55th ACM Symposium on Theory of Computing (STOC 2023), 672-685"
    locator: the lower bound n for deterministic truthful mechanisms
  - paper: "Ahuva Mu'alem and Michael Schapira, Setting lower bounds on truthfulness, Games and Economic Behavior 110 (2018), 174-193"
    locator: the short weak-monotonicity proof of the lower bound 2 and the lower bound for randomized mechanisms
  - paper: "Aaron Archer and Eva Tardos, Truthful mechanisms for one-parameter agents, Proceedings of the 42nd IEEE Symposium on Foundations of Computer Science (FOCS 2001), 482-491"
    locator: related machines as a one-parameter problem, the monotone optimal algorithm and the randomized 3-approximation
  - paper: "George Christodoulou and Annamaria Kovacs, A deterministic truthful PTAS for scheduling related machines, SIAM Journal on Computing 42(4) (2013), 1572-1595"
    locator: the deterministic truthful PTAS for related machines
  - paper: "Itai Ashlagi, Shahar Dobzinski and Ron Lavi, Optimal lower bounds for anonymous scheduling mechanisms, Mathematics of Operations Research 37(2) (2012), 244-258"
    locator: the lower bound n for anonymous truthful mechanisms
  - paper: "George Christodoulou, Elias Koutsoupias and Annamaria Kovacs, Mechanism design for fractional scheduling on unrelated machines, ACM Transactions on Algorithms 6 (2010), Article 2"
    locator: fractional truthful mechanisms and their bounds
---

In truthful scheduling on unrelated machines, each machine is a selfish agent that privately knows how long it needs for each job, and the mechanism must assign the jobs and pay the machines so that reporting the true times is a dominant strategy, while keeping the [makespan](/makespan/) small. The problem was posed by Nisan and Ronen (1999) and started algorithmic mechanism design. This page is about the problem, its variants and all the known bounds. Its close page, the [Nisan-Ronen theorem](/nisan-ronen-conjecture/), is about one result: no deterministic truthful mechanism has approximation ratio below $n$, which shows that the simple VCG mechanism is optimal.

## In plain words

A company has some jobs and some computers owned by different people. Each owner knows how long its computer needs for each job, and nobody else knows. The company asks the owners for these times, chooses which computer runs which job, and pays the owners. Each owner wants to be paid as much as possible for as little work as possible. The company wants all jobs done as early as possible. The question is how close to the best finishing time the company can get, if its rule must make honest answers the best plan for every owner. The answer for rules without chance is surprising: the simplest rule, which gives each job to the fastest computer, is the best possible, even though it can be many times slower than the best plan.

## Definition

There are $n$ machines and $m$ jobs. Machine $i$ needs time $t_{ij} \ge 0$ for job $j$, and the vector $t_i = (t_{i1}, \dots, t_{im})$ is its private type. A mechanism asks each machine for a vector $b_i \in \mathbb{R}_{\ge 0}^m$ and returns

- an allocation $A_1, \dots, A_n$, a partition of the jobs among the machines, and
- payments $q_1, \dots, q_n$ to the machines.

Machine $i$ has utility $q_i - \sum_{j \in A_i} t_{ij}$, the payment minus its work. This is a cost setting. In the convention of this area the payment *by* agent $i$ is $p_i = -q_i$, and the valuation of machine $i$ for an allocation is $-\sum_{j \in A_i} t_{ij}$. The mechanism is truthful if reporting $b_i = t_i$ maximizes the utility of machine $i$ for every report of the others, which is [DSIC](/dominant-strategy-incentive-compatibility/).

The objective is the makespan of the true times,
$$\mathrm{MS}(A, t) = \max_{i} \sum_{j \in A_i} t_{ij},$$
and a mechanism has approximation ratio $\rho$ if $\mathrm{MS}(A(t), t) \le \rho \cdot \mathrm{OPT}(t)$ for every $t$. The question is the smallest $\rho$ that a truthful mechanism can reach, with no limit on running time. Without the incentive constraint this is the [unrelated machine scheduling](/unrelated-machine-scheduling/) problem.

The tool for lower bounds is weak monotonicity, the 2-cycle case of [cycle monotonicity](/cycle-monotonicity/), in cost form. Fix the reports of the other machines. If machine $i$ with type $t_i$ gets the set $A$ and with type $t_i'$ gets the set $A'$, then
$$\sum_{j \in A} (t_{ij}' - t_{ij}) \;\ge\; \sum_{j \in A'} (t_{ij}' - t_{ij}).$$
In words: measured by the change of times, the new set $A'$ must be at least as favorable to the new report as the old set $A$. A machine that lowers some of its times cannot end up with a set on which its times went up, compared with the old set.

## Variants

- **Deterministic or randomized.** Deterministic mechanisms must be DSIC. Randomized ones are usually required to be [truthful in expectation](/truthful-in-expectation/) or universally truthful. *Fractional* mechanisms may split a job among machines.
- **Related machines.** Machine $i$ has one private speed, and $t_{ij} = w_j / s_i$ for public job sizes $w_j$. This is a [single-parameter environment](/single-parameter-environment/) in cost form, and the incentive condition is a [monotone allocation rule](/monotone-allocation-rule/): a machine that reports itself slower must not get more work. See [uniform machine scheduling](/uniform-machine-scheduling/).
- **Restricted value sets.** Lavi and Swamy (2007 conference, 2009 journal) studied the case where each job has only two possible times, low or high, and gave a deterministic truthful 2-approximation by checking cycle monotonicity.
- **Anonymous mechanisms.** If the mechanism treats machines symmetrically, the ratio is at least $n$ (Ashlagi, Dobzinski and Lavi 2012).
- **Other objectives.** For the total work, the sum of the loads, VCG is optimal and truthful. The difficulty comes from the min-max objective.

## Examples

**VCG.** Give each job to the machine with the smallest reported time, with a fixed tie-breaking order, and pay that machine the second smallest reported time for the job. Each job is a separate [Vickrey auction](/vickrey-auction/) in cost form, so the mechanism is truthful.

A small instance where VCG is bad. Take $n$ machines and $n$ jobs. Machine 1 needs time 1 for every job, and every other machine needs time $1 + \varepsilon$ for every job. VCG gives all $n$ jobs to machine 1, with makespan $n$. Giving one job to each machine has makespan $1 + \varepsilon$. The ratio tends to $n$ as $\varepsilon \to 0$.

**The lower bound 2, by hand.** Take two machines and three jobs, with
$$t_1 = (1, 100, 1), \qquad t_2 = (100, 1, 1).$$
The optimal makespan is 2. Suppose a truthful mechanism has ratio at most $2 - \delta$ for some $\delta > 0$. On this instance its makespan is below 4, so job 1 goes to machine 1 and job 2 to machine 2. By symmetry assume job 3 goes to machine 2, so machine 1 gets $A = \{1\}$. Now let machine 1 report
$$t_1' = (0, 100, 1 + \varepsilon),$$
with $\varepsilon > 0$ so small that $2 / (1 + \varepsilon) > 2 - \delta$. The optimum is now $1 + \varepsilon$: machine 1 takes jobs 1 and 3. Any allocation that gives job 3 to machine 2 has makespan at least 2, which is too much, so machine 1 gets $A' = \{1, 3\}$. The change of times is $t_1' - t_1 = (-1, 0, \varepsilon)$. Its sum over $A = \{1\}$ is $-1$, and its sum over $A' = \{1, 3\}$ is $-1 + \varepsilon$. Weak monotonicity requires $-1 \ge -1 + \varepsilon$, which is false. So no truthful mechanism has ratio below 2. For $n > 2$ machines, add machines with time 1000 for every job. A mechanism with ratio below 2 never uses them, and the argument is unchanged. This short proof is due to Mu'alem and Schapira; Nisan and Ronen proved the same bound.

## Known algorithms

- **VCG**, ratio $n$, polynomial time, deterministic and truthful. Its makespan is at most $\sum_j \min_i t_{ij}$, and every schedule has makespan at least $\frac{1}{n} \sum_j \min_i t_{ij}$, so the ratio is at most $n$.
- **Randomized mechanisms for two machines.** Nisan and Ronen gave a universally truthful randomized mechanism for two machines with ratio $7/4$.
- **Fractional mechanisms.** Christodoulou, Koutsoupias and Kovacs (2010) studied mechanisms that split jobs. The best known upper bound for fractional and for randomized mechanisms is $(n + 1)/2$, as stated in their 2023 overview.
- **Related machines.** Archer and Tardos (2001) showed that an optimal allocation, with a fixed tie-breaking order, is monotone, so it can be made truthful in exponential time, and gave a randomized 3-approximation that is truthful in expectation. Christodoulou and Kovacs (2013) gave a deterministic truthful PTAS.
- **Without incentives**, the [Lenstra-Shmoys-Tardos algorithm](/lenstra-shmoys-tardos/) is a 2-approximation, and no polynomial algorithm beats $3/2$ unless P = NP ([inapproximability](/unrelated-makespan-inapproximability/)). The truthfulness bounds below hold even without limits on running time, so they come from incentives, not from computation.

## Bounds

For deterministic truthful mechanisms on $n$ unrelated machines, the upper bound is $n$ (VCG). The lower bounds:

| Paper | Lower bound | Authors |
| --- | --- | --- |
| STOC 1999, GEB 2001 | 2 | Nisan and Ronen |
| Algorithmica 2009 | $1 + \sqrt{2} \approx 2.414$ for $n \ge 3$ | Christodoulou, Koutsoupias and Vidali |
| Algorithmica 2012 | $1 + \varphi \approx 2.618$ as $n \to \infty$ | Koutsoupias and Vidali |
| Algorithmica 2021 | $\approx 2.755$ | Giannakopoulos, Hammerl and Pocas |
| arXiv 2020 | 3 | Dobzinski and Shaulker |
| FOCS 2021 | $1 + \sqrt{n - 1}$ | Christodoulou, Koutsoupias and Kovacs |
| STOC 2023 | $n$ | Christodoulou, Koutsoupias and Kovacs |

So the optimal ratio for deterministic truthful mechanisms is exactly $n$. For anonymous mechanisms the bound $n$ was known earlier (Ashlagi, Dobzinski and Lavi 2012).

For randomized and fractional mechanisms, the best known lower bound is about 2, from Mu'alem and Schapira and from Christodoulou, Koutsoupias and Kovacs (2010), and the best known upper bound is $(n + 1)/2$. Closing this gap is open.

## Reductions

- **From multi-parameter to single-parameter.** Related machines are the special case where each type is one number times a public vector, and there the problem becomes as easy as without incentives, up to the PTAS. The hardness of the unrelated case comes from the vector types.
- **Lower bounds through weak monotonicity.** All the lower bounds above use only weak monotonicity on small instances embedded in larger ones. Since every truthful mechanism satisfies it, the bounds hold for all truthful mechanisms, whatever their running time.
- **VCG is an affine maximizer.** VCG maximizes minus the total work, a weighted sum. The min-max objective is not affine. The scheduling domain is not unrestricted, so [Roberts' theorem](/roberts-theorem/) does not apply directly, and the bound $n$ needed a new proof.

## Applications

- **Outsourcing computation.** Jobs are sent to computers owned by others, such as in grid or cloud computing, where the owners know their own speeds.
- **Routing and networks.** Nisan and Ronen used the problem, with shortest paths, as the first examples of mechanism design for algorithmic problems.
- **Selfish load balancing.** The [load balancing game](/load-balancing-game/) studies the same machines when jobs are the selfish agents and there are no payments, a different model.

## References
