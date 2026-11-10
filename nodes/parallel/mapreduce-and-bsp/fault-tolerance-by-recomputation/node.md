---
tag: M9PXF3
kind: concept
slug: fault-tolerance-by-recomputation
name: Fault tolerance by re-execution
aliases:
- task re-execution
- lineage-based recovery
area: parallel/mapreduce-and-bsp
level: core
summary: Recover from the failure of a machine by running again only the tasks whose results were lost. It needs deterministic tasks without side effects and inputs that survive the failure.
prereqs: [mapreduce-model, crash-failure]
see_also: [speculative-execution, resilient-distributed-datasets, checkpointing, crash-recovery, pregel-model, word-count]
sources:
  - paper: "Jeffrey Dean and Sanjay Ghemawat, MapReduce: simplified data processing on large clusters, OSDI 2004"
    locator: Section 3.3 (worker failure, master failure and the semantics in the presence of failures), Section 4 (skipping bad records) and Section 5.5 (the sort with 200 workers killed)
  - paper: doi:10.1145/1327452.1327492
    title: "Jeffrey Dean and Sanjay Ghemawat, MapReduce: simplified data processing on large clusters, Communications of the ACM 51(1), 2008"
    locator: the journal version, with the same fault tolerance design
  - paper: "Matei Zaharia, Mosharaf Chowdhury, Tathagata Das, Ankur Dave, Justin Ma, Murphy McCauley, Michael J. Franklin, Scott Shenker and Ion Stoica, Resilient distributed datasets: a fault-tolerant abstraction for in-memory cluster computing, NSDI 2012"
    locator: Section 2.1 (lineage) and Section 5.4 (checkpointing), recovery by recomputation for general dataflow
---

Fault tolerance by re-execution is the way [MapReduce](/mapreduce-model/) and its successors survive the failure of machines. The master does not save the state of the computation. When a worker fails, the master sets every task whose result was on that worker back to idle and runs it again on another worker. This is correct because each task is a deterministic function of input that is stored safely elsewhere, so a second run gives the same result as the first, and it is cheap because only the lost tasks run again.

## In plain words

Imagine a kitchen that cooks a large dinner from written recipes, with all ingredients kept in a safe store room. If a cook gets sick and leaves, the head chef does not try to rescue the half-made dish on that cook's table. The chef gives the same recipe to another cook, who takes fresh ingredients from the store room and makes the dish again. Dishes that are already on the serving table are safe and do not need to be made again. This works because a recipe gives the same dish each time, and because cooking it twice does no harm. It would fail if a recipe said "add whatever is left in the fridge", or if cooking a dish also sent a bill to a guest.

## The idea

**What the master does (Dean and Ghemawat, Section 3.3).** The master pings each worker from time to time. A worker that does not answer for some time is marked failed, and the master then sets back to idle:

- every map or reduce task that was in progress on that worker;
- every completed map task of that worker, because a map task writes its output to the local disk of its worker, which is now out of reach.

Completed reduce tasks are not run again, because their output is in the global file system, which keeps copies on several machines. When a map task runs again on a new worker, the master tells all reduce tasks, and any reduce task that has not yet read the data of that map task reads it from the new worker.

**Why the output is right.** Assume that the map and reduce functions are deterministic and that a task affects nothing outside its own output. Then:

1. Every run of map task $i$ produces the same $R$ partitions, since it reads the same split of the input, which the failure did not touch.
2. A reduce task reads one copy of each map output, so its input is the same whichever runs of the map tasks it read from, and its output is the same.
3. Each task commits its output once. A map worker reports its $R$ temporary files to the master when it finishes, and the master ignores a second report for a map task that is already complete. A reduce worker writes to a temporary file and renames it to the final name; the rename is atomic, so if two runs of one reduce task finish, the final file holds the output of exactly one run.

So the output of the job is the same as the output of a run without failures. Dean and Ghemawat state this as: with deterministic operators, the distributed run gives the same output as a non-faulting sequential execution of the program.

If an operator is not deterministic, the guarantee is weaker. Each reduce output equals the output of some sequential execution, but two reduce tasks may have read the outputs of two different runs of the same map task, which differ. So the outputs of reduce tasks $1$ and $2$ may come from different sequential executions.

**What it needs.**

- Durable inputs. The input splits are in a replicated file system, so a lost task can read them again.
- Deterministic tasks without side effects, or side effects that are atomic and idempotent.
- A record of which task produced which data, so that the master knows what to run again. In MapReduce the record is fixed: maps feed reduces. A general dataflow keeps a lineage graph, which is the basis of [resilient distributed datasets](/resilient-distributed-datasets/).
- A reliable master. In the original design a failure of the single master stops the job, and the client runs the job again; the master could also write checkpoints of its own small state.

**Recomputation against checkpoints.** The other classic method is [checkpointing](/checkpointing/): every process saves its state from time to time, and after a failure all processes roll back to the last checkpoint, as in MPI programs and in [Pregel](/pregel-model/). A checkpoint costs time and storage even when nothing fails, and a failure makes all processes redo the work since the last checkpoint. Re-execution costs nothing when nothing fails, and a failure makes only the lost tasks run again, often in parallel on many workers. Its cost grows with the length of the chain of tasks that must be run again to rebuild the lost data. For long chains, such as many iterations of an algorithm, systems combine the two: they recompute short chains and checkpoint the data at the end of a long one.

## Examples

**A small timeline.** Three workers $A$, $B$, $C$ run six map tasks $m_0, \ldots, m_5$ and two reduce tasks $r_0, r_1$; each task takes one step, and the reduce tasks start when all maps are done.

| step | without failure | $A$ fails at the start of step 3 |
|---|---|---|
| 1 | $A{:}m_0$, $B{:}m_1$, $C{:}m_2$ | $A{:}m_0$, $B{:}m_1$, $C{:}m_2$ |
| 2 | $A{:}m_3$, $B{:}m_4$, $C{:}m_5$ | $A{:}m_3$, $B{:}m_4$, $C{:}m_5$ |
| 3 | $A{:}r_0$, $B{:}r_1$ (done) | $B{:}m_0$, $C{:}m_3$ (outputs on $A$ are lost) |
| 4 | | $B{:}r_0$, $C{:}r_1$ (done) |

The failure costs two extra map runs and one step. If $A$ fails at the start of step 4 instead, after it committed $r_0$, nothing runs again: the output of $r_0$ is in the global file system, and the job is done.

The simulator of this page runs a master like this in discrete steps for word count, with task times of one to three steps and seeded failures of workers at random steps. On 200 seeded jobs it checks that the output always equals the word count of the input, that every completed reduce task ran once, and that the number of map runs equals the number of map tasks plus the number of lost map outputs, less the map tasks whose output was lost after every reduce task had read it (the job can end without running those again).

**Measured cost.** In the sort benchmark of the MapReduce paper, about 1 TB on about 1800 machines, the authors killed 200 of the 1746 worker processes several minutes into the run. The scheduler restarted the lost tasks at once, and the sort finished in $933$ seconds, against $891$ seconds without failures: an increase of $5\%$. The paper also tells of network maintenance that made groups of $80$ machines unreachable for several minutes at a time; the master ran their work again and the job went on.

**A non-example: a task with a side effect.** A map function that, besides emitting pairs, appends a line to a shared log or sends a message to another service, runs these effects again on each re-execution and on each [backup copy](/speculative-execution/). After one failure, the log has duplicate lines, although the output of the job is still right. Such effects must be made idempotent, for example by writing them under the task number and keeping one copy per task.

**A non-example: a deterministic crash.** If a map function crashes on one bad record, every re-execution crashes again on the same record, and the job never ends. MapReduce has an optional mode in which a worker reports the number of the record that caused a crash, and after more than one crash on the same record the master tells the next run to skip it.

## Where it is used

- MapReduce and Hadoop, for map and reduce tasks, with the input and the final output in a replicated file system and the intermediate data on local disks.
- Dataflow systems such as Dryad and Spark, which run again the lost vertices of a job graph. Spark keeps the lineage of each [resilient distributed dataset](/resilient-distributed-datasets/) and rebuilds lost partitions from their parents.
- Together with [speculative execution](/speculative-execution/), which uses the same property, that a task can run twice, to deal with slow machines instead of failed ones.
- As the model behind the failure assumption of these systems: workers fail by [crashing](/crash-failure/), not by giving wrong answers, and a crashed worker does not come back with old state. Recovery of a single process with its state is the topic of [crash recovery](/crash-recovery/).

## References
