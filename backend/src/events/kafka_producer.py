"""Kafka event producer for task operations.

Publishes events to Kafka topics when tasks are created, updated, or deleted.
Fire-and-forget pattern: API works even if Kafka is unavailable.
"""
import json
import logging
from datetime import datetime
from typing import Optional
from uuid import UUID

logger = logging.getLogger(__name__)


class TaskEventProducer:
    """Produces task lifecycle events to Kafka topics."""

    TOPIC = "todo.task.events"

    def __init__(self, bootstrap_servers: str = "localhost:9092"):
        self._bootstrap_servers = bootstrap_servers
        self._producer = None

    def _get_producer(self):
        if self._producer is None:
            try:
                from confluent_kafka import Producer
                self._producer = Producer({
                    "bootstrap.servers": self._bootstrap_servers,
                    "client.id": "todo-backend",
                    "acks": "all",
                })
            except Exception as e:
                logger.warning(f"Kafka producer init failed: {e}")
                raise
        return self._producer

    def _delivery_callback(self, err, msg):
        if err:
            logger.error(f"Kafka delivery failed: {err}")
        else:
            logger.info(f"Event delivered to {msg.topic()} [{msg.partition()}]")

    def publish_event(self, event_type: str, task_id: str, data: dict):
        """Publish a task event to Kafka (fire-and-forget)."""
        event = {
            "event_type": event_type,
            "task_id": str(task_id),
            "timestamp": datetime.utcnow().isoformat(),
            "data": data,
        }
        try:
            producer = self._get_producer()
            producer.produce(
                topic=self.TOPIC,
                key=str(task_id),
                value=json.dumps(event, default=str),
                callback=self._delivery_callback,
            )
            producer.flush(timeout=5)
        except Exception as e:
            logger.warning(f"Failed to publish event: {e}")

    def task_created(self, task_id: UUID, title: str):
        self.publish_event("task.created", str(task_id), {"title": title})

    def task_updated(self, task_id: UUID, changes: dict):
        self.publish_event("task.updated", str(task_id), {"changes": changes})

    def task_deleted(self, task_id: UUID):
        self.publish_event("task.deleted", str(task_id), {})
