import sys
import openmc
def create_materials(operating_temp):

    safety_block = openmc.Material(name='safety_block')
    safety_block.add_element('Mo',1.1399e-3,'ao')
    safety_block.add_nuclide('U233',4.6384e-6,'ao')
    safety_block.add_nuclide('U234',4.7068e-4,'ao')
    safety_block.add_nuclide('U235',4.2848e-2,'ao')
    safety_block.add_nuclide('U236',3.1140e-4,'ao')
    safety_block.add_nuclide('U238',2.3253e-3,'ao')
    
    ISP = openmc.Material(name='ISP')
    ISP.add_element('Mo',1.7248e-3,'ao')
    ISP.add_nuclide('U233',4.6326e-6,'ao')
    ISP.add_nuclide('U234',4.7007e-4,'ao')
    ISP.add_nuclide('U235',4.2791e-2,'ao')
    ISP.add_nuclide('U236',3.1101e-4,'ao')
    ISP.add_nuclide('U238',2.3249e-3,'ao')
    
    fuel_ring = openmc.Material(name='fuel_ring')
    fuel_ring.add_element('Mo',1.7030e-3,'ao')
    fuel_ring.add_nuclide('U233',4.6343e-6,'ao')
    fuel_ring.add_nuclide('U234',4.7016e-4,'ao')
    fuel_ring.add_nuclide('U235',4.2801e-2,'ao')
    fuel_ring.add_nuclide('U236',3.1112e-4,'ao')
    fuel_ring.add_nuclide('U238',2.3328e-3,'ao')
    
    control_rod = openmc.Material(name='control_rod')
    control_rod.add_element('Mo',1.5550e-3,'ao')
    control_rod.add_nuclide('U233',4.7315e-6,'ao')
    control_rod.add_nuclide('U234',4.8008e-4,'ao')
    control_rod.add_nuclide('U235',4.3703e-2,'ao')
    control_rod.add_nuclide('U236',3.1765e-4,'ao')
    control_rod.add_nuclide('U238',2.3767e-3,'ao')

    burst_rod = openmc.Material(name='burst_rod')
    burst_rod.add_element('Mo',1.5909e-3,'ao')
    burst_rod.add_nuclide('U233',4.8405e-6,'ao')
    burst_rod.add_nuclide('U234',4.9114e-4,'ao')
    burst_rod.add_nuclide('U235',4.4710e-2,'ao')
    burst_rod.add_nuclide('U236',3.2497e-4,'ao')
    burst_rod.add_nuclide('U238',2.4314e-3,'ao')
    
    ss303 = openmc.Material(name='ss303')
    ss303.add_element('C',0.075,'wt')
    ss303.add_element('Si',1.00,'wt')
    ss303.add_element('P',0.1,'wt')
    ss303.add_element('S',0.3,'wt')
    ss303.add_element('Cr',18.00,'wt')
    ss303.add_element('Mn',1.00,'wt')
    ss303.add_element('Fe',70.225,'wt')
    ss303.add_element('Ni',9.0,'wt')
    ss303.add_element('Mo',0.30,'wt')


    vascomax300 = openmc.Material(name='vascomax300')
    vascomax300.add_element('C',0.02,'wt')
    vascomax300.add_element('Al',0.1,'wt')
    vascomax300.add_element('Si',0.05,'wt')
    vascomax300.add_element('P',0.005,'wt')
    vascomax300.add_element('S',0.005,'wt')
    vascomax300.add_element('Ti',0.730,'wt')
    vascomax300.add_element('Mn',0.05,'wt')
    vascomax300.add_element('Fe',66.94,'wt')
    vascomax300.add_element('Co',8.8,'wt')
    vascomax300.add_element('Ni',18.5,'wt')
    vascomax300.add_element('Mo',4.8,'wt')
    

    sae4340 = openmc.Material(name='sae4340')
    sae4340.add_element('C',0.405,'wt')
    sae4340.add_element('Si',0.225,'wt')
    sae4340.add_element('P',0.018,'wt')
    sae4340.add_element('S',0.02,'wt')
    sae4340.add_element('Cr',0.8,'wt')
    sae4340.add_element('Mn',0.725,'wt')
    sae4340.add_element('Fe',95.757,'wt')
    sae4340.add_element('Ni',1.8,'wt')
    sae4340.add_element('Mo',0.250,'wt')
    sae4340.set_density('g/cc',7.85)
 
    aluminium = openmc.Material(name='aluminium')
    aluminium.add_element('Mg',1.0,'wt')
    aluminium.add_element('Al',97.23,'wt')
    aluminium.add_element('Si',0.6,'wt')
    aluminium.add_element('Ti',0.075,'wt')
    aluminium.add_element('Cr',0.5*(0.04+0.35),'wt')
    aluminium.add_element('Mn',0.075,'wt')
    aluminium.add_element('Fe',0.35,'wt')
    aluminium.add_element('Cu',0.5*(0.15+0.4),'wt')
    aluminium.add_element('Zn',0.125,'wt')
    aluminium.set_density('g/cc',2.7)

    mats = [fuel_ring,safety_block,control_rod,burst_rod,ISP,ss303,vascomax300,sae4340,aluminium]
    return mats
Molybdenum 1.1399 x 10-3 1.7248 x 10-3 1.7030 x 10-3 1.5550 x 10-3 1.5909 x 10-3
233U 4.6384 x 10-6 4.6326 x 10-6 4.6343 x 10-6 4.7315 x 10-6 4.8405 x 10-6
234U 4.7068 x 10-4 4.7007 x 10-4 4.7016 x 10-4 4.8008 x 10-4 4.9114 x 10-4
235U 4.2848 x 10-2 4.2791 x 10-2 4.2801 x 10-2 4.3703 x 10-2 4.4710 x 10-2
236U 3.1140 x 10-4 3.1101 x 10-4 3.1112 x 10-4 3.1765 x 10-4 3.2497 x 10-4
238U 2.3253 x 10-3 2.3249 x 10-3 2.3328 x 10-3 2.3767 x 10-3 2.4314 x 10-3
