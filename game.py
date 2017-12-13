# jjh5bc, zb4fw
# The game we intend to make is a Galega styled space-shooter where a ship shoots up at
# enemies(who possibly shoot back) floating down in a fixed pattern. There would also be three
# boss fights with actual attacks and health bars. The optional requirements we plan to fulfill include animation for the
# ship and bullets, enemies, health meter for the player and boss, music/sound effects for the background
# and bullets, and possibly two player if everything else within the game works right in time.

import pygame
import gamebox
import math


camera = gamebox.Camera(600,600)

creators = gamebox.from_text(camera.x, 540, 'A Joey Henderson (jjh5bc) & Zane Belkhayat (zb4fw) Production', 'Arial', 20, 'white')
ship = gamebox.from_color(300,300,'white',25,25)
shot = gamebox.from_image(300, -300, 'http://i.imgur.com/u3Mh2UU.png')
loser = gamebox.from_text(camera.x, camera.y, 'YOU DIED', 'Arial', 100, 'red', bold=True)
winner = gamebox.from_text(camera.x, camera.y, 'HE DIED', 'Arial', 100, 'red', bold=True)
explosion = gamebox.from_image(30000, 3000000, 'http://asecrettoeverybody.com/.images/.fire.gif')
ship_explosion = gamebox.from_image(30000, 3000000, 'http://asecrettoeverybody.com/.images/.fire.gif')
explosion.scale_by(.1)
ship_explosion.scale_by(.1)
boss_explosion = gamebox.from_image(30000, 3000000, 'http://asecrettoeverybody.com/.images/.fire.gif')
boss_explosion.scale_by(.3)
shot.rotate(90)
shot.scale_by(.2)
shot_sound = gamebox.load_sound('http://www.eng.auburn.edu/~sealscd/COMP7970/project/3Dstudio/levels/MISSION2/radaran.WAV')
explosion_sound = gamebox.load_sound('http://codeskulptor-demos.commondatastorage.googleapis.com/GalaxyInvaders/explosion%2001.wav')
b1_life = 15
b2_life = 15
b3_life = 15
lives = 3
recharge = 0
invulnerability = 0
bounce = 0
shield = gamebox.from_image(30000,300000, "http://i.imgur.com/OcVyq.png")
shield.scale_by(.1)
music = gamebox.load_sound('http://commondatastorage.googleapis.com/codeskulptor-demos/pyman_assets/intromusic.ogg')
musicplayer = music.play(-1)
b1 = gamebox.from_image(camera.x, 100, 'https://i.pinimg.com/originals/d8/e9/33/d8e9338e3aeb757bcfdab76af944abb7.gif')
b1.scale_by(.2)
b2 = gamebox.from_image(camera.x, 60000000, 'http://1.bp.blogspot.com/-MQE-zK1mVSE/UdSVGV3GP3I/AAAAAAAAAu8/EOsv__HnS-M/s1600/spacestation.png')
b2.scale_by(.15)
b3 = gamebox.from_color(camera.x, 90000000, 'red', 100, 100)
b1.rotate(-135)
b3speed = 8
laser_recharge = 0
beam = gamebox.from_image(camera.x, 90000000, 'https://media.giphy.com/media/991ckTBaOYH2o/source.gif')
beam.scale_by(.8)
beam.rotate(-90)
beam_recharge = 0


walls = [
    gamebox.from_color(300, 0, "darkgreen", 800, 30),
    gamebox.from_color(300, 600, "darkgreen", 800, 30),
    gamebox.from_color(0, 300, "darkgreen", 30, 800),
    gamebox.from_color(600, 300, "darkgreen", 30, 800)
]

sheet = gamebox.load_sprite_sheet("pixeljoint.com/files/icons/full/spaceshipsprites.gif",8,3)
boss3_sheet = gamebox.load_sprite_sheet("http://i.imgur.com/8zY5sBR.png",4,3)
background = gamebox.from_image(camera.x,camera.y,"cdn.mysitemyway.com/etc-mysitemyway/webtreats/assets/posts/857/full/tileable-classic-nebula-space-patterns-1.jpg")
b1_xspeed = 12
b1_yspeed = 16
b2_xspeed = 0
b2_yspeed = 0

show_splash = True
show_instructions = True
show_story = True
show_b1_win = False
show_b2 = False
show_b2_win = False
show_b3 = False
show_b3_win = False

ticks = 0


def splash(keys):
    global show_splash
    camera.clear('black')
    camera.draw(background)
    title = gamebox.from_text(camera.x, camera.y, "Rage Against", "Arial", 50, 'white', bold=True)
    camera.draw(title)
    directions = gamebox.from_text(camera.x, camera.y, "Press space to continue", "Arial", 30, "white")
    directions.top = title.bottom
    camera.draw(creators)
    camera.draw(directions)
    if pygame.K_SPACE in keys:
        show_splash = False
    camera.display()


def story(keys):
    global show_story
    camera.clear('black')
    camera.draw(background)
    story1 = gamebox.from_text(camera.x, 270, "Just one mission ago you were the greatest mercenary duo the universe had ever seen.", 'Arial', 18, 'white')
    camera.draw(story1)
    story2 = gamebox.from_text(camera.x, camera.y, "That all changed when he shot you down and left you for dead.", 'Arial', 18, 'white')
    story2.top = story1.bottom
    camera.draw(story2)
    story3 = gamebox.from_text(camera.x, camera.y, "But you\'re not dead, and you managed to track your old partner down.", 'Arial', 18, 'white')
    story3.top = story2.bottom
    camera.draw(story3)
    directions = gamebox.from_text(camera.x, camera.y,"Press A to get your revenge", 'Arial', 18, 'white')
    directions.top = story3.bottom
    camera.draw(directions)
    if pygame.K_a in keys:
        show_story = False
    camera.display()



def instructions(keys):
    global show_instructions
    camera.clear('black')
    camera.draw(background)
    instructions1 = gamebox.from_text(camera.x, 290, "Press the arrow keys to move, space bar to shoot", "Arial", 20, 'white')
    camera.draw(instructions1)
    instructions2 = gamebox.from_text(camera.x, camera.y, "You're the small ship, shoot the big ship", "Arial", 20, 'white')
    instructions2.top = instructions1.bottom
    camera.draw(instructions2)
    directions = gamebox.from_text(camera.x, camera.y, "Press S to start", "Arial", 20, "white")
    directions.top = instructions2.bottom
    camera.draw(directions)
    if pygame.K_s in keys:
        show_instructions = False
    camera.display()


def you_got_lucky(keys):
    global show_b1_win
    camera.clear('black')
    camera.draw(background)
    b1_win1 = gamebox.from_text(camera.x, 270,
                                'In his dying breaths, Rampage revealed how he was forced to shoot you down', 'Arial',
                                18, 'white')
    camera.draw(b1_win1)
    b1_win2 = gamebox.from_text(camera.x, camera.y,
                                'by a hitman named Rolling Thunder after he kidnapped his daughter.', 'Arial',
                                18, 'white')
    b1_win2.top = b1_win1.bottom
    camera.draw(b1_win2)
    b1_win3 = gamebox.from_text(camera.x, camera.y, 'He tells you he\'s sorry and gives you Rolling Thunder\'s location.',
                                'Arial', 18, 'white')
    b1_win3.top = b1_win2.bottom
    camera.draw(b1_win3)
    b1_win4 = gamebox.from_text(camera.x, camera.y, 'You know what you must do next.', 'Arial', 18, 'white')
    b1_win4.top = b1_win3.bottom
    camera.draw(b1_win4)
    directions = gamebox.from_text(camera.x, camera.y, 'Press A to continue your journey of revenge', 'Arial', 18,
                                   'white')
    directions.top = b1_win4.bottom
    camera.draw(directions)
    if pygame.K_a in keys:
        show_b1_win = False
    camera.display()


def another_twist(keys):
    global show_b2_win
    camera.clear('black')
    camera.draw(background)
    b2_win1 = gamebox.from_text(camera.x, 270,
                                'Before dying, Rolling Thunder revealed that the man who hired him to blackmail Rampage', 'Arial',
                                18, 'white')
    camera.draw(b2_win1)
    b2_win2 = gamebox.from_text(camera.x, camera.y,
                                'was none other than the Commander-in-Chief himself, who found the duo\'s mercenary',
                                'Arial', 18,'white')
    b2_win2.top = b2_win1.bottom
    camera.draw(b2_win2)
    b2_win3 = gamebox.from_text(camera.x, camera.y,
                                'success to be a threat to his own for-profit militia. He then tells you his top secret location.',
                                'Arial', 18, 'white')
    b2_win3.top = b2_win2.bottom
    camera.draw(b2_win3)
    b2_win4 = gamebox.from_text(camera.x, camera.y, 'You know what you must do next.', 'Arial', 18, 'white')
    b2_win4.top = b2_win3.bottom
    camera.draw(b2_win4)
    directions = gamebox.from_text(camera.x, camera.y, 'Press A to finish your journey of revenge', 'Arial', 18,
                                   'white')
    directions.top = b2_win4.bottom
    camera.draw(directions)
    if pygame.K_a in keys:
        show_b2_win = False
    camera.display()


def the_end(keys):
    global show_b3_win
    camera.clear('black')
    camera.draw(background)
    b3_win1 = gamebox.from_text(camera.x, 270,
                                'The Commander-in-Chief has been defeated,', 'Arial',
                                18, 'white')
    camera.draw(b3_win1)
    b3_win2 = gamebox.from_text(camera.x, camera.y,
                                'and any future hope for the state of America has been destroyed for generations to come.',
                                'Arial', 18,'white')
    b3_win2.top = b3_win1.bottom
    camera.draw(b3_win2)
    b3_win3 = gamebox.from_text(camera.x, camera.y,
                                'But your personal tale of vengeance has been completed.',
                                'Arial', 18, 'white')
    b3_win3.top = b3_win2.bottom
    camera.draw(b3_win3)
    b3_win4 = gamebox.from_text(camera.x, camera.y, 'Thank you for playing!', 'Arial', 18, 'white')
    b3_win4.top = b3_win3.bottom
    camera.draw(b3_win4)
    the_end = gamebox.from_text(camera.x, camera.y, 'The End', 'Arial', 18,
                                   'white')
    the_end.top = b3_win4.bottom
    camera.draw(the_end)
    camera.display()
    gamebox.pause()

def tick(keys):
    global recharge, b1_life, b1_xspeed, b1_yspeed, lives, invulnerability, show_b1_win, \
        show_b2, b2_life, b2_xspeed, b2_yspeed, bounce, show_b2_win, show_b3, ticks, b3_life, b3speed, beam_recharge, show_b3_win
    ticks += 1
    if show_splash:
        splash(keys)
        return
    if show_story:
        story(keys)
        return
    if show_instructions:
        instructions(keys)
        return
    invulnerability -= 1
    bounce -= 1
    ship.image = sheet[1]
    camera.clear('black')
    if pygame.K_UP in keys:
        ship.image = sheet[4]
        ship.y -= 10
    if pygame.K_DOWN in keys:
        ship.image = sheet[7]
        ship.y += 10
    if pygame.K_LEFT in keys:
        ship.image = sheet[0]
        ship.x -= 10
    if pygame.K_RIGHT in keys:
        ship.image = sheet[2]
        ship.x += 10
    if pygame.K_RIGHT in keys and pygame.K_UP in keys:
        ship.image = sheet[5]
    if pygame.K_LEFT in keys and pygame.K_UP in keys:
        ship.image = sheet[3]
    if pygame.K_RIGHT in keys and pygame.K_DOWN in keys:
        ship.image = sheet[8]
    if pygame.K_LEFT in keys and pygame.K_DOWN in keys:
        ship.image = sheet[6]
    if pygame.K_SPACE in keys and recharge > 27:
        shot.center = ship.x, (ship.y-10)
        shot.speedy = -20
        shot_sound.play()
        recharge = 0

    shot.move_speed()
    recharge += 1

    if b1.touches(walls[3], padding=10) and b1_yspeed > 0:
        b1.rotate(-90)
    if b1.touches(walls[3], padding=10) and b1_yspeed < 0:
        b1.rotate(90)
    if b1.touches(walls[1], padding=10) and b1_xspeed < 0:
        b1.rotate(-90)
    if b1.touches(walls[1], padding=10) and b1_xspeed > 0:
        b1.rotate(90)
    if b1.touches(walls[2], padding=10) and b1_yspeed < 0:
        b1.rotate(-90)
    if b1.touches(walls[2], padding=10) and b1_yspeed > 0:
        b1.rotate(90)
    if b1.touches(walls[0], padding=10) and b1_xspeed < 0:
        b1.rotate(90)
    if b1.touches(walls[0], padding=10) and b1_xspeed > 0:
        b1.rotate(-90)
    b1.move(b1_xspeed, b1_yspeed)
    camera.draw(background)
    camera.draw(ship)
    camera.draw(b1)

    if ship.touches(b1) and invulnerability < 0:
        lives -= 1
        invulnerability = 60
    lives_box = gamebox.from_text(camera.x, 20, 'Lives: ' + str(lives), 'Arial', 25, 'white')
    lives_box.top = walls[0].bottom
    lives_box.left = walls[2].right
    camera.draw(lives_box)

    for wall in walls:
        if ship.touches(wall):
            ship.move_to_stop_overlapping(wall)
        if b1.top_touches(wall, padding=10):
            b1.move_to_stop_overlapping(wall)
            b1_yspeed = -b1_yspeed
        if b1.bottom_touches(wall, padding=10):
            b1.move_to_stop_overlapping(wall)
            b1_yspeed = -b1_yspeed
        if b1.right_touches(wall, padding=10):
            b1.move_to_stop_overlapping(wall)
            b1_xspeed = -b1_xspeed
        if b1.left_touches(wall, padding=10):
            b1.move_to_stop_overlapping(wall)
            b1_xspeed = -b1_xspeed

    if invulnerability >= 0 and lives > 0:
        shield.center = ship.center
        camera.draw(shield)

    b1_lives = gamebox.from_text(500, 25, 'Rampage: ' + str(b1_life), 'Arial', 25, 'white')
    if b1_life > 0:
        camera.draw(b1_lives)
    if shot.touches(b1):
        b1_life -= 1
        explosion.center = shot.center
        camera.draw(explosion)
        shot.x = 3000000
        if b1_life <= 0:
            boss_explosion.center = b1.center
            camera.draw(boss_explosion)
            explosion_sound.play()
            b1.x = 3000000
            b2.x, b2.y = 0, 0
            show_b2 = True
            show_b1_win = True
            lives = 3
    if show_b1_win:
        you_got_lucky(keys)
        return

    if ship.x < b2.x:
        b2.speedx -= 1
    if ship.y < b2.y:
        b2.speedy -= 1
    if ship.x > b2.x:
        b2.speedx += 1
    if ship.y > b2.y:
        b2.speedy += 1
    b2.speedx *= .95
    b2.speedy *= .95
    b2.move_speed()
    b2.move(b2_xspeed, b2_yspeed)
    b2.rotate(math.degrees(math.atan2(ship.y - b2.y, ship.x - b2.x)))
    if ship.touches(b2) and invulnerability < 0:
        lives -= 1
        invulnerability = 60
        if bounce > 0:
            b2.speedx, b2.speedy = -b2.speedx, -b2.speedy
        bounce = 60

    if shot.touches(b2):
        b2_life -= 1
        explosion.center = shot.center
        camera.draw(explosion)
        shot.x = 3000000
        if b2_life == 0:
            boss_explosion.center = b2.center
            camera.draw(boss_explosion)
            explosion_sound.play()
            b2.x = 3000000
            b3.x, b3.y = camera.x, camera.y-200
            show_b3 = True
            show_b2_win = True
            lives = 3

    if ticks%3 == 1:
        b3.image = boss3_sheet[1]
    if ticks%3 == 2:
        b3.image = boss3_sheet[2]
    if ticks%3 == 0:
        b3.image = boss3_sheet[0]
    if shot.touches(b3):
        b3_life -= 1
        explosion.center = shot.center
        camera.draw(explosion)
        shot.x = 3000000
        if b3_life == 0:
            boss_explosion.center = b2.center
            camera.draw(boss_explosion)
            explosion_sound.play()
            b3.x = 3000000
            show_b3_win = True
    b3.move(b3speed,0)
    if b3.right_touches(walls[3]):
        b3speed = -b3speed
    if b3.left_touches(walls[2]):
        b3speed = -b3speed
    if show_b2:
        camera.draw(b2)
        b2_lives = gamebox.from_text(500, 25, 'Rolling Thunder: ' + str(b2_life), 'Arial', 25, 'white')
        if b2_life > 0:
            camera.draw(b2_lives)
    beam.x = b3.x
    beam.y = b3.y + 300
    if show_b2_win:
        another_twist(keys)
        return
    if show_b3:
        beam_recharge -=1
        if beam_recharge < -50:
            beam_recharge += 70
        if beam_recharge > 0:
            camera.draw(beam)
        camera.draw(b3)
        b3_lives = gamebox.from_text(480, 25, 'Comander-in-Chief: ' + str(b3_life), 'Arial', 25, 'white')
        if b3_life > 0:
            camera.draw(b3_lives)
    if beam_recharge > 0:
        if beam.touches(ship) and invulnerability < 0:
            lives -= 1
            invulnerability = 60
    if ship.touches(b3):
        lives -= 1
    if show_b3_win:
        the_end(keys)
        return

    if lives == 0:
        ship_explosion.center = ship.center
        camera.draw(ship_explosion)
        explosion_sound.play()
        camera.draw(loser)
        gamebox.pause()

    camera.draw(shot)

    camera.display()
    return

gamebox.timer_loop(60, tick)