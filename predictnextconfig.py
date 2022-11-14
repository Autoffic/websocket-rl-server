import sys
from pathlib import Path
import os

from stable_baselines3 import PPO

import numpy

import time

# whether or not to enable debugging
debug = True

# to change to project relative paths and properly resolve paths in different platforms
FILE = Path(__file__).resolve()
# traffic-intersection-rl-environment-sumo root directory
ROOT = FILE.parents[0]
if str(ROOT) not in sys.path:
    sys.path.append(str(ROOT))  # add ROOT to PATH
ROOT = Path(os.path.relpath(ROOT, Path.cwd()))  # relative


# model information
'''
    For model.predict() the argument is an array of number of vehicles in lanes
    The order is west, north, east and south
    The lanes order is from outermost(0) to innermost(2)

    Example: [" E0_0", " E0_1", " E0_2",
              "-E1_0", "-E1_1", "-E1_2",
              "-E2_0", "-E2_1", "-E2_2",
              "-E3_0", "-E3_1", "-E3_2"]


    Various traffic light configuration corresponding to numbers.
    The model will only output number corresponding to green,
    it's up to the enviroment to set the yellow light

    <tlLogic id="J1" type="static" programID="0" offset="0">
0       <phase duration="40" state="GrrGGrGrrGGr"/>        # horizontal green
        <phase duration="10"  state="GrrGyrGrrGyr"/>       # horizontal yellow
1       <phase duration="40" state="GGrGrrGGrGrr"/>        # vertical green
        <phase duration="10"  state="GyrGrrGyrGrr"/>       # vertical yellow
2       <phase duration="40" state="GrrGrGGrrGrG"/>        # west to south green, east to north green
        <phase duration="10"  state="GrrGryGrrGry"/>       # west to south yellow, east to north yellow
3       <phase duration="40" state="GrGGrrGrGGrr"/>        # north to west green, south to east green
        <phase duration="10"  state="GryGrrGryGrr"/>       # north to west yellow, south to east yellow
    </tlLogic>


'''

models_path = Path(str(ROOT) + "/models").resolve()
model_path = Path(str(models_path) +
                  "/2022_08_26_20_31_22_136701_TrafficIntersection_TripleLaneGUI_ppo").resolve()

# the model for prediction
model = PPO.load(str(model_path))

'''
Takes in array of vehicles count in each lanes and
returns the next predicted configuration
'''


def predictNextConfiguration(lanes_observation):
    next_configuration, _state = model.predict(
        lanes_observation, deterministic=True)

    return next_configuration


# random test code
if __name__ == "__main__":
    number_of_lanes_to_observe = 12

    lanes_observation = numpy.zeros(number_of_lanes_to_observe, numpy.int32)

    for i, _ in enumerate(lanes_observation):
        lanes_observation[i] = numpy.random.randint(low=10, high=200)

    time_before_prediction = time.time()
    next_config = predictNextConfiguration(lanes_observation=lanes_observation)
    time_after_prediction = time.time()

    time_taken_for_prediction = time_after_prediction - time_before_prediction

    if debug:
        print(f"\n The observation was: \
            {lanes_observation} \
                \n predicted configuration: \
            {next_config} \
                \n Time taken: {time_taken_for_prediction}")
