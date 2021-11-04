# coding: utf-8
import asyncio
import sys

import pytest
import numpy as np

import ray
from ray.cluster_utils import Cluster

avoid_multi_node = (sys.platform == "win32")


@pytest.mark.xfail("avoid_multi_node", reason="cluster requires multi-node")
@pytest.mark.asyncio
async def test_asyncio_cluster_wait():
    cluster = Cluster()
    head_node = cluster.add_node()
    cluster.add_node(resources={"OTHER_NODE": 100})

    ray.init(address=head_node.address)

    @ray.remote(num_cpus=0, resources={"OTHER_NODE": 1})
    def get_array():
        return np.random.random((192, 1080, 3)).astype(np.uint8)  # ~ 0.5MB

    object_ref = get_array.remote()

    await asyncio.wait_for(object_ref, timeout=10)

    ray.shutdown()
    cluster.shutdown()


if __name__ == "__main__":
    import pytest
    sys.exit(pytest.main(["-v", __file__]))
