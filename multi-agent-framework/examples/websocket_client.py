#!/usr/bin/env python3
"""
Example WebSocket Client - Real-time monitoring of multi-agent executions.

Demonstrates how to connect to the framework's WebSocket endpoint
and monitor execution progress in real-time.

Usage:
    python websocket_client.py <execution_id>

Prerequisites:
    - Framework API running on localhost:8000
    - WebSocket at ws://localhost:8000/ws/{execution_id}
"""

import asyncio
import json
import sys
import websockets
from datetime import datetime


class ExecutionMonitor:
    """Monitors execution progress via WebSocket."""

    def __init__(self, execution_id: str, host: str = "localhost", port: int = 8000):
        """
        Initialize monitor.

        Args:
            execution_id: The execution ID to monitor
            host: API server host
            port: API server port
        """
        self.execution_id = execution_id
        self.ws_url = f"ws://{host}:{port}/ws/{execution_id}"
        self.agent_status = {}
        self.current_phase = None

    async def connect(self):
        """Connect to WebSocket and start monitoring."""
        print(f"📡 Connecting to {self.ws_url}")
        print(f"⏳ Monitoring execution: {self.execution_id}\n")

        try:
            async with websockets.connect(self.ws_url) as websocket:
                print("✅ Connected to execution stream\n")

                # Send initial ping to get status
                await websocket.send(json.dumps({
                    "type": "ping"
                }))

                # Listen for messages
                async for message in websocket:
                    await self._handle_message(json.loads(message))

        except ConnectionRefusedError:
            print(f"❌ Failed to connect to {self.ws_url}")
            print("   Make sure the API server is running: uvicorn backend.api.main:app")
            sys.exit(1)

    async def _handle_message(self, msg: dict):
        """
        Handle incoming WebSocket message.

        Args:
            msg: Parsed JSON message
        """
        msg_type = msg.get("type", "unknown")
        timestamp = msg.get("timestamp", "")
        data = msg.get("data", {})

        if msg_type == "initial":
            self._print_initial_status(data)

        elif msg_type == "progress":
            self._print_progress(data)

        elif msg_type == "agent_update":
            self._print_agent_update(data)

        elif msg_type == "debate":
            self._print_debate(data)

        elif msg_type == "complete":
            self._print_completion(data)

        elif msg_type == "error":
            self._print_error(data)

        elif msg_type == "heartbeat":
            print(f"💓 Heartbeat @ {timestamp[:19]}")

        elif msg_type == "pong":
            print(f"🏓 Pong received @ {timestamp[:19]}")

        elif msg_type == "status":
            self._print_status_response(data)

        else:
            print(f"❓ Unknown message type: {msg_type}")
            print(f"   Data: {data}\n")

    def _print_initial_status(self, data: dict):
        """Print initial connection status."""
        status = data.get("status", "unknown")
        print(f"📋 Initial Status: {status}")
        print(f"   Message: {data.get('message', '')}\n")

    def _print_progress(self, data: dict):
        """Print progress update."""
        phase = data.get("phase", "")
        percentage = data.get("percentage", 0)
        message = data.get("message", "")

        self.current_phase = phase

        bar_filled = int(percentage / 5)
        bar = "█" * bar_filled + "░" * (20 - bar_filled)

        print(f"📊 Phase: {phase}")
        print(f"   Progress: [{bar}] {percentage}%")
        print(f"   {message}\n")

    def _print_agent_update(self, data: dict):
        """Print agent status update."""
        agent_name = data.get("agent_name", "Unknown")
        status = data.get("status", "unknown")
        output = data.get("output")

        self.agent_status[agent_name] = status

        status_emoji = {
            "running": "🔄",
            "completed": "✅",
            "failed": "❌",
            "pending": "⏳"
        }.get(status, "❓")

        print(f"{status_emoji} Agent: {agent_name} → {status}")

        if status == "completed" and output:
            print(f"   Output summary: {str(output)[:100]}...")

        print()

    def _print_debate(self, data: dict):
        """Print debate update."""
        round_num = data.get("round", 0)
        topic = data.get("topic", "Unknown")
        positions = data.get("positions", {})
        resolution = data.get("resolution")

        print(f"🎭 Debate Round {round_num}")
        print(f"   Topic: {topic}")

        for agent, position in positions.items():
            print(f"   • {agent}: {position[:80]}")

        if resolution:
            print(f"   ✨ Resolution: {resolution}")

        print()

    def _print_completion(self, data: dict):
        """Print completion message."""
        status = data.get("status", "unknown")
        final_output = data.get("final_output", {})
        tokens = data.get("total_tokens", 0)

        emoji = "🎉" if status == "completed" else "⚠️"

        print(f"\n{emoji} EXECUTION {status.upper()}")
        print(f"   Total Tokens Used: {tokens:,}")
        print(f"   Final Output: {str(final_output)[:200]}...")
        print()

    def _print_error(self, data: dict):
        """Print error message."""
        error = data.get("error", "Unknown error")
        details = data.get("details", "")

        print(f"❌ ERROR: {error}")
        if details:
            print(f"   Details: {details}")
        print()

    def _print_status_response(self, data: dict):
        """Print status query response."""
        print(f"📊 Current Status:")
        for key, value in data.items():
            print(f"   {key}: {value}")
        print()

    def print_summary(self):
        """Print execution summary."""
        print("\n" + "=" * 50)
        print("📈 EXECUTION SUMMARY")
        print("=" * 50)

        print("\nAgent Status:")
        for agent, status in self.agent_status.items():
            emoji = {
                "completed": "✅",
                "running": "🔄",
                "failed": "❌",
                "pending": "⏳"
            }.get(status, "❓")
            print(f"  {emoji} {agent}: {status}")

        if self.current_phase:
            print(f"\nLast Phase: {self.current_phase}")

        print("\n" + "=" * 50)


async def main():
    """Main entry point."""
    if len(sys.argv) < 2:
        print("Usage: python websocket_client.py <execution_id>")
        print("\nExample:")
        print("  python websocket_client.py 550e8400-e29b-41d4-a716-446655440000")
        sys.exit(1)

    execution_id = sys.argv[1]
    monitor = ExecutionMonitor(execution_id)

    try:
        await monitor.connect()
    except KeyboardInterrupt:
        print("\n\n⏹️ Monitoring stopped by user")
        monitor.print_summary()
    except Exception as e:
        print(f"\n❌ Error: {str(e)}")
        sys.exit(1)


if __name__ == "__main__":
    asyncio.run(main())
