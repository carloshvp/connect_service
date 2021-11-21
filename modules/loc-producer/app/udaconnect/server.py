from concurrent import futures
from kafka import KafkaProducer
import logging
import grpc
import json

import location_pb2
import location_pb2_grpc

producer = KafkaProducer(bootstrap_servers="my-cluster-kafka-bootstrap.kafka.svc.cluster.local:9092")

class LocationServicer(location_pb2_grpc.LocationServiceServicer):
    def Create(self, request, context):
        location = {
            "person_id": int(request.person_id),
            "latitude": float(request.latitude),
            "longitude": float(request.longitude),
        }

        publish_message(location)

        return location_pb2.LocationMessage(**location)

def publish_message(message):
    request = json.dumps(message).encode()
    producer.send("Locations", request)
    producer.flush()

def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    location_pb2_grpc.add_LocationServiceServicer_to_server(LocationServicer(), server)
    server.add_insecure_port("[::]:5005")
    server.start()
    server.wait_for_termination()

if __name__ == "__main__":
    logging.basicConfig()
    serve()