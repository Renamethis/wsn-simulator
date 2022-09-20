# This file provides unit-tests for the main functional models of the software
# Run: python3 unittests.py

import os
import sys

from sklearn import cluster

TEST_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_DIR = os.path.abspath(os.path.join(TEST_DIR, os.pardir))
PROJECT_DIR = os.path.abspath(os.path.join(PROJECT_DIR, os.pardir))
sys.path.insert(0, PROJECT_DIR)

from src.Network.Device import Device, State, Sensors
from src.Network.Cluster import DeviceCluster
from src.Network.Network import DeviceNetwork
import unittest
from random import random
from math import sqrt
TEST_POSITION = (500, 500)
TEST_VALUE = random()

class DeviceUnitTests(unittest.TestCase):
    
    def setUp(self):
        self.device = Device((TEST_POSITION))
        self.receiver = Device((TEST_POSITION))
    
    def test_init(self):
        self.assertEqual(self.device.get_pos(), TEST_POSITION)
        self.assertEqual(self.device.get_state(), State.ACTIVE)
        self.assertTrue(self.device.is_active())
        self.assertEqual(self.device.get_sensor_type(), Sensors.DEFAULT)
        
    def test_energy_consumption(self):
        energy = self.device.get_energy()
        self.device.consume(TEST_VALUE)
        self.assertEqual(self.device.get_energy(), energy - TEST_VALUE)

    def test_data_sending(self):
        device_energy = self.device.get_energy()
        receiver_energy = self.receiver.get_energy()
        self.device.send_data(receiver=self.receiver)
        self.assertLess(self.device.get_energy(), device_energy)
        self.assertLess(self.receiver.get_energy(), receiver_energy)
        
    def test_data_receiving(self):
        energy = self.device.get_energy()
        self.device.receive(TEST_VALUE)
        self.assertLess(self.device.get_energy(), energy)
    
    def test_device_aggregation(self):
        energy = self.device.get_energy()
        self.device.add_data_to_aggregation(TEST_VALUE + 1)
        self.device.aggregate()
        self.assertLess(self.device.get_energy(), energy)
        
    
    def test_device_stay(self):
        energy = self.device.get_energy()
        self.device.stay()
        self.assertLess(self.device.get_energy(), energy)
    
    def test_device_reset(self):
        self.device.set_state(State.DEAD)
        self.device.set_energy(0)
        self.device.reset()
        self.assertEqual(self.device.get_energy(), self.device.get_initial_energy())
        self.assertEqual(self.device.get_state(), State.ACTIVE)
        
    def test_calculate_distance(self):
        distance = self.device.calculate_distance(self.receiver)
        self.assertEqual(distance, 0)
        position = (TEST_VALUE, TEST_VALUE)
        self.receiver.set_pos(position)
        distance = sqrt((TEST_POSITION[0] - TEST_VALUE)**2 + (TEST_POSITION[1]- TEST_VALUE)**2)
        self.assertEqual(distance, self.device.calculate_distance(self.receiver))
        self.assertEqual(distance, self.device.calculate_distance_pos(position))

class ClusterUnitTests(unittest.TestCase):

    def setUp(self):
        devices = [Device(TEST_POSITION)]
        self.cluster = DeviceCluster(devices, devices[0], TEST_POSITION)

    def test_init(self):
        self.assertIs(self.cluster.get_head(), self.cluster.get_devices()[0])
        self.assertEqual(self.cluster.get_centroid(), TEST_POSITION)
        self.assertIsNotNone(self.cluster.get_color())
    
class NetworkUnitTests(unittest.TestCase):
    def setUp(self):
        devices = [Device(TEST_POSITION)]
        station = Device(TEST_POSITION)
        clusters = [DeviceCluster(devices=devices, head=devices[0], centroid=TEST_POSITION)]
        self.network = DeviceNetwork(clusters, station, TEST_POSITION)

    def test_init(self):
        self.assertEqual(self.network.get_map_size(), TEST_POSITION)
        self.assertIs(self.network.get_clusters()[0].get_head(), self.network.get_clusters()[0].get_devices()[0])
        self.assertEqual(self.network.get_station().get_pos(), TEST_POSITION)
        self.assertIsNotNone(self.network.get_color())

if __name__ == "__main__":
  unittest.main()