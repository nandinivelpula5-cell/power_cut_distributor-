# Smart Power Cut Management

## Description
Simulates real-world power distribution under limited supply using priority-based allocation.

## Tasks
- Easy: Simple zones
- Medium: Limited power
- Hard: Random demand

## Action Space
Select zone index

## Observation Space
{
  "supply": int,
  "zones": list
}

## Reward
0.0 to 1.0 based on priority and allocation

## Run
python inference.py