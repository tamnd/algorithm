---
tag: 1NTC06
kind: technique
slug: secondary-sort
name: Secondary sort
aliases:
- value-to-key sort
- composite key sort
- value-to-key conversion
area: parallel/mapreduce-and-bsp
level: advanced
summary: Let the MapReduce framework sort the values of each key by moving the sort field into a composite key, with a partitioner and a grouping on the natural key only.
prereqs: [mapreduce-model, shuffle-phase, partitioner]
see_also: [combiner, inverted-index, reduce-side-join, distributed-sorting, external-merge-sort, stable-sort, data-skew, word-count]
sources:
  - book: isbn:9781608453429
    title: Jimmy Lin and Chris Dyer, Data-Intensive Text Processing with MapReduce, Morgan and Claypool, 2010
    locator: Section 3.3 (computing relative frequencies, the order inversion pattern), Section 3.4 (secondary sorting, the value-to-key conversion pattern with the sensor example), Section 3.5.1 (reduce-side join) and Section 4.4 (revised inverted indexing)
  - paper: "Jeffrey Dean and Sanjay Ghemawat, MapReduce: simplified data processing on large clusters, 6th Symposium on Operating Systems Design and Implementation (OSDI), 2004"
    locator: Section 4.1 (partitioning function) and Section 4.2 (ordering guarantees, keys processed in increasing order within a partition)
  - book: isbn:9781491901632
    title: Tom White, Hadoop, The Definitive Guide, fourth edition, O'Reilly, 2015
    locator: Chapter 9 (MapReduce Features), the part on sorting with secondary sort
---

A secondary sort is a [MapReduce](/mapreduce-model/) technique that delivers the values of each key to the reducer in a chosen order, using the framework's sort instead of a sort inside the reducer. The mapper moves the sort field from the value into a composite key (natural key, sort field), the [partitioner](/partitioner/) and the grouping use only the natural key, and the [shuffle](/shuffle-phase/) sorts by the whole composite key. Lin and Dyer (Section 3.4) call this **value-to-key conversion**. It turns a reducer that needs memory for its largest group into one that streams.

## In plain words

Suppose each receiving computer gets all the readings of one sensor, but in random order, and it must output them in time order. It could hold all the readings and sort them, but one sensor may have more readings than fit in memory. The system already sorts by key before the receivers start. So put the time into the key next to the sensor name. Tell the system to send keys by the sensor name only, so that one sensor still goes to one receiver, and to sort by the name and then the time. The receiver now gets the readings of each sensor already in time order, one after another, and needs to keep almost nothing in memory.

## When it applies

- The reducer needs the values of a key in a fixed order: time series, the postings of an [inverted index](/inverted-index/) in document order, or the records of a group sorted by some field.
- A group can be larger than the memory of a reduce task, so a buffer and an in-memory sort do not scale (Lin and Dyer, Section 3.4).
- The reducer needs one special value before all the others, for example the total count before the counts it divides by (the order inversion pattern of Section 3.3), or the one tuple of a small relation before the many tuples it joins with (Section 3.5.1).
- It does not apply when the values have no order that the reducer can use, for example when they are only added up. Then a [combiner](/combiner/) is the right tool.

## The template

Let the input give records with a natural key $k$, a sort field $s$ with a total order, and a payload $x$. The goal is one reduce call per $k$ whose values are the payloads in increasing $s$.

1. **Map.** Emit the composite key $(k, s)$ with the value $x$ (and $s$ as well, when the reducer needs it).
2. **Partition** on the natural key: $\pi((k, s)) = h(k) \bmod R$.
3. **Sort** the pairs by the composite key in lexicographic order: by $k$, then by $s$.
4. **Group** on the natural key: consecutive pairs with equal $k$ form one reduce call. Hadoop calls the function that decides this the grouping comparator. Without it, as in Lin and Dyer's description, each composite key is its own reduce call, and the reducer keeps state across calls and notices when $k$ changes.
5. **Reduce.** Read the values in order and emit as they arrive.

**Why it works.** By step 2, every pair with natural key $k$ goes to the reduce task $h(k) \bmod R$, so one task holds all of them. By step 3, the pairs of that task are in lexicographic order, so all pairs with natural key $k$ form one contiguous run (any pair between two pairs with key $k$ has key $k$ too), and inside the run they are in increasing $s$. By step 4, this run is exactly one group. So the reduce call for $k$ gets all values of $k$, sorted by $s$. When two records have the same $(k, s)$, their order is not fixed, so add a tie-break field if the order matters.

**Cost.** The number of pairs and the bytes of the [shuffle](/shuffle-phase/) are the same as in the plain job with key $k$ and value $(s, x)$, since $s$ only moves from the value to the key. The framework does the sorting with its external merge, which works for any group size. The reducer needs $O(1)$ memory besides its output, while the buffer-and-sort reducer needs memory for the largest group, $\Theta(\max_k |V_k|)$ values. The extra work is in the comparisons, which now compare composite keys. The secondary sort does not change the largest reducer input: one natural key still goes to one task, so a heavy key is still a problem of [data skew](/data-skew/).

## Classic examples

**Sensor time series (Lin and Dyer, Section 3.4).** Records are (sensor, time, reading). The mapper emits ((sensor, time), reading). With the readings (m1, 3, 30), (m2, 1, 11), (m1, 1, 10), (m1, 2, 20), (m2, 2, 12), the sort order inside the reduce tasks is (m1, 1), (m1, 2), (m1, 3), (m2, 1), (m2, 2), and the output is m1 with [10, 20, 30] and m2 with [11, 12], whatever the order of arrival.

**Postings of an inverted index (Lin and Dyer, Section 4.4).** The baseline [inverted index](/inverted-index/) emits (term, (doc id, term frequency)) and sorts each posting list in the reducer, which runs out of memory for frequent terms. The revised version emits ((term, doc id), term frequency) with a partitioner on the term, so the postings arrive in document order and can be gap-encoded on the fly.

**Relative frequencies with order inversion (Lin and Dyer, Section 3.3).** To compute $f(u \mid w) = N(w, u)/\sum_{u'} N(w, u')$ for neighbour words, the mapper emits $((w, u), 1)$ for each neighbour pair and also $((w, *), 1)$, where $*$ sorts before every word. The partitioner uses $w$ only. The reducer for $w$ then sees all $(w, *)$ values first, adds them into the marginal $\sum_{u'} N(w, u')$, and divides each following count $N(w, u)$ by it, in one pass and with no buffer of the counts.

**The reduce-side join, one-to-many (Lin and Dyer, Section 3.5.1).** To join a relation $S$ with unique keys to a relation $T$ with many tuples per key, the mapper tags each tuple and emits the composite key (join key, tag) with the tag of $S$ sorting first. The reducer holds the one $S$ tuple in memory and streams the $T$ tuples past it. See [reduce-side join](/reduce-side-join/).

## Variations

- **More sort fields.** The same pattern sorts by a third and fourth field: the composite key is $(k, s_1, s_2, \dots)$, the sort is lexicographic, and the partitioner and the grouping still use $k$ only.
- **Descending order.** Sort the second field in decreasing order, for example to read the top values of each group first and stop early.
- **Grouping without a grouping comparator.** If the framework groups by the whole key, the reducer keeps the current natural key in a variable and starts a new output when it changes. This is the form that Lin and Dyer give.
- **The total sort.** Sorting the whole input by the key across all reduce tasks needs a range [partitioner](/partitioner/) instead, see [distributed sorting](/distributed-sorting/). A secondary sort only orders values inside each key.

## Pitfalls

- **Partitioning on the whole composite key.** Then the pairs of one natural key are spread over several reduce tasks, and each task emits a part of the series. The output has the same natural key more than once.
- **Grouping on the whole composite key in a reducer that expects one call per natural key.** Each (key, sort field) becomes its own reduce call, so a series of 20 readings gives 20 calls of one value each.
- **A sort order that is not lexicographic on (natural key, sort field).** If the sort compares the sort field first, the pairs of one natural key are not contiguous, and the grouping splits them.
- **Relying on the order of equal composite keys.** The framework does not promise a [stable sort](/stable-sort/) across map tasks, so ties need an explicit tie-break.
- **Expecting balance.** A secondary sort does nothing for a natural key with most of the data.

## Exercises

1. A log has records (user, time, page). Design a secondary sort that outputs, for each user, the pages in time order. Give the composite key, the partitioner and the grouping. *Answer:* key (user, time), value page, partition and group on user, sort by (user, time).
2. Show that the template is wrong if the partitioner is $h((k, s)) \bmod R$, with a concrete input. *Answer:* one natural key with two sort fields that hash to two different tasks gives two output groups for the same key.
3. For each user, output only the 3 latest pages. Which sort order lets the reducer stop after 3 values? *Answer:* sort the time in decreasing order, so the reducer emits the first 3 values of each group and skips the rest.
4. In the order inversion example, why must the partitioner use only $w$ and not $(w, u)$? *Answer:* the marginal key $(w, *)$ and the keys $(w, u)$ must reach the same reduce task, or the task that holds $(w, u)$ never sees the marginal.

## References
