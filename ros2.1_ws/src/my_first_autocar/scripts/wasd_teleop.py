#!/usr/bin/env python3
import rclpy
from rclpy.node import Node
from geometry_msgs.msg import Twist
import sys, select, termios, tty

class AdvancedWASD(Node):
    def __init__(self):
        super().__init__('wasd_teleop')
        self.publisher_ = self.create_publisher(Twist, 'cmd_vel', 10)
        self.timer = self.create_timer(0.1, self.timer_callback)
        
        self.speed = 1.0
        self.turn = 1.5
        
        # Save terminal settings so we can restore them on exit
        self.settings = termios.tcgetattr(sys.stdin)
        
        # Lock terminal in raw mode ONCE at startup to stop the "wwwww" echo completely
        tty.setraw(sys.stdin.fileno())
        
        self.print_menu()

    def print_menu(self):
        # In raw mode, we must use \r\n to properly return the carriage to the left
        menu = (
            "\r\n"
            "🎮 Advanced WASD Controller\r\n"
            "---------------------------\r\n"
            "Moving around:\r\n"
            "        w\r\n"
            "   a    s    d\r\n"
            "\r\n"
            "Speed Controls:\r\n"
            "   q / z : increase/decrease ALL speeds by 10%\r\n"
            "   e / c : increase/decrease LINEAR speed by 10%\r\n"
            "   r / v : increase/decrease ANGULAR speed by 10%\r\n"
            "   space : force stop\r\n"
            "   CTRL-C to quit\r\n"
            f"\r\nCurrent speeds - Linear: {self.speed:.2f}, Angular: {self.turn:.2f}\r\n"
        )
        sys.stdout.write(menu)
        sys.stdout.flush()

    def get_key(self):
        # Non-blocking terminal read
        rlist, _, _ = select.select([sys.stdin], [], [], 0.1)
        if rlist:
            key = sys.stdin.read(1)
            return key
        return ''

    def timer_callback(self):
        key = self.get_key()
        msg = Twist()
        update_menu = False
        
        # --- Speed Control Logic ---
        if key == 'q':
            self.speed *= 1.1
            self.turn *= 1.1
            update_menu = True
        elif key == 'z':
            self.speed *= 0.9
            self.turn *= 0.9
            update_menu = True
        elif key == 'e':
            self.speed *= 1.1
            update_menu = True
        elif key == 'c':
            self.speed *= 0.9
            update_menu = True
        elif key == 'r':
            self.turn *= 1.1
            update_menu = True
        elif key == 'v':
            self.turn *= 0.9
            update_menu = True
        
        if update_menu:
            self.print_menu()
        
        # --- Movement Logic ---
        if key == 'w':
            msg.linear.x = self.speed
        elif key == 's':
            msg.linear.x = -self.speed
        elif key == 'a':
            msg.angular.z = self.turn
        elif key == 'd':
            msg.angular.z = -self.turn
        elif key == ' ': # Spacebar
            msg.linear.x = 0.0
            msg.angular.z = 0.0
        elif key == '\x03': # Catch CTRL-C
            self.restore_terminal()
            sys.exit()
        else:
            # Brake if no key is pressed
            msg.linear.x = 0.0
            msg.angular.z = 0.0

        self.publisher_.publish(msg)

    def restore_terminal(self):
        # Put the terminal back to normal before closing
        termios.tcsetattr(sys.stdin, termios.TCSADRAIN, self.settings)

def main(args=None):
    rclpy.init(args=args)
    node = AdvancedWASD()
    try:
        rclpy.spin(node)
    except SystemExit:
        pass
    finally:
        node.restore_terminal()
        node.destroy_node()
        rclpy.shutdown()

if __name__ == '__main__':
    main()
