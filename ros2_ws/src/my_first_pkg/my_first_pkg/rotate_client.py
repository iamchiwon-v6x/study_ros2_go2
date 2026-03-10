import rclpy
from rclpy.action import ActionClient
from rclpy.node import Node
from turtlesim.action import RotateAbsolute
import math


class RotateClient(Node):
    def __init__(self):
        super().__init__('rotate_client')
        self._client = ActionClient(
            self, RotateAbsolute, '/turtle1/rotate_absolute'
        )

    def send_goal(self, angle_deg):
        goal_msg = RotateAbsolute.Goal()
        goal_msg.theta = math.radians(angle_deg)

        self.get_logger().info(f'Sending goal: {angle_deg} degrees')
        self._client.wait_for_server()

        self._send_goal_future = self._client.send_goal_async(
            goal_msg, feedback_callback=self.feedback_callback
        )
        self._send_goal_future.add_done_callback(self.goal_response_callback)

    def goal_response_callback(self, future):
        goal_handle = future.result()
        if not goal_handle.accepted:
            self.get_logger().info('Goal rejected')
            return
        self.get_logger().info('Goal accepted')
        self._get_result_future = goal_handle.get_result_async()
        self._get_result_future.add_done_callback(self.get_result_callback)

    def get_result_callback(self, future):
        result = future.result().result
        self.get_logger().info(
            f'Result: rotated {math.degrees(result.delta):.1f} degrees'
        )
        rclpy.shutdown()

    def feedback_callback(self, feedback_msg):
        remaining = feedback_msg.feedback.remaining
        self.get_logger().info(
            f'Feedback: {math.degrees(remaining):.1f} degrees remaining'
        )


def main(args=None):
    rclpy.init(args=args)
    node = RotateClient()
    node.send_goal(90.0)
    rclpy.spin(node)


if __name__ == '__main__':
    main()