###############################################################################
# Converting step files to h5m file to be read by openmc
###############################################################################
import numpy as np
import pathlib as pl
import os
import CAD_to_OpenMC.assembly as ab
import subprocess as sp
from datetime import datetime
from contextlib import redirect_stdout,redirect_stderr
###############################################################################

# inputs
#step_paths = [ 'step_files' / pl.Path('zpre_' + x + '.step') for x in ['control_rod','source','wout_fuel_v5','w_fuel_v5'][-2:]]
step_paths = [ 'step_files' / pl.Path('godiva_iv_simplified_'+x+'.step') for x in ['core','BR','CR'] ]
#step_paths = [ 'step_files' / pl.Path('godiva_iv_simplified_'+x+'.step') for x in ['case1','case2','case3','case4','case5'] ]
#step_paths.reverse()
h5m_paths = [ 'h5m_files2' / pl.Path(s.name).with_suffix('.h5m') for s in step_paths ]

tags={
    'control_r.*':'control_rod',
    'fuel_ring':'fuel_ring',
    'safety_block':'safety_block',
    'spindle.*':'ss303',
    'safety_block_base':'ss303',
    'clamp_support':'ss303',
    'clamp':'vascomax300',
    'subassembly_cover_plate':'sae4340',
    'support_pad_ring':'sae4340',
    'bearing_ring':'sae4340',
    'subassembly_plate_inner':'ISP',
    'burst_rod':'burst_rod',
    'mounting_plate':'aluminium',
}

#output
for sf,hf in zip(step_paths,h5m_paths):
  logfile=datetime.now().strftime(f"{hf.stem}_%Y%m%d_%H%M%S")
  with redirect_stdout(open(logfile+'.out','a')), redirect_stderr(open(logfile+'.err','a')):
    a=ab.Assembly([str(sf)], verbose=2)
    tol=0.2
    atol=0.2
    if not 'core' in str(sf):
        print('setting ic to helium')
        a.implicit_complement='helium'
    else:
        print('unsetting ic')
        a.implicit_complement=None
    a.threads=1
    ab.mesher_config['threads']=1
    ab.mesher_config['tolerance']=tol
    ab.mesher_config['angular_tolerance']=atol
    ab.mesher_config['verbose']=2
    a.verbose=2
    a.set_tag_delim('\s')
    a.run(merge=True,backend='db',h5m_filename=hf, tolerance=tol, angular_tolerance=atol)#, tags=tags)

    try:
        #pass
        sp.run(['check_watertight', hf])
    except IOError as e:
        print(f'Error: {str(e)}. No file {hf} could be opened')
