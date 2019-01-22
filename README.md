# Mercurius

Mercurius aims to simulate the behavior of an IoT system taking into account the whole protocol stack, the traffic generated from the whole system and the energy
consumption of all devices, in such a way it can also approximate the lifetime of an IoT device. All stack layers are implemented as a Black-Box. Each layer can send data to lower levels without any particular knowledge about them. Mercurius lets the user define a task being ran in each device n times in a given period of time (e.g. hourly, daily). In this way it can simulate the periodical energy consumption or generated traffic of the whole system.

### Prerequisites

• python3
• python3-matplotlib

## Getting Started

1) Download the files.
2) Define the devices task function in configurations/task.py, returning an array of integers which represent the amount of bytes sent from the devices. It is an array because a task can require more than one communication.
3) Configure the environment through the configurations/config.yaml file.
4) Run 'python3 simulator.py' script.

## Output

Mercurius provides many outputs:
• A log file containing all the events occurred during the simulation.
• A visualization of the scenario letting users check the energy consumption and the generated traffic device by device.
• A json file containing all the simulation data, letting users compute further analysis on data.

## Available Protocols 

####Application Layer
• HTML
####Transport Layer
• TCP
####Network Layer
• IP
####Link Layer
• Narrow-Band IoT

## NB-IoT Simulation
The link layer was simulated taking many ideas provided by the following papers:

• Izhak Rubin, Stefania Colonnese, Francesca Cuomo, Federica Calanca, and Tommaso Melodia. Mobile http-based streaming using flexible lte base station control. 
In 2015 IEEE 16th International Symposium on, pages 1–9. IEEE, 2015.
• Serdar Vural, Ning Wang, Gerard Foster, and Rahim Tafazolli. Success probability of multiple-preamble based single-attempt random access to mobile networks.
IEEE Communications Letters, pages 1–5, 2017.
• Quang Hien Chu, Jean-Marc Conrat, and Jean-Christophe Cousin. Propagation path loss models for lte-advanced urban relaying systems. 
In Antennas and Propagation (APSURSI), 2011 IEEE International Symposium on, pages 2797–2800. IEEE, 2011.
• Haojun Teng, Xiao Liu, Anfeng Liu, Hailan Shen, Changqin Huang, and Tian Wang. Adaptive transmission power control for reliable data forwarding in sensor based networks. Wireless Communications and Mobile Computing, 2018.



