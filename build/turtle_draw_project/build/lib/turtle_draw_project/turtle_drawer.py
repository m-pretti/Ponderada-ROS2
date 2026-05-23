import rclpy
from rclpy.node import Node
from turtlesim.srv import TeleportAbsolute, SetPen
import time
import os

class TurtleDrawerNode(Node):
    def __init__(self):
        super().__init__('turtle_drawer')
        self.cli_teleport = self.create_client(TeleportAbsolute, '/turtle1/teleport_absolute')
        self.cli_pen = self.create_client(SetPen, '/turtle1/set_pen')

        while not self.cli_teleport.wait_for_service(timeout_sec=1.0):
            self.get_logger().info('Aguardando Turtlesim...')

        self.caminho_arquivo = '/home/inteli/pond-prog/caminho_turtlesim.txt'
        self.desenhar_silhueta()

    def set_pen(self, off):
        req = SetPen.Request()
        req.off = off
        req.r, req.g, req.b = 255, 255, 255
        req.width = 2
        self.cli_pen.call_async(req)

    def teleportar(self, x, y):
        req = TeleportAbsolute.Request()
        req.x, req.y = x, y
        future = self.cli_teleport.call_async(req)
        rclpy.spin_until_future_complete(self, future)

    def desenhar_silhueta(self):
        if not os.path.exists(self.caminho_arquivo): return

        pontos_brutos = []
        with open(self.caminho_arquivo, 'r') as f:
            for linha in f:
                pontos_brutos.append(linha.strip())

        if not pontos_brutos: return

        self.set_pen(1)
        primeiro_ponto = pontos_brutos[0].split(',')
        if primeiro_ponto[0] != 'None':
            self.teleportar(float(primeiro_ponto[0]), float(primeiro_ponto[1]))

        for linha in pontos_brutos:
            partes = linha.split(',')
            if partes[0] == 'None':
                self.set_pen(1)
                continue

            x, y = float(partes[0]), float(partes[1])
            self.teleportar(x, y)
            self.set_pen(0)
            time.sleep(0.02)

def main(args=None):
    rclpy.init(args=args)
    node = TurtleDrawerNode()
    rclpy.shutdown()
    
if __name__ == '__main__':
    main()