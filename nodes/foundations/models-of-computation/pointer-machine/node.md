---
tag: ZZAQ4P
kind: model
slug: pointer-machine
name: Pointer machine
aliases:
- pointer machine model
area: foundations/models-of-computation
level: advanced
summary: Model where records are nodes with pointer fields and no arithmetic on addresses; used for lower bounds on data structures.
prereqs: [random-access-machine, unit-cost-model, asymptotic-notation]
see_also: [word-ram, cell-probe-model, disjoint-set-forest, union-find-lower-bound, inverse-ackermann-function, turing-machine, comparison-model]
sources:
  - paper: "Andrei N. Kolmogorov and Vladimir A. Uspenskii, On the definition of an algorithm, Uspekhi Matematicheskikh Nauk 13(4) (1958); English translation in American Mathematical Society Translations, series 2, 29 (1963)"
    locator: the definition of the machine on graphs
  - paper: "Arnold Schönhage, Storage modification machines, SIAM Journal on Computing 9(3) (1980)"
    locator: the definition of the machine and the comparison with the Kolmogorov and Uspenskii machine
  - paper: "Robert E. Tarjan, A class of algorithms which require nonlinear time to maintain disjoint sets, Journal of Computer and System Sciences 18(2) (1979)"
    locator: the pointer machine, the separability assumption and the lower bound for set union
  - paper: "Robert E. Tarjan, Efficiency of a good but not linear set union algorithm, Journal of the ACM 22(2) (1975)"
    locator: the upper bound for union by rank with path compression
  - paper: 'Amir M. Ben-Amram, What is a "pointer machine"?, SIGACT News 26(2) (1995), 88 to 95'
    locator: the survey of the different definitions
  - paper: "Norbert Blum, On the single-operation worst-case time complexity of the disjoint set union problem, SIAM Journal on Computing 15(4) (1986)"
    locator: abstract (the bound for one operation)
  - paper: "Michael L. Fredman and Michael E. Saks, The cell probe complexity of dynamic data structures, Proceedings of the 21st ACM Symposium on Theory of Computing (STOC 1989)"
    locator: the lower bound for the union-find problem in the cell-probe model
  - paper: "Johannes A. La Poutré, Lower bounds for the union-find and the split-find problem on pointer machines, Proceedings of the 22nd ACM Symposium on Theory of Computing (STOC 1990); journal version in Journal of Computer and System Sciences 52(1) (1996)"
    locator: the main theorem (the union-find lower bound for all pointer machine algorithms, without separability)
  - paper: "Bernard Chazelle, Lower bounds for orthogonal range searching: I. The reporting case, Journal of the ACM 37(2) (1990)"
    locator: the main theorem (the space lower bound on the pointer machine)
  - paper: "James R. Driscoll, Neil Sarnak, Daniel D. Sleator and Robert E. Tarjan, Making data structures persistent, Journal of Computer and System Sciences 38(1) (1989)"
    locator: the node-copying and node-splitting methods for linked structures of bounded in-degree
---

A pointer machine is a model of computation whose memory is a graph of nodes. Each node has a fixed number of pointer fields. A program follows pointers, changes them, and makes new nodes, but it never does arithmetic on an address. Kolmogorov and Uspenskii, Schönhage and Tarjan gave three forms of it. It is the model of the lower bound of Tarjan for the union-find problem.

## The machine

The following form is common (Tarjan 1979; Ben-Amram 1995 compares the forms).

**Memory.** The memory is a finite directed graph. Its nodes are records. Each node has $k$ pointer fields $f_1, \dots, f_k$, where $k$ is a constant of the program, and each field points to a node. Some definitions also give each node a fixed number of data fields, with values from a finite alphabet. Other definitions let the data fields hold integers that the program can add and compare, but never use as a pointer.

**Registers.** The program has a constant number of registers. Each register holds a pointer to a node. The input is a sequence of symbols, or a graph given at the start.

**Instructions.** Each of these costs one step.

- $x := y$: copy a pointer between registers.
- $x := \mathrm{nil}$: make $x$ point to a special node $\mathrm{nil}$, which has all its fields pointing to itself.
- $x := y.f$: follow the field $f$ of the node that $y$ points to.
- $x.f := y$: make the field $f$ of the node $x$ point to the node that $y$ points to.
- $x := \mathrm{new}$: make a new node, with a fixed rule for its pointers (for example, all point to a special node), and put a pointer to it in $x$.
- A test of two registers for equality, or of one register against $\mathrm{nil}$, and a conditional jump.

A pointer is a value that the program can copy, follow and compare with another pointer for equality. It has no number. So the program cannot compute an index and jump to the item at that index. Memory that no register can reach is lost, and the space of a program is the number of nodes in use.

**The forms of the model.** Kolmogorov and Uspenskii (1958) gave the first form. Their memory is an undirected graph of bounded degree, with labelled nodes. One step replaces a neighbourhood of fixed radius around an active node by another one. Schönhage (1980) gave the *storage modification machine*. Its memory is a directed graph in which every node has one outgoing edge for each symbol of a finite alphabet, and a distinguished *center* node. A program names a node by a word of symbols that it follows from the center, and it makes new nodes, redirects edges and tests two named nodes for equality. A node can have any number of incoming edges. Schönhage compared it with the machine of Kolmogorov and Uspenskii in the same paper. Tarjan (1979) gave the form with registers and records that is stated above, and used it for data structures. All three forms compute the same functions as a Turing machine. This page uses Tarjan's form.

**Example.** Reverse a singly linked list of $n$ nodes, where $\mathrm{next}$ is the pointer field and $\mathrm{head}$ points to the first node. The program is as follows.

```
prev := nil
cur := head
L: if cur = nil goto E
   nxt := cur.next
   cur.next := prev
   prev := cur
   cur := nxt
   goto L
E: (the list starts at prev)
```

Each node costs 6 steps, and the start and the last test cost 3 steps. The total is $6n + 3$. The program uses the registers $\mathrm{head}$, $\mathrm{prev}$, $\mathrm{cur}$ and $\mathrm{nxt}$, and no new node.

**Non-example.** No pointer structure gives access to any one of $n$ stored items in $O(1)$ steps. Let the program have $r$ registers and $k$ fields in each node. A node that the program reaches in $t$ steps is at the end of a path of at most $t$ edges from a node that a register held at the start, so at most $r(1 + k + \dots + k^t) \le r(k+1)^t$ nodes can be reached. To reach each of $n$ stored items for some query, the program needs $r(k+1)^t \ge n$, so $t \ge \log_{k+1}(n/r) = \Omega(\log n)$ steps in the worst case. A balanced tree meets this bound. A [random access machine](/random-access-machine/) with the items in an array reads any one of them in one step.

## What it counts

The cost is the number of instructions, as in the [unit-cost model](/unit-cost-model/), and the space is the number of nodes in use. A pointer is one unit. In the form with finite data fields, no node holds a number whose size depends on $n$, so the model has no word size. The cost of an operation is the number of instructions it executes, and most of them read or write one pointer. An address cannot be computed. Lower bounds are about the structure of the pointers.

## Relation to other models

- **RAM.** A [random access machine](/random-access-machine/) can run a pointer machine program with the same number of steps. It stores each node as $k$ consecutive cells, a pointer is the address of the first cell, and a new node takes the next free cells. So a lower bound for the RAM is a lower bound for the pointer machine, and an upper bound on the pointer machine is an upper bound on the RAM. A lower bound on the pointer machine does not carry over to the RAM. The RAM can compute an address, so it can index an array, hash a key and add two pointers. The pointer machine cannot.
- **Word RAM and hashing.** On the [word RAM](/word-ram/) a hash table gives $O(1)$ expected time for a lookup. The pointer machine cannot use a key as an address.
- **Turing machine.** A pointer machine can simulate a [Turing machine](/turing-machine/) with a constant number of steps for each step of the machine, because the tape is a doubly linked list. Schönhage (1980) used the storage modification machine to multiply two $n$-bit integers in $O(n)$ steps, which is faster than the known bounds for a multitape Turing machine.
- **Cell-probe model.** The [cell-probe model](/cell-probe-model/) counts the memory cells that a program reads and writes, with free computation. A lower bound there holds for every pointer machine, after each pointer is written as an address of $O(\log S)$ bits, where $S$ is the number of nodes. This is $O(\log n)$ when the space is polynomial in $n$.

## Known results in the model

**Union-find.** The set union problem keeps a partition of $n$ elements under *union* of two sets and *find* of the set of an element. A sequence has $n - 1$ unions and $m \ge n$ finds.

Upper bound: the forest of [union by rank](/union-by-rank/) with [path compression](/path-compression/) takes $O(m\,\alpha(m,n))$ time in total (Tarjan 1975), where $\alpha$ is the inverse Ackermann function (see [inverse Ackermann function](/inverse-ackermann-function/) and [disjoint-set forest](/disjoint-set-forest/)). It uses parent pointers and a rank at each root, so it is a pointer machine algorithm for the form of the model whose nodes hold integers that are never used as addresses.

Lower bound: Tarjan (1979) proved that every *separable* pointer algorithm needs $\Omega(m\,\alpha(m,n))$ time on some sequence of $n - 1$ unions and $m \ge n$ finds, so $\Omega(\alpha(m,n))$ amortized time for each operation. This matches the upper bound. Informally, an algorithm is separable if the nodes of the structure divide into parts, one for each current set, and an operation on an element reads only the part of its own set, and a union merges two parts. The exact conditions are in the paper. The family of such algorithms includes all the usual forest algorithms: linking by size or rank, with path compression, path halving or path splitting. Tarjan's result is a statement about a class of algorithms. La Poutré (1990, journal version 1996) removed the separability condition: every pointer machine algorithm needs $\Omega(m\,\alpha(m,n))$ time on some sequence. See [union-find lower bound](/union-find-lower-bound/).

Further results: Blum (1986) proved that for a class of pointer algorithms the worst-case time of a single operation is $\Theta(\log n / \log\log n)$. Fredman and Saks (1989) proved in the cell-probe model, with cells of $O(\log n)$ bits, that union-find needs $\Omega(\alpha(m,n))$ amortized time. This bound holds in a model that can compute addresses, so the amortized $\alpha$ is needed for every data structure in that model, and so on the word RAM.

**Sorting and searching.** Here the keys are held in data fields that the program can compare, or are compared by an oracle, since the form with finite data fields has no keys. Sorting by comparisons needs $\Omega(n \log n)$ comparisons (see [comparison model](/comparison-model/)). [Merge sort](/merge-sort/) on linked lists meets this bound on a pointer machine, with $O(n \log n)$ steps.

**Orthogonal range reporting.** Chazelle (1990) proved that on the pointer machine, a structure that answers $d$-dimensional [orthogonal range reporting](/orthogonal-range-reporting/) queries on $n$ points in $O(\log^c n + k)$ time, for a constant $c$ and output size $k$, needs $\Omega\big(n (\log n / \log\log n)^{d-1}\big)$ space.

**Persistence.** Driscoll, Sarnak, Sleator and Tarjan (1989) showed how to make a linked structure [persistent](/persistent-data-structure/) when each node has in-degree bounded by a constant. Node copying gives partial persistence, and node splitting gives full persistence. Both cost $O(1)$ amortized time and space for each step of an update. The methods are pointer machine programs, and they need the bound on the in-degree.

## References
