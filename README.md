# #Universal_Robots_deserialize_primary.md

### Overview
- This document demonstrates the following:
  - Establishing a connection to a Universal Robots (UR) cobot using Python, via its primary interface over a network, by utilizing TCP/IP sockets.
  - Receiving a message from the cobot and processing the incoming data.
  - Decoding the received message into a human-readable format.
- This document also provides a technical explanation for the implementation. 
  
### Demo
- The demonstration initiates a Python client that establishes a connection with the UR simulator, receives messages, extracts the `isRobotPowerOn` value, and then displays it in the console.
    
  <kbd>![decode_demo](https://user-images.githubusercontent.com/80125540/227660650-c607e6e6-79ae-4c0d-805e-4c3dca30ba40.gif)</kbd>

### Requirements 
- Python 3
- Docker
- Google Chrome
- Git

## Setup

1. Create a UR simulator by opening a console and running the following command:
     
   ```Console
   docker run -it -e ROBOT_MODEL=UR3e --net ursim_net --ip 192.168.56.101 -p 30001:30001 -p 30002:30002 -p 30004:30004 -p 6080:6080 --name ur3e_container universalrobots/ursim_e-series
   ```
2. Interact with the simulator by opening Google Chrome and navigating to http://localhost:6080/vnc_auto.html.

3. Get the Python client by cloning the demo repository into a directory of your choice with the following command:
     
   ```Console
   git clone <URL>
   ```
   
4. Start the client by navigating inside the directory you cloned and running the following command:
     
   ```Console
   python3 ./decodeMessage.py
   ```
5. Observe the communication inside the console between the client and the UR simulator when toggling the simulator on / off.
     
   <kbd>![decode_demo](https://user-images.githubusercontent.com/80125540/227660650-c607e6e6-79ae-4c0d-805e-4c3dca30ba40.gif)</kbd>
   
## Technical Details

### Primary Client Interface
UR robots are capable of communicating with external devices through a variety of client interfaces. In the example, the primary client interface is utilized for communication. The robot's controller unit hosts an internal server that listens for incoming client request messages on port 30001, while also periodically transmitting messages containing robot data to these clients. This enables the robot to both receive commands from external devices and relay data back to them. 

Messages with robot data are sent as hexadecimal strings, which represent binary data and formatted as outlined in their primary interface specification. In short, the binary data is organized into sections. The first section serves as the package, while every subsequent section acts as a sub-package. A helpful analogy is to think of the package as the title of a book and the subpackages as its chapters. The subpackages are the areas within the string that you're likely interested in decoding. 

### How do I read the specification to decode messages / packages?

It's better to give an example. 
- The robot sends you a message. 
- The message has $x$ bytes.
- Your next step is to consult the specification to determine the message format for your PolyScope version. In this example, we will be using version 5.9.

<kbd>![image](https://user-images.githubusercontent.com/80125540/227675068-58fcf29f-00d9-436e-b287-129f21b1595f.png)</kbd>

- The diagram demonstrates that the first four bytes of the string must be interpreted as an integer, representing the length of the package. The fifth byte is an unsigned character that indicates the package type. This marks the end of the initial section, with every subsequent byte belonging to a sub-package.
- The following four bytes of the string represent the length of the first sub-package as an integer. The byte immediately after this will be an unsigned character that signifies the sub-package type.
- In this [example](https://onlinegdb.com/LYKpUJUTNb), I hard-coded a message for demonstration purposes, extracted the data using `struct` and displayed its values to the console. 
    
  ```Console
  Package Length: 1471,  Package Type: 16, Sub-package Length: 47, Sub-package Type: 0
  ```

- Using the technical specification, as seen directly below, we can see that our package type is a Robot State Message and the first subpackage is Robot Mode Data.
    
  <kbd>![image](https://user-images.githubusercontent.com/80125540/227684736-817e2eda-a94d-48dc-89b0-0d1b69fd5a4e.png)</kbd>

### What is this table trying to tell me?
- This table is telling us what comes next in the data string.
- The first item is `uint64_t timestamp`. This means the next 8 bytes represent an unsigned integer value for the timestamp of the robot. We can extract this data in a similar manner as demonstrated [here](https://onlinegdb.com/WTkt0g_8u).
- The next item in the data string is `isRealRobotConnected`, which is of type `bool`(1 byte). Therefore, the next byte represents its value. You can decode this variable, as well as the next 6 bools, using this [code](https://onlinegdb.com/H4iXgkbUL).
- If you sum the bytes of all the variables in the table, including variables length and type, it adds up to 47, which is the value we observed earlier.
- In principle, this approach can be applied to all sub-packages: read the bytes according to the types and order specified in the table, and then decode the values accordingly.

## Summary
- We created a client, connected it to a UR simulator, received messages, and decoded them into a human-readable format.
- The technical explanation and demonstration code provided should be adequate for adapting it to your specific needs.