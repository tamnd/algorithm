# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/cuda-programming-model/.

import random

from cuda_programming_model import one_kernel_sum, two_kernel_sum, vec_add


def test_vector_add_covers_every_index_once():
    rng = random.Random(3)
    for n in (0, 1, 2, 255, 256, 257, 1000):
        for threads in (32, 128, 256):
            a = [rng.randrange(-99, 99) for _ in range(n)]
            b = [rng.randrange(-99, 99) for _ in range(n)]
            c, ran = vec_add(a, b, threads)
            assert c == [x + y for x, y in zip(a, b)]
            assert ran == -(-n // threads) * threads  # the guard idles ran - n threads
            assert ran - n < threads


def test_two_launches_give_the_sum_for_every_block_order():
    rng = random.Random(4)
    for n in (0, 1, 63, 64, 65, 300):
        x = [rng.randrange(-1000, 1000) for _ in range(n)]
        blocks = max(1, -(-n // 64))
        for _ in range(3):
            order = [(b, 0, 0) for b in range(blocks)]
            rng.shuffle(order)
            assert two_kernel_sum(x, 64, order) == sum(x)


def test_one_launch_has_no_barrier_across_blocks():
    rng = random.Random(5)
    x = [rng.randrange(1, 1000) for _ in range(300)]
    blocks = 5
    first = [(0, 0, 0)] + [(b, 0, 0) for b in range(1, blocks)]
    last = [(b, 0, 0) for b in range(1, blocks)] + [(0, 0, 0)]
    assert one_kernel_sum(x, 64, last) == sum(x)  # correct only by luck of the order
    assert one_kernel_sum(x, 64, first) == sum(x[:64])  # block 0 sees only its own sum
