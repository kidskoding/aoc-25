from collections import deque

def prob09_1() -> int:
    max_area = 0
    coords = []
    with open('./input/prob09.txt') as f:
        lines = f.readlines()
        for line in lines:
            coord_str = line.strip()
            coord = coord_str.split(',')
            coord = (int(coord[0]), int(coord[1]))
            
            coords.append(coord)

    for i in range(len(coords)):
        for j in range(i, len(coords)):
            first = coords[i]
            second = coords[j]

            area = (abs(second[0] - first[0]) + 1) * (abs(second[1] - first[1]) + 1)
            max_area = max(max_area, area)
            
    return max_area

def prob09_2() -> int:
    max_area = 0
    coords = []
    with open('./input/prob09.txt') as f:
        lines = f.readlines()
        for line in lines:
            coord_str = line.strip()
            coord = coord_str.split(',')
            coord = (int(coord[0]), int(coord[1]))

            coords.append(coord)

    set_x, set_y = set(), set()
    for x, y in coords:
        set_x.add(x)
        set_x.add(x + 1)

        set_y.add(y)
        set_y.add(y + 1)

    lst_x = sorted(set_x)
    lst_y = sorted(set_y)

    x_to_idx = {x: i + 1 for i, x in enumerate(lst_x)}
    y_to_idx = {y: i + 1 for i, y in enumerate(lst_y)}
    
    grid = [[0] * (len(lst_x) + 2) for _ in range(len(lst_y) + 2)]
    for i in range(len(coords)):
        x1, y1 = coords[i]
        x2, y2 = coords[(i + 1) % len(coords)]

        c1, r1 = x_to_idx[x1], y_to_idx[y1]
        c2, r2 = x_to_idx[x2], y_to_idx[y2]

        for c in range(min(c1, c2), max(c1, c2) + 1):
            grid[r1][c] = 1
        
        for r in range(min(r1, r2), max(r1, r2) + 1):
            grid[r][c1] = 1
   
    rows = len(grid)
    cols = len(grid[0])

    grid[0][0] = 2
    queue = deque([(0, 0)])
    DIRECTIONS = [(1, 0), (-1, 0), (0, 1), (0, -1)]
    while queue:
        r, c = queue.popleft()
        for dr, dc in DIRECTIONS:
            nr, nc = r + dr, c + dc
            if 0 <= nr < rows and 0 <= nc < cols and grid[nr][nc] == 0:
                grid[nr][nc] = 2
                queue.append((nr, nc))

    for i in range(len(coords)):
        for j in range(i, len(coords)):
            first = coords[i]
            second = coords[j]

            area = (abs(second[0] - first[0]) + 1) * (abs(second[1] - first[1]) + 1)
            if area <= max_area:
                continue

            c1 = x_to_idx[first[0]]
            c2 = x_to_idx[second[0]]
            r1 = y_to_idx[first[1]]
            r2 = y_to_idx[second[1]]

            valid = True
            for r in range(min(r1, r2), max(r1, r2) + 1):
                for c in range(min(c1, c2), max(c1, c2) + 1):
                    if grid[r][c] == 2:
                        valid = False
                        break

                if not valid:
                    break

            if not valid:
                continue

            max_area = area

    return max_area
