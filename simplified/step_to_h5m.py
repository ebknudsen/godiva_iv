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
step_paths = [ pl.Path('godiva_iv_simplified_'+x+'.step') for x in ['core','BR','CR'] ] 
#step_paths.reverse()
h5m_paths = [ 'h5m_files' / pl.Path(s.name).with_suffix('.h5m') for s in step_paths ]

#tags={
#    'Bottom\*':'steel',
#    'Fuel Ring':'fuel',
#    'Safety.*':'poison',
#}
# output
for sf,hf in zip(step_paths,h5m_paths):
  logfile=datetime.now().strftime(f"{hf.stem}_%Y%m%d_%H%M%S")
  with redirect_stdout(open(logfile+'.out','a')), redirect_stderr(open(logfile+'.err','a')):
    a=ab.Assembly([str(sf)], verbose=2)
    tol=0.2
    atol=0.2
    
    a.implit_complement=None
    a.threads=1
    ab.mesher_config['threads']=1
    ab.mesher_config['tolerance']=tol
    ab.mesher_config['angular_tolerance']=atol
    ab.mesher_config['verbose']=2
    a.run(merge=True,backend='db',h5m_filename=hf, tolerance=tol, angular_tolerance=atol)

    try:
        #pass
        sp.run(['check_watertight', hf])
    except IOError as e:
        print(f'Error: {str(e)}. No file {hf} could be opened')
