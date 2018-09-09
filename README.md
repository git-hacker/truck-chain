# Truck-Chain

## Introduction:-

Truck-Chain is a web application based on a blockchain model to solve many problems that Highway Logistics encounter. During the 48hrs at Unleash Highway Logistics Hackathon, our team created from scratch a multi-layered project from Blockchain Network to a Web Application. 
Our projects core foundation is based on a Blockchain Network. On top of the Blockchain Network, we coded a SMART Contract as well as a Deep Learning Algorithm. Above the projects core, is the Database which is serves as a local backup for a company. Truck-Chain’s business logic is based on three main pillars: Administrator, Driver and Insurance which will further be extended to other areas of industries such as: Finance, Health..etc. On top of our Core and Business Logic we built a web application which our focused users are Truck drivers. 

## Truck-Chain Application Implementation:-

**Main Features:**

- Map provides multiple routes to destination
- Allows user to enter multiple locations
- Users can enter in a via point location
- Awards drivers points dependening on mileage,speed and time of arrival at destination
- Call native map app

**Dependencies:**

- Works with most modern web browsers, Google Chrome is preferred for best outcome.
- If you want to run code, you will need Node.JS v8+

**How to run code:**
```Shell
git clone git@github.com:git-hacker/truck-map-web.git
npm install
npm start
```
## Truck-Chain Blockchain Python Implementation:-


**Main Features:**

- Possibility of adding multiple nodes to the blockchain
- Proof of Work (PoW)
- Conflict resolution between nodes
- Transactions with encryption and hashing


**Blockchain Client Features:**

- Wallets generation using Public/Private key encryption (based on RSA algorithm)
- Generation of transactions with RSA encryption 

This Github repository also contains 2 dashboards for each transacting participant(Admin, Insurance and Driver): 

- "Admin_Node" for Miners 
- "Admin_Client" for administrators to generate transactions on truck management.

- "Driver_Node" for Miners 
- "Driver_Client" for Drivers to generate transactions on truck deliveries. 

- "Insurance_Node" for Miners 
- "Insurance_Client" for administrators to generate transactions on truck insurance. 


**Dependencies:**

- Works with '''Python 3.6'''
- [Anaconda's Python distribution](https://www.continuum.io/downloads) contains all the dependencies for the code to run.


**How to run the code:**

1. To start a blockchain node, navigate to the ('filename'_Node) directory and execute the command below:
'''python (filename).py'''

2. You can add a new node to blockchain by executing the same command and specifying a port that is not already used. For example, '''python (filename).py -p (new_port_number)'''

3. To start the blockchain client, navigate to the ('filename'_Node) directory and execute the command below:
'''python (filename).py'''

4. You can access the blockchain node and blockchain client dashboards from your browser by going to -->localhost:"port_number"<--

**Ports:**

Participant dashboards are executed on localhost:"port_number". The different (port_numbers) can be referenced from below:
1. Admin_Node ---> localhost:5008.
2. Admin_Client ---> localhost:8088.
3. Driver_Node ---> localhost:5007.
4. Driver_Client ---> localhost: 8087.
5. Insurance_Node ---> localhost:5006".
6. Insurance_Client ---> localhost:8089.
