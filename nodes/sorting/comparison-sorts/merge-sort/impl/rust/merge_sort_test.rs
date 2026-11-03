// SPDX-License-Identifier: MIT
// Part of https://algorithm.tamnd.com/merge-sort/. The authors are listed in prov/4MRG7S.jsonl.

use algo_merge_sort::merge_sort;

#[test]
fn example() {
    let mut a = [38, 27, 43, 3, 9, 82, 10];
    merge_sort(&mut a);
    assert_eq!(a, [3, 9, 10, 27, 38, 43, 82]);
}

#[test]
fn stable() {
    #[derive(Clone, Debug)]
    struct K(i32, char);
    impl PartialEq for K {
        fn eq(&self, o: &Self) -> bool {
            self.0 == o.0
        }
    }
    impl Eq for K {}
    impl PartialOrd for K {
        fn partial_cmp(&self, o: &Self) -> Option<std::cmp::Ordering> {
            Some(self.cmp(o))
        }
    }
    impl Ord for K {
        fn cmp(&self, o: &Self) -> std::cmp::Ordering {
            self.0.cmp(&o.0)
        }
    }
    let mut a = vec![K(2, 'a'), K(1, 'b'), K(2, 'c'), K(1, 'd'), K(2, 'e')];
    merge_sort(&mut a);
    let tags: String = a.iter().map(|k| k.1).collect();
    assert_eq!(tags, "bdace");
}

#[test]
fn random_against_std() {
    let mut s: u64 = 2150;
    let mut next = |m: u64| {
        s = s.wrapping_mul(6364136223846793005).wrapping_add(1442695040888963407);
        (s >> 33) % m
    };
    for _ in 0..500 {
        let n = next(61) as usize;
        let a: Vec<i64> = (0..n).map(|_| next(101) as i64 - 50).collect();
        let mut b = a.clone();
        let mut want = a.clone();
        merge_sort(&mut b);
        want.sort();
        assert_eq!(b, want);
    }
}
