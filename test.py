from typing import List

# nums = [2, 100, 83, 169, 59, 151, 180, 107, 150, 199, 198, 81, 190, 127, 145, 86, 153, 2, 70, 144, 161, 143, 181, 142, 100, 113, 139, 12, 60, 154, 161, 9, 5, 128, 35, 5, 125, 13, 40, 137, 74, 50, 136, 52, 159, 15, 164, 23, 135, 53, 98, 143, 129, 47, 43, 151, 61, 120, 90, 93, 25, 111, 180, 123, 137, 1, 56, 164, 60, 165, 39, 114, 161, 176, 192, 39, 172, 22, 182, 74, 12, 143, 58, 67, 178, 134, 82, 95, 155, 29, 195, 181, 78, 3, 95, 167, 198, 63, 16, 55]
# nums = [-3,4,3,90]
nums = [3, 2, 4]
# nums = [3,3]
# nums = [2,7,11,15]


class Solution:
    def twoSum(self, nums: List[int], target: int) -> List[int]:
        def binary_search(arr, target):
            low = 0
            high = len(arr) - 1

            while low <= high:
                mid = (low + high) // 2
                
                if arr[mid] == target:
                    return mid  # Target found, return its index
                elif target < arr[mid]:
                    high = mid - 1  # Target is in the left half
                else:
                    low = mid + 1   # Target is in the right half
                    
            return -1  # Target not found in the list

        positions = []
        for i in range(len(nums)):
            nums_copy = nums.copy()
            nums_copy.pop(i)

            for j in range(i, len(nums_copy)):
                if j == i:
                    v1 = nums[i]
                else:
                    v2 = target - v1
                    pos = binary_search(nums_copy, v2)
                    if pos >= 0:
                        positions.append(j)
                        positions.append(pos)
                        return positions
        return positions

positions = Solution().twoSum(nums=nums, target=6)
print(positions)