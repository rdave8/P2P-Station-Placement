import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import Circle
import argparse
import random

class ProblemInstance:
    def __init__(self, num_residents, num_stations, resident_distribution, mpsd, threshold, std_dev, seed=None):
        self.num_residents = num_residents
        self.num_stations = num_stations
        self.mpsd = mpsd
        self.threshold = threshold

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

    def distance(self, loc1, loc2):
        return np.sqrt((loc1[0] - loc2[0])**2 + (loc1[1] - loc2[1])**2)

    def solve(self):
        self.selected_locations = set()
        self.covered_residents = set()
        stations_left = self.num_stations
        
        while stations_left > self.num_stations / 2:
            max_coverage = -1
            best_location = -1
            for i in range(self.num_residents):
                if i in self.selected_locations:
                    continue
                new_coverage = len(set(self.residents_within_mpsd[i]) - self.covered_residents)
                likelihood = self.getInstallationLikelihoodSimplified(i)
                if new_coverage  > max_coverage and likelihood > 0:
                    max_coverage = new_coverage
                    best_location = i
            self.selected_locations.add(best_location)
            self.covered_residents.update(self.residents_within_mpsd[best_location])
            stations_left -= 1

        while stations_left > 0:
            max_coverage = -1
            best_location = -1
            for i in range(self.num_residents):
                if i in self.selected_locations:
                    continue
                coverage = len(set(self.residents_within_mpsd[i]) & self.covered_residents)
                likelihood = self.getInstallationLikelihoodSimplified(i)
                if coverage * likelihood > max_coverage:
                    max_coverage = coverage * likelihood
                    best_location = i
            self.selected_locations.add(best_location)
            self.covered_residents.update(self.residents_within_mpsd[best_location])
            stations_left -= 1

        num_trials = 5000
        num_successes = 0

        for _ in range(num_trials):
            num_covered = set()
            for location in self.selected_locations:
                if random.random() < self.getInstallationLikelihoodSimplified(location):
                    num_covered.update(self.residents_within_mpsd[location])
            if len(num_covered) >= self.threshold * self.num_residents:
                num_successes += 1

        print('Selected Installation Locations:', self.selected_locations)
        print()
        print('Covered Residents:', self.covered_residents)
        print()
        print('Approximate Probability of Covering Threshold:', num_successes / num_trials)

    def getInstallationLikelihoodSimplified(self, location):
        return 0.5

    def getInstallationLikelihood(self, location):
        scale_factor = 5
        mean = scale_factor * len(self.residents_within_mpsd[location]) / self.num_residents
        return np.clip(np.random.normal(mean, 0.05), 0, 1)

    def plot(self, filename=None):
        fig, ax = plt.subplots()

        for loc in self.selected_locations:
            circle = Circle((self.resident_locations[loc][0], self.resident_locations[loc][1]), self.mpsd, fill=True, color='green', linewidth=0, alpha=0.4)
            ax.add_patch(circle)

        ax.scatter(self.resident_locations[:, 0], self.resident_locations[:, 1], color='blue', label='Resident Locations', s=10)

        ax.legend()
        plt.axis('equal')
        plt.xlabel('x')
        plt.ylabel('y')
        plt.title('Charging Station Problem')

        if filename:
            plt.savefig(filename)
        else:
            plt.show()

def main():
    parser = argparse.ArgumentParser(description="Create and solve Charging Station Problem")
    parser.add_argument("--num_residents", type=int, default=500, help="Number of residents")
    parser.add_argument("--num_stations", type=int, default=50, help="Number of stations available")
    parser.add_argument("--mpsd", type=float, default=6, help="Maximum serviceable distance")
    parser.add_argument("--threshold", type=float, default=0.80, help="Threshold for solving the problem")
    parser.add_argument("--resident_distribution", choices=["uniform", "normal"], default="normal", help="Distribution of resident locations")
    parser.add_argument("--std_dev", type=float, default=10, help="Standard deviation for normal distribution of resident locations")
    parser.add_argument("--seed", type=int, default=None, help="Random seed for reproducibility")

    args = parser.parse_args()

    problem = ProblemInstance(args.num_residents, args.num_stations, args.resident_distribution, args.mpsd, args.threshold, args.std_dev, args.seed)

    problem.solve()
    
    problem.plot()

if __name__ == "__main__":
    main()