from collections import deque

def prob10_1() -> int:
    total = 0
    with open('./input/prob10.txt') as f:
        for line in f:
            parts = line.split()
            
            target = parts[0]
            schematics = parts[1:-1]

            target = target.strip("[]")
            parsed_schematics = []
            for schematic in schematics:
                schematic = schematic.strip("()")
                nums = list(map(int, schematic.split(",")))
                parsed_schematics.append(nums)

            target_mask = 0
            for i, ch in enumerate(target):
                if ch == '#':
                    target_mask |= (1 << i)

            queue = deque([(0, 0)])
            visited = {0}
            while queue:
                curr_mask, presses = queue.popleft()
                if curr_mask == target_mask:
                    total += presses
                    break

                for schematic in parsed_schematics:
                    button_mask = 0

                    for idx in schematic:
                        button_mask |= (1 << idx)

                    next_mask = curr_mask ^ button_mask
                    if next_mask not in visited:
                        visited.add(next_mask)
                        queue.append((next_mask, presses + 1))

    return total

def prob10_2() -> int:
    total = 0
    def dfs(button_index, current_counters, presses):
        nonlocal best
        if presses >= best:
            return
        
        if button_index == len(parsed_schematics):
            if current_counters == target_counters:
                best = min(best, presses)
            return

        state = (button_index, current_counters)
        if state in memo and memo[state] <= presses:
            return

        schematic = parsed_schematics[button_index]
        max_presses = min(
            target_counters[idx] - current_counters[idx]
            for idx in schematic
        )

        memo[state] = presses
        
        for k in range(max_presses + 1):
            new_counters = list(current_counters)
            for idx in schematic:
                new_counters[idx] += k            
            new_counters = tuple(new_counters)

            dfs(button_index + 1, new_counters, presses + k)
            
    with open('./input/prob10.txt') as f:
        for line in f:
            parts = line.split()
            
            target = parts[0]
            schematics = parts[1:-1]
            joltage = parts[-1]

            target = target.strip("[]")
            parsed_schematics = []
            for schematic in schematics:
                schematic = schematic.strip("()")
                nums = list(map(int, schematic.split(",")))
                parsed_schematics.append(nums)

            joltage = joltage.strip("{}")
            target_counters = tuple(map(int, joltage.split(",")))

            start = tuple(0 for _ in target_counters)
            best = float('inf')
            memo = {}
            dfs(0, start, 0)

            total += best
        
    return int(total)
