import rclpy
from rclpy.action import ActionServer
from rclpy.node import Node
from turtlesim.action import RotateAbsolute
import time
import math


class RotateServer(Node):
    def __init__(self):
        super().__init__('rotate_server')
        self._action_server = ActionServer(
            self,
            RotateAbsolute,
            'my_rotate',
            self.execute_callback
        )
        self.get_logger().info('Rotate Server ready on /my_rotate')

    def execute_callback(self, goal_handle):
        self.get_logger().info(
            f'Goal received: {math.degrees(goal_handle.request.theta):.1f} deg'
        )

        feedback_msg = RotateAbsolute.Feedback()
        target = goal_handle.request.theta
        current = 0.0
        step = target / 10.0  # 10단계로 나눠서 실행

        for i in range(10):
            current += step
            feedback_msg.remaining = target - current
            goal_handle.publish_feedback(feedback_msg)
            self.get_logger().info(
                f'Feedback: {math.degrees(feedback_msg.remaining):.1f} deg remaining'
            )
            time.sleep(0.5)

        goal_handle.succeed()

        result = RotateAbsolute.Result()
        result.delta = target
        return result


def main(args=None):
    rclpy.init(args=args)
    node = RotateServer()
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()


if __name__ == '__main__':
    main()