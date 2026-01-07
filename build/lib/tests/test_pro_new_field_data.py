import numpy as np
import ase
from ase.io import write
import os

def generate_water_molecule(with_noise=False):
    # 创建一个基本的水分子
    atoms = ase.Atoms('H2O', 
                      positions=[[0, 0, 0], 
                                 [0.95, 0, 0], 
                                 [0.95*np.cos(104.5*np.pi/180), 0.95*np.sin(104.5*np.pi/180), 0]])
    
    if with_noise:
        # 添加一些随机噪声到原子位置
        noise = np.random.normal(0, 0.1, (3, 3))
        atoms.positions += noise
    
    return atoms

def add_field_info(atoms):
    # 为每个原子添加随机的外场信息
    num_atoms = len(atoms)
    
    # 生成随机的矢量场 (3D向量)
    field_vector = np.random.uniform(-0.1, 0.1, (num_atoms, 3))
    
    # 生成随机的标量场
    field_scalar = np.random.uniform(0, 0.1, num_atoms)

    
    # 计算一个虚拟的能量和力 (仅用于演示)
    energy = np.random.uniform(-10, 10)
    forces = np.random.uniform(-1, 1, (num_atoms, 3))
    atoms.arrays['forces'] = forces  # 将forces作为数组添加到atoms对象
    # 将场信息添加到原子对象中
    atoms.arrays['field_vector'] = field_vector
    atoms.arrays['field_scalar'] = field_scalar

    return atoms, energy, forces

def generate_dataset(num_structures, filename):
    structures = []
    for _ in range(num_structures):
        atoms = generate_water_molecule(with_noise=True)
        atoms, energy, forces = add_field_info(atoms)
        
        # 将能量和力添加到原子对象的info字典中
        atoms.info['energy'] = energy
        
        # 添加field_vector和field_scalar到info字典中，以便在xyz文件中显示
        #atoms.info['field_vector'] = atoms.arrays['field_vector'].tolist()
        #atoms.info['field_scalar'] = atoms.arrays['field_scalar'].tolist()
        
        structures.append(atoms)
    
    # 保存为xyz文件
    write(filename, structures, format='extxyz')

# 生成训练集和测试集
generate_dataset(100, 'train_data.xyz')
generate_dataset(20, 'test_data.xyz')

print("数据集生成完成。")