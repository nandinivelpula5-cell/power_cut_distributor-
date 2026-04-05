# Smart Power Cut Management (OpenEnv)

## Description
This project simulates real-world power distribution under limited supply. 
An AI agent must allocate electricity efficiently to zones like hospitals, residential areas, and industries.

## Tasks
- Easy: Few zones, enough power
- Medium: Limited power, prioritization needed
- Hard: Random demand and supply

## Action Space
0 → Zone 1  
1 → Zone 2  
2 → Zone 3  

## Observation Space
{
  "supply": int,
  "zones": list
}

## Reward Logic
- High reward for powering critical zones
- Partial rewards for partial allocation
- Penalty for invalid actions

## Run
python inference.py
