import argparse
import torch
import numpy as np
import os
import sys
# 将当前目录添加到Python路径
current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir)
sys.path.append(parent_dir)
from mace.tools import torch_geometric
from mace import data, tools
from mace.modules import models
from mace.calculators import MACECalculator
import ase
import ase.io

def parse_args():
    parser = argparse.ArgumentParser(description="MACE训练和模拟测试脚本")
    parser.add_argument("--train_file", type=str, default="./train_data.xyz", help="训练数据文件路径")
    parser.add_argument("--valid_file", type=str, default="./test_data.xyz", help="验证数据文件路径")
    parser.add_argument("--model_path", type=str, default="./mace_model.pt", help="保存模型的路径")
    parser.add_argument("--num_epochs", type=int, default=100, help="训练轮数")
    parser.add_argument("--batch_size", type=int, default=32, help="批次大小")
    parser.add_argument("--lr", type=float, default=1e-3, help="学习率")
    parser.add_argument("--field_vector_key", type=str, default="field_vector", help="矢量场数据的键名")
    parser.add_argument("--field_scalar_key", type=str, default="field_scalar", help="标量场数据的键名")
    return parser.parse_args()

def train(args):
    # 设置设备
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

    # 加载数据
    atoms_list = ase.io.read(args.train_file, index=":")
    train_configs = data.config_from_atoms_list(
        atoms_list,
        field_vector_key=args.field_vector_key,
        field_scalar_key=args.field_scalar_key
    )

    atoms_list = ase.io.read(args.valid_file, index=":")
    valid_configs = data.config_from_atoms_list(
        atoms_list,
        field_vector_key=args.field_vector_key,
        field_scalar_key=args.field_scalar_key
    )

    z_table = tools.AtomicNumberTable([1, 8])  # 根据您的数据调整原子类型

    train_data = [data.AtomicData.from_config(config, z_table=z_table, cutoff=5.0) for config in train_configs]
    valid_data = [data.AtomicData.from_config(config, z_table=z_table, cutoff=5.0) for config in valid_configs]

    train_loader = torch_geometric.data.DataLoader(train_data, batch_size=args.batch_size, shuffle=True)
    valid_loader = torch_geometric.data.DataLoader(valid_data, batch_size=args.batch_size)

    # 初始化模型
    model = models.MACE_Field(
        r_max=5.0,
        num_bessel=8,
        num_polynomial_cutoff=5,
        max_ell=2,
        interaction_cls=models.InteractionBlock,
        num_interactions=3,
        num_elements=10,
        hidden_irreps="32x0e + 32x1o",
        MLP_irreps="32x0e",
        atomic_energies=None,
        avg_num_neighbors=20,
        atomic_numbers=[1, 6, 7, 8],
        correlation=3,
        gate=torch.nn.SiLU(),
        vector_field_irreps="1x1o",
        scalar_field_irreps="1x0e"
    ).to(device)

    # 定义优化器和损失函数
    optimizer = torch.optim.Adam(model.parameters(), lr=args.lr)
    loss_fn = torch.nn.MSELoss()

    # 训练循环
    for epoch in range(args.num_epochs):
        model.train()
        total_loss = 0
        for batch in train_loader:
            batch = batch.to(device)
            optimizer.zero_grad()
            out = model(batch)
            loss = loss_fn(out['energy'], batch.energy) + loss_fn(out['forces'], batch.forces)
            loss.backward()
            optimizer.step()
            total_loss += loss.item()
        
        # 验证
        model.eval()
        valid_loss = 0
        with torch.no_grad():
            for batch in valid_loader:
                batch = batch.to(device)
                out = model(batch)
                valid_loss += loss_fn(out['energy'], batch.energy) + loss_fn(out['forces'], batch.forces)
        
        print(f"Epoch {epoch+1}/{args.num_epochs}, Train Loss: {total_loss/len(train_loader):.4f}, Valid Loss: {valid_loss/len(valid_loader):.4f}")

    # 保存模型
    torch.save(model.state_dict(), args.model_path)
    print(f"Model saved to {args.model_path}")

def simulate():
    # 加载模型
    model = models.MACE_Field(
        # ... 使用与训练时相同的参数 ...
    )
    model.load_state_dict(torch.load(args.model_path))
    
    # 创建MACE计算器
    calculator = MACECalculator(model=model, device="cpu")

    # 创建一个简单的分子系统
    atoms = ase.Atoms('H2O', positions=[[0, 0, 0], [0.95, 0, 0], [0.95*np.cos(104.5*np.pi/180), 0.95*np.sin(104.5*np.pi/180), 0]])
    
    # 设置外场
    field_vector = np.array([[0.1, 0, 0], [0.1, 0, 0], [0.1, 0, 0]])  # 假设有一个沿x方向的外场
    field_scalar = np.array([0.05, 0.05, 0.05])  # 假设有一个标量场

    # 将外场信息添加到原子对象中
    atoms.arrays['field_vector'] = field_vector
    atoms.arrays['field_scalar'] = field_scalar

    # 设置计算器
    atoms.calc = calculator

    # 计算能量和力
    energy = atoms.get_potential_energy()
    forces = atoms.get_forces()

    print(f"Energy: {energy} eV")
    print(f"Forces:\n{forces} eV/Å")

if __name__ == "__main__":
    if 'ipykernel' in sys.modules:
        # 在Jupyter环境中运行
        class Args:
            def __init__(self):
                self.train_file = "train_data.xyz"
                self.valid_file = "valid_data.xyz"
                self.model_path = "mace_model.pt"
                self.num_epochs = 100
                self.batch_size = 32
                self.lr = 1e-3
                self.field_vector_key = "field_vector"
                self.field_scalar_key = "field_scalar"
        args = Args()
    else:
        # 在命令行环境中运行
        args = parse_args()
    train(args)
    simulate()