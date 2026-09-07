import cadquery as cq
import os

# 出力用ディレクトリの作成
os.makedirs("output", exist_ok=True)

# 1. 衛星バス (Main Bus)
bus = cq.Workplane("XY").box(500, 500, 600)

# 2. 燃料タンク (Fuel Tank)
tank = cq.Workplane("XY").sphere(150)

# 3. 展開型ソーラーパネル (Solar Panels)
solar_panel = cq.Workplane("XY").box(800, 200, 10)

# 4. ECRスラスタ詳細化: 燃焼室とノズル
chamber = cq.Workplane("XY").cylinder(60, 35)
nozzle = cq.Workplane("XY").workplane(offset=60).circle(20).workplane(offset=50).circle(35).loft()
thruster = chamber.union(nozzle)

# 5. アセンブリ構造の構築
satellite = cq.Assembly(name="satellite_system")
satellite.add(bus, name="bus")
satellite.add(tank, name="fuel_tank", loc=cq.Location(cq.Vector(0, 0, 150)))
satellite.add(thruster, name="main_thruster", loc=cq.Location(cq.Vector(0, 0, -380)))
satellite.add(thruster, name="rcs_thruster_right", loc=cq.Location(cq.Vector(220, 0, -200), cq.Vector(0, 1, 0), 30))
satellite.add(thruster, name="rcs_thruster_left", loc=cq.Location(cq.Vector(-220, 0, -200), cq.Vector(0, 1, 0), -30))
satellite.add(solar_panel, name="solar_panel_right", loc=cq.Location(cq.Vector(450, 0, 0)))
satellite.add(solar_panel, name="solar_panel_left", loc=cq.Location(cq.Vector(-450, 0, 0)))

# --- 製造・シミュレーション用パイプライン出力 ---
# ① アセンブリ全体のSTEP出力（CAD・受託受渡し用）
assembly_step = "output/satellite_assembly.step"
satellite.save(assembly_step)

# ② 各単体パーツのSTEP出力（個別加工用）
bus.val().exportStep("output/bus.step")
tank.val().exportStep("output/tank.step")
thruster.val().exportStep("output/thruster.step")

# ③ 3Dプリンタ・CFD解析用のSTL出力（ラピッドプロトタイピング・流体解析用）
bus.val().exportStl("output/bus.stl")
tank.val().exportStl("output/tank.stl")
thruster.val().exportStl("output/thruster.stl")
solar_panel.val().exportStl("output/solar_panel.stl")

print("Manufacturing & Simulation pipeline export completed successfully!")
