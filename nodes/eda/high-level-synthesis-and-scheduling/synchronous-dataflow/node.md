---
tag: SZZFZY
kind: model
slug: synchronous-dataflow
name: Synchronous dataflow
aliases:
- SDF graph
- synchronous data flow graph
area: eda/high-level-synthesis-and-scheduling
level: core
summary: Lee and Messerschmitt's dataflow model whose actors produce and consume fixed numbers of tokens per firing, so schedules and buffer sizes are known at compile time.
prereqs: [petri-net, rank, nullspace]
see_also: [sdf-static-scheduling, kahn-process-network, iteration-bound, dsp-unfolding, timed-event-graph, deadlock, rank-nullity-theorem, nullspace-computation]
sources:
  - paper: doi:10.1109/PROC.1987.13876
    title: Edward A. Lee and David G. Messerschmitt, Synchronous data flow, Proceedings of the IEEE 75(9), 1235 to 1245, 1987
    locator: the model (actors with fixed token rates, delays as initial tokens), the topology matrix and the rank condition, and its use for signal processing
  - paper: doi:10.1109/TC.1987.5009446
    title: Edward A. Lee and David G. Messerschmitt, Static scheduling of synchronous data flow programs for digital signal processing, IEEE Transactions on Computers C-36(1), 24 to 35, 1987
    locator: the theorems on periodic admissible schedules (rank n - 1 is necessary, the repetition vector, deadlock, bounded memory) and the expansion into a precedence graph
  - paper: doi:10.1016/S0022-0000(71)80013-2
    title: F. Commoner, A. W. Holt, S. Even and A. Pnueli, Marked directed graphs, Journal of Computer and System Sciences 5(5), 511 to 523, 1971
    locator: the token count of a directed cycle is invariant, and a marked graph is live exactly when every directed cycle holds a token
  - book: isbn:0792397223
    title: Shuvra S. Bhattacharyya, Praveen K. Murthy and Edward A. Lee, Software Synthesis from Dataflow Graphs, Kluwer, 1996
    locator: the chapters on SDF consistency, scheduling and the buffer memory of schedules
  - paper: "Edward A. Lee and Thomas M. Parks, Dataflow process networks, Proceedings of the IEEE 83(5), 773 to 801, 1995"
    title: Edward A. Lee and Thomas M. Parks, Dataflow process networks, Proceedings of the IEEE 83(5), 773 to 801, 1995
    locator: SDF as a special case of Kahn process networks, and the dataflow models with data-dependent rates
---

Synchronous dataflow, or SDF, is a model of a signal processing program as a directed graph of actors that pass tokens along FIFO edges. Each actor consumes a fixed number of tokens from each input edge and produces a fixed number of tokens on each output edge every time it fires, and these numbers never depend on the data. Lee and Messerschmitt introduced it in 1987. Because the rates are fixed, a compiler can decide before the program runs whether it can run forever in bounded memory, how often each actor fires per period, and how large each buffer must be. This page defines the model and proves its basic theorems: the rank condition, the repetition vector, the cycle criterion for deadlock and the bounded memory theorem. The method that builds a schedule is on the [static scheduling of SDF](/sdf-static-scheduling/) page.

## The machine

An SDF graph has actors $1, \ldots, n$ and a finite set $E$ of directed edges. Each edge $e = (a, b)$ from actor $a$ to actor $b$ carries three integers: the production rate $p_e \ge 1$, the consumption rate $c_e \ge 1$ and the delay $d_e \ge 0$. Parallel edges and self loops are allowed. The delay is not a time: it is the number of tokens on the edge at the start, and in a signal flow graph it is the number of unit delays $z^{-1}$ on the arc.

The state of the machine is the vector $b \in \mathbb{Z}_{\ge 0}^E$ of token counts, with $b = d$ at the start. Actor $a$ is enabled in state $b$ when every input edge $e$ of $a$ holds $b_e \ge c_e$ tokens. One step fires one enabled actor: it removes $c_e$ tokens from each input edge and then adds $p_e$ tokens to each output edge. A firing is atomic, and the values of the tokens play no part in the model. A firing sequence is admissible when each actor in it is enabled at the moment it fires.

The topology matrix $\Gamma$ has one row per edge and one column per actor. For $e = (a, b)$ with $a \ne b$, row $e$ has $p_e$ in column $a$, $-c_e$ in column $b$ and 0 elsewhere. For a self loop on $a$, row $e$ has $p_e - c_e$ in column $a$. If $\mathbf{1}_a$ is the unit vector of actor $a$, firing $a$ changes the state from $b$ to $b + \Gamma \mathbf{1}_a$. So after an admissible sequence in which actor $a$ fires $x_a$ times, the state is
$$b = d + \Gamma x,$$
whatever the order of the firings. This is the same bookkeeping as the state equation of a [Petri net](/petri-net/).

The graph is called connected when it is connected after the edge directions are dropped. A graph with several components is a set of separate programs, so the results below assume a connected graph.

## What it counts

The cost unit is one firing, and the memory is the number of tokens on the edges. The questions of the model are about firing sequences:

- **Periodic admissible sequential schedule (PASS).** A finite admissible sequence $\sigma$ in which every actor fires at least once and after which the state is $d$ again. Repeating $\sigma$ runs the program forever.
- **Repetition vector.** The firing counts $q$ of the shortest periodic schedules.
- **Buffer bound.** The largest token count of each edge while a schedule runs, which is the memory a compiler must reserve.
- **Deadlock.** A state that no admissible sequence can leave toward the end of a period.

With an execution time per actor, the model also has a throughput, the number of periods per unit of time on unlimited processors. That question reduces to the [iteration bound](/iteration-bound/) of an expanded graph, as explained below.

## Relation to other models

- **Petri nets and marked graphs.** An SDF graph is a weighted Petri net in which every place has exactly one input transition and one output transition: actors are transitions, edges are places, rates are arc weights and delays are the initial marking. When all rates are 1 the graph is homogeneous, and it is exactly a marked graph in the sense of Commoner, Holt, Even and Pnueli. A [timed event graph](/timed-event-graph/) is the timed version of a marked graph.
- **Kahn process networks.** An SDF actor is a Kahn process that reads a fixed number of tokens from each input with blocking reads, so SDF is a special case of a [Kahn process network](/kahn-process-network/) and inherits its determinacy. The fixed rates are what make the questions above decidable, while they are undecidable for general Kahn networks.
- **Signal flow graphs and data flow graphs.** A homogeneous SDF graph whose actors have execution times is the data flow graph of the [iteration bound](/iteration-bound/), [retiming](/retiming/), [unfolding](/dsp-unfolding/) and [folding](/dsp-folding/) pages: one firing of each actor is one iteration, and the delays are registers.
- **Control data flow graphs.** A [CDFG](/control-data-flow-graph/) describes one run of a block with branches. SDF has no branches and describes a stream that never ends; its edges are queues, not single values.
- **Models with data-dependent rates.** Boolean dataflow adds actors whose rates depend on a control token. Lee and Parks (1995) survey this family and explain that such models can simulate any program, so the questions that SDF answers become undecidable for them.

## Known results in the model

Throughout, $G$ is connected, with $n$ actors and topology matrix $\Gamma$.

**Theorem 1 (rank condition and repetition vector).** If $G$ has a PASS, then $\operatorname{rank} \Gamma = n - 1$. If $\operatorname{rank} \Gamma = n - 1$, then the integer vectors $x$ with $\Gamma x = 0$ are exactly the multiples $t q$, $t \in \mathbb{Z}$, of one vector $q$ whose entries are positive integers with greatest common divisor 1. Every PASS fires each actor $a$ exactly $J q_a$ times for one integer $J \ge 1$.

*Proof.* First, $\operatorname{rank} \Gamma \ge n - 1$. Let $\Gamma x = 0$ with $x$ real. The row of an edge $e = (a, b)$ with $a \ne b$ says $p_e x_a = c_e x_b$, so $x_b = (p_e / c_e) x_a$. Along a spanning tree of the undirected graph, every entry of $x$ is a fixed positive multiple of $x_1$. So the null space has dimension at most 1, and the [rank-nullity theorem](/rank-nullity-theorem/) gives $\operatorname{rank} \Gamma \ge n - 1$.

Now let $\sigma$ be a PASS with firing counts $x$. The state after $\sigma$ is $d + \Gamma x = d$, so $\Gamma x = 0$ with $x \ne 0$. Hence the null space is not zero and $\operatorname{rank} \Gamma = n - 1$.

If $\operatorname{rank} \Gamma = n - 1$, the null space is one line. The spanning tree argument shows that this line is spanned by the vector $y$ with $y_1 = 1$ whose entries are the positive rationals forced by the tree. Multiply $y$ by the least common multiple of the denominators and divide by the greatest common divisor of the result: this gives $q$, with positive integer entries and gcd 1. Let $x$ be an integer null vector. Then $x = r q$ for a rational $r = u / v$ in lowest terms, and $v$ divides $u q_a$ for every $a$, so $v$ divides every $q_a$ and hence their gcd, which is 1. So $r$ is an integer. For a PASS, $x$ is a null vector with positive entries, so $x = J q$ with $J \ge 1$. $\square$

The vector $q$ is the repetition vector. A graph with $\operatorname{rank} \Gamma = n - 1$ is called consistent, and one with $\operatorname{rank} \Gamma = n$ is inconsistent: it has no PASS at all. The [nullspace computation](/nullspace-computation/) by [Gaussian elimination](/gaussian-elimination/) gives $q$, but the spanning tree walk above is simpler and is what the scheduling page uses.

**Theorem 2 (bounded memory).** If $G$ is inconsistent, then every infinite admissible firing sequence of $G$ has unbounded token counts.

*Proof.* Suppose an infinite admissible sequence keeps every count at most $B$. Then it visits finitely many states, so some state appears after two prefixes with firing counts $x < x'$ (componentwise $\le$, and not equal). Then $d + \Gamma x = d + \Gamma x'$, so $y = x' - x$ is a nonzero null vector with $y \ge 0$. For each edge, $p_e y_a = c_e y_b$, so $y_a = 0$ exactly when $y_b = 0$, and since $G$ is connected, every entry of $y$ is positive. So $\operatorname{rank} \Gamma \le n - 1$, and $G$ is consistent, a contradiction. $\square$

So an inconsistent graph either deadlocks or overflows any finite memory. A consistent graph can still deadlock, and the next theorem says exactly when.

**Theorem 3 (deadlock comes from a cycle).** Let $G$ be consistent with repetition vector $q$. For a directed simple cycle $C$ of $G$, let $G_C$ be the graph that has only the actors and edges of $C$, with the same rates and delays. Then $G$ has a PASS exactly when, for every directed simple cycle $C$, the graph $G_C$ alone has an admissible sequence in which each actor $a$ of $C$ fires $q_a$ times.

In words: deadlock always comes from a directed cycle whose initial tokens are too few for the cycle alone to complete its share of one period. An acyclic consistent graph never deadlocks. For a homogeneous graph, $q = \mathbf{1}$, and a cycle alone completes one firing of each actor exactly when it holds at least one token, which is the liveness theorem of Commoner, Holt, Even and Pnueli for marked graphs.

*Proof.* Number the firings of each actor $a$ as $(a, 1), (a, 2), \ldots$. For an edge $e = (a, b)$, the $j$-th firing of $b$ needs $j c_e$ tokens taken from $e$ in total, which holds exactly when $a$ has fired at least
$$f_e(j) = \max\left(0, \left\lceil \frac{j c_e - d_e}{p_e} \right\rceil\right)$$
times. Each $f_e$ is nondecreasing, $f_e(0) = 0$, and $f_e(j) \le \lceil j c_e / p_e \rceil$. Since $p_e q_a = c_e q_b$, this gives $f_e(q_b) \le q_a$, so $j \le q_b$ implies $f_e(j) \le q_a$.

Firings only add tokens to the edges that other actors read, so an enabled actor stays enabled until it fires. Hence the firings that a run can reach form a set that is closed downward, and $G$ reaches the counts $q$ exactly when the following requirement graph $R$ has no directed cycle. Its nodes are the firings $(a, j)$ with $1 \le j \le q_a$. It has an arc $(b, j) \to (b, j - 1)$ for $j \ge 2$, and an arc $(b, j) \to (a, f_e(j))$ for each input edge $e = (a, b)$ of $b$ with $f_e(j) \ge 1$. If $R$ is acyclic, firing in reverse topological order is admissible and reaches $q$, and the state is then $d + \Gamma q = d$, so this is a PASS. If $R$ has a cycle, no firing on it can come first, so no run fires all of them. By Theorem 1 a PASS fires each actor $a$ at least $q_a$ times, so it would fire every node of $R$, and no PASS exists. The same holds for $G_C$ with its own requirement graph $R_C$, whose arcs are a subset of the arcs of $R$ on the same nodes.

If some $G_C$ fails, then $R_C$ has a cycle, which is also a cycle of $R$, so $G$ has no PASS.

Conversely, suppose every $G_C$ completes, and let a closed walk $W$ in $G$ pass through actor $b$. Write $f_W$ for the composition of the functions $f_e$ of the edges of $W$, read backward from $b$ around to $b$. A cycle of $R$ through $(b, j)$ projects to a closed walk $W$ with $f_W(j) \ge j \ge 1$, since the arcs inside one actor only lower the index and every $f_e$ is nondecreasing. So it is enough to show $f_W(j) \le j - 1$ for every closed walk $W$ and every $1 \le j \le q_b$. For a simple cycle $C$, a value $f_C(j) \ge j$ would give a cycle of $R_C$ through $(b, j)$, since all the intermediate values stay in their windows and stay at least 1 (once a value is 0, all later ones are 0). So $f_C(j) \le j - 1 \le j$ on the window, and $f_C(0) = 0$. A closed walk $W$ that is not simple contains a simple cycle $C$ as a closed sub-walk at some actor $v$. Removing $C$ gives a shorter closed walk $W'$, and since $f_C(i) \le i$ and every $f_e$ is nondecreasing, $f_W(j) \le f_{W'}(j)$. Induction on the length of $W$ gives $f_W(j) \le j - 1$. So $R$ is acyclic and $G$ has a PASS. $\square$

The condition "fires $q_a$ times" can be read with the repetition vector of $G_C$ instead: the rows of $C$ are rows of $\Gamma$, so the repetition vector $q^C$ of $G_C$ satisfies $q|_C = t q^C$ for an integer $t \ge 1$, and a cycle that completes $q^C$ is back in its start state and can repeat it $t$ times.

**Precedence expansion.** Lee and Messerschmitt (1987, IEEE Transactions on Computers) expand a consistent SDF graph into an acyclic precedence graph with $q_a$ nodes for actor $a$, one per firing in one period, and an arc from each firing to the firings of the same period that need its tokens. It orders the same firings as the requirement graph $R$ above, read in the other direction. If the dependencies on tokens of earlier periods are added as edges with delays, the result is a homogeneous graph with one iteration per period. With execution times on the actors, the throughput on unlimited processors is then the inverse of the [iteration bound](/iteration-bound/) of that homogeneous graph.

### Example

Take three actors $A, B, C$ on a ring: $A$ produces 2 tokens and $B$ consumes 3 on edge $A \to B$; $B$ produces 1 and $C$ consumes 2 on edge $B \to C$; $C$ produces 3 and $A$ consumes 1 on edge $C \to A$, which holds $d$ initial tokens. Then
$$\Gamma = \begin{pmatrix} 2 & -3 & 0 \\ 0 & 1 & -2 \\ -1 & 0 & 3 \end{pmatrix}, \qquad q = (3, 2, 1).$$
The rows give $2 q_A = 3 q_B$, $q_B = 2 q_C$ and $3 q_C = q_A$, which $q$ meets, and the rank is 2. One period fires $A$ three times, $B$ twice and $C$ once.

The graph is one cycle, so Theorem 3 reduces to running it. With $d = 3$, the sequence $AAABBC$ is admissible: $A$ uses the 3 tokens and puts 6 on $A \to B$, $B$ fires twice and puts 2 on $B \to C$, and $C$ fires once and puts 3 tokens back on $C \to A$. With $d = 2$, $A$ fires twice, $B$ fires once, and then 1 token waits on $A \to B$ for $B$, 1 token waits on $B \to C$ for $C$, and nothing waits for $A$: a deadlock, although the graph is consistent. Any $d \le 2$ deadlocks in the same way.

Change the rates of $C \to A$ to "$C$ produces 2, $A$ consumes 1". The third row becomes $(-1, 0, 2)$, the determinant is $-2$, the rank is 3, and by Theorem 2 every infinite run of this graph either stops or needs unbounded memory: $A$ now gets $2/3$ of the tokens it needs per period of the other two actors.

## References
