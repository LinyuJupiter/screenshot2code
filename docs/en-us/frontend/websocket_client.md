# websocket_client

## Overview

websocket_client is a websocket-based client. In this frontend project, it is used to establish a websocket connection to the backend interface, thereby enabling real-time communication with the backend.

## Features

- Supports the websocket protocol
- Has two signals and slots: one for receiving messages and one for interrupting the connection
- The receive message slot can send received messages to the slot
- The interrupt connection slot sends a signal to the slot when disconnected from the server