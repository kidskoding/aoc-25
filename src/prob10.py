from collections import deque, defaultdict

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

    def min_presses(b: tuple) -> float:
        if all(x == 0 for x in b):
            return 0

        if b in dp:
            return dp[b]

        b_parity = tuple(x % 2 for x in b)
        best = float('inf')

        for effect, cost in by_parity.get(b_parity, {}).items():
            if any(b[i] < effect[i] for i in range(n)):
                continue

            next_b = tuple((b[i] - effect[i]) // 2 for i in range(n))
            best = min(best, cost + 2 * min_presses(next_b))

        dp[b] = best
        return best

    with open('./input/prob10.txt') as f:
        for line in f:
            parts = line.split()
            
            schematics = parts[1:-1]
            joltage = parts[-1]

            parsed_schematics = []
            for schematic in schematics:
                schematic = schematic.strip("()")
                nums = list(map(int, schematic.split(",")))
                parsed_schematics.append(nums)

            joltage = joltage.strip("{}")
            target_counters = tuple(map(int, joltage.split(",")))
            n, m = len(target_counters), len(parsed_schematics)
            by_parity = defaultdict(dict)

            for mask in range(1 << m):
                effect = [0] * n
                for j in range(m):
                    if (mask >> j) & 1:
                        for idx in parsed_schematics[j]:
                            effect[idx] += 1

                effect = tuple(effect)
                parity = tuple(x % 2 for x in effect)
                cost = mask.bit_count()
                if cost < by_parity[parity].get(effect, float('inf')):
                    by_parity[parity][effect] = cost

            dp = {}
            total += min_presses(target_counters)

    return int(total)

