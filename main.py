import math
import pygame
import pymunk

WIDTH, HEIGHT = 800, 400
FPS = 60
PHYSICS_SUBSTEPS = 25
PHYSICS_DT = 1 / FPS / PHYSICS_SUBSTEPS

pygame.init()

display = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Pendulum Simulation")

clock = pygame.time.Clock()

space = pymunk.Space()
space.gravity = 0, -981

def convert_coords(point):
    return int(point[0]), int(HEIGHT - point[1])

def calculate_distance(p1, p2):
    return math.sqrt((p2[1] - p1[1])**2 + (p2[0] - p1[0])**2)

def calculate_angle(p1, p2):
    return math.atan2(p2[1] - p1[1], p2[0] - p1[0])
    
def create_pendulum():
    x = WIDTH / 3
    pivot = (x, HEIGHT)
        
    mass = 10
    radius = 25
    moment = pymunk.moment_for_circle(mass, 0, radius)
        
    body = pymunk.Body(mass, moment)
    body.position = (x, HEIGHT / 3)
        
    ball = pymunk.Circle(body, radius)
    ball.elasticity = 0.9999999
        
    joint = pymunk.PinJoint(space.static_body, body, pivot, (0, 0))
        
    space.add(body, ball, joint)
    
    return body, ball, joint

def create_stack_scene():
    floor = pymunk.Segment(space.static_body, (20, 55), (780, 55), 1)
    wall = pymunk.Segment(space.static_body, (780, 55), (780, 350), 1)
    for line in (floor, wall):
        line.friction = 0.3
        line.elasticity = 0.4
    space.add(floor, wall)

    boxes = []
    size = 20
    mass = 10
    for column in range(5):
        for row in range(5):
            moment = pymunk.moment_for_box(mass, (size, size))
            body = pymunk.Body(mass, moment)
            body.position = (520 + column * 50, 66 + row * (size + 0.1))
            shape = pymunk.Poly.create_box(body, (size, size))
            shape.friction = 0.3
            space.add(body, shape)
            boxes.append(shape)
    
    return (floor, wall), boxes

def draw_stack_scene(lines, boxes):
    for line in lines:
        pygame.draw.line(display, "white", convert_coords(line.a),
                         convert_coords(line.b), 2)
    for box in boxes:
        vertices = [convert_coords(box.body.local_to_world(vertex))
                    for vertex in box.get_vertices()]
        pygame.draw.polygon(display, "skyblue", vertices)

def create_ball(pos):
    mass, radius = 100, 15
    moment = pymunk.moment_for_circle(mass, 0, radius)
    ball_body = pymunk.Body(body_type=pymunk.Body.STATIC)
    ball_body.position = convert_coords(pos)
    
    ball = pymunk.Circle(ball_body, radius)
    ball.friction = 0.3
    ball.elasticity = 0.9999999
    ball.mass = mass
    
    space.add(ball_body, ball)
    
    return ball, ball_body

def draw_projectile(projectile, projectile_body):
    pygame.draw.circle(display, (255, 150, 150), convert_coords(projectile_body.position), int(projectile.radius))

def main():
    p_body, p_ball, joint = create_pendulum()
    lines, boxes = create_stack_scene()
    pivot = convert_coords(joint.a.local_to_world(joint.anchor_a))
    ball, ball_body = None, None
    
    pos = None
    
    p_body.apply_impulse_at_local_point((-4000, 0))
    
    while True:
        line = None
        if ball and pos:
            line = [pos, pygame.mouse.get_pos()]
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                return
            
            if event.type == pygame.MOUSEBUTTONDOWN:
                if ball is None or ball_body is None:
                    pos = event.pos
                    ball, ball_body = create_ball(pos)
                elif pos is not None and line is not None:
                    ball_body.body_type = pymunk.Body.DYNAMIC
                    
                    angle = calculate_angle(*line)
                    force = calculate_distance(*line) * 500
                    fx = math.cos(angle) * force
                    fy = math.sin(angle) * force
                    
                    ball_body.apply_impulse_at_local_point((-fx, fy), (0, 0))
                    pos = None
                else:
                    space.remove(ball, ball_body)
                    ball, ball_body = None, None
                    pos = None
                
        display.fill((7, 12, 54))
        
        if line:
            pygame.draw.line(display, "green", line[0], line[1], 3)
        
        draw_stack_scene(lines, boxes)
        
        if ball is not None and ball_body is not None:
            draw_projectile(ball, ball_body)
        
        # display.blit(instructions, (10, 10))
        
        centre = convert_coords(p_body.position)
        pygame.draw.aaline(display, "white", pivot, centre)
        pygame.draw.circle(display, "red", centre, int(p_ball.radius))
        
        for i in range(PHYSICS_SUBSTEPS):
            space.step(PHYSICS_DT)
            
        pygame.display.update()
        clock.tick(FPS)
        
        
        
if __name__ == "__main__":
    main()
    pygame.quit()
