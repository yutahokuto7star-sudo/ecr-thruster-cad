import cadquery as cq

# 衛星バス (Main Bus)
bus = cq.Workplane("XY").box(500, 500, 600)

# 燃料タンク (Fuel Tank)
tank = cq.Workplane("XY").sphere(150)

# ECRスラスタ詳細化: 燃焼室とノズルの安全な結合モデル
chamber = cq.Workplane("XY").cylinder(60, 35)
nozzle = cq.Workplane("XY").workplane(offset=60).circle(20).workplane(offset=50).circle(35).loft()
thruster = chamber.union(nozzle)

# アセンブリ構造の構築
satellite = cq.Assembly(name="satellite_system")
satellite.add(bus, name="bus")
satellite.add(tank, name="fuel_tank", loc=cq.Location(cq.Vector(0, 0, 150)))
satellite.add(thruster, name="ecr_thruster", loc=cq.Location(cq.Vector(0, 0, -380)))

assembly_file = "satellite_assembly.step"
satellite.save(assembly_file)
print("Detailed assembly saved successfully.")
