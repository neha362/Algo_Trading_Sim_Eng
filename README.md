# Algo_Trading_Sim_Eng

TODOs:

- Order Book class
  - Keeps track of list of Bids and Asks
  - Implements price-time priority
    - higher bids and lower asks first
    - secondary time sorting
- Order class
  - id, price, quantity, side, timestamp
  - store linked list position
- Price Level class
  - order objects at the same price
- matching algorithm
  - price >= lowest ask
    - execute from front
  - else add to end
- use Yahoo Finance for real-time data
- low-latency efficiency
  - implement O(1) or O(log n) adding, matching, cancelling operations
- map of orders
  - O(1) lookup
- doubly linked order list
  - O(1) modification to head or tail
- price tree BST
  - keeps prices organized
