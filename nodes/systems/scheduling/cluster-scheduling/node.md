---
tag: F55AYR
kind: problem
slug: cluster-scheduling
name: Cluster scheduling
aliases:
- datacenter scheduling
- job placement
area: systems/scheduling
level: advanced
summary: Decide which jobs of many users run on which machines of a shared cluster, and when, so that each machine's CPU, memory and other resources suffice and the cluster is used well and fairly.
prereqs: [cpu-scheduling, bin-packing]
see_also: [dominant-resource-fairness, backfilling, gang-scheduling, list-scheduling, makespan, strip-packing, max-min-fairness, utilization]
sources:
  - paper: "Abhishek Verma, Luis Pedrosa, Madhukar Korupolu, David Oppenheimer, Eric Tune and John Wilkes, Large-scale cluster management at Google with Borg, Proceedings of the Tenth European Conference on Computer Systems (EuroSys), 2015"
    title: "Large-scale cluster management at Google with Borg"
    locator: Section 3.2 (feasibility checking and scoring of machines) and Section 5 (utilization, priorities and preemption)
  - paper: "Benjamin Hindman, Andy Konwinski, Matei Zaharia, Ali Ghodsi, Anthony D. Joseph, Randy Katz, Scott Shenker and Ion Stoica, Mesos: A Platform for Fine-Grained Resource Sharing in the Data Center, Proceedings of the 8th USENIX Symposium on Networked Systems Design and Implementation (NSDI), 2011"
    title: "Mesos: A Platform for Fine-Grained Resource Sharing in the Data Center"
    locator: Section 3 (resource offers, two-level scheduling, and the allocation module with fair sharing)
  - paper: "Malte Schwarzkopf, Andy Konwinski, Michael Abd-El-Malek and John Wilkes, Omega: flexible, scalable schedulers for large compute clusters, Proceedings of the 8th European Conference on Computer Systems (EuroSys), 2013"
    title: "Omega: flexible, scalable schedulers for large compute clusters"
    locator: Section 3 (the taxonomy of monolithic, two-level and shared-state schedulers) and Section 4 (optimistic concurrency on shared cluster state)
  - paper: "Ali Ghodsi, Matei Zaharia, Benjamin Hindman, Andy Konwinski, Scott Shenker and Ion Stoica, Dominant Resource Fairness: Fair Allocation of Multiple Resource Types, NSDI 2011"
    title: "Dominant Resource Fairness: Fair Allocation of Multiple Resource Types"
    locator: pages 323 to 336 (fair sharing of several resource types in a cluster)
---

Cluster scheduling is the problem of running the jobs of many users on a shared cluster of machines. Each machine has a capacity of several resources, such as CPU cores, memory, disk and accelerators. Each job consists of tasks, and each task needs a fixed amount of each resource for as long as it runs. The scheduler decides which tasks run, on which machines, and when, so that no machine is used beyond its capacity. It also aims for several goals at once: high [utilization](/utilization/), short waits for batch jobs, low latency and few failures for long-running services, and a fair share for each user. Even the simplest version, placing tasks with one resource on identical machines, contains [bin packing](/bin-packing/), so the problem is NP-hard. Real systems such as Borg at Google, Mesos and Omega use fast heuristics, priorities and fairness rules instead of exact optimization.

## In plain words

A company has thousands of computers and many teams that want to run programs on them. Each program says how many processor cores and how much memory it needs. A scheduler must choose a computer for each program, with enough free cores and enough free memory.

This is like packing boxes of different shapes into trucks. A box may fit by weight but not by size. Some programs must run all at once or not at all, some are more important than others, and some teams must not take more than their fair part.

The scheduler must decide fast, because new programs arrive all the time and computers fail.

## Definition

**Machines.** There are $m$ machines. Machine $k$ has a capacity vector $C_k \in \mathbb{R}_{\ge 0}^{d}$ for $d$ resource types.

**Jobs.** Jobs arrive over time. Job $j$ has a release time $r_j$, a number of tasks, a demand vector $D_j \in \mathbb{R}_{\ge 0}^{d}$ per task, a priority, an owner, and a set of machines on which its tasks may run (from constraints such as the type of hardware or the operating system). A task may have a known duration (a batch task) or run until it is stopped (a service).

**Schedule.** A schedule assigns each task that runs to a machine and a time interval. It is feasible if, at every time and on every machine $k$, the sum of the demand vectors of the tasks that run there is at most $C_k$ in every coordinate, and every task runs on an allowed machine after its release.

**Goals.** Common goals, often combined with weights, are:

- the number of tasks placed, or the utilization of each resource;
- the mean or weighted completion time of batch jobs, or their [makespan](/makespan/);
- the share of each user, under a fairness rule such as [dominant resource fairness](/dominant-resource-fairness/);
- few evictions of running tasks, and spreading the tasks of one service across failure domains.

The scheduler learns jobs online, often does not know their true run times, and must decide in milliseconds to seconds.

## Variants

- **One machine of many processors.** If $m = 1$, there is one resource (processors), and each job needs a number of processors for a time, this is the batch queue of a supercomputer. [Backfilling](/backfilling/) is the standard policy, and the offline problem is [strip packing](/strip-packing/).
- **All tasks at once.** Some jobs, such as parallel programs and machine learning training, need all their tasks to start together. This is [gang scheduling](/gang-scheduling/), and placement must reserve resources for the whole gang.
- **Fair sharing.** When the demand is higher than the cluster, the scheduler must divide the resources between users. With several resource types, [dominant resource fairness](/dominant-resource-fairness/) extends [max-min fairness](/max-min-fairness/).
- **Priorities and preemption.** A task of high priority may evict tasks of low priority to get room. Borg runs production services at high priority and batch work in the room that is left.
- **Data locality.** A task that reads data runs faster on a machine that stores the data. Schedulers may wait a short time for a local machine before they use a remote one.
- **Heterogeneous machines.** Machines differ in speed, accelerators and network position, so the value of a placement depends on the machine.
- **Architecture.** A *monolithic* scheduler places every task. A *two-level* scheduler, as in Mesos, offers free resources to the schedulers of frameworks, which accept or decline them. A *shared-state* scheduler, as in Omega, lets several schedulers work in parallel on a shared view of the cluster and resolves conflicts with optimistic concurrency.

## Examples

**Packing by more than one resource.** Two machines each have $\langle 4\ \text{cores}, 8\ \text{GB} \rangle$. Four tasks arrive: A and B need $\langle 2, 6 \rangle$ each, and C and D need $\langle 2, 1 \rangle$ each. A scheduler that looks only at cores sees four tasks of 2 cores and may put A and B on machine 1. That needs 12 GB, more than the 8 GB of the machine. A feasible placement puts A and C on machine 1 and B and D on machine 2, each machine with $\langle 4, 7 \rangle$ in use. A first fit in the order A, B, C, D finds this: B does not fit beside A, so it goes to machine 2, and C and D fill the rest.

**Stranded resources.** A machine with $\langle 4, 8 \rangle$ runs a task of $\langle 4, 2 \rangle$. Its other 6 GB are free but useless, because no task can run without a core. A good placement puts tasks with high memory and low CPU next to tasks with the opposite needs.

**Fair shares.** A cluster of 9 cores and 18 GB is shared by a user with tasks of $\langle 1, 4 \rangle$ and a user with tasks of $\langle 3, 1 \rangle$. Dominant resource fairness gives the first user 3 tasks and the second 2 tasks, so each holds $2/3$ of its main resource.

## Known algorithms

- **Greedy placement with scoring.** For each task, find the machines on which it fits (a feasibility check), give each a score, and take the best. Borg scores machines by a mix of packing tightly (best fit, which keeps whole machines free for large tasks) and spreading (worst fit, which leaves room for growth and limits the loss when one machine fails). This is a form of [list scheduling](/list-scheduling/).
- **Vector bin packing heuristics.** First fit, best fit and rules that score a machine by the dot product of its free vector and the demand vector, to place tasks where they use the free resources in a balanced way.
- **[Dominant resource fairness](/dominant-resource-fairness/)** chooses which user gets the next resources, and is used in Mesos and in the fair scheduler of Hadoop YARN.
- **[Backfilling](/backfilling/)** for batch queues of rigid parallel jobs, with reservations that prevent starvation.
- **[Gang scheduling](/gang-scheduling/)** for jobs whose tasks must run together.
- **Min-cost flow.** Model tasks, machines and the costs of placements (such as data locality and waiting) as a flow network, and solve it again as the cluster changes. Quincy, for example, works this way.

## Bounds

- **NP-hard.** Deciding whether a set of tasks with one resource fits on $m$ identical machines is [bin packing](/bin-packing/), which is strongly NP-hard. So exact optimization is out of reach for large clusters, and online schedulers do not know the future anyway.
- **Several resources make packing harder.** For $d \ge 2$ resources the problem is vector bin packing, which has no asymptotic approximation scheme unless P = NP, and simple greedy rules lose a factor that grows with $d$.
- **Makespan.** For tasks that each need one machine, greedy [list scheduling](/list-scheduling/) gets within a factor $2 - 1/m$ of the optimal [makespan](/makespan/).
- **Fairness.** With several resources, no allocation rule can have every desired fairness property at once; the properties that [dominant resource fairness](/dominant-resource-fairness/) keeps and loses are proved on its page.

## Reductions

- **From bin packing.** Take one resource, give every task an infinite duration, and ask whether all tasks can be placed. This is bin packing, so cluster scheduling is at least as hard.
- **From makespan scheduling.** Take one resource, machines of capacity 1 and tasks of demand 1 with given durations. Then each machine runs one task at a time, and minimizing the last completion time is makespan minimization on identical machines.
- **From strip packing.** One machine with $P$ processors and rigid jobs with durations gives [strip packing](/strip-packing/), if the processors that a job uses must be contiguous; without that rule it is the scheduling of rigid parallel jobs.

## Applications

Cluster schedulers run the data centers of large internet companies (Borg at Google, and Kubernetes, which grew out of that work), shared analytics clusters (Hadoop YARN and Mesos for Spark and MapReduce), supercomputers (batch systems such as Slurm), and clusters of GPUs for machine learning. They decide how much hardware a company needs, since better packing and sharing serve the same work with fewer machines.

## References
