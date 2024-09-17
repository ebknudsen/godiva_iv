import openmc

g=openmc.Geometry().from_xml('geometry.xml')
s=openmc.Settings().from_xml('settings.xml')
m=openmc.Materials().from_xml('materials.xml')
model=openmc.Model(geometry=g,settings=s,materials=m)
model.export_to_model_xml()
