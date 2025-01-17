import openmc


fuels={
"fuel_ring_101": ( ('U233',4.6624e-6),('U234',4.7311e-4),('U235',4.3069e-2),('U236', 3.1300e-4),('U238',2.3373e-3),('Mo',1.7013e-3) ),
"fuel_ring_102": ( ('U233',4.6953e-6),('U234',4.7635e-4),('U235',4.3364e-2),('U236', 3.1521e-4),('U238',2.3631e-3),('Mo',1.7366e-3) ),
"fuel_ring_103": ( ('U233',4.6795e-6),('U234',4.7439e-4),('U235',4.3186e-2),('U236', 3.1416e-4),('U238',2.3876e-3),('Mo',1.7209e-3) ),
"fuel_ring_104": ( ('U233',4.6634e-6),('U234',4.7327e-4),('U235',4.3083e-2),('U236', 3.1308e-4),('U238',2.3332e-3),('Mo',1.6974e-3) ),
"fuel_ring_105": ( ('U233',4.6427e-6),('U234',4.7116e-4),('U235',4.2892e-2),('U236', 3.1168e-4),('U238',2.3228e-3),('Mo',1.7104e-3) ),
"fuel_ring_106": ( ('U233',4.6903e-6),('U234',4.7581e-4),('U235',4.3313e-2),('U236', 3.1488e-4),('U238',2.3652e-3),('Mo',1.7319e-3) ),
"up_in_subassy_plate" : ( ('U233',4.7059e-6),('U234',4.7743e-4),('U235',4.3462e-2),('U236', 3.1593e-4),('U238',2.3684e-3),('Mo',1.7319e-3) ),
"int_in_subassy_plate" : ( ('U233',4.5562e-6),('U234',4.6239e-4),('U235',4.2092e-2),('U236', 3.0587e-4),('U238',2.2795e-3),('Mo',1.7319e-3) ),
"safety_block" : ( ('U233',4.6411e-6),('U234',4.7095e-4),('U235',4.2873e-2),('U236', 3.1158e-4),('U238',2.3266e-3),('Mo',1.7319e-3) ),
"cr" : ( ('U233',4.6944e-6),('U234',4.7632e-4),('U235',4.3360e-2),('U236', 3.1516e-4),('U238',2.3580e-3),('Mo',1.7319e-3) ),
"br" : ( ('U233',4.7807e-6),('U234',4.8507e-4),('U235',4.4157e-2),('U236', 3.2095e-4),('U238',2.4013e-3),('Mo',1.7319e-3) ),
}

steel303_composition=( ('C',3.0083e-4),('Si',1.7154e-3),('P',1.5554e-4,),('S',4.5067e-4),('Cr',1.6678e-2),('Mn',8.7693e-4),('Fe',6.0580e-2),('Ni',7.3878e-3),('Mo',1.5065e-4) )
s303_bits={ nm:steel303_composition for nm in ["spindle","spindle_nut","safety_block_base" ,"clamp_support","long_align_pin", "belly_band", "belly_band_bolt", "locking_bolt", "steel_screen", "steel_invertedt", "steel"]}

vascomax300_composition=(
('C',8.0221e-5),('Al',1.7855e-4),('Si',8.5768e-5),('P',7.7770e-6),('S',7.5112e-6),('Ti',7.3453e-4),('Mn',4.3847e-5),
('Fe',5.7746e-2),('Co',7.1938e-3),('Ni',1.5186e-2),('Mo',2.4103e-3) )

vmax_bits={ nm:vascomax300_composition for nm in ["clamp"]}

SAE_4340_composition=(
('C',1.5940e-3),
('Si',3.7872e-4),
('P',2.7472e-5),
('S',2.9481e-5),
('Cr',7.2734e-4),
('Mn',6.2385e-4),
('Fe',8.1057e-2),
('Ni',1.4499e-3),
('Mo',1.2319e-4),
)
sae_bits={nm:SAE_4340_composition for nm in ["bearing_ring", "sub_assy_cover_plate", "support_pad","br_pin"]}

AISI_1019_Carbon_Steel_composition=(
('C',6.7080e-4),
('P',3.0603e-5),
('S',3.6946e-5),
('Mn',7.3328e-4),
('Fe',8.3960e-2),
)

aisi_bits={nm:AISI_1019_Carbon_Steel_composition for nm in ["steel_bottom_cont_shield"]}

al_6061_t6_composition=(
('Mg',6.6898e-4),
('Al',5.8593e-2),
('Si',3.4736e-4),
('Ti',2.5469e-5),
('Cr',6.0978e-5),
('Mn',2.2197e-5),
('Fe',1.0190e-4),
('Cu',7.0365e-5),
('Zn',3.1082e-5),
)

al_6061_bits = {nm:al_6061_t6_composition for nm in ["mounting_plate", "core_cover" ]}

lexguard_plastic_composition=(
('C',75.48),
('H',5.55),
('O',18.87)
)
lexguard = {nm:lexguard_plastic_composition for nm in [ "plastic_cont_shield" ]}


def create_materials(temp):
    ms=openmc.Materials()
    for grp in [vmax_bits,aisi_bits,al_6061_bits,fuels,sae_bits,s303_bits,lexguard]:
        for k,v in grp.items():
            print(k)
            m=openmc.Material(name=k, temperature=temp)
            rho=0
            if "plastic" in k:
                for nuc in v:
                    m.add_element(nuc[0],nuc[1],'wo')
                m.set_density('g/cc',1.2)
                ms.append(m)
                continue
            for nuc in v:
                rho+=nuc[1]
                if nuc[0][-1] in set('0123456789'):
                    m.add_nuclide(nuc[0],nuc[1],'ao')
                else:
                    m.add_element(nuc[0],nuc[1],'ao')
            m.set_density('atom/b-cm',rho)
            ms.append(m)
    return ms

#materials = construct_materials()
#materials.export_to_xml()
