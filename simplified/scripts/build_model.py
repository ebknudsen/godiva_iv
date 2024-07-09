from initialize_materials import create_materials
import openmc
import matplotlib.colors as mcolors
from matplotlib import colormaps as cm
import sys
import math
import pathlib as pl
import numpy as np
import itertools as it
in2cm = 2.54


class GIV_reactor:
    def __init__(self, core_h5m, CAD_rods=True, burst_rod_h5m,control_rod_h5m,
            fuel=None,operating_temp=977.59,batches=20,inactive=5,particles=1000,
            padding=0, shim_rod_z=[0,0,0], ctrl_rod_z=0, output_dir='.'):

        for ff in [core_h5m, shim_rod_h5m,control_rod_h5m]:
            if (not pl.Path(ff).exists()):
                print(f'That file \"{ff}\" does not appear to exist')
                raise IOError
        self.fuel=fuel

        self.core_h5m = core_h5m
        self.shim_rod_h5m = shim_rod_h5m
        self.control_rod_h5m = control_rod_h5m

        self.padding=padding
        try:
            iter(shim_rod_z)
            self.shim_rod_z=shim_rod_z
        except TypeError as e:
            self.shim_rod_z=[shim_rod_z]*3
        self.ctrl_rod_z=ctrl_rod_z

        self.operating_temp=operating_temp
        self.batches=batches
        self.particles=particles
        self.inactive=inactive

        self.model=None
        self.geometry=None
        self.materials=None
        self.settings=None
        self.tallies=openmc.Tallies()
        self.plots=None
        self.verbose=False

        self.verbose=False
        self.output_dir=output_dir

    def bld_materials(self):
        mats=create_materials(self.operating_temp)
        if self.fuel is not None:
            mats = [m for m in mats if m.name != 'salt']
            mats.append(self.fuel)
        self.materials=openmc.Materials(mats)

    def bld_geometry(self):
        if self.materials is None:
            self.bld_materials()
        helium=[m for m in self.materials if m.name=='helium'][0]
        #import dagmc-geometry defining the reactor core
        du=openmc.DAGMCUniverse(self.core_h5m, auto_geom_ids=True)
        
        self.bc=du.bounding_region()

        #shim rods
        control_rod_du=openmc.DAGMCUniverse(self.control_rod_h5m, auto_geom_ids=True)
        burst_rod_du = openmc,DAGMCUniverse(self.burst_rod_h5m, auto_geom_ids=True)

        dr=6.6675

        posBR=np.array( (-dr, 0,0, 4.64820+BRz) )
        posCR1=np.array( (dr*cos(pi/3),dr*sin(pi/3), 4.64820+CR1z) )
        posCR2=np.array( (dr*cos(-pi/3),dr*sin(-pi/3), 4.64820+CR2z) )

        BR_cyl=openmc.ZCylinder(r=2.54,x0=posBR[0],y0=posBR[1])
        CR1_cyl=openmc.ZCylinder(r=2.54,x0=posCR1[0],y0=posCR1[1])
        CR2_cyl=openmc.ZCylinder(r=2.54,x0=posCR2[0],y0=posCR2[1])

        BR_uppper=openmc.ZPlane(z0=4.64820+posBR[2])
        CR1_upper=openmc.ZPlane(z0=4.64820+posCR1[2])
        CR2_upper=openmc.ZPlane(z0=4.64820+posCR2[2])

        rod_lower = openmc.ZPlane(z0=1000)
        rod_cyl_top = openmc.ZPlane(z0=4.64820)

        BR=openmc.Cell(region=(-BR_cyl & -BR_upper & +rod_lower), fill=burst_rod_du)
        BR.translation=posBR
        BR_void=openmc.Cell(region=(-BR_cyl & +BR_upper & -rod_cyl_top), fill=helium)

        CR1=openmc.Cell(region=(-CR1_cyl & -CR1_upper & +rod_lower), fill=shim_rod_du)
        CR1.translation=posCR1
        CR1_void=openmc.Cell(region=(-CR1_cyl & +CR1_upper & -rod_cyl_top), fill=helium)

        CR2=openmc.Cell(region=(-CR2_cyl & -CR2_upper & +rod_lower), fill=shim_rod_du)
        CR2.translation=posCR2
        CR2_void=openmc.Cell(region=(-CR2_cyl & +CR2_upper & -rod_cyl_top), fill=helium)

        #core cell definition
        core_region=self.bc & ~BR.region & ~CR1.region & ~CR2.region
        core = openmc.Cell(region=core_region, fill=du)

        #define geometry
        root = openmc.Universe()
        root.add_cells([core,BR,BR_void,CR1,CR1_void,CR2, CR2_void])

        self.geometry = openmc.Geometry(root)

    def bld_settings(self):
        s=openmc.Settings(particles=int(self.particles), batches=self.batches)
        s.inactive=self.inactive
        s.max_lost_particles=1000
        s.source=self.bld_source()
        s.temperature={'method':'interpolation', 'range':[950,1000]}
        self.settings=s

    def bld_source(self):
        src = openmc.Source()
        src.space = openmc.stats.Box(lower_left=[-30,-30,0], upper_right=[30,30,100], only_fissionable=True)
        src.angle = openmc.stats.Isotropic()
        src.energy = openmc.stats.Watt()
        return src

    def add_nflux_meshxy_tally(self, dims=[256,256,1],ll=None, ur=None):
        if ll is None:
            ll=self.geometry.bounding_box()[0]
        if ur is None:
            ll=self.geometry.bounding_box()[1]
        meshxy=openmc.RegularMesh(name='meshxy')
        meshxy.n_dimensions=2
        meshxy.dimension=dims
        meshxy.lower_lef=ll
        meshxy.upper_right=ur
        flt=openmc.MeshFilter(meshxy)
        npf=openmc.ParticleFilter('neutron')
        tally=openmc.Tally()
        tally.filters=[flt,npf]
        tally.scores=['flux','fission']
        return tally

    def add_nflux_etall(self,erange=None):
        if erange is None:
            ebins=np.logspace(1,7,200)
        ef=openmc.EnergyFilter(ebins)
        tally=openmc.Tally(name='energy')
        tally.filters=[ef]
        tally.scores=['flux']
        return tally

    def bld_tallies(self):
        #if not specified add default tallies
        if self.tallies is None:
            self.tallies.append(self.add_nflux_meshxy_tally)
            self.tallies.append(self.add_nflux_energy_tally)

    def bld_plots(self):
        if self.geometry is None:
            self.bld_geometry()
        #if not specified add default plots
        if self.plots is None:
            colordict={m:c for m,c in zip(self.materials,it.cycle(cm['Paired'].colors))}
            if self.verbose:
                for k,v in colordict.items():
                    print(k.name,v)

            bb=self.geometry.bounding_box
            width=np.array([300,300,300])
            pixels=8192
            p1=openmc.Plot().from_geometry(self.geometry)
            p1.basis='xy'
            p1.width=width[:2]
            p1.origin=(0,0,0)
            p1.color_by='material'
            #p1.colors=colordict
            p1.pixels=(pixels,pixels)
            p1.filename='reactor_xy'

            p2=openmc.Plot().from_geometry(self.geometry)
            p2.basis='xz'
            p2.width=width[[0,2]]
            p2.origin=(0,0,0)
            p2.color_by='material'
            #p2.colors=colordict
            p2.pixels=(pixels,pixels)
            p2.filename='reactor_xz'

            p3=openmc.Plot().from_geometry(self.geometry)
            p3.basis='yz'
            p3.width=width[1:3]
            p3.origin=(0,0,0)
            p3.color_by='material'
            #p3.colors=colordict
            p3.pixels=(pixels,pixels)
            p3.filename='reactor_yz'
            self.plots=openmc.Plots([p1,p2,p3])

    def bld_model(self):
        self.bld_materials()
        self.bld_geometry()
        self.bld_tallies()
        if self.settings is None:
          self.bld_settings()
        self.model = openmc.Model(geometry=self.geometry, materials=self.materials, tallies=self.tallies, plots=self.plots, settings=self.settings)
        return self.model

    def keff_run(self):
        if self.model is None:
            self.bld_model()
        openmc.lib.init()

    def export_to_xml(self,cwd=None):
        if self.model is None:
            self.bld_model()
        if cwd is not None:
            pp=pl.Path(cwd)
            pp.mkdir(parents=True, exist_ok=True)
            self.model.cwd=cwd
        self.model.export_to_model_xml()

if __name__=='__main__':
    ARE=ARE_reactor(sys.argv[1],sys.argv[2],sys.argv[3])
    ARE.export_to_xml()
