import argparse
from ProblemInstance import ProblemInstance

PRESET_PARAMETERS = {
    'uniform1': {'num_residents': 100, 'mpsd': 0.2, 'threshold': 0.80, 'resident_distribution': 'uniform', 'std_dev': 'N/A', 'seed': 8},
    'uniform2': {'num_residents': 1000, 'mpsd': 0.2, 'threshold': 0.90, 'resident_distribution': 'uniform', 'std_dev': 'N/A', 'seed': 8},
    'uniform3': {'num_residents': 5000, 'mpsd': 0.2, 'threshold': 0.90, 'resident_distribution': 'uniform', 'std_dev': 'N/A', 'seed': 8},
    'normal1': {'num_residents': 100, 'mpsd': 0.5, 'threshold': 0.80, 'resident_distribution': 'normal', 'std_dev': 1, 'seed': 8},
    'normal2': {'num_residents': 1000, 'mpsd': 3, 'threshold': 0.90, 'resident_distribution': 'normal', 'std_dev': 5, 'seed': 8},
    'normal3': {'num_residents': 5000, 'mpsd': 40, 'threshold': 0.80, 'resident_distribution': 'normal', 'std_dev': 100, 'seed': 8},
}

def main():
    parser = argparse.ArgumentParser(description="Generate, solve, and plot preset problem instances")
    parser.add_argument("keyword", choices=PRESET_PARAMETERS.keys(), help="Keyword for preset problem instance")

    args = parser.parse_args()

    parameters = PRESET_PARAMETERS[args.keyword]
    problem = ProblemInstance(parameters['num_residents'], parameters['resident_distribution'], parameters['mpsd'], parameters['std_dev'], parameters['seed'])
    problem.solve(parameters['threshold'])

    print("Residents: ", parameters['num_residents'])
    print("Distribution: ", parameters['resident_distribution'])
    print("Threshold: ", parameters['threshold'])
    print("MPSD: ", parameters['mpsd'])

    print("Selected Residents:", problem.selected_locations)
    print("Total Cost:", problem.total_cost)

    problem.plot(args.keyword)

if __name__ == "__main__":
    main()
