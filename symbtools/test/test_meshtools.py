# -*- coding: utf-8 -*-
"""
Created on 2019-12-12 00:14:14

@author: Carsten Knoll
"""

import numpy as np
import matplotlib.pyplot as plt
import mpl_toolkits.mplot3d as a3

import symbtools.meshtools as met
import ipydex as ipd

import unittest


# noinspection PyShadowingNames,PyPep8Naming,PySetFunctionToLiteral
class TestHelperFuncs1(unittest.TestCase):

    def setUp(self):
        pass

    def test_absmax(self):
        l1 = [1, 2, 3]
        l2 = [-1, -2, -3]
        l3 = [1, 2, -3]

        self.assertEqual(met.absmax(*l1), 3)
        self.assertEqual(met.absmax(*l2), -3)
        self.assertEqual(met.absmax(*l3), -3)

    def test_modify_tuple(self):

        t1 = (3, 4.5, 10.7)

        self.assertEqual(met.modify_tuple(t1, 0, 1), (4, 4.5, 10.7))
        self.assertEqual(met.modify_tuple(t1, 1, 1), (3, 5.5, 10.7))
        self.assertEqual(met.modify_tuple(t1, 2, -1), (3, 4.5, 9.7))


class TestNode(unittest.TestCase):
    def setUp(self):
        xx = np.linspace(-4, 4, 9)
        yy = np.linspace(-4, 4, 9)

        XX, YY = mg = np.meshgrid(xx, yy, indexing="ij")

        met.create_nodes_from_mg(mg)


class TestGrid2d(unittest.TestCase):
    def setUp(self):
        xx = np.linspace(-4, 4, 9)
        yy = np.linspace(-4, 4, 9)

        XX, YY = mg = np.meshgrid(xx, yy, indexing="ij")

        self.mg = mg

    def test_create_cell(self):
        # met.create_nodes_from_mg(self.mg)
        grid = met.Grid(self.mg)

        self.assertEqual(grid.idx_edge_pairs, [(0, 1), (0, 2), (1, 3), (2, 3)])

        gc = met.GridCell(grid.ndb.all_nodes[:4], grid)

        childs1 = gc.make_childs()

        self.assertEqual(len(childs1), 4)
        expected_vertices = np.array([[-4., -4.], [-4., -3.5], [-3.5, -4.],  [-3.5, -3.5]])
        self.assertTrue(np.all(childs1[0].get_vertex_coords() == expected_vertices))

        childs2 = childs1[0].make_childs()

        self.assertEqual(childs1[0].child_cells, childs2)
        self.assertEqual(childs2[0].parent_cell, childs1[0])

        if 0:
            plt.plot(*grid.all_mg_points, '.')
            plot_cells2d([gc]+childs1+childs2, show=True)

    def _test_plot(self):
        # create images where each new cell is shown
        grid = met.Grid(self.mg)

        plt.plot(*grid.all_mg_points, '.')
        plt.savefig("tmp_0.png")
        for i, cell in enumerate(grid.cells):
            edges = np.array(cell.get_edge_coords())
            plt.plot(*edges.T)
            plt.savefig("tmp_{:03d}.png".format(i))

        ipd.IPS()


class TestGrid3d(unittest.TestCase):

    def setUp(self):
        xx = np.linspace(-4, 4, 9)
        yy = np.linspace(-4, 4, 9)
        zz = np.linspace(-4, 4, 9)

        mg = np.meshgrid(xx, yy, zz, indexing="ij")

        self.mg = mg

    def test_create_cells(self):
        grid = met.Grid(self.mg)

        self.assertEqual(grid.cells[0].vertex_nodes[0].coords, [-4.0, -4.0, -4.0])
        self.assertEqual(grid.cells[0].vertex_nodes[3].coords, [-4.0, -3.0, -3.0])

    def test_plot(self):
        # create images where each new cell is shown
        grid = met.Grid(self.mg)

        fig = plt.figure()
        ax = fig.add_subplot(1, 1, 1, projection='3d')

        all_points = np.array([arr.flat[:] for arr in grid.mg])
        ax.plot(*all_points, '.', ms=1, color="k")

        for i, cell in enumerate(grid.cells):
            edges = np.array(cell.get_edge_coords())

            vn = np.array([n.coords for n in cell.vertex_nodes])
            ax.scatter(*vn.T, "rs")

            for j, e in enumerate(edges):
                ax.plot(*e.T)
                # plt.savefig("tmp_{:03d}_{:02d}.png".format(i, j))
            plt.savefig("tmp_{:03d}.png".format(i))

            if i >= 10:
                break

        ipd.IPS()
        plt.show()


def plot_cells2d(cells, fname=None, show=False):
    for i, cell in enumerate(cells):
        edges = np.array(cell.get_edge_coords())
        plt.plot(*edges.T)
        if fname is not None:
            # expect something like "tmp_{:03d}.png"
            plt.savefig(fname.format(i))

    if show:
        plt.show()





