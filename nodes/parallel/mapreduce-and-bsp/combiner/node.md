---
tag: 1WW8S5
kind: concept
slug: combiner
name: Combiner
aliases:
- map-side combiner
- mini-reducer
area: parallel/mapreduce-and-bsp
level: intro
summary: An optional local reduce on mapper output that cuts shuffle volume when the reduce function is associative and commutative.
prereqs: [mapreduce-model, associative-operator]
see_also: [shuffle-phase, word-count, monoid, partitioner, data-skew, group-by-aggregation, parallel-reduce, secondary-sort]
sources:
  - paper: "Jeffrey Dean and Sanjay Ghemawat, MapReduce: simplified data processing on large clusters, 6th Symposium on Operating Systems Design and Implementation (OSDI), 2004"
    locator: Section 4.3 (combiner function, for a Reduce function that is commutative and associative)
  - book: isbn:9781608453429
    title: Jimmy Lin and Chris Dyer, Data-Intensive Text Processing with MapReduce, Morgan and Claypool, 2010
    locator: Section 2.4 (partitioners and combiners), Section 3.1.1 (combiners and in-mapper combining) and Section 3.1.2 (algorithmic correctness with local aggregation, the mean example)
  - book: isbn:9781108476348
    title: Jure Leskovec, Anand Rajaraman and Jeffrey D. Ullman, Mining of Massive Datasets, third edition, Cambridge University Press, 2020
    locator: Section 2.2.4 (Combiners)
  - paper: "Jim Gray, Surajit Chaudhuri, Adam Bosworth, Andrew Layman, Don Reichart, Murali Venkatrao, Frank Pellow and Hamid Pirahesh, Data Cube: A Relational Aggregation Operator Generalizing Group-By, Cross-Tab, and Sub-Totals, Data Mining and Knowledge Discovery 1(1), 1997"
    locator: the classification of aggregate functions as distributive, algebraic and holistic
---

A combiner is a function that a [MapReduce](/mapreduce-model/) job runs on the output of each map task before the [shuffle](/shuffle-phase/), to merge the values of each key locally. It has the type of a reduce function whose output pairs have the same type as the map output, and it is often the reduce function itself. It cuts the data sent over the network, but the framework may run it zero, one or many times, so it is correct only when the result does not depend on how often and on which groups of values it runs. The exact condition is that the reduce function is a function of an [associative](/associative-operator/) and commutative combination of its values.

## In plain words

In word count, a computer that reads "the" a thousand times sends a thousand notes that each say "the, 1". A combiner lets it add these up first and send one note that says "the, 1000". The receiving computer then adds up far fewer notes and gets the same total. This works for sums because you can add numbers in any order and any grouping. It does not work for an average: the average of a few small averages is not, in general, the average of all the numbers. The fix is to send a running total and a count instead, add those up in the same way, and divide only at the very end.

## The idea

### When a combiner is correct

Let one key $k$ receive the multiset $V_k$ of values from the map calls. The system may apply the combiner to any non-empty group of the values of $k$ in a map task's buffer, any number of times, before the values reach the reducer (Lin and Dyer, Section 3.1.2: zero, one or multiple times). Hadoop, for example, runs it on each spill and may run it again on the merge, see [shuffle phase](/shuffle-phase/).

**A sufficient condition.** Suppose that

1. the values have a type $T$ with a binary operation $\oplus$ that is associative and commutative (a commutative semigroup, for example a commutative [monoid](/monoid/)),
2. the combiner, given $k$ and a non-empty list $S$ of values, emits the single pair $(k, \bigoplus S)$, with the same key and a value of type $T$, and
3. the reducer, given $k$ and a list $X$, outputs $f(k, \bigoplus X)$ for some function $f$.

Then the output of the job is the same for every way of running the combiner, and equals the output with no combiner.

*Proof.* In a commutative semigroup, the combination $\bigoplus S$ of a finite non-empty multiset is the same for every order and every bracketing, so it is well defined. Fix a key $k$ and let $X$ be the multiset of its values that exist at some moment (in buffers, spill files or in transit). The claim is that $\bigoplus X = \bigoplus V_k$ at all times. It holds at the start, when $X = V_k$. One combiner call takes a non-empty sub-multiset $S \subseteq X$ and replaces it with the single value $\bigoplus S$, so the new multiset is $X' = (X \setminus S) \cup \{\bigoplus S\}$. If $X \setminus S$ is empty, then $\bigoplus X' = \bigoplus S = \bigoplus X$. Else $\bigoplus X' = \big(\bigoplus (X \setminus S)\big) \oplus \big(\bigoplus S\big) = \bigoplus X$, by associativity and commutativity. The combiner keeps the key, so the pair still goes to the reduce task that owns $k$. There are finitely many combiner calls, so by induction the reducer receives a multiset $X$ with $\bigoplus X = \bigoplus V_k$, and it outputs $f(k, \bigoplus V_k)$, which is the output with no combiner. $\blacksquare$

The condition is the precise form of Dean and Ghemawat's "the Reduce function is commutative and associative" (Section 4.3). It needs three things that are easy to miss: the mapper must already emit values of type $T$, the combiner must emit the same type, and the final step $f$ runs only in the reducer. In the language of Gray et al., the aggregates with such a plan are the **distributive** ones (sum, count, min, max), where $f$ is the identity, and the **algebraic** ones (mean, variance), where $T$ is a tuple of a fixed size. A **holistic** aggregate such as the median has no summary of a fixed size, so a combiner cannot shrink its data.

### What it saves

Without a combiner, map task $i$ sends one pair for each of its $n_i$ output pairs. With one combiner pass on its whole output, it sends one pair for each of its $D_i$ distinct keys, and $D_i \le n_i$. So the shuffle shrinks from $\sum_i n_i$ to $\sum_i D_i$ pairs, and each key group at a reducer has at most $M$ values for $M$ map tasks. The saving is large when the keys repeat often within a split, which is the case for the frequent keys that also cause [data skew](/data-skew/). The [word count](/word-count/) page derives the expected saving for words with a Zipf distribution. When almost every key in a split is distinct, the combiner saves nothing and costs a sort of the map output.

### In-mapper combining

Lin and Dyer (Section 3.1.1) describe a pattern that does the combining inside the mapper: the map task keeps a hash table from keys to partial values across all its map calls, and emits the table at the end. It always runs exactly once, so its correctness does not depend on the framework, and it avoids writing the uncombined pairs at all. It needs memory for one entry per distinct key of the split, and it must flush the table when the memory fills.

## Examples

**Sum (correct).** Map emits $(w, 1)$ for each word, and the combiner and the reducer both add the values. Here $T = \mathbb{Z}$, $\oplus = +$ and $f$ is the identity. The split "a rose is a rose" sends (a, 2), (is, 1), (rose, 2) instead of 5 pairs.

**Count of values (incorrect).** A reducer that outputs the number of values it receives is not a valid combiner. If (a, 1), (a, 1) are combined into (a, 2) and a third (a, 1) arrives from another map task, the reducer sees 2 values and outputs (a, 2) instead of (a, 3). The count is $f(\bigoplus X)$ only if each value is the number 1 and $\oplus$ is $+$, so the fix is to use the sum as the combiner and the reducer.

**Mean (incorrect).** Let the reducer output the mean of its values, and let the values of one key be 1, 2, 3, 4, 5, where one map task has 1, 2 and another has 3, 4, 5. With the mean reducer as the combiner, the reducer sees the two values 1.5 and 4 and outputs

$$\text{mean}(\text{mean}(1, 2), \text{mean}(3, 4, 5)) = \text{mean}(1.5, 4) = 2.75,$$

while the true mean is $\text{mean}(1, 2, 3, 4, 5) = 3$. The mean is commutative but not associative: $\text{mean}(\text{mean}(x, y), z) \ne \text{mean}(x, y, z)$ in general. This is Lin and Dyer's example (Section 3.1.2).

**Mean (the fix).** Let the mapper emit $(k, (x, 1))$ for each value $x$. Let the combiner add the pairs componentwise, $(s_1, c_1) \oplus (s_2, c_2) = (s_1 + s_2, c_1 + c_2)$, which is associative and commutative. Let the reducer add its pairs into $(s, c)$ and output $s/c$. In the example, the map tasks send $(3, 2)$ and $(12, 3)$, and the reducer outputs $15/5 = 3$. The mapper must emit pairs too: if it emits plain numbers and only the combiner makes pairs, the reducer receives numbers whenever the combiner does not run, and it fails.

**Other algebraic aggregates.** The variance uses $(c, s, q) = (\text{count}, \sum x, \sum x^2)$ with componentwise addition and $f(c, s, q) = q/c - (s/c)^2$. The top $j$ values use $T$ = sorted lists of at most $j$ values, with $A \oplus B$ = the $j$ largest of $A \cup B$. A distinct count uses sets with union, or a mergeable sketch when the sets are too large.

## Where it is used

- [Word count](/word-count/), [group-by aggregation](/group-by-aggregation/), histograms and every MapReduce job that aggregates with a sum, count, min or max.
- The pre-aggregation of a [hash aggregation](/hash-aggregation/) before a repartition in parallel databases, which is the same idea with the same correctness condition.
- [Parallel reduce](/parallel-reduce/) in shared memory, which also needs an associative operator so that a tree of partial results gives the same answer as a sequential pass.
- Combiners reduce the input of the reducers of heavy keys, so they are the first fix for [data skew](/data-skew/) in aggregations. They do not help a [reduce-side join](/reduce-side-join/), where every value of a key is needed.

## References
