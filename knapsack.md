# The Complete Knapsack Master Guide — 0/1, Unbounded & Beyond (Interview Prep)

> Goal: after this guide you should be able to recognize **any** knapsack-family LeetCode problem in <30 seconds, pick the correct template, and write it bug-free.

---

## Part 1 — Foundations

### 1.1 Why LeetCode 2915 Is 0/1 Knapsack

Three direct matches to the pattern:

1. **Item Selection (Include/Exclude):** For each number, a binary choice — include it or not. Each index is used at most once.
2. **Fixed Capacity Constraint:** The total sum must not exceed `target` (weight capacity).
3. **Maximization Objective:** Maximize the **count** of chosen items. Each item contributes weight `nums[i]` toward the sum and value `1` toward the answer.

> **Note:** LC 2915 says "sum **at most** target" → answer is `max(dp[0..target])`, not `dp[target]`. The strict Subset-Sum variant returns `dp[target]` (or -1 when unreachable).

### 1.2 General DP signals

- **Optimal substructure + overlapping subproblems:** the answer to a large input reuses answers to smaller ones (to reach sum 9 with item 5, you need the best answer for sum 4).
- **Sequential binary choices:** include/exclude, take/skip.
- **Optimization/counting keywords:** "maximum length", "minimum cost", "number of ways", "is it possible to form..."

### 1.3 The Two Families

| Feature | 0/1 Knapsack | Unbounded Knapsack |
| --- | --- | --- |
| Item frequency | at most **once** | **infinitely** many times |
| Key keywords | subsequence, subsets, partition | denominations, change, cut rod, infinite supply |
| Inner loop direction | **backwards** (`target → num`) | **forwards** (`num → target`) |
| Why | backwards prevents reusing the current item in the same pass | forwards lets updated low states feed higher states (reuse) |
| Classic problems | Partition Equal Subset Sum, Target Sum, LC 2915 | Coin Change, Coin Change II, Rod Cutting |

### 1.4 Worked Example: `nums = [1,2,3,4]`, `target = 4` (0/1, exact sum, max count)

`dp[j]` = max items forming exact sum `j`. Start: `dp = [0, -1, -1, -1, -1]`.

- After `num = 1` (j = 4 → 1): `dp = [0, 1, -1, -1, -1]`
- After `num = 2` (j = 4 → 2): `dp = [0, 1, 1, 2, -1]`
- After `num = 3` (j = 4 → 3): `dp = [0, 1, 1, 2, 2]`
- After `num = 4` (j = 4 → 4): `dp = [0, 1, 1, 2, 2]`

Answer `dp[4] = 2` (e.g., `[1,3]`).

**Contrast — same input, unbounded (forwards):** after `num = 1`, `dp = [0,1,2,3,4]`; you can form sum 4 with four 1's — reuse happened.

---

## Part 2 — The Six Core Templates (Java)

### 2.1 Universal State/Sentinel Rules

| Goal | dp[0] | Sentinel | Update |
| --- | --- | --- | --- |
| Max count / max value | 0 | -1 (or MIN_VALUE) | `dp[j] = max(dp[j], dp[j-w] + value)` |
| Boolean feasibility | true | false | `dp[j] \|= dp[j-w]` |
| Count ways | 1 | 0 | `dp[j] += dp[j-w]` |
| Min items | 0 | amount + 1 (> any answer) | `dp[j] = min(dp[j], dp[j-w] + 1)` |

Rule: **the sentinel must be a value impossible for a valid answer**, and guard updates when using -1/MIN_VALUE.

### 2.2 Template A — 0/1 Max Value (generic `weights[] + values[]`)

The base of the family. Not a LeetCode problem by itself — every 0/1 variant is a special case of this.

```java
public int knapsack01(int[] weights, int[] values, int capacity) {
    int[] dp = new int[capacity + 1];
    // dp[0] = 0 is implicit; all states default to "value 0" (reachable via empty set)

    for (int i = 0; i < weights.length; i++) {
        for (int j = capacity; j >= weights[i]; j--) {   // BACKWARDS: each item once
            dp[j] = Math.max(dp[j], dp[j - weights[i]] + values[i]);
        }
    }
    return dp[capacity];
}
```

### 2.3 Template B — 0/1 Max Count (LC 2915)

```java
public int lengthOfLongestSubsequence(List<Integer> nums, int target) {
    int[] dp = new int[target + 1];
    Arrays.fill(dp, -1);                 // -1 = unreachable
    dp[0] = 0;

    for (int num : nums) {
        for (int j = target; j >= num; j--) {          // BACKWARDS
            if (dp[j - num] != -1) {
                dp[j] = Math.max(dp[j], dp[j - num] + 1);
            }
        }
    }
    int ans = 0;                          // "at most target": best over all reachable sums
    for (int v : dp) ans = Math.max(ans, v);
    return ans;
}
```

### 2.4 Template C — 0/1 Boolean Feasibility (LC 416 Partition Equal Subset Sum)

```java
public boolean canPartition(int[] nums) {
    int sum = 0;
    for (int n : nums) sum += n;
    if (sum % 2 != 0) return false;
    int target = sum / 2;

    boolean[] dp = new boolean[target + 1];
    dp[0] = true;

    for (int num : nums) {
        for (int j = target; j >= num; j--) {          // BACKWARDS
            dp[j] = dp[j] || dp[j - num];
        }
    }
    return dp[target];
}
```

### 2.5 Template D — 0/1 Count Ways (LC 494 Target Sum)

Reduce "+/-" assignment to: count subsets whose sum = `(total + target) / 2`.

```java
public int findTargetSumWays(int[] nums, int target) {
    int total = 0;
    for (int n : nums) total += n;
    if ((total + target) % 2 != 0 || total < Math.abs(target)) return 0;
    int t = (total + target) / 2;

    int[] dp = new int[t + 1];
    dp[0] = 1;

    for (int num : nums) {
        for (int j = t; j >= num; j--) {               // BACKWARDS: each num once
            dp[j] += dp[j - num];
        }
    }
    return dp[t];
}
```

### 2.6 Template E — Unbounded Min Items (LC 322 Coin Change)

```java
public int coinChange(int[] coins, int amount) {
    int[] dp = new int[amount + 1];
    Arrays.fill(dp, amount + 1);         // sentinel = "infinity"
    dp[0] = 0;

    for (int coin : coins) {
        for (int j = coin; j <= amount; j++) {         // FORWARDS: reuse allowed
            dp[j] = Math.min(dp[j], dp[j - coin] + 1);
        }
    }
    return dp[amount] > amount ? -1 : dp[amount];
}
```

### 2.7 Template F — Unbounded Count, COMBINATIONS (LC 518 Coin Change II)

```java
public int change(int amount, int[] coins) {
    int[] dp = new int[amount + 1];
    dp[0] = 1;

    for (int coin : coins) {             // items OUTER -> order does NOT matter
        for (int j = coin; j <= amount; j++) {     // FORWARDS
            dp[j] += dp[j - coin];
        }
    }
    return dp[amount];
}
```

### 2.8 Template G — Unbounded Count, PERMUTATIONS (LC 377 Combination Sum IV)

```java
public int combinationSum4(int[] nums, int target) {
    int[] dp = new int[target + 1];
    dp[0] = 1;

    for (int j = 1; j <= target; j++) {  // weight OUTER -> order MATTERS
        for (int num : nums) {           // items INNER
            if (j >= num) {
                dp[j] += dp[j - num];
            }
        }
    }
    return dp[target];
}
```

**Why the flip:** items-outer "locks in" earlier coins, so `1+2` and `2+1` collapse into one combination. Weight-outer aggregates *every* way to reach a smaller sum plus *any* coin, so every ordering is counted separately.

Dry-run `amount=3, coins=[1,2]`: combinations = 2 (`[1,1,1]`, `[1,2]`); permutations = 3 (adds `[2,1]`).

### 2.9 Template H — Unbounded Max Value (LC 1449 Form Largest Integer With Digits That Add up to Target)

Value isn't "count" anymore — each item has its own score; maximize total score.

```java
// digits 1..9, digit d has weight d and value d; also maximize number of digits -> lexicographically largest
public String largestNumber(int[] cost, int target) {
    // dp[j] = max number of digits summing to j, or MIN_VALUE if unreachable
    int[] dp = new int[target + 1];
    Arrays.fill(dp, Integer.MIN_VALUE);
    dp[0] = 0;

    for (int j = 1; j <= target; j++) {              // FORWARDS (unbounded)
        for (int d = 1; d <= 9; d++) {               // try every digit
            if (j >= cost[d - 1]) {
                dp[j] = Math.max(dp[j], dp[j - cost[d - 1]] + 1);
            }
        }
    }
    // then greedily reconstruct the largest number from dp
    // (reconstruction omitted for brevity)
    return dp[target] < 0 ? "0" : reconstruct(cost, target, dp);
}
```

### 2.10 Template I — 2D Knapsack (LC 474 Ones and Zeroes)

Two capacity constraints (zeros and ones). Add one inner loop per dimension; both backwards (0/1).

```java
public int findMaxForm(String[] strs, int m, int n) {
    int[][] dp = new int[m + 1][n + 1];              // dp[zeros][ones] = max strings

    for (String s : strs) {
        int zeros = 0, ones = 0;
        for (char c : s.toCharArray()) {
            if (c == '0') zeros++; else ones++;
        }
        for (int i = m; i >= zeros; i--) {           // BACKWARDS
            for (int j = n; j >= ones; j--) {        // BACKWARDS
                dp[i][j] = Math.max(dp[i][j], dp[i - zeros][j - ones] + 1);
            }
        }
    }
    return dp[m][n];
}
```

### 2.11 Template J — Bounded / Group Knapsack (LC 1155 Number of Dice Rolls With Target Sum)

Each "item group" (die) must be used exactly once, choosing one value from 1..k. Generalized: for each item with limit `k` copies, either loop copies or add a dimension.

```java
// Ways to roll n dice, each 1..k, summing to target
public int numRollsToTarget(int n, int k, int target) {
    int MOD = 1_000_000_007;
    int[] dp = new int[target + 1];
    dp[0] = 1;

    for (int die = 0; die < n; die++) {              // each die used exactly once
        int[] next = new int[target + 1];
        for (int j = 0; j <= target; j++) {
            if (dp[j] == 0) continue;
            for (int face = 1; face <= k && j + face <= target; face++) {
                next[j + face] = (next[j + face] + dp[j]) % MOD;
            }
        }
        dp = next;
    }
    return dp[target];
}
```

---

## Part 3 — The Master Decision Flowchart

```
Is it a Knapsack problem?
│
├─ Can items be used only ONCE? ───────────────────── 0/1 (inner loop BACKWARDS)
│   ├─ Max value/count  → Template A/B   (dp[j] = max(dp[j], dp[j-w] + v))
│   ├─ Feasibility      → Template C     (dp[j] |= dp[j-w])
│   └─ Count ways       → Template D     (dp[j] += dp[j-w])
│
├─ Can items be REUSED infinitely? ────────────────── Unbounded (inner loop FORWARDS)
│   ├─ Min items        → Template E     (dp[j] = min(...))
│   ├─ Max value        → Template H     (dp[j] = max(...))
│   └─ Count ways
│       ├─ Combinations (order irrelevant) → Template F (items OUTER)
│       └─ Permutations (order matters)    → Template G (weight OUTER)
│
└─ Special shapes
    ├─ Two capacities (e.g. zeros+ones) → Template I (2D array, both loops backwards)
    └─ Groups / copies limit            → Template J (extra loop or dimension)
```

---

## Part 4 — Master Table: Every Knapsack-Style LeetCode Problem

### 4.1 0/1 Knapsack family

| # | Problem | Goal | Template | Direction | Difficulty | Key insight |
|---|---------|------|----------|-----------|-----------|-------------|
| 416 | Partition Equal Subset Sum | boolean | C | backwards | Medium | subset sum = total/2 |
| 494 | Target Sum | count ways | D | backwards | Medium | map "+/-" to subset sum `(total+target)/2` |
| 1049 | Last Stone Weight II | min residual | C-variant | backwards | Medium | partition into two groups minimizing difference |
| 2915 | Longest Subseq With Sum ≤ Target | max count | B | backwards | Medium | answer = max(dp[0..target]) |
| 698 | Partition to K Equal Sum Subsets | boolean (k groups) | C + backtrack | — | Medium | pruning + memo on used-bitmask |
| 473 | Matchsticks to Square | boolean (4 groups) | C + backtrack | — | Medium | same as 698 with k=4 |
| 2787 | Ways to Express Integer as Sum of Powers | count ways | D | backwards | Medium | each power value used at most once |
| 879 | Profitable Schemes | count ways, 2 constraints | D 2D | backwards | Hard | dp[members][profit], items backwards |
| 956 | Tallest Billboard | max diff balance | C-variant | backwards | Hard | dp[diff] = max taller height |
| 1125 | Smallest Sufficient Team | min team size | A, skills as bitmask | backwards | Hard | each person = item, skill mask = "weight" |
| 1255 | Max Score Words Formed by Letters | max score | A | backwards | Hard | word cost = letter counts; subset of words |
| 3180 | Maximum Total Reward Using Operations I/II | max value | A | backwards | Medium/Hard | each reward used once; LC II needs optimization |
| 343* | Integer Break | max product | unbounded-style | forwards | Medium | reuse allowed, max product not sum |

### 4.2 Unbounded Knapsack family

| # | Problem | Goal | Template | Direction | Difficulty | Key insight |
|---|---------|------|----------|-----------|-----------|-------------|
| 322 | Coin Change | min items | E | forwards | Medium | classic min unbounded |
| 518 | Coin Change II | count combinations | F | forwards, items outer | Medium | order irrelevant |
| 377 | Combination Sum IV | count permutations | G | forwards, weight outer | Medium | order matters; 32-bit overflow → use long |
| 279 | Perfect Squares | min items | E | forwards | Medium | coins = squares ≤ n |
| 1449 | Form Largest Integer With Digits That Add up to Target | max value | H | forwards | Hard | then reconstruct greedily for lexicographic max |

### 4.3 Special shapes

| # | Problem | Shape | Template | Difficulty | Key insight |
|---|---------|-------|----------|-----------|-------------|
| 474 | Ones and Zeroes | 2D 0/1 | I | Medium | zeros and ones are two capacities |
| 1155 | Number of Dice Rolls With Target Sum | bounded groups | J | Medium | each die = group, face = choice; mod 1e9+7 |

---

## Part 5 — Complexity

All 1D templates: **Time O(n × target)**, **Space O(target)**.
2D (LC 474): **O(n × m × k)**.
Bounded/group (LC 1155): **O(n × target × k)**.

If `target` is astronomically large (e.g., 1e9), the DP is infeasible — switch to meet-in-the-middle, math, or greedy.

---

## Part 6 — Common Pitfalls Checklist

- [ ] Forgetting base case: `dp[0]` = 0 (best) / true (possible) / 1 (ways).
- [ ] 0/1 with **forwards** inner loop → silently becomes unbounded (coin reuse).
- [ ] Off-by-one: iterate j down **to** `num` (inclusive) in 0/1; from `coin` (inclusive) in unbounded.
- [ ] Sentinel confusion: guard `dp[j-w] != -1` before combining when using -1/MIN_VALUE.
- [ ] "At most target" problems: return `max(dp[0..target])`, not `dp[target]`.
- [ ] Counting with wrong loop order: items-outer = combinations, weight-outer = permutations.
- [ ] Integer overflow in counting (LC 377): use `long` or check against `Integer.MAX_VALUE`.
- [ ] Mod arithmetic: apply `% MOD` on **every** addition, not just at the end (LC 1155, 879, 518-style big counts).
- [ ] 2D knapsack: both inner loops backwards.
- [ ] Reconstruction problems (LC 1449): max-count DP first, greedy reconstruction second.

---

## Part 7 — One-Line Memory Hooks

- **0/1 = backwards** (once only); **unbounded = forwards** (reuse freely).
- **dp[0]:** 0 for "best", 1 for "ways", true for "possible".
- **Counting?** Items outer = combinations; weight outer = permutations.
- **Sentinel** = a value impossible for a valid answer.
- **"At most" target → max over dp[0..target]; "exact" target → dp[target].**
- **Two capacities → 2D dp; limited copies → extra loop/dimension.**
