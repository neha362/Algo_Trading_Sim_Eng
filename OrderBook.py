'''
- Order Book class
    - Keeps track of list of Bids and Asks
    - Implements price-time priority
        - higher bids and lower asks first
        - secondary time sorting

- matching algorithm 
    - price >= lowest ask
        - execute from front
    - else add to end
'''