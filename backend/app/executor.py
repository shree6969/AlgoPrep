"""
Visualization step generators for algorithm problems.
Each function returns a list of VizStep objects.
"""
import time
from app.models import VizStep


# ─── Helper ──────────────────────────────────────────────────────────────────

def _step(num: int, desc: str, data, highlights: dict = None, state: dict = None) -> VizStep:
    return VizStep(
        step_num=num,
        description=desc,
        data=data,
        highlights=highlights or {},
        state=state or {},
    )


# ─── Two Pointers: Container With Most Water ─────────────────────────────────

def two_pointers_container_water(height: list[int]) -> list[VizStep]:
    steps = []
    n = len(height)
    left, right = 0, n - 1
    max_water = 0
    step_num = 0

    steps.append(_step(step_num, f"Initialize: left=0, right={n-1}. Array has {n} bars.",
        data=height,
        highlights={"left": left, "right": right},
        state={"left": left, "right": right, "max_water": 0, "current_water": 0}
    ))

    while left < right:
        step_num += 1
        width = right - left
        water = width * min(height[left], height[right])
        max_water = max(max_water, water)

        steps.append(_step(step_num,
            f"left={left} (h={height[left]}), right={right} (h={height[right]}). "
            f"width={width}, water={water}, max={max_water}",
            data=height,
            highlights={"left": left, "right": right, "water_range": list(range(left, right + 1))},
            state={"left": left, "right": right, "max_water": max_water,
                   "current_water": water, "width": width,
                   "limiting_height": min(height[left], height[right])}
        ))

        if height[left] < height[right]:
            steps.append(_step(step_num,
                f"height[left]={height[left]} < height[right]={height[right]}, move left pointer right",
                data=height,
                highlights={"left": left, "right": right, "moving": left},
                state={"left": left, "right": right, "max_water": max_water, "action": "move_left"}
            ))
            left += 1
        else:
            steps.append(_step(step_num,
                f"height[right]={height[right]} <= height[left]={height[left]}, move right pointer left",
                data=height,
                highlights={"left": left, "right": right, "moving": right},
                state={"left": left, "right": right, "max_water": max_water, "action": "move_right"}
            ))
            right -= 1

    step_num += 1
    steps.append(_step(step_num, f"Pointers met. Maximum water = {max_water}",
        data=height,
        highlights={"result": max_water},
        state={"left": left, "right": right, "max_water": max_water, "done": True}
    ))

    return steps


# ─── Two Pointers: Trapping Rain Water ────────────────────────────────────────

def trapping_rain_water(height: list[int]) -> list[VizStep]:
    steps = []
    n = len(height)
    left, right = 0, n - 1
    max_left = max_right = 0
    water = 0
    step_num = 0

    steps.append(_step(step_num, f"Initialize two pointers. left=0, right={n-1}.",
        data={"height": height, "water_at": [0] * n},
        highlights={"left": 0, "right": n - 1},
        state={"left": 0, "right": n - 1, "total_water": 0, "max_left": 0, "max_right": 0}
    ))

    water_at = [0] * n
    while left < right:
        step_num += 1
        if height[left] <= height[right]:
            if height[left] >= max_left:
                max_left = height[left]
                steps.append(_step(step_num,
                    f"height[{left}]={height[left]} >= max_left={max_left-height[left] if max_left != height[left] else max_left}. Update max_left={max_left}",
                    data={"height": height, "water_at": water_at[:]},
                    highlights={"left": left, "right": right, "active": left},
                    state={"left": left, "right": right, "total_water": water,
                           "max_left": max_left, "max_right": max_right}
                ))
            else:
                trapped = max_left - height[left]
                water += trapped
                water_at[left] = trapped
                steps.append(_step(step_num,
                    f"Trap water at index {left}: max_left({max_left}) - height[{left}]({height[left]}) = {trapped}. Total water = {water}",
                    data={"height": height, "water_at": water_at[:]},
                    highlights={"left": left, "right": right, "filling": left},
                    state={"left": left, "right": right, "total_water": water,
                           "max_left": max_left, "max_right": max_right, "trapped_here": trapped}
                ))
            left += 1
        else:
            if height[right] >= max_right:
                max_right = height[right]
                steps.append(_step(step_num,
                    f"height[{right}]={height[right]} >= max_right. Update max_right={max_right}",
                    data={"height": height, "water_at": water_at[:]},
                    highlights={"left": left, "right": right, "active": right},
                    state={"left": left, "right": right, "total_water": water,
                           "max_left": max_left, "max_right": max_right}
                ))
            else:
                trapped = max_right - height[right]
                water += trapped
                water_at[right] = trapped
                steps.append(_step(step_num,
                    f"Trap water at index {right}: max_right({max_right}) - height[{right}]({height[right]}) = {trapped}. Total water = {water}",
                    data={"height": height, "water_at": water_at[:]},
                    highlights={"left": left, "right": right, "filling": right},
                    state={"left": left, "right": right, "total_water": water,
                           "max_left": max_left, "max_right": max_right, "trapped_here": trapped}
                ))
            right -= 1

    step_num += 1
    steps.append(_step(step_num, f"Done! Total water trapped = {water}",
        data={"height": height, "water_at": water_at},
        highlights={"result": water},
        state={"total_water": water, "done": True}
    ))

    return steps


# ─── Sliding Window: Minimum Window Substring ────────────────────────────────

def sliding_window_min_substr(s: str, t: str) -> list[VizStep]:
    from collections import Counter
    steps = []
    step_num = 0

    need = Counter(t)
    missing = len(t)
    best = ""
    left = 0
    window_counts: dict = {}

    steps.append(_step(step_num, f'Init: s="{s}", t="{t}". Need: {dict(need)}',
        data={"s": list(s), "t": list(t), "window": []},
        highlights={"left": 0, "right": -1},
        state={"left": 0, "right": -1, "missing": missing, "best": ""}
    ))

    for right, c in enumerate(s):
        step_num += 1
        window_counts[c] = window_counts.get(c, 0) + 1
        if need.get(c, 0) > 0 and window_counts[c] <= need[c]:
            missing -= 1

        steps.append(_step(step_num,
            f'Expand: right={right}, char="{c}". missing={missing}',
            data={"s": list(s), "window": list(s[left:right+1])},
            highlights={"left": left, "right": right, "current": right},
            state={"left": left, "right": right, "missing": missing, "best": best, "window_counts": dict(window_counts)}
        ))

        if missing == 0:
            # Shrink
            while window_counts.get(s[left], 0) > need.get(s[left], 0):
                step_num += 1
                steps.append(_step(step_num,
                    f'Shrink: s[{left}]="{s[left]}" is excess, move left',
                    data={"s": list(s), "window": list(s[left:right+1])},
                    highlights={"left": left, "right": right, "shrinking": left},
                    state={"left": left, "right": right, "missing": missing, "best": best}
                ))
                window_counts[s[left]] -= 1
                left += 1

            window = s[left:right + 1]
            if not best or len(window) < len(best):
                best = window
            step_num += 1
            steps.append(_step(step_num,
                f'Valid window: "{window}" (len={len(window)}). Best so far: "{best}"',
                data={"s": list(s), "window": list(window)},
                highlights={"left": left, "right": right, "window_range": list(range(left, right + 1))},
                state={"left": left, "right": right, "missing": missing, "best": best, "valid": True}
            ))
            window_counts[s[left]] = window_counts.get(s[left], 0) - 1
            missing += 1
            left += 1

    step_num += 1
    steps.append(_step(step_num, f'Result: "{best}"',
        data={"s": list(s), "result": list(best)},
        highlights={"result": best},
        state={"best": best, "done": True}
    ))

    return steps


# ─── Binary Search: Search in Rotated Sorted Array ───────────────────────────

def binary_search_rotated(nums: list[int], target: int) -> list[VizStep]:
    steps = []
    step_num = 0
    left, right = 0, len(nums) - 1

    steps.append(_step(step_num, f"Binary search for target={target} in rotated array",
        data=nums,
        highlights={"left": left, "right": right},
        state={"left": left, "right": right, "target": target}
    ))

    while left <= right:
        step_num += 1
        mid = (left + right) // 2
        steps.append(_step(step_num,
            f"left={left}, right={right}, mid={mid}. nums[mid]={nums[mid]}",
            data=nums,
            highlights={"left": left, "right": right, "mid": mid},
            state={"left": left, "right": right, "mid": mid, "target": target}
        ))

        if nums[mid] == target:
            step_num += 1
            steps.append(_step(step_num, f"Found target={target} at index={mid}!",
                data=nums,
                highlights={"found": mid},
                state={"result": mid, "done": True}
            ))
            return steps

        if nums[left] <= nums[mid]:
            step_num += 1
            steps.append(_step(step_num,
                f"Left half [{left}..{mid}] is sorted. nums[left]={nums[left]}, nums[mid]={nums[mid]}",
                data=nums,
                highlights={"left": left, "right": right, "mid": mid, "sorted_half": list(range(left, mid + 1))},
                state={"left": left, "right": right, "mid": mid, "sorted": "left"}
            ))
            if nums[left] <= target < nums[mid]:
                right = mid - 1
                steps.append(_step(step_num, f"Target in left half, set right={right}", data=nums,
                    highlights={"left": left, "right": right}, state={"left": left, "right": right}))
            else:
                left = mid + 1
                steps.append(_step(step_num, f"Target in right half, set left={left}", data=nums,
                    highlights={"left": left, "right": right}, state={"left": left, "right": right}))
        else:
            step_num += 1
            steps.append(_step(step_num,
                f"Right half [{mid}..{right}] is sorted. nums[mid]={nums[mid]}, nums[right]={nums[right]}",
                data=nums,
                highlights={"left": left, "right": right, "mid": mid, "sorted_half": list(range(mid, right + 1))},
                state={"left": left, "right": right, "mid": mid, "sorted": "right"}
            ))
            if nums[mid] < target <= nums[right]:
                left = mid + 1
                steps.append(_step(step_num, f"Target in right sorted half, set left={left}", data=nums,
                    highlights={"left": left, "right": right}, state={"left": left, "right": right}))
            else:
                right = mid - 1
                steps.append(_step(step_num, f"Target in left part, set right={right}", data=nums,
                    highlights={"left": left, "right": right}, state={"left": left, "right": right}))

    step_num += 1
    steps.append(_step(step_num, f"Target={target} not found. Return -1.",
        data=nums, highlights={}, state={"result": -1, "done": True}
    ))
    return steps


# ─── DP: Longest Increasing Subsequence ──────────────────────────────────────

def longest_increasing_subseq(nums: list[int]) -> list[VizStep]:
    steps = []
    step_num = 0
    n = len(nums)
    dp = [1] * n

    steps.append(_step(step_num, f"Initialize dp array. All values = 1 (each element is LIS of length 1).",
        data={"nums": nums, "dp": dp[:]},
        highlights={},
        state={"dp": dp[:], "max_lis": 1}
    ))

    for i in range(1, n):
        for j in range(i):
            step_num += 1
            if nums[j] < nums[i]:
                new_val = dp[j] + 1
                if new_val > dp[i]:
                    dp[i] = new_val
                    steps.append(_step(step_num,
                        f"nums[{j}]={nums[j]} < nums[{i}]={nums[i]}. dp[{i}] = dp[{j}]+1 = {dp[i]}",
                        data={"nums": nums, "dp": dp[:]},
                        highlights={"comparing": j, "current": i, "updated": i},
                        state={"i": i, "j": j, "dp": dp[:], "max_lis": max(dp)}
                    ))
                else:
                    steps.append(_step(step_num,
                        f"nums[{j}]={nums[j]} < nums[{i}]={nums[i]}, but dp[{j}]+1={new_val} <= dp[{i}]={dp[i]}, no update",
                        data={"nums": nums, "dp": dp[:]},
                        highlights={"comparing": j, "current": i},
                        state={"i": i, "j": j, "dp": dp[:], "max_lis": max(dp)}
                    ))
            else:
                steps.append(_step(step_num,
                    f"nums[{j}]={nums[j]} >= nums[{i}]={nums[i]}, skip",
                    data={"nums": nums, "dp": dp[:]},
                    highlights={"comparing": j, "current": i, "skipped": j},
                    state={"i": i, "j": j, "dp": dp[:]}
                ))

    result = max(dp)
    step_num += 1
    steps.append(_step(step_num, f"Done! LIS length = {result}. dp = {dp}",
        data={"nums": nums, "dp": dp},
        highlights={"result_idx": dp.index(result)},
        state={"dp": dp, "max_lis": result, "done": True}
    ))

    return steps


# ─── DP: Coin Change ──────────────────────────────────────────────────────────

def coin_change(coins: list[int], amount: int) -> list[VizStep]:
    steps = []
    step_num = 0
    INF = float('inf')
    dp = [INF] * (amount + 1)
    dp[0] = 0

    steps.append(_step(step_num, f"Init dp[0..{amount}] = ∞. dp[0] = 0 (base case). coins={coins}",
        data={"dp": [x if x != INF else -1 for x in dp], "coins": coins, "amount": amount},
        highlights={"base": 0},
        state={"dp": dp[:], "coins": coins}
    ))

    for i in range(1, amount + 1):
        for coin in coins:
            if coin <= i and dp[i - coin] + 1 < dp[i]:
                step_num += 1
                old = dp[i]
                dp[i] = dp[i - coin] + 1
                steps.append(_step(step_num,
                    f"dp[{i}]: coin={coin}, dp[{i}-{coin}]+1 = dp[{i-coin}]+1 = {dp[i]} {'(improved from '+str(old)+')' if old != INF else '(first update)'}",
                    data={"dp": [x if x != INF else -1 for x in dp], "coins": coins, "amount": amount},
                    highlights={"current": i, "source": i - coin, "active_coin": coin},
                    state={"i": i, "coin": coin, "dp": [x if x != INF else -1 for x in dp]}
                ))

    result = dp[amount] if dp[amount] != INF else -1
    step_num += 1
    steps.append(_step(step_num, f"Result: dp[{amount}] = {result}",
        data={"dp": [x if x != INF else -1 for x in dp], "coins": coins, "amount": amount},
        highlights={"result": amount},
        state={"result": result, "done": True}
    ))

    return steps


# ─── DP 2D: Edit Distance ─────────────────────────────────────────────────────

def edit_distance(word1: str, word2: str) -> list[VizStep]:
    steps = []
    step_num = 0
    m, n = len(word1), len(word2)
    dp = [[0] * (n + 1) for _ in range(m + 1)]

    # Init
    for i in range(m + 1):
        dp[i][0] = i
    for j in range(n + 1):
        dp[0][j] = j

    steps.append(_step(step_num,
        f'Init DP table for word1="{word1}", word2="{word2}". Base cases filled.',
        data={"dp": [row[:] for row in dp], "word1": word1, "word2": word2},
        highlights={"row": 0, "col": 0},
        state={"word1": word1, "word2": word2}
    ))

    for i in range(1, m + 1):
        for j in range(1, n + 1):
            step_num += 1
            c1, c2 = word1[i - 1], word2[j - 1]
            if c1 == c2:
                dp[i][j] = dp[i - 1][j - 1]
                desc = f'word1[{i-1}]="{c1}" == word2[{j-1}]="{c2}": dp[{i}][{j}] = dp[{i-1}][{j-1}] = {dp[i][j]}'
            else:
                dp[i][j] = 1 + min(dp[i - 1][j], dp[i][j - 1], dp[i - 1][j - 1])
                best = min(dp[i-1][j], dp[i][j-1], dp[i-1][j-1])
                desc = f'word1[{i-1}]="{c1}" != word2[{j-1}]="{c2}": dp[{i}][{j}] = 1 + min({dp[i-1][j]},{dp[i][j-1]},{dp[i-1][j-1]}) = {dp[i][j]}'

            steps.append(_step(step_num, desc,
                data={"dp": [row[:] for row in dp], "word1": word1, "word2": word2},
                highlights={"current_row": i, "current_col": j,
                             "top": (i-1, j), "left": (i, j-1), "diag": (i-1, j-1)},
                state={"i": i, "j": j, "c1": c1, "c2": c2, "value": dp[i][j]}
            ))

    step_num += 1
    steps.append(_step(step_num, f"Edit distance between '{word1}' and '{word2}' = {dp[m][n]}",
        data={"dp": [row[:] for row in dp], "word1": word1, "word2": word2},
        highlights={"result": (m, n)},
        state={"result": dp[m][n], "done": True}
    ))

    return steps


# ─── Monotonic Stack: Largest Rectangle in Histogram ────────────────────────

def largest_rect_histogram(heights: list[int]) -> list[VizStep]:
    steps = []
    step_num = 0
    stack: list[int] = []
    max_area = 0
    n = len(heights)
    extended = heights + [0]

    steps.append(_step(step_num, f"Init monotonic stack. heights={heights}",
        data={"heights": heights, "stack": [], "max_area": 0},
        highlights={},
        state={"stack": [], "max_area": 0}
    ))

    for i, h in enumerate(extended):
        start = i
        while stack and extended[stack[-1]] > h:
            step_num += 1
            idx = stack.pop()
            width = i - (stack[-1] if stack else -1) - 1
            area = extended[idx] * width
            max_area = max(max_area, area)
            steps.append(_step(step_num,
                f"Pop idx={idx} (h={extended[idx]}). Width from {stack[-1]+1 if stack else 0} to {i-1} = {width}. Area={area}. Max={max_area}",
                data={"heights": heights, "stack": stack[:], "max_area": max_area,
                      "rect": {"left": stack[-1]+1 if stack else 0, "right": i-1, "height": extended[idx]}},
                highlights={"popped": idx, "bar_range": list(range(stack[-1]+1 if stack else 0, i)),
                             "stack_top": stack[-1] if stack else -1},
                state={"stack": stack[:], "max_area": max_area, "area": area, "i": i}
            ))

        step_num += 1
        if i < n:
            stack.append(i)
            steps.append(_step(step_num, f"Push index {i} (h={h}) onto stack. stack={stack}",
                data={"heights": heights, "stack": stack[:], "max_area": max_area},
                highlights={"current": i, "stack_indices": stack[:]},
                state={"stack": stack[:], "max_area": max_area, "i": i}
            ))

    step_num += 1
    steps.append(_step(step_num, f"Done! Largest rectangle area = {max_area}",
        data={"heights": heights, "max_area": max_area},
        highlights={"result": max_area},
        state={"max_area": max_area, "done": True}
    ))

    return steps


# ─── Intervals: Merge Intervals ──────────────────────────────────────────────

def merge_intervals(intervals: list[list[int]]) -> list[VizStep]:
    steps = []
    step_num = 0

    steps.append(_step(step_num, f"Input intervals: {intervals}. Sorting by start time.",
        data={"intervals": intervals, "merged": []},
        highlights={},
        state={"merged": []}
    ))

    intervals = sorted(intervals, key=lambda x: x[0])
    step_num += 1
    steps.append(_step(step_num, f"Sorted: {intervals}",
        data={"intervals": intervals, "merged": []},
        highlights={"sorted": True},
        state={"merged": []}
    ))

    merged = [intervals[0][:]]
    step_num += 1
    steps.append(_step(step_num, f"Add first interval {intervals[0]} to merged list.",
        data={"intervals": intervals, "merged": [merged[0][:]]},
        highlights={"current": 0, "merged_top": 0},
        state={"merged": [merged[0][:]]}
    ))

    for i in range(1, len(intervals)):
        cur = intervals[i]
        last = merged[-1]
        step_num += 1
        if cur[0] <= last[1]:
            old_end = last[1]
            last[1] = max(last[1], cur[1])
            steps.append(_step(step_num,
                f"Overlap: [{cur[0]},{cur[1]}] overlaps [{last[0]},{old_end}]. Merge → [{last[0]},{last[1]}]",
                data={"intervals": intervals, "merged": [m[:] for m in merged]},
                highlights={"current": i, "merged_top": len(merged) - 1, "overlap": True},
                state={"merged": [m[:] for m in merged], "action": "merge"}
            ))
        else:
            merged.append(cur[:])
            steps.append(_step(step_num,
                f"No overlap: [{cur[0]},{cur[1]}] starts after [{last[0]},{last[1]}] ends. Add new.",
                data={"intervals": intervals, "merged": [m[:] for m in merged]},
                highlights={"current": i, "merged_top": len(merged) - 1, "overlap": False},
                state={"merged": [m[:] for m in merged], "action": "add_new"}
            ))

    step_num += 1
    steps.append(_step(step_num, f"Done! Merged intervals: {merged}",
        data={"intervals": intervals, "merged": merged},
        highlights={"result": True},
        state={"merged": merged, "done": True}
    ))

    return steps


# ─── Backtracking: N-Queens ───────────────────────────────────────────────────

def n_queens_solver(n: int) -> list[VizStep]:
    steps = []
    step_num = 0
    cols: set[int] = set()
    diag1: set[int] = set()
    diag2: set[int] = set()
    board = [[-1] * n for _ in range(n)]  # -1=empty, 0=tried, 1=queen
    solutions = []

    def board_snapshot():
        return [row[:] for row in board]

    steps.append(_step(step_num, f"Init {n}x{n} board. Placing queens row by row.",
        data={"board": board_snapshot(), "n": n},
        highlights={},
        state={"row": 0, "solutions": 0}
    ))

    def backtrack(row: int):
        nonlocal step_num
        if row == n:
            solutions.append(board_snapshot())
            step_num += 1
            steps.append(_step(step_num, f"Solution #{len(solutions)} found!",
                data={"board": board_snapshot(), "n": n},
                highlights={"solution": True},
                state={"solutions": len(solutions), "board": board_snapshot()}
            ))
            return

        for col in range(n):
            if col in cols or (row - col) in diag1 or (row + col) in diag2:
                step_num += 1
                board[row][col] = 0  # tried and failed
                steps.append(_step(step_num, f"Row {row}, col {col}: conflict, skip.",
                    data={"board": board_snapshot(), "n": n},
                    highlights={"conflict": (row, col)},
                    state={"row": row, "col": col, "action": "conflict"}
                ))
                board[row][col] = -1
                continue

            # Place queen
            board[row][col] = 1
            cols.add(col)
            diag1.add(row - col)
            diag2.add(row + col)
            step_num += 1
            steps.append(_step(step_num, f"Place queen at row={row}, col={col}.",
                data={"board": board_snapshot(), "n": n},
                highlights={"placed": (row, col)},
                state={"row": row, "col": col, "action": "place", "queens": list(cols)}
            ))

            backtrack(row + 1)

            # Remove queen
            board[row][col] = -1
            cols.remove(col)
            diag1.remove(row - col)
            diag2.remove(row + col)
            step_num += 1
            steps.append(_step(step_num, f"Backtrack: remove queen from row={row}, col={col}.",
                data={"board": board_snapshot(), "n": n},
                highlights={"removed": (row, col)},
                state={"row": row, "col": col, "action": "backtrack"}
            ))

        # Limit steps to prevent massive output
        if step_num > 200:
            return

    backtrack(0)

    step_num += 1
    steps.append(_step(step_num, f"Done! Found {len(solutions)} solution(s) for {n}-Queens.",
        data={"board": solutions[0] if solutions else board_snapshot(), "n": n, "solutions": len(solutions)},
        highlights={"done": True},
        state={"solutions": len(solutions), "done": True}
    ))

    return steps[:201]  # cap at 200 steps


# ─── DP 2D: Unique Paths ──────────────────────────────────────────────────────

def unique_paths_viz(m: int, n: int) -> list[VizStep]:
    steps = []
    step_num = 0
    dp = [[1] * n for _ in range(m)]

    steps.append(_step(step_num, f"Init {m}x{n} grid. First row and column = 1 (only one path).",
        data={"dp": [row[:] for row in dp], "m": m, "n": n},
        highlights={"row": 0, "col": 0},
        state={"m": m, "n": n}
    ))

    for i in range(1, m):
        for j in range(1, n):
            step_num += 1
            dp[i][j] = dp[i - 1][j] + dp[i][j - 1]
            steps.append(_step(step_num,
                f"dp[{i}][{j}] = dp[{i-1}][{j}]({dp[i-1][j]}) + dp[{i}][{j-1}]({dp[i][j-1]}) = {dp[i][j]}",
                data={"dp": [row[:] for row in dp], "m": m, "n": n},
                highlights={"current": (i, j), "top": (i-1, j), "left": (i, j-1)},
                state={"i": i, "j": j, "value": dp[i][j]}
            ))

    step_num += 1
    steps.append(_step(step_num, f"Result: dp[{m-1}][{n-1}] = {dp[m-1][n-1]} unique paths.",
        data={"dp": [row[:] for row in dp], "m": m, "n": n},
        highlights={"result": (m-1, n-1)},
        state={"result": dp[m-1][n-1], "done": True}
    ))

    return steps


# ─── Dispatch: run visualization for a problem ───────────────────────────────

def execute_problem(problem_id: str, input_data: dict) -> tuple[list[VizStep], str, bool]:
    """Returns (steps, output_string, passed)."""
    t_start = time.time()

    try:
        if problem_id == "container-with-most-water":
            height = input_data.get("height", [1, 8, 6, 2, 5, 4, 8, 3, 7])
            steps = two_pointers_container_water(height)
            # compute result
            left, right = 0, len(height) - 1
            max_w = 0
            while left < right:
                max_w = max(max_w, (right - left) * min(height[left], height[right]))
                if height[left] < height[right]:
                    left += 1
                else:
                    right -= 1
            return steps, str(max_w), True

        elif problem_id == "trapping-rain-water":
            height = input_data.get("height", [0, 1, 0, 2, 1, 0, 1, 3, 2, 1, 2, 1])
            steps = trapping_rain_water(height)
            # compute result
            left, right = 0, len(height) - 1
            ml = mr = w = 0
            while left < right:
                if height[left] <= height[right]:
                    ml = max(ml, height[left])
                    w += ml - height[left]
                    left += 1
                else:
                    mr = max(mr, height[right])
                    w += mr - height[right]
                    right -= 1
            return steps, str(w), True

        elif problem_id == "minimum-window-substring":
            s = input_data.get("s", "ADOBECODEBANC")
            t = input_data.get("t", "ABC")
            steps = sliding_window_min_substr(s, t)
            return steps, steps[-1].state.get("best", ""), True

        elif problem_id == "search-in-rotated-sorted-array":
            nums = input_data.get("nums", [4, 5, 6, 7, 0, 1, 2])
            target = input_data.get("target", 0)
            steps = binary_search_rotated(nums, target)
            result = steps[-1].state.get("result", -1)
            return steps, str(result), True

        elif problem_id == "longest-increasing-subsequence":
            nums = input_data.get("nums", [10, 9, 2, 5, 3, 7, 101, 18])
            steps = longest_increasing_subseq(nums)
            result = steps[-1].state.get("max_lis", 0)
            return steps, str(result), True

        elif problem_id == "coin-change":
            coins = input_data.get("coins", [1, 2, 5])
            amount = input_data.get("amount", 11)
            # Cap amount for visualization
            amount = min(amount, 20)
            steps = coin_change(coins, amount)
            result = steps[-1].state.get("result", -1)
            return steps, str(result), True

        elif problem_id == "edit-distance":
            word1 = input_data.get("word1", "horse")[:8]
            word2 = input_data.get("word2", "ros")[:8]
            steps = edit_distance(word1, word2)
            result = steps[-1].state.get("result", 0)
            return steps, str(result), True

        elif problem_id == "largest-rectangle-in-histogram":
            heights = input_data.get("heights", [2, 1, 5, 6, 2, 3])
            steps = largest_rect_histogram(heights)
            result = steps[-1].state.get("max_area", 0)
            return steps, str(result), True

        elif problem_id == "merge-intervals":
            intervals = input_data.get("intervals", [[1, 3], [2, 6], [8, 10], [15, 18]])
            steps = merge_intervals(intervals)
            result = steps[-1].state.get("merged", [])
            return steps, str(result), True

        elif problem_id == "n-queens":
            n = min(input_data.get("n", 4), 6)  # cap at 6 for viz
            steps = n_queens_solver(n)
            result = steps[-1].state.get("solutions", 0)
            return steps, str(result), True

        elif problem_id == "unique-paths":
            m = min(input_data.get("m", 3), 6)
            n = min(input_data.get("n", 7), 6)
            steps = unique_paths_viz(m, n)
            result = steps[-1].state.get("result", 0)
            return steps, str(result), True

        else:
            # Generic: just return a single "no visualization" step
            steps = [_step(0, f"Visualization not available for this problem. Study the solution code!",
                data=None, highlights={}, state={"message": "no_viz"})]
            return steps, "No visualization available", False

    except Exception as e:
        steps = [_step(0, f"Error during execution: {str(e)}",
            data=None, highlights={}, state={"error": str(e)})]
        return steps, f"Error: {str(e)}", False
