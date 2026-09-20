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

def main():
    body, ball, joint = create_pendulum()
    pivot = convert_coords(joint.a.local_to_world(joint.anchor_a))
    
    body.apply_impulse_at_local_point((-4000, 0))
    
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                return
                
        display.fill((7, 12, 54))
        
        centre = convert_coords(body.position)
        pygame.draw.aaline(display, "white", pivot, centre)
        pygame.draw.circle(display, "red", centre, int(ball.radius))
        
        for _ in range(PHYSICS_SUBSTEPS):
            space.step(PHYSICS_DT)
            
        pygame.display.update()
        clock.tick(FPS)
        
        
        
if __name__ == "__main__":
    main()
    pygame.quit()
