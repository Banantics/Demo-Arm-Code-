
import time

import follower
from lerobot.robots.so_follower import SO101Follower, SO101FollowerConfig
from lerobot.teleoperators.so_leader import SO101Leader, SO101LeaderConfig

PORT = ["/dev/ttyACM0","/dev/ttyACM1"]
BOTS = ["T300", "SKYNET"]

# ARM SETTINGS
FOLLOWER_NAME = BOTS[0]
LEADER_NAME = BOTS[1]

FOLLOWER_PORT = PORT[0]

def reset_arm(follower):
    follower.send_action({"shoulder_lift.pos":-100.0})
    follower.send_action({"elbow_flex.pos":100.0})
    time.sleep(1)
    follower.send_action({"wrist_flex.pos":-100.0})
    time.sleep(1)
    follower.send_action({"wrist_roll.pos":0.0})
    follower.send_action({"gripper.pos":10.0})
    follower.send_action({"shoulder_pan.pos":-100.0})

def main():
    follower = Follower.Follower(port=FOLLOWER_PORT, id=FOLLOWER_NAME)  
    reset_arm(follower)

if __name__ == "__main__":
    main()