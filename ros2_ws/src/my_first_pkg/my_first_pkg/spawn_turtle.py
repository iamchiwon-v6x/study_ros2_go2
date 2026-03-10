import rclpy
from rclpy.node import Node
from turtlesim.srv import Spawn


class SpawnTurtle(Node):
    def __init__(self):
        super().__init__('spawn_turtle')
        self.client = self.create_client(Spawn, '/spawn')
        while not self.client.wait_for_service(timeout_sec=1.0):
            self.get_logger().info('Waiting for /spawn service...')

    def spawn(self, x, y, theta, name):
        request = Spawn.Request()
        request.x = x
        request.y = y
        request.theta = theta
        request.name = name
        future = self.client.call_async(request)
        return future


def main(args=None):
    rclpy.init(args=args)
    node = SpawnTurtle()

    future = node.spawn(3.0, 3.0, 0.0, 'my_turtle')
    rclpy.spin_until_future_complete(node, future)

    result = future.result()
    node.get_logger().info(f'Spawned turtle: {result.name}')

    node.destroy_node()
    rclpy.shutdown()


if __name__ == '__main__':
    main()