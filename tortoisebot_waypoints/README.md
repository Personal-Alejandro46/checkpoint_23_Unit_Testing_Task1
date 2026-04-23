# tortoisebot_waypoints

## Como testar — Condição de PASSAR
No arquivo `test/waypoints_test.py`, defina:
TARGET_X = 0.5
TARGET_Y = 0.5
(Valores que o robô consegue alcançar)

## Como testar — Condição de FALHAR
Mude os valores para algo impossível:
TARGET_X = 99.0
TARGET_Y = 99.0

## Executar os testes
```bash
source /opt/ros/noetic/setup.bash
cd ~/simulation_ws && catkin_make && source devel/setup.bash
rostest tortoisebot_waypoints waypoints_test.test --reuse-master
```