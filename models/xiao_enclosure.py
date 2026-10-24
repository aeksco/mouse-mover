"""Two-part enclosure for a Seeed Studio XIAO with a USB-C cable plugged in.

Single source of truth for the project: every dimension lives in the constants
below, and all the other `models/*.py` files import from here. Tune a test
print by editing one number and re-running `make MODEL=<name>`.

Models built from this file:
  xiao_enclosure      closed assembly (this file's build): bottom + top + board + plug
  enclosure_exploded  same assembly pulled apart so the board is visible inside
  enclosure_bottom    printable bottom half, floor on the bed
  enclosure_top       printable top half, flipped so the roof is on the bed
  xiao_board          the mocked-up XIAO on its own

Layout: the board drops into a pocket at the back and rests on a ledge. In
front of it a deliberately roomy rectangular bay swallows the whole plug
housing and strain relief, whatever cable is used, and the bare cable leaves
through a round hole in the end wall. The enclosure is modelled as one solid,
then sliced horizontally through the cable axis so the hole splits into two
half-rounds and the cable simply lays in. The bottom half gets a thin lip
around the inside of its wall and the top a matching groove; glue with CA.
Ribs hanging from the top hold the board down on its ledge. A small round
hole in the roof sits over the XIAO's status LEDs (power, user "L", RX, TX
cluster beside the receptacle) so they show through the closed case.

Coordinates: X runs along the board with the USB-C end at +X, Y across the
board (centred on 0), Z up with the outside of the floor at Z = 0.
"""

from build123d import (
    Align,
    Axis,
    Box,
    BuildPart,
    BuildSketch,
    Circle,
    Color,
    Compound,
    Cylinder,
    GridLocations,
    Keep,
    Location,
    Locations,
    Mode,
    Part,
    Plane,
    Rectangle,
    RectangleRounded,
    SlotOverall,
    add,
    extrude,
    fillet,
    loft,
    split,
)

# --- XIAO board (mm) ---------------------------------------------------------
# 21 x 17.8 is the shared XIAO footprint (SAMD21, RP2040, ESP32C3, nRF52840...).
# Component sizes are visual approximations for the mock; the enclosure only
# depends on the PCB outline, the receptacle height and the component envelopes.
PCB_L = 21.0
PCB_W = 17.8
PCB_T = 1.2
PCB_CORNER_R = 1.0
PAD_PITCH = 2.54  # castellated pads along each long edge
PADS_PER_SIDE = 7
PAD_NOTCH_R = 0.5

USB_W = 8.94  # receptacle outer width, sits on top of the PCB
USB_H = 3.26  # receptacle height; its centreline is the cable axis
USB_L = 7.35
USB_OVERHANG = 1.3  # receptacle sticks out past the PCB edge by this much
USB_EDGE_R = 1.2
USB_OPENING_W = 8.4
USB_OPENING_H = 2.5
USB_OPENING_DEPTH = 6.0

SHIELD_L = 10.0  # RF can / radio module on top of the board
SHIELD_W = 10.0
SHIELD_H = 2.2
SHIELD_X = -2.5  # offset from PCB centre; negative = away from the USB end
BUTTON_L = 2.0  # reset pads / button near the USB end, on the +Y side
BUTTON_W = 1.6
BUTTON_H = 1.0
BUTTON_X = 6.5
BUTTON_Y = 6.0

# Status LEDs: 2 x 2 cluster between the receptacle and the -Y pad row (SAMD21 XIAO).
# Row nearest the USB edge is user "L" (pin 13) + TX, the other row power + RX.
LED_L = 1.0  # each LED package, long axis along X
LED_W = 0.6
LED_H = 0.5
LED_PITCH_X = 1.8
LED_PITCH_Y = 0.85
LED_X = 7.45  # cluster centre from the PCB centre; positive = toward the USB end
LED_Y = -5.6

TOP_COMP_H = 4.0  # tallest thing above the PCB top face (receptacle + margin)
BOTTOM_COMP_H = 1.5  # tallest thing below the PCB bottom face

# --- USB-C cable (mm) --------------------------------------------------------
# CABLE_ASSY_L and CABLE_D are what the enclosure is sized from. Everything
# else here only shapes the mock of this particular cable; the bay around it
# is roomy on purpose so a different cable fits without a redesign.
CABLE_ASSY_L = 56.0  # plugged in: board far edge to the end of the strain relief
CABLE_D = 4.0  # bare (braided) cable
PLUG_SHELL_W = 8.25  # metal plug shell that goes into the receptacle
PLUG_SHELL_H = 2.4
PLUG_SHELL_L = 6.5
PLUG_GAP = 2.1  # shell left exposed between housing and receptacle when mated
PLUG_BODY_W = 10.5  # housing: stadium section, sides are full semicircles
PLUG_BODY_H = 6.1
PLUG_BODY_L = 15.0
RELIEF_END_W = 6.2  # strain relief width at the cable end (same thickness as the housing)
CABLE_STUB_L = 10.0  # bare cable drawn in the mock beyond the strain relief

# --- Enclosure (mm) ----------------------------------------------------------
WALL = 2.0
FLOOR = 1.6
ROOF = 1.6
CORNER_R = 3.0  # vertical outer corners
EDGE_R = 1.0  # top and bottom outer edges (must be < CORNER_R)
PCB_FIT_XY = 0.2  # pocket clearance per side around the PCB
PCB_FIT_Z = 0.2  # gap between PCB top and the hold-down ribs
LEDGE = 1.0  # shelf the PCB rests on, measured in from the pocket wall
TOP_CLEAR = 0.5  # headroom above TOP_COMP_H
CABLE_BAY_W = 14.0  # generic room for the plug housing + strain relief, centred on the cable axis
CABLE_BAY_H = 8.0
CABLE_END_GAP = 2.0  # strain relief end to the inside of the end wall
CABLE_HOLE_D = 4.5  # round exit for the bare cable, centred on the cable axis
LED_HOLE_D = 3.2  # light hole through the roof, centred over the LED cluster
LIP_H = 1.0  # alignment lip on the bottom half
LIP_CLEAR = 0.15  # lip-to-groove clearance per side
LIP_CLEAR_Z = 0.1  # extra groove depth so the halves close on the outer wall
RIB_W = 1.0  # hold-down ribs in the top half pressing on the PCB edges
RIB_L = 12.0  # ribs run this far from the back wall (stops short of the buttons)
RIB_CLEAR = 0.2  # rib to the bottom half's pocket wall
EXPLODE_GAP = 12.0  # vertical spacing in the exploded view
PLUG_PULL = 8.0  # how far the plug is drawn out in the exploded view

# --- Derived layout (do not edit; change the constants above) ----------------
X_POCKET0 = WALL
X_PCB0 = X_POCKET0 + PCB_FIT_XY
X_PCB1 = X_PCB0 + PCB_L
X_POCKET1 = X_PCB1 + PCB_FIT_XY
X_USB_FACE = X_PCB1 + USB_OVERHANG
X_PLUG0 = X_USB_FACE + PLUG_GAP  # housing front face (mock)
X_RELIEF_END = X_PCB0 + CABLE_ASSY_L
X_BAY1 = X_RELIEF_END + CABLE_END_GAP  # inside face of the end wall
OUTER_L = X_BAY1 + WALL
RELIEF_L = X_RELIEF_END - (X_PLUG0 + PLUG_BODY_L)  # mock only

POCKET_L = X_POCKET1 - X_POCKET0
POCKET_W = PCB_W + 2 * PCB_FIT_XY
OUTER_W = max(POCKET_W, CABLE_BAY_W) + 2 * WALL
INNER_R = CORNER_R - WALL  # plan-view corner radius of the pocket

# The board sits high enough that both the recess under it and the cable bay clear the floor
Z_PCB0 = FLOOR + max(BOTTOM_COMP_H, CABLE_BAY_H / 2 - PCB_T - USB_H / 2)
Z_PCB1 = Z_PCB0 + PCB_T
Z_AXIS = Z_PCB1 + USB_H / 2  # cable axis: receptacle centreline, bay centre, hole centre
Z_BAY0 = Z_AXIS - CABLE_BAY_H / 2
Z_BAY1 = Z_AXIS + CABLE_BAY_H / 2
Z_RIB0 = Z_PCB1 + PCB_FIT_Z
Z_SPLIT = Z_AXIS  # through the cable hole so the cable lays into the bottom half
Z_CEILING = max(Z_PCB1 + TOP_COMP_H + TOP_CLEAR, Z_BAY1)
OUTER_H = Z_CEILING + ROOF
Z_BRIDGE0 = Z_SPLIT + LIP_H + LIP_CLEAR_Z  # lowest Z at which the top may touch its own wall
X_LED = X_PCB0 + PCB_L / 2 + LED_X  # LED cluster / roof hole centre in enclosure coordinates
Y_LED = LED_Y

assert INNER_R > 0 and EDGE_R < CORNER_R, "CORNER_R must exceed WALL and EDGE_R"
assert INNER_R <= PCB_CORNER_R + PCB_FIT_XY, "pocket corners too round for the PCB"
assert Z_BRIDGE0 < Z_CEILING, "lip taller than the top cavity"
assert CABLE_HOLE_D < min(CABLE_BAY_W, CABLE_BAY_H), "cable hole must be smaller than the bay"
assert RELIEF_L > 0, "CABLE_ASSY_L is shorter than the board + housing"
assert RELIEF_END_W > PLUG_BODY_H, "relief keeps the housing thickness; set RELIEF_END_W just above PLUG_BODY_H"
assert X_POCKET0 < X_LED - LED_HOLE_D / 2 and X_LED + LED_HOLE_D / 2 < X_POCKET1, "LED hole must open over the PCB pocket"
assert abs(Y_LED) + LED_HOLE_D / 2 < POCKET_W / 2 - RIB_CLEAR - RIB_W, "LED hole runs into the hold-down ribs"

# --- Colours for the assembly views -----------------------------------------
COLOR_BOTTOM = Color(0.36, 0.58, 0.85)
COLOR_TOP = Color(0.55, 0.72, 0.92)
COLOR_PCB = Color(0.12, 0.45, 0.28)
COLOR_METAL = Color(0.78, 0.78, 0.80)
COLOR_PLASTIC = Color(0.25, 0.25, 0.27)
COLOR_CABLE = Color(0.15, 0.15, 0.15)
COLOR_LED = Color(0.95, 0.80, 0.20)


def _tag(part: Part, label: str, color: Color) -> Part:
    part.label = label
    part.color = color
    return part


def _outline(inset: float, mode: Mode = Mode.ADD) -> None:
    """Outer plan outline shrunk by `inset`, centred on the enclosure (sketch helper)."""
    with Locations((OUTER_L / 2, 0)):
        RectangleRounded(
            OUTER_L - 2 * inset,
            OUTER_W - 2 * inset,
            max(CORNER_R - inset, 0.05),
            mode=mode,
        )


def _plan_ring(outer_inset: float, inner_inset: float, z0: float, height: float) -> Part:
    """Prism between two insets of the outer outline, from z0 up by `height`."""
    with BuildPart() as ring:
        with BuildSketch(Plane.XY.offset(z0)):
            _outline(outer_inset)
            _outline(inner_inset, mode=Mode.SUBTRACT)
        extrude(amount=height)
    return ring.part


# --- Enclosure ---------------------------------------------------------------
def enclosure_solid() -> Part:
    """The whole enclosure as one closed solid, before it is split in two."""
    with BuildPart() as p:
        Box(OUTER_L, OUTER_W, OUTER_H, align=(Align.MIN, Align.CENTER, Align.MIN))
        fillet(p.edges().filter_by(Axis.Z), CORNER_R)
        by_z = p.edges().group_by(Axis.Z)
        fillet(by_z[0] + by_z[-1], EDGE_R)

        # PCB pocket, continuing up as the component cavity to the ceiling
        with BuildSketch(Plane.XY.offset(Z_PCB0)):
            with Locations(((X_POCKET0 + X_POCKET1) / 2, 0)):
                RectangleRounded(POCKET_L, POCKET_W, INNER_R)
        extrude(amount=Z_CEILING - Z_PCB0, mode=Mode.SUBTRACT)

        # Recess under the PCB for bottom-side parts; the PCB rests on the ledge around it
        with BuildSketch(Plane.XY.offset(FLOOR)):
            with Locations(((X_POCKET0 + X_POCKET1) / 2, 0)):
                Rectangle(POCKET_L - 2 * LEDGE, POCKET_W - 2 * LEDGE)
        extrude(amount=Z_PCB0 - FLOOR + 0.5, mode=Mode.SUBTRACT)

        # Cable bay: receptacle overhang, plug housing and strain relief all live here
        with Locations((X_POCKET1, 0, Z_BAY0)):
            Box(
                X_BAY1 - X_POCKET1,
                CABLE_BAY_W,
                CABLE_BAY_H,
                align=(Align.MIN, Align.CENTER, Align.MIN),
                mode=Mode.SUBTRACT,
            )

        # Round exit for the bare cable through the end wall
        with Locations((X_BAY1 + WALL / 2, 0, Z_AXIS)):
            Cylinder(CABLE_HOLE_D / 2, WALL + 2, rotation=(0, 90, 0), mode=Mode.SUBTRACT)

        # Light hole through the roof over the XIAO's status LEDs
        with Locations((X_LED, Y_LED, Z_CEILING - 1)):
            Cylinder(
                LED_HOLE_D / 2,
                ROOF + 2,
                align=(Align.CENTER, Align.CENTER, Align.MIN),
                mode=Mode.SUBTRACT,
            )
    return p.part


def _add_ribs() -> None:
    """Hold-down ribs for the top half (call inside its BuildPart, after the groove).

    Each rib is a fin that reaches down past the seam to just above the PCB edge,
    kept RIB_CLEAR away from the bottom half's walls, plus a bridge above the
    groove that ties the fin into the top half's own wall.
    """
    x0 = X_POCKET0 + INNER_R + RIB_CLEAR  # start past the pocket's rounded corner
    fin_h = Z_CEILING + 0.5 - Z_RIB0  # +0.5 so it fuses into the roof
    bridge_w = RIB_CLEAR + 0.5  # spans the fin-to-wall gap and bites 0.5 into the wall
    bridge_h = Z_CEILING + 0.5 - Z_BRIDGE0
    for side in (-1, 1):
        fin_y = side * (POCKET_W / 2 - RIB_CLEAR - RIB_W / 2)
        with Locations((x0, fin_y, Z_RIB0)):
            Box(RIB_L, RIB_W, fin_h, align=(Align.MIN, Align.CENTER, Align.MIN))
        bridge_y = side * (POCKET_W / 2 - RIB_CLEAR + bridge_w / 2)
        with Locations((x0, bridge_y, Z_BRIDGE0)):
            Box(RIB_L, bridge_w, bridge_h, align=(Align.MIN, Align.CENTER, Align.MIN))


def enclosure_halves() -> tuple[Part, Part]:
    """(bottom, top) in assembled position. Bottom carries the lip, top the groove and ribs."""
    full = enclosure_solid()
    cut = Plane.XY.offset(Z_SPLIT)

    with BuildPart() as lip:
        add(full)
        add(_plan_ring(WALL / 2 + LIP_CLEAR / 2, WALL, Z_SPLIT, LIP_H), mode=Mode.INTERSECT)

    with BuildPart() as bottom:
        add(full)
        split(bisect_by=cut, keep=Keep.BOTTOM)
        add(lip.part)

    with BuildPart() as top:
        add(full)
        split(bisect_by=cut, keep=Keep.TOP)
        add(
            _plan_ring(
                WALL / 2 - LIP_CLEAR / 2,
                WALL + LIP_CLEAR,
                Z_SPLIT - 0.01,
                LIP_H + LIP_CLEAR_Z + 0.01,
            ),
            mode=Mode.SUBTRACT,
        )
        _add_ribs()

    return (
        _tag(bottom.part, "enclosure_bottom", COLOR_BOTTOM),
        _tag(top.part, "enclosure_top", COLOR_TOP),
    )


def top_for_printing(top: Part) -> Part:
    """Flip the top half so its roof sits on the print bed at Z = 0."""
    return top.rotate(Axis.X, 180).move(Location((0, 0, OUTER_H)))


# --- Mock-ups ----------------------------------------------------------------
def xiao_board() -> list[Part]:
    """Approximate XIAO: PCB centred on the origin, bottom face at Z = 0, USB at +X."""
    with BuildPart() as pcb:
        with BuildSketch():
            RectangleRounded(PCB_L, PCB_W, PCB_CORNER_R)
        extrude(amount=PCB_T)
        with GridLocations(PAD_PITCH, PCB_W, PADS_PER_SIDE, 2):
            Cylinder(PAD_NOTCH_R, PCB_T * 3, mode=Mode.SUBTRACT)

    usb_front = PCB_L / 2 + USB_OVERHANG
    with BuildPart() as usb:
        with Locations((usb_front - USB_L / 2, 0, PCB_T)):
            Box(USB_L, USB_W, USB_H, align=(Align.CENTER, Align.CENTER, Align.MIN))
        fillet(usb.edges().filter_by(Axis.X), USB_EDGE_R)
        with BuildSketch(Plane.YZ.offset(usb_front - USB_OPENING_DEPTH)):
            with Locations((0, PCB_T + USB_H / 2)):
                RectangleRounded(USB_OPENING_W, USB_OPENING_H, USB_OPENING_H / 2 - 0.01)
        extrude(amount=USB_OPENING_DEPTH + 1, mode=Mode.SUBTRACT)

    with BuildPart() as shield:
        with Locations((SHIELD_X, 0, PCB_T)):
            Box(SHIELD_L, SHIELD_W, SHIELD_H, align=(Align.CENTER, Align.CENTER, Align.MIN))

    with BuildPart() as button:
        with Locations((BUTTON_X, BUTTON_Y, PCB_T)):
            Box(BUTTON_L, BUTTON_W, BUTTON_H, align=(Align.CENTER, Align.CENTER, Align.MIN))

    with BuildPart() as leds:
        with Locations((LED_X, LED_Y, PCB_T)):
            with GridLocations(LED_PITCH_X, LED_PITCH_Y, 2, 2):
                Box(LED_L, LED_W, LED_H, align=(Align.CENTER, Align.CENTER, Align.MIN))

    return [
        _tag(pcb.part, "pcb", COLOR_PCB),
        _tag(usb.part, "usb_c_receptacle", COLOR_METAL),
        _tag(shield.part, "shield", COLOR_METAL),
        _tag(button.part, "button", COLOR_PLASTIC),
        _tag(leds.part, "leds", COLOR_LED),
    ]


def usb_c_plug() -> list[Part]:
    """Mated USB-C plug: housing front face at X = 0, cable running toward +X."""
    with BuildPart() as shell:
        with BuildSketch(Plane.YZ.offset(-PLUG_SHELL_L)):
            SlotOverall(PLUG_SHELL_W, PLUG_SHELL_H)
        extrude(amount=PLUG_SHELL_L)
    with BuildPart() as body:
        with BuildSketch(Plane.YZ):
            SlotOverall(PLUG_BODY_W, PLUG_BODY_H)
        extrude(amount=PLUG_BODY_L)
    with BuildPart() as relief:
        # Continues the housing section with no step; only the sides taper
        with BuildSketch(Plane.YZ.offset(PLUG_BODY_L)):
            SlotOverall(PLUG_BODY_W, PLUG_BODY_H)
        with BuildSketch(Plane.YZ.offset(PLUG_BODY_L + RELIEF_L)):
            SlotOverall(RELIEF_END_W, PLUG_BODY_H)
        loft(ruled=True)
    with BuildPart() as cable:
        with BuildSketch(Plane.YZ.offset(PLUG_BODY_L + RELIEF_L)):
            Circle(CABLE_D / 2)
        extrude(amount=CABLE_STUB_L)
    return [
        _tag(shell.part, "plug_shell", COLOR_METAL),
        _tag(body.part, "plug_housing", COLOR_PLASTIC),
        _tag(relief.part, "strain_relief", COLOR_PLASTIC),
        _tag(cable.part, "cable", COLOR_CABLE),
    ]


# --- Assembly ----------------------------------------------------------------
def assembly(exploded: bool = False) -> Compound:
    """Bottom, top, board and plug in their assembled (or exploded) positions."""
    bottom, top = enclosure_halves()
    lift = EXPLODE_GAP if exploded else 0.0
    board_at = Location((X_PCB0 + PCB_L / 2, 0, Z_PCB0 + lift))
    plug_at = Location((X_PLUG0 + (PLUG_PULL if exploded else 0.0), 0, Z_AXIS + lift))
    top_at = Location((0, 0, 2 * lift))
    parts = [
        bottom,
        top.moved(top_at),
        *(part.moved(board_at) for part in xiao_board()),
        *(part.moved(plug_at) for part in usb_c_plug()),
    ]
    return Compound(children=parts, label="xiao_enclosure_exploded" if exploded else "xiao_enclosure")


def build() -> Compound:
    return assembly(exploded=False)
