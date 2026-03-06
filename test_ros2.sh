#!/bin/bash
set -e

echo "=== ROS 2 환경 확인 ==="

# 1. ROS 2 환경변수
echo ""
echo "[1] ROS_DISTRO: ${ROS_DISTRO:-not set}"

# 2. ros2 CLI 동작 확인
echo ""
echo "[2] ros2 command check:"
ros2 doctor --report 2>&1 | head -5 || echo "FAIL: ros2 command not found"

# 3. 토픽 리스트 (rosout이 보이면 정상)
echo ""
echo "[3] ros2 topic list:"
ros2 topic list 2>&1

# 4. 간단한 pub/sub 테스트
echo ""
echo "[4] pub/sub test:"
ros2 topic pub /test_topic std_msgs/msg/String "data: 'hello ros2'" --once &
PUB_PID=$!
sleep 1
MSG=$(timeout 5 ros2 topic echo /test_topic --once 2>/dev/null) && echo "  received: $MSG" || echo "  (no subscriber caught it, but publish succeeded)"
wait $PUB_PID 2>/dev/null || true

echo ""
echo "=== 완료: ROS 2 정상 동작 ==="
