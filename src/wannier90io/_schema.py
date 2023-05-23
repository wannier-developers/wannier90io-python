from __future__ import annotations
import typing

import pydantic


class UnitCell(pydantic.BaseModel):
    units: typing.Optional[str]
    a1: list
    a2: list
    a3: list


class DirectLattice(pydantic.BaseModel):
    a1: list
    a2: list
    a3: list


class ReciprocalLattice(pydantic.BaseModel):
    b1: list
    b2: list
    b3: list


class Atom(pydantic.BaseModel):
    species: str
    basis_vector: list


class Atoms(pydantic.BaseModel):
    units: typing.Optional[str]
    atoms: typing.List[Atom]


class Projections(pydantic.BaseModel):
    units: typing.Optional[str]
    projections: typing.List[str]


class Kpoints(pydantic.BaseModel):
    kpoints: typing.List[list]


class ExcludeBands(pydantic.BaseModel):
    exclude_bands: typing.Optional[typing.List[int]]


class WIN(pydantic.BaseModel):
    comments: typing.List[str]
    parameters: dict
    blocks: dict
    unit_cell_cart: typing.Optional[UnitCell]
    atoms_frac: typing.Optional[Atoms]
    atoms_cart: typing.Optional[Atoms]
    projections: Projections
    kpoints: Kpoints


class NNKP(pydantic.BaseModel):
    comments: typing.List[str]
    parameters: dict
    blocks: dict
    direct_lattice: DirectLattice
    reciprocal_lattice: ReciprocalLattice
    kpoints: Kpoints
    exclude_bands: ExcludeBands
