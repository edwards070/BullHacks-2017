# The script of the game goes in this file.



init:

    image bg pong field = "pong_field.png"

    python:

        class PongDisplayable(renpy.Displayable):

            def __init__(self):

                renpy.Displayable.__init__(self)

                # Some displayables we use.
                self.paddle = Image("pong.png")
                self.ball = Image("pong_ball.png")
                self.player = Text(_("Player 1"), size=36)
                self.thedonald = (_("Player 2"), size=36)
                self.ctb = Text(_("Click to Begin"), size=36)

                # The sizes of some of the images.
                self.PADDLE_WIDTH = 8
                self.PADDLE_HEIGHT = 79
                self.BALL_WIDTH = 15
                self.BALL_HEIGHT = 15
                self.COURT_TOP = 80
                self.COURT_BOTTOM = 1000

                # If the ball is stuck to the paddle.
                self.stuck = True

                # The positions of the two paddles.
                self.playery = (self.COURT_BOTTOM - self.COURT_TOP) / 2
                self.computery = self.playery

                # The speed of the computer.
                self.computerspeed = 500.0

                # The position, dental-position, and the speed of the
                # ball.
                self.bx = 150
                self.by = self.playery
                self.bdx = .5
                self.bdy = .5
                self.bspeed = 500.0

                # The time of the past render-frame.
                self.oldst = None

                # The winner.
                self.winner = None

            def visit(self):
                return [ self.paddle, self.ball, self.player, self.thedonald, self.ctb ]

            # Recomputes the position of the ball, handles bounces, and
            # draws the screen.
            def render(self, width, height, st, at):

                # The Render object we'll be drawing into.
                r = renpy.Render(width, height)

                # Figure out the time elapsed since the previous frame.
                if self.oldst is None:
                    self.oldst = st

                dtime = st - self.oldst
                self.oldst = st

                # Figure out where we want to move the ball to.
                speed = dtime * self.bspeed
                oldbx = self.bx

                if self.stuck:
                    self.by = self.playery
                else:
                    self.bx += self.bdx * speed
                    self.by += self.bdy * speed

                # Move the computer's paddle. It wants to go to self.by, but
                # may be limited by it's speed limit.
                cspeed = self.computerspeed * dtime
                if abs(self.by - self.computery) <= cspeed:
                    self.computery = self.by
                else:
                    self.computery += cspeed * (self.by - self.computery) / abs(self.by - self.computery)

                # Handle bounces.

                # Bounce off of top.
                ball_top = self.COURT_TOP + self.BALL_HEIGHT / 2
                if self.by < ball_top:
                    self.by = ball_top + (ball_top - self.by)
                    self.bdy = -self.bdy
                    renpy.sound.play("pong_beep.wav", channel=0)

                # Bounce off bottom.
                ball_bot = self.COURT_BOTTOM - self.BALL_HEIGHT / 2
                if self.by > ball_bot:
                    self.by = ball_bot - (self.by - ball_bot)
                    self.bdy = -self.bdy
                    renpy.sound.play("pong_beep.wav", channel=0)

                # This draws a paddle, and checks for bounces.
                def paddle(px, py, hotside):

                    # Render the paddle.
                    pi = renpy.render(self.paddle, 1920, 1080, st, at)

                    r.blit(pi, (int(px), int(py - self.PADDLE_HEIGHT / 2)))

                    if py - self.PADDLE_HEIGHT / 2 <= self.by <= py + self.PADDLE_HEIGHT / 2:

                        hit = False

                        if oldbx >= hotside >= self.bx:
                            self.bx = hotside + (hotside - self.bx)
                            self.bdx = -self.bdx
                            hit = True

                        elif oldbx <= hotside <= self.bx:
                            self.bx = hotside - (self.bx - hotside)
                            self.bdx = -self.bdx
                            hit = True

                        if hit:
                            renpy.sound.play("pong_boop.wav", channel=1)
                            self.bspeed *= 1.10

                # Render two paddles.
                paddle(120, self.playery, 120 + self.PADDLE_WIDTH)
                paddle(1800, self.computery, 1800)

                # Draw the ball.
                ball = renpy.render(self.ball, 1920, 1080, st, at)
                r.blit(ball, (int(self.bx - self.BALL_WIDTH / 2),
                              int(self.by - self.BALL_HEIGHT / 2)))

                # Show the player names.
                player = renpy.render(self.player, 1920, 1080, st, at)
                r.blit(player, (20, 25))

                # Show Donald's name.
                thedonald = renpy.render(self.thedonald, 1920, 1080, st, at)
                ew, eh = thedonald.get_size()
                r.blit(thedonald, (1900 - ew, 25))

                # Show the "Click to Begin" label.
                if self.stuck:
                    ctb = renpy.render(self.ctb, 1920, 1080, st, at)
                    cw, ch = ctb.get_size()
                    r.blit(ctb, (960 - cw / 2, 30))


                # Check for a winner.
                if self.bx < -200:
                    self.winner = "thedonald"

                    # Needed to ensure that event is called, annoucning the winner.
                    renpy.timeout(0)

                elif self.bx > 2100:
                    self.winner = "player"
                    renpy.timeout(0)

                # Ask that we be re-rendered ASAP, so we can show the next frame.
                renpy.redraw(self, 0)

                # Return the Render object.
                return r

            # Handles events.
            def event(self, ev, x, y, st):

                import pygame

                # Mousebutton down == start the game.
                if ev.type == pygame.MOUSEBUTTONDOWN and ev.button == 1:
                    self.stuck = False

                # Set the position of the human player's paddle.
                y = max(y, self.COURT_TOP)
                y = min(y, self.COURT_BOTTOM)
                self.playery = y

                # We have a winner.
                if self.winner:
                    return self.winner
                else:
                    raise renpy.IgnoreEvent()


# Declare characters used by this game. The color argument colorizes the
#name of the character.


# Define characters
define b = Character("Bernie Sanders")
define m = Character("Theresa May")
define t = Character("Donald Trump")
define k = Character("Kim Jong-Un")
define v = Character("Vladimir Putin")


# Define images
image bg oval = "OO.jpg"
image Sanders normal = "bs-normal.png"
image Sanders blush = "bs-blush.png"
image Trump normal = "dt-normal.png"
# image Trump blush = "dt-blush.png"
image May normal = "tm-normal.png"
# image May blush = "tm-blush.png"
# image Kim normal = "kju-normal.png"
# image Kim blush = "kju-blush.png"
# image Putin normal = "vp-normal.png"
# image Putin blush = "vp-blush.png"


# The game starts here.
label start:
    scene bg oval
    "Choose your character:"

    menu:
        "Bernie Sanders":
            self.player = Text(_("Bernie Sanders"), size=36)
            self.thedonald = Text(_("Donald Trump"), size=36)
            jump berniestart
        "Theresa May":
            self.player = Text(_("Theresa May"), size=36)
            self.thedonald = Text(_("Kim Jong-Un"), size=36)
            jump maystart
        "Donald Trump":
            self.player = Text(_("Donald Trump"), size=36)
            self.thedonald = Text(_("Vladimir Putin"), size=36)
            jump donaldstart
        "Kim Jong-Un":
            self.player = Text(_("Kim Jong-Un"), size=36)
            self.thedonald = Text(_("Vladimir Putin"), size=36)
            jump kimstart
        "Vladimir Putin":
            self.player = Text(_("Vladimir Putin"), size=36)
            self.thedonald = Text(_("Theresa May"), size=36)
            jump putinstart

label donaldstart:
    show Trump normal
    with fade
    t "Make America Great Again"
    show head normal at left
    with move
    show Sanders normal at right
    python:
        ui.add(PongDisplayable())
        winner = ui.interact(suppress_overlay=True, suppress_underlay=True)
        # if winner = donald, play us_anthem.mp3
        # if winner = random, play random_anthem.mp3
    return

label berniestart:
    show Sanders normal
    with fade
    b "Ah, what a lovely day in the White House as President of the United States of America."
    b "Nothing could possibly go wrong!"
    show Sanders normal at left
    with move
    show May normal at right
    m "Ahaha! It is I, Theresa May."
    m "Britain will take back control of the USA and I will rule over you with an iron fist!"
    python:
        ui.add(PongDisplayable())
        winner = ui.interact(suppress_overlay=True, suppress_underlay=True)
        # if winner = bernie, play us_anthem.mp3
        # if winner = random, play random_anthem.mp3
    return

label maystart:
    show May normal
    with fade
    python:
        ui.add(PongDisplayable())
        winner = ui.interact(suppress_overlay=True, suppress_underlay=True)
        # if winner = may, play uk_anthem.mp3
        # if winner = random, play random_anthem.mp3
    return

label kimstart:
    show May normal
    with fade
    python:
        ui.add(PongDisplayable())
        winner = ui.interact(suppress_overlay=True, suppress_underlay=True)
        # if winner = kim, play nk_anthem.mp3
        # if winner = random, play random_anthem.mp3
    return

label putinstart:
    show May normal
    with fade
    python:
        ui.add(PongDisplayable())
        winner = ui.interact(suppress_overlay=True, suppress_underlay=True)
        # if winner = putin, play ru_anthem.mp3
        # if winner = random, play random_anthem.mp3
    return
