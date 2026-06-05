from logging_middleware.log import Log

class VehicleService:
    def __init__(self):
        Log("backend", "info", "service", "Initilializing VehicleService")
        
    @staticmethod
    def knapsack(tasks, capacity):
        n = len(tasks)
        dp = [[0] * (capacity + 1) for _ in range(n + 1)]

        for i in range(1, n + 1):
            duration = tasks[i - 1]["Duration"]
            impact = tasks[i - 1]["Impact"]

            for h in range(capacity + 1):
                if duration <= h:
                    dp[i][h] = max(
                        dp[i - 1][h],
                        dp[i - 1][h - duration] + impact
                    )
                else:
                    dp[i][h] = dp[i - 1][h]
        selected = []
        h = capacity

        for i in range(n, 0, -1):
            if dp[i][h] != dp[i - 1][h]:
                selected.append(tasks[i - 1])
                h -= tasks[i - 1]["Duration"]

        selected.reverse()

        return {
            "max_impact": dp[n][capacity],
            "selected_tasks": selected,
            "hours_used": sum(t["Duration"] for t in selected)
        }
    
    @staticmethod    
    def computer_per_depo(vehicles_data, depots_data):
        Log("backend", "info", "service", "Computing per depo")
        tasks = vehicles_data["vehicles"]

        for depot in depots_data["depots"]:
            depot_id = depot["ID"]
            capacity = depot["MechanicHours"]

            result = VehicleService.knapsack(tasks, capacity)

            print(f"\n=== DEPOT {depot_id} ===")
            print("Capacity:", capacity)
            print("Max Impact:", result["max_impact"])
            print("Hours Used:", result["hours_used"])
            print("Tasks Selected:", len(result["selected_tasks"]))
            
        for task in result["selected_tasks"]:
            print(task["TaskID"])
        
    @staticmethod
    def compute_overall(vehicles_data, depots_data):
        Log("backend", "info", "service", "Computing overall")
        tasks = vehicles_data["vehicles"]

        total_capacity = sum(
            depot["MechanicHours"]
            for depot in depots_data["depots"]
        )

        result = VehicleService.knapsack(tasks, total_capacity)

        print("=== OVERALL OPTIMIZATION ===")
        print("Capacity:", total_capacity)
        print("Max Impact:", result["max_impact"])
        print("Hours Used:", result["hours_used"])

        print("\nSelected Tasks:")
        for task in result["selected_tasks"]:
            print(task["TaskID"])