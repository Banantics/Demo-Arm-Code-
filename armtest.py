
import time

from lerobot.robots.so_follower import SO101Follower, SO101FollowerConfig
from lerobot.teleoperators.so_leader import SO101Leader, SO101LeaderConfig

# ARM SETTINGS
FOLLOWER_NAME = "T300"
LEADER_NAME = "SKYNET"

FOLLOWER_PORT = "/dev/ttyACM1"
LEADER_PORT = "/dev/ttyACM0"

# Configure the arms
follower = SO101Follower(
    SO101FollowerConfig(
        port=FOLLOWER_PORT,
        id=FOLLOWER_NAME,
    )
)

leader = SO101Leader(
    SO101LeaderConfig(
        port=LEADER_PORT,
        id=LEADER_NAME,
    )
)

try:
    print("Connecting T300...")
    follower.connect(calibrate=True)

    print("Connecting SKYNET...")
    leader.connect(calibrate=True)

    # Require valid calibration before allowing movement
    if not follower.calibration or not leader.calibration:
        raise RuntimeError(
            "Missing saved calibration for T300 or SKYNET. "
            "Calibrate each arm once before teleoperation."
        )

    if not follower.is_calibrated or not leader.is_calibrated:
        raise RuntimeError(
            "Motor calibration does not match saved calibration. "
            "Restore or verify calibration before moving."
        )

    print("\nT300 and SKYNET connected!")
    print("Move SKYNET to control T300.")
    print("Press Ctrl+C to stop.\n")

    while True:
        positions = leader.get_action()
        follower.send_action(positions)
        time.sleep(0.02)

except KeyboardInterrupt:
    print("\nStopping...")

finally:
    if follower.is_connected:
        follower.disconnect()

    if leader.is_connected:
        leader.disconnect()

    print("Both arms disconnected.")

