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
                self.player = Text(_("Bernie Sanders"), size=36)
                self.thedonald = Text(_("Theresa May"), size=36)
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
define p1 = Character("Bernie Sanders")
define p2 = Character("Theresa May")


# Define images
image bg oval = "OO.jpg"
image Bernie normal = "bs-normal.png"
image Bernie blush = "bs-blush.png"
image Theresa normal = "tm-normal.png"
image Theresa blush = "tm-blush.png"
image winner = "winner.png"



# The game starts here.
label start:
    scene bg oval

    menu:
        "Choose your character."
        "Bernie Sanders":
            jump Bernie
        "Theresa May":
            jump Theresa

label Theresa:
    show Theresa normal
    with fade
    "Unfortunately, you have chosen to play as Theresa May."
    "We honestly didn't expect anyone to choose this option, so there's nothing here."
    "Please feel free to go back and pick Bernie Sanders."
    return

label Bernie:
    show Bernie normal
    with fade
    p1 "Ah, what a lovely day in the White House as President of the United States of America."
    p1 "Nothing could possibly go wrong!"
    show Bernie normal at left
    with move
    show Theresa blush at right
    p2 "Ahaha! It is I, Theresa May."
    p2 "I will steal your nuclear launch codes and destroy your filthy liberal society!"
    hide Bernie normal
    hide Theresa blush
    window hide
    play music "us_anthem.mp3"
    python:
        ui.add(PongDisplayable())
        winner = ui.interact(suppress_overlay=True, suppress_underlay=True)
    play sound "game_over.mp3"
    show winner
    with fade
    p1 "Bernie wins!"
    show winner
    with fade
    p1 "Remember kids, Bernie Sanders always wins."
    return
