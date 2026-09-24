"""
Autoencoder anomaly detector using PyTorch.
Trains on normal-only data; reconstruction error is the anomaly score.
"""

from __future__ import annotations

import numpy as np

from utils.config import get


class _Autoencoder:
    """Thin wrapper around a PyTorch autoencoder."""

    def __init__(self, input_dim: int, hidden_dims: list[int], lr: float):
        import torch
        import torch.nn as nn

        dims = [input_dim] + hidden_dims
        layers_enc, layers_dec = [], []
        for i in range(len(dims) - 1):
            layers_enc += [nn.Linear(dims[i], dims[i + 1]), nn.ReLU()]
        bottleneck = dims[-1]
        rev = list(reversed(dims))
        for i in range(len(rev) - 1):
            layers_dec += [nn.Linear(rev[i], rev[i + 1])]
            if i < len(rev) - 2:
                layers_dec.append(nn.ReLU())

        self.encoder = nn.Sequential(*layers_enc)
        self.decoder = nn.Sequential(*layers_dec)
        self.net = nn.Sequential(self.encoder, self.decoder)
        self.optimizer = torch.optim.Adam(self.net.parameters(), lr=lr)
        self.criterion = nn.MSELoss()
        self.torch = torch

    def fit(self, X: np.ndarray, epochs: int, batch_size: int) -> None:
        import torch
        self.net.train()
        tensor = torch.FloatTensor(X)
        dataset = torch.utils.data.TensorDataset(tensor)
        loader  = torch.utils.data.DataLoader(dataset, batch_size=batch_size, shuffle=True)
        for epoch in range(epochs):
            total_loss = 0.0
            for (batch,) in loader:
                self.optimizer.zero_grad()
                recon = self.net(batch)
                loss  = self.criterion(recon, batch)
                loss.backward()
                self.optimizer.step()
                total_loss += loss.item()
            if (epoch + 1) % 10 == 0:
                print(f"    epoch {epoch+1}/{epochs}  loss={total_loss/len(loader):.6f}")
        self.net.eval()

    def reconstruction_error(self, X: np.ndarray) -> np.ndarray:
        import torch
        with torch.no_grad():
            tensor = torch.FloatTensor(X)
            recon  = self.net(tensor)
            errors = ((recon - tensor) ** 2).mean(dim=1).numpy()
        return errors


def train(X_train: np.ndarray, y_train: np.ndarray | None, cfg: dict):
    """
    Fit autoencoder on normal-only rows.
    Returns (model, meta_dict).
    """
    try:
        import torch  # noqa: F401
    except ImportError:
        raise ImportError("torch is not installed. Run: pip install torch")

    hp = cfg.get("hyperparameters", {}).get("autoencoder", {})
    hidden_dims = list(hp.get("hidden_dims", [32, 16, 32]))
    epochs      = int(hp.get("epochs", 50))
    batch_size  = int(hp.get("batch_size", 256))
    lr          = float(hp.get("learning_rate", 0.001))

    X_fit = X_train[y_train == 0] if y_train is not None else X_train
    input_dim = X_fit.shape[1]

    print(f"  [Autoencoder] input_dim={input_dim}  hidden={hidden_dims}  epochs={epochs}")

    ae = _Autoencoder(input_dim=input_dim, hidden_dims=hidden_dims, lr=lr)
    ae.fit(X_fit, epochs=epochs, batch_size=batch_size)

    meta = {"hidden_dims": hidden_dims, "input_dim": input_dim}
    return ae, meta


def get_scores(model: _Autoencoder, X: np.ndarray, meta: dict) -> np.ndarray:
    """Higher reconstruction error = more anomalous."""
    return model.reconstruction_error(X)
