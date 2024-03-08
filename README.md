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
- uniform3
- normal1
- normal2
- normal3

## Instructions for Custom Instances

```
pip install -r requirements.txt
```

```
python ProblemInstance.py --num_residents [0+] --mpsd 5 --threshold [0-1] --resident_distribution [uniform/normal] --std_dev [None/0+] --seed [None/0+]
```