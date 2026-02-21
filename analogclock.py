
import pygame
import math 
import sys
from datetime import datetime


#  Bresenham Line Algorithm 
def bla(screen, x1, y1, x2, y2, color, t):
    dx = abs(x2 - x1)
    dy = abs(y2 - y1)
    x = x1
    y = y1

    lx = 1 if x2 > x1 else -1
    ly = 1 if y2 > y1 else -1

    if dx > dy:
        p = (2 * dy) - dx
        for _ in range(dx):
            if p < 0:
                x += lx
                p += 2 * dy
            else:
                x += lx
                y += ly
                p += 2 * dy - 2 * dx

            for i in range(t):
                screen.set_at((round(x + i), round(y)), color)
    else:
        p = 2 * dx - dy
        for _ in range(dy):
            if p < 0:
                y += ly
                p += 2 * dx
            else:
                x += lx
                y += ly
                p += 2 * dx - 2 * dy

            for i in range(t):
                screen.set_at((round(x + i), round(y)), color)


# Clock lines
def clock_ticks(screen, cx, cy, r):
    for i in range(60):
        angle = math.radians(i * 6)

        x1 = cx + (r - 10) * math.sin(angle) #outer tip of harek tick
        y1 = cy - (r - 10) * math.cos(angle)

        if i % 5 == 0:  # hour tick
            x2 = cx + (r - 25) * math.sin(angle)
            y2 = cy - (r - 25) * math.cos(angle)
            width = 4
        else:  # minute tick
            x2 = cx + (r - 18) * math.sin(angle)
            y2 = cy - (r - 18) * math.cos(angle)
            width = 2

        pygame.draw.line(screen, (255, 255, 255), (x1, y1), (x2, y2), width)


#  Numbers 
def clock_numbers(screen, cx, cy, r):
    font = pygame.font.SysFont('calibri', 36, True)

    for i in range(1, 13):
        angle = math.radians(i * 30)
        x = cx + (r - 45) * math.sin(angle)
        y = cy - (r - 45) * math.cos(angle)

        text = font.render(str(i), True, (255, 255, 255)) #number ko image banyo memory ma
        rect = text.get_rect(center=(x, y)) #creates rectangle in that image
        screen.blit(text, rect) #drawing step place the number image onto screen at given rec position


# Clock Hands 
def draw_hands(screen, cx, cy, r):
    now = datetime.now()

    h = now.hour % 12
    m = now.minute
    s = now.second

    sec_ang = math.radians(s / 60 * 360)
    min_ang = math.radians((m + s / 60) / 60 * 360) #minute hand moves slowly every sec
    hr_ang = math.radians((h + m / 60) / 12 * 360)

    # Second hand
    sec_x = int(cx + (r - 30) * math.sin(sec_ang))
    sec_y = int(cy - (r - 30) * math.cos(sec_ang))

    # Minute hand
    min_x = int(cx + (r - 60) * math.sin(min_ang))
    min_y = int(cy - (r - 60) * math.cos(min_ang))

    # Hour hand
    hr_x = int(cx + (r - 100) * math.sin(hr_ang))
    hr_y = int(cy - (r - 100) * math.cos(hr_ang))

    # Draw hands
    bla(screen, cx, cy, hr_x, hr_y, (255, 255, 255), 8)
    bla(screen, cx, cy, min_x, min_y, (255, 255, 255), 5)
    bla(screen, cx, cy, sec_x, sec_y, (255, 0, 0), 2)

    # Center ko dot
    pygame.draw.circle(screen, (255, 255, 255), (cx, cy), 6)


#  Date Box
def draw_date(screen, cx, cy):
    now = datetime.now()
    font = pygame.font.SysFont('calibri', 22, True)

    # Left box (Day bhako)
    day_text = now.strftime('%a')   # Only weekday
    left = font.render(day_text, True, (255, 255, 255))
    left_rect = left.get_rect(center=(cx - 90, cy))
    pygame.draw.rect(screen, (255, 255, 255), left_rect.inflate(20, 10), 1)
    screen.blit(left, left_rect)


    # Right box (Month)
    month_text = f"{now.strftime('%b').upper()} {now.day}"
    right = font.render(month_text, True, (255, 255, 255))
    right_rect = right.get_rect(center=(cx + 90, cy))
    pygame.draw.rect(screen, (255, 255, 255), right_rect.inflate(20, 10), 1)
    screen.blit(right, right_rect)

    # Year box
    year_text = str(now.year)
    year = font.render(year_text, True, (255, 255, 255))
    year_rect = year.get_rect(center=(cx, cy + 70))
    pygame.draw.rect(screen, (255, 255, 255), year_rect.inflate(20, 10), 1)
    screen.blit(year, year_rect)


# --------- Main ----------
def main():
    pygame.init()

    width, height = 600, 600
    screen = pygame.display.set_mode((width, height))
    pygame.display.set_caption("Analog Clock")

    cx, cy = width // 2, height // 2
    r = 230

    clock = pygame.time.Clock()
    running = True

    while running:
        clock.tick(60) #60 frames per second,smooth aauxa

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        screen.fill((0, 0, 0))

        # Outer white border
        pygame.draw.circle(screen, (255, 255, 255), (cx, cy), r + 10, 5)

        # Inner black face
        pygame.draw.circle(screen, (0, 0, 0), (cx, cy), r)

        clock_ticks(screen, cx, cy, r)
        clock_numbers(screen, cx, cy, r)
        draw_hands(screen, cx, cy, r)
        draw_date(screen, cx, cy)

        pygame.display.update()

    pygame.quit()
    sys.exit()


if __name__=="__main__":
    main()
    