# Building Mapping Tool
## Overview
![HTML5](https://img.shields.io/badge/html5-%23E34F26.svg?style=for-the-badge&logo=html5&logoColor=white) ![Flask](https://img.shields.io/badge/flask-%23000.svg?style=for-the-badge&logo=flask&logoColor=white) ![JavaScript](https://img.shields.io/badge/javascript-%23323330.svg?style=for-the-badge&logo=javascript&logoColor=%23F7DF1E) ![Python](https://img.shields.io/badge/python-3670A0?style=for-the-badge&logo=python&logoColor=ffdd54) 

This project aims to create a tool that would assist a user to map a building and test if a route can be found between two points within the building. The system utilizes the concept of djisktra algorithm for finding the shortest route. The project utilizes HTML5 and JavaScript as the frontend and Python for backend with Flask as the framework. CSS was used for styling of the UI. 

## Tech Stack
|||
|--|--|
| Frontend | HTML5, JavaScript |
| Backend | Python 3.13 |
| Framework | Flask |

## What does it do?
### Project Creation
1. Create new projects saved in .json file format.
2. Open existing projects.

### Mapping a Building
1. Add floors and rearrange the order of the floors.
2. Add locations / rooms on each floor.
3. Add checkpoints on each floor connected to the locations / rooms.
4. Add connectors (stairs, escalators, elevators) that would provide connection across different level of floors. Connectors are considered a checkpoint.
5. Create path links between a room and a checkpoint.
6. Create path links between two checkpoint.
7. Create path links between two connectors on separate floors to mark the location that allows users to go up or down a floor.

### Testing Possible Routes
1. Allows user to test if there is a route from one point to another.
2. Allows user to perform a full test of all possible start and end location a user may choose. This helps to check if there is any location not mapped to any checkpoint.
