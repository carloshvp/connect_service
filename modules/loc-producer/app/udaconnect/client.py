from __future__ import print_function
import logging
import grpc

import location_pb2
import location_pb2_grpc

def run():
    with grpc.insecure_channel("localhost:30003") as channel:
        stub = location_pb2_grpc.LocationServiceStub(channel)

        response = stub.Create(
            location_pb2.LocationMessage(person_id=99, latitude=100.01, longitude=10.01)
        )
        print(
            "Location received: "
            + str(response.person_id)
            + ","
            + str(response.latitude)
            + ","
            + str(response.longitude)
        )

if __name__ == "__main__":
    logging.basicConfig()
    run()