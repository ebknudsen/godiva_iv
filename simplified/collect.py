import h5py
import pathlib as pl

batches=100
sp=f'statepoint.{batches}.h5'
print("# model_type   case    k_eff    dk_eff")
for typ in ('full','in_parts'):
    for i in range(1,6):
        ssp=pl.Path(f'.attic_20092024/{typ}_case{i}') / sp
        f=h5py.File(ssp)
        print(typ,i,f['k_combined'][0],f['k_combined'][1])
        f.close()
    print()
