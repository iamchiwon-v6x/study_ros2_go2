import sys
import rclpy
from rclpy.node import Node
from example_interfaces.srv import AddTwoInts


class AddClient(Node):
    def __init__(self):
        super().__init__('add_client')
        self.client = self.create_client(AddTwoInts, 'add_two_ints')
        # 서버가 준비될 때까지 대기
        while not self.client.wait_for_service(timeout_sec=1.0):
            self.get_logger().info('Waiting for server...')

    def send_request(self, a, b):
        request = AddTwoInts.Request()
        request.a = a
        request.b = b
        future = self.client.call_async(request)
        return future


def main(args=None):
    rclpy.init(args=args)
    node = AddClient()

    a = int(sys.argv[1]) if len(sys.argv) > 1 else 3
    b = int(sys.argv[2]) if len(sys.argv) > 2 else 5

    future = node.send_request(a, b)
    rclpy.spin_until_future_complete(node, future)

    result = future.result()
    node.get_logger().info(f'Result: {a} + {b} = {result.sum}')

    node.destroy_node()
    rclpy.shutdown()


if __name__ == '__main__':
    main()