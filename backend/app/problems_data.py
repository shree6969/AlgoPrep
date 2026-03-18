from app.models import Problem, Example

PROBLEMS: list[Problem] = [
    # ─── TWO POINTERS ────────────────────────────────────────────────────────────
    Problem(
        id="container-with-most-water",
        title="Container With Most Water",
        difficulty="Medium",
        pattern="Two Pointers",
        companies=["google", "meta", "amazon"],
        description=(
            "You are given an integer array `height` of length `n`. There are `n` vertical lines drawn such that the "
            "two endpoints of the `i`th line are `(i, 0)` and `(i, height[i])`.\n\n"
            "Find two lines that together with the x-axis form a container, such that the container contains the most water.\n\n"
            "Return the maximum amount of water a container can store.\n\n"
            "**Note**: You may not slant the container."
        ),
        examples=[
            Example(input="height = [1,8,6,2,5,4,8,3,7]", output="49",
                    explanation="The above vertical lines are represented by array [1,8,6,2,5,4,8,3,7]. In this case, the max area is 49."),
            Example(input="height = [1,1]", output="1"),
        ],
        constraints=["n == height.length", "2 <= n <= 10^5", "0 <= height[i] <= 10^4"],
        hints=[
            "Use two pointers starting at both ends.",
            "Move the pointer with the smaller height inward.",
            "Track the maximum area at each step.",
        ],
        solution_code="""def maxArea(height):
    left, right = 0, len(height) - 1
    max_water = 0
    while left < right:
        width = right - left
        water = width * min(height[left], height[right])
        max_water = max(max_water, water)
        if height[left] < height[right]:
            left += 1
        else:
            right -= 1
    return max_water""",
        time_complexity="O(n)",
        space_complexity="O(1)",
        viz_type="array",
    ),
    Problem(
        id="trapping-rain-water",
        title="Trapping Rain Water",
        difficulty="Hard",
        pattern="Two Pointers",
        companies=["google", "meta", "amazon", "apple"],
        description=(
            "Given `n` non-negative integers representing an elevation map where the width of each bar is 1, "
            "compute how much water it can trap after raining."
        ),
        examples=[
            Example(input="height = [0,1,0,2,1,0,1,3,2,1,2,1]", output="6",
                    explanation="The elevation map is represented by array [0,1,0,2,1,0,1,3,2,1,2,1]. In this case, 6 units of rain water are being trapped."),
            Example(input="height = [4,2,0,3,2,5]", output="9"),
        ],
        constraints=["n == height.length", "1 <= n <= 2 * 10^4", "0 <= height[i] <= 10^5"],
        hints=[
            "For each position, water trapped = min(max_left, max_right) - height[i].",
            "Use two pointers with max_left and max_right tracking.",
            "Move the pointer where the max is smaller.",
        ],
        solution_code="""def trap(height):
    if not height:
        return 0
    left, right = 0, len(height) - 1
    max_left = max_right = 0
    water = 0
    while left < right:
        if height[left] <= height[right]:
            if height[left] >= max_left:
                max_left = height[left]
            else:
                water += max_left - height[left]
            left += 1
        else:
            if height[right] >= max_right:
                max_right = height[right]
            else:
                water += max_right - height[right]
            right -= 1
    return water""",
        time_complexity="O(n)",
        space_complexity="O(1)",
        viz_type="array",
    ),
    Problem(
        id="3sum",
        title="3Sum",
        difficulty="Medium",
        pattern="Two Pointers",
        companies=["meta", "google", "microsoft"],
        description=(
            "Given an integer array `nums`, return all the triplets `[nums[i], nums[j], nums[k]]` such that "
            "`i != j`, `i != k`, `j != k`, and `nums[i] + nums[j] + nums[k] == 0`.\n\n"
            "Notice that the solution set must not contain duplicate triplets."
        ),
        examples=[
            Example(input="nums = [-1,0,1,2,-1,-4]", output="[[-1,-1,2],[-1,0,1]]"),
            Example(input="nums = [0,1,1]", output="[]"),
            Example(input="nums = [0,0,0]", output="[[0,0,0]]"),
        ],
        constraints=["3 <= nums.length <= 3000", "-10^5 <= nums[i] <= 10^5"],
        hints=[
            "Sort the array first.",
            "For each element, use two pointers to find pairs that sum to its negation.",
            "Skip duplicates to avoid duplicate triplets.",
        ],
        solution_code="""def threeSum(nums):
    nums.sort()
    result = []
    for i in range(len(nums) - 2):
        if i > 0 and nums[i] == nums[i - 1]:
            continue
        left, right = i + 1, len(nums) - 1
        while left < right:
            total = nums[i] + nums[left] + nums[right]
            if total == 0:
                result.append([nums[i], nums[left], nums[right]])
                while left < right and nums[left] == nums[left + 1]:
                    left += 1
                while left < right and nums[right] == nums[right - 1]:
                    right -= 1
                left += 1
                right -= 1
            elif total < 0:
                left += 1
            else:
                right -= 1
    return result""",
        time_complexity="O(n²)",
        space_complexity="O(1)",
        viz_type="array",
    ),
    Problem(
        id="valid-palindrome-ii",
        title="Valid Palindrome II",
        difficulty="Easy",
        pattern="Two Pointers",
        companies=["meta"],
        description=(
            "Given a string `s`, return `true` if the `s` can be palindrome after deleting at most one character from it."
        ),
        examples=[
            Example(input='s = "aba"', output="true"),
            Example(input='s = "abca"', output="true", explanation="You could delete the character 'c'."),
            Example(input='s = "abc"', output="false"),
        ],
        constraints=["1 <= s.length <= 10^5", "s consists of lowercase English letters."],
        hints=[
            "Use two pointers from both ends.",
            "When a mismatch is found, try skipping either the left or right character.",
        ],
        solution_code="""def validPalindrome(s):
    def is_palindrome(lo, hi):
        while lo < hi:
            if s[lo] != s[hi]:
                return False
            lo += 1
            hi -= 1
        return True

    left, right = 0, len(s) - 1
    while left < right:
        if s[left] != s[right]:
            return is_palindrome(left + 1, right) or is_palindrome(left, right - 1)
        left += 1
        right -= 1
    return True""",
        time_complexity="O(n)",
        space_complexity="O(1)",
        viz_type="array",
    ),

    # ─── SLIDING WINDOW ──────────────────────────────────────────────────────────
    Problem(
        id="minimum-window-substring",
        title="Minimum Window Substring",
        difficulty="Hard",
        pattern="Sliding Window",
        companies=["meta", "google", "amazon"],
        description=(
            "Given two strings `s` and `t` of lengths `m` and `n` respectively, return the **minimum window substring** "
            "of `s` such that every character in `t` (including duplicates) is included in the window. "
            "If there is no such substring, return the empty string `\"\"`."
        ),
        examples=[
            Example(input='s = "ADOBECODEBANC", t = "ABC"', output='"BANC"',
                    explanation="The minimum window substring 'BANC' includes 'A', 'B', and 'C' from string t."),
            Example(input='s = "a", t = "a"', output='"a"'),
            Example(input='s = "a", t = "aa"', output='""',
                    explanation="Both 'a's from t must be included in the window."),
        ],
        constraints=["m == s.length", "n == t.length", "1 <= m, n <= 10^5",
                     "s and t consist of uppercase and lowercase English letters."],
        hints=[
            "Use a sliding window with two pointers.",
            "Maintain a frequency map for characters in t.",
            "Expand right pointer until window is valid, then shrink left pointer.",
        ],
        solution_code="""from collections import Counter

def minWindow(s, t):
    if not t or not s:
        return ""
    need = Counter(t)
    missing = len(t)
    best = ""
    left = 0
    for right, c in enumerate(s):
        if need[c] > 0:
            missing -= 1
        need[c] -= 1
        if missing == 0:
            while need[s[left]] < 0:
                need[s[left]] += 1
                left += 1
            window = s[left:right + 1]
            if not best or len(window) < len(best):
                best = window
            need[s[left]] += 1
            missing += 1
            left += 1
    return best""",
        time_complexity="O(m + n)",
        space_complexity="O(m + n)",
        viz_type="array",
    ),
    Problem(
        id="longest-substring-without-repeating",
        title="Longest Substring Without Repeating Characters",
        difficulty="Medium",
        pattern="Sliding Window",
        companies=["amazon", "google", "meta"],
        description=(
            "Given a string `s`, find the length of the **longest substring** without repeating characters."
        ),
        examples=[
            Example(input='s = "abcabcbb"', output="3", explanation='The answer is "abc", with the length of 3.'),
            Example(input='s = "bbbbb"', output="1", explanation='The answer is "b", with the length of 1.'),
            Example(input='s = "pwwkew"', output="3", explanation='The answer is "wke", with the length of 3.'),
        ],
        constraints=["0 <= s.length <= 5 * 10^4", "s consists of English letters, digits, symbols and spaces."],
        hints=[
            "Use a sliding window with a hash set to track characters in current window.",
            "When a duplicate is found, shrink the window from the left.",
        ],
        solution_code="""def lengthOfLongestSubstring(s):
    char_index = {}
    max_len = 0
    left = 0
    for right, c in enumerate(s):
        if c in char_index and char_index[c] >= left:
            left = char_index[c] + 1
        char_index[c] = right
        max_len = max(max_len, right - left + 1)
    return max_len""",
        time_complexity="O(n)",
        space_complexity="O(min(m,n))",
        viz_type="array",
    ),
    Problem(
        id="sliding-window-maximum",
        title="Sliding Window Maximum",
        difficulty="Hard",
        pattern="Sliding Window",
        companies=["google", "amazon"],
        description=(
            "You are given an array of integers `nums`, there is a sliding window of size `k` which is moving from the "
            "very left of the array to the very right. You can only see the `k` numbers in the window. Each time the "
            "sliding window moves right by one position.\n\nReturn the max sliding window."
        ),
        examples=[
            Example(input="nums = [1,3,-1,-3,5,3,6,7], k = 3", output="[3,3,5,5,6,7]"),
            Example(input="nums = [1], k = 1", output="[1]"),
        ],
        constraints=["1 <= nums.length <= 10^5", "-10^4 <= nums[i] <= 10^4", "1 <= k <= nums.length"],
        hints=[
            "Use a monotonic deque (decreasing) to track maximum in window.",
            "Remove elements outside the window from the front.",
            "Remove smaller elements from the back before adding new element.",
        ],
        solution_code="""from collections import deque

def maxSlidingWindow(nums, k):
    dq = deque()  # stores indices
    result = []
    for i, num in enumerate(nums):
        # Remove elements outside window
        while dq and dq[0] < i - k + 1:
            dq.popleft()
        # Remove smaller elements from back
        while dq and nums[dq[-1]] < num:
            dq.pop()
        dq.append(i)
        if i >= k - 1:
            result.append(nums[dq[0]])
    return result""",
        time_complexity="O(n)",
        space_complexity="O(k)",
        viz_type="array",
    ),
    Problem(
        id="permutation-in-string",
        title="Permutation in String",
        difficulty="Medium",
        pattern="Sliding Window",
        companies=["microsoft", "amazon"],
        description=(
            "Given two strings `s1` and `s2`, return `true` if `s2` contains a permutation of `s1`, or `false` otherwise.\n\n"
            "In other words, return `true` if one of `s1`'s permutations is the substring of `s2`."
        ),
        examples=[
            Example(input='s1 = "ab", s2 = "eidbaooo"', output="true",
                    explanation="s2 contains one permutation of s1 (\"ba\")."),
            Example(input='s1 = "ab", s2 = "eidboaoo"', output="false"),
        ],
        constraints=["1 <= s1.length, s2.length <= 10^4", "s1 and s2 consist of lowercase English letters."],
        hints=[
            "Use a fixed-size sliding window of size len(s1).",
            "Maintain character frequency counts for the window.",
        ],
        solution_code="""from collections import Counter

def checkInclusion(s1, s2):
    if len(s1) > len(s2):
        return False
    need = Counter(s1)
    window = Counter(s2[:len(s1)])
    if window == need:
        return True
    for i in range(len(s1), len(s2)):
        window[s2[i]] += 1
        left = s2[i - len(s1)]
        window[left] -= 1
        if window[left] == 0:
            del window[left]
        if window == need:
            return True
    return False""",
        time_complexity="O(n)",
        space_complexity="O(1)",
        viz_type="array",
    ),

    # ─── BINARY SEARCH ───────────────────────────────────────────────────────────
    Problem(
        id="median-of-two-sorted-arrays",
        title="Median of Two Sorted Arrays",
        difficulty="Hard",
        pattern="Binary Search",
        companies=["google", "amazon", "meta"],
        description=(
            "Given two sorted arrays `nums1` and `nums2` of size `m` and `n` respectively, return the median of the "
            "two sorted arrays.\n\nThe overall run time complexity should be `O(log(m+n))`."
        ),
        examples=[
            Example(input="nums1 = [1,3], nums2 = [2]", output="2.00000"),
            Example(input="nums1 = [1,2], nums2 = [3,4]", output="2.50000"),
        ],
        constraints=["nums1.length == m", "nums2.length == n", "0 <= m <= 1000", "0 <= n <= 1000",
                     "1 <= m + n <= 2000", "-10^6 <= nums1[i], nums2[i] <= 10^6"],
        hints=[
            "Binary search on the smaller array.",
            "Find the partition such that left half and right half have equal counts.",
        ],
        solution_code="""def findMedianSortedArrays(nums1, nums2):
    if len(nums1) > len(nums2):
        nums1, nums2 = nums2, nums1
    m, n = len(nums1), len(nums2)
    lo, hi = 0, m
    while lo <= hi:
        i = (lo + hi) // 2
        j = (m + n + 1) // 2 - i
        max_left1 = float('-inf') if i == 0 else nums1[i - 1]
        min_right1 = float('inf') if i == m else nums1[i]
        max_left2 = float('-inf') if j == 0 else nums2[j - 1]
        min_right2 = float('inf') if j == n else nums2[j]
        if max_left1 <= min_right2 and max_left2 <= min_right1:
            if (m + n) % 2 == 0:
                return (max(max_left1, max_left2) + min(min_right1, min_right2)) / 2
            else:
                return max(max_left1, max_left2)
        elif max_left1 > min_right2:
            hi = i - 1
        else:
            lo = i + 1""",
        time_complexity="O(log(min(m,n)))",
        space_complexity="O(1)",
        viz_type="array",
    ),
    Problem(
        id="search-in-rotated-sorted-array",
        title="Search in Rotated Sorted Array",
        difficulty="Medium",
        pattern="Binary Search",
        companies=["meta", "google", "amazon"],
        description=(
            "There is an integer array `nums` sorted in ascending order (with **distinct** values).\n\n"
            "Prior to being passed to your function, `nums` is **possibly rotated** at an unknown pivot index `k`.\n\n"
            "Given the array `nums` after the possible rotation and an integer `target`, return the index of `target` "
            "if it is in `nums`, or `-1` if it is not in `nums`."
        ),
        examples=[
            Example(input="nums = [4,5,6,7,0,1,2], target = 0", output="4"),
            Example(input="nums = [4,5,6,7,0,1,2], target = 3", output="-1"),
            Example(input="nums = [1], target = 0", output="-1"),
        ],
        constraints=["1 <= nums.length <= 5000", "-10^4 <= nums[i] <= 10^4", "All values of nums are unique.",
                     "nums is an ascending array that is possibly rotated.", "-10^4 <= target <= 10^4"],
        hints=[
            "The array has two sorted halves.",
            "Determine which half is sorted and check if target is in that range.",
        ],
        solution_code="""def search(nums, target):
    left, right = 0, len(nums) - 1
    while left <= right:
        mid = (left + right) // 2
        if nums[mid] == target:
            return mid
        # Left half is sorted
        if nums[left] <= nums[mid]:
            if nums[left] <= target < nums[mid]:
                right = mid - 1
            else:
                left = mid + 1
        else:  # Right half is sorted
            if nums[mid] < target <= nums[right]:
                left = mid + 1
            else:
                right = mid - 1
    return -1""",
        time_complexity="O(log n)",
        space_complexity="O(1)",
        viz_type="array",
    ),
    Problem(
        id="find-minimum-rotated-sorted-array",
        title="Find Minimum in Rotated Sorted Array",
        difficulty="Medium",
        pattern="Binary Search",
        companies=["google", "microsoft"],
        description=(
            "Suppose an array of length `n` sorted in ascending order is **rotated** between `1` and `n` times. "
            "Given the sorted rotated array `nums` of **unique** elements, return the **minimum** element of this array.\n\n"
            "You must write an algorithm that runs in `O(log n)` time."
        ),
        examples=[
            Example(input="nums = [3,4,5,1,2]", output="1"),
            Example(input="nums = [4,5,6,7,0,1,2]", output="0"),
            Example(input="nums = [11,13,15,17]", output="11"),
        ],
        constraints=["n == nums.length", "1 <= n <= 5000", "-5000 <= nums[i] <= 5000",
                     "All the integers of nums are unique.", "nums is sorted and rotated between 1 and n times."],
        hints=[
            "Binary search: if mid > right, minimum is in right half.",
        ],
        solution_code="""def findMin(nums):
    left, right = 0, len(nums) - 1
    while left < right:
        mid = (left + right) // 2
        if nums[mid] > nums[right]:
            left = mid + 1
        else:
            right = mid
    return nums[left]""",
        time_complexity="O(log n)",
        space_complexity="O(1)",
        viz_type="array",
    ),
    Problem(
        id="koko-eating-bananas",
        title="Koko Eating Bananas",
        difficulty="Medium",
        pattern="Binary Search",
        companies=["google"],
        description=(
            "Koko loves to eat bananas. There are `n` piles of bananas, the `i`th pile has `piles[i]` bananas. "
            "Koko can decide her bananas-per-hour eating speed of `k`. Each hour, she chooses some pile of bananas and "
            "eats `k` bananas from that pile. If the pile has less than `k` bananas, she eats all of them and will not "
            "eat any more bananas during this hour.\n\n"
            "Koko likes to eat slowly but still wants to finish eating all the bananas before the guards return.\n\n"
            "Return the minimum integer `k` such that she can eat all the bananas within `h` hours."
        ),
        examples=[
            Example(input="piles = [3,6,7,11], h = 8", output="4"),
            Example(input="piles = [30,11,23,4,20], h = 5", output="30"),
            Example(input="piles = [30,11,23,4,20], h = 6", output="23"),
        ],
        constraints=["1 <= piles.length <= 10^4", "piles.length <= h <= 10^9", "1 <= piles[i] <= 10^9"],
        hints=[
            "Binary search on the eating speed k.",
            "For a given speed k, compute total hours needed using ceiling division.",
        ],
        solution_code="""import math

def minEatingSpeed(piles, h):
    def hours_needed(k):
        return sum(math.ceil(p / k) for p in piles)

    left, right = 1, max(piles)
    while left < right:
        mid = (left + right) // 2
        if hours_needed(mid) <= h:
            right = mid
        else:
            left = mid + 1
    return left""",
        time_complexity="O(n log(max(piles)))",
        space_complexity="O(1)",
        viz_type="array",
    ),

    # ─── DP 1D ───────────────────────────────────────────────────────────────────
    Problem(
        id="climbing-stairs",
        title="Climbing Stairs",
        difficulty="Easy",
        pattern="Dynamic Programming 1D",
        companies=["amazon", "google", "meta"],
        description=(
            "You are climbing a staircase. It takes `n` steps to reach the top.\n\n"
            "Each time you can either climb `1` or `2` steps. In how many distinct ways can you climb to the top?"
        ),
        examples=[
            Example(input="n = 2", output="2", explanation="There are two ways to climb to the top. 1. 1 step + 1 step; 2. 2 steps"),
            Example(input="n = 3", output="3", explanation="There are three ways: 1+1+1, 1+2, 2+1"),
        ],
        constraints=["1 <= n <= 45"],
        hints=[
            "dp[i] = dp[i-1] + dp[i-2] — this is essentially Fibonacci.",
        ],
        solution_code="""def climbStairs(n):
    if n <= 2:
        return n
    dp = [0] * (n + 1)
    dp[1] = 1
    dp[2] = 2
    for i in range(3, n + 1):
        dp[i] = dp[i - 1] + dp[i - 2]
    return dp[n]""",
        time_complexity="O(n)",
        space_complexity="O(n)",
        viz_type="grid",
    ),
    Problem(
        id="house-robber",
        title="House Robber",
        difficulty="Medium",
        pattern="Dynamic Programming 1D",
        companies=["google", "amazon"],
        description=(
            "You are a professional robber planning to rob houses along a street. Each house has a certain amount of "
            "money stashed, the only constraint stopping you from robbing each of them is that adjacent houses have "
            "security systems connected and **it will automatically contact the police if two adjacent houses were "
            "broken into on the same night**.\n\n"
            "Given an integer array `nums` representing the amount of money of each house, return the maximum amount "
            "of money you can rob tonight **without alerting the police**."
        ),
        examples=[
            Example(input="nums = [1,2,3,1]", output="4", explanation="Rob house 1 (money = 1) and then rob house 3 (money = 3). Total = 4."),
            Example(input="nums = [2,7,9,3,1]", output="12"),
        ],
        constraints=["1 <= nums.length <= 100", "0 <= nums[i] <= 400"],
        hints=[
            "dp[i] = max(dp[i-1], dp[i-2] + nums[i]).",
        ],
        solution_code="""def rob(nums):
    if len(nums) == 1:
        return nums[0]
    dp = [0] * len(nums)
    dp[0] = nums[0]
    dp[1] = max(nums[0], nums[1])
    for i in range(2, len(nums)):
        dp[i] = max(dp[i - 1], dp[i - 2] + nums[i])
    return dp[-1]""",
        time_complexity="O(n)",
        space_complexity="O(n)",
        viz_type="array",
    ),
    Problem(
        id="coin-change",
        title="Coin Change",
        difficulty="Medium",
        pattern="Dynamic Programming 1D",
        companies=["meta", "google", "amazon"],
        description=(
            "You are given an integer array `coins` representing coins of different denominations and an integer "
            "`amount` representing a total amount of money.\n\n"
            "Return the fewest number of coins that you need to make up that amount. If that amount of money cannot "
            "be made up by any combination of the coins, return `-1`.\n\n"
            "You may assume that you have an infinite number of each kind of coin."
        ),
        examples=[
            Example(input="coins = [1,2,5], amount = 11", output="3", explanation="11 = 5 + 5 + 1"),
            Example(input="coins = [2], amount = 3", output="-1"),
            Example(input="coins = [1], amount = 0", output="0"),
        ],
        constraints=["1 <= coins.length <= 12", "1 <= coins[i] <= 2^31 - 1", "0 <= amount <= 10^4"],
        hints=[
            "dp[i] = minimum coins to make amount i.",
            "For each coin, dp[i] = min(dp[i], dp[i - coin] + 1).",
        ],
        solution_code="""def coinChange(coins, amount):
    dp = [float('inf')] * (amount + 1)
    dp[0] = 0
    for i in range(1, amount + 1):
        for coin in coins:
            if coin <= i:
                dp[i] = min(dp[i], dp[i - coin] + 1)
    return dp[amount] if dp[amount] != float('inf') else -1""",
        time_complexity="O(amount × coins)",
        space_complexity="O(amount)",
        viz_type="grid",
    ),
    Problem(
        id="longest-increasing-subsequence",
        title="Longest Increasing Subsequence",
        difficulty="Medium",
        pattern="Dynamic Programming 1D",
        companies=["google", "amazon", "meta"],
        description=(
            "Given an integer array `nums`, return the length of the longest strictly increasing subsequence."
        ),
        examples=[
            Example(input="nums = [10,9,2,5,3,7,101,18]", output="4", explanation="The longest increasing subsequence is [2,3,7,101]."),
            Example(input="nums = [0,1,0,3,2,3]", output="4"),
            Example(input="nums = [7,7,7,7,7,7,7]", output="1"),
        ],
        constraints=["1 <= nums.length <= 2500", "-10^4 <= nums[i] <= 10^4"],
        hints=[
            "dp[i] = length of LIS ending at index i.",
            "For each i, check all j < i where nums[j] < nums[i].",
        ],
        solution_code="""def lengthOfLIS(nums):
    n = len(nums)
    dp = [1] * n
    for i in range(1, n):
        for j in range(i):
            if nums[j] < nums[i]:
                dp[i] = max(dp[i], dp[j] + 1)
    return max(dp)""",
        time_complexity="O(n²)",
        space_complexity="O(n)",
        viz_type="array",
    ),
    Problem(
        id="word-break",
        title="Word Break",
        difficulty="Medium",
        pattern="Dynamic Programming 1D",
        companies=["google", "meta", "amazon"],
        description=(
            "Given a string `s` and a dictionary of strings `wordDict`, return `true` if `s` can be segmented into "
            "a space-separated sequence of one or more dictionary words.\n\n"
            "Note that the same word in the dictionary may be reused multiple times in the segmentation."
        ),
        examples=[
            Example(input='s = "leetcode", wordDict = ["leet","code"]', output="true"),
            Example(input='s = "applepenapple", wordDict = ["apple","pen"]', output="true"),
            Example(input='s = "catsandog", wordDict = ["cats","dog","sand","and","cat"]', output="false"),
        ],
        constraints=["1 <= s.length <= 300", "1 <= wordDict.length <= 1000",
                     "1 <= wordDict[i].length <= 20", "s and wordDict[i] consist of only lowercase English letters.",
                     "All the strings of wordDict are unique."],
        hints=[
            "dp[i] = True if s[:i] can be segmented.",
            "For each i, check all j < i where dp[j] and s[j:i] in word set.",
        ],
        solution_code="""def wordBreak(s, wordDict):
    word_set = set(wordDict)
    n = len(s)
    dp = [False] * (n + 1)
    dp[0] = True
    for i in range(1, n + 1):
        for j in range(i):
            if dp[j] and s[j:i] in word_set:
                dp[i] = True
                break
    return dp[n]""",
        time_complexity="O(n²)",
        space_complexity="O(n)",
        viz_type="grid",
    ),
    Problem(
        id="decode-ways",
        title="Decode Ways",
        difficulty="Medium",
        pattern="Dynamic Programming 1D",
        companies=["meta", "amazon"],
        description=(
            "A message containing letters from `A-Z` can be **encoded** into numbers using the following mapping:\n\n"
            "`'A' -> \"1\"`, `'B' -> \"2\"`, ..., `'Z' -> \"26\"`\n\n"
            "To **decode** an encoded message, all the digits must be grouped then mapped back into letters using the "
            "reverse of the mapping above.\n\n"
            "Given a string `s` containing only digits, return the **number of ways** to **decode** it."
        ),
        examples=[
            Example(input='s = "12"', output="2", explanation='"12" could be decoded as "AB" (1 2) or "L" (12).'),
            Example(input='s = "226"', output="3"),
            Example(input='s = "06"', output="0"),
        ],
        constraints=["1 <= s.length <= 100", "s contains only digits and may contain leading zero(s)."],
        hints=[
            "dp[i] = number of ways to decode s[:i].",
            "Single digit decode: if s[i-1] != '0', dp[i] += dp[i-1].",
            "Two digit decode: if 10 <= int(s[i-2:i]) <= 26, dp[i] += dp[i-2].",
        ],
        solution_code="""def numDecodings(s):
    n = len(s)
    dp = [0] * (n + 1)
    dp[0] = 1
    dp[1] = 1 if s[0] != '0' else 0
    for i in range(2, n + 1):
        if s[i - 1] != '0':
            dp[i] += dp[i - 1]
        two_digit = int(s[i - 2:i])
        if 10 <= two_digit <= 26:
            dp[i] += dp[i - 2]
    return dp[n]""",
        time_complexity="O(n)",
        space_complexity="O(n)",
        viz_type="grid",
    ),

    # ─── DP 2D ───────────────────────────────────────────────────────────────────
    Problem(
        id="edit-distance",
        title="Edit Distance",
        difficulty="Hard",
        pattern="Dynamic Programming 2D",
        companies=["google", "meta", "microsoft"],
        description=(
            "Given two strings `word1` and `word2`, return the **minimum number of operations** required to convert "
            "`word1` to `word2`.\n\n"
            "You have the following three operations permitted on a word:\n"
            "- Insert a character\n- Delete a character\n- Replace a character"
        ),
        examples=[
            Example(input='word1 = "horse", word2 = "ros"', output="3"),
            Example(input='word1 = "intention", word2 = "execution"', output="5"),
        ],
        constraints=["0 <= word1.length, word2.length <= 500", "word1 and word2 consist of lowercase English letters."],
        hints=[
            "dp[i][j] = edit distance between word1[:i] and word2[:j].",
            "If chars match: dp[i][j] = dp[i-1][j-1].",
            "Else: dp[i][j] = 1 + min(dp[i-1][j], dp[i][j-1], dp[i-1][j-1]).",
        ],
        solution_code="""def minDistance(word1, word2):
    m, n = len(word1), len(word2)
    dp = [[0] * (n + 1) for _ in range(m + 1)]
    for i in range(m + 1):
        dp[i][0] = i
    for j in range(n + 1):
        dp[0][j] = j
    for i in range(1, m + 1):
        for j in range(1, n + 1):
            if word1[i - 1] == word2[j - 1]:
                dp[i][j] = dp[i - 1][j - 1]
            else:
                dp[i][j] = 1 + min(dp[i - 1][j], dp[i][j - 1], dp[i - 1][j - 1])
    return dp[m][n]""",
        time_complexity="O(m × n)",
        space_complexity="O(m × n)",
        viz_type="grid",
    ),
    Problem(
        id="longest-common-subsequence",
        title="Longest Common Subsequence",
        difficulty="Medium",
        pattern="Dynamic Programming 2D",
        companies=["google", "meta", "amazon"],
        description=(
            "Given two strings `text1` and `text2`, return the length of their **longest common subsequence**. "
            "If there is no common subsequence, return `0`.\n\n"
            "A **subsequence** of a string is a new string generated from the original string with some characters "
            "(can be none) deleted without changing the relative order of the remaining characters."
        ),
        examples=[
            Example(input='text1 = "abcde", text2 = "ace"', output="3", explanation='The longest common subsequence is "ace".'),
            Example(input='text1 = "abc", text2 = "abc"', output="3"),
            Example(input='text1 = "abc", text2 = "def"', output="0"),
        ],
        constraints=["1 <= text1.length, text2.length <= 1000", "text1 and text2 consist of only lowercase English letters."],
        hints=[
            "dp[i][j] = LCS of text1[:i] and text2[:j].",
            "If chars match: dp[i][j] = dp[i-1][j-1] + 1.",
            "Else: dp[i][j] = max(dp[i-1][j], dp[i][j-1]).",
        ],
        solution_code="""def longestCommonSubsequence(text1, text2):
    m, n = len(text1), len(text2)
    dp = [[0] * (n + 1) for _ in range(m + 1)]
    for i in range(1, m + 1):
        for j in range(1, n + 1):
            if text1[i - 1] == text2[j - 1]:
                dp[i][j] = dp[i - 1][j - 1] + 1
            else:
                dp[i][j] = max(dp[i - 1][j], dp[i][j - 1])
    return dp[m][n]""",
        time_complexity="O(m × n)",
        space_complexity="O(m × n)",
        viz_type="grid",
    ),
    Problem(
        id="unique-paths",
        title="Unique Paths",
        difficulty="Medium",
        pattern="Dynamic Programming 2D",
        companies=["google", "amazon"],
        description=(
            "There is a robot on an `m x n` grid. The robot is initially located at the **top-left corner**. "
            "The robot tries to move to the **bottom-right corner**. The robot can only move either down or right.\n\n"
            "Given the two integers `m` and `n`, return the number of possible unique paths."
        ),
        examples=[
            Example(input="m = 3, n = 7", output="28"),
            Example(input="m = 3, n = 2", output="3"),
        ],
        constraints=["1 <= m, n <= 100"],
        hints=[
            "dp[i][j] = dp[i-1][j] + dp[i][j-1].",
            "Base case: first row and first column are all 1.",
        ],
        solution_code="""def uniquePaths(m, n):
    dp = [[1] * n for _ in range(m)]
    for i in range(1, m):
        for j in range(1, n):
            dp[i][j] = dp[i - 1][j] + dp[i][j - 1]
    return dp[m - 1][n - 1]""",
        time_complexity="O(m × n)",
        space_complexity="O(m × n)",
        viz_type="grid",
    ),

    # ─── TREES ───────────────────────────────────────────────────────────────────
    Problem(
        id="binary-tree-max-path-sum",
        title="Binary Tree Maximum Path Sum",
        difficulty="Hard",
        pattern="Trees",
        companies=["meta", "google", "amazon"],
        description=(
            "A **path** in a binary tree is a sequence of nodes where each pair of adjacent nodes in the sequence "
            "has an edge connecting them. A node can only appear in the sequence **at most once**. Note that the "
            "path does not need to pass through the root.\n\n"
            "The **path sum** of a path is the sum of the node's values in the path.\n\n"
            "Given the `root` of a binary tree, return the **maximum path sum** of any **non-empty** path."
        ),
        examples=[
            Example(input="root = [1,2,3]", output="6", explanation="The optimal path is 2 -> 1 -> 3."),
            Example(input="root = [-10,9,20,null,null,15,7]", output="42", explanation="The optimal path is 15 -> 20 -> 7."),
        ],
        constraints=["-1000 <= Node.val <= 1000", "The number of nodes in the tree is in the range [1, 3 * 10^4]."],
        hints=[
            "For each node, compute the max gain from left and right subtrees.",
            "Update global max with left_gain + node.val + right_gain.",
            "Return node.val + max(left_gain, right_gain, 0) to parent.",
        ],
        solution_code="""def maxPathSum(root):
    max_sum = [float('-inf')]

    def dfs(node):
        if not node:
            return 0
        left = max(dfs(node.left), 0)
        right = max(dfs(node.right), 0)
        max_sum[0] = max(max_sum[0], node.val + left + right)
        return node.val + max(left, right)

    dfs(root)
    return max_sum[0]""",
        time_complexity="O(n)",
        space_complexity="O(h)",
        viz_type="tree",
    ),
    Problem(
        id="serialize-deserialize-binary-tree",
        title="Serialize and Deserialize Binary Tree",
        difficulty="Hard",
        pattern="Trees",
        companies=["meta", "google", "amazon"],
        description=(
            "Serialization is the process of converting a data structure or object into a sequence of bits so that "
            "it can be stored in a file or memory buffer, or transmitted across a network connection link to be "
            "reconstructed later in the same or another computer environment.\n\n"
            "Design an algorithm to serialize and deserialize a binary tree."
        ),
        examples=[
            Example(input="root = [1,2,3,null,null,4,5]", output="[1,2,3,null,null,4,5]"),
        ],
        constraints=["The number of nodes in the tree is in the range [0, 10^4].", "-1000 <= Node.val <= 1000"],
        hints=[
            "Use BFS or DFS with null markers.",
            "For DFS: preorder with 'null' for missing nodes.",
        ],
        solution_code="""from collections import deque

class Codec:
    def serialize(self, root):
        if not root:
            return "null"
        result = []
        queue = deque([root])
        while queue:
            node = queue.popleft()
            if node:
                result.append(str(node.val))
                queue.append(node.left)
                queue.append(node.right)
            else:
                result.append("null")
        return ",".join(result)

    def deserialize(self, data):
        if data == "null":
            return None
        vals = data.split(",")
        root = TreeNode(int(vals[0]))
        queue = deque([root])
        i = 1
        while queue and i < len(vals):
            node = queue.popleft()
            if vals[i] != "null":
                node.left = TreeNode(int(vals[i]))
                queue.append(node.left)
            i += 1
            if i < len(vals) and vals[i] != "null":
                node.right = TreeNode(int(vals[i]))
                queue.append(node.right)
            i += 1
        return root""",
        time_complexity="O(n)",
        space_complexity="O(n)",
        viz_type="tree",
    ),
    Problem(
        id="lca-binary-tree",
        title="Lowest Common Ancestor of a Binary Tree",
        difficulty="Medium",
        pattern="Trees",
        companies=["meta", "amazon"],
        description=(
            "Given a binary tree, find the **lowest common ancestor (LCA)** of two given nodes in the tree.\n\n"
            "The lowest common ancestor is defined between two nodes `p` and `q` as the lowest node in `T` that has "
            "both `p` and `q` as descendants (where we allow **a node to be a descendant of itself**)."
        ),
        examples=[
            Example(input="root = [3,5,1,6,2,0,8,null,null,7,4], p = 5, q = 1", output="3"),
            Example(input="root = [3,5,1,6,2,0,8,null,null,7,4], p = 5, q = 4", output="5"),
        ],
        constraints=["The number of nodes in the tree is in the range [2, 10^5].", "-10^9 <= Node.val <= 10^9"],
        hints=[
            "If current node is p or q, return it.",
            "If both left and right subtrees return non-null, current node is LCA.",
        ],
        solution_code="""def lowestCommonAncestor(root, p, q):
    if not root or root == p or root == q:
        return root
    left = lowestCommonAncestor(root.left, p, q)
    right = lowestCommonAncestor(root.right, p, q)
    if left and right:
        return root
    return left or right""",
        time_complexity="O(n)",
        space_complexity="O(h)",
        viz_type="tree",
    ),
    Problem(
        id="diameter-of-binary-tree",
        title="Diameter of Binary Tree",
        difficulty="Easy",
        pattern="Trees",
        companies=["meta", "google"],
        description=(
            "Given the `root` of a binary tree, return the **length of the diameter** of the tree.\n\n"
            "The **diameter** of a binary tree is the **length of the longest path** between any two nodes in a tree. "
            "This path may or may not pass through the root.\n\n"
            "The **length** of a path between two nodes is represented by the number of edges between them."
        ),
        examples=[
            Example(input="root = [1,2,3,4,5]", output="3", explanation="3 is the length of the path [4,2,1,3] or [5,2,1,3]."),
            Example(input="root = [1,2]", output="1"),
        ],
        constraints=["The number of nodes in the tree is in the range [1, 10^4].", "-100 <= Node.val <= 100"],
        hints=[
            "The diameter through a node = left_height + right_height.",
            "Use DFS to compute height and update global diameter.",
        ],
        solution_code="""def diameterOfBinaryTree(root):
    diameter = [0]

    def height(node):
        if not node:
            return 0
        left = height(node.left)
        right = height(node.right)
        diameter[0] = max(diameter[0], left + right)
        return 1 + max(left, right)

    height(root)
    return diameter[0]""",
        time_complexity="O(n)",
        space_complexity="O(h)",
        viz_type="tree",
    ),
    Problem(
        id="construct-binary-tree-preorder-inorder",
        title="Construct Binary Tree from Preorder and Inorder Traversal",
        difficulty="Medium",
        pattern="Trees",
        companies=["amazon", "google"],
        description=(
            "Given two integer arrays `preorder` and `inorder` where `preorder` is the preorder traversal of a "
            "binary tree and `inorder` is the inorder traversal of the same tree, construct and return the binary tree."
        ),
        examples=[
            Example(input="preorder = [3,9,20,15,7], inorder = [9,3,15,20,7]", output="[3,9,20,null,null,15,7]"),
            Example(input="preorder = [-1], inorder = [-1]", output="[-1]"),
        ],
        constraints=["1 <= preorder.length <= 3000", "inorder.length == preorder.length",
                     "-3000 <= preorder[i], inorder[i] <= 3000", "preorder and inorder consist of unique values."],
        hints=[
            "First element of preorder is always the root.",
            "Find root in inorder to split left/right subtrees.",
        ],
        solution_code="""def buildTree(preorder, inorder):
    if not preorder or not inorder:
        return None
    root_val = preorder[0]
    root = TreeNode(root_val)
    mid = inorder.index(root_val)
    root.left = buildTree(preorder[1:mid + 1], inorder[:mid])
    root.right = buildTree(preorder[mid + 1:], inorder[mid + 1:])
    return root""",
        time_complexity="O(n)",
        space_complexity="O(n)",
        viz_type="tree",
    ),

    # ─── GRAPH TRAVERSAL ─────────────────────────────────────────────────────────
    Problem(
        id="course-schedule-ii",
        title="Course Schedule II",
        difficulty="Medium",
        pattern="Graph Traversal",
        companies=["google", "meta", "amazon"],
        description=(
            "There are a total of `numCourses` courses you have to take, labeled from `0` to `numCourses - 1`. "
            "You are given an array `prerequisites` where `prerequisites[i] = [ai, bi]` indicates that you **must** "
            "take course `bi` first if you want to take course `ai`.\n\n"
            "Return the ordering of courses you should take to finish all courses. If there are many valid answers, "
            "return any of them. If it is impossible to finish all courses, return an empty array."
        ),
        examples=[
            Example(input="numCourses = 2, prerequisites = [[1,0]]", output="[0,1]"),
            Example(input="numCourses = 4, prerequisites = [[1,0],[2,0],[3,1],[3,2]]", output="[0,2,1,3]"),
            Example(input="numCourses = 1, prerequisites = []", output="[0]"),
        ],
        constraints=["1 <= numCourses <= 2000", "0 <= prerequisites.length <= numCourses * (numCourses - 1)"],
        hints=[
            "Topological sort using DFS or BFS (Kahn's algorithm).",
            "Detect cycle: if a node is visited in current DFS path, there's a cycle.",
        ],
        solution_code="""from collections import deque

def findOrder(numCourses, prerequisites):
    graph = [[] for _ in range(numCourses)]
    in_degree = [0] * numCourses
    for course, pre in prerequisites:
        graph[pre].append(course)
        in_degree[course] += 1
    queue = deque([i for i in range(numCourses) if in_degree[i] == 0])
    order = []
    while queue:
        node = queue.popleft()
        order.append(node)
        for neighbor in graph[node]:
            in_degree[neighbor] -= 1
            if in_degree[neighbor] == 0:
                queue.append(neighbor)
    return order if len(order) == numCourses else []""",
        time_complexity="O(V + E)",
        space_complexity="O(V + E)",
        viz_type="graph",
    ),
    Problem(
        id="network-delay-time",
        title="Network Delay Time",
        difficulty="Medium",
        pattern="Graph Traversal",
        companies=["google", "amazon"],
        description=(
            "You are given a network of `n` nodes, labeled from `1` to `n`. You are also given `times`, a list of "
            "travel times as directed edges `times[i] = (ui, vi, wi)`, where `ui` is the source node, `vi` is the "
            "target node, and `wi` is the time it takes for a signal to travel from source to target.\n\n"
            "We will send a signal from a given node `k`. Return the **minimum time** it takes for all `n` nodes to "
            "receive the signal. If it is impossible for all `n` nodes to receive the signal, return `-1`."
        ),
        examples=[
            Example(input="times = [[2,1,1],[2,3,1],[3,4,1]], n = 4, k = 2", output="2"),
            Example(input="times = [[1,2,1]], n = 2, k = 1", output="1"),
        ],
        constraints=["1 <= k <= n <= 100", "1 <= times.length <= 6000"],
        hints=["Use Dijkstra's algorithm from node k."],
        solution_code="""import heapq
from collections import defaultdict

def networkDelayTime(times, n, k):
    graph = defaultdict(list)
    for u, v, w in times:
        graph[u].append((v, w))
    dist = {i: float('inf') for i in range(1, n + 1)}
    dist[k] = 0
    heap = [(0, k)]
    while heap:
        d, u = heapq.heappop(heap)
        if d > dist[u]:
            continue
        for v, w in graph[u]:
            if dist[u] + w < dist[v]:
                dist[v] = dist[u] + w
                heapq.heappush(heap, (dist[v], v))
    max_dist = max(dist.values())
    return max_dist if max_dist < float('inf') else -1""",
        time_complexity="O((V + E) log V)",
        space_complexity="O(V + E)",
        viz_type="graph",
    ),
    Problem(
        id="number-of-islands",
        title="Number of Islands",
        difficulty="Medium",
        pattern="Graph Traversal",
        companies=["amazon", "google", "meta"],
        description=(
            "Given an `m x n` 2D binary grid `grid` which represents a map of `'1'`s (land) and `'0'`s (water), "
            "return the number of islands.\n\n"
            "An **island** is surrounded by water and is formed by connecting adjacent lands horizontally or vertically."
        ),
        examples=[
            Example(input='grid = [["1","1","1","1","0"],["1","1","0","1","0"],["1","1","0","0","0"],["0","0","0","0","0"]]', output="1"),
            Example(input='grid = [["1","1","0","0","0"],["1","1","0","0","0"],["0","0","1","0","0"],["0","0","0","1","1"]]', output="3"),
        ],
        constraints=["m == grid.length", "n == grid[i].length", "1 <= m, n <= 300",
                     'grid[i][j] is \'0\' or \'1\'.'],
        hints=[
            "DFS/BFS from each unvisited '1'.",
            "Mark visited cells to avoid revisiting.",
        ],
        solution_code="""def numIslands(grid):
    if not grid:
        return 0
    rows, cols = len(grid), len(grid[0])
    count = 0

    def dfs(r, c):
        if r < 0 or r >= rows or c < 0 or c >= cols or grid[r][c] != '1':
            return
        grid[r][c] = '#'  # mark visited
        dfs(r + 1, c)
        dfs(r - 1, c)
        dfs(r, c + 1)
        dfs(r, c - 1)

    for r in range(rows):
        for c in range(cols):
            if grid[r][c] == '1':
                dfs(r, c)
                count += 1
    return count""",
        time_complexity="O(m × n)",
        space_complexity="O(m × n)",
        viz_type="grid",
    ),
    Problem(
        id="clone-graph",
        title="Clone Graph",
        difficulty="Medium",
        pattern="Graph Traversal",
        companies=["meta", "amazon"],
        description=(
            "Given a reference of a node in a **connected** undirected graph, return a **deep copy** (clone) of the graph.\n\n"
            "Each node in the graph contains a value (`int`) and a list (`List[Node]`) of its neighbors."
        ),
        examples=[
            Example(input="adjList = [[2,4],[1,3],[2,4],[1,3]]", output="[[2,4],[1,3],[2,4],[1,3]]"),
        ],
        constraints=["The number of nodes in the graph is in the range [0, 100].",
                     "1 <= Node.val <= 100", "Node.val is unique for each node."],
        hints=[
            "Use a hash map from original node to its clone.",
            "BFS or DFS to traverse all nodes.",
        ],
        solution_code="""def cloneGraph(node):
    if not node:
        return None
    cloned = {}

    def dfs(n):
        if n in cloned:
            return cloned[n]
        clone = Node(n.val)
        cloned[n] = clone
        for neighbor in n.neighbors:
            clone.neighbors.append(dfs(neighbor))
        return clone

    return dfs(node)""",
        time_complexity="O(V + E)",
        space_complexity="O(V)",
        viz_type="graph",
    ),

    # ─── HEAP / PRIORITY QUEUE ───────────────────────────────────────────────────
    Problem(
        id="merge-k-sorted-lists",
        title="Merge K Sorted Lists",
        difficulty="Hard",
        pattern="Heap / Priority Queue",
        companies=["google", "meta", "amazon"],
        description=(
            "You are given an array of `k` linked-lists `lists`, each linked-list is sorted in ascending order.\n\n"
            "Merge all the linked-lists into one sorted linked-list and return it."
        ),
        examples=[
            Example(input="lists = [[1,4,5],[1,3,4],[2,6]]", output="[1,1,2,3,4,4,5,6]"),
            Example(input="lists = []", output="[]"),
        ],
        constraints=["k == lists.length", "0 <= k <= 10^4", "0 <= lists[i].length <= 500",
                     "-10^4 <= lists[i][j] <= 10^4"],
        hints=[
            "Use a min-heap of size k.",
            "Push the head of each list, then pop minimum and push next node.",
        ],
        solution_code="""import heapq

def mergeKLists(lists):
    heap = []
    for i, node in enumerate(lists):
        if node:
            heapq.heappush(heap, (node.val, i, node))
    dummy = ListNode(0)
    curr = dummy
    while heap:
        val, i, node = heapq.heappop(heap)
        curr.next = node
        curr = curr.next
        if node.next:
            heapq.heappush(heap, (node.next.val, i, node.next))
    return dummy.next""",
        time_complexity="O(n log k)",
        space_complexity="O(k)",
        viz_type="array",
    ),
    Problem(
        id="top-k-frequent-elements",
        title="Top K Frequent Elements",
        difficulty="Medium",
        pattern="Heap / Priority Queue",
        companies=["meta", "amazon"],
        description=(
            "Given an integer array `nums` and an integer `k`, return the `k` most frequent elements. "
            "You may return the answer in any order."
        ),
        examples=[
            Example(input="nums = [1,1,1,2,2,3], k = 2", output="[1,2]"),
            Example(input="nums = [1], k = 1", output="[1]"),
        ],
        constraints=["1 <= nums.length <= 10^5", "-10^4 <= nums[i] <= 10^4",
                     "k is in the range [1, the number of unique elements in the array].",
                     "It is guaranteed that the answer is unique."],
        hints=[
            "Count frequency with a hash map.",
            "Use a min-heap of size k or bucket sort.",
        ],
        solution_code="""from collections import Counter
import heapq

def topKFrequent(nums, k):
    count = Counter(nums)
    return heapq.nlargest(k, count.keys(), key=count.get)""",
        time_complexity="O(n log k)",
        space_complexity="O(n)",
        viz_type="array",
    ),
    Problem(
        id="task-scheduler",
        title="Task Scheduler",
        difficulty="Medium",
        pattern="Heap / Priority Queue",
        companies=["google", "meta"],
        description=(
            "Given a characters array `tasks`, representing the tasks a CPU needs to do, where each letter represents "
            "a different task. Tasks could be done in any order. Each task is done in one unit of time. For each "
            "unit of time, the CPU could complete either one task or just be idle.\n\n"
            "However, there is a non-negative integer `n` that represents the cooldown interval between two **same** "
            "tasks (the same letter in the array), that is that there must be at least `n` units of time between "
            "any two same tasks.\n\n"
            "Return the **least** number of units of times that the CPU will take to finish all the given tasks."
        ),
        examples=[
            Example(input='tasks = ["A","A","A","B","B","B"], n = 2', output="8"),
            Example(input='tasks = ["A","A","A","B","B","B"], n = 0', output="6"),
        ],
        constraints=["1 <= task.length <= 10^4", "tasks[i] is upper-case English letter.", "0 <= n <= 100"],
        hints=[
            "Count task frequencies. Most frequent task determines the frame size.",
            "Total time = max(len(tasks), (max_count - 1) * (n + 1) + tasks_with_max_count).",
        ],
        solution_code="""from collections import Counter

def leastInterval(tasks, n):
    counts = Counter(tasks)
    max_count = max(counts.values())
    tasks_with_max = sum(1 for c in counts.values() if c == max_count)
    return max(len(tasks), (max_count - 1) * (n + 1) + tasks_with_max)""",
        time_complexity="O(n)",
        space_complexity="O(1)",
        viz_type="array",
    ),

    # ─── BACKTRACKING ─────────────────────────────────────────────────────────────
    Problem(
        id="n-queens",
        title="N-Queens",
        difficulty="Hard",
        pattern="Backtracking",
        companies=["google", "meta", "amazon"],
        description=(
            "The **n-queens** puzzle is the problem of placing `n` queens on an `n x n` chessboard such that no two "
            "queens attack each other.\n\n"
            "Given an integer `n`, return all distinct solutions to the **n-queens puzzle**. You may return the "
            "answer in **any order**.\n\n"
            "Each solution contains a distinct board configuration of the n-queens' placement, where `'Q'` and `'.'` "
            "both indicate a queen and an empty space, respectively."
        ),
        examples=[
            Example(input="n = 4", output='[[".Q..","...Q","Q...","..Q."],["..Q.","Q...","...Q",".Q.."]]'),
            Example(input="n = 1", output='[["Q"]]'),
        ],
        constraints=["1 <= n <= 9"],
        hints=[
            "Use backtracking, placing queens row by row.",
            "Track occupied columns, diagonals, and anti-diagonals.",
        ],
        solution_code="""def solveNQueens(n):
    solutions = []
    cols = set()
    diag1 = set()  # row - col
    diag2 = set()  # row + col
    board = ['.' * n for _ in range(n)]

    def backtrack(row):
        if row == n:
            solutions.append(board[:])
            return
        for col in range(n):
            if col in cols or (row - col) in diag1 or (row + col) in diag2:
                continue
            cols.add(col)
            diag1.add(row - col)
            diag2.add(row + col)
            board[row] = '.' * col + 'Q' + '.' * (n - col - 1)
            backtrack(row + 1)
            cols.remove(col)
            diag1.remove(row - col)
            diag2.remove(row + col)
            board[row] = '.' * n

    backtrack(0)
    return solutions""",
        time_complexity="O(n!)",
        space_complexity="O(n)",
        viz_type="grid",
    ),
    Problem(
        id="combination-sum",
        title="Combination Sum",
        difficulty="Medium",
        pattern="Backtracking",
        companies=["google", "meta", "amazon"],
        description=(
            "Given an array of **distinct** integers `candidates` and a target integer `target`, return a list of all "
            "**unique combinations** of `candidates` where the chosen numbers sum to `target`. You may return the "
            "combinations in **any order**.\n\n"
            "The **same** number may be chosen from `candidates` an **unlimited number of times**."
        ),
        examples=[
            Example(input="candidates = [2,3,6,7], target = 7", output="[[2,2,3],[7]]"),
            Example(input="candidates = [2,3,5], target = 8", output="[[2,2,2,2],[2,3,3],[3,5]]"),
        ],
        constraints=["1 <= candidates.length <= 30", "2 <= candidates[i] <= 40",
                     "All elements of candidates are distinct.", "1 <= target <= 40"],
        hints=[
            "Backtrack with start index to avoid duplicate combinations.",
            "Sort candidates to enable early termination.",
        ],
        solution_code="""def combinationSum(candidates, target):
    result = []
    candidates.sort()

    def backtrack(start, current, remaining):
        if remaining == 0:
            result.append(current[:])
            return
        for i in range(start, len(candidates)):
            if candidates[i] > remaining:
                break
            current.append(candidates[i])
            backtrack(i, current, remaining - candidates[i])
            current.pop()

    backtrack(0, [], target)
    return result""",
        time_complexity="O(n^(T/M))",
        space_complexity="O(T/M)",
        viz_type="array",
    ),
    Problem(
        id="palindrome-partitioning",
        title="Palindrome Partitioning",
        difficulty="Medium",
        pattern="Backtracking",
        companies=["google", "meta"],
        description=(
            "Given a string `s`, partition `s` such that every substring of the partition is a **palindrome**. "
            "Return all possible palindrome partitioning of `s`."
        ),
        examples=[
            Example(input='s = "aab"', output='[["a","a","b"],["aa","b"]]'),
            Example(input='s = "a"', output='[["a"]]'),
        ],
        constraints=["1 <= s.length <= 16", "s consists of only lowercase English letters."],
        hints=[
            "Backtrack: at each index, try all substrings starting there.",
            "If substring is palindrome, recurse on the rest.",
        ],
        solution_code="""def partition(s):
    result = []

    def is_palindrome(sub):
        return sub == sub[::-1]

    def backtrack(start, path):
        if start == len(s):
            result.append(path[:])
            return
        for end in range(start + 1, len(s) + 1):
            sub = s[start:end]
            if is_palindrome(sub):
                path.append(sub)
                backtrack(end, path)
                path.pop()

    backtrack(0, [])
    return result""",
        time_complexity="O(n × 2^n)",
        space_complexity="O(n)",
        viz_type="array",
    ),

    # ─── MONOTONIC STACK ─────────────────────────────────────────────────────────
    Problem(
        id="largest-rectangle-in-histogram",
        title="Largest Rectangle in Histogram",
        difficulty="Hard",
        pattern="Monotonic Stack",
        companies=["google", "meta", "amazon"],
        description=(
            "Given an array of integers `heights` representing the histogram's bar height where the width of each "
            "bar is `1`, return the area of the largest rectangle in the histogram."
        ),
        examples=[
            Example(input="heights = [2,1,5,6,2,3]", output="10", explanation="The largest rectangle is shown in the red area, which has an area = 10 units."),
            Example(input="heights = [2,4]", output="4"),
        ],
        constraints=["1 <= heights.length <= 10^5", "0 <= heights[i] <= 10^4"],
        hints=[
            "Use a monotonic increasing stack.",
            "When a bar is shorter than the top of stack, calculate area with stack top as height.",
        ],
        solution_code="""def largestRectangleArea(heights):
    stack = []  # stores indices
    max_area = 0
    heights = heights + [0]  # sentinel
    for i, h in enumerate(heights):
        start = i
        while stack and heights[stack[-1]] > h:
            idx = stack.pop()
            width = i - (stack[-1] if stack else -1) - 1
            max_area = max(max_area, heights[idx] * width)
            start = idx
        stack.append(i)
    return max_area""",
        time_complexity="O(n)",
        space_complexity="O(n)",
        viz_type="array",
    ),
    Problem(
        id="daily-temperatures",
        title="Daily Temperatures",
        difficulty="Medium",
        pattern="Monotonic Stack",
        companies=["google", "amazon"],
        description=(
            "Given an array of integers `temperatures` represents the daily temperatures, return an array `answer` "
            "such that `answer[i]` is the number of days you have to wait after the `i`th day to get a warmer temperature. "
            "If there is no future day for which this is possible, keep `answer[i] == 0` instead."
        ),
        examples=[
            Example(input="temperatures = [73,74,75,71,69,72,76,73]", output="[1,1,4,2,1,1,0,0]"),
            Example(input="temperatures = [30,40,50,60]", output="[1,1,1,0]"),
        ],
        constraints=["1 <= temperatures.length <= 10^5", "30 <= temperatures[i] <= 100"],
        hints=[
            "Use a monotonic decreasing stack storing indices.",
            "When current temp > stack top, pop and compute days difference.",
        ],
        solution_code="""def dailyTemperatures(temperatures):
    n = len(temperatures)
    answer = [0] * n
    stack = []  # indices with decreasing temperatures
    for i, temp in enumerate(temperatures):
        while stack and temperatures[stack[-1]] < temp:
            idx = stack.pop()
            answer[idx] = i - idx
        stack.append(i)
    return answer""",
        time_complexity="O(n)",
        space_complexity="O(n)",
        viz_type="array",
    ),
    Problem(
        id="next-greater-element-ii",
        title="Next Greater Element II",
        difficulty="Medium",
        pattern="Monotonic Stack",
        companies=["amazon", "google"],
        description=(
            "Given a circular integer array `nums` (i.e., the next element of `nums[nums.length - 1]` is `nums[0]`), "
            "return the **next greater number** for every element in `nums`.\n\n"
            "The **next greater number** of a number `x` is the first greater number to its traversing-order next in "
            "the array, which means you could search circularly to find its next greater number. If it doesn't exist, return `-1`."
        ),
        examples=[
            Example(input="nums = [1,2,1]", output="[2,-1,2]"),
            Example(input="nums = [1,2,3,4,3]", output="[2,3,4,-1,4]"),
        ],
        constraints=["1 <= nums.length <= 10^4", "-10^9 <= nums[i] <= 10^9"],
        hints=[
            "Iterate through the array twice (2n) to simulate circular behavior.",
            "Use a monotonic stack; use index % n.",
        ],
        solution_code="""def nextGreaterElements(nums):
    n = len(nums)
    result = [-1] * n
    stack = []
    for i in range(2 * n):
        while stack and nums[stack[-1]] < nums[i % n]:
            idx = stack.pop()
            result[idx] = nums[i % n]
        if i < n:
            stack.append(i)
    return result""",
        time_complexity="O(n)",
        space_complexity="O(n)",
        viz_type="array",
    ),

    # ─── TRIE ────────────────────────────────────────────────────────────────────
    Problem(
        id="implement-trie",
        title="Implement Trie (Prefix Tree)",
        difficulty="Medium",
        pattern="Trie",
        companies=["google", "meta", "amazon"],
        description=(
            "A **trie** (pronounced as 'try') or **prefix tree** is a tree data structure used to efficiently store "
            "and retrieve keys in a dataset of strings. There are various applications of this data structure, such "
            "as autocomplete and spellchecker.\n\n"
            "Implement the Trie class:\n"
            "- `Trie()` Initializes the trie object.\n"
            "- `void insert(String word)` Inserts the string word into the trie.\n"
            "- `boolean search(String word)` Returns true if the string word is in the trie.\n"
            "- `boolean startsWith(String prefix)` Returns true if there is a previously inserted string that has prefix."
        ),
        examples=[
            Example(
                input='["Trie","insert","search","search","startsWith","insert","search"]\n[[],["apple"],["apple"],["app"],["app"],["app"],["app"]]',
                output='[null,null,true,false,true,null,true]'
            ),
        ],
        constraints=["1 <= word.length, prefix.length <= 2000",
                     "word and prefix consist only of lowercase English letters.",
                     "At most 3 * 10^4 calls in total will be made to insert, search, and startsWith."],
        hints=[
            "Use a hash map at each node to store children.",
            "Mark end of word with a boolean flag.",
        ],
        solution_code="""class TrieNode:
    def __init__(self):
        self.children = {}
        self.is_end = False

class Trie:
    def __init__(self):
        self.root = TrieNode()

    def insert(self, word):
        node = self.root
        for ch in word:
            if ch not in node.children:
                node.children[ch] = TrieNode()
            node = node.children[ch]
        node.is_end = True

    def search(self, word):
        node = self.root
        for ch in word:
            if ch not in node.children:
                return False
            node = node.children[ch]
        return node.is_end

    def startsWith(self, prefix):
        node = self.root
        for ch in prefix:
            if ch not in node.children:
                return False
            node = node.children[ch]
        return True""",
        time_complexity="O(m) per operation",
        space_complexity="O(m × n)",
        viz_type="tree",
    ),

    # ─── UNION FIND ──────────────────────────────────────────────────────────────
    Problem(
        id="accounts-merge",
        title="Accounts Merge",
        difficulty="Medium",
        pattern="Union Find",
        companies=["google", "meta"],
        description=(
            "Given a list of `accounts` where each element `accounts[i]` is a list of strings, where the first "
            "element `accounts[i][0]` is a name, and the rest of the elements are **emails** representing emails of "
            "the account.\n\n"
            "Now, we would like to merge these accounts. Two accounts definitely belong to the same person if there "
            "is some common email to both accounts. After merging the accounts, return the accounts in the format "
            "where the first element of each account is the name and the rest of the elements are emails in sorted order."
        ),
        examples=[
            Example(
                input='accounts = [["John","johnsmith@mail.com","john_newyork@mail.com"],["John","johnsmith@mail.com","john00@mail.com"],["Mary","mary@mail.com"],["John","johnnybravo@mail.com"]]',
                output='[["John","john00@mail.com","john_newyork@mail.com","johnsmith@mail.com"],["Mary","mary@mail.com"],["John","johnnybravo@mail.com"]]'
            ),
        ],
        constraints=["1 <= accounts.length <= 1000", "2 <= accounts[i].length <= 10",
                     "1 <= accounts[i][j].length <= 30"],
        hints=[
            "Union-Find: union all emails in the same account.",
            "Group emails by root, then sort and format.",
        ],
        solution_code="""from collections import defaultdict

def accountsMerge(accounts):
    parent = {}
    email_to_name = {}

    def find(x):
        if parent[x] != x:
            parent[x] = find(parent[x])
        return parent[x]

    def union(x, y):
        parent[find(x)] = find(y)

    for account in accounts:
        name = account[0]
        for email in account[1:]:
            if email not in parent:
                parent[email] = email
            email_to_name[email] = name
            union(email, account[1])

    groups = defaultdict(list)
    for email in parent:
        groups[find(email)].append(email)

    result = []
    for root, emails in groups.items():
        result.append([email_to_name[root]] + sorted(emails))
    return result""",
        time_complexity="O(n log n)",
        space_complexity="O(n)",
        viz_type="graph",
    ),
    Problem(
        id="redundant-connection",
        title="Redundant Connection",
        difficulty="Medium",
        pattern="Union Find",
        companies=["amazon", "google"],
        description=(
            "In this problem, a tree is an **undirected graph** that is connected and has no cycles.\n\n"
            "You are given a graph that started as a tree with `n` nodes labeled from `1` to `n`, with one additional "
            "edge added. The added edge has two different vertices chosen from `1` to `n`, and was not an edge that "
            "already existed. The graph is represented as an array `edges` of length `n` where `edges[i] = [ai, bi]` "
            "indicates that there is an edge between nodes `ai` and `bi` in the graph.\n\n"
            "Return an edge that can be removed so that the resulting graph is a tree of `n` nodes."
        ),
        examples=[
            Example(input="edges = [[1,2],[1,3],[2,3]]", output="[2,3]"),
            Example(input="edges = [[1,2],[2,3],[3,4],[1,4],[1,5]]", output="[1,4]"),
        ],
        constraints=["n == edges.length", "3 <= n <= 1000", "edges[i].length == 2",
                     "1 <= ai < bi <= edges.length"],
        hints=[
            "Use Union-Find. If two nodes are already connected, the current edge is redundant.",
        ],
        solution_code="""def findRedundantConnection(edges):
    n = len(edges)
    parent = list(range(n + 1))
    rank = [0] * (n + 1)

    def find(x):
        if parent[x] != x:
            parent[x] = find(parent[x])
        return parent[x]

    def union(x, y):
        rx, ry = find(x), find(y)
        if rx == ry:
            return False
        if rank[rx] < rank[ry]:
            rx, ry = ry, rx
        parent[ry] = rx
        if rank[rx] == rank[ry]:
            rank[rx] += 1
        return True

    for u, v in edges:
        if not union(u, v):
            return [u, v]""",
        time_complexity="O(n α(n))",
        space_complexity="O(n)",
        viz_type="graph",
    ),

    # ─── SYSTEM DESIGN CODING ────────────────────────────────────────────────────
    Problem(
        id="lru-cache",
        title="LRU Cache",
        difficulty="Medium",
        pattern="System Design Coding",
        companies=["meta", "google", "amazon", "uber", "netflix"],
        description=(
            "Design a data structure that follows the constraints of a **Least Recently Used (LRU) cache**.\n\n"
            "Implement the `LRUCache` class:\n"
            "- `LRUCache(int capacity)` Initialize the LRU cache with **positive size** `capacity`.\n"
            "- `int get(int key)` Return the value of the `key` if the key exists, otherwise return `-1`.\n"
            "- `void put(int key, int value)` Update the value of the `key` if the key exists. Otherwise, add the "
            "`key-value` pair to the cache. If the number of keys exceeds the `capacity` from this operation, "
            "**evict the least recently used key**.\n\n"
            "The functions `get` and `put` must each run in `O(1)` average time complexity."
        ),
        examples=[
            Example(
                input='["LRUCache","put","put","get","put","get","put","get","get","get"]\n[[2],[1,1],[2,2],[1],[3,3],[2],[4,4],[1],[3],[4]]',
                output='[null,null,null,1,null,-1,null,-1,3,4]'
            ),
        ],
        constraints=["1 <= capacity <= 3000", "0 <= key <= 10^4", "0 <= value <= 10^5",
                     "At most 2 * 10^5 calls will be made to get and put."],
        hints=[
            "Use a doubly linked list + hash map.",
            "Move to front on access, remove from tail when over capacity.",
        ],
        solution_code="""class LRUCache:
    class Node:
        def __init__(self, key=0, val=0):
            self.key = key
            self.val = val
            self.prev = self.next = None

    def __init__(self, capacity):
        self.cap = capacity
        self.cache = {}
        self.head = self.Node()  # dummy head (most recent)
        self.tail = self.Node()  # dummy tail (least recent)
        self.head.next = self.tail
        self.tail.prev = self.head

    def _remove(self, node):
        node.prev.next = node.next
        node.next.prev = node.prev

    def _add_front(self, node):
        node.next = self.head.next
        node.prev = self.head
        self.head.next.prev = node
        self.head.next = node

    def get(self, key):
        if key in self.cache:
            node = self.cache[key]
            self._remove(node)
            self._add_front(node)
            return node.val
        return -1

    def put(self, key, value):
        if key in self.cache:
            self._remove(self.cache[key])
        node = self.Node(key, value)
        self._add_front(node)
        self.cache[key] = node
        if len(self.cache) > self.cap:
            lru = self.tail.prev
            self._remove(lru)
            del self.cache[lru.key]""",
        time_complexity="O(1) per operation",
        space_complexity="O(capacity)",
        viz_type="none",
    ),
    Problem(
        id="insert-delete-getrandom",
        title="Insert Delete GetRandom O(1)",
        difficulty="Medium",
        pattern="System Design Coding",
        companies=["meta", "google"],
        description=(
            "Implement the `RandomizedSet` class:\n"
            "- `RandomizedSet()` Initializes the `RandomizedSet` object.\n"
            "- `bool insert(int val)` Inserts an item `val` into the set if not present. Returns `true` if the item was "
            "not present, `false` otherwise.\n"
            "- `bool remove(int val)` Removes an item `val` from the set if present. Returns `true` if the item was "
            "present, `false` otherwise.\n"
            "- `int getRandom()` Returns a random element from the current set of elements (each element must have the "
            "same probability of being returned).\n\n"
            "You must implement the functions of the class such that each function works in **average** `O(1)` time complexity."
        ),
        examples=[
            Example(
                input='["RandomizedSet","insert","remove","insert","getRandom","remove","insert","getRandom"]\n[[],[1],[2],[2],[],[1],[2],[]]',
                output='[null,true,false,true,2,true,false,2]'
            ),
        ],
        constraints=["-2^31 <= val <= 2^31 - 1",
                     "At most 2 * 10^5 calls will be made to insert, remove, and getRandom.",
                     "There will be at least one element in the data structure when getRandom is called."],
        hints=[
            "Use a list (for O(1) random access) + a hash map (for O(1) lookup).",
            "For O(1) remove: swap element with last, update map, pop last.",
        ],
        solution_code="""import random

class RandomizedSet:
    def __init__(self):
        self.nums = []
        self.val_to_idx = {}

    def insert(self, val):
        if val in self.val_to_idx:
            return False
        self.val_to_idx[val] = len(self.nums)
        self.nums.append(val)
        return True

    def remove(self, val):
        if val not in self.val_to_idx:
            return False
        idx = self.val_to_idx[val]
        last = self.nums[-1]
        self.nums[idx] = last
        self.val_to_idx[last] = idx
        self.nums.pop()
        del self.val_to_idx[val]
        return True

    def getRandom(self):
        return random.choice(self.nums)""",
        time_complexity="O(1) per operation",
        space_complexity="O(n)",
        viz_type="none",
    ),

    # ─── INTERVALS ───────────────────────────────────────────────────────────────
    Problem(
        id="meeting-rooms-ii",
        title="Meeting Rooms II",
        difficulty="Medium",
        pattern="Intervals",
        companies=["meta", "google", "amazon"],
        description=(
            "Given an array of meeting time intervals `intervals` where `intervals[i] = [starti, endi]`, return the "
            "minimum number of conference rooms required."
        ),
        examples=[
            Example(input="intervals = [[0,30],[5,10],[15,20]]", output="2"),
            Example(input="intervals = [[7,10],[2,4]]", output="1"),
        ],
        constraints=["1 <= intervals.length <= 10^4", "0 <= starti < endi <= 10^6"],
        hints=[
            "Sort by start time. Use a min-heap to track end times.",
            "If current start >= heap top, reuse the room.",
        ],
        solution_code="""import heapq

def minMeetingRooms(intervals):
    if not intervals:
        return 0
    intervals.sort(key=lambda x: x[0])
    heap = []  # end times
    for start, end in intervals:
        if heap and heap[0] <= start:
            heapq.heapreplace(heap, end)
        else:
            heapq.heappush(heap, end)
    return len(heap)""",
        time_complexity="O(n log n)",
        space_complexity="O(n)",
        viz_type="array",
    ),
    Problem(
        id="merge-intervals",
        title="Merge Intervals",
        difficulty="Medium",
        pattern="Intervals",
        companies=["google", "meta", "amazon"],
        description=(
            "Given an array of `intervals` where `intervals[i] = [starti, endi]`, merge all overlapping intervals, "
            "and return an array of the non-overlapping intervals that cover all the intervals in the input."
        ),
        examples=[
            Example(input="intervals = [[1,3],[2,6],[8,10],[15,18]]", output="[[1,6],[8,10],[15,18]]"),
            Example(input="intervals = [[1,4],[4,5]]", output="[[1,5]]"),
        ],
        constraints=["1 <= intervals.length <= 10^4", "intervals[i].length == 2",
                     "0 <= starti <= endi <= 10^4"],
        hints=[
            "Sort intervals by start time.",
            "For each interval, merge with previous if overlap exists.",
        ],
        solution_code="""def merge(intervals):
    intervals.sort(key=lambda x: x[0])
    merged = [intervals[0]]
    for start, end in intervals[1:]:
        if start <= merged[-1][1]:
            merged[-1][1] = max(merged[-1][1], end)
        else:
            merged.append([start, end])
    return merged""",
        time_complexity="O(n log n)",
        space_complexity="O(n)",
        viz_type="array",
    ),
    Problem(
        id="non-overlapping-intervals",
        title="Non-overlapping Intervals",
        difficulty="Medium",
        pattern="Intervals",
        companies=["google"],
        description=(
            "Given an array of intervals `intervals` where `intervals[i] = [starti, endi]`, return the minimum number "
            "of intervals you need to remove to make the rest of the intervals non-overlapping."
        ),
        examples=[
            Example(input="intervals = [[1,2],[2,3],[3,4],[1,3]]", output="1"),
            Example(input="intervals = [[1,2],[1,2],[1,2]]", output="2"),
            Example(input="intervals = [[1,2],[2,3]]", output="0"),
        ],
        constraints=["1 <= intervals.length <= 10^5", "intervals[i].length == 2",
                     "-5 * 10^4 <= starti < endi <= 5 * 10^4"],
        hints=[
            "Greedy: sort by end time, keep the interval with earliest end.",
            "Remove intervals that overlap with the last kept interval.",
        ],
        solution_code="""def eraseOverlapIntervals(intervals):
    intervals.sort(key=lambda x: x[1])
    removed = 0
    prev_end = float('-inf')
    for start, end in intervals:
        if start < prev_end:
            removed += 1
        else:
            prev_end = end
    return removed""",
        time_complexity="O(n log n)",
        space_complexity="O(1)",
        viz_type="array",
    ),

    # ─── Additional problems to round out to 45+ ────────────────────────────────
    Problem(
        id="word-ladder",
        title="Word Ladder",
        difficulty="Hard",
        pattern="Graph Traversal",
        companies=["amazon", "google", "meta"],
        description=(
            "A **transformation sequence** from word `beginWord` to word `endWord` using a dictionary `wordList` is a "
            "sequence of words `beginWord -> s1 -> s2 -> ... -> sk` such that every adjacent pair of words differs by "
            "a single letter, and every `si` for `1 <= i <= k` is in `wordList`.\n\n"
            "Given two words, `beginWord` and `endWord`, and a dictionary `wordList`, return the **number of words** "
            "in the shortest transformation sequence from `beginWord` to `endWord`, or `0` if no such sequence exists."
        ),
        examples=[
            Example(input='beginWord = "hit", endWord = "cog", wordList = ["hot","dot","dog","lot","log","cog"]', output="5"),
            Example(input='beginWord = "hit", endWord = "cog", wordList = ["hot","dot","dog","lot","log"]', output="0"),
        ],
        constraints=["1 <= beginWord.length <= 10", "endWord.length == beginWord.length",
                     "1 <= wordList.length <= 5000", "wordList[i].length == beginWord.length"],
        hints=[
            "BFS from beginWord, try all single-character mutations.",
            "Use word set for O(1) lookup and remove visited words.",
        ],
        solution_code="""from collections import deque

def ladderLength(beginWord, endWord, wordList):
    word_set = set(wordList)
    if endWord not in word_set:
        return 0
    queue = deque([(beginWord, 1)])
    visited = {beginWord}
    while queue:
        word, length = queue.popleft()
        for i in range(len(word)):
            for c in 'abcdefghijklmnopqrstuvwxyz':
                new_word = word[:i] + c + word[i+1:]
                if new_word == endWord:
                    return length + 1
                if new_word in word_set and new_word not in visited:
                    visited.add(new_word)
                    queue.append((new_word, length + 1))
    return 0""",
        time_complexity="O(M² × N)",
        space_complexity="O(M² × N)",
        viz_type="graph",
    ),
    Problem(
        id="find-median-data-stream",
        title="Find Median from Data Stream",
        difficulty="Hard",
        pattern="Heap / Priority Queue",
        companies=["google", "meta", "amazon"],
        description=(
            "The **median** is the middle value in an ordered integer list. If the size of the list is even, there is "
            "no middle value and the median is the mean of the two middle values.\n\n"
            "Implement the `MedianFinder` class:\n"
            "- `MedianFinder()` initializes the `MedianFinder` object.\n"
            "- `void addNum(int num)` adds the integer `num` from the data stream to the data structure.\n"
            "- `double findMedian()` returns the median of all elements so far."
        ),
        examples=[
            Example(
                input='["MedianFinder","addNum","addNum","findMedian","addNum","findMedian"]\n[[],[1],[2],[],[3],[]]',
                output="[null,null,null,1.5,null,2.0]"
            ),
        ],
        constraints=["-10^5 <= num <= 10^5", "There will be at least one element in the data structure before calling findMedian.",
                     "At most 5 * 10^4 calls will be made to addNum and findMedian."],
        hints=[
            "Use two heaps: max-heap for lower half, min-heap for upper half.",
            "Balance heaps so sizes differ by at most 1.",
        ],
        solution_code="""import heapq

class MedianFinder:
    def __init__(self):
        self.small = []  # max-heap (negate values)
        self.large = []  # min-heap

    def addNum(self, num):
        heapq.heappush(self.small, -num)
        # Balance: move largest of small to large
        heapq.heappush(self.large, -heapq.heappop(self.small))
        # Keep small >= large in size
        if len(self.large) > len(self.small):
            heapq.heappush(self.small, -heapq.heappop(self.large))

    def findMedian(self):
        if len(self.small) > len(self.large):
            return -self.small[0]
        return (-self.small[0] + self.large[0]) / 2""",
        time_complexity="O(log n) addNum, O(1) findMedian",
        space_complexity="O(n)",
        viz_type="array",
    ),
    Problem(
        id="split-array-largest-sum",
        title="Split Array Largest Sum",
        difficulty="Hard",
        pattern="Binary Search",
        companies=["google", "meta"],
        description=(
            "Given an integer array `nums` and an integer `k`, split `nums` into `k` non-empty subarrays such that "
            "the largest sum of any subarray is **minimized**.\n\n"
            "Return the minimized largest sum of the split."
        ),
        examples=[
            Example(input="nums = [7,2,5,10,8], k = 2", output="18"),
            Example(input="nums = [1,2,3,4,5], k = 2", output="9"),
        ],
        constraints=["1 <= nums.length <= 1000", "0 <= nums[i] <= 10^6", "1 <= k <= min(50, nums.length)"],
        hints=[
            "Binary search on the answer (largest sum).",
            "For a given mid, greedily count the number of subarrays needed.",
        ],
        solution_code="""def splitArray(nums, k):
    def can_split(max_sum):
        count, curr = 1, 0
        for num in nums:
            if curr + num > max_sum:
                count += 1
                curr = num
            else:
                curr += num
        return count <= k

    left, right = max(nums), sum(nums)
    while left < right:
        mid = (left + right) // 2
        if can_split(mid):
            right = mid
        else:
            left = mid + 1
    return left""",
        time_complexity="O(n log(sum))",
        space_complexity="O(1)",
        viz_type="array",
    ),
    Problem(
        id="regular-expression-matching",
        title="Regular Expression Matching",
        difficulty="Hard",
        pattern="Dynamic Programming 2D",
        companies=["google", "meta"],
        description=(
            "Given an input string `s` and a pattern `p`, implement regular expression matching with support for `'.'` and `'*'` where:\n\n"
            "- `'.'` Matches any single character.\n"
            "- `'*'` Matches zero or more of the preceding element.\n\n"
            "The matching should cover the **entire** input string (not partial)."
        ),
        examples=[
            Example(input='s = "aa", p = "a"', output="false"),
            Example(input='s = "aa", p = "a*"', output="true"),
            Example(input='s = "ab", p = ".*"', output="true"),
        ],
        constraints=["1 <= s.length <= 20", "1 <= p.length <= 30",
                     "s contains only lowercase English letters.", "p contains only lowercase English letters, '.', and '*'."],
        hints=[
            "dp[i][j] = whether s[:i] matches p[:j].",
            "If p[j-1] == '*': dp[i][j] = dp[i][j-2] (zero match) or (dp[i-1][j] and match(s[i-1], p[j-2])).",
        ],
        solution_code="""def isMatch(s, p):
    m, n = len(s), len(p)
    dp = [[False] * (n + 1) for _ in range(m + 1)]
    dp[0][0] = True
    for j in range(2, n + 1):
        if p[j - 1] == '*':
            dp[0][j] = dp[0][j - 2]
    for i in range(1, m + 1):
        for j in range(1, n + 1):
            if p[j - 1] == '*':
                dp[i][j] = dp[i][j - 2]
                if p[j - 2] == '.' or p[j - 2] == s[i - 1]:
                    dp[i][j] = dp[i][j] or dp[i - 1][j]
            elif p[j - 1] == '.' or p[j - 1] == s[i - 1]:
                dp[i][j] = dp[i - 1][j - 1]
    return dp[m][n]""",
        time_complexity="O(m × n)",
        space_complexity="O(m × n)",
        viz_type="grid",
    ),
    Problem(
        id="flatten-binary-tree",
        title="Flatten Binary Tree to Linked List",
        difficulty="Medium",
        pattern="Trees",
        companies=["meta"],
        description=(
            "Given the `root` of a binary tree, flatten the tree into a 'linked list':\n\n"
            "- The 'linked list' should use the same `TreeNode` class where the `right` child pointer points to the "
            "next node in the list and the `left` child pointer is always `null`.\n"
            "- The 'linked list' should be in the same order as a **pre-order traversal** of the binary tree."
        ),
        examples=[
            Example(input="root = [1,2,5,3,4,null,6]", output="[1,null,2,null,3,null,4,null,5,null,6]"),
            Example(input="root = []", output="[]"),
        ],
        constraints=["The number of nodes in the tree is in the range [0, 2000].", "-100 <= Node.val <= 100"],
        hints=[
            "For each node, move left subtree to right, connect to right subtree.",
        ],
        solution_code="""def flatten(root):
    def dfs(node):
        if not node:
            return None
        left_tail = dfs(node.left)
        right_tail = dfs(node.right)
        if left_tail:
            left_tail.right = node.right
            node.right = node.left
            node.left = None
        return right_tail or left_tail or node
    dfs(root)""",
        time_complexity="O(n)",
        space_complexity="O(h)",
        viz_type="tree",
    ),
    Problem(
        id="number-of-connected-components",
        title="Number of Connected Components in an Undirected Graph",
        difficulty="Medium",
        pattern="Union Find",
        companies=["linkedin", "google"],
        description=(
            "You have a graph of `n` nodes. You are given an integer `n` and an array `edges` where "
            "`edges[i] = [ai, bi]` indicates that there is an edge between `ai` and `bi` in the graph.\n\n"
            "Return the number of connected components in the graph."
        ),
        examples=[
            Example(input="n = 5, edges = [[0,1],[1,2],[3,4]]", output="2"),
            Example(input="n = 5, edges = [[0,1],[1,2],[2,3],[3,4]]", output="1"),
        ],
        constraints=["1 <= n <= 2000", "1 <= edges.length <= 5000", "edges[i].length == 2",
                     "0 <= ai <= bi < n", "ai != bi", "There are no repeated edges."],
        hints=[
            "Use Union-Find or DFS/BFS to count connected components.",
        ],
        solution_code="""def countComponents(n, edges):
    parent = list(range(n))
    rank = [0] * n

    def find(x):
        if parent[x] != x:
            parent[x] = find(parent[x])
        return parent[x]

    def union(x, y):
        rx, ry = find(x), find(y)
        if rx == ry:
            return 0
        if rank[rx] < rank[ry]:
            rx, ry = ry, rx
        parent[ry] = rx
        if rank[rx] == rank[ry]:
            rank[rx] += 1
        return 1

    components = n
    for u, v in edges:
        components -= union(u, v)
    return components""",
        time_complexity="O(n α(n))",
        space_complexity="O(n)",
        viz_type="graph",
    ),
    Problem(
        id="subsets-ii",
        title="Subsets II",
        difficulty="Medium",
        pattern="Backtracking",
        companies=["meta", "amazon"],
        description=(
            "Given an integer array `nums` that may contain duplicates, return all possible subsets (the power set).\n\n"
            "The solution set **must not** contain duplicate subsets. Return the solution in **any order**."
        ),
        examples=[
            Example(input="nums = [1,2,2]", output="[[],[1],[1,2],[1,2,2],[2],[2,2]]"),
            Example(input="nums = [0]", output="[[],[0]]"),
        ],
        constraints=["1 <= nums.length <= 10", "-10 <= nums[i] <= 10"],
        hints=[
            "Sort array first. Skip duplicates at same recursion level.",
        ],
        solution_code="""def subsetsWithDup(nums):
    nums.sort()
    result = []

    def backtrack(start, path):
        result.append(path[:])
        for i in range(start, len(nums)):
            if i > start and nums[i] == nums[i - 1]:
                continue
            path.append(nums[i])
            backtrack(i + 1, path)
            path.pop()

    backtrack(0, [])
    return result""",
        time_complexity="O(n × 2^n)",
        space_complexity="O(n × 2^n)",
        viz_type="array",
    ),
    Problem(
        id="reorganize-string",
        title="Reorganize String",
        difficulty="Medium",
        pattern="Heap / Priority Queue",
        companies=["google", "meta"],
        description=(
            "Given a string `s`, rearrange the characters of `s` so that any two adjacent characters are not the same.\n\n"
            "Return any possible rearrangement of `s` or return `\"\"` if not possible."
        ),
        examples=[
            Example(input='s = "aab"', output='"aba"'),
            Example(input='s = "aaab"', output='""'),
        ],
        constraints=["1 <= s.length <= 500", "s consists of lowercase English letters."],
        hints=[
            "Greedily pick the most frequent character that is not the same as the previous.",
            "Use a max-heap by frequency.",
        ],
        solution_code="""from collections import Counter
import heapq

def reorganizeString(s):
    counts = Counter(s)
    heap = [(-cnt, ch) for ch, cnt in counts.items()]
    heapq.heapify(heap)
    result = []
    prev_cnt, prev_ch = 0, ''
    while heap:
        cnt, ch = heapq.heappop(heap)
        result.append(ch)
        if prev_cnt < 0:
            heapq.heappush(heap, (prev_cnt, prev_ch))
        prev_cnt, prev_ch = cnt + 1, ch
    return ''.join(result) if len(result) == len(s) else ''""",
        time_complexity="O(n log k)",
        space_complexity="O(k)",
        viz_type="array",
    ),
    Problem(
        id="employee-free-time",
        title="Employee Free Time",
        difficulty="Hard",
        pattern="Intervals",
        companies=["airbnb", "google"],
        description=(
            "We are given a list `schedule` of employees, which represents the working time for each employee.\n\n"
            "Each employee has a list of non-overlapping `Intervals`, and these intervals are in sorted order.\n\n"
            "Return the list of finite intervals representing **common, positive-length free time** for all employees, "
            "also in sorted order."
        ),
        examples=[
            Example(input="schedule = [[[1,3],[6,7]],[[2,4]],[[2,5],[9,12]]]", output="[[5,6],[7,9]]"),
        ],
        constraints=["1 <= schedule.length , schedule[i].length <= 50",
                     "0 <= schedule[i].start < schedule[i].end <= 10^8"],
        hints=[
            "Flatten all intervals, sort by start time, then find gaps.",
        ],
        solution_code="""def employeeFreeTime(schedule):
    all_intervals = sorted(
        [interval for employee in schedule for interval in employee],
        key=lambda x: x.start
    )
    result = []
    prev_end = all_intervals[0].end
    for interval in all_intervals[1:]:
        if interval.start > prev_end:
            result.append(Interval(prev_end, interval.start))
        prev_end = max(prev_end, interval.end)
    return result""",
        time_complexity="O(n log n)",
        space_complexity="O(n)",
        viz_type="array",
    ),
    Problem(
        id="alien-dictionary",
        title="Alien Dictionary",
        difficulty="Hard",
        pattern="Graph Traversal",
        companies=["meta", "google", "airbnb"],
        description=(
            "There is a new alien language that uses the English alphabet. However, the order among the letters is "
            "unknown to you.\n\n"
            "You are given a list of strings `words` from the alien language's dictionary, where the strings in "
            "`words` are **sorted lexicographically** by the rules of this new language.\n\n"
            "Return a string of the unique letters in the new alien language sorted in **lexicographically increasing "
            "order** by the new language's rules. If there is no solution, return `\"\"`. If there are multiple solutions, "
            "return **any of them**."
        ),
        examples=[
            Example(input='words = ["wrt","wrf","er","ett","rftt"]', output='"wertf"'),
            Example(input='words = ["z","x"]', output='"zx"'),
            Example(input='words = ["z","x","z"]', output='""', explanation="The order is invalid."),
        ],
        constraints=["1 <= words.length <= 100", "1 <= words[i].length <= 100",
                     "words[i] consists of only lowercase English letters."],
        hints=[
            "Build a directed graph from character ordering constraints.",
            "Topological sort; cycle means invalid order.",
        ],
        solution_code="""from collections import defaultdict, deque

def alienOrder(words):
    # Build adjacency list and in-degree map
    adj = defaultdict(set)
    in_degree = {ch: 0 for word in words for ch in word}
    for i in range(len(words) - 1):
        w1, w2 = words[i], words[i + 1]
        min_len = min(len(w1), len(w2))
        if len(w1) > len(w2) and w1[:min_len] == w2[:min_len]:
            return ""
        for j in range(min_len):
            if w1[j] != w2[j]:
                if w2[j] not in adj[w1[j]]:
                    adj[w1[j]].add(w2[j])
                    in_degree[w2[j]] += 1
                break
    queue = deque([ch for ch in in_degree if in_degree[ch] == 0])
    result = []
    while queue:
        ch = queue.popleft()
        result.append(ch)
        for neighbor in adj[ch]:
            in_degree[neighbor] -= 1
            if in_degree[neighbor] == 0:
                queue.append(neighbor)
    return ''.join(result) if len(result) == len(in_degree) else """"",
        time_complexity="O(C) where C = total chars",
        space_complexity="O(1) bounded by 26 chars",
        viz_type="graph",
    ),
]


def get_all_problems() -> list[Problem]:
    return PROBLEMS


def get_problem_by_id(problem_id: str) -> Problem | None:
    for p in PROBLEMS:
        if p.id == problem_id:
            return p
    return None


def get_patterns() -> dict[str, int]:
    counts: dict[str, int] = {}
    for p in PROBLEMS:
        counts[p.pattern] = counts.get(p.pattern, 0) + 1
    return counts


def get_companies() -> dict[str, int]:
    counts: dict[str, int] = {}
    for p in PROBLEMS:
        for c in p.companies:
            counts[c] = counts.get(c, 0) + 1
    return counts
