# Online Multiplayer Reaction Game Using a Synchronization Protocol

## Introduction
This project, undertaken as part of the ELEN4017A: Network Fundamentals course at the University of the Witwatersrand, Johannesburg, illustrates the design and implementation of a synchronization protocol for an online multiplayer reaction game. The project achieved a distinction. 

## Project Description
The project aims to design a robust synchronization protocol using socket programming to enable synchronized gameplay for multiple users in a networked environment. A simple mathematics game was implemented to demonstrate the protocol’s functionality. The project focuses on latency checking, delay propagation, and response time capturing to ensure fair and synchronized gameplay.

## Key Features
- **Synchronization Protocol**: A custom synchronization protocol ensuring all users receive the game challenges simultaneously.
- **Multithreading**: Utilized to handle multiple client connections efficiently.
- **Latency Check and Delay Propagation**: Dynamically calculated and applied to ensure fair play.
- **Login System**: Secure username and password authentication, with passwords stored as hashes.
- **Error Handling**: Robust error checking and timeout functionalities on both server and client sides.
- **Score Calculation**: Dynamic calculation and update of players' scores based on response accuracy and speed.

## Methodology
1. **Data Collection**: Collected data on latency and delay for different network conditions.
2. **System Design**: Designed a multi-threaded server and client architecture with a focus on synchronization.
3. **Protocol Implementation**: Implemented a custom synchronization protocol using Python's socket library.
4. **Feature Development**: Developed features like login authentication, latency checks, delay propagation, and score calculation.
5. **Testing and Validation**: Conducted rigorous testing using Wireshark packet capturing and simulated different network speed conditions to validate synchronization.

## Technologies Used
- **Programming Language**: Python
- **Libraries**: Pandas, NumPy, Scikit-Learn, Matplotlib, Seaborn, Scipy, OS
- **Tools**: Wireshark for packet capturing

## Results
The synchronization protocol was successfully implemented and tested, ensuring fair and synchronized gameplay across different network conditions. The project achieved a distinction, demonstrating the effective application of network programming and synchronization techniques.


## Conclusion
This project successfully demonstrates the design and implementation of a robust synchronization protocol for online multiplayer games. The practical application of network programming, multithreading, and synchronization techniques provides a strong foundation for further research and development in distributed systems.


