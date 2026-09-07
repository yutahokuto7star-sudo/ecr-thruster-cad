import cadquery as cq
import os

# --- 1. 設計パラメータの定義（ここで一括調整可能） ---
BUS_SIZE = (500, 500, 600)
TANK_RADIUS = 150
SOLAR_SIZE = (800, 200, 10)
CHAMBER_SPEC = (60, 35) # (高さ, 半径)
RCS_ANGLE = 35 # 姿勢制御スラスタの傾き角（度）

# 出力用ディレクトリの確保
os.makedirs("output", exist_ok=True)

# --- 2. ジオメトリの構築 ---
bus = cq.Workplane("XY").box(*BUS_SIZE)
tank = cq.Workplane("XY").sphere(TANK_RADIUS)
solar_panel = cq.Workplane("XY").box(*SOLAR_SIZE)

chamber = cq.Workplane("XY").cylinder(CHAMBER_SPEC[0], CHAMBER_SPEC[1])
nozzle = cq.Workplane("XY").workplane(offset=CHAMBER_SPEC[0]).circle(20).workplane(offset=50).circle(35).loft()
thruster = chamber.union(nozzle)

# --- 3. アセンブリの組み立て ---
satellite = cq.Assembly(name="satellite_system")
satellite.add(bus, name="bus")
satellite.add(tank, name="fuel_tank", loc=cq.Location(cq.Vector(0, 0, 150)))
satellite.add(thruster, name="main_thruster", loc=cq.Location(cq.Vector(0, 0, -380)))
satellite.add(thruster, name="rcs_thruster_right", loc=cq.Location(cq.Vector(220, 0, -200), cq.Vector(0, 1, 0), RCS_ANGLE))
satellite.add(thruster, name="rcs_thruster_left", loc=cq.Location(cq.Vector(-220, 0, -200), cq.Vector(0, 1, 0), -RCS_ANGLE))
satellite.add(solar_panel, name="solar_panel_right", loc=cq.Location(cq.Vector(450, 0, 0)))
satellite.add(solar_panel, name="solar_panel_left", loc=cq.Location(cq.Vector(-450, 0, 0)))

# --- 4. 解析・製造用パイプライン出力 ---
satellite.save("output/satellite_assembly.step")
bus.val().exportStep("output/bus.step")
tank.val().exportStep("output/tank.step")
thruster.val().exportStep("output/thruster.step")

bus.val().exportStl("output/bus.stl")
tank.val().exportStl("output/tank.stl")
thruster.val().exportStl("output/thruster.stl")
solar_panel.val().exportStl("output/solar_panel.stl")

print("Parametric design update and analysis export completed!")
