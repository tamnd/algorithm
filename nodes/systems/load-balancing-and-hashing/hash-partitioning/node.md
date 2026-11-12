---
tag: FCHGS3
kind: technique
slug: hash-partitioning
name: Hash partitioning
aliases:
- hash sharding
area: systems/load-balancing-and-hashing
level: intro
summary: Put each record in partition h(key) mod P, then map the P partitions to nodes. Point lookups touch one partition and loads are even, but a range query must visit every partition.
prereqs: [hash-function, sharding]
see_also: [range-partitioning, consistent-hashing, partitioner, grace-hash-join, load-skew, balls-into-bins-max-load, dynamic-partitioning-problem, virtual-nodes]
sources:
  - paper: doi:10.1145/129888.129894
    title: David DeWitt and Jim Gray, Parallel database systems, the future of high performance database systems, Communications of the ACM 35(6), 1992, pages 85 to 98
    locator: the section on data partitioning (round-robin, hash and range partitioning of a relation over the disks of a parallel database, and their effect on point and range queries)
  - book: isbn:9781449373320
    title: Martin Kleppmann, Designing Data-Intensive Applications, O'Reilly, 2017
    locator: "Chapter 6, Partitioning: partitioning by hash of key, skewed workloads and relieving hot spots, rebalancing (why not hash mod N, a fixed number of partitions), request routing"
  - url: https://redis.io/docs/latest/operate/oss_and_stack/reference/cluster-spec/
    title: Redis cluster specification
    locator: "Key distribution model (HASH_SLOT = CRC16(key) mod 16384, CRC16 XMODEM with output 31C3 for 123456789) and Hash tags"
  - url: https://www.elastic.co/docs/reference/elasticsearch/mapping-reference/mapping-routing-field
    title: Elasticsearch reference, the _routing field
    locator: "the formula shard_num = hash(_routing) % num_primary_shards, and the older form with num_routing_shards"
---

Hash partitioning splits a data set over $P$ partitions by a [hash](/hash-function/) of each record's key: the record with key $k$ goes to partition $h(k) \bmod P$, and a separate map assigns partitions to nodes. It is the most common way to place data in [sharding](/sharding/), in parallel databases and in the shuffle of a parallel join. With a good hash and many distinct keys the partitions are close to equal, whatever the order and the pattern of the keys. The price is the loss of order: keys that are close are spread over all partitions, so a range query must ask every partition. This page covers placement of stored data; the [partitioner](/partitioner/) page covers the same rule for the reducers of a MapReduce job.

## In plain words

You must split a large table over several machines. Take the key of each row, run it through a hash function that scrambles it into a number, and use the number to pick a partition. To find a row later, compute the same number. Rows spread evenly, even if the keys come in order, like user 1, user 2, user 3.

Two problems remain. Rows with nearby keys end up far apart, so a question such as "all orders from March" has to go to every machine. And if you tie the partition directly to the number of machines, adding one machine moves almost every row. So most systems make many more partitions than machines, and move whole partitions when machines come and go.

## When it applies

- The workload is mostly point operations by key: get, put and delete of one record, or of a group of records that share a key.
- The key has enough distinct values that are used evenly. Many keys of small and similar weight spread well; one very hot key does not (see [load skew](/load-skew/)).
- Range scans over the key are rare, or they are on another attribute that needs a scan of all partitions anyway.
- Two data sets joined on the same key can be partitioned by the same hash and the same $P$, so that the join runs in each partition with no data movement.

The model: $m$ records with distinct keys, $P$ partitions, $N$ nodes, and a hash that behaves like a random function. The measures are the largest partition, the number of partitions a query touches, and the number of records that move when $N$ changes.

## The template

```pseudo id=main
PARTITION(k)                         ▷ P partitions, fixed when the data set is created
L1  return h(k) mod P

ROUTE(k)                             ▷ owner[0..P-1]: partition to node, kept by a coordinator
L2  return owner[PARTITION(k)]

ADD-NODE(x)                          ▷ N counts x; move whole partitions, never single records
L3  while x owns fewer than ⌊P / N⌋ partitions do
L4      move one partition from the node with the most partitions to x
```

**Balance.** For distinct keys and a random hash, the size of one partition is binomial with $m$ trials and success probability $1/P$, so its mean is $m/P$ and its standard deviation is $\sqrt{m (1/P)(1 - 1/P)}$. The largest partition is $m/P + O(\sqrt{(m/P) \ln P})$ with high probability when $m \ge P \ln P$, the heavy case of [balls into bins](/balls-into-bins-max-load/). This bound counts keys. It says nothing about the traffic per key.

**Moves when the node count changes.** If the partition is $h(k) \bmod N$ for $N$ nodes, going to $N + 1$ nodes keeps a record in place only when $h(k) \bmod N = h(k) \bmod (N+1)$. By the Chinese remainder theorem, for $h(k)$ uniform over a multiple of $N(N+1)$, this has probability $1/(N+1)$, so the fraction $N/(N+1)$ of the records moves. With $P$ fixed partitions and ADD-NODE, the new node takes about $P/(N+1)$ partitions and only their records move, about the fraction $1/(N+1)$. No scheme that keeps the nodes equal can move less, because the new node must end up with $1/(N+1)$ of the records.

**Queries.** A point query touches 1 partition. A range query on the key touches all $P$ partitions, because the hash destroys the order, unless the range is known to be small enough to list its keys. A query on another attribute touches all partitions under any partitioning by key.

## Classic examples

**Records over 8 partitions.** Hash the keys user0 to user99999 with 64-bit BLAKE2b into $P = 8$ partitions. The partitions hold between 12,316 and 12,657 records, against a mean of 12,500 and a standard deviation of about 105. The thousand keys user1000 to user1999, which are adjacent in key order, fall in all 8 partitions.

**Rebalancing from 4 to 5 nodes.** With partition $= h(k) \bmod N$, going from 4 to 5 nodes moves 79,832 of the 100,000 records; the theory says $4/5$. With 64 fixed partitions, 16 on each of the 4 nodes, the new node takes 3 partitions from each old node: 12 partitions and 18,420 records move. The nodes then hold 13, 13, 13, 13 and 12 partitions, and between 18,420 and 20,595 records. The minimum possible move is $100{,}000 / 5 = 20{,}000$ records for exact balance; the 64 partitions cannot be split into five equal groups, so the new node is a little light.

**Redis Cluster.** The key space has 16,384 hash slots, and a key's slot is $\mathrm{CRC16}(\text{key}) \bmod 16384$, with the XMODEM variant of CRC-16. The key foo is in slot 12182. Each master node owns a set of slots, and resharding moves slots between nodes. A *hash tag* hashes only the part of the key between the first `{` and the next `}`, so `{user1000}.following` and `{user1000}.followers` are both in slot 3443, the slot of user1000, and an operation on both keys runs on one node.

**Elasticsearch.** A document goes to shard $\mathrm{hash}(\text{routing}) \bmod P$, where the routing value is the document ID by default and $P$ is the number of primary shards of the index. Since $P$ is in the formula, the number of primary shards is set when the index is created; changing it means a split or shrink by an allowed factor, or a reindex.

**Parallel joins.** A parallel database hash partitions both relations of an equi-join on the join attribute, with the same function and the same $P$, so that matching tuples meet in the same partition. DeWitt and Gray (1992) describe this with round-robin and range partitioning as the three basic ways to spread a relation. The local join in each partition is then a [hash join](/hash-join/), and the [Grace hash join](/grace-hash-join/) applies the same split on one machine to make the partitions fit in memory.

## Variations

- **A fixed number of partitions.** Choose $P$ much larger than the number of nodes, for example 16,384 slots in Redis Cluster, and move whole partitions on a change. This is the most common form. The cost is a map of $P$ entries that all clients must learn.
- **Consistent hashing.** Put nodes and keys on a ring, as in [consistent hashing](/consistent-hashing/), or use [rendezvous hashing](/rendezvous-hashing/) or [jump consistent hash](/jump-consistent-hash/). Then there is no partition map to keep, and a change of one node moves about $1/N$ of the keys. With [virtual nodes](/virtual-nodes/), each virtual node is in effect a partition.
- **Hash ranges.** Partition the hash values into ranges, as [range partitioning](/range-partitioning/) does with keys, and split a range that grows too big. The number of partitions then grows with the data.
- **Compound keys.** Hash only the first part of a key and sort by the rest inside the partition. All rows of one user are then in one partition, in order, and a range scan within one user touches one partition. Redis hash tags are a form of this.
- **Salting.** Append a small random number to a hot key and spread its records over several partitions; reads must then ask all of them. See [load skew](/load-skew/).

## Pitfalls

- **Partitions tied to the node count.** $h(k) \bmod N$ moves about $N/(N+1)$ of the data when a node is added. Use fixed partitions or a consistent hash.
- **A weak hash.** With integer keys and $h(k) = k$, keys that are all multiples of 4 use only partitions 0 and 4 of 8. Some language runtimes hash small integers to themselves, so the default hash code is not a partitioning hash.
- **A hash that differs between clients.** All clients and servers must compute the same function. A hash that is seeded per process, such as the string hash of several language runtimes, sends the same key to different partitions in different processes.
- **Range queries.** A range scan on the partition key becomes a query to every partition, and its latency is that of the slowest partition. If range scans matter, use range partitioning or a compound key.
- **Hot keys.** All records and all requests of one key go to one partition, so even balance of keys does not mean even balance of load.
- **Too few partitions.** With $P$ fixed, a data set can never use more than $P$ nodes, and $P$ that is not a multiple of the node count leaves some nodes with one more partition.

## Exercises

1. Show that with $h(k) \bmod N$, going from $N$ to $2N$ nodes moves exactly half of the records, if $h(k)$ is uniform over a multiple of $2N$. Which records move?
2. A data set has $m = 10^6$ distinct keys and $P = 100$ partitions. Estimate the standard deviation of a partition's size, and the size of the largest partition with the normal approximation.
3. Two tables are hash partitioned on the join key with $P = 64$ and $P = 48$. Explain why a join cannot run partition by partition, and how many partitions of the second table each partition of the first must meet if both use $h(k) \bmod P$.
4. A store uses 1,024 fixed partitions over 10 nodes. Give the largest and smallest number of partitions per node, and the fraction of data that moves when an 11th node joins and takes partitions evenly from the others.

## References
