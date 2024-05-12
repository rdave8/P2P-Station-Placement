import argparse
from probleminstance import ProblemInstance

PRESET_PARAMETERS = {
    'uniform1': {'num_residents': 100, 'num_stations': 15, 'mpsd': 0.2, 'threshold': 0.70, 'resident_distribution': 'uniform', 'std_dev': 'N/A', 'seed': 8},
    'uniform2': {'num_residents': 1000, 'num_stations': 30, 'mpsd': 0.16, 'threshold': 0.60, 'resident_distribution': 'uniform', 'std_dev': 'N/A', 'seed': 8},
    'normal1': {'num_residents': 100, 'num_stations': 12, 'mpsd': 1, 'threshold': 0.80, 'resident_distribution': 'normal', 'std_dev': 1, 'seed': 8},
    'normal2': {'num_residents': 1000, 'num_stations': 50, 'mpsd': 5, 'threshold': 0.90, 'resident_distribution': 'normal', 'std_dev': 5, 'seed': 8},
}

def main():
    parser = argparse.ArgumentParser(description="Generate, solve, and plot preset problem instances")
    parser.add_argument("keyword", choices=PRESET_PARAMETERS.keys(), help="Keyword for preset problem instance")

    args = parser.parse_args()

    parameters = PRESET_PARAMETERS[args.keyword]
    problem = ProblemInstance(parameters['num_residents'], parameters['num_stations'], parameters['resident_distribution'], parameters['mpsd'], parameters['threshold'], parameters['std_dev'], parameters['seed'])
    problem.solve()

    print("Residents: ", parameters['num_residents'])
    print("Distribution: ", parameters['resident_distribution'])
    print("Threshold: ", parameters['threshold'])
    print("MPSD: ", parameters['mpsd'])

    problem.plot('./Figures/' + args.keyword)
    # problem.plot()

if __name__ == "__main__":
    main()
