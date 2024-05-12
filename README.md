# P2P Drone Delivery Charging Station Placemnt

## Instructions for Running Preset Instances

```
pip install -r requirements.txt
```

```
python instances.py [instance]
```

### The current available set of intances:
- uniform1
- uniform2
- normal1
- normal2

## Instructions for Custom Instances

```
pip install -r requirements.txt
```

```
python ProblemInstance.py --num_residents [0+] --num_stations [0+] --mpsd [0+] --threshold [0-1] --resident_distribution [uniform/normal] --std_dev [None/0+] --seed [None/0+]
```