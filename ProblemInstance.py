import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import Circle
import argparse

class ProblemInstance:
    def __init__(self, num_residents, resident_distribution, mpsd, std_dev, seed=None):
        self.num_residents = num_residents
        self.mpsd = mpsd

        if seed is not None:
            np.random.seed(seed)

        if resident_distribution == 'uniform':
            self.resident_locations = np.random.rand(num_residents, 2)
        elif resident_distribution == 'normal':
            mean = 0
            self.resident_locations = np.random.normal(mean, std_dev, (num_residents, 2))
        else:
            raise ValueError("Invalid resident distribution specified.")

        self.residents_within_mpsd = {}
        for i in range(num_residents):
            self.residents_within_mpsd[i] = [j for j in range(num_residents) if self.distance(self.resident_locations[i], self.resident_locations[j]) <= mpsd]

        self.initial_costs = num_residents - np.array([len(self.residents_within_mpsd[loc]) for loc in range(num_residents)])

    def distance(self, loc1, loc2):
        return np.sqrt((loc1[0] - loc2[0])**2 + (loc1[1] - loc2[1])**2)

    def solve(self, threshold=1.0):
        uncovered_residents = set(range(self.num_residents))
        selected_locations = set()
        total_cost = 0
        uncovered_resident_goal = (1 - threshold) * self.num_residents

        while len(uncovered_residents) > uncovered_resident_goal:
            min_ratio = float('inf')
            selected_location = None

            for resident in list(uncovered_residents):
                residents_covered = [r for r in self.residents_within_mpsd[resident] if r in uncovered_residents]
                ratio = self.initial_costs[resident] / len(residents_covered)

                if ratio < min_ratio:
                    min_ratio = ratio
                    selected_location = resident

            selected_locations.add(selected_location)
            total_cost += self.initial_costs[selected_location]

            uncovered_residents = uncovered_residents - set(self.residents_within_mpsd[selected_location])

        self.selected_locations = selected_locations
        self.total_cost = total_cost

    def plot(self, filename=None):
        fig, ax = plt.subplots()

        ax.scatter(self.resident_locations[:, 0], self.resident_locations[:, 1], color='blue', label='Resident Locations', s=10)

        for loc in self.selected_locations:
            ax.scatter(self.resident_locations[loc][0], self.resident_locations[loc][1], color='red', s=15)
            circle = Circle((self.resident_locations[loc][0], self.resident_locations[loc][1]), self.mpsd, fill=False, color='red', linewidth=0.8)
            ax.add_patch(circle)

        ax.set_aspect('equal', adjustable='box')
        ax.set_title('Charging Station Locations with Coverage Circles')
        
        if filename != None:
            plt.savefig("./Figures/" + filename + ".png")
            
        plt.show()

def main():
    parser = argparse.ArgumentParser(description="Create and solve Charging Station Problem")
    parser.add_argument("--num_residents", type=int, default=1000, help="Number of residents")
    parser.add_argument("--mpsd", type=float, default=3, help="Maximum serviceable distance")
    parser.add_argument("--threshold", type=float, default=0.90, help="Threshold for solving the problem")
    parser.add_argument("--resident_distribution", choices=["uniform", "normal"], default="normal", help="Distribution of resident locations")
    parser.add_argument("--std_dev", type=float, default=10, help="Standard deviation for normal distribution of resident locations")
    parser.add_argument("--seed", type=int, default=None, help="Random seed for reproducibility")

    args = parser.parse_args()

    problem = ProblemInstance(args.num_residents, args.resident_distribution, args.mpsd, args.std_dev, args.seed)
    problem.solve(args.threshold)

    print("Selected Locations (Residents):", problem.selected_locations)
    print("Total Cost:", problem.total_cost)
    
    problem.plot()

if __name__ == "__main__":
    main()