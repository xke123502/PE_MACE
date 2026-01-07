# PE_MACE

PE_MACE （Potential-embedded MACE) is a mace implementation of Explicit Electric Potential - Machine Learning Force Field (EEP-MLFF). This project extends the [mace](https://github.com/ACEsuit/mace.git) framework to support explicit electric potential modeling  as described in [Constant-Potential Machine Learning Molecular Dynamics Simulations Reveal Potential-Regulated Cu Cluster Formation on MoS$_2$](https://pubs.acs.org/doi/10.1021/acs.jpcc.4c08188).

## Installation

1. Follow the installation instructions for [mace](https://github.com/ACEsuit/mace.git)
2. Install PE_MACE:
   ```sh
   pip install .
   ```

## Usage

### Training
```sh
mace_run_train \
    --name="model" \
    --train_file="./train.xyz" \
    --valid_fraction=0.05 \
    --test_file="./test.xyz" \
    --E0s="average" \
    --energy_key="energy" \
    --forces_key="forces" \
    --model="MACE_Field" \
    --num_interactions=2 \
    --max_ell=2 \
    --hidden_irreps="64x0e+64x1o" \
    --num_cutoff_basis=5 \
    --correlation=2 \
    --r_max=5.0 \
    --batch_size=50 \
    --valid_batch_size=5 \
    --eval_interval=1 \
    --max_num_epochs=100 \
    --start_swa=15 \
    --swa_energy_weight=1000 \
    --ema \
    --ema_decay=0.99 \
    --amsgrad \
    --error_table="PerAtomRMSE" \
    --default_dtype="float64" \
    --swa \
    --device=cuda \
    --seed=1234 \
    --save_cpu \
    --field_scalar_key="field_scalar" \
    --scalar_field_irreps="1x0e" \
    --restart_latest 
```

### Evaluation

To evaluate your MACE model on an XYZ file, run the `mace_eval_configs` command:

```sh
mace_eval_configs \
    --configs="your_configs.xyz" \
    --model="your_model.model" \
    --output="./your_output.xyz"
```

### Constant Potential MLMD

To use PE-MACE model to run constant potential molecular dynamics (CP-MLMD):

1. Copy the following files to replace the normal MACE-LAMMPS version:
   - `PE_MACE/lammps_plugin/pe_mace_lammps/KOKKOS/*`
   - `PE_MACE/lammps_plugin/pe_mace_lammps/ML-MACE/*`

2. Build the plugin by following the instructions in `PE_MACE/lammps_plugin/pe_mace_lammps/build_set/cmake_install_mace.sh`

3. After training:
   - Run `mace_create_lammps_model your_model.model` to generate `your_model.model-lammps.pt`
   - For the LAMMPS input file, refer to `PE_MACE/lammps_plugin/pe_mace_lammps/example/md.in`
   - In the input file, the `pair_style mace no_domain_decomposition scalar -4.62` parameter represents the Fermi level. You need to convert this value to electric potential (U).

## References

If you use this code, please cite the following papers:

```text
@article{Zhou2025,
  title = {Constant-Potential Machine Learning Molecular Dynamics Simulations Reveal Potential-Regulated Cu Cluster Formation on MoS$_2$},
  author = {Zhou, Jingwen and Fu, Yunsong and Liu, Ling and Liu, Chungen},
  year = {2025},
  journal = {The Journal of Physical Chemistry C},
  volume = {129},
  number = {13},
  pages = {6414--6422},
  doi = {10.1021/acs.jpcc.4c08188},
}

@inproceedings{Batatia2022mace,
  title={{MACE}: Higher Order Equivariant Message Passing Neural Networks for Fast and Accurate Force Fields},
  author={Ilyes Batatia and David Peter Kovacs and Gregor N. C. Simm and Christoph Ortner and Gabor Csanyi},
  booktitle={Advances in Neural Information Processing Systems},
  editor={Alice H. Oh and Alekh Agarwal and Danielle Belgrave and Kyunghyun Cho},
  year={2022},
  url={https://openreview.net/forum?id=YPpSngE-ZU}
}

@misc{Batatia2022Design,
  title = {The Design Space of E(3)-Equivariant Atom-Centered Interatomic Potentials},
  author = {Batatia, Ilyes and Batzner, Simon and Kov{\'a}cs, D{\'a}vid P{\'e}ter and Musaelian, Albert and Simm, Gregor N. C. and Drautz, Ralf and Ortner, Christoph and Kozinsky, Boris and Cs{\'a}nyi, G{\'a}bor},
  year = {2022},
  number = {arXiv:2205.06643},
  eprint = {2205.06643},
  eprinttype = {arxiv},
  doi = {10.48550/arXiv.2205.06643},
  archiveprefix = {arXiv}
}
```

## Contact

If you have any questions, please contact us at jwzhou1998@gmail.com

## License

PE-MACE is published and distributed under the [MIT License](LICENSE.md).
