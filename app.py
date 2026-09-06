import cadquery as cq

bus = cq.Workplane("XY").box(500, 500, 600)
tank = cq.Workplane("XY").sphere(150)
thruster = cq.Workplane("XY").cylinder(100, 30)

satellite = cq.Assembly(name="satellite_system")
satellite.add(bus, name="bus")
satellite.add(tank, name="fuel_tank", loc=cq.Location(cq.Vector(0, 0, 150)))
satellite.add(thruster, name="ecr_thruster", loc=cq.Location(cq.Vector(0, 0, -350)))

assembly_file = "satellite_assembly.step"
satellite.save(assembly_file)
print("Assembly saved successfully.")
