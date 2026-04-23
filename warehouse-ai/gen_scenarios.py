import json
import os

def save_json(name, data):
    with open(f"scenarios/{name}.json", "w") as f:
        json.dump(data, f, indent=4)

os.makedirs("scenarios", exist_ok=True)

# 01: Basic
save_json("scenario_01", {
    "width": 10, "height": 10, "robot_start": [0,0], "items": [[9,9]], "shelves": [[2,2,6,1]], "obstacles": []
})

# 02: Standard Layout
save_json("scenario_02", {
    "width": 15, "height": 15, "robot_start": [1,1], "items": [[13,13]], "shelves": [[3,3,2,8], [7,3,2,8], [11,3,2,8]], "obstacles": []
})

# 03: Maze
save_json("scenario_03", {
    "width": 15, "height": 15, "robot_start": [1,1], "items": [[13,1]], "shelves": [], "obstacles": [[2,0,1,10], [4,5,1,10], [6,0,1,10], [8,5,1,10], [10,0,1,10]]
})

# 04: Scattered
save_json("scenario_04", {
    "width": 20, "height": 15, "robot_start": [10,7], "items": [[1,1], [18,13], [1,13], [18,1]], "shelves": [], "obstacles": [[5,5,2,2], [15,5,2,2], [5,10,2,2], [15,10,2,2]]
})

# 05: Bottleneck
save_json("scenario_05", {
    "width": 20, "height": 10, "robot_start": [2,5], "items": [[18,5]], "shelves": [], "obstacles": [[0,0,10,4], [0,6,10,4], [11,0,9,4], [11,6,9,4]]
})

# 06: Spiral
save_json("scenario_06", {
    "width": 15, "height": 15, "robot_start": [0,0], "items": [[7,7]], "shelves": [], "obstacles": [
        [0, 14, 15, 1], [14, 0, 1, 14], [0, 0, 14, 1], [0, 1, 1, 12], [2, 12, 10, 1],
        [12, 2, 1, 10], [2, 2, 10, 1], [2, 3, 1, 8], [4, 10, 6, 1]
    ]
})

# 07-10 variants
save_json("scenario_07", {"width": 30, "height": 20, "robot_start": [1,1], "items": [[28,18]], "shelves": [[5,5,2,10], [10,5,2,10], [15,5,2,10], [20,5,2,10], [25,5,2,10]], "obstacles": []})
save_json("scenario_08", {"width": 20, "height": 20, "robot_start": [0,19], "items": [[19,0]], "shelves": [], "obstacles": [[0,15,15,1], [5,10,15,1], [0,5,15,1]]})
save_json("scenario_09", {"width": 15, "height": 15, "robot_start": [7,7], "items": [[0,0], [14,14], [0,14], [14,0]], "shelves": [[2,2,2,2], [11,11,2,2]], "obstacles": []})
save_json("scenario_10", {"width": 20, "height": 20, "robot_start": [1,1], "items": [[18,18]], "shelves": [[x,y,1,1] for x in range(2,18,2) for y in range(2,18,2)], "obstacles": []})

print("10 scenarios generated.")
