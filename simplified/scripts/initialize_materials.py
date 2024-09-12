import sys
import openmc
def create_materials(operating_temp):
    #fuel-like materials
    safety_block = openmc.Material(name='safety_block', temperature=operating_temp)
    safety_block.add_element('Mo',1.1399e-3,'ao')
    safety_block.add_nuclide('U233',4.6384e-6,'ao')
    safety_block.add_nuclide('U234',4.7068e-4,'ao')
    safety_block.add_nuclide('U235',4.2848e-2,'ao')
    safety_block.add_nuclide('U236',3.1140e-4,'ao')
    safety_block.add_nuclide('U238',2.3253e-3,'ao')
    safety_block.set_density('g/cc',7288/401.298)
    safety_block.volume=401.298

    ISP = openmc.Material(name='ISP', temperature=operating_temp)
    ISP.add_element('Mo',1.7248e-3,'ao')
    ISP.add_nuclide('U233',4.6326e-6,'ao')
    ISP.add_nuclide('U234',4.7007e-4,'ao')
    ISP.add_nuclide('U235',4.2791e-2,'ao')
    ISP.add_nuclide('U236',3.1101e-4,'ao')
    ISP.add_nuclide('U238',2.3249e-3,'ao')
    ISP.set_density('g/cc',(3511.0+3312.0)/386.869)
    ISP.volume=386.869
    subassembly_plate_inner = ISP.clone()
    subassembly_plate_inner.name = 'subassembly_plate_inner'

    fuel_ring = openmc.Material(name='fuel_ring', temperature=operating_temp)
    fuel_ring.add_element('Mo',1.7030e-3,'ao')
    fuel_ring.add_nuclide('U233',4.6343e-6,'ao')
    fuel_ring.add_nuclide('U234',4.7016e-4,'ao')
    fuel_ring.add_nuclide('U235',4.2801e-2,'ao')
    fuel_ring.add_nuclide('U236',3.1112e-4,'ao')
    fuel_ring.add_nuclide('U238',2.3328e-3,'ao')
    fuel_ring_mass=8378.0+8134.0+8046.0+6909.0+8166.0+9283.0
    fuel_ring.set_density('g/cc',fuel_ring_mass/2782.931)
    fuel_ring.volume=2782.931

    control_rod = openmc.Material(name='control_rod', temperature=operating_temp)
    control_rod.add_element('Mo',1.5550e-3,'ao')
    control_rod.add_nuclide('U233',4.7315e-6,'ao')
    control_rod.add_nuclide('U234',4.8008e-4,'ao')
    control_rod.add_nuclide('U235',4.3703e-2,'ao')
    control_rod.add_nuclide('U236',3.1765e-4,'ao')
    control_rod.add_nuclide('U238',2.3767e-3,'ao')
    control_rod.set_density('g/cc',824.0/44.88)
    control_rod.volume=44.88

    burst_rod = openmc.Material(name='burst_rod', temperature=operating_temp)
    burst_rod.add_element('Mo',1.5909e-3,'ao')
    burst_rod.add_nuclide('U233',4.8405e-6,'ao')
    burst_rod.add_nuclide('U234',4.9114e-4,'ao')
    burst_rod.add_nuclide('U235',4.4710e-2,'ao')
    burst_rod.add_nuclide('U236',3.2497e-4,'ao')
    burst_rod.add_nuclide('U238',2.4314e-3,'ao')
    burst_rod.set_density('g/cc',826.0/43.975)
    burst_rod.volume=43.975

    #structure materials
    ss303 = openmc.Material(name='ss303', temperature=operating_temp)
    ss303.add_element('C',0.075,'wo')
    ss303.add_element('Si',1.00,'wo')
    ss303.add_element('P',0.1,'wo')
    ss303.add_element('S',0.3,'wo')
    ss303.add_element('Cr',18.00,'wo')
    ss303.add_element('Mn',1.00,'wo')
    ss303.add_element('Fe',70.225,'wo')
    ss303.add_element('Ni',9.0,'wo')
    ss303.add_element('Mo',0.30,'wo')
    ss303.set_density('g/cc',8.0)
    spindle = ss303.clone()
    spindle.name='spindle'
    safety_block_base = ss303.clone()
    safety_block_base.name='safety_block_base'
    clamp_support = ss303.clone()
    clamp_support.name='clamp_support'
    
    vascomax300 = openmc.Material(name='vascomax300', temperature=operating_temp)
    vascomax300.add_element('C',0.02,'wo')
    vascomax300.add_element('Al',0.1,'wo')
    vascomax300.add_element('Si',0.05,'wo')
    vascomax300.add_element('P',0.005,'wo')
    vascomax300.add_element('S',0.005,'wo')
    vascomax300.add_element('Ti',0.730,'wo')
    vascomax300.add_element('Mn',0.05,'wo')
    vascomax300.add_element('Fe',66.94,'wo')
    vascomax300.add_element('Co',8.8,'wo')
    vascomax300.add_element('Ni',18.5,'wo')
    vascomax300.add_element('Mo',4.8,'wo')
    vascomax300.set_density('g/cc',8.0)
    clamp = vascomax300.clone()
    clamp.name='clamp'

    sae4340 = openmc.Material(name='sae4340', temperature=operating_temp)
    sae4340.add_element('C',0.405,'wo')
    sae4340.add_element('Si',0.225,'wo')
    sae4340.add_element('P',0.018,'wo')
    sae4340.add_element('S',0.02,'wo')
    sae4340.add_element('Cr',0.8,'wo')
    sae4340.add_element('Mn',0.725,'wo')
    sae4340.add_element('Fe',95.757,'wo')
    sae4340.add_element('Ni',1.8,'wo')
    sae4340.add_element('Mo',0.250,'wo')
    sae4340.set_density('g/cc',7.85)
    subassembly_cover_plate = sae4340.clone()
    subassembly_cover_plate.name='subassembly_cover_plate'
    support_pad_ring = sae4340.clone()
    support_pad_ring.name='support_pad_ring'
    bearing_ring = sae4340.clone()
    bearing_ring.name='bearing_ring'

    aluminium = openmc.Material(name='aluminium', temperature=operating_temp)
    aluminium.add_element('Mg',1.0,'wo')
    aluminium.add_element('Al',97.23,'wo')
    aluminium.add_element('Si',0.6,'wo')
    aluminium.add_element('Ti',0.075,'wo')
    aluminium.add_element('Cr',0.5*(0.04+0.35),'wo')
    aluminium.add_element('Mn',0.075,'wo')
    aluminium.add_element('Fe',0.35,'wo')
    aluminium.add_element('Cu',0.5*(0.15+0.4),'wo')
    aluminium.add_element('Zn',0.125,'wo')
    aluminium.set_density('g/cc',2.7)
    mounting_plate = aluminium.clone()
    mounting_plate.name='mounting_plate'

    helium=openmc.Material(name='helium', temperature=operating_temp)
    helium.add_nuclide('He3',1.0,'ao')
    helium.set_density('g/cc',1.23456e-5)

    mats = [fuel_ring,safety_block,control_rod,burst_rod,ISP,subassembly_plate_inner,ss303,
        spindle, safety_block_base,clamp_support, clamp, vascomax300, subassembly_cover_plate,support_pad_ring, bearing_ring,sae4340,mounting_plate,aluminium, helium]
    return mats
