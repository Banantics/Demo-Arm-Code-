
import time

from lerobot.robots.so_follower import (
    SO101Follower,
    SO101FollowerConfig,
)


class Follower:

    # ===== FOLLOWER CLASS VARIABLES =====

    # self.port             - USB port connected to the robot
    # self.id               - Unique identifier/name of the robot
    # self.follower         - SO101Follower object used to control the robot

    # ===== PRIVATE JOINT POSITION VARIABLES =====

    # self.__shoulder_pan    - Current shoulder rotation position
    # self.__shoulder_lift   - Current shoulder lift position
    # self.__elbow_flex      - Current elbow joint position
    # self.__wrist_flex      - Current wrist bending position
    # self.__wrist_roll      - Current wrist rotation position
    # self.__gripper         - Current gripper position

    def __init__(self, port="/dev/ttyACM1", id="T300"):

        self.port = port
        self.id = id

        config = SO101FollowerConfig(
            port=self.port,
            id=self.id,
            cameras={}
        )

        self.follower = SO101Follower(config)

        self.follower.connect()

        if not self.follower.is_calibrated:
            raise RuntimeError(
                "Robot is not calibrated. "
                "Calibrate it before moving."
            )

        # Store the current joint positions
        observation = self.follower.get_observation()

        self.__shoulder_pan = observation["shoulder_pan.pos"]
        self.__shoulder_lift = observation["shoulder_lift.pos"]
        self.__elbow_flex = observation["elbow_flex.pos"]
        self.__wrist_flex = observation["wrist_flex.pos"]
        self.__wrist_roll = observation["wrist_roll.pos"]
        self.__gripper = observation["gripper.pos"]

    def slower_move(self, joint, pos) -> bool:

        match joint:
            case "shoulder_pan":
                prev_pos = self.__shoulder_pan
            case "shoulder_lift":
                prev_pos = self.__shoulder_lift
            case "elbow_flex":
                prev_pos = self.__elbow_flex
            case "wrist_flex":
                prev_pos = self.__wrist_flex
            case "wrist_roll":
                prev_pos = self.__wrist_roll
            case "gripper":
                prev_pos = self.__gripper
            case _:
                print("Invalid joint:", joint)
                return False

        # Gradually move toward target
        while  prev_pos != pos:

            if prev_pos < pos:
                prev_pos += 1
            else:
                prev_pos -= 1
    

        # Update stored position
        match joint:
            case "shoulder_pan":
                self.__shoulder_pan = pos
                
            case "shoulder_lift":
                self.__shoulder_lift = pos
            case "elbow_flex":
                self.__elbow_flex = pos
            case "wrist_flex":
                self.__wrist_flex = pos
            case "wrist_roll":
                self.__wrist_roll = pos
            case "gripper":
                self.__gripper = pos

        return True

    def reset_arm(self):
        # Example target positions only.
        # Verify safe limits before enabling motion.
        targets = {
            "shoulder_lift": -100.0,
            "elbow_flex": 100.0,
            "wrist_flex": -100.0,
            "wrist_roll": 0.0,
            "gripper": 10.0,
            "shoulder_pan": 0.0
        }

        for joint, position in targets.items():
            self.slower_move(joint, position)

    def disconnect(self):
        if self.follower.is_connected:
            self.follower.disconnect()
